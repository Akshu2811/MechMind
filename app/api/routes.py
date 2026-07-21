import logging
import time

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AskRequest,
    AskResponse,
    EquipmentStatusItem,
    EquipmentStatusResponse,
    KnowledgeGraphResponse,
    RecentActivityItem,
    RecentActivityResponse,
    SourceInfo,
)
from app.services.equipment_status import get_equipment_status, get_recent_activity
from app.services.generation import GENERATION_MODEL, GenerationError, generate_answer
from app.services.knowledge_graph import get_knowledge_graph
from app.services.observability import observation, safe_flush
from app.services.retrieval import RetrievalError, search

logger = logging.getLogger(__name__)

router = APIRouter()

MAX_QUESTION_LENGTH = 2000


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    if len(question) > MAX_QUESTION_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Question is too long ({len(question)} characters); "
                f"max is {MAX_QUESTION_LENGTH}."
            ),
        )

    t0 = time.perf_counter()
    try:
        with observation("ask", as_type="span", input={"question": question}) as root:
            try:
                chunks = search(question)
            except RuntimeError as exc:
                logger.error("retrieval misconfigured: %s", exc, exc_info=True)
                root.update(level="ERROR", status_message=str(exc))
                raise HTTPException(
                    status_code=503, detail=f"Retrieval service is not configured: {exc}"
                ) from exc
            except RetrievalError as exc:
                logger.error(
                    "retrieval failed: question=%r error=%s", question, exc, exc_info=True
                )
                root.update(level="ERROR", status_message=str(exc))
                raise HTTPException(status_code=502, detail=f"Retrieval failed: {exc}") from exc

            if not chunks:
                answer = "No relevant information was found in the knowledge base for this question."
                latency_ms = (time.perf_counter() - t0) * 1000
                root.update(output={"answer": answer}, metadata={"retrieved_chunk_count": 0})
                logger.info(
                    "ask completed: question=%r chunk_count=0 latency_ms=%.1f",
                    question, latency_ms,
                )
                return AskResponse(
                    answer=answer,
                    sources=[],
                    retrieved_chunk_count=0,
                    latency_ms=round(latency_ms, 1),
                )

            try:
                result = await generate_answer(question, chunks)
            except RuntimeError as exc:
                logger.error("generation misconfigured: %s", exc, exc_info=True)
                root.update(level="ERROR", status_message=str(exc))
                raise HTTPException(
                    status_code=503, detail=f"Generation service is not configured: {exc}"
                ) from exc
            except GenerationError as exc:
                logger.error(
                    "generation failed: question=%r error=%s", question, exc, exc_info=True
                )
                root.update(level="ERROR", status_message=str(exc))
                raise HTTPException(
                    status_code=502, detail=f"Answer generation failed: {exc}"
                ) from exc

            sources = [
                SourceInfo(
                    source_file=c.source_file,
                    section_title=c.section_title,
                    log_id=c.log_id,
                    alarm_code=c.alarm_code,
                    score=c.score,
                )
                for c in result.sources
            ]
            latency_ms = (time.perf_counter() - t0) * 1000
            root.update(
                output={"answer": result.answer},
                metadata={"retrieved_chunk_count": len(chunks), "latency_ms": round(latency_ms, 1)},
            )
            logger.info(
                "ask completed: question=%r chunk_count=%d latency_ms=%.1f",
                question, len(chunks), latency_ms,
            )
            return AskResponse(
                answer=result.answer,
                sources=sources,
                retrieved_chunk_count=len(chunks),
                groundedness=result.groundedness,
                relevance=result.relevance,
                latency_ms=round(latency_ms, 1),
                model=GENERATION_MODEL,
            )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(
            "unexpected error handling /ask: question=%r error=%s", question, exc, exc_info=True
        )
        raise HTTPException(
            status_code=502, detail="An unexpected error occurred while processing the request."
        ) from exc
    finally:
        safe_flush()


@router.get("/equipment/status", response_model=EquipmentStatusResponse)
async def equipment_status() -> EquipmentStatusResponse:
    units = get_equipment_status()
    return EquipmentStatusResponse(
        units=[
            EquipmentStatusItem(
                equipment_id=u.equipment_id,
                equipment_tag=u.equipment_tag,
                last_alarm_code=u.last_alarm_code,
                last_event_date=u.last_event_date,
                days_ago=u.days_ago,
                resolved=u.resolved,
                severity=u.severity,
                status=u.status,
            )
            for u in units
        ]
    )


@router.get("/knowledge-graph", response_model=KnowledgeGraphResponse)
async def knowledge_graph(equipment: str | None = None) -> KnowledgeGraphResponse:
    data = get_knowledge_graph(equipment)
    return KnowledgeGraphResponse(nodes=data["nodes"], edges=data["edges"])


@router.get("/equipment/recent-activity", response_model=RecentActivityResponse)
async def recent_activity() -> RecentActivityResponse:
    entries = get_recent_activity(limit=5)
    return RecentActivityResponse(
        entries=[
            RecentActivityItem(
                equipment_id=e.equipment_id,
                alarm_code=e.alarm_code,
                date=e.date,
                days_ago=e.days_ago,
                resolved=e.resolved,
            )
            for e in entries
        ]
    )
