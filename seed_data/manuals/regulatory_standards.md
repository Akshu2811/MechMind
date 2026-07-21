# MechMind Site Regulatory Compliance Standard

## Inspection Intervals & Alarm Resolution Requirements

**Covering All Units: Pump-1/2/3, Motor-1/2, Compressor-1/2**

| Document Control | |
|---|---|
| Standard Number | MM-REG-9000-REV-A |
| Applicable Scope | All rotating equipment covered by MM-TM-4300 (Pumps), MM-TM-2200 (Motors), MM-TM-6100 (Compressors) |
| Applicable Units | Pump-1 (P-101), Pump-2 (P-102), Pump-3 (P-103), Motor-1 (M-201), Motor-2 (M-202), Compressor-1 (C-301), Compressor-2 (C-302) |
| Issuing Authority | MechMind Industrial Systems — Site Compliance & Regulatory Affairs (synthetic) |
| Revision | A |
| Status | Fully synthetic regulatory reference document for demonstration and testing purposes. It does not reproduce, paraphrase, or reference any real regulation, standard number, statutory instrument, or government body, and has no legal or regulatory effect. Any resemblance to real inspection intervals or resolution-time requirements is coincidental. |

> **Note on scope:** This standard sets the minimum inspection frequency and alarm-resolution-time requirements applicable to the seven-unit rotating equipment fleet described above. It is a site-level compliance overlay and does not replace or restate the equipment-specific technical, installation, or troubleshooting content already documented in MM-TM-4300, MM-TM-2200, and MM-TM-6100 — it should be read alongside those manuals, not in place of them.

---

## Table of Contents

1. Purpose & Scope
2. Applicability by Equipment Type
3. Inspection Frequency Requirements
4. Alarm Resolution Time Requirements
5. Rationale & Consequences of Non-Compliance
6. Recordkeeping & Audit Requirements
7. Document Revision History

---

# Section 1: Purpose & Scope

## 1.1 Purpose

This standard establishes the minimum periodic inspection frequency and maximum allowable alarm-resolution time for all rotating equipment operated under the MechMind site compliance program. It exists to give maintenance planning, reliability engineering, and site compliance staff a single, unambiguous reference for two questions that recur constantly in daily operations: *"is this unit due for inspection?"* and *"has this open alarm been outstanding longer than it is allowed to be?"*. Both questions matter independently of whether a unit is currently showing a fault — a unit with no active alarms can still be in violation of this standard if its last documented inspection has lapsed, and a unit that has since stabilized can still have been in violation while a Critical or Safety alarm sat unresolved past its allowed window.

This standard is intended to be read by maintenance planners scheduling routine work, by reliability engineers reviewing fleet health, and by automated maintenance-assistance tooling (including compliance-checking logic) that needs firm, numeric thresholds rather than qualitative guidance.

## 1.2 Relationship to Equipment Manuals

Sections 5 (Routine Maintenance Schedule) of MM-TM-4300, MM-TM-2200, and MM-TM-6100 each describe *what* a routine inspection or PM activity for that equipment type consists of — checklists, torque values, lubrication points, and similar procedural detail. This standard does not repeat that content. Instead, it answers a narrower, site-compliance-specific question: *how often* must some documented inspection or maintenance touchpoint occur, and *how quickly* must a Critical or Safety alarm be closed out, in order for a unit to be considered in compliance. Where a technical manual's maintenance schedule recommends a *shorter* interval than this standard for a specific procedure (for example, an oil analysis sub-task performed more frequently than the headline inspection interval), the shorter, more conservative interval always governs for that specific task; this standard sets the floor, not a ceiling.

## 1.3 Definitions

- **Inspection-qualifying event.** For the purposes of this standard, any documented maintenance log entry against a unit — whether triggered by a routine walkdown, a Warning-level observation, or a Critical/Safety alarm response — counts as evidence that the unit received hands-on attention on that date. A unit accumulates "days since last inspection" from the most recent such entry, regardless of the entry's severity, since any documented visit gives a technician the opportunity to observe the unit's general condition, not only the specific fault that prompted the visit.
- **Resolution time.** The elapsed time between a Critical- or Safety-severity alarm being logged and that same alarm being marked resolved. Where an explicit resolution timestamp is not separately recorded, the logged downtime duration for that event is used as the operative measure of how long the condition was outstanding, since it reflects the same underlying quantity (time the unit spent in the faulted condition before being returned to a resolved state).
- **Compliance gap.** Any unit for which either the inspection interval or an applicable resolution-time requirement in Sections 3–4 has been exceeded, as of the date compliance is evaluated.

# Section 2: Applicability by Equipment Type

## 2.1 Equipment Type Classification

This standard applies its inspection-interval requirements by *equipment type*, not by individual unit tag, since the underlying failure modes and duty cycles that justify a given interval are properties of the equipment class as a whole:

| Equipment Type | Units Covered | Governing Technical Manual |
|---|---|---|
| Pump | Pump-1 (P-101), Pump-2 (P-102), Pump-3 (P-103) | MM-TM-4300 |
| Motor | Motor-1 (M-201), Motor-2 (M-202) | MM-TM-2200 |
| Compressor | Compressor-1 (C-301), Compressor-2 (C-302) | MM-TM-6100 |

## 2.2 Standby and Duty Units

This standard applies identically to units in active duty service and units held in standby (for example, Pump-3, which operates as an installed standby per MM-TM-4300 Section 1.2). Standby status does not extend the applicable inspection interval — a unit in standby still accumulates seal wear, bearing grease degradation, and corrosion exposure while idle, and its instrumentation and start circuits must be verified functional on the same cycle as duty units so that it is genuinely available when called upon.

# Section 3: Inspection Frequency Requirements

## 3.1 Required Inspection Intervals

Each equipment type carries a distinct maximum inspection interval, reflecting differences in duty severity, failure-mode progression rate, and consequence of an undetected fault across the three equipment classes:

| Equipment Type | Maximum Inspection Interval | Basis |
|---|---|---|
| Pump | 90 days | Moderate-duty rotating equipment with wetted mechanical seal wear as the dominant time-based failure mode (see MM-TM-4300 Sections 3–4) |
| Motor | 120 days | Lower duty-cycle severity relative to pumps and compressors at this site; insulation and bearing degradation progress more slowly under the induction motors' typical loading profile (see MM-TM-2200 Sections 3–4) |
| Compressor | 60 days | Highest duty severity of the three classes — continuous compression cycling, oil carryover, and separator element loading progress faster and carry a higher consequence-of-failure profile (see MM-TM-6100 Sections 3–4) |

## 3.2 Interpretation

"Days since last inspection" is measured from the date of the most recent inspection-qualifying event (Section 1.3) for that unit to the date compliance is being evaluated. A unit whose elapsed days exceed the interval in Section 3.1 for its equipment type is in a compliance gap for inspection frequency, independent of whether it currently has any active alarm. A unit that received attention for an unrelated Warning-level alarm two weeks ago is treated identically, for interval-reset purposes, to a unit that received a scheduled routine walkdown two weeks ago — both demonstrate that the unit was inspected.

## 3.3 Rationale for Type-Specific Intervals

The 60/90/120-day spread across compressors, pumps, and motors is not arbitrary. Compressors in continuous service accumulate separator element loading and oil carryover on a timescale that makes a 60-day ceiling appropriate — beyond that window, undetected degradation in discharge temperature control or separator differential pressure has historically preceded unplanned trips at comparable installations. Pumps sit in the middle at 90 days, reflecting mechanical seal and bearing wear that progresses more gradually than compressor internals but still benefits from quarterly-scale attention. Motors, with the lowest duty severity of the three classes under typical site loading, are assigned the longest 120-day interval, consistent with slower-progressing insulation and bearing-grease degradation.

# Section 4: Alarm Resolution Time Requirements

## 4.1 Required Resolution Windows

Critical- and Safety-severity alarms (as classified in the Full Alarm Code Matrix of each equipment's technical manual, Section 3) each carry a maximum allowable resolution time, measured from the moment the alarm is logged:

| Alarm Severity | Maximum Resolution Time | Maximum Resolution Time (days) |
|---|---|---|
| Critical | 72 hours | 3 days |
| Safety | 24 hours | 1 day |

Warning-severity alarms carry no fixed resolution-time requirement under this standard; they are expected to be addressed through routine maintenance planning per each technical manual's troubleshooting guidance, but leaving a Warning open for an extended period is not, by itself, a compliance gap under this standard.

## 4.2 Why Safety Alarms Carry a Shorter Window Than Critical Alarms

Safety-classified alarms (for example, an Emergency Stop activation or an interlock-driven safety trip) indicate a condition where a hazard to personnel was judged credible enough to trigger an automatic protective action. The 24-hour window reflects that these conditions must be understood and corrected before the unit is returned to a state where the same hazard could recur, and that the investigation itself (confirming root cause, verifying interlock integrity, completing any required incident documentation) is expected to be achievable within one working day for a unit that is, by definition, already shut down. Critical alarms, while serious, more often reflect an equipment-protection threshold (a temperature, vibration, or electrical limit) rather than an immediate personnel hazard, and the 72-hour window allows for parts sourcing, more involved diagnostic work, or coordination with a planned outage window while still bounding how long a unit can run — or sit idle — with a known Critical-level condition outstanding.

## 4.3 Interpretation for Open (Unresolved) Alarms

Where a Critical or Safety alarm remains unresolved as of the date compliance is evaluated, the elapsed time since that alarm was logged is compared directly against the applicable window in Section 4.1. An unresolved Critical alarm logged 5 days ago has already exceeded its 72-hour window and constitutes an active compliance gap, regardless of how much longer it ultimately remains open. Where a Critical or Safety alarm has since been marked resolved, the logged downtime duration for that event (Section 1.3) is compared against the same window to determine whether the resolution, once it occurred, was still timely.

# Section 5: Rationale & Consequences of Non-Compliance

## 5.1 Why Inspection Intervals Matter Independently of Alarm State

A unit that has not thrown any alarm in months is not necessarily a unit in good condition — it may simply be a unit that has not been looked at closely enough, recently enough, to notice a slowly developing problem before it escalates to an alarm. This is the central justification for treating "days since last inspection" as a compliance dimension separate from active alarm state. Waiting for equipment to alarm before scheduling attention inverts the purpose of a maintenance program; the interval requirements in Section 3 exist specifically to force a documented touchpoint before that inversion can happen.

## 5.2 Why Resolution-Time Windows Matter Independently of Eventual Resolution

Similarly, a Critical or Safety alarm that is *eventually* resolved is not equivalent, from a compliance standpoint, to one resolved *promptly*. A Critical alarm left open for eleven days before being addressed represents eleven days of operating (or idling) a unit with a known equipment-protection threshold already breached — the fact that it was fixed on day eleven does not retroactively make days four through eleven compliant. This is why Section 4 evaluates resolution time as its own pass/fail condition rather than folding it into a simple "was it eventually resolved, yes or no" check.

## 5.3 Consequences of an Identified Compliance Gap

When a unit is identified as having a compliance gap under this standard — whether an inspection-interval lapse or a resolution-time violation — the following applies:

1. The gap and its specific basis (which requirement was exceeded, by how much) must be recorded in the site compliance record per Section 6.
2. The unit is not automatically removed from service solely on the basis of an inspection-interval lapse, but the lapse must be closed out with a documented inspection at the earliest practical opportunity, and in no case should a second interval be allowed to lapse on top of the first.
3. An open resolution-time violation on a Critical or Safety alarm should be escalated to a maintenance supervisor or reliability engineer for expedited action, since by definition the unit has already exceeded the window this standard considers acceptable for that severity class.
4. Repeated compliance gaps on the same unit, or the same equipment type across multiple units, should prompt a review of whether the interval or resolution-time requirement itself remains appropriate, or whether a root cause in staffing, spares availability, or scheduling is driving a recurring pattern rather than an isolated lapse.

## 5.4 Consequences of Ignoring This Standard

Sites that do not track inspection recency and resolution time as explicit, numeric compliance dimensions tend to discover degraded equipment only at the point of failure, when the cost of correction — unplanned downtime, secondary damage, and in the case of Safety-classified conditions, a credible personnel hazard recurring before its root cause was fully addressed — is highest. The specific numeric thresholds in Sections 3 and 4 are deliberately conservative relative to worst-case failure progression rates, so that a unit identified as in-compliance under this standard has a comfortable margin before the underlying equipment-protection or personnel-safety concern that motivated the requirement actually materializes.

# Section 6: Recordkeeping & Audit Requirements

## 6.1 Minimum Recordkeeping

For each unit, the site compliance record should retain, at minimum, the date of the most recent inspection-qualifying event and the outcome (compliant / gap-detected, with reason) of the most recent compliance evaluation against Sections 3 and 4. This is the minimum information needed to answer, on demand, whether any unit in the seven-unit fleet currently has an open compliance gap.

## 6.2 Evaluation Cadence

Compliance status under this standard should be evaluated on a rolling basis — in practice, continuously, since both the inspection-interval clock and any open resolution-time window advance every day regardless of whether anyone has looked at them. Automated tooling that re-evaluates all seven units against current date, rather than relying on a periodic manual review, is the preferred implementation of this requirement.

## 6.3 Audit Trail

Where automated compliance tooling is used to evaluate this standard, the specific reason string produced for a gap-detected unit (for example, identifying the exact interval or window exceeded, and by how much) should be treated as the audit-relevant record, not merely the pass/fail status alone. A bare "non-compliant" flag without the underlying reason does not give a reviewer enough information to prioritize a response or to verify, after the fact, that the gap was correctly identified.

# Section 7: Document Revision History

| Revision | Date | Summary |
|---|---|---|
| A | Initial issue | Establishes inspection interval requirements by equipment type (Section 3) and alarm resolution time requirements by severity (Section 4) for the seven-unit fleet (Pump-1/2/3, Motor-1/2, Compressor-1/2). |
