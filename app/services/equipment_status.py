"""Equipment status summary for the operator UI.

Queries Qdrant for log-type chunk payloads rather than reading
maintenance_logs.csv off disk -- data/ is excluded from the production
Docker image (see Dockerfile: only `app` is copied in), so a local-file
read here works locally but breaks on Render. This reuses the same
Qdrant client/collection ingestion.py already writes to.

`equipment_tag` and `resolved` aren't stored as their own payload fields
(chunk_maintenance_log in ingestion.py only sets source_file/equipment_id/
alarm_code/date/log_id/equipment_type) -- they're pulled back out of the
chunk's free-text `text` field via two regexes matching that function's
fixed text template, rather than changing the ingested schema.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import date, datetime

from qdrant_client.http import models as qmodels

from app.services.ingestion import COLLECTION_NAME, LOGS_CSV, get_qdrant_client

logger = logging.getLogger(__name__)

LOGS_SOURCE_FILE = LOGS_CSV.name

KNOWN_EQUIPMENT_IDS = [
    "Pump-1",
    "Pump-2",
    "Pump-3",
    "Motor-1",
    "Motor-2",
    "Compressor-1",
    "Compressor-2",
]

# A resolved event older than this is considered settled (green); anything
# unresolved, or resolved more recently than this, is still worth an
# operator's attention (amber).
RESOLVED_STALE_DAYS = 14

# Matches chunk_maintenance_log's fixed text template (ingestion.py):
# "Log {log_id} -- {equipment_id} ({equipment_tag}) on {date}: ..."
TAG_RE = re.compile(r"^Log\s+\S+\s+--\s+\S+\s+\(([^)]+)\)")
# "... Downtime: {downtime_hours} hours. Resolved: {resolved}."
RESOLVED_RE = re.compile(r"Resolved:\s*(yes|no)\b", re.IGNORECASE)


@dataclass
class EquipmentStatus:
    equipment_id: str
    equipment_tag: str | None
    last_alarm_code: str | None
    last_event_date: str | None
    days_ago: int | None
    resolved: bool | None
    status: str


def _fetch_log_chunk_payloads() -> list[dict]:
    """Scrolls every log-chunk payload (source_file == maintenance_logs.csv)
    out of Qdrant. Log chunks number in the low hundreds at most, so a
    couple of paginated scroll calls comfortably cover the whole set --
    same pagination pattern retrieval.py uses for equipment-ID discovery."""
    client = get_qdrant_client()
    payloads: list[dict] = []
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="source_file", match=qmodels.MatchValue(value=LOGS_SOURCE_FILE)
                    )
                ]
            ),
            with_payload=True,
            with_vectors=False,
            limit=256,
            offset=offset,
        )
        payloads.extend(p.payload or {} for p in points)
        if offset is None:
            break
    return payloads


def _sort_key(payload: dict) -> tuple[str, str]:
    """(date, log_id). Several log entries can share a date (e.g. Pump-3 had
    three on 2026-07-07), and `date` alone can't break that tie the same way
    twice -- Qdrant doesn't guarantee scroll order matches CSV row order the
    way plain file iteration did. `log_id` (LOG-0001, LOG-0002, ...) is
    zero-padded and assigned in the same chronological order as the source
    CSV rows, so sorting by it too resolves same-day ties deterministically
    and picks the actual last event of the day, not just whichever one the
    scroll happened to return first."""
    return payload.get("date", ""), payload.get("log_id", "")


def _latest_payload_by_equipment() -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for payload in _fetch_log_chunk_payloads():
        eid = payload.get("equipment_id")
        if not eid:
            continue
        if eid not in latest or _sort_key(payload) > _sort_key(latest[eid]):
            latest[eid] = payload
    return latest


def _extract_tag(text: str) -> str | None:
    m = TAG_RE.match(text)
    return m.group(1) if m else None


def _extract_resolved(text: str) -> bool | None:
    m = RESOLVED_RE.search(text)
    return m.group(1).lower() == "yes" if m else None


def get_equipment_status(today: date | None = None) -> list[EquipmentStatus]:
    today = today or date.today()
    latest = _latest_payload_by_equipment()

    results: list[EquipmentStatus] = []
    for eid in KNOWN_EQUIPMENT_IDS:
        payload = latest.get(eid)
        if payload is None:
            results.append(
                EquipmentStatus(
                    equipment_id=eid,
                    equipment_tag=None,
                    last_alarm_code=None,
                    last_event_date=None,
                    days_ago=None,
                    resolved=None,
                    status="amber",
                )
            )
            continue

        text = payload.get("text", "")
        event_date = datetime.strptime(payload["date"], "%Y-%m-%d").date()
        days_ago = (today - event_date).days
        resolved = _extract_resolved(text)
        status = "green" if resolved and days_ago > RESOLVED_STALE_DAYS else "amber"

        results.append(
            EquipmentStatus(
                equipment_id=eid,
                equipment_tag=_extract_tag(text),
                last_alarm_code=payload.get("alarm_code"),
                last_event_date=payload["date"],
                days_ago=days_ago,
                resolved=resolved,
                status=status,
            )
        )

    return results
