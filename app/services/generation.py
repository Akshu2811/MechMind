"""LLM answer generation: builds a context-grounded RAG prompt from
retrieved chunks and calls gpt-4o-mini via LangChain.

Instrumented with LangFuse: the LLM call is logged as a "generation"
observation (prompt, response, token usage, latency), and two LLM-as-judge
evaluators (groundedness, relevance) run afterwards -- concurrently via
asyncio.gather, since they're independent of each other and running them
sequentially just adds their latencies for no benefit -- and log their
scores back onto the trace.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.services.observability import observation, safe_score_current_trace
from app.services.retrieval import RetrievedChunk

logger = logging.getLogger(__name__)

GENERATION_MODEL = "gpt-4o-mini"

NO_INFO_MESSAGE = (
    "I don't have enough information in the provided documentation to answer this question."
)

SYSTEM_PROMPT = f"""You are MechMind, an assistant that answers industrial equipment \
maintenance questions strictly from the provided context excerpts.

Rules:
- Answer ONLY using the information in the context below. Never use outside or general \
knowledge, even if you know the answer.
- For every claim or step in your answer, cite the source it came from in the format \
[source_file, section_title].
- If the context does not contain enough information to answer the question, respond with \
exactly this sentence and nothing else: "{NO_INFO_MESSAGE}"
"""

GROUNDEDNESS_JUDGE_SYSTEM = """You are an evaluator checking whether an AI-generated answer is \
grounded in the provided context. Respond with ONLY a JSON object of the form \
{"score": <float 0.0-1.0>, "reasoning": "<one sentence>"}.
A score of 1.0 means every claim in the answer is directly supported by the context. A score \
of 0.0 means the answer relies entirely on information not present in the context \
(hallucinated / general knowledge). Judge only the answer against the context -- do not judge \
whether the answer is a good answer to any question."""

RELEVANCE_JUDGE_SYSTEM = """You are an evaluator checking whether an AI-generated answer \
actually addresses the user's question. Respond with ONLY a JSON object of the form \
{"score": <float 0.0-1.0>, "reasoning": "<one sentence>"}.
A score of 1.0 means the answer directly and completely addresses the question asked. A score \
of 0.0 means the answer is off-topic or fails to address the question. Judge only relevance to \
the question -- not whether the answer is factually grounded."""


class GenerationError(Exception):
    """Raised when the LLM generation call fails in a way that should
    surface to the API layer as a clear upstream-failure response."""


@dataclass
class GenerationResult:
    answer: str
    sources: list[RetrievedChunk]


def _format_context(chunks: list[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        section = c.section_title or "N/A"
        parts.append(f"[{i}] Source: {c.source_file} | Section: {section}\n{c.text}")
    return "\n\n".join(parts)


def _build_llm() -> ChatOpenAI:
    settings = get_settings()
    if not settings.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Generation requires an OpenAI key "
            "(set it in .env) since it uses ChatOpenAI/gpt-4o-mini."
        )
    return ChatOpenAI(model=GENERATION_MODEL, temperature=0, api_key=settings.OPENAI_API_KEY)


def _usage_details(response) -> dict[str, int] | None:
    usage = getattr(response, "usage_metadata", None)
    if not usage:
        return None
    return {
        "input": int(usage.get("input_tokens", 0)),
        "output": int(usage.get("output_tokens", 0)),
        "total": int(usage.get("total_tokens", 0)),
    }


def _messages_as_dicts(messages: list[BaseMessage]) -> list[dict[str, str]]:
    role_by_type = {"system": "system", "human": "user", "ai": "assistant"}
    return [{"role": role_by_type.get(m.type, m.type), "content": m.content} for m in messages]


async def generate_answer(question: str, chunks: list[RetrievedChunk]) -> GenerationResult:
    """Calls gpt-4o-mini with the retrieved chunks as context. `sources` on
    the result always lists every retrieved chunk (not just ones the model
    explicitly cited), so the API can show full citations regardless of how
    well the model followed the citation instruction.

    Raises `RuntimeError` if generation isn't configured (no API key) and
    `GenerationError` if the LLM call itself fails -- the API layer maps
    these to 503 and 502 respectively.
    """
    if not chunks:
        return GenerationResult(answer=NO_INFO_MESSAGE, sources=[])

    llm = _build_llm()
    context = _format_context(chunks)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion: {question}\n\n"
            "Answer the question using only the context above, with citations."
        ),
    ]

    t0 = time.perf_counter()
    with observation(
        "generation", as_type="generation", model=GENERATION_MODEL, input=_messages_as_dicts(messages)
    ) as gen:
        try:
            response = await llm.ainvoke(messages)
        except Exception as exc:
            logger.error(
                "generation LLM call failed: question=%r error=%s", question, exc, exc_info=True
            )
            gen.update(level="ERROR", status_message=str(exc))
            raise GenerationError(f"LLM generation call failed: {exc}") from exc

        answer = response.content if isinstance(response.content, str) else str(response.content)
        latency_ms = (time.perf_counter() - t0) * 1000
        gen.update(
            output=answer,
            usage_details=_usage_details(response),
            metadata={"latency_ms": round(latency_ms, 1)},
        )

    logger.info(
        "generation completed: question=%r chunk_count=%d latency_ms=%.1f",
        question, len(chunks), latency_ms,
    )

    await _run_evaluators(question=question, chunks=chunks, answer=answer, llm=llm)

    return GenerationResult(answer=answer, sources=chunks)


# ---------------------------------------------------------------------------
# LLM-as-judge evaluators
# ---------------------------------------------------------------------------


def _parse_judge_response(text: str) -> tuple[float, str]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
    try:
        data = json.loads(cleaned)
        score = float(data.get("score", 0.0))
        reasoning = str(data.get("reasoning", ""))
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0.0, f"Judge response could not be parsed: {text[:200]}"
    return max(0.0, min(1.0, score)), reasoning


async def _run_judge(
    name: str, system_prompt: str, user_prompt: str, llm: ChatOpenAI
) -> tuple[float, str] | None:
    """Runs a single judge call. Judges are an evaluation/observability
    side-effect, not part of the user-facing answer, so a judge failure is
    logged and skipped (returns None) rather than propagated -- it must
    never fail /ask."""
    judge_messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

    with observation(
        name, as_type="generation", model=GENERATION_MODEL, input=_messages_as_dicts(judge_messages)
    ) as gen:
        try:
            response = await llm.ainvoke(judge_messages)
        except Exception as exc:
            logger.warning("judge '%s' call failed; skipping this score.", name, exc_info=True)
            gen.update(level="ERROR", status_message=str(exc))
            return None
        text = response.content if isinstance(response.content, str) else str(response.content)
        score, reasoning = _parse_judge_response(text)
        gen.update(output=text, usage_details=_usage_details(response))

    return score, reasoning


async def _run_evaluators(
    question: str, chunks: list[RetrievedChunk], answer: str, llm: ChatOpenAI
) -> None:
    """Runs groundedness (does the answer stick to the retrieved context?)
    and relevance (does it address the question?) concurrently -- both are
    independent LLM calls, so running them sequentially only adds their
    latencies together for no benefit."""
    context = _format_context(chunks)
    t0 = time.perf_counter()

    groundedness_result, relevance_result = await asyncio.gather(
        _run_judge(
            "groundedness_judge",
            GROUNDEDNESS_JUDGE_SYSTEM,
            f"Context:\n{context}\n\nAnswer:\n{answer}",
            llm,
        ),
        _run_judge(
            "relevance_judge",
            RELEVANCE_JUDGE_SYSTEM,
            f"Question:\n{question}\n\nAnswer:\n{answer}",
            llm,
        ),
    )
    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info("evaluators completed: latency_ms=%.1f", latency_ms)

    if groundedness_result is not None:
        score, reasoning = groundedness_result
        safe_score_current_trace(
            name="groundedness", value=score, data_type="NUMERIC", comment=reasoning
        )
    if relevance_result is not None:
        score, reasoning = relevance_result
        safe_score_current_trace(
            name="relevance", value=score, data_type="NUMERIC", comment=reasoning
        )
