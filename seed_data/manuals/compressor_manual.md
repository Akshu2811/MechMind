# MechMind MC-6100 Series Rotary Screw Air Compressor

## Technical Reference & Operations Manual

**Covering Unit Tags: Compressor-1 (C-301), Compressor-2 (C-302)**

| Document Control | |
|---|---|
| Manual Number | MM-TM-6100-REV-C |
| Applicable Model Line | MC-6100 Series, Oil-Flooded Rotary Screw Air Compressor Package |
| Applicable Units | Compressor-1 (Tag C-301, S/N MM-6100-3001), Compressor-2 (Tag C-302, S/N MM-6100-3002) |
| Controller Platform | CompGuard™ Local Controller, firmware 1.8.x |
| Revision | C |
| Issued By | MechMind Industrial Systems — Technical Publications |
| Status | Fully synthetic reference document for demonstration and testing purposes. No affiliation with any real manufacturer. |

> **Note on scope:** This manual documents a two-unit installation (Compressor-1, Compressor-2) of identical MC-6100 Series construction, installed in a base-load/trim arrangement supplying the site's Plant Compressed Air System. Except where a procedure or specification explicitly calls out one unit by tag, all content applies equally to Compressor-1 and Compressor-2.

---

## Table of Contents

1. Overview & Technical Specifications
2. Installation & Commissioning Procedures
3. Full Alarm Code Matrix
4. Detailed Troubleshooting Procedures
5. Routine Maintenance Schedule
6. System Sizing & Duty Cycle
7. Appendix A — Safety & Compliance
8. Glossary of Terms and Abbreviations
9. Document Revision History

---

# Section 1: Overview & Technical Specifications

## 1.1 Purpose and Scope

This manual provides the technical reference, installation, commissioning, alarm response, troubleshooting, maintenance, and safety documentation for the MechMind MC-6100 Series oil-flooded rotary screw air compressor package, as installed in the two-unit configuration designated **Compressor-1** and **Compressor-2**. Both units are of identical mechanical, electrical, and pneumatic construction and share a common instrumentation and control architecture built around the CompGuard™ Local Controller. Where information in this manual differs between units — for example, a unit's current lead/trim role assignment, which alternates per Section 1.8 — this is called out explicitly. Otherwise, all specifications, procedures, and alarm behaviors apply uniformly across the two-compressor set.

This document is intended for use by commissioning engineers, mechanical and electrical maintenance technicians, reliability engineers, and control system integrators responsible for the operation and upkeep of Compressor-1 and Compressor-2. It is also intended to serve as a structured knowledge source for automated maintenance-assistance tooling, including alarm-code lookup, troubleshooting guidance retrieval, and maintenance scheduling support.

## 1.2 Equipment Identification

Compressor-1 and Compressor-2 are installed in the site's Compressor House and discharge into a common Plant Compressed Air System, consisting of a wet air receiver, downstream air treatment (dryers and filtration, outside the scope of this manual), a dry air receiver, and separate Plant Instrument Air and Plant Utility Air headers serving the wider site.

| Unit Tag | Equipment Tag | Serial Number | Install Location | Discharges To |
|---|---|---|---|---|
| Compressor-1 | C-301 | MM-6100-3001 | Compressor House, Bay 1 | Wet Air Receiver R-301 |
| Compressor-2 | C-302 | MM-6100-3002 | Compressor House, Bay 2 | Wet Air Receiver R-301 |

Rather than a duty/standby arrangement, Compressor-1 and Compressor-2 normally operate together in a base-load/trim sequencing arrangement managed by the CompGuard sequencing logic (Section 1.8): one unit runs fully loaded as the base-load machine, while the other modulates via its integral VFD to track the difference between total plant demand and the base-load unit's fixed output. Lead/trim roles are alternated on a scheduled basis to equalize wear between the two units, in keeping with the wear-equalization philosophy applied across the MechMind rotating equipment fleet.

## 1.3 Compressor Design Description

The MC-6100 Series is an oil-flooded, single-stage rotary twin-screw air compressor package intended for continuous-duty industrial compressed air service. Key construction features common to Compressor-1 and Compressor-2:

- **Airend**: Asymmetric-profile twin-screw rotor set (male/female rotor pair), oil-flooded for sealing, cooling, and lubrication of the compression process, direct-coupled to the drive motor without a step-up gearbox.
- **Drive motor**: Integral high-efficiency induction motor of the same MX-2200 Series design used elsewhere in the MechMind rotating equipment fleet (see the separate MX-2200 Series motor manual), rated 250 kW, 400 V, 3-phase, 60 Hz, driven via an integral VFD providing capacity turndown through the range described in Section 1.9.
- **Oil separation system**: Two-stage separation — a cyclonic primary stage integral to the discharge receiver vessel, followed by a coalescing final separator element — limiting residual oil carryover in the discharge air to below 3 mg/m³.
- **Cooling package**: Integral air-cooled oil cooler and aftercooler, each served by a dedicated cooling fan, sized for the ambient design range in Section 1.4.
- **Inlet filtration**: Dry-type pleated inlet air filter with a replaceable element, protecting the airend from ambient particulate ingestion.
- **Minimum pressure valve**: A combination check/minimum-pressure valve at the wet receiver outlet, maintaining a minimum vessel pressure sufficient to sustain oil injection differential pressure across the full capacity turndown range (see Section 1.9 and Section 3.3, `MIN_PRESS_VALVE_18`).
- **Condensate management**: An automatic zero-air-loss electronic condensate drain valve on the wet receiver, removing separated moisture without discharging compressed air.
- **Enclosure**: Acoustic package enclosure reducing package sound level to the value given in Section 1.4, with access panels for routine service points.
- **Skid**: Fabricated steel base skid, common to the airend, motor, oil system, and cooling package as a single shippable unit.
- **Paint system**: Two-coat epoxy, RAL 5015 (sky blue) finish coat, consistent with the MechMind fleet-wide equipment color standard.

## 1.4 Technical Specifications

| Parameter | Value |
|---|---|
| Compressor type | Oil-flooded, single-stage rotary twin-screw, VFD capacity control |
| Free air delivery (FAD), rated | 42 m³/min (1,483 cfm) |
| Rated discharge pressure | 8.6 bar(g) (125 psig) |
| Adjustable discharge pressure range | 5.5–10.3 bar(g) (80–150 psig) |
| Maximum vessel working pressure | 13 bar(g) (188 psig) |
| Drive motor | 250 kW (335 hp), 400 V, 3-phase, 60 Hz, IE3, integral VFD |
| Motor full-load current | 410 A at 400 V |
| Capacity turndown range (VFD modulation) | 40–100% of rated FAD |
| Specific power at full load | 6.4 kW per m³/min FAD (see Section 1.9) |
| Oil charge volume | 110 L, ISO VG46 compressor lubricant |
| Oil separator residual carryover | < 3 mg/m³ |
| Inlet air filter | Dry pleated element, replaceable |
| Ambient design range | 5 °C to 46 °C |
| Altitude (no derating) | Up to 1,000 m |
| Sound pressure level | 78 dB(A) at 1 m, enclosed package |
| Weight (complete package) | 3,200 kg |
| Vibration classification | ISO 10816-3 |
| Enclosure/control cabinet rating | IP54 |
| Paint system | 2-coat epoxy, RAL 5015 |

## 1.5 Nameplate Data and Identification

Each package carries a stainless steel nameplate mounted on the enclosure, stamped with the equipment tag, serial number, rated capacity and pressure, and year of manufacture. Nameplate data must match the values recorded in the commissioning record (Section 2.11) and the asset record in the plant CMMS. As with all MechMind fleet equipment, a mismatch between nameplate serial number and CMMS record should be treated as a documentation discrepancy requiring investigation before further work is performed on the unit.

## 1.6 Control System Overview

Compressor-1 and Compressor-2 are each monitored and protected by an individual CompGuard™ Local Controller, mounted in the package's integral control cabinet. Each CompGuard controller aggregates:

- A discharge air temperature sensor at the airend discharge, upstream of the oil separator,
- An oil temperature sensor,
- An oil injection pressure transducer, used together with the discharge pressure reading to derive oil injection differential pressure,
- A discharge (system) pressure transmitter,
- An oil separator element differential pressure transmitter,
- An inlet air filter differential pressure transmitter,
- An aftercooler air-side outlet temperature sensor, used together with an ambient temperature reference to derive approach temperature,
- An oil reservoir level sensor,
- Two MEMS accelerometer-based vibration sensors (airend drive-end and motor non-drive-end housings), ISO 10816-3 zone classification,
- Condensate drain valve cycle status,
- Capacity control valve/VFD modulation position feedback,
- VFD status, output current, and speed feedback via Modbus RTU,
- A starts-per-hour counter derived from VFD run commands,
- Local E-Stop and safety interlock status.

The CompGuard controller evaluates these inputs continuously against configured thresholds and raises one of the twenty standardized alarm codes described in full in **Section 3** when a threshold is exceeded or a fault condition is detected. Alarms are surfaced on the local HMI, forwarded to the plant DCS over Modbus TCP, and logged with timestamp, unit tag, and triggering value in the CompGuard historian, following the same architectural pattern used by the PumpGuard and MotorGuard platforms documented for the site's process pump and motor fleets. Section 4 of this manual expands on the diagnostic and corrective procedures for the most operationally significant of these alarm codes.

## 1.7 Process Air Quality and Service Conditions

The service basis assumed by the specifications in Section 1.4 is as follows:

| Parameter | Design Basis |
|---|---|
| Inlet air condition | Ambient plant air, filtered per Section 1.3; not suitable for direct compression of process gases or contaminated atmospheres without engineering review |
| Discharge air quality (at package outlet, before downstream drying) | Oil carryover < 3 mg/m³ per Section 1.4; moisture content per saturation at discharge temperature and pressure, reduced by downstream dryers (outside this manual's scope) |
| Duty cycle | Continuous (S1) for the base-load unit; variable, demand-following duty for the trim unit (see Section 1.8 and Section 6) |
| Starts per hour | 2 evenly spaced starts per hour maximum for a full stop/restart cycle (see `STARTS_EXCEED_19`); VFD capacity modulation within a continuous run is not counted as a start |
| Supply voltage tolerance | ±10% of nominal 400 V |
| Voltage imbalance limit | 1% maximum, phase-to-phase, measured at the motor terminals |

A change to the inlet air environment, process air quality requirement, or demand pattern outside this design basis should be reviewed against these parameters before being accepted as normal operation, since several alarm codes in Section 3 (`INLET_FILT_DP_09`, `SEP_DP_HIGH_08`, `PH_LOSS_13`) are directly sensitive to exactly these conditions.

## 1.8 Lead/Trim Sequencing and Unit-to-Unit Comparison

The CompGuard sequencing logic assigns one unit as base-load (running fully loaded, continuously, near its most efficient operating point) and the other as trim (modulating via VFD speed to track fluctuating plant demand above the base-load unit's fixed output). Because the trim role involves substantially more frequent speed modulation, and in some demand profiles more frequent full stop/start cycling, than the base-load role, the two units do not accumulate wear identically even though they are of identical construction — this is an intentional operational asymmetry, not a design flaw, and it is central to the discussion in Section 6.

Lead/trim roles are alternated between Compressor-1 and Compressor-2 on a scheduled basis (nominally every 336 hours of combined run time) so that neither unit accumulates a disproportionate share of trim-role wear over its service life. Because of this alternation, the cross-unit comparison techniques used throughout this manual (Section 4.1, Section 4.9) must account for which role each unit was performing during the period being compared — a direct comparison of Compressor-1's vibration trend while it was in the trim role against Compressor-2's trend while in the base-load role is not a like-for-like comparison, and should be corrected for role before being used to judge unit-specific condition.

## 1.9 Capacity Turndown and Part-Load Power Characteristics

The following data characterizes MC-6100 Series behavior across its VFD-driven capacity turndown range and is the basis for the `DISCH_PRESS_LOW_07` diagnostic procedure in Section 4, the `CAPACITY_FAULT_17` alarm response, and the System Sizing & Duty Cycle discussion in Section 6:

| Capacity (% of Rated FAD) | Motor Speed (% of Rated) | Package Power (% of Rated) | Specific Power (kW per m³/min) |
|---|---|---|---|
| 100% (full load) | 100% | 100% | 6.4 |
| 80% | 82% | 78% | 6.5 |
| 60% | 63% | 58% | 6.7 |
| 40% (minimum stable turndown) | 45% | 42% | 7.1 |
| Below 40% (unload/idle) | N/A | ~25% (idle, no useful output) | Not applicable |

Specific power — the electrical power consumed per unit of air delivered — rises as capacity turndown deepens, since certain package losses (bearing friction, oil pump work where fitted, cooling fan power) do not scale down proportionally with reduced airend throughput. Operating for extended periods below the 40% minimum stable turndown point forces the unit into a load/unload cycle rather than smooth VFD modulation, consuming idle power without producing useful compressed air output — the efficiency and equipment-wear implications of this are addressed in full in Section 6, which uses this table as its starting reference point.

## 1.10 Relationship to the MechMind Rotating Equipment Fleet's Controller Architecture

The CompGuard controller platform documented in this manual follows the same general architecture as the PumpGuard and MotorGuard platforms used elsewhere in the site's rotating equipment fleet (see the separate MP-4300 Series pump manual and MX-2200 Series motor manual): each uses per-unit local controllers aggregating temperature, vibration, and electrical instrumentation into a standardized set of severity-classified alarm codes, each forwards alarms to the plant DCS over Modbus TCP, and each applies the same ISO 10816-3 vibration zone classification for rotating machinery condition. This shared architecture is a deliberate site-level standardization decision, not a coincidence, and it has a practical consequence for personnel working across multiple equipment types: a technician trained on alarm acknowledgement, reset, and escalation procedure for one platform (Section 3.4 in this manual) can apply the same procedural logic to the others with only the specific alarm codes and thresholds differing between them.

The three platforms do differ in instrumentation and sequencing emphasis in ways that reflect the different failure modes and operating patterns of their respective machines: the pump fleet's PumpGuard instrumentation emphasizes seal chamber and flush-circuit monitoring across a three-unit duty/duty/standby arrangement; the motor fleet's MotorGuard instrumentation emphasizes winding insulation monitoring and starts-per-hour supervision across two continuously-loaded parallel units; and the CompGuard platform documented here emphasizes oil circuit health (injection pressure, separator condition, oil temperature) and capacity/demand-matching supervision across a two-unit base-load/trim arrangement with no dedicated standby unit (see Section 6.7). A reliability engineer reviewing alarm history across the combined fleet should keep these differences in emphasis and redundancy philosophy in mind rather than expecting the three alarm code sets, or the three sequencing arrangements, to map directly onto one another.

---

# Section 2: Installation & Commissioning Procedures

## 2.1 Pre-Installation Inspection

Before Compressor-1 or Compressor-2 is unpacked at its final installation location, perform the following inspection and record results in the commissioning checklist:

1. Verify the shipping crate/wrap is undamaged and any tilt/shock indicators have not been triggered.
2. Confirm nameplate data (Section 1.5) matches the purchase order and the intended install location (Bay 1 or Bay 2).
3. Confirm the oil charge shipped with the unit is present and at the correct level per Section 5.7, and confirm it is the specified ISO VG46 compressor lubricant grade, not a substitute.
4. Inspect the inlet air filter housing and element for shipping damage or dust ingress during transit.
5. Confirm the enclosure panels are undamaged and all access points needed for routine service (Section 5) are unobstructed.
6. Rotate the airend by hand where a manual rotation point is provided, to confirm free rotation with no binding, before any electrical connection is made.

## 2.2 Site and Foundation Requirements

Each compressor bay (Bay 1, Bay 2) in the Compressor House is designed with a level, reinforced concrete floor sized for the package weight (3,200 kg) with a standard industrial floor loading margin; unlike some larger rotating equipment in the MechMind fleet, the MC-6100 Series does not require a dedicated engineered foundation or grouted baseplate, since the package's internal skid and vibration isolation are designed for placement directly on a level floor.

Minimum clearances around each installed unit:

| Direction | Minimum Clearance |
|---|---|
| Cooling air intake side | 1.0 m |
| Cooling air discharge side | 1.5 m (to avoid recirculation of warm discharge air back into the intake of the same or an adjacent unit) |
| Service access panels | 0.8 m |
| Overhead | 2.0 m |

The cooling air discharge clearance is particularly important in a two-unit installation: if Compressor-1's cooling air discharge is not adequately separated from Compressor-2's cooling air intake, one unit's rejected heat can elevate the other's intake air temperature, contributing to `DISCH_TEMP_01` and `OIL_TEMP_02` on the downwind unit even when that unit's own condition is otherwise normal.

## 2.3 Rigging and Placement

The complete package (3,200 kg) must be lifted using the four tapped lifting points on the skid. Do not lift the package using the enclosure panels, piping connections, or any point not specifically designated as a lifting point.

1. Use a rated 4-leg chain sling or spreader bar sized for the package weight plus a minimum 25% safety margin.
2. Confirm no personnel are positioned beneath the suspended load at any point during the lift.
3. Lower the package onto the prepared floor location, confirming the skid sits flat with no rocking; shim under the skid if the floor is not sufficiently level, rather than relying on the package's internal isolation to compensate for gross floor unevenness.

## 2.4 Piping Connections

1. Connect the discharge piping to the wet air receiver (R-301) using a flexible connector at the package discharge to isolate the package from piping-transmitted vibration and thermal expansion loads, consistent with the piping-isolation philosophy applied to rotating equipment across the MechMind fleet.
2. Ensure discharge piping is independently supported so that no piping weight is transmitted into the package discharge connection.
3. Install an isolation valve and check valve on each unit's discharge line upstream of the common header, so that either unit can be isolated for maintenance without depressurizing the shared receiver or requiring the other unit to be stopped.
4. Confirm the condensate drain line from each unit's automatic drain valve is routed to the site's oil/water separator system before discharge to any drain, since compressor condensate contains residual oil carryover and must not be routed to a stormwater or unoiled drain system.
5. Confirm inlet air ducting (if used to draw air from outside the Compressor House rather than directly from the room) is sized to avoid excessive inlet pressure drop, which would otherwise present as reduced capacity and elevated specific power beyond the Section 1.9 reference values without any fault on the package itself.

## 2.5 Electrical Connections

1. Confirm motor nameplate voltage, frequency, and rotation match the supply and the integral VFD configuration before energizing — because the drive motor is integral to the package and pre-wired at the factory, this check is primarily a supply-side verification rather than a field motor-wiring exercise.
2. Terminate incoming power at the package's main disconnect per the torque values in Section 5.8.
3. Confirm the CompGuard controller's instrument inputs are landed correctly, distinguishing discharge air temperature from oil temperature and from aftercooler outlet temperature by the labeling scheme on the package wiring diagram — a swapped temperature sensor connection is a known source of confusing `DISCH_TEMP_01` versus `OIL_TEMP_02` versus `AFTERCOOLER_FOUL_10` alarm behavior if made during commissioning and not caught until a later troubleshooting investigation.
4. Confirm the condensate drain valve's independent control circuit is verified separately from the main package control power.
5. Perform a phase rotation check at initial start (Section 2.10) to confirm airend rotation direction matches the required direction before the unit is run under load — reverse rotation on a screw airend can cause rapid internal damage and must be caught at the very first start attempt, not discovered after a period of running.

## 2.6 Piping and Vibration Isolation Verification

Although the MC-6100 Series does not require a grouted foundation (Section 2.2), vibration transmission through rigid piping connections remains a relevant installation consideration:

1. Confirm the discharge flexible connector (Section 2.4) is installed in-line, not offset or twisted, per the connector manufacturer's installation instructions, since an improperly installed flexible connector can itself become a source of vibration or premature failure rather than isolating vibration as intended.
2. After piping connections are complete, perform a baseline vibration reading (Section 2.11) and compare against the factory test data supplied with the unit; a reading significantly above the factory baseline immediately after piping connection, with no such elevation before piping was connected, points to a piping-transmitted strain or vibration path rather than a package-internal condition.

## 2.7 VFD and Capacity Control Setup

1. Confirm the integral VFD is programmed with the correct motor nameplate parameters and the capacity turndown range specified in Section 1.9 (40–100% of rated FAD).
2. Configure the discharge pressure setpoint and control band per the site's Section 6 system sizing analysis, not simply left at the factory default, since the correct setpoint depends on the specific downstream system's pressure requirements and the sequencing arrangement with the sister unit.
3. Configure the starts-per-hour supervision function in the CompGuard controller to the design limit in Section 1.7 (2 full stop/restart cycles per hour), which raises `STARTS_EXCEED_19` if exceeded; note that VFD capacity modulation within a continuous run does not count toward this limit, only a genuine stop/restart of the unit.
4. Configure the minimum pressure valve (Section 1.3) cracking pressure to maintain adequate oil injection differential pressure across the full turndown range specified in Step 1; an incorrectly configured or mismatched minimum pressure valve is a documented contributing cause of `OIL_PRESS_03` at low capacity, even when the valve itself is not faulty.
5. Confirm the VFD carrier frequency and output filtering are configured per the motor manufacturer's recommendation, consistent with the practice applied to the MX-2200 Series motor line elsewhere in the MechMind fleet.

## 2.8 Instrumentation Wiring and CompGuard Controller Commissioning

Each CompGuard controller must be commissioned individually per unit tag before that unit is placed in service:

1. Confirm the controller is configured with the correct unit tag (Compressor-1 / Compressor-2) — a mis-tagged controller will log alarms under the wrong unit identity in the historian and DCS, complicating later maintenance record reconciliation (Section 5.10).
2. Load the standard MC-6100 alarm threshold configuration set (see Section 3 for the full list of codes and default thresholds).
3. Verify each of the following instrument loops with a simulated or physical test signal before leaving the site: discharge air temperature, oil temperature, oil injection pressure, discharge pressure, oil separator differential pressure, inlet filter differential pressure, aftercooler outlet temperature, oil level, vibration sensors (airend/motor), condensate drain status, capacity control position feedback.
4. Confirm the local E-Stop pushbutton correctly triggers `ESTOP_ACT_20` and removes the run permissive at the VFD.
5. Confirm Modbus TCP communication to the plant DCS is established and that all 20 alarm codes map correctly to their assigned DCS alarm points.
6. Confirm the lead/trim sequencing logic (Section 1.8) correctly recognizes both units and that role alternation is configured per the site's operating philosophy before either unit is released to automatic sequencing.

## 2.9 Pre-Start Checks

Before the first start of any unit, confirm:

- Oil level is correct per Section 5.7, checked with the unit at rest.
- Inlet air filter element is clean and correctly seated.
- All discharge and condensate piping connections are complete and leak-tested.
- Discharge isolation valve is open (or per the site's specific start sequence, cracked open initially per Section 2.10).
- All temporary shipping restraints have been removed.
- Local E-Stop and safety interlocks are verified functional.

## 2.10 Initial Start-Up Procedure

Compressor-1 and Compressor-2 are commissioned sequentially so that any systemic issue (piping, electrical supply, control logic) is identified and resolved before the second unit is exposed to it.

1. Start the unit and immediately confirm correct rotation direction per Section 2.5 Step 5; stop immediately if rotation is incorrect, before the unit reaches operating pressure.
2. Confirm the unit loads smoothly and discharge pressure rises toward the configured setpoint without excessive overshoot.
3. Monitor discharge air temperature, oil temperature, oil pressure, and vibration continuously through the initial loading sequence.
4. Hold the unit at a stable operating point for a minimum 30-minute run-in period, logging discharge air temperature, oil temperature, oil pressure, discharge pressure, motor current, and vibration at 5-minute intervals.
5. Exercise the capacity turndown range described in Section 1.9 during the run-in period, confirming stable modulation down to the 40% minimum turndown point without triggering `CAPACITY_FAULT_17` or `OIL_PRESS_03`.
6. Confirm no CompGuard alarms are active at the end of the run-in period.
7. Repeat for the second unit.

## 2.11 Performance Verification and Commissioning Sign-off

At the conclusion of run-in for each unit, record the following in the commissioning record and compare against the rated specifications in Section 1.4 and Section 1.9:

- Free air delivery and specific power at full load, compared against the Section 1.9 reference table
- Discharge air temperature, oil temperature, and oil injection differential pressure at full load and at the minimum turndown point
- Vibration levels, airend and motor bearing housings (must be within ISO 10816-3 Zone A/B for a newly commissioned machine)
- Motor current at full load (must be below nameplate full-load current of 410 A)
- Oil separator and inlet filter differential pressure at commissioning (the clean-element baseline against which future fouling trends are compared, per Section 5.5)

Commissioning is not considered complete, and the unit should not be released to automatic lead/trim sequencing, until all values above are recorded within acceptance bands and signed off by both the commissioning engineer and the site reliability engineer. Retain the signed commissioning record permanently as the baseline reference for all future trending.

## 2.12 Key VFD and Control Parameters to Verify at Commissioning

| Parameter | Typical Setting | Relevance |
|---|---|---|
| Capacity turndown range | 40–100% of rated FAD | Sustained operation below this floor forces load/unload cycling rather than smooth modulation (Section 1.9, Section 6) |
| Discharge pressure setpoint and control band | Per site Section 6 system sizing analysis | Misconfiguration is a common root cause of nuisance `DISCH_PRESS_LOW_07` or `DISCH_PRESS_HIGH_05` events |
| Starts-per-hour supervision | 2 full stop/restart cycles/hour maximum | Raises `STARTS_EXCEED_19` if exceeded |
| Minimum pressure valve cracking pressure | Per Section 2.7 Step 4 | Directly affects oil injection differential pressure margin at low capacity, see `OIL_PRESS_03` |
| Current limit | Motor nameplate full-load current (410 A) plus drive-specific service factor | Misconfiguration is a documented root cause of nuisance `MOTOR_OVLD_12` trips (Section 4) |
| Lead/trim role alternation interval | 336 hours combined run time | Equalizes trim-role wear between Compressor-1 and Compressor-2 (Section 1.8) |
| Modbus communication timeout | Per CompGuard controller default | A timeout set too short can produce nuisance `VFD_FAULT_14` events during normal plant network congestion |

## 2.13 Common Commissioning Pitfalls and Their Downstream Alarm Consequences

- **Skipping the pre-start oil level and grade verification (Section 2.1, Section 2.9).** Starting a unit with an incorrect oil level or the wrong lubricant grade risks both an early `OIL_LEVEL_LOW_04` or `OIL_PRESS_03` event and, in a severe case, accelerated airend wear that would not be caught until a much later `VIB_HIGH_11` or bearing-related finding.
- **Swapping discharge air, oil, and aftercooler temperature sensor wiring (Section 2.5 Step 3).** This is the single most common instrumentation commissioning error on the MC-6100 Series and produces confusing, internally-inconsistent alarm behavior that can consume significant troubleshooting time before the wiring error itself is identified as the root cause.
- **Leaving the discharge pressure setpoint at factory default without a Section 6 system sizing review.** A setpoint that does not match the actual downstream system's requirements produces chronic `DISCH_PRESS_LOW_07` or excessive part-load/unload cycling, neither of which reflects a genuine equipment fault.
- **Mis-tagging the CompGuard controller (Section 2.8).** As with the pump and motor fleets' respective controllers, a controller commissioned under the wrong unit tag silently corrupts the historian record for both units involved, and is often not discovered until a maintenance history review under Section 5.10 fails to reconcile with observed physical work.
- **Failing to verify the minimum pressure valve setting before exercising the full turndown range (Section 2.10 Step 5).** A unit that passes commissioning at full load but has not been verified across its full turndown range can pass initial commissioning and still present an early `OIL_PRESS_03` event the first time plant demand genuinely drops the trim unit to a low capacity point.

## 2.14 Documentation Handover Package

On completion of commissioning for each unit, the following documentation must be assembled into a permanent handover package and filed both in the site CMMS and in the physical or electronic equipment file for that unit tag, before the unit is released to automatic lead/trim sequencing:

| Document | Source | Purpose |
|---|---|---|
| Signed commissioning record | Section 2.11 | Performance and condition baseline for all future comparisons |
| VFD and control parameter record | Section 2.12 | Baseline for detecting later configuration drift |
| Clean-element differential pressure baselines (inlet filter, oil separator) | Section 2.11 | Baseline for future fouling-trend comparison under Section 5.5 |
| Instrument loop verification checklist | Section 2.8 | Confirms each protective input was functional at handover |
| Minimum pressure valve turndown verification record | Section 2.10 Step 5 | Confirms the valve was verified across the full capacity range, not only at full load |
| Nameplate and CMMS asset record cross-check | Section 1.5 | Confirms no documentation discrepancy exists at the point of handover, when it is easiest to correct |

A unit should not be released to automatic lead/trim sequencing until this package is complete. An incomplete handover package is not merely a paperwork gap: several of the diagnostic procedures in Section 4 (notably `DISCH_TEMP_01` in Section 4.2, `VIB_HIGH_11` in Section 4.6, and the filter/separator trend checks in Section 4.9) depend on comparing a current reading against the specific unit's own commissioning baseline, and a missing or incomplete baseline materially weakens the diagnostic value of every future alarm investigation on that unit for the remainder of its service life.

---

# Section 3: Full Alarm Code Matrix

## 3.1 How to Use This Section

Every alarm raised by the CompGuard controller on Compressor-1 or Compressor-2 is identified by one of the twenty standardized codes below. Each code is fixed across both units — the same code always means the same condition, regardless of which unit tag raised it. The summary table gives a quick-reference view; the subsections that follow give the full detail (likely causes and recommended immediate steps) for each code. Seven of these codes — `DISCH_TEMP_01`, `OIL_TEMP_02`, `OIL_PRESS_03`, `DISCH_PRESS_LOW_07`, `VIB_HIGH_11`, `MOTOR_OVLD_12`, and `PH_LOSS_13` — have full step-by-step diagnostic procedures in Section 4; this section gives the first-response summary for all twenty.

Severity levels used throughout this manual:

- **Warning** — degraded condition, unit remains in service, investigate at next opportunity.
- **Critical** — unit performance or equipment integrity at risk, investigate promptly; some Critical codes are configured to auto-trip the unit.
- **Safety** — condition involves a safety interlock or protective device; unit is stopped and will not restart until the interlock is manually cleared.

## 3.2 Summary Table

| Code | Description | Severity | Auto-Trip? |
|---|---|---|---|
| `DISCH_TEMP_01` | Discharge Air Temperature High (airend discharge, pre-separator) | Warning at 100 °C / Critical at 110 °C | Yes, at Critical threshold |
| `OIL_TEMP_02` | Oil Temperature High | Warning at 90 °C / Critical at 100 °C | Yes, at Critical threshold |
| `OIL_PRESS_03` | Oil Injection Pressure Low (Differential) | Critical | Yes |
| `OIL_LEVEL_LOW_04` | Oil Reservoir Level Low | Warning, escalates to Critical | Yes, if sustained |
| `DISCH_PRESS_HIGH_05` | Discharge Pressure High | Warning | No |
| `HIGH_HIGH_PRESS_06` | High-High Discharge Pressure (safety-relief adjacent) | Safety/Critical | Yes (immediate) |
| `DISCH_PRESS_LOW_07` | Discharge Pressure Low / System Demand Exceeds Capacity | Warning | No |
| `SEP_DP_HIGH_08` | Oil Separator Element Differential Pressure High | Warning | No |
| `INLET_FILT_DP_09` | Inlet Air Filter Differential Pressure High | Warning | No |
| `AFTERCOOLER_FOUL_10` | Aftercooler Fouling / High Approach Temperature | Warning | No |
| `VIB_HIGH_11` | Excessive Vibration (airend or motor bearings) | Warning at Zone C / Critical at Zone D (ISO 10816-3) | Yes, at Critical threshold |
| `MOTOR_OVLD_12` | Motor Overload / Overcurrent | Critical | Yes |
| `PH_LOSS_13` | Phase Loss / Voltage Imbalance | Critical | Yes |
| `VFD_FAULT_14` | VFD Communication or Drive Fault | Critical | Yes |
| `SENSOR_FAIL_15` | Instrument/Sensor Signal Failure | Warning | No |
| `CONDENSATE_FAULT_16` | Automatic Condensate Drain Fault | Warning | No |
| `CAPACITY_FAULT_17` | Capacity Control / Modulation Fault | Warning | No |
| `MIN_PRESS_VALVE_18` | Minimum Pressure Valve Fault | Warning, escalates to Critical | Yes, if sustained low oil pressure results |
| `STARTS_EXCEED_19` | Excessive Starts Per Hour | Warning | No (start inhibited, not a running trip) |
| `ESTOP_ACT_20` | Emergency Stop Activated | Safety | Yes (immediate) |

## 3.3 Detailed Alarm Descriptions

### `DISCH_TEMP_01` — Discharge Air Temperature High

**Severity:** Warning at 100 °C sustained for 1 minute; Critical (auto-trip) at 110 °C, measured at the airend discharge upstream of the oil separator.

**Likely causes:**
- Oil cooler fouling or cooling fan fault, reducing oil cooling and therefore raising the injected oil temperature (see `OIL_TEMP_02`)
- Low oil flow to the airend from a developing `OIL_PRESS_03` condition
- Elevated ambient or inlet air temperature (see Section 2.2 cooling air discharge/intake separation, and Section 6)
- Airend internal wear increasing compression work and heat generation
- A swapped temperature sensor wiring error from commissioning (see Section 2.13)

**Recommended immediate steps:**
1. Confirm the reading against the oil temperature reading before assuming a genuine airend condition rather than a sensor or wiring issue.
2. Check oil cooler and cooling fan operation.
3. Full diagnostic procedure: see Section 4.2.

### `OIL_TEMP_02` — Oil Temperature High

**Severity:** Warning at 90 °C sustained for 2 minutes; Critical (auto-trip) at 100 °C.

**Likely causes:**
- Oil cooler fouling (external fins or internal passages) or cooling fan fault
- Low oil level (see `OIL_LEVEL_LOW_04`) reducing the oil system's thermal mass and cooling capacity
- Elevated ambient temperature at the package cooling air intake (see Section 2.2)
- Degraded oil (extended service life, wrong grade, or contamination) with reduced heat transfer properties
- Thermostatic bypass valve (where fitted) stuck in a bypass position, routing oil around the cooler

**Recommended immediate steps:**
1. Check cooling air intake and discharge clearances per Section 2.2, particularly in a two-unit installation where one unit's discharge can elevate the other's intake temperature.
2. Inspect the oil cooler for external fouling.
3. Full diagnostic procedure: see Section 4.3.

### `OIL_PRESS_03` — Oil Injection Pressure Low (Differential)

**Severity:** Critical (auto-trip). Evaluated as the differential between the oil injection pressure and the airend discharge pressure, since it is this differential, not the absolute oil pressure, that drives oil flow into the airend for sealing, cooling, and lubrication.

**Likely causes:**
- Minimum pressure valve (Section 1.3) misconfigured or faulty, failing to maintain adequate vessel pressure at low capacity (see `MIN_PRESS_VALVE_18`)
- Oil filter fouling restricting oil flow
- Low oil level (see `OIL_LEVEL_LOW_04`)
- Operation at or below the minimum stable turndown point (Section 1.9) without a correctly configured minimum pressure valve
- Oil injection pressure transducer or discharge pressure transmitter fault (cross-check against `SENSOR_FAIL_15`)

**Recommended immediate steps:**
1. Do not continue operating a unit with a confirmed low oil injection differential; inadequate lubrication and cooling at the airend can cause rapid internal damage.
2. Full diagnostic procedure: see Section 4.4.

### `OIL_LEVEL_LOW_04` — Oil Reservoir Level Low

**Severity:** Warning; escalates to Critical (auto-trip) if level drops further toward the point where oil injection cannot be reliably sustained.

**Likely causes:**
- Oil leak at a fitting, seal, or the oil filter housing
- Carryover loss exceeding the oil separator's rated performance (see `SEP_DP_HIGH_08`, indicating a degraded separator element)
- Missed scheduled oil top-up or change interval (see Section 5.7)

**Recommended immediate steps:**
1. Inspect for visible external oil leakage before assuming the loss is entirely through separator carryover.
2. Check oil separator differential pressure and condition; an element near end of life allows increased carryover, which presents as a slow oil level decline without any visible external leak.

### `DISCH_PRESS_HIGH_05` — Discharge Pressure High

**Severity:** Warning.

**Likely causes:**
- Downstream control valve or dryer inlet valve closed or restricted
- Discharge pressure setpoint configured above the intended operating band (see Section 2.12)
- Discharge pressure transmitter fault or drift

**Recommended immediate steps:**
1. Confirm downstream valve positions and the configured setpoint against the Section 6 system sizing basis before assuming a fault.
2. Cross-check the reading against the sister unit's discharge pressure, since both units discharge into the same header and should read consistently.

### `HIGH_HIGH_PRESS_06` — High-High Discharge Pressure

**Severity:** Safety/Critical (immediate auto-trip), configured as a secondary electronic protection layer working alongside (not in place of) the mechanical pressure relief valve on the wet receiver.

**Likely causes:**
- A control system fault allowing discharge pressure to rise beyond the `DISCH_PRESS_HIGH_05` Warning threshold without the expected corrective control action occurring
- A downstream blockage severe enough to approach the vessel's mechanical relief valve set pressure
- Minimum pressure valve or check valve fault allowing unexpected pressure buildup

**Recommended immediate steps:**
1. Treat as a safety-significant event even though it is normally cleared by the electronic protection before the mechanical relief valve lifts; do not restart without identifying why the `DISCH_PRESS_HIGH_05` Warning stage did not prevent escalation to this point.
2. Inspect the mechanical relief valve for signs of having lifted, even briefly, and follow the site's relief valve inspection procedure if so.

### `DISCH_PRESS_LOW_07` — Discharge Pressure Low / System Demand Exceeds Capacity

**Severity:** Warning.

**Likely causes:**
- Plant air demand exceeding the combined capacity of Compressor-1 and Compressor-2 at their current lead/trim operating points
- Inlet filter fouling (see `INLET_FILT_DP_09`) reducing achievable capacity on one or both units
- A large, sudden demand event (a downstream process start-up) outpacing the trim unit's modulation response
- A capacity control fault preventing the trim unit from reaching full output when commanded (see `CAPACITY_FAULT_17`)
- An air leak somewhere in the distribution system downstream of the receivers

**Recommended immediate steps:**
1. Confirm both units are running and available, and that the trim unit is responding to a full-capacity command if plant demand requires it.
2. Check inlet filter differential pressure on both units.
3. Full diagnostic procedure: see Section 4.5. For the underlying capacity-planning perspective on this condition — distinguishing a genuine transient demand event from a chronic undersizing of the two-compressor system — see Section 6.

### `SEP_DP_HIGH_08` — Oil Separator Element Differential Pressure High

**Severity:** Warning.

**Likely causes:**
- Separator element approaching end of service life (normal fouling with operating hours)
- Oil degradation or contamination accelerating element fouling
- Operation significantly beyond the rated capacity or pressure, increasing element loading

**Recommended immediate steps:**
1. Compare current differential pressure against the clean-element baseline recorded at commissioning (Section 2.11).
2. Plan element replacement before differential pressure approaches the level associated with increased oil carryover and `OIL_LEVEL_LOW_04` risk.

### `INLET_FILT_DP_09` — Inlet Air Filter Differential Pressure High

**Severity:** Warning.

**Likely causes:**
- Normal dust/particulate loading on the filter element from ambient air
- Missed filter replacement interval (see Section 5.4)
- An unusually dusty ambient condition, for example from nearby construction or process activity

**Recommended immediate steps:**
1. Replace the filter element per Section 5.7 if differential pressure approaches the manufacturer's replacement threshold.
2. Recognize that inlet restriction reduces achievable capacity and elevates specific power (Section 1.9) even before the alarm threshold is reached, so a unit trending toward this alarm may already be contributing to a `DISCH_PRESS_LOW_07` condition under high plant demand before the filter alarm itself fires.

### `AFTERCOOLER_FOUL_10` — Aftercooler Fouling / High Approach Temperature

**Severity:** Warning. Evaluated as the difference between the aftercooler air outlet temperature and the ambient air temperature (the "approach temperature"), rather than the outlet temperature alone, since ambient temperature itself varies through the day and across seasons.

**Likely causes:**
- External fouling of the aftercooler fins (dust, oil mist deposits)
- Cooling fan fault or reduced airflow
- Elevated ambient temperature beyond a level the aftercooler was sized to fully compensate for (see Section 6)

**Recommended immediate steps:**
1. Inspect and clean aftercooler fins if visibly fouled.
2. Confirm cooling fan operation.
3. Distinguish a genuine fouling-driven approach temperature rise from an ambient-driven one by comparing the reading against the sister unit under similar load, since an ambient effect should appear on both units while fouling is typically unit-specific.

### `VIB_HIGH_11` — Excessive Vibration

**Severity:** Warning at ISO 10816-3 Zone C; Critical (auto-trip) at Zone D, either the airend or motor bearing housing.

**Likely causes:**
- Airend rotor wear or internal damage
- Motor bearing wear (shared instrumentation architecture with the MX-2200 Series motor line)
- Coupling condition, on the direct-coupled airend-to-motor connection
- Piping-transmitted vibration from an improperly installed flexible connector (see Section 2.6)
- Loose enclosure panels or mounting hardware (a frequent false-positive source)

**Recommended immediate steps:**
1. Confirm the vibration spectrum against the baseline signature recorded at commissioning (Section 2.11) to identify the dominant frequency component.
2. Full diagnostic procedure: see Section 4.6.

### `MOTOR_OVLD_12` — Motor Overload / Overcurrent

**Severity:** Critical (auto-trip).

**Likely causes:**
- Mechanical binding or internal airend damage
- Voltage imbalance across phases (see `PH_LOSS_13`)
- Operation at a discharge pressure above the rated setpoint range, increasing compression work and motor loading
- VFD parameter misconfiguration (incorrect current limit or motor nameplate data)

**Recommended immediate steps:**
1. Do not attempt an immediate restart after an overload trip without first checking for mechanical binding, with power isolated.
2. Full diagnostic procedure: see Section 4.7.

### `PH_LOSS_13` — Phase Loss / Voltage Imbalance

**Severity:** Critical (auto-trip).

**Likely causes:**
- Upstream breaker or fuse failure on one phase
- Loose or corroded terminal connection at the package main disconnect
- Utility supply fault or imbalance upstream of the plant switchgear

**Recommended immediate steps:**
1. Do not attempt to restart the unit until phase voltages have been confirmed balanced and within tolerance.
2. Full diagnostic procedure: see Section 4.8.

### `VFD_FAULT_14` — VFD Communication or Drive Fault

**Severity:** Critical (auto-trip, since loss of VFD control is treated as loss of capacity control).

**Likely causes:**
- Damaged or disconnected Modbus communication cable between the integral VFD and CompGuard controller
- VFD internal overtemperature fault
- VFD firmware fault or unexpected reset

**Recommended immediate steps:**
1. Check the VFD's own local fault display/log for a specific internal fault code before assuming a communications-only issue.
2. Confirm the sister unit can carry additional load if it is not already at full capacity, while the faulted unit is investigated.

### `SENSOR_FAIL_15` — Instrument/Sensor Signal Failure

**Severity:** Warning. Raised when any monitored instrument loop reads outside its physically valid range, rather than an in-range but abnormal process value.

**Likely causes:**
- Damaged signal cable or connector corrosion
- Failed transmitter or sensing element
- Moisture or oil mist ingress at a compromised enclosure seal

**Recommended immediate steps:**
1. Identify which specific instrument loop is flagged from the CompGuard alarm detail.
2. Note that a `SENSOR_FAIL_15` on a temperature, pressure, or vibration input disables the corresponding protective function for that input until cleared — treat this as reducing the unit's protection coverage, not merely as a nuisance alarm.

### `CONDENSATE_FAULT_16` — Automatic Condensate Drain Fault

**Severity:** Warning. Raised when the drain valve cycle behavior is inconsistent with expected operation — either failing to open when commanded (moisture accumulation risk) or failing to close (continuous air/oil loss risk).

**Likely causes:**
- Drain valve solenoid or mechanism fouling from oil/particulate accumulation
- Drain valve control circuit fault
- Drain line downstream blockage preventing the valve from fully discharging even when it opens correctly

**Recommended immediate steps:**
1. Determine whether the fault is a stuck-open (continuous discharge, audible air loss) or stuck-closed (no discharge cycle observed) condition, since the two have different urgency: a stuck-open condition wastes compressed air and should be corrected promptly, while a stuck-closed condition risks moisture carryover into the downstream system and should be corrected before the next scheduled dryer/filter inspection.
2. Manually cycle the drain valve (per the site's manual override procedure) to confirm mechanical operation while the automatic control fault is investigated.

### `CAPACITY_FAULT_17` — Capacity Control / Modulation Fault

**Severity:** Warning. Raised when the VFD's actual speed/capacity output does not track the commanded capacity control signal within a configured tolerance and duration.

**Likely causes:**
- VFD or control wiring fault between the CompGuard controller and the VFD
- Minimum pressure valve or check valve condition affecting achievable turndown (see `MIN_PRESS_VALVE_18`)
- A capacity control setpoint or control band misconfiguration inconsistent with the Section 6 system sizing basis

**Recommended immediate steps:**
1. Compare commanded versus actual capacity/speed at the CompGuard HMI to confirm the discrepancy and its magnitude.
2. Where the affected unit is currently in the trim role, confirm the base-load unit and overall system pressure are not being adversely affected while the fault is investigated (see Section 1.8, Section 6).

### `MIN_PRESS_VALVE_18` — Minimum Pressure Valve Fault

**Severity:** Warning; escalates to Critical if the resulting condition drives a sustained low oil injection differential pressure (`OIL_PRESS_03`).

**Likely causes:**
- Valve mechanism sticking (fully open, failing to maintain minimum vessel pressure at low capacity) or sticking closed (restricting flow and elevating pressure drop even at full capacity)
- Spring or pilot mechanism wear affecting the valve's cracking pressure setting
- Debris or oil varnish buildup affecting valve movement

**Recommended immediate steps:**
1. Cross-check current oil injection differential pressure trend (`OIL_PRESS_03` history) to assess urgency, since a minimum pressure valve fault that has not yet caused a low differential condition is lower urgency than one that has.
2. Inspect and service the valve at the next planned outage, or sooner if oil pressure trend indicates urgency.

### `STARTS_EXCEED_19` — Excessive Starts Per Hour

**Severity:** Warning. The CompGuard controller inhibits a further full stop/restart attempt once the configured starts-per-hour limit (Section 1.7, Section 2.12) is reached; VFD capacity modulation within a continuous run does not count toward this limit.

**Likely causes:**
- Repeated nuisance trips on another code causing repeated restart attempts
- A demand pattern causing the unit to fully stop and restart rather than modulate down to its minimum turndown point and idle there — see Section 6 for the capacity-planning perspective on this condition
- An operator or automatic sequence attempting rapid restart after a trip without allowing thermal margin to recover

**Recommended immediate steps:**
1. Identify and resolve the underlying cause of the repeated start attempts rather than simply waiting out the inhibit period and restarting.
2. Where the cause is a demand pattern rather than a fault, review the Section 6 sizing and sequencing basis rather than treating this as a maintenance issue on the affected unit alone.

### `ESTOP_ACT_20` — Emergency Stop Activated

**Severity:** Safety (immediate stop, no auto-trip delay).

**Likely causes:**
- Local E-Stop pushbutton manually pressed
- Safety interlock circuit fault
- An enclosure access panel interlock opened while the unit was running

**Recommended immediate steps:**
1. Do not reset or restart the unit until the cause of the E-Stop event has been positively identified.
2. Follow the lockout/tagout and restart authorization procedure in Section 7 (Appendix A) before returning the unit to service.

## 3.4 Alarm Acknowledgement, Reset, and Escalation

All twenty alarm codes follow a common lifecycle at the CompGuard controller, regardless of severity:

1. **Raise.** The controller detects the triggering condition and raises the alarm on the local HMI and to the plant DCS, with a timestamp and the triggering value logged to the historian.
2. **Acknowledge.** An operator or technician acknowledges the alarm at the HMI, silencing any audible annunciation. Acknowledgement does not clear the underlying condition and does not, by itself, permit a tripped unit to restart.
3. **Investigate.** The applicable procedure from Section 3.3 (summary) or Section 4 (full procedure, where available) is followed to identify and correct the root cause.
4. **Clear.** Once the underlying condition returns to within normal operating range, Warning-severity alarms clear automatically, while Critical- and Safety-severity alarms that caused an auto-trip require an explicit manual reset at the HMI before a restart can be commanded.
5. **Reset.** Manual reset of a Critical or Safety alarm should only be performed once the root cause has been identified and corrected — never as a first response to "see if it happens again."

**Nuisance alarm handling.** Where a specific alarm is confirmed, through the diagnostic procedures in Section 4 or the general principles in Section 4.1, to be a false trigger from a faulty sensor (`SENSOR_FAIL_15`) rather than a genuine process condition, the affected input may be temporarily forced to a safe bypass state by the site reliability engineer while the sensor is repaired or replaced. This bypass must be time-limited, documented in the maintenance record (Section 5.10), and reversed immediately once the sensor is restored.

**Escalation criteria.** Any alarm that recurs more than twice within a rolling 7-day period on the same unit, even if each individual event was successfully cleared, should be escalated from routine maintenance handling to a formal reliability review, since a recurring alarm indicates the underlying root cause was not actually resolved, only temporarily masked.

## 3.5 Threshold Configuration and Site Customization

The default thresholds referenced throughout this section (for example, the 100 °C/110 °C discharge temperature limits for `DISCH_TEMP_01`, or ISO 10816-3 Zone C/D for `VIB_HIGH_11`) are the MC-6100 Series factory defaults loaded during commissioning per Section 2.8.

- Thresholds tied to a published standard (ISO 10816-3 vibration zones, motor nameplate current for `MOTOR_OVLD_12`) should generally not be relaxed, since doing so directly reduces the equipment protection margin the standard is designed to preserve.
- Thresholds tied to site-specific conditions (discharge pressure setpoint and control band for `DISCH_PRESS_LOW_07`/`DISCH_PRESS_HIGH_05`, starts-per-hour limit for `STARTS_EXCEED_19`) may reasonably be tuned once sufficient operating history exists, provided the change is reviewed and approved by the site reliability engineer, is consistent with the Section 6 system sizing analysis, and is documented in the maintenance record (Section 5.10).
- Any threshold change must be applied consistently across Compressor-1 and Compressor-2, since these units alternate lead/trim roles (Section 1.8) and are compared against one another to distinguish unit-specific mechanical issues from fleet-wide supply-side or demand-pattern effects.
- Threshold changes should never be made as an undocumented workaround to stop a specific alarm from recurring; the correct response to a recurring alarm is the escalation path above, not a threshold relaxation that merely stops the symptom from being reported.

## 3.6 Detection Signature Reference

| Code | Primary Input(s) | Detection Logic |
|---|---|---|
| `DISCH_TEMP_01` | Airend discharge temperature sensor | Threshold-and-duration against Warning/Critical setpoint |
| `OIL_TEMP_02` | Oil temperature sensor | Threshold-and-duration against Warning/Critical setpoint |
| `OIL_PRESS_03` | Oil injection pressure transducer, discharge pressure transmitter | Calculated differential pressure below configured minimum |
| `OIL_LEVEL_LOW_04` | Oil reservoir level sensor | Threshold-and-duration below configured minimum level |
| `DISCH_PRESS_HIGH_05` / `DISCH_PRESS_LOW_07` | Discharge pressure transmitter | Threshold deviation from the configured setpoint/control band |
| `HIGH_HIGH_PRESS_06` | Discharge pressure transmitter (independent high-set channel) | Threshold above the `DISCH_PRESS_HIGH_05` level, configured as a secondary electronic protection layer |
| `SEP_DP_HIGH_08` | Oil separator differential pressure transmitter | Threshold deviation from clean-element baseline |
| `INLET_FILT_DP_09` | Inlet filter differential pressure transmitter | Threshold deviation from clean-element baseline |
| `AFTERCOOLER_FOUL_10` | Aftercooler outlet temperature sensor, ambient reference | Calculated approach temperature above configured maximum |
| `VIB_HIGH_11` | Airend and motor bearing housing accelerometers | Overall vibration amplitude classified against ISO 10816-3 zone boundaries |
| `MOTOR_OVLD_12` | VFD current feedback | Threshold-and-duration above configured current limit |
| `PH_LOSS_13` | VFD input voltage sensing | Phase-to-phase voltage comparison against balance tolerance |
| `VFD_FAULT_14` | VFD internal diagnostics via Modbus | Drive-reported fault code or loss of Modbus communication |
| `SENSOR_FAIL_15` | Any monitored instrument loop | Out-of-physical-range signal (open or short circuit) |
| `CONDENSATE_FAULT_16` | Drain valve cycle/position feedback | Cycle pattern inconsistent with expected open/close behavior |
| `CAPACITY_FAULT_17` | VFD commanded vs. actual capacity/speed feedback | Percentage deviation threshold sustained over a configured duration |
| `MIN_PRESS_VALVE_18` | Inferred from oil injection pressure trend at low capacity | Pattern analysis correlating valve position/capacity state with resulting oil pressure margin |
| `STARTS_EXCEED_19` | VFD run-command counter | Rolling-hour full stop/restart count against configured limit |
| `ESTOP_ACT_20` | Local E-Stop circuit / safety relay | Hardwired safety circuit state, independent of CompGuard software logic |

Because `SENSOR_FAIL_15` and `ESTOP_ACT_20` are architecturally distinct from the process-condition alarms (the former detects a signal validity problem across any loop, the latter is a hardwired safety circuit rather than a software threshold), neither can itself be dismissed as a nuisance alarm caused by another sensor fault in the way that, for example, an isolated `DISCH_TEMP_01` reading might be — both should always be treated as reported.

## 3.7 Pressure-Related Codes and This Manual's Two Perspectives

Three of the twenty codes in this section — `DISCH_PRESS_LOW_07`, `DISCH_PRESS_HIGH_05`, and `CAPACITY_FAULT_17` — are deliberately covered from two different angles across this manual, and it is worth being explicit about the distinction so a reader is not confused when finding what looks like overlapping content in two places. This section (Section 3, together with the diagnostic procedure in Section 4.5) covers `DISCH_PRESS_LOW_07` from an **alarm-response perspective**: what the CompGuard controller detected, how severe it is, and what to check once the alarm is already active — valve positions, filter fouling, a capacity control fault, or a genuine transient demand spike. Section 6 (System Sizing & Duty Cycle) covers the same underlying pressure-shortfall phenomenon from a **capacity-planning perspective**: whether the combined installed capacity of Compressor-1 and Compressor-2, the receiver sizing, and the lead/trim sequencing strategy are actually adequate for the site's demand profile in the first place, independent of any single fault event.

A technician responding to an active `DISCH_PRESS_LOW_07` alarm should use Section 4.5 first, since it is written specifically for that in-the-moment diagnostic sequence. A reliability engineer or plant engineer trying to understand why this alarm recurs periodically even when no fault is ever found should read Section 6, since that is where the underlying capacity and demand-matching factors are addressed. Both sections cross-reference each other for exactly this reason, and neither is a substitute for the other.

---

# Section 4: Detailed Troubleshooting Procedures

This section expands seven of the twenty alarm codes from Section 3 into full step-by-step diagnostic procedures: `DISCH_TEMP_01`, `OIL_TEMP_02`, `OIL_PRESS_03`, `DISCH_PRESS_LOW_07`, `VIB_HIGH_11`, `MOTOR_OVLD_12`, and `PH_LOSS_13`. These seven were selected because they represent the highest-frequency and highest-consequence alarm events observed across the MC-6100 Series install base, and because several of them (notably `DISCH_TEMP_01`, `OIL_TEMP_02`, and `OIL_PRESS_03`) are frequently root-caused to a common set of underlying conditions in the oil system — so diagnosing one thoroughly often resolves or prevents another.

Each procedure assumes the technician has reviewed the corresponding summary entry in Section 3 and has basic access to the CompGuard local HMI and historian trend data.

## 4.1 General Diagnostic Principles

Before following any of the specific procedures below, apply these general principles, which hold across nearly all alarm conditions on the MC-6100 Series:

- **Confirm before correcting.** A meaningful fraction of alarms on any rotating equipment fleet trace back to a faulty sensor rather than a genuine process condition (see `SENSOR_FAIL_15`). Always cross-check a suspect reading against a second sensor, a handheld instrument, or a physical inspection before taking corrective action on the equipment itself.
- **Check the historian trend, not just the instantaneous value.** A slowly rising trend over days or weeks points to a different class of root cause (fouling, oil degradation, filter loading) than a sudden step change (sensor fault, mechanical failure, external event).
- **Consider the unit's current lead/trim role.** Because Compressor-1 and Compressor-2 alternate lead/trim roles (Section 1.8), a unit's recent operating pattern — continuous full load versus frequent modulation — should be checked before comparing its readings to its sister unit or to its own historical baseline, since the two roles are not directly comparable without accounting for this difference.
- **Record findings against the unit's individual commissioning baseline** (Section 2.11), not against a generic specification, since minor unit-to-unit variation is normal and expected.

## 4.2 `DISCH_TEMP_01` — Discharge Air Temperature High: Diagnostic Procedure

1. **Verify the alarm.** At the CompGuard HMI, note the peak discharge air temperature reached and whether the unit auto-tripped at the Critical threshold (110 °C) or remains running at the Warning threshold (100 °C).
2. **Cross-check the reading against oil temperature** (`OIL_TEMP_02`). Discharge air temperature and oil temperature are closely linked on an oil-flooded screw compressor, since the injected oil is the primary cooling mechanism for the compression process; a discharge temperature alarm with a normal oil temperature reading should raise suspicion of a sensor or wiring fault (see Section 2.13) rather than a genuine airend condition.
3. **Review the trend.** A gradual rise over days or weeks suggests a developing cooling deficiency (oil cooler fouling, cooling fan degradation) or oil degradation; a step change coincident with a specific event points to that event as the likely trigger.
4. **Check oil injection differential pressure** (`OIL_PRESS_03`). Reduced oil flow to the airend directly elevates discharge temperature, and a low differential pressure condition should be ruled out before pursuing a cooling-system-only explanation.
5. **Check oil cooler condition and cooling fan operation.** Inspect for external fouling on the cooler fins, and confirm the fan runs and produces expected airflow.
6. **Check cooling air intake/discharge separation** (Section 2.2) between Compressor-1 and Compressor-2. Where the two units are installed close together, confirm one unit's cooling air discharge is not being drawn into the other's intake, particularly if both units show an elevated discharge temperature trend simultaneously.
7. **If no cooling or oil-flow cause is found**, consider airend internal wear as a longer-term possibility; schedule an airend inspection at the next planned outage rather than continuing to operate a unit with a chronically elevated, unexplained discharge temperature.
8. **Document** the finding, corrective action, and post-correction temperature trend in the unit's maintenance history.

## 4.3 `OIL_TEMP_02` — Oil Temperature High: Diagnostic Procedure

1. **Verify the alarm** and note the peak oil temperature reached and whether the unit auto-tripped at the Critical threshold (100 °C) or remains running at the Warning threshold (90 °C).
2. **Inspect the oil cooler** for external fouling (dust, oil mist deposits on the fins) — this is the single most common recoverable root cause of `OIL_TEMP_02` on the MC-6100 Series and should be checked before more invasive investigation.
3. **Confirm cooling fan operation**, including actual airflow, not just that the fan is electrically running, since a fan with a damaged or fouled blade can draw normal current while producing significantly reduced airflow.
4. **Check oil level** (`OIL_LEVEL_LOW_04`). A low oil charge reduces the system's thermal mass and can elevate operating temperature even with a fully functional cooler.
5. **Check for a thermostatic bypass valve fault** (where fitted), which can route oil around the cooler even when the cooler itself is functioning correctly; a unit with a confirmed clean, functional cooler and fan but still trending hot should have this valve inspected next.
6. **Compare against the sister unit under an equivalent lead/trim role and load** (Section 4.1) to help distinguish a unit-specific fault from a shared ambient or cooling-air-recirculation effect (Section 2.2).
7. **Check oil condition and service interval** (Section 5.7). Degraded or overdue oil has reduced heat transfer properties and should be ruled out, particularly on a unit approaching or past its scheduled oil change interval.
8. **Document** the finding, corrective action, and post-correction temperature trend.

## 4.4 `OIL_PRESS_03` — Oil Injection Pressure Low: Diagnostic Procedure

1. **Verify the alarm** and note the calculated oil injection differential pressure at the time of the trip, and the capacity/speed the unit was operating at when the condition occurred.
2. **Check whether the event occurred at or near the minimum turndown point** (Section 1.9). If so, this points strongly toward the minimum pressure valve (`MIN_PRESS_VALVE_18`) as the likely root cause, since low-capacity operation is precisely the condition this valve exists to protect against.
3. **Inspect the minimum pressure valve** for correct cracking pressure setting and mechanical condition, cross-referencing the Section 2.7 Step 4 and Section 2.12 commissioning configuration record.
4. **Check oil filter condition.** A fouled oil filter restricts flow and can produce a low injection differential pressure even with a fully functional minimum pressure valve; compare current filter differential pressure against the maintenance record if a differential pressure reading is available for the filter specifically, or inspect the element directly if not.
5. **Check oil level** (`OIL_LEVEL_LOW_04`). Confirm the reservoir has adequate oil to sustain flow before investigating further into the oil circuit.
6. **Cross-check the oil injection pressure transducer and discharge pressure transmitter** against `SENSOR_FAIL_15` history, since this alarm is calculated from two separate instrument readings and a fault on either one can produce a false low-differential calculation.
7. **Do not restart or continue operating a unit with a confirmed genuine low oil injection differential**; inadequate lubrication and cooling at the airend from insufficient oil flow can cause rapid, severe internal damage, unlike some of the other Warning-level conditions in this manual where continued short-term operation is acceptable while the root cause is investigated.
8. **Document** the root cause and corrective action; if the minimum pressure valve was found at fault, verify correct behavior across the full capacity turndown range (Section 1.9) before returning the unit to unattended automatic operation, not just at the single operating point where the alarm occurred.

**Worked example.** Suppose Compressor-2, currently in the trim role, trips on `OIL_PRESS_03` while operating at 42% capacity — just above its 40% minimum stable turndown point. Step 2 of this procedure directs attention to the minimum pressure valve first, since the event occurred near minimum turndown. Inspection finds the valve's cracking pressure has drifted below its commissioned setting (Section 2.12), likely from gradual spring wear rather than any sudden failure. Because Compressor-2 has spent a disproportionate share of recent operating time in the trim role (per the Section 1.8 role-alternation schedule having been extended past its normal 336-hour interval due to a scheduling oversight), this unit has accumulated more time near minimum turndown than Compressor-1 over the same period — directly illustrating the Section 6.5 duty-cycle-driven wear asymmetry. The corrective action is twofold: replace or re-set the minimum pressure valve per Step 8 above, and separately flag the role-alternation lapse for correction per Section 1.8, since the valve wear itself is a symptom of the uncorrected duty-cycle imbalance, not an isolated component failure unrelated to it.

## 4.5 `DISCH_PRESS_LOW_07` — Discharge Pressure Low / System Demand Exceeds Capacity: Diagnostic Procedure

1. **Confirm the alarm** and note the discharge pressure reading against the configured setpoint and control band (Section 2.12).
2. **Confirm both units are running and available.** If one unit is out of service (planned maintenance or an unresolved fault), the remaining single unit's capacity may simply be inadequate for current plant demand — this is an expected consequence of single-unit operation, not necessarily a new fault on the running unit.
3. **Check whether the trim unit is responding to a full-capacity command.** If the trim unit is commanded to full output but not reaching it, cross-check `CAPACITY_FAULT_17` history before assuming the shortfall is purely a demand-side issue.
4. **Check inlet filter differential pressure on both units** (`INLET_FILT_DP_09`). A heavily loaded filter reduces achievable capacity in the same way a valve restriction would, and this reduction can be significant enough to matter under peak demand even before the filter alarm threshold itself is reached.
5. **Check for a large, sudden, and genuinely transient demand event** — a downstream process start-up or a similar known event — using the plant DCS event log or operations log, since a transient event that resolves on its own within a few minutes does not require the same investigation as a sustained shortfall.
6. **If the condition persists beyond a transient event and both units are confirmed running at full available capacity**, this is evidence of a capacity/demand mismatch at the system level rather than a unit-specific fault; proceed to the Section 6 system sizing and duty cycle discussion rather than continuing to search for an equipment fault that may not exist.
7. **Check for a distribution-system air leak** downstream of the receivers, particularly if the shortfall has developed gradually over weeks or months rather than appearing suddenly, since a growing leak load has the same effect on discharge pressure as a growing demand and is easily conflated with a genuine demand increase.
8. **Document** whether the root cause was equipment-related (a specific unit or component fault), transient (a known demand event), or systemic (a persistent capacity/demand mismatch), since the appropriate corrective action differs sharply between the three.

## 4.6 `VIB_HIGH_11` — Excessive Vibration: Diagnostic Procedure

1. **Confirm the alarm** and note which bearing housing (airend or motor), the peak amplitude reached, and the ISO 10816-3 zone (Warning = Zone C, Critical = Zone D).
2. **Pull the vibration spectrum** (not just overall amplitude) from the CompGuard historian and identify the dominant frequency component:
   - **1x running speed** — most consistent with rotor imbalance, on either the airend or motor rotor.
   - **2x running speed** — most consistent with coupling condition, on the direct-coupled airend-to-motor connection.
   - **Airend meshing frequency** (calculated from rotor lobe count and running speed) — consistent with airend internal wear or damage.
   - **Bearing defect frequencies** — consistent with bearing wear on either the airend or motor bearing housing.
   - **Broadband, no clear dominant frequency** — consider loose enclosure panels or mounting hardware, or a piping-transmitted vibration path from an improperly installed flexible connector (Section 2.6).
3. **Compare against the commissioning baseline spectrum** (Section 2.11) to determine whether this is a new frequency component or a growth in amplitude of a component already present at low level.
4. **If 1x or 2x dominant:** perform a physical inspection walk-down, checking enclosure panel security and the flexible discharge connector installation (Section 2.6), before considering a coupling or balance investigation.
5. **If airend meshing frequency dominant:** treat as an indicator of internal airend wear or damage and schedule an airend inspection promptly, since this signature does not typically respond to any external correction.
6. **If bearing-defect frequency dominant:** identify which bearing housing (airend or motor) is affected and schedule the corresponding component for inspection or replacement.
7. **If the unit auto-tripped at Critical (Zone D):** do not restart until at least a visual inspection and spectral review have been completed.
8. **Document** the spectral signature and corrective action for trend comparison at the next alarm event.

**Worked example.** Suppose Compressor-1 raises `VIB_HIGH_11` at the airend drive-end housing, Warning zone. Pulling the spectrum per Step 2 shows the dominant component at approximately twice running speed rather than at 1x, with no significant component at the calculated airend meshing frequency or at any known bearing defect frequency. Per Step 4, this 2x signature points toward a physical inspection walk-down before pursuing any balance-related correction. The walk-down finds the discharge flexible connector (Section 2.6) installed with a slight offset rather than fully in-line, likely introduced when the connector was disturbed during an unrelated piping modification several weeks earlier and not re-verified afterward. Correcting the connector installation and re-running the vibration check confirms the 2x component drops back within the Zone A/B baseline range. This example illustrates why Step 4 directs a physical walk-down before an alignment or balance investigation specifically for a 2x-dominant signature: on a direct-coupled package with no separate coupling alignment procedure of its own (unlike the multi-piece machine trains documented elsewhere in the MechMind fleet), a piping-side installation issue is at least as likely a source of this signature as a coupling condition issue, and is often faster to rule out first.

## 4.7 `MOTOR_OVLD_12` — Motor Overload / Overcurrent: Diagnostic Procedure

1. **Confirm the alarm** and pull the motor current trend from the VFD/CompGuard historian for the minutes leading up to the trip, noting whether current rose gradually or stepped up suddenly.
2. **Before any restart attempt, isolate electrical power and check for mechanical binding** at the airend, where a manual rotation check point is provided, per the site's lockout procedure (Section 7).
3. **If no mechanical binding is found**, review recent `PH_LOSS_13` history for any voltage imbalance event coincident with or preceding the overload.
4. **Check whether the unit was operating at a discharge pressure above its configured setpoint range** at the time of the trip, since operation against an abnormally high system pressure increases compression work and motor loading independent of any mechanical fault.
5. **If no phase imbalance or high-pressure operating condition is found**, verify VFD configuration parameters (current limit, motor nameplate data) against the values specified in Section 2.12 to rule out a configuration fault.
6. **If mechanical binding is confirmed**, this indicates airend or bearing damage requiring further disassembly to locate; cross-check recent `VIB_HIGH_11` or oil-system alarm history for a prior indication that may have gone unaddressed.
7. **Once the root cause is corrected**, restart at reduced capacity if possible and ramp gradually to full load while monitoring current.
8. **Document** the root cause; a mechanical bind finding should trigger a full airend inspection at the next outage even if the immediate obstruction is cleared.

## 4.8 `PH_LOSS_13` — Phase Loss / Voltage Imbalance: Diagnostic Procedure

1. **Confirm the alarm** and note which phase(s) were affected and the magnitude of imbalance or the specific phase reported lost.
2. **Do not restart the unit** until phase voltages have been measured and confirmed balanced and within tolerance at the package main disconnect, since restarting into a genuine phase-loss condition risks immediate `MOTOR_OVLD_12` and potential winding damage.
3. **Check the upstream breaker or fuse** for the affected unit's circuit for a tripped or blown condition on a single phase — this is the most common single-unit root cause.
4. **If the breaker/fuse is intact**, check terminal connections at the package main disconnect for looseness or corrosion.
5. **Check whether the sister unit or other loads on the same electrical bus experienced a coincident event.** A simultaneous event across multiple units points to an upstream supply-side fault rather than a fault local to the single unit, and should be escalated to the electrical/utility team.
6. **Once the fault is corrected and phase voltages confirmed balanced**, restart per the standard start-up sequence (Section 2.10), monitoring current closely through the loading sequence.
7. **Document** whether the event was isolated to one unit or affected multiple units on the same bus.

## 4.9 Cross-Cutting Root Cause Relationships

The seven procedures above are presented as independent alarm responses, but in practice a small number of underlying conditions are shared root causes across several of them:

- **Cooling system condition** links `DISCH_TEMP_01` (Section 4.2) and `OIL_TEMP_02` (Section 4.3) directly, since the injected oil is the primary cooling mechanism for the compression process on an oil-flooded screw airend — a fouled oil cooler or degraded cooling fan typically presents on both codes together, or on one shortly after the other, rather than in isolation.
- **Oil circuit health** connects `OIL_PRESS_03` (Section 4.4), `OIL_LEVEL_LOW_04`, and `SEP_DP_HIGH_08` as a single system: a fouled oil filter or degrading separator element can each independently reduce effective oil flow or increase carryover loss, and a unit presenting any one of these should have the others checked as part of the same investigation rather than treated as unrelated findings.
- **Minimum pressure valve condition** links `OIL_PRESS_03` (Section 4.4) and `MIN_PRESS_VALVE_18` particularly at low capacity operation — a unit whose trim-role duty cycle involves extended periods near the minimum turndown point (Section 1.9, Section 6) is more exposed to a marginal minimum pressure valve condition than a unit that spends most of its time at or near full load.
- **Electrical supply quality** connects `PH_LOSS_13` (Section 4.8) and `MOTOR_OVLD_12` (Section 4.7): a voltage imbalance event that does not itself reach the phase-loss threshold can still elevate motor current enough to approach an overload trip.

## 4.10 Post-Repair Verification and Return-to-Service Checklist

Regardless of which of the seven procedures above was followed, the following verification steps apply generally before returning a unit to automatic lead/trim sequencing after any Critical or Safety alarm event:

1. **Confirm the specific corrective action taken** is recorded against the unit and the alarm code in the maintenance record (Section 5.10), including parts replaced, adjustments made, and any threshold or configuration changes per Section 3.5.
2. **Run the unit at reduced capacity first**, where process conditions allow, rather than commanding full load immediately on restart, so that early signs of an incomplete repair are observed under lower mechanical and thermal stress.
3. **Exercise the full capacity turndown range** (Section 1.9) before releasing the unit to unattended automatic sequencing, particularly following any oil-system-related repair, since a repair verified only at full load may not reveal a condition — such as a marginal minimum pressure valve — that only manifests at reduced capacity.
4. **Monitor continuously for the first two hours of operation following any oil-system or vibration-related repair**, since infant-mortality failures of a freshly repaired or replaced component typically present within this window.
5. **Compare post-repair readings against the unit's own commissioning baseline** (Section 2.11) rather than against a generic specification.
6. **Re-arm all bypassed instrument inputs** (Section 3.4, nuisance alarm handling) that may have been temporarily forced to a safe state during the investigation, and confirm each shows a valid, in-range reading before the unit is released to service.

## 4.11 Tools and Instruments Required

| Tool/Instrument | Used In | Notes |
|---|---|---|
| Handheld infrared thermometer | Sections 4.2, 4.3 | For cross-checking discharge and oil temperature readings against a physical measurement |
| Vibration analyzer with spectral (FFT) capability | Section 4.6, Section 3.6 | Overall-amplitude-only meters are insufficient for the spectral diagnosis described in Section 4.6 Step 2 |
| Clamp-on multimeter / phase rotation tester | Sections 4.7, 4.8, 2.5 | For motor current and phase voltage verification |
| Portable differential pressure gauge | Sections 4.4, 4.5 | For spot-checking oil filter and inlet filter differential pressure where a permanent transmitter reading is in question |
| Oil sampling kit | Section 4.3 Step 7 | For oil condition assessment against the Section 5.7 service interval |
| CompGuard historian workstation access | All seven procedures | Required for trend review; field investigation without historian access should be considered incomplete per Section 4.1 |

## 4.12 Common Diagnostic Mistakes to Avoid

The following mistakes recur often enough across the seven procedures in this section to call out explicitly, since each one has been observed to significantly extend investigation time or, in some cases, to cause a repeat failure of the same alarm shortly after an apparently successful correction:

- **Resetting and restarting a Critical alarm without a specific corrective action.** This is addressed in Section 3.4, but bears repeating here: an `OIL_PRESS_03` or `MOTOR_OVLD_12` trip that is reset and restarted purely because "it might not happen again" discards the diagnostic value of the trip and, for `OIL_PRESS_03` specifically, risks rapid airend damage from a genuinely under-lubricated restart.
- **Treating `DISCH_TEMP_01` as an airend condition without first checking `OIL_TEMP_02`.** Because the two readings are closely linked through the oil cooling mechanism, investigating discharge temperature in isolation, without the oil temperature cross-check in Section 4.2 Step 2, risks missing a simple cooling-system cause and proceeding directly to a more invasive airend investigation that was not yet warranted.
- **Investigating an `OIL_PRESS_03` event without first checking whether it occurred near the minimum turndown point.** As illustrated in the Section 4.4 worked example, this single piece of context — capacity at the time of the event — often points directly to the minimum pressure valve as the most likely cause and should be checked before a broader oil-circuit investigation begins.
- **Treating a chronic, recurring `DISCH_PRESS_LOW_07` as a series of unrelated fault investigations.** As discussed in Section 3.7 and Section 6.6, repeated "no fault found" conclusions on this code are themselves useful information pointing toward a system sizing or sequencing issue, not toward the need for a more thorough equipment inspection each time.
- **Comparing Compressor-1 and Compressor-2 readings without accounting for their current lead/trim roles.** As emphasized in Section 4.1, a direct comparison that ignores which unit was in which role during the period being compared can produce a misleading conclusion about unit-specific condition.

---

# Section 5: Routine Maintenance Schedule

## 5.1 Maintenance Philosophy

The MC-6100 Series maintenance schedule combines fixed-interval preventive tasks (filter and element replacement, oil service, inspection) with condition-based tasks driven by CompGuard trend data (differential pressures, temperatures, vibration). Fixed intervals below are the minimum required frequency; any unit trending toward an alarm threshold ahead of schedule (per Section 4 diagnostic procedures) should have its maintenance interval shortened accordingly rather than waiting for the next scheduled date.

Because Compressor-1 and Compressor-2 alternate lead/trim roles (Section 1.8) rather than one running continuously as duty and the other standing idle, maintenance intervals in this schedule are based on accumulated run hours per unit rather than calendar time alone, and the CompGuard historian should be consulted for actual run hours before scheduling hour-based tasks, since the two units will not necessarily reach a given run-hour milestone on the same calendar date.

## 5.2 Daily Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Visual walk-down | Inspect for visible oil leaks, unusual discoloration, or debris accumulation | `OIL_LEVEL_LOW_04` |
| Unusual noise/vibration | Listen for abnormal noise; note any change from baseline | `VIB_HIGH_11` |
| CompGuard HMI review | Confirm no active or unacknowledged alarms on either unit | All codes |
| Condensate drain check | Visually confirm drain valve is cycling normally | `CONDENSATE_FAULT_16` |
| Oil level sight glass | Visually confirm oil level within normal range | `OIL_LEVEL_LOW_04` |

## 5.3 Weekly Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Vibration trend review | Review 7-day vibration trend for both units at the CompGuard historian | `VIB_HIGH_11` |
| Discharge and oil temperature trend review | Review 7-day trend for both readings | `DISCH_TEMP_01`, `OIL_TEMP_02` |
| Oil injection differential pressure trend | Review for gradual decline, particularly on the unit currently in the trim role | `OIL_PRESS_03` |
| Inlet filter and separator differential pressure | Compare against clean-element baseline | `INLET_FILT_DP_09`, `SEP_DP_HIGH_08` |
| Motor current trend | Review for gradual upward drift | `MOTOR_OVLD_12` |

## 5.4 Monthly Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Inlet air filter inspection | Inspect element; replace if differential pressure approaches replacement threshold | `INLET_FILT_DP_09` |
| Oil cooler and aftercooler external cleaning | Inspect and clean fins if fouled | `OIL_TEMP_02`, `AFTERCOOLER_FOUL_10` |
| Condensate drain function test | Manually cycle drain valve to confirm mechanical operation | `CONDENSATE_FAULT_16` |
| Instrument loop spot-check | Verify one monitored loop per visit against a reference reading | `SENSOR_FAIL_15` |
| Lead/trim role and starts-per-hour history review | Confirm role alternation is occurring per Section 1.8 and no unit is approaching the `STARTS_EXCEED_19` limit | `STARTS_EXCEED_19` |

## 5.5 Quarterly Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Oil separator element differential pressure trend review | Full trend comparison against commissioning baseline; replace if approaching end-of-life threshold | `SEP_DP_HIGH_08` |
| Oil sample analysis | Laboratory or portable analysis for oxidation, contamination, and viscosity against Section 5.7 acceptance criteria | `OIL_TEMP_02`, `OIL_PRESS_03` |
| Vibration spectral baseline comparison | Full spectrum analysis against commissioning baseline (Section 2.11), not just overall amplitude | `VIB_HIGH_11` |
| Minimum pressure valve function check | Verify correct operation across the full capacity turndown range (Section 1.9) | `MIN_PRESS_VALVE_18`, `OIL_PRESS_03` |
| Electrical connection torque check | Verify main disconnect and terminal torque per Section 5.8 | `PH_LOSS_13`, `MOTOR_OVLD_12` |

## 5.6 Annual Checks / Major Overhaul Planning

| Task | Action | Related Alarm Codes |
|---|---|---|
| Full oil change | Drain and refill per Section 5.7 specification, regardless of oil sample results at the time | `OIL_TEMP_02`, `OIL_PRESS_03` |
| Oil separator element replacement | Replace regardless of current differential pressure reading, per planned service life | `SEP_DP_HIGH_08` |
| Airend inspection | Inspect rotor condition and clearances where accessible without full teardown; escalate to major overhaul if wear indicators are present | `VIB_HIGH_11`, `DISCH_TEMP_01` |
| Full performance verification | Re-run the commissioning performance verification (Section 2.11) at multiple capacity points across the turndown range | All codes related to capacity and thermal performance |
| CompGuard controller calibration | Full instrument loop calibration check, all inputs | `SENSOR_FAIL_15` |
| VFD parameter audit | Confirm all Section 2.12 parameters remain as commissioned | `MOTOR_OVLD_12`, `CAPACITY_FAULT_17`, `STARTS_EXCEED_19` |

## 5.7 Lubrication and Fluid Specifications

| Item | Specification | Interval |
|---|---|---|
| Compressor lubricant | ISO VG46 compressor-rated synthetic or mineral lubricant per the oil charge specification in Section 1.4 | Full change annually (Section 5.6), or immediately upon confirmed contamination |
| Oil sample analysis acceptance criteria | Viscosity within 10% of new-oil baseline; no significant water content; particle count within the manufacturer's rated limit | Quarterly (Section 5.5) |
| Oil filter element | Manufacturer-specified replacement element | Concurrent with each oil change, or sooner if differential pressure indicates fouling |

Using a lubricant other than the specified ISO VG46 grade, including a substitution that appears equivalent on a general specification sheet, risks both accelerated oil separator fouling (contributing to `SEP_DP_HIGH_08`) and reduced elastomer compatibility with seals throughout the oil circuit; any substitution should be reviewed against the compressor manufacturer's approved lubricant list before use, not approved solely on the basis of a matching viscosity grade.

## 5.8 Torque Specifications (Key Fasteners)

| Fastener | Torque |
|---|---|
| Package main disconnect terminal lugs | Per motor manufacturer nameplate/data sheet — verify at each quarterly electrical check (Section 5.5) |
| Skid-to-floor anchor bolts (where used) | 175 N·m |
| Discharge flexible connector flange bolts | 95 N·m |
| Oil filter housing | Per filter manufacturer specification — typically hand-tight plus a specified fraction of a turn, not a fixed torque value |
| Enclosure access panel fasteners | 15 N·m |

## 5.9 Recommended Spare Parts and Insurance Spares

| Part | Recommended Quantity On-Hand | Rationale |
|---|---|---|
| Oil separator element | 1 per unit (2 total) | Directly tied to `SEP_DP_HIGH_08` and downstream `OIL_LEVEL_LOW_04` risk from carryover |
| Inlet air filter element | 2 per unit | Low cost, consumable item with a relatively short service life |
| Oil filter element | 2 per unit | Consumable item, concurrent with oil changes |
| Minimum pressure valve (complete assembly) | 1, shared across the fleet | Directly tied to `OIL_PRESS_03` and `MIN_PRESS_VALVE_18`; a fault here risks rapid airend damage if not corrected promptly |
| CompGuard controller (spare unit) | 1, shared across the fleet | Minimizes downtime from a `VFD_FAULT_14`-adjacent controller hardware fault |
| Full oil charge (110 L) | 1 charge on hand | Supports an unplanned full oil change without a procurement delay |

Typical procurement lead times mirror those of comparable rotating equipment components elsewhere in the MechMind fleet: filter and separator elements are generally available within 1–2 weeks, while the CompGuard controller carries a longer 6–10 week lead time and should be treated as a priority stocking item, consistent with the equivalent guidance for the PumpGuard and MotorGuard controller platforms.

## 5.10 Maintenance Record Keeping

All maintenance actions, whether scheduled or triggered by an alarm event under Section 4, must be logged against the specific unit tag (Compressor-1 or Compressor-2) in the site CMMS, cross-referenced to the relevant alarm code where applicable, and tagged with the unit's lead/trim role at the time of the event (Section 1.8). This last point is specific to the compressor fleet's operating pattern: without recording which role a unit was performing, a later reviewer cannot correctly interpret why, for example, one unit shows a different starts-per-hour history than the other over a given period.

## 5.11 Consumables, Waste Handling, and Disposal

- **Used compressor lubricant** from the annual oil change (Section 5.6) should be collected and disposed of per the site's lubricant waste stream.
- **Removed oil separator and filter elements** should be handled as oil-contaminated waste per the site's procedure, since even a "spent" separator element retains a meaningful oil content.
- **Condensate drained from the wet receiver** contains residual oil carryover (Section 1.7) and must be routed through the site's oil/water separator system (Section 2.4) rather than to an unoiled drain, regardless of how the drain valve fault history (`CONDENSATE_FAULT_16`) for the unit has been.

## 5.12 Condition Monitoring Review Cadence

| Review | Frequency | Purpose |
|---|---|---|
| Cross-unit comparison review | Monthly | Compare discharge/oil temperature, vibration, and motor current baselines between Compressor-1 and Compressor-2, correcting for lead/trim role per Section 4.1 |
| Trend-code review (`SEP_DP_HIGH_08`, `INLET_FILT_DP_09`, oil sample trends) | Monthly | Confirm these early-warning trends are being acted on before they progress to a Critical alarm |
| Alarm recurrence review | Monthly | Apply the escalation criteria in Section 3.4 across the full alarm history |
| Lead/trim role balance review | Monthly | Confirm role alternation (Section 1.8) is actually occurring as configured, not just theoretically enabled |
| Full commissioning-baseline re-comparison | Annual, aligned with Section 5.6 | Confirm each unit's current performance and vibration/temperature baseline against its original Section 2.11 commissioning record |

## 5.13 Ambient Temperature Effects on Cooling Maintenance Intervals

The fixed-interval schedule in Sections 5.2 through 5.6 applies year-round, but ambient temperature has a direct effect on cooling-related fouling and thermal margin that should inform how strictly those intervals are followed:

- **Ahead of the summer high-ambient period**, bring forward the monthly oil cooler and aftercooler external cleaning (Section 5.4) if the preceding period showed any external fouling, since reduced cooling margin from ambient heat compounds with any residual fouling to increase `DISCH_TEMP_01`, `OIL_TEMP_02`, and `AFTERCOOLER_FOUL_10` risk during the warmest months, particularly on whichever unit is currently in the base-load role and therefore running continuously at full thermal load.
- **During any period of unusually high ambient temperature relative to the site's normal seasonal range**, increase the frequency of the weekly discharge and oil temperature trend review (Section 5.3) to a shorter interval until conditions return to normal, so that a genuine cooling-system fault emerging during a period of ambient stress is not masked by, or confused with, an expected ambient-driven baseline shift shared across both units.
- **A simultaneous rise in discharge and oil temperature baseline across both Compressor-1 and Compressor-2**, without either unit showing a corresponding rise in cooler fouling or fan degradation on physical inspection, is consistent with an ambient effect (see also Section 2.2 on cooling air discharge/intake separation between the two bays) rather than a coincidental simultaneous fault on both units, and should prompt an ambient temperature review before further component-level investigation on either unit.

---

# Section 6: System Sizing & Duty Cycle

## 6.1 Purpose and Relationship to Section 3 / Section 4

This section addresses discharge pressure shortfall and capacity-related behavior from the perspective of **system sizing, demand matching, and duty cycle design** — as distinct from the **alarm-response perspective** already covered for `DISCH_PRESS_LOW_07` (Sections 3.3 and 4.5), `DISCH_PRESS_HIGH_05` (Section 3.3), and `CAPACITY_FAULT_17` (Section 3.3). As established in the bridging note at Section 3.7, Sections 3 and 4 address what to do once one of these alarms has already been raised on a specific unit: what to check, and how to distinguish a genuine fault from a transient demand event. This section instead addresses whether the combined installed capacity of Compressor-1 and Compressor-2, the receiver sizing, and the lead/trim sequencing strategy are actually adequate for the site's demand profile in the first place — a question that matters even when no alarm has ever fired, and that remains relevant even after every individual alarm investigation under Section 4.5 has concluded "no fault found."

A site that experiences `DISCH_PRESS_LOW_07` repeatedly, with each individual investigation under Section 4.5 concluding that both units were running correctly and no component fault was found, should treat this section — not a further round of Section 4.5 investigation — as the next step.

## 6.2 Demand Profile Characterization

Correctly sizing and sequencing a two-compressor system begins with characterizing the actual plant demand profile, not the nameplate capacity of the connected equipment using compressed air:

- **Base demand** — the continuous, relatively constant air consumption present at all times (small pneumatic instruments, continuously-open control valves with a bleed requirement, and similar steady loads).
- **Variable demand** — consumption that fluctuates with production activity (pneumatic tools, intermittent process equipment, batch operations).
- **Peak demand** — the highest simultaneous demand the system must be able to meet, which may occur only briefly and infrequently but still determines the combined capacity requirement if it must be met without a pressure shortfall.

The MC-6100 Series base-load/trim arrangement (Section 1.8) is specifically designed around this three-part demand structure: the base-load unit is sized and operated to cover the base demand plus a substantial share of typical variable demand at high efficiency (near its full-load specific power point per Section 1.9), while the trim unit's VFD modulation absorbs the remaining variable demand and any peak demand excursions. A demand profile that has shifted significantly since the original system sizing — for example, from added production equipment — should prompt a re-characterization against this structure rather than an assumption that the original base-load/trim split remains appropriate.

## 6.3 Receiver Sizing and Its Effect on Pressure Stability

The wet air receiver (R-301, Section 1.2) provides a volume of stored compressed air that buffers short-duration demand spikes without requiring an immediate capacity response from either compressor, reducing the frequency of both `DISCH_PRESS_LOW_07` events and unnecessary trim-unit modulation cycling. A receiver that is undersized relative to the demand profile's peak excursion characteristics (Section 6.2) will show pressure drop and recovery cycles that are faster and deeper than a correctly sized receiver would produce under the same demand pattern, and this can present as a `DISCH_PRESS_LOW_07` alarm pattern that is actually a receiver sizing issue rather than a compressor capacity or fault issue — a distinction that is easy to miss if the investigation stays focused on the compressors themselves rather than stepping back to the system level.

## 6.4 Base-Load/Trim Sequencing Strategy

The sequencing logic's core objective is to keep the base-load unit operating as close to its full-load, most-efficient point (Section 1.9) as possible, while using the trim unit's modulation range to absorb variability — this minimizes total system specific power compared to, for example, running both units at a partial, mid-range capacity simultaneously. Two sequencing failure patterns are worth recognizing:

- **Trim unit chronically near its minimum turndown point.** If the trim unit spends a large fraction of its running time near the 40% minimum turndown point (Section 1.9), this suggests the base-load unit is oversized relative to actual base demand, or that the sequencing split point itself should be adjusted — running the trim unit chronically near minimum turndown both wastes efficiency (per the rising specific power curve in Section 1.9) and increases exposure to the turndown-related conditions discussed in Section 4.9 (`OIL_PRESS_03`, `MIN_PRESS_VALVE_18`).
- **Trim unit cycling between minimum turndown and full stop rather than modulating smoothly.** Where demand regularly drops below the trim unit's 40% minimum stable turndown point, the unit is forced into a load/unload or full stop/restart pattern rather than smooth modulation, directly contributing to `STARTS_EXCEED_19` risk and to the idle-power inefficiency described in Section 1.9. This pattern typically indicates the base-load/trim split is mismatched to the actual demand profile rather than indicating any equipment fault, and the corrective action is a sequencing or role-split adjustment, not a compressor repair.

## 6.5 Duty Cycle Implications for Wear and Maintenance

Because the trim role involves substantially more frequent modulation and, in a poorly matched system, more frequent full stop/start cycling than the base-load role (Section 1.8), a unit's maintenance needs are influenced by its accumulated role history, not only its accumulated run hours:

- A unit that has spent a disproportionate share of its service life in the trim role should be expected to show more starts-per-hour history, more time spent near minimum turndown, and correspondingly closer attention to the `OIL_PRESS_03` and `MIN_PRESS_VALVE_18` conditions discussed in Section 4.9, compared to a unit that has spent more of its life in the steadier base-load role.
- The role-alternation schedule (Section 1.8, nominally every 336 hours of combined run time) exists specifically to prevent this asymmetry from concentrating permanently on one unit; a site that disables or extends this alternation for operational convenience should expect accelerated wear on whichever unit is left in the trim role for the extended period, and the maintenance schedule in Section 5 should be adjusted accordingly for that unit rather than left at the standard interval.

## 6.6 Worked Example: Distinguishing a Fault from a Sizing Issue

Suppose `DISCH_PRESS_LOW_07` has fired on three occasions over the past month, each time during the same daily production shift change window, with each individual Section 4.5 investigation confirming both units running, no capacity control fault, and clean filters. Under the alarm-response perspective alone, each of these three investigations correctly concludes "no fault found" and the alarm clears once the transient passes. Applying the Section 6 perspective instead: the recurring time-of-day correlation suggests a genuine, repeatable demand pattern — likely a shift-change event where multiple pneumatic tools or process steps start simultaneously — that briefly exceeds combined capacity even with both units healthy and fully available. The appropriate response is not further equipment troubleshooting but a review of receiver sizing (Section 6.3) and sequencing strategy (Section 6.4) against this specific, now-characterized demand event — for example, staggering the shift-change activities that drive the spike, or re-evaluating whether the installed combined capacity has adequate margin for it at all.

## 6.7 Single-Unit Operation During Maintenance Outages

Because the MC-6100 Series installation consists of only two units with no dedicated standby (unlike the three-unit duty/duty/standby arrangement used elsewhere in the MechMind rotating equipment fleet's pump manual), any planned or unplanned outage on one unit leaves the entire Plant Compressed Air System dependent on the single remaining unit's capacity, which is inherently less than the combined two-unit capacity that the Section 6.2 demand profile analysis was based on.

- **Planned maintenance outages** (Section 5.6 annual overhaul, in particular) should be scheduled against the demand profile characterized in Section 6.2, targeting a period of lower expected base and variable demand where the single remaining unit's capacity, combined with the receiver's buffering capacity (Section 6.3), is more likely to be adequate without triggering a sustained `DISCH_PRESS_LOW_07` condition.
- **During a single-unit outage**, the remaining unit necessarily operates in an effective base-load-only mode regardless of its normal role assignment, and should be expected to run closer to its full-load point more continuously than under normal two-unit sequencing — this is an expected and acceptable short-term operating mode, not a fault condition, but it does mean the remaining unit accumulates run hours and full-load thermal cycling faster than its normal role-alternation schedule (Section 1.8) would suggest, and its next scheduled maintenance interval (Section 5) should be adjusted to reflect the additional accumulated run hours rather than left on the original calendar-based schedule.
- **An unplanned outage** (a Critical trip on one unit) during a period of high demand is the scenario most likely to produce a sustained `DISCH_PRESS_LOW_07` condition that is a genuine, unavoidable capacity shortfall rather than a sizing or sequencing issue to be corrected — in this specific scenario, the Section 4.5 alarm-response guidance to check whether both units are running and available is not a preliminary check to rule out before deeper investigation, but very often the entire answer, with the real corrective action being the Section 4 troubleshooting procedure for whatever originally tripped the unstable unit rather than anything at the system level.

This section's capacity-planning perspective and Section 4's alarm-response perspective therefore converge in exactly this scenario: recognizing that a two-unit system with no standby will predictably show a demand-side symptom during any single-unit outage is itself a system sizing consideration (this section), even though the underlying trigger and its correction are squarely an equipment-fault matter (Section 4).

## 6.8 Recommended System-Level Review Cadence

In addition to the per-unit condition monitoring cadence in Section 5.12, the following system-level reviews should be performed to keep the sizing and sequencing basis in this section current against actual operating experience, rather than treating the original commissioning-time sizing analysis as permanently valid:

| Review | Frequency | Purpose |
|---|---|---|
| Demand profile re-characterization | Annual, or after any known significant change to connected plant equipment | Confirm the Section 6.2 base/variable/peak demand structure still reflects actual site consumption |
| Trim unit turndown distribution review | Quarterly | Confirm the trim unit is not chronically operating near its minimum turndown point (Section 6.4); a shifting distribution toward the low end of the turndown range is an early indicator that the base-load/trim split should be reviewed before it manifests as a `STARTS_EXCEED_19` or `OIL_PRESS_03` pattern |
| `DISCH_PRESS_LOW_07` recurrence pattern review | Quarterly, or immediately following the third occurrence in a rolling 30-day period per Section 3.4 escalation criteria | Distinguish a genuine, characterizable recurring demand pattern (Section 6.6) from isolated unrelated transient events |
| Receiver sizing adequacy review | Following any demand profile re-characterization that identifies a materially different peak demand excursion | Confirm receiver volume (Section 6.3) remains adequate for the current peak demand characteristics, not only the demand profile in place when the receiver was originally sized |

Treating these as routine, scheduled reviews rather than reactive investigations triggered only after a `DISCH_PRESS_LOW_07` pattern has already become disruptive is the practical difference between using this section proactively and using it only as a last resort once the Section 4.5 alarm-response procedure has been run through repeatedly without resolution.

---

# Section 7: Appendix A — Safety & Compliance

## A.0 How to Use This Appendix

This appendix is organized to be read in two ways. Read sequentially (A.1 through A.10), it functions as a general safety and compliance reference for anyone new to the Compressor-1/Compressor-2 installation. Read selectively via the cross-reference index in Section A.8, it functions as a fast lookup during an active alarm event — for example, a technician responding to an active `OIL_PRESS_03` alarm can go directly from Section 3.3 or Section 4.4 to the pressurized-system safety guidance in Section A.5 without reading the full appendix in order. Both uses are intentional, which is why safety-critical guidance (lockout/tagout in Section A.3, PPE in Section A.4, emergency procedures in Section A.7) is written to stand on its own rather than assuming the reader has already absorbed every preceding subsection.

## A.1 Applicable Standards Framework

The MC-6100 Series and its associated CompGuard control system are designed with reference to the following general classes of industrial standards. This manual is a synthetic reference document and does not itself constitute a certificate of compliance; site-specific compliance documentation should be maintained separately in the plant's regulatory record.

- General pressure vessel and piping safety practice consistent with ASME Boiler and Pressure Vessel Code (Section VIII) principles for the wet air receiver
- General rotating and reciprocating compressed air equipment safety practice consistent with ISO 5388-series principles
- Vibration severity classification per ISO 10816-3, as referenced throughout Section 3 and Section 4 for `VIB_HIGH_11`
- Electrical area classification and equipment protection consistent with IEC 60079-series principles, where the installation area classification requires it
- General machinery safety and guarding principles consistent with ISO 12100
- Lockout/tagout practice consistent with generally accepted hazardous energy control principles (site-specific procedures govern; the outline in Section A.3 is a minimum baseline, not a replacement for the site's own LOTO program)

## A.2 General Safety Precautions

The following hazards are present on Compressor-1 and Compressor-2 and must be considered before any inspection, maintenance, or troubleshooting activity described elsewhere in this manual:

- **Pressurized system.** The package, discharge piping, and wet air receiver operate up to 13 bar(g) (Section 1.4). Do not open any pressurized connection without first confirming the system is depressurized and isolated.
- **Hot surfaces.** Airend discharge piping, the oil system, and the aftercooler can exceed safe touch temperatures during normal operation, particularly near the 100 °C `DISCH_TEMP_01` and `OIL_TEMP_02` Critical thresholds (Section 3.3), and remain hot for a period after shutdown.
- **Rotating equipment.** The airend and integral motor present an entanglement hazard whenever the unit is running or capable of starting; the acoustic enclosure is a safety guard and must not be operated with access panels open or removed.
- **Electrical hazards.** The 400 V motor supply and integral VFD present electrical shock and arc-flash hazards. All electrical work must be performed only by personnel qualified and authorized for the applicable voltage class, following the site's electrical safety program.
- **Stored pneumatic energy.** Even after the compressor itself is stopped and electrically isolated, the wet and dry air receivers retain stored compressed air energy that must be independently vented and confirmed at zero pressure before any downstream work, per Section A.5.
- **Oil mist and hot oil.** The oil circuit operates at elevated temperature (Section 1.4) and under pressure during operation; opening any oil-system connection without confirming depressurization and adequate cooling time risks hot oil spray or mist exposure.

## A.3 Lockout/Tagout Procedure (Baseline)

Before any activity requiring physical access to the airend, motor, oil system, or associated piping described in Sections 2, 4, or 5 of this manual, the following minimum hazardous energy control sequence applies. This baseline must be supplemented with the site's own documented LOTO procedure, which takes precedence where more stringent.

1. Notify affected operations personnel of the intended isolation and its expected duration.
2. Stop the unit through normal control means (not via the Emergency Stop, which is reserved for the conditions in Section A.7) and confirm zero speed.
3. Isolate and lock out the electrical supply at the package main disconnect, applying a personal lock and tag.
4. Isolate the unit's discharge from the shared header at the discharge isolation valve (Section 2.4), applying a personal lock and tag, so the isolated unit cannot be re-pressurized from the sister unit's continued operation on the common header.
5. Vent the isolated unit and its associated piping to atmosphere through the appropriate vent point, and confirm zero pressure at a gauge before opening any connection.
6. Verify zero energy state directly at the point of work: confirm zero pressure at the vent and attempt a start from the local HMI to confirm no response before beginning any work.
7. On completion of work, remove locks and tags only in reverse order, and only by the person who applied each lock (or per the site's authorized alternate-removal procedure), followed by the restart authorization sequence in Section A.7.

## A.4 Personal Protective Equipment Requirements

| Activity | Minimum PPE |
|---|---|
| General area walk-down (Section 5.2 daily checks) | Standard site PPE (hard hat, safety glasses, hearing protection near running units per the 78 dB(A) rating in Section 1.4) |
| Direct contact with running or recently stopped unit | Add insulated/heat-resistant gloves |
| Oil system service (Sections 4.3, 4.4, 5.6, 5.7) | Add face shield and oil-resistant gloves |
| Pressurized system work (venting, filter/separator element replacement) | Add face shield; confirm zero pressure per Section A.3 before any connection is opened |
| Electrical panel or VFD work (Sections 2.5, 2.7) | Arc-flash rated PPE per the site electrical safety program and the panel's calculated incident energy category |

## A.5 Hazardous Energy Sources Specific to This Equipment

- **Stored compressed air in the receivers.** As noted in Section A.2, the wet and dry air receivers retain pressure independent of whether the compressor itself is stopped and electrically isolated; venting and zero-pressure verification per Section A.3 must address the receiver-side stored energy specifically, not only the compressor package.
- **VFD DC bus residual voltage.** The integral VFD's internal capacitors can retain hazardous voltage for a period after the disconnect is opened; follow the drive manufacturer's specified discharge time before internal VFD panel work, in addition to the external disconnect lockout in Section A.3.
- **Hot, pressurized oil.** The oil circuit combines thermal and pressure hazards simultaneously during and shortly after operation; allow adequate cooling time in addition to pressure venting before opening any oil-system connection.
- **Spring energy in the minimum pressure valve and relief valve.** Both contain spring mechanisms under compression; follow the valve manufacturer's disassembly procedure to avoid a sudden release of stored mechanical energy during service (Section 4.4, Section 5.5).

## A.6 Guarding and Access

- The acoustic package enclosure (Section 1.3) is a safety guard in addition to its noise-reduction function, and must never be operated with access panels open or removed, including for brief diagnostic purposes — use the vibration, temperature, and pressure instrumentation described in Sections 3 and 4 for running diagnostics instead of visual/physical access to the airend or motor while running.
- Access to Bay 1 and Bay 2 should respect the clearance envelope in Section 2.2, which serves a dual purpose of maintenance and cooling-airflow access and safe separation between personnel and the adjacent operating unit during any single-unit maintenance activity.

## A.7 Emergency Procedures

**Emergency Stop (`ESTOP_ACT_20`, Section 3.3):** Any person observing an immediate hazard — abnormal noise suggesting imminent mechanical failure, visible oil spray, or a person at risk of contact with rotating or energized equipment — should activate the local E-Stop pushbutton without waiting for supervisory approval. Following any E-Stop activation:

1. Do not reset the E-Stop or attempt a restart until the cause has been positively identified, per the guidance already given for `ESTOP_ACT_20` in Section 3.3.
2. Treat the unit as under lockout (Section A.3) for the duration of the investigation, even though the E-Stop itself is a separate protective function from the electrical disconnect lockout.
3. Restart authorization following any Safety-severity event requires sign-off from the site reliability engineer or designated safety authority, not solely the technician who investigated the cause.

**High-High discharge pressure (`HIGH_HIGH_PRESS_06`):** Treat as a safety-significant event per Section 3.3. Do not restart without identifying why the `DISCH_PRESS_HIGH_05` Warning stage did not prevent escalation, and inspect the mechanical relief valve for signs of having lifted per Section 3.3 Step 2 of that alarm's response guidance.

**Oil or air leak response:** Contain the leak using site spill-response materials appropriate to compressor lubricant, barricade the wet or pressurized area to prevent slip/fall or pressure-release exposure, and follow the site's environmental reporting requirements, in addition to the equipment-level corrective actions described in Section 4.

## A.7a Environmental Program Interface

The oil-flooded nature of the MC-6100 Series airend means environmental handling considerations are more prominent for this equipment than for some other rotating equipment in the MechMind fleet, and this manual's guidance interfaces with, rather than replaces, the site's environmental management program in the following specific ways:

- **Condensate handling** (Section 2.4, Section 5.11) must route to the site's oil/water separator system; this manual assumes such a system exists and is properly sized for the combined condensate load of both units, and does not itself specify oil/water separator design — that is a site environmental engineering responsibility outside this manual's scope.
- **Used oil and oil-contaminated waste** (separator elements, filter elements, oil samples) generated under Section 5 maintenance activities must be tracked per the site's waste manifest requirements where applicable, in addition to the physical disposal handling described in Section 5.11.
- **A `CONDENSATE_FAULT_16` event affecting the drain valve's ability to route condensate to the oil/water separator** should be treated as having a potential environmental compliance dimension, not only an equipment reliability dimension, and escalated per the site's environmental incident reporting threshold if any condensate is confirmed to have bypassed the separator system during the fault period.

## A.8 Cross-Reference Index

The table below consolidates every alarm code introduced in Section 3 with the primary manual locations where it is discussed, to support rapid navigation during an active event.

| Code | Section 3 (Summary) | Section 4 (Full Procedure) | Other References |
|---|---|---|---|
| `DISCH_TEMP_01` | 3.3 | 4.2 | Section 2.13 (sensor wiring pitfall), Section 4.9 |
| `OIL_TEMP_02` | 3.3 | 4.3 | Section 2.2 (cooling air separation), Section 5.7 |
| `OIL_PRESS_03` | 3.3 | 4.4 | Section 2.7 (minimum pressure valve config), Section 4.9 |
| `OIL_LEVEL_LOW_04` | 3.3 | — | Section 5.7 (lubrication schedule) |
| `DISCH_PRESS_HIGH_05` | 3.3 | — | Section 2.12 (setpoint configuration) |
| `HIGH_HIGH_PRESS_06` | 3.3 | — | Section A.7 (emergency procedures) |
| `DISCH_PRESS_LOW_07` | 3.3 | 4.5 | Section 6 (full system sizing/duty cycle discussion) |
| `SEP_DP_HIGH_08` | 3.3 | — | Section 5.5, Section 5.6 (element replacement), Section 4.9 |
| `INLET_FILT_DP_09` | 3.3 | — | Section 5.4 (filter inspection) |
| `AFTERCOOLER_FOUL_10` | 3.3 | — | Section 2.2 (cooling air separation) |
| `VIB_HIGH_11` | 3.3 | 4.6 | Section 2.6 (piping/vibration isolation) |
| `MOTOR_OVLD_12` | 3.3 | 4.7 | Section 2.12 (VFD current limit) |
| `PH_LOSS_13` | 3.3 | 4.8 | Section 1.7 (supply conditions) |
| `VFD_FAULT_14` | 3.3 | — | Section 2.12 (VFD parameters) |
| `SENSOR_FAIL_15` | 3.3 | — | Section 4.1 (general diagnostic principle) |
| `CONDENSATE_FAULT_16` | 3.3 | — | Section 2.4 (condensate routing), Section 5.11 |
| `CAPACITY_FAULT_17` | 3.3 | — | Section 1.8 (lead/trim sequencing), Section 6.4 |
| `MIN_PRESS_VALVE_18` | 3.3 | — | Section 2.7, Section 5.5, Section 4.9 |
| `STARTS_EXCEED_19` | 3.3 | — | Section 1.7, Section 2.12, Section 6.4 |
| `ESTOP_ACT_20` | 3.3 | — | Section A.7 (emergency procedures) |

## A.9 Compliance Statement and Disclaimer

This manual, including all equipment identifiers (Compressor-1, Compressor-2; tags C-301/C-302; serial numbers MM-6100-3001/3002), the MC-6100 Series model designation, the CompGuard controller platform, and all specification values, alarm codes, and procedures contained herein, is a fully synthetic reference document prepared for demonstration, testing, and documentation-tooling purposes. It does not describe a real commercially available product, is not associated with any real manufacturer, and must not be relied upon as an actual equipment manual, safety certification, or regulatory compliance record for any physical installation. Any resemblance to a real product's specifications, alarm nomenclature, or procedures is coincidental.

## A.10 Training and Competency Requirements

| Activity | Minimum Competency |
|---|---|
| Daily/weekly visual checks (Sections 5.2, 5.3) | General site safety orientation; no specialized compressor training required |
| Routine filter/element inspection (Section 5.4, 5.5) | Site-authorized maintenance technician, LOTO-qualified per Section A.3 |
| Alarm investigation per Section 4 procedures | Site-authorized maintenance technician with documented familiarity with this manual's alarm codes (Section 3) and the specific procedure being followed |
| Oil system service, including minimum pressure valve work (Sections 4.4, 5.6, 5.7) | Technician trained specifically on oil-flooded screw compressor oil circuits |
| Pressurized system venting and isolation (Section A.3) | Site-authorized maintenance technician, LOTO-qualified, with specific training on pressure vessel isolation |
| Electrical panel and VFD work (Sections 2.5, 2.7) | Personnel qualified and authorized for the applicable voltage class, with specific VFD/drive training |
| Restart authorization following a Critical auto-trip | Site-authorized maintenance technician who performed or directly verified the corrective action |
| Restart authorization following a Safety-severity event (`ESTOP_ACT_20`) or high-high pressure event (`HIGH_HIGH_PRESS_06`) | Site reliability engineer or designated safety authority only, per Section A.7 |
| Threshold, setpoint, or sequencing configuration changes (Section 3.5, Section 6) | Site reliability engineer approval required regardless of who performs the technical change |

---

# Section 8: Glossary of Terms and Abbreviations

| Term | Definition |
|---|---|
| Airend | The compression element of a rotary screw compressor, consisting of the matched male/female rotor pair and its housing; see Section 1.3 |
| Approach temperature | The difference between a cooler's air outlet temperature and the ambient air temperature, used to assess cooler fouling independent of ambient variation; see `AFTERCOOLER_FOUL_10` |
| Base-load unit | In a two-compressor sequencing arrangement, the unit operated continuously at or near full load; see Section 1.8, Section 6.4 |
| CMMS | Computerized Maintenance Management System — the site's system of record for maintenance history, referenced throughout Section 5 |
| DCS | Distributed Control System — the plant-level control system to which CompGuard alarms are forwarded per Section 1.6 |
| FAD (Free Air Delivery) | The volume of air delivered by a compressor, expressed at standard inlet conditions; the primary capacity rating for the MC-6100 Series, see Section 1.4 |
| Historian | The time-series database within the CompGuard system that stores instrument readings and alarm events for trend analysis |
| HMI | Human-Machine Interface — the local operator display on each CompGuard controller |
| ISO 10816-3 | The international standard used to classify mechanical vibration severity into zones (A through D) for industrial machinery |
| LOTO | Lockout/Tagout — the hazardous energy control procedure outlined in Section A.3 |
| Minimum pressure valve | A combination check/pressure-holding valve maintaining minimum receiver pressure to sustain oil injection differential pressure at reduced capacity; see Section 1.3, `MIN_PRESS_VALVE_18` |
| Modbus RTU / TCP | Industrial communication protocols used between the VFD, CompGuard controller, and plant DCS |
| Oil carryover | Residual compressor lubricant remaining entrained in the discharge air after separation; see Section 1.3, Section 1.7 |
| Oil injection differential pressure | The pressure difference between the oil injection point and airend discharge that drives oil flow into the airend for sealing, cooling, and lubrication; see `OIL_PRESS_03` |
| Receiver (wet / dry) | A pressure vessel providing stored compressed air volume to buffer demand fluctuations; the wet receiver is upstream of drying equipment, the dry receiver downstream; see Section 1.2, Section 6.3 |
| Specific power | Electrical power consumed per unit of air delivered, typically expressed in kW per m³/min; rises as capacity turndown deepens, see Section 1.9 |
| Trim unit | In a two-compressor sequencing arrangement, the unit whose VFD modulates to track demand above the base-load unit's fixed output; see Section 1.8, Section 6.4 |
| Turndown | The range over which a compressor can reduce its capacity via VFD speed modulation while remaining in stable, continuous operation; see Section 1.9 |
| VFD | Variable Frequency Drive — the motor speed control device providing capacity turndown, described in Sections 1.3, 2.7, and 2.12 |

---

# Section 9: Document Revision History

| Revision | Summary of Changes |
|---|---|
| A | Initial issue covering Compressor-1 only, prior to Compressor-2 installation |
| B | Expanded to cover both units following Compressor-2 commissioning; added full Alarm Code Matrix (Section 3) |
| C (current) | Added detailed troubleshooting procedures (Section 4), System Sizing & Duty Cycle section (Section 6), and expanded Safety & Compliance appendix (Section 7) with full cross-reference index |

*End of MechMind MC-6100 Series Technical Reference & Operations Manual — Manual Number MM-TM-6100-REV-C.*
