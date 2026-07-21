"""Regulatory compliance checks for MechMind's seven-unit equipment fleet.

Reuses the same Qdrant-backed maintenance-log payload scan equipment_status.py
already performs -- no new database or ingestion path. The requirements this
module enforces are documented in data/manuals/regulatory_standards.md (ingested
through the same pipeline as the other manuals), but the two threshold tables
below are a small, explicitly-labeled config transcribed from that document
rather than parsed out of its ingested chunks at request time: these are fixed
regulatory constants known in full at doc-authoring time, and the deterministic
checks below need them to be reliable for date arithmetic, not subject to
silently breaking if the document's wording changes. The /ask RAG path is
unaffected -- a user asking "what's the pump inspection interval" still gets
it answered straight from the ingested document text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime

from app.services.equipment_status import (
    KNOWN_EQUIPMENT_IDS,
    _extract_resolved,
    _extract_severity,
    _fetch_log_chunk_payloads,
)

# Sourced from regulatory_standards.md Section 3.1 ("Required Inspection
# Intervals").
INSPECTION_INTERVAL_DAYS = {
    "pump": 90,
    "motor": 120,
    "compressor": 60,
}

# Sourced from regulatory_standards.md Section 4.1 ("Required Resolution
# Windows"). Keys are lowercased alarm severities.
RESOLUTION_SLA_HOURS = {
    "critical": 72,
    "safety": 24,
}

# Matches chunk_maintenance_log's fixed text template (ingestion.py):
# "... Downtime: {downtime_hours} hours. Resolved: {resolved}." Not already
# extracted anywhere else in the codebase (equipment_status.py only pulls
# severity/resolved/tag out of this same free text), so added here.
DOWNTIME_RE = re.compile(r"Downtime:\s*([\d.]+)\s*hours", re.IGNORECASE)


@dataclass
class ComplianceStatus:
    equipment_id: str
    equipment_type: str
    compliant: bool
    reasons: list[str] = field(default_factory=list)


def _extract_downtime_hours(text: str) -> float | None:
    m = DOWNTIME_RE.search(text)
    return float(m.group(1)) if m else None


def _equipment_type_of(equipment_id: str) -> str:
    return equipment_id.split("-")[0].lower()


def _check_inspection_interval(
    equipment_type: str, payloads: list[dict], today: date
) -> str | None:
    """Any log entry -- not just a dedicated "inspection" record type, since
    the CSV has no such type -- counts as an inspection-qualifying touchpoint
    per regulatory_standards.md Section 1.3."""
    if not payloads:
        return None

    last = max(payloads, key=lambda p: (p.get("date", ""), p.get("log_id", "")))
    last_date = datetime.strptime(last["date"], "%Y-%m-%d").date()
    days_ago = (today - last_date).days
    interval = INSPECTION_INTERVAL_DAYS[equipment_type]

    if days_ago > interval:
        return (
            f"Last inspection {days_ago} days ago ({last['date']}), exceeds the "
            f"{interval}-day requirement for {equipment_type}s."
        )
    return None


def _check_resolution_time(payloads: list[dict], today: date) -> str | None:
    """Evaluates every Critical/Safety log entry for the unit, not just the
    most recent one -- a unit can have one promptly-resolved incident and a
    separate still-open one at the same time. Still-unresolved entries are
    compared by elapsed time since logged (regulatory_standards.md Section
    4.3: an open Critical/Safety alarm is a live gap regardless of how old);
    resolved entries are compared by downtime_hours as the resolution-time
    proxy, since no separate resolution timestamp is recorded. Reports the
    single worst (largest-overage) violation if more than one exists."""
    violations: list[tuple[float, str]] = []

    for p in payloads:
        text = p.get("text", "")
        severity = (_extract_severity(text) or "").lower()
        threshold_hours = RESOLUTION_SLA_HOURS.get(severity)
        if threshold_hours is None:
            continue

        resolved = _extract_resolved(text)
        event_date = datetime.strptime(p["date"], "%Y-%m-%d").date()
        alarm_code = p.get("alarm_code", "?")
        log_id = p.get("log_id", "?")

        if resolved is False:
            days_open = (today - event_date).days
            elapsed_hours = days_open * 24
            if elapsed_hours > threshold_hours:
                violations.append((
                    elapsed_hours - threshold_hours,
                    f"{alarm_code} ({severity.capitalize()}, {log_id}) logged {days_open} "
                    f"day{'s' if days_open != 1 else ''} ago and is still unresolved, "
                    f"exceeding the {threshold_hours}-hour resolution requirement.",
                ))
        elif resolved is True:
            downtime = _extract_downtime_hours(text)
            if downtime is not None and downtime > threshold_hours:
                violations.append((
                    downtime - threshold_hours,
                    f"{alarm_code} ({severity.capitalize()}, {log_id}) took {downtime:.1f} "
                    f"hours to resolve, exceeding the {threshold_hours}-hour resolution "
                    f"requirement.",
                ))

    if not violations:
        return None
    violations.sort(key=lambda v: v[0], reverse=True)
    return violations[0][1]


def get_compliance_status(today: date | None = None) -> list[ComplianceStatus]:
    today = today or date.today()
    payloads = _fetch_log_chunk_payloads()

    grouped: dict[str, list[dict]] = {}
    for p in payloads:
        eid = p.get("equipment_id")
        if eid:
            grouped.setdefault(eid, []).append(p)

    results: list[ComplianceStatus] = []
    for eid in KNOWN_EQUIPMENT_IDS:
        equipment_type = _equipment_type_of(eid)
        unit_payloads = grouped.get(eid, [])

        reasons = []
        inspection_reason = _check_inspection_interval(equipment_type, unit_payloads, today)
        if inspection_reason:
            reasons.append(inspection_reason)
        resolution_reason = _check_resolution_time(unit_payloads, today)
        if resolution_reason:
            reasons.append(resolution_reason)

        results.append(
            ComplianceStatus(
                equipment_id=eid,
                equipment_type=equipment_type,
                compliant=not reasons,
                reasons=reasons,
            )
        )

    return results
