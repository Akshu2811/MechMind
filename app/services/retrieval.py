"""Vector search logic: embeds a query, searches Qdrant, and applies the
equipment-ID guarantee (see module docstring on `search`).
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass

from qdrant_client.http import models as qmodels

from app.services.ingestion import (
    COLLECTION_NAME,
    LOGS_CSV,
    EmbeddingProvider,
    get_qdrant_client,
)
from app.services.observability import observation

logger = logging.getLogger(__name__)


class RetrievalError(Exception):
    """Raised when retrieval (embedding or Qdrant) fails in a way that
    should surface to the API layer as a clear upstream-failure response."""


TOP_K = 10
MIN_MANUAL_CHUNKS = 3
# Alarm-type candidates (Section 4 diagnostic procedures especially) can rank
# well outside the top 8 of a manual-only vector search -- e.g. for "Pump-3
# overheating" the matching Section 4 diagnostic procedure ranks 11th. Pool
# needs to be wide enough that content-type re-ranking has something to work
# with, not just whatever the raw top-8 happened to catch.
MANUAL_CANDIDATE_POOL = 20

LOGS_SOURCE_FILE = LOGS_CSV.name

# Query-side signal for which "angle" of a manual the user is likely after.
# Matched against the query text to decide whether to prefer alarm/
# troubleshooting content (Section 3/4-style) or ambient/sizing/context
# content (Section 6-style) when filling the equipment-ID guarantee slots.
ALARM_INTENT_KEYWORDS = [
    "alarm", "trip", "fault", "code", "overheating", "critical", "warning",
    "triggered", "failed",
]
CONTEXT_INTENT_KEYWORDS = [
    "ambient", "installation", "sizing", "summer", "seasonal", "running hot",
    "capacity", "demand",
]


@dataclass
class RetrievedChunk:
    id: str
    text: str
    source_file: str
    section_title: str | None
    section_number: str | None
    log_id: str | None
    alarm_code: str | None
    score: float


# ---------------------------------------------------------------------------
# Equipment-ID detection
# ---------------------------------------------------------------------------

_equipment_ids_cache: set[str] | None = None


def _load_known_equipment_ids(client) -> set[str]:
    """Pulls the distinct `equipment_id` values off log-chunk payloads in
    Qdrant (rather than hardcoding "Pump-1", "Motor-2", etc.), so newly
    ingested equipment is picked up automatically without a code change."""
    ids: set[str] = set()
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            with_payload=["equipment_id"],
            with_vectors=False,
            limit=256,
            offset=offset,
        )
        for p in points:
            eid = (p.payload or {}).get("equipment_id")
            if eid:
                ids.add(eid)
        if offset is None:
            break
    return ids


def get_known_equipment_ids(client) -> set[str]:
    global _equipment_ids_cache
    if _equipment_ids_cache is None:
        _equipment_ids_cache = _load_known_equipment_ids(client)
    return _equipment_ids_cache


def detect_equipment_id(query: str, known_ids: set[str]) -> str | None:
    """Case-insensitive, word-boundary match against known equipment IDs.
    Word boundaries prevent e.g. "Motor-1" from matching inside a future
    "Motor-10"."""
    for eid in known_ids:
        if re.search(rf"\b{re.escape(eid)}\b", query, re.IGNORECASE):
            return eid
    return None


def equipment_type_for_id(equipment_id: str) -> str:
    return equipment_id.split("-")[0].lower()


# ---------------------------------------------------------------------------
# Content-type intent (alarm/troubleshooting vs ambient/context)
# ---------------------------------------------------------------------------


def _keyword_hits(query: str, keywords: list[str]) -> int:
    return sum(1 for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", query, re.IGNORECASE))


def classify_query_intent(query: str) -> str | None:
    """Returns "alarm", "context", or None (no clear signal / a tie)."""
    alarm_hits = _keyword_hits(query, ALARM_INTENT_KEYWORDS)
    context_hits = _keyword_hits(query, CONTEXT_INTENT_KEYWORDS)
    if alarm_hits > context_hits:
        return "alarm"
    if context_hits > alarm_hits:
        return "context"
    return None


def classify_chunk_content_type(section_number: str | None) -> str | None:
    """Maps a chunk's section_number to "alarm" (Section 3/4-style: alarm
    codes + troubleshooting) or "context" (Section 6-style: ambient/
    installation/sizing) -- confirmed structurally consistent across the
    pump, motor, and compressor manuals (each Section 6 opens with a
    "Purpose and Relationship to Section 3 / Section 4" bridge)."""
    if not section_number:
        return None
    prefix = section_number.split(".")[0]
    if prefix in ("3", "4"):
        return "alarm"
    if prefix == "6":
        return "context"
    return None


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


def _to_chunk(point) -> RetrievedChunk:
    payload = point.payload or {}
    return RetrievedChunk(
        id=str(point.id),
        text=payload.get("text", ""),
        source_file=payload.get("source_file", "?"),
        section_title=payload.get("section_title"),
        section_number=payload.get("section_number"),
        log_id=payload.get("log_id"),
        alarm_code=payload.get("alarm_code"),
        score=point.score,
    )


def search(query: str, top_k: int = TOP_K) -> list[RetrievedChunk]:
    """Embeds `query`, searches Qdrant, and returns the top `top_k` chunks.

    If the query names a specific piece of equipment (e.g. "Pump-3"), a
    plain top-k search tends to be dominated by maintenance-log entries for
    that equipment (they're numerous and textually close to the query),
    crowding out the equipment's manual sections. To fix that, when an
    equipment ID is detected we run a second query filtered to that
    equipment's manual chunks, merge it into the primary results
    (deduplicated by chunk id), and guarantee at least MIN_MANUAL_CHUNKS of
    the final result come from the manual -- evicting the lowest-scoring
    non-guaranteed chunks if needed to keep the total at top_k -- then
    re-sort everything by score for presentation.

    Which manual chunks fill those guaranteed slots is further biased (soft
    preference, not a hard filter) by query intent: an alarm/fault-sounding
    query prefers Section 3/4-style chunks, an ambient/sizing-sounding query
    prefers Section 6-style chunks. Non-preferred chunks aren't excluded --
    they just fall back in line behind preferred ones and still fill
    remaining slots by score, since a good answer can benefit from both
    angles.

    Wrapped in a LangFuse "retrieval" span logging the query, retrieved
    chunk count, top chunk scores, and latency. Embedding/Qdrant failures
    are raised as `RetrievalError` so the API layer can return a clear
    502 instead of leaking a stack trace.
    """
    t0 = time.perf_counter()
    with observation("retrieval", as_type="span", input={"query": query, "top_k": top_k}) as span:
        try:
            results = _search_impl(query, top_k)
        except RuntimeError:
            raise
        except RetrievalError as exc:
            latency_ms = (time.perf_counter() - t0) * 1000
            logger.error(
                "retrieval failed: query=%r latency_ms=%.1f error=%s",
                query, latency_ms, exc, exc_info=True,
            )
            span.update(level="ERROR", status_message=str(exc))
            raise

        latency_ms = (time.perf_counter() - t0) * 1000
        span.update(
            output={
                "retrieved_chunk_count": len(results),
                "top_scores": [round(c.score, 4) for c in results[:3]],
            },
            metadata={"latency_ms": round(latency_ms, 1)},
        )
        logger.info(
            "retrieval completed: query=%r top_k=%d chunk_count=%d latency_ms=%.1f",
            query, top_k, len(results), latency_ms,
        )
    return results


def _search_impl(query: str, top_k: int) -> list[RetrievedChunk]:
    try:
        embedder = EmbeddingProvider()
    except RuntimeError:
        raise
    except Exception as exc:
        raise RetrievalError(f"Failed to initialize embedding provider: {exc}") from exc

    try:
        vector = embedder.embed([query])[0]
    except Exception as exc:
        raise RetrievalError(f"Embedding request failed: {exc}") from exc

    try:
        client = get_qdrant_client()
        primary_points = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=top_k,
        ).points
        primary = [_to_chunk(p) for p in primary_points]

        known_ids = get_known_equipment_ids(client)
        equipment_id = detect_equipment_id(query, known_ids)
        if equipment_id is None:
            return primary

        equipment_type = equipment_type_for_id(equipment_id)
        manual_in_primary = [
            c for c in primary if c.source_file != LOGS_SOURCE_FILE
        ]

        if len(manual_in_primary) >= MIN_MANUAL_CHUNKS:
            return primary

        manual_points = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=MANUAL_CANDIDATE_POOL,
            query_filter=qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="equipment_type", match=qmodels.MatchValue(value=equipment_type)
                    ),
                ],
                must_not=[
                    qmodels.FieldCondition(
                        key="source_file", match=qmodels.MatchValue(value=LOGS_SOURCE_FILE)
                    ),
                ],
            ),
        ).points
        manual_candidates = [_to_chunk(p) for p in manual_points]
    except Exception as exc:
        raise RetrievalError(f"Qdrant query failed: {exc}") from exc

    existing_ids = {c.id for c in primary}
    new_manual = [c for c in manual_candidates if c.id not in existing_ids]

    candidate_pool = manual_in_primary + new_manual
    intent = classify_query_intent(query)
    if intent:
        candidate_pool.sort(
            key=lambda c: (classify_chunk_content_type(c.section_number) != intent, -c.score)
        )
    else:
        candidate_pool.sort(key=lambda c: -c.score)

    guaranteed_manual = candidate_pool[:MIN_MANUAL_CHUNKS]
    guaranteed_ids = {c.id for c in guaranteed_manual}

    others = [c for c in primary if c.id not in guaranteed_ids]
    others.sort(key=lambda c: c.score, reverse=True)

    slots_left = max(top_k - len(guaranteed_manual), 0)
    final = guaranteed_manual + others[:slots_left]
    final.sort(key=lambda c: c.score, reverse=True)
    return final
