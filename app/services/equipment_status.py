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

# A resolved event older than this is considered settled (green); resolved
# but more recent than this is still amber. Unresolved events escalate to
# red only if their severity is Critical/Safety -- an unresolved Warning
# stays amber rather than crying wolf.
RESOLVED_STALE_DAYS = 10
RED_SEVERITIES = {"critical", "safety"}
# Red is driven by *any* unresolved Critical/Safety event in this window, not
# just the single latest log row -- a unit's most recent entry can be a minor
# resolved warning while an older-but-still-open critical issue is sitting
# unresolved a few weeks back, and that shouldn't get masked.
RED_LOOKBACK_DAYS = 30

# Matches chunk_maintenance_log's fixed text template (ingestion.py):
# "Log {log_id} -- {equipment_id} ({equipment_tag}) on {date}: ..."
TAG_RE = re.compile(r"^Log\s+\S+\s+--\s+\S+\s+\(([^)]+)\)")
# "... Alarm {alarm_code} ({severity}). Technician notes: ..."
SEVERITY_RE = re.compile(r"Alarm\s+\S+\s+\(([^)]+)\)")
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
    severity: str | None
    status: str


@dataclass
class RecentActivityEntry:
    equipment_id: str
    alarm_code: str | None
    date: str
    days_ago: int
    resolved: bool | None


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


def _group_payloads_by_equipment(payloads: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for payload in payloads:
        eid = payload.get("equipment_id")
        if not eid:
            continue
        groups.setdefault(eid, []).append(payload)
    return groups


def _extract_tag(text: str) -> str | None:
    m = TAG_RE.match(text)
    return m.group(1) if m else None


def _extract_resolved(text: str) -> bool | None:
    m = RESOLVED_RE.search(text)
    return m.group(1).lower() == "yes" if m else None


def _extract_severity(text: str) -> str | None:
    m = SEVERITY_RE.search(text)
    return m.group(1) if m else None


def _has_recent_unresolved_critical(payloads: list[dict], today: date) -> bool:
    for payload in payloads:
        date_str = payload.get("date")
        if not date_str:
            continue
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if (today - event_date).days > RED_LOOKBACK_DAYS:
            continue
        text = payload.get("text", "")
        if _extract_resolved(text) is False and (_extract_severity(text) or "").lower() in RED_SEVERITIES:
            return True
    return False


def _classify(resolved: bool | None, days_ago: int, has_recent_unresolved_critical: bool) -> str:
    if has_recent_unresolved_critical:
        return "red"
    if resolved and days_ago > RESOLVED_STALE_DAYS:
        return "green"
    return "amber"


def get_equipment_status(today: date | None = None) -> list[EquipmentStatus]:
    today = today or date.today()
    grouped = _group_payloads_by_equipment(_fetch_log_chunk_payloads())

    results: list[EquipmentStatus] = []
    for eid in KNOWN_EQUIPMENT_IDS:
        unit_payloads = grouped.get(eid, [])
        if not unit_payloads:
            results.append(
                EquipmentStatus(
                    equipment_id=eid,
                    equipment_tag=None,
                    last_alarm_code=None,
                    last_event_date=None,
                    days_ago=None,
                    resolved=None,
                    severity=None,
                    status="amber",
                )
            )
            continue

        payload = max(unit_payloads, key=_sort_key)
        text = payload.get("text", "")
        event_date = datetime.strptime(payload["date"], "%Y-%m-%d").date()
        days_ago = (today - event_date).days
        resolved = _extract_resolved(text)
        severity = _extract_severity(text)
        status = _classify(
            resolved, days_ago, _has_recent_unresolved_critical(unit_payloads, today)
        )

        results.append(
            EquipmentStatus(
                equipment_id=eid,
                equipment_tag=_extract_tag(text),
                last_alarm_code=payload.get("alarm_code"),
                last_event_date=payload["date"],
                days_ago=days_ago,
                resolved=resolved,
                severity=severity,
                status=status,
            )
        )

    return results


def get_recent_activity(limit: int = 5, today: date | None = None) -> list[RecentActivityEntry]:
    """Most recent log entries across all units, newest first -- feeds the
    UI's "recent activity" strip. Reuses the same Qdrant-backed payload scan
    as get_equipment_status() rather than a separate data path."""
    today = today or date.today()
    payloads = sorted(_fetch_log_chunk_payloads(), key=_sort_key, reverse=True)

    entries: list[RecentActivityEntry] = []
    for payload in payloads[:limit]:
        event_date = datetime.strptime(payload["date"], "%Y-%m-%d").date()
        entries.append(
            RecentActivityEntry(
                equipment_id=payload.get("equipment_id", "?"),
                alarm_code=payload.get("alarm_code"),
                date=payload["date"],
                days_ago=(today - event_date).days,
                resolved=_extract_resolved(payload.get("text", "")),
            )
        )
    return entries
