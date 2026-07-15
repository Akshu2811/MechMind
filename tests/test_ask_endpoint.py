"""Tests for the /ask endpoint's request validation and error handling.

Uses FastAPI's TestClient with `app.api.routes.search` / `generate_answer`
mocked out -- no real Qdrant, OpenAI, or LangFuse calls are made.
"""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.generation import GenerationError, GenerationResult
from app.services.retrieval import RetrievalError, RetrievedChunk

client = TestClient(app)


class _FakeSpan:
    def update(self, *args, **kwargs) -> None:
        pass


@contextmanager
def _fake_observation(name, **kwargs):
    yield _FakeSpan()


@pytest.fixture(autouse=True)
def _no_real_langfuse_calls(monkeypatch):
    """Every test in this file goes through routes.py's `observation`/
    `safe_flush`; replace them with no-ops so tests never hit the network."""
    monkeypatch.setattr("app.api.routes.observation", _fake_observation)
    monkeypatch.setattr("app.api.routes.safe_flush", lambda: None)


def _fake_chunk(i: int = 1) -> RetrievedChunk:
    return RetrievedChunk(
        id=f"chunk-{i}",
        text=f"Chunk {i} body text.",
        source_file="pump_manual.md",
        section_title="4.2 Bearing Temperature High",
        section_number="4.2",
        score=0.9,
    )


# ---------------------------------------------------------------------------
# Request validation
# ---------------------------------------------------------------------------


def test_ask_empty_question_returns_400():
    resp = client.post("/ask", json={"question": ""})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_ask_whitespace_only_question_returns_400():
    resp = client.post("/ask", json={"question": "     "})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_ask_excessively_long_question_returns_400():
    resp = client.post("/ask", json={"question": "a" * 2001})
    assert resp.status_code == 400
    assert "too long" in resp.json()["detail"].lower()


def test_ask_max_length_question_is_accepted(monkeypatch):
    monkeypatch.setattr("app.api.routes.search", lambda q: [])
    resp = client.post("/ask", json={"question": "a" * 2000})
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Retrieval failure handling
# ---------------------------------------------------------------------------


def test_ask_retrieval_failure_returns_502(monkeypatch):
    def _raise(question: str):
        raise RetrievalError("Qdrant query failed: connection refused")

    monkeypatch.setattr("app.api.routes.search", _raise)

    resp = client.post("/ask", json={"question": "Why is Pump-3 overheating?"})

    assert resp.status_code == 502
    assert "retrieval failed" in resp.json()["detail"].lower()


def test_ask_retrieval_misconfigured_returns_503(monkeypatch):
    def _raise(question: str):
        raise RuntimeError("No embedding provider configured.")

    monkeypatch.setattr("app.api.routes.search", _raise)

    resp = client.post("/ask", json={"question": "Why is Pump-3 overheating?"})

    assert resp.status_code == 503
    assert "not configured" in resp.json()["detail"].lower()


def test_ask_no_chunks_returns_no_info_message(monkeypatch):
    monkeypatch.setattr("app.api.routes.search", lambda q: [])

    resp = client.post("/ask", json={"question": "What is the capital of France?"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["retrieved_chunk_count"] == 0
    assert body["sources"] == []
    assert "no relevant information" in body["answer"].lower()


# ---------------------------------------------------------------------------
# Generation failure handling
# ---------------------------------------------------------------------------


def test_ask_generation_failure_returns_502(monkeypatch):
    monkeypatch.setattr("app.api.routes.search", lambda q: [_fake_chunk()])
    monkeypatch.setattr(
        "app.api.routes.generate_answer",
        AsyncMock(side_effect=GenerationError("LLM generation call failed: timeout")),
    )

    resp = client.post("/ask", json={"question": "Why is Pump-3 overheating?"})

    assert resp.status_code == 502
    assert "answer generation failed" in resp.json()["detail"].lower()


def test_ask_generation_misconfigured_returns_503(monkeypatch):
    monkeypatch.setattr("app.api.routes.search", lambda q: [_fake_chunk()])
    monkeypatch.setattr(
        "app.api.routes.generate_answer",
        AsyncMock(side_effect=RuntimeError("OPENAI_API_KEY is not set.")),
    )

    resp = client.post("/ask", json={"question": "Why is Pump-3 overheating?"})

    assert resp.status_code == 503
    assert "not configured" in resp.json()["detail"].lower()


# ---------------------------------------------------------------------------
# Happy path (fully mocked -- no real Qdrant/OpenAI calls)
# ---------------------------------------------------------------------------


def test_ask_happy_path_returns_200(monkeypatch):
    chunk = _fake_chunk()
    monkeypatch.setattr("app.api.routes.search", lambda q: [chunk])
    monkeypatch.setattr(
        "app.api.routes.generate_answer",
        AsyncMock(
            return_value=GenerationResult(
                answer="Check bearing temperature per section 4.2 [1, pump_manual.md].",
                sources=[chunk],
            )
        ),
    )

    resp = client.post("/ask", json={"question": "Why is Pump-3 overheating?"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["retrieved_chunk_count"] == 1
    assert body["sources"][0]["source_file"] == "pump_manual.md"
    assert "bearing temperature" in body["answer"].lower()
