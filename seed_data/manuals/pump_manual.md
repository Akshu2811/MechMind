# MechMind MP-4300 Series Centrifugal Process Pump

## Technical Reference & Operations Manual

**Covering Unit Tags: Pump-1 (P-101), Pump-2 (P-102), Pump-3 (P-103)**

| Document Control | |
|---|---|
| Manual Number | MM-TM-4300-REV-C |
| Applicable Model Line | MP-4300 Series, Horizontal End-Suction Centrifugal Pump |
| Applicable Units | Pump-1 (Tag P-101, S/N MM-4300-1001), Pump-2 (Tag P-102, S/N MM-4300-1002), Pump-3 (Tag P-103, S/N MM-4300-1003) |
| Controller Platform | PumpGuard™ Local Controller, firmware 3.2.x |
| Revision | C |
| Issued By | MechMind Industrial Systems — Technical Publications |
| Status | Fully synthetic reference document for demonstration and testing purposes. No affiliation with any real manufacturer. |

> **Note on scope:** This manual documents a three-pump installation (Pump-1, Pump-2, Pump-3) of identical MP-4300 Series construction, installed as a duty/duty/standby set on a single suction header. Except where a procedure or specification explicitly calls out one unit by tag, all content applies equally to Pump-1, Pump-2, and Pump-3.

---

## Table of Contents

1. Overview & Technical Specifications
2. Installation & Commissioning Procedures
3. Full Alarm Code Matrix
4. Detailed Troubleshooting Procedures
5. Routine Maintenance Schedule
6. Thermal Management & Ambient Operating Conditions
7. Appendix A — Safety & Compliance
8. Glossary of Terms and Abbreviations
9. Document Revision History

---

# Section 1: Overview & Technical Specifications

## 1.1 Purpose and Scope

This manual provides the technical reference, installation, commissioning, alarm response, troubleshooting, maintenance, and safety documentation for the MechMind MP-4300 Series horizontal end-suction centrifugal pump, as installed in the three-unit configuration designated **Pump-1**, **Pump-2**, and **Pump-3**. All three units are of identical mechanical construction and share a common instrumentation and control architecture built around the PumpGuard™ Local Controller. Where information in this manual differs between units — for example, differing duty assignments or install dates — this is called out explicitly. Otherwise, all specifications, procedures, and alarm behaviors apply uniformly across the three-pump set.

This document is intended for use by commissioning engineers, maintenance technicians, reliability engineers, and control system integrators responsible for the operation and upkeep of Pump-1, Pump-2, and Pump-3. It is also intended to serve as a structured knowledge source for automated maintenance-assistance tooling, including alarm-code lookup, troubleshooting guidance retrieval, and maintenance scheduling support.

## 1.2 Equipment Identification

The three units covered by this manual are installed on a common suction header drawing from the Site Utility Water Loop and discharging into a shared header feeding the Heat Exchanger Bank (HX-Bank-1). The duty arrangement is as follows:

| Unit Tag | Equipment Tag | Serial Number | Role | Install Location |
|---|---|---|---|---|
| Pump-1 | P-101 | MM-4300-1001 | Lead duty pump | Utility Pump House, Bay 1 |
| Pump-2 | P-102 | MM-4300-1002 | Lag duty pump (auto-rotated with Pump-1) | Utility Pump House, Bay 2 |
| Pump-3 | P-103 | MM-4300-1003 | Installed standby (auto-start on duty pump fault) | Utility Pump House, Bay 3 |

Duty rotation between Pump-1 and Pump-2 is managed automatically by the plant DCS on a 168-hour running-hours basis to equalize wear. Pump-3 is held in standby and is auto-started by the PumpGuard interlock logic if either duty pump trips or fails to reach commanded speed within 15 seconds of a start command. Because Pump-3 spends the majority of its service life in standby, its maintenance schedule includes additional exercise-run requirements not applicable to Pump-1 and Pump-2 (see Section 5.4).

## 1.3 Pump Design Description

The MP-4300 Series is a horizontal, single-stage, end-suction, back pull-out design centrifugal pump intended for continuous-duty transfer of treated process water and similar non-abrasive, non-corrosive fluids in industrial utility service. The back pull-out configuration allows the bearing housing, mechanical seal, and impeller to be removed for service without disturbing the casing or piping connections, minimizing maintenance downtime.

Key construction features common to Pump-1, Pump-2, and Pump-3:

- **Casing**: ASTM A216 Grade WCB cast steel volute casing, radially split, rated for 16 bar (232 psi) maximum working pressure at 90 °C.
- **Impeller**: Enclosed, single-suction design in ASTM A743 Grade CA6NM martensitic stainless steel, dynamically balanced to ISO 21940 Grade G6.3. Standard trim diameter is 285 mm against a maximum casing bore of 315 mm, permitting future impeller up-trim if process conditions change.
- **Shaft**: ASTM A479 Type 420 stainless steel, hard-chromed in the seal chamber and stuffing box area for wear resistance.
- **Bearing housing**: Grease-lubricated; angular contact ball bearing pair at the drive end to absorb combined radial and axial loads, deep-groove ball bearing at the non-drive end.
- **Mechanical seal**: Single cartridge-style mechanical seal, Type 2100, carbon-vs-silicon-carbide face combination with EPDM secondary elastomers, arranged per API Plan 11 (flush from pump discharge back to the seal chamber through a flow control orifice).
- **Coupling**: Spacer-type elastomeric insert coupling, permitting seal and bearing housing removal without moving the driver.
- **Baseplate**: Fabricated structural steel baseplate, epoxy-grout fill, common to pump and motor.
- **Driver**: 132 kW (175 hp) TEFC IE3 premium-efficiency induction motor, 400 V / 3-phase / 60 Hz, driven through a dedicated variable frequency drive (VFD) for soft-start and flow trim capability.
- **Coating**: Two-coat epoxy system, RAL 5015 (sky blue) finish coat, suitable for indoor/outdoor industrial exposure.

## 1.4 Technical Specifications

| Parameter | Value |
|---|---|
| Pump type | Horizontal end-suction, single-stage, back pull-out centrifugal |
| Rated flow | 450 m³/h (1,980 US gpm) |
| Rated total head | 62 m (203 ft) |
| Rated speed | 1,780 rpm (nominal, 60 Hz, 4-pole) |
| NPSH required at rated flow | 4.2 m |
| Suction connection | 200 mm (8 in), ANSI Class 150 RF flange |
| Discharge connection | 150 mm (6 in), ANSI Class 150 RF flange |
| Max. casing working pressure | 16 bar (232 psi) |
| Max. continuous fluid temperature | 90 °C (194 °F) |
| Max. intermittent fluid temperature | 110 °C (230 °F) |
| Ambient design range | −10 °C to 50 °C (14 °F to 122 °F) |
| Motor rating | 132 kW (175 hp), 400 V, 3-phase, 60 Hz, IE3, TEFC |
| Motor full-load current | 218 A at 400 V |
| Drive | Dedicated VFD, 20–60 Hz operating range |
| Mechanical seal | Single cartridge, carbon/SiC, EPDM, API Plan 11 flush |
| Bearing lubrication | Grease, NLGI Grade 2 lithium-complex, replenished per Section 5.7 |
| Sound pressure level | 78 dB(A) at 1 m, free field |
| Bare pump weight | 340 kg |
| Total assembly weight (pump, motor, baseplate) | 610 kg |
| Enclosure rating (junction boxes / local instruments) | IP65 |
| Paint system | 2-coat epoxy, RAL 5015 |

## 1.5 Nameplate Data and Identification

Each unit carries a stainless steel nameplate riveted to the bearing housing, stamped with the equipment tag, serial number, rated duty point (flow/head/speed), maximum working pressure, and year of manufacture. The nameplate data must match the values recorded in the commissioning record (Section 2.11) and the asset record in the plant CMMS. A mismatch between nameplate serial number and CMMS record should be treated as a documentation discrepancy requiring investigation before further work is performed on the unit — do not assume the nameplate or the CMMS is correct without verification.

## 1.6 Control System Overview

All three units are monitored and protected by an individual PumpGuard™ Local Controller, one per pump, mounted in the associated motor control cabinet. Each PumpGuard controller aggregates:

- Two Pt100 RTD bearing temperature inputs (drive end and non-drive end),
- Three PTC motor winding thermistor inputs (one per phase),
- One MEMS accelerometer-based vibration sensor per bearing housing, ISO 10816-3 zone classification,
- Suction and discharge pressure transmitters (4–20 mA),
- A magnetic flowmeter signal from the common discharge header,
- A seal chamber leak/moisture sensor,
- A baseplate drip-tray leak sensor,
- VFD status and speed feedback via Modbus RTU,
- Local E-Stop and safety interlock status.

The PumpGuard controller evaluates these inputs continuously against configured thresholds and raises one of the twenty standardized alarm codes described in full in **Section 3** when a threshold is exceeded or a fault condition is detected. Alarms are surfaced on the local HMI, forwarded to the plant DCS over Modbus TCP, and logged with timestamp, unit tag, and triggering value in the PumpGuard historian. Section 4 of this manual expands on the diagnostic and corrective procedures for the most operationally significant of these alarm codes.

## 1.7 Process Fluid and Service Conditions

Pump-1, Pump-2, and Pump-3 handle treated process water drawn from the Site Utility Water Loop and delivered to the Heat Exchanger Bank (HX-Bank-1) as described in Section 1.2. The service basis assumed by the specifications in Section 1.4 is as follows:

| Parameter | Design Basis |
|---|---|
| Fluid | Treated utility water (closed-loop, chemically dosed for corrosion and scale control) |
| Specific gravity | 0.97–1.00 across the operating temperature range |
| Total dissolved solids | Maintained below 500 ppm per the site water treatment program |
| Suspended solids | Removed to below 50 micron nominal by upstream filtration; the 40-mesh suction strainer (Section 2.5) is a secondary protective device, not the primary filtration stage |
| Operating temperature range | 15 °C to 65 °C typical; up to 90 °C continuous rated per Section 1.4 |
| Chemical compatibility | Seal elastomers (EPDM) and wetted metallurgy (CA6NM, A216 WCB) selected for compatibility with the site's standard corrosion-inhibitor dosing chemistry |

A change to the process fluid's chemistry, temperature range, or solids loading outside this design basis — for example, a change in water treatment chemical supplier, or a decision to use the same header for a different fluid — should be reviewed against these design parameters before being implemented, since several alarm codes in Section 3 (`SEAL_FAIL_03`, `SUCT_STRAIN_15`, `MOTOR_OVLD_09`) are sensitive to exactly these fluid properties, and a fluid change outside the original design basis can produce a step change in alarm frequency that is easily mistaken for an equipment fault when it is actually a process change.

## 1.8 Duty Rotation and Unit-to-Unit Wear Tracking

Because Pump-1, Pump-2, and Pump-3 are of identical construction and share a common duty (Section 1.2), their PumpGuard trend data is directly comparable in a way that is not generally true for dissimilar equipment — this comparability is used repeatedly throughout this manual (see in particular Section 6.8 and Section 5.12) to distinguish a genuine unit-specific fault from a fleet-wide ambient or process effect.

This comparability depends on two conditions being maintained over the life of the installation: first, that duty rotation between Pump-1 and Pump-2 continues on the 168-hour basis described in Section 1.2 so that running hours remain roughly equalized between them; and second, that Pump-3's standby exercise-run schedule (Section 5.4) is maintained so that its baseline, despite accumulating far fewer running hours than the duty units, remains a meaningful comparison point rather than an idle unit whose behavior on any given start is effectively unpredictable. A site that disables automatic duty rotation for operational convenience, or defers Pump-3 exercise runs, should expect the cross-unit comparison techniques described elsewhere in this manual to become less reliable in proportion to how long that condition persists.

## 1.9 Performance Curve Data

The following performance data, taken at rated speed (1,780 rpm, 60 Hz) with the standard 285 mm impeller trim, is the reference curve against which field performance checks (Section 2.11, Section 5.6) and low-performance troubleshooting (`PRESS_LOW_06`, `FLOW_LOW_05`, Section 4.5) should be compared. Field readings should be corrected to rated speed before comparison if the unit was running at a different VFD-commanded speed at the time of the reading.

| Flow (% of rated) | Flow (m³/h) | Total Head (m) | Hydraulic Efficiency (%) | NPSH Required (m) | Shaft Power (kW) |
|---|---|---|---|---|---|
| 0 (shutoff) | 0 | 74 | 0 | 2.1 | 68 |
| 40% | 180 | 71 | 58 | 2.6 | 92 |
| 60% | 270 | 68 | 71 | 3.1 | 108 |
| 80% | 360 | 65 | 79 | 3.7 | 121 |
| 100% (rated) | 450 | 62 | 82 | 4.2 | 132 |
| 120% | 540 | 55 | 77 | 5.4 | 138 |
| 140% | 630 | 44 | 68 | 6.9 | 137 |

Two points on this curve are directly relevant to alarm thresholds elsewhere in this manual:

- The **minimum continuous stable flow** referenced by `FLOW_LOW_05` (Sections 3.3, 4.5) is set well above the shutoff point shown here, since operating close to shutoff head for any sustained period risks internal recirculation and overheating even though the pump is technically still producing flow.
- The **NPSH required** column rises steeply beyond the 100% rated flow point, which is why the `CAV_DET_08` mitigation of reducing flow toward the best efficiency point (Section 4.6 Step 2) is effective — moving from 120–140% flow back toward the 80–100% range reduces the NPSH required at a rate that typically outpaces any corresponding drop in NPSH available, clearing a marginal cavitation condition within seconds.

This curve reflects the standard 285 mm impeller trim only; a unit that has been up-trimmed toward the 315 mm maximum casing bore (Section 1.3) will show a different curve and should have its own trim-specific reference data obtained from engineering before being used as a troubleshooting baseline.

---

# Section 2: Installation & Commissioning Procedures

## 2.1 Pre-Installation Inspection

Before Pump-1, Pump-2, or Pump-3 is unpacked at its final installation location, perform the following inspection and record results in the commissioning checklist:

1. Verify the shipping crate is undamaged and the tilt/shock indicators (if fitted) have not been triggered.
2. Confirm nameplate data (Section 1.5) matches the purchase order and the intended install location (Bay 1, Bay 2, or Bay 3).
3. Rotate the shaft by hand at the coupling. It should turn freely with no binding, grinding, or unusual resistance. Record the direction of free rotation.
4. Inspect flange faces for shipping damage, rust preventative buildup, or foreign debris. Clean flange faces with a non-abrasive solvent before piping is connected.
5. Confirm bearing housing grease fittings are present and undamaged, and that shipping grease (a lower-grade preservative grease, not the service-fill grease) has not been mistaken for a completed lubrication fill.
6. Confirm the mechanical seal has not been shipped with the axial shipping clip still installed; if fitted, do not remove it until the pump is fully installed on the baseplate and ready for final alignment, per Section 2.6.

## 2.2 Site and Foundation Requirements

Each pump bay (Bay 1, Bay 2, Bay 3) in the Utility Pump House is designed with an independent reinforced concrete foundation sized at a minimum of three times the combined pump-motor-baseplate weight (610 kg per unit), per standard hydraulic institute practice for vibration damping. Foundation top surface must be level to within 0.5 mm per meter prior to baseplate placement.

Minimum clearances around each installed unit:

| Direction | Minimum Clearance |
|---|---|
| Front (coupling/motor end, for future pull-out) | 1.2 m |
| Rear (casing/piping end) | 0.6 m |
| Sides | 0.5 m |
| Overhead (for lifting equipment access) | 2.0 m |

These clearances are required not only for maintenance access but also for the ambient airflow around the motor and VFD cabinet discussed in Section 6.

## 2.3 Rigging and Lifting

The complete pump-motor-baseplate assembly (610 kg) must be lifted using the four tapped lifting points on the baseplate. Do not lift the assembly using eyebolts on the motor frame alone, and never lift by rigging through the pump casing or discharge flange, as this can spring the baseplate out of alignment before it has ever been grouted.

1. Use a rated 4-leg chain sling or spreader bar sized for the full assembly weight plus a minimum 25% safety margin.
2. Confirm no personnel are positioned beneath the suspended load at any point during the lift.
3. Lower the assembly onto pre-placed leveling wedges or jack screws at the foundation location, not directly onto the bare foundation.

## 2.4 Baseplate Installation and Grouting

1. Position the baseplate on leveling wedges at the four corner points and rough-level using a precision machinist's level placed on the machined motor and pump mounting pads.
2. Shim as required until level is within 0.1 mm per meter in both axes.
3. Confirm foundation bolt sleeves are clear of debris, then install anchor bolts finger-tight only at this stage — final torque is applied after grout cure.
4. Build a grout form around the baseplate perimeter, leaving the underside grout cavity open per baseplate design.
5. Pour a non-shrink, epoxy-based grout to fill the full cavity beneath the baseplate in a single continuous pour, working from one end to avoid trapping air pockets.
6. Allow grout to cure per the grout manufacturer's data sheet (typically 5–7 days for full structural cure at 20 °C) before torquing anchor bolts to final value and proceeding to alignment.

## 2.5 Piping Connections

Suction and discharge piping must be independently supported so that no piping weight, thermal expansion load, or misalignment strain is transmitted into the pump casing flanges. Before final bolt-up, confirm piping flanges meet the pump flanges with no more than 0.5 mm gap and no forced alignment (i.e., the piping should meet the flange under its own support, not be pulled into place with the flange bolts).

Required in-line components on every unit:

- A basket-type suction strainer (40 mesh) immediately upstream of the suction flange, fitted with local differential pressure gauge — this strainer is the primary root cause investigated under alarm code `SUCT_STRAIN_15` (Section 3).
- An eccentric reducer at the suction flange (flat side up) if the suction header diameter differs from the 200 mm suction connection, to avoid trapping air at the top of the reducer.
- A check valve and isolation valve on the discharge side of each unit, both located far enough downstream that they do not restrict flow to the discharge pressure transmitter tap.
- A seal flush line per API Plan 11, routed from a discharge tap through a flow control orifice back to the seal chamber, with a local flow sight glass.
- An auxiliary cooling water tap for the seal flush cooling jacket where ambient conditions require it (see Section 6.7).

## 2.6 Alignment Procedure

Final shaft alignment between pump and motor must be performed after grout cure and anchor bolt torque, and again verified after piping bolt-up (piping strain can shift alignment even when piping is nominally "free").

1. Remove the coupling guard and coupling spacer.
2. Mount a laser alignment system (or dial indicators, if laser equipment is unavailable) across the coupling hubs.
3. Measure and record angular and parallel offset in both the vertical and horizontal planes.
4. Target alignment tolerance for the MP-4300 Series at the coupling: parallel offset ≤ 0.05 mm, angular offset ≤ 0.05 mm/100 mm of coupling spacer length. These are tighter than the coupling manufacturer's maximum allowable values by design margin, since alignment drift is a leading contributor to `VIB_HIGH_04` and `COUPL_MISALIGN_11` alarms (Section 3) over the service life of the unit.
5. Correct alignment using shims under the motor feet only — never shim under the pump feet, as the pump centerline is the fixed reference.
6. Re-torque motor hold-down bolts to spec after final shim adjustment and re-verify alignment did not shift during torqueing.
7. Reinstall the coupling spacer and guard, and confirm the guard does not contact the rotating coupling at any point through a full manual rotation.

## 2.7 Electrical Connections and VFD Setup

1. Confirm motor nameplate voltage, frequency, and rotation match the supply and the VFD configuration before energizing.
2. Verify the VFD is programmed with the correct motor nameplate parameters (voltage, current, frequency, pole count) and that the minimum speed floor is set to 20 Hz to avoid sustained low-flow operation risk (see `FLOW_LOW_05`, Section 3).
3. Confirm the VFD carrier frequency and output filtering are configured per the motor manufacturer's recommendation to minimize bearing current damage from PWM switching transients.
4. Perform a phase rotation check with the coupling disconnected (motor solo run) to confirm rotation matches the direction arrow cast into the pump casing before the coupling is reconnected.
5. Confirm all three PTC winding thermistor circuits and both bearing RTD circuits show a valid resistance reading at the PumpGuard controller terminal strip before closing up the motor terminal box.

## 2.8 Instrumentation Wiring and PumpGuard Controller Commissioning

Each PumpGuard controller must be commissioned individually per unit tag before that unit is placed in service:

1. Confirm the controller is configured with the correct unit tag (Pump-1 / Pump-2 / Pump-3) — a mis-tagged controller will log alarms under the wrong unit identity in the historian and DCS, which is a common root cause of confusing maintenance records.
2. Load the standard MP-4300 alarm threshold configuration set (see Section 3 for the full list of codes and default thresholds).
3. Verify each of the following instrument loops with a simulated or physical test signal before leaving the site: bearing RTDs (DE/NDE), winding thermistors (3 phases), vibration sensors (DE/NDE), suction and discharge pressure transmitters, discharge flowmeter, seal chamber leak sensor, baseplate drip-tray leak sensor.
4. Confirm the local E-Stop pushbutton correctly triggers `ESTOP_ACT_19` and removes the run permissive at the VFD.
5. Confirm Modbus TCP communication to the plant DCS is established and that all 20 alarm codes map correctly to their assigned DCS alarm points.

## 2.9 Pre-Start Checks

Before the first start of any unit, confirm:

- Bearing housings are filled to the correct grease level per Section 5.7 (not over-greased — over-greasing is a common cause of early bearing temperature alarms).
- Seal flush line is open and flow is visible at the sight glass.
- Suction valve is fully open and discharge valve is cracked open (approximately 10%) for the initial start, to avoid deadheading the pump against a closed valve.
- Casing is fully vented of air via the casing vent valve, with fluid observed at the vent before closing it.
- Coupling guard is installed and secure.
- All temporary shipping restraints have been removed from the mechanical seal and coupling.

## 2.10 Initial Start-Up Procedure

The three units are commissioned sequentially, starting with Pump-1, so that any systemic issue (piping, header pressure, control logic) is identified and resolved before Pump-2 and Pump-3 are exposed to it.

1. Start the unit at minimum VFD speed (20 Hz) and confirm smooth rotation, no abnormal noise, and stable suction/discharge pressure readings for a minimum of 2 minutes.
2. Gradually ramp speed toward the rated operating point (nominally 60 Hz / 1,780 rpm) over no less than 5 minutes, monitoring bearing temperature, vibration, and motor current continuously.
3. Slowly open the discharge valve to the fully open position once stable operation is confirmed at rated speed, adjusting VFD speed as required to reach the rated flow/head duty point.
4. Hold the unit at duty point for a minimum 30-minute run-in period, logging bearing temperature, vibration, motor current, suction pressure, discharge pressure, and flow at 5-minute intervals.
5. Confirm no PumpGuard alarms are active at the end of the run-in period.
6. Repeat for the remaining two units.

## 2.11 Performance Verification and Commissioning Sign-off

At the conclusion of run-in for each unit, record the following in the commissioning record and compare against the rated specifications in Section 1.4:

- Measured flow at rated speed (acceptance band: rated flow ±5%)
- Measured total head at rated flow (acceptance band: rated head ±5%)
- Bearing temperatures, DE and NDE (must be stable and below the `TEMP_HIGH_01` Warning threshold defined in Section 3)
- Vibration levels, DE and NDE (must be within ISO 10816-3 Zone A/B for a newly commissioned machine)
- Motor current at duty point (must be below nameplate full-load current of 218 A)
- Seal flush flow rate and confirmation of no visible seal leakage

Commissioning is not considered complete, and the unit should not be released to routine automatic duty rotation, until all values above are recorded within acceptance bands and signed off by both the commissioning engineer and the site reliability engineer. Retain the signed commissioning record permanently as the baseline reference for all future vibration and temperature trending.

## 2.12 Key VFD Parameters to Verify at Commissioning

In addition to the motor nameplate parameters and minimum speed floor described in Section 2.7, the following VFD parameters should be explicitly confirmed and recorded (not merely left at factory default) during commissioning of each unit:

| Parameter | Typical Setting | Relevance |
|---|---|---|
| Minimum output frequency | 20 Hz | Prevents sustained operation in the low-flow region associated with `FLOW_LOW_05` and `CAV_DET_08` |
| Maximum output frequency | 60 Hz | Matches rated speed; should not be increased beyond nameplate without an engineering review of resulting hydraulic and mechanical loading |
| Acceleration ramp time | 10–15 seconds to rated speed | Avoids a hard, high-current start that stresses the coupling and can contribute to `MOTOR_OVLD_09` on a marginal supply |
| Deceleration ramp time | 15–20 seconds | Avoids water-hammer transients in the discharge header on stop, particularly relevant when Pump-3 is commanded to stop after an auto-start event |
| Current limit | Motor nameplate full-load current (218 A) plus drive-specific service factor per the drive manufacturer's data sheet | Misconfiguration here is a documented root cause of nuisance `MOTOR_OVLD_09` trips (Section 4.7 Step 4) |
| Carrier (switching) frequency | Per motor manufacturer recommendation for the cable length installed | Excessively high carrier frequency increases motor bearing current risk; excessively low carrier frequency increases audible noise and motor heating contributing to `TEMP_HIGH_02` |
| Modbus communication timeout | Per PumpGuard controller default | A timeout set too short can produce nuisance `VFD_FAULT_12` events during normal plant network congestion |

Recording these values in the commissioning file, alongside the nameplate and performance data in Section 2.11, gives future troubleshooting activity (Section 4) a documented baseline to compare against when a parameter is suspected to have drifted or been inadvertently changed during later service work.

## 2.13 Common Commissioning Pitfalls and Their Downstream Alarm Consequences

Experience across the MP-4300 Series install base shows that a small number of commissioning shortcuts account for a disproportionate share of later alarm activity. These are called out explicitly here so that commissioning personnel understand not just the procedural step but the consequence of skipping it:

- **Starting duty rotation before the grout has fully cured (Section 2.4).** Anchor bolts torqued against uncured or partially cured grout can loosen slightly as curing completes, producing a slow alignment drift over the following weeks that later presents as a `COUPL_MISALIGN_11` or `VIB_HIGH_04` event with no obvious immediate cause. Always confirm cure time against the grout manufacturer's data sheet before final torque, not against a generic assumption.
- **Treating alignment as a one-time task rather than a verify-after-piping-bolt-up task (Section 2.6).** Piping strain introduced during final bolt-up is a common source of alignment that was correct before piping connection but out of tolerance afterward. Skipping the post-piping alignment check is one of the most frequent root causes of an early-life `VIB_HIGH_04` or `TEMP_HIGH_01` event on a newly commissioned unit.
- **Omitting the seal flush sight-glass baseline flow reading (Section 2.11).** Without a recorded baseline flush flow rate, a later reduced-flow condition cannot be reliably distinguished from normal unit-to-unit variation, which delays root-cause diagnosis under Section 4.3.
- **Leaving the mechanical seal shipping clip in place through commissioning, or removing it too early (Section 2.1).** Either error risks damaging the seal faces before the unit ever reaches revenue service, and any resulting `SEAL_FAIL_03` event within the first days of operation should prompt a check of the commissioning record for this specific step.
- **Mis-tagging the PumpGuard controller (Section 2.8).** A controller commissioned under the wrong unit tag silently corrupts the historian record for both the mis-tagged unit and whichever unit's tag it was mistakenly assigned, and this error is often not discovered until a maintenance history review under Section 5.10 fails to reconcile with observed physical work. Confirm the unit tag displayed on the local HMI against the physical nameplate (Section 1.5) as the very first commissioning step for each controller, before any instrument loop verification.

## 2.14 Documentation Handover Package

On completion of commissioning for each unit, the following documentation must be assembled into a permanent handover package and filed both in the site CMMS and in the physical or electronic equipment file for that unit tag, before the unit is released to the maintenance organization for routine operation:

| Document | Source | Purpose |
|---|---|---|
| Signed commissioning record | Section 2.11 | Performance and condition baseline for all future comparisons |
| VFD parameter record | Section 2.12 | Baseline for detecting later configuration drift |
| Alignment record (initial and post-piping) | Section 2.6 | Baseline for future alignment verification (Section 5.5) |
| Instrument loop verification checklist | Section 2.8 | Confirms each protective input was functional at handover |
| Nameplate and CMMS asset record cross-check | Section 1.5 | Confirms no documentation discrepancy exists at the point of handover, when it is easiest to correct |
| As-built piping and instrumentation deviations (if any) from the reference design | Site engineering records | Ensures later troubleshooting is not based on an assumed configuration that was actually changed during installation |

A unit should not be released to automatic duty rotation, nor should Pump-3 be armed for standby auto-start, until this package is complete. An incomplete handover package is not merely a paperwork gap: several of the diagnostic procedures in Section 4 (notably `TEMP_HIGH_01` in Section 4.2 and `VIB_HIGH_04` in Section 4.4) depend on comparing a current reading against the specific unit's own commissioning baseline, and a missing or incomplete baseline materially weakens the diagnostic value of every future alarm investigation on that unit for the remainder of its service life.

---

# Section 3: Full Alarm Code Matrix

## 3.1 How to Use This Section

Every alarm raised by the PumpGuard controller on Pump-1, Pump-2, or Pump-3 is identified by one of the twenty standardized codes below. Each code is fixed across all three units — the same code always means the same condition, regardless of which unit tag raised it. The summary table gives a quick-reference view; the subsections that follow give the full detail (likely causes and recommended immediate steps) for each code. Six of these codes — `TEMP_HIGH_01`, `SEAL_FAIL_03`, `VIB_HIGH_04`, `FLOW_LOW_05`, `CAV_DET_08`, `MOTOR_OVLD_09`, and `POWER_PHASE_14` — have full step-by-step diagnostic procedures in Section 4; this section gives the first-response summary for all twenty.

Severity levels used throughout this manual:

- **Warning** — degraded condition, unit remains in service, investigate at next opportunity.
- **Critical** — unit performance or equipment integrity at risk, investigate promptly; some Critical codes are configured to auto-trip the unit.
- **Safety** — condition involves a safety interlock or protective device; unit is stopped and will not restart until the interlock is manually cleared.

## 3.2 Summary Table

| Code | Description | Severity | Auto-Trip? |
|---|---|---|---|
| `TEMP_HIGH_01` | Bearing Temperature High (DE or NDE) | Warning at 85 °C / Critical at 100 °C | Yes, at Critical threshold |
| `TEMP_HIGH_02` | Motor Winding Temperature High | Critical | Yes |
| `SEAL_FAIL_03` | Mechanical Seal Failure / Leak Detected | Critical | No (operator decision) |
| `VIB_HIGH_04` | Excessive Vibration (DE or NDE) | Warning at Zone C / Critical at Zone D (ISO 10816-3) | Yes, at Critical threshold |
| `FLOW_LOW_05` | Low Flow / Dry-Run Risk | Critical | Yes |
| `PRESS_LOW_06` | Discharge Pressure Low | Warning | No |
| `PRESS_HIGH_07` | Discharge Pressure High | Warning | No |
| `CAV_DET_08` | Cavitation Detected (acoustic/vibration signature) | Warning, escalates to Critical if sustained | Yes, if sustained >10 min |
| `MOTOR_OVLD_09` | Motor Overload / Overcurrent | Critical | Yes |
| `LUBE_LOW_10` | Bearing Lubricant Level/Condition Low | Warning | No |
| `COUPL_MISALIGN_11` | Coupling Misalignment Detected | Warning | No |
| `VFD_FAULT_12` | VFD Communication or Drive Fault | Critical | Yes |
| `SENSOR_FAIL_13` | Instrument/Sensor Signal Failure | Warning | No |
| `POWER_PHASE_14` | Phase Loss / Voltage Imbalance | Critical | Yes |
| `SUCT_STRAIN_15` | Suction Strainer Differential Pressure High | Warning | No |
| `BEARING_WEAR_16` | Bearing Wear / Degradation Trend | Warning | No |
| `LEAK_DET_17` | External Process Leak Detected (baseplate drip tray) | Critical | No (operator decision) |
| `SPEED_DEV_18` | Speed Deviation (commanded vs. actual) | Warning | No |
| `ESTOP_ACT_19` | Emergency Stop Activated | Safety | Yes (immediate) |
| `COOLANT_LOW_20` | Auxiliary Cooling/Flush Water Flow Low | Warning | No |

## 3.3 Detailed Alarm Descriptions

### `TEMP_HIGH_01` — Bearing Temperature High

**Severity:** Warning at 85 °C sustained for 2 minutes; Critical (auto-trip) at 100 °C sustained for 30 seconds, either bearing (DE or NDE).

**Likely causes:**
- Bearing lubrication degraded, low, or contaminated
- Bearing wear or incipient failure
- Shaft misalignment (see `COUPL_MISALIGN_11`) inducing abnormal bearing loads
- Elevated ambient temperature around the bearing housing (see Section 6)
- RTD sensor fault giving a false high reading (cross-check against `SENSOR_FAIL_13` history)

**Recommended immediate steps:**
1. Confirm the reading against the second bearing RTD and, if accessible, a handheld infrared reading at the bearing housing before assuming the sensor is correct.
2. Check bearing housing grease level and condition per Section 5.7.
3. Check recent vibration trend for the same bearing (Section 3.3, `VIB_HIGH_04`) — a coincident vibration rise strongly suggests a mechanical cause rather than a lubrication or ambient cause.
4. If temperature reaches the Critical threshold, allow the automatic trip to occur; do not override the trip.
5. Full diagnostic procedure: see Section 4.2.

### `TEMP_HIGH_02` — Motor Winding Temperature High

**Severity:** Critical (auto-trip) when any of the three phase PTC thermistors exceeds its rated trip resistance.

**Likely causes:**
- Sustained motor overload (see `MOTOR_OVLD_09`)
- Blocked or fouled motor cooling fan/shroud
- Elevated ambient temperature at the motor location, or inadequate enclosure ventilation (see Section 6.7)
- VFD harmonic content causing additional motor heating
- Voltage imbalance (see `POWER_PHASE_14`)

**Recommended immediate steps:**
1. Allow the auto-trip to complete; do not attempt to restart until winding temperature has returned to normal and the trigger condition has been identified.
2. Inspect the motor cooling fan and shroud for obstruction or debris.
3. Review VFD output current trend for the period preceding the trip for signs of sustained overload.
4. Check for an open `POWER_PHASE_14` or recent phase imbalance event in the historian.
5. If ambient conditions are suspected, refer to Section 6 for ambient design limits and mitigation.

### `SEAL_FAIL_03` — Mechanical Seal Failure / Leak Detected

**Severity:** Critical. Does not auto-trip by default (site-configurable), since a slow seal weep may be manageable for a short period until a planned shutdown, but sustained operation with an active `SEAL_FAIL_03` risks bearing housing contamination and floor-level fluid hazard.

**Likely causes:**
- Seal face wear reaching end of service life
- Dry-running or momentary loss of flush flow (see `COOLANT_LOW_20`, `FLOW_LOW_05`)
- Thermal shock from rapid temperature change at start-up
- Elastomer (EPDM) degradation from chemical incompatibility or age
- Improper seal flush orifice sizing or flush line blockage

**Recommended immediate steps:**
1. Confirm the alarm at the seal chamber moisture sensor and visually inspect the seal chamber drain and weep hole for active leakage.
2. Check seal flush flow at the sight glass; a blocked flush line is a common and easily corrected root cause.
3. If leakage is a slow weep, plan a controlled shutdown for seal replacement within the current shift; if leakage is a stream or spray, stop the unit immediately.
4. Full diagnostic procedure: see Section 4.3.

### `VIB_HIGH_04` — Excessive Vibration

**Severity:** Warning at ISO 10816-3 Zone C; Critical (auto-trip) at Zone D, either bearing housing.

**Likely causes:**
- Shaft misalignment (see `COUPL_MISALIGN_11`)
- Impeller or rotor imbalance
- Cavitation (see `CAV_DET_08`)
- Bearing wear (see `BEARING_WEAR_16`)
- Loose foundation bolts, degraded grout, or baseplate resonance
- Loose coupling guard or other loose attached hardware (a frequent false-positive source)

**Recommended immediate steps:**
1. Confirm the vibration spectrum against the baseline signature recorded at commissioning (Section 2.11) to identify whether the dominant frequency is 1x running speed (imbalance/misalignment), blade-pass frequency (cavitation/hydraulic), or bearing defect frequency (bearing wear).
2. Visually inspect for loose external hardware (guards, brackets, conduit) before assuming a rotor-dynamic cause.
3. Full diagnostic procedure: see Section 4.4.

### `FLOW_LOW_05` — Low Flow / Dry-Run Risk

**Severity:** Critical (auto-trip) if flow remains below the minimum continuous stable flow threshold for more than 60 seconds.

**Likely causes:**
- Suction strainer blockage (see `SUCT_STRAIN_15`)
- Suction or discharge valve inadvertently left closed or partially closed
- Low level in the upstream supply tank
- Air entrainment or vortexing at the suction source
- Worn impeller or wear rings reducing pump performance below duty point

**Recommended immediate steps:**
1. Confirm suction and discharge valve positions.
2. Check upstream tank level.
3. Check suction strainer differential pressure.
4. Full diagnostic procedure: see Section 4.5.

### `PRESS_LOW_06` — Discharge Pressure Low

**Severity:** Warning.

**Likely causes:**
- Impeller wear or wear ring clearance excessive (loss of hydraulic performance)
- Entrained air or vapor lock in the casing
- Incorrect motor/pump rotation direction
- Leak in the discharge piping between the pump and the pressure transmitter tap

**Recommended immediate steps:**
1. Confirm casing is fully vented of air (see Section 2.9).
2. Confirm rotation direction matches the casing arrow.
3. Trend discharge pressure against flow to distinguish a genuine performance loss (falling on the same curve) from a control/valve issue.

### `PRESS_HIGH_07` — Discharge Pressure High

**Severity:** Warning.

**Likely causes:**
- Downstream control valve closed or fully throttled
- Blockage in the discharge line or at the heat exchanger inlet
- Discharge pressure transmitter fault or drift
- An unintended change in downstream system configuration, such as a manual valve left closed following unrelated maintenance elsewhere on the discharge header

**Recommended immediate steps:**
1. Confirm downstream valve positions and heat exchanger inlet strainer condition.
2. Cross-check reading against the redundant header pressure transmitter, if fitted.
3. Do not throttle the pump discharge valve to "fix" a high reading without first confirming the reading is genuine, since throttling a healthy pump toward shutoff head risks overheating from low flow (see `FLOW_LOW_05`).
4. Where two units (for example Pump-1 and Pump-2) are running simultaneously on the common discharge header, confirm whether both units show the same elevated reading; a header-wide condition points toward a downstream restriction, while an elevated reading on only one unit points toward that unit's own discharge check valve or local instrumentation.

### `CAV_DET_08` — Cavitation Detected

**Severity:** Warning; escalates to Critical (auto-trip) if the characteristic acoustic/vibration cavitation signature is sustained for more than 10 minutes.

**Likely causes:**
- Insufficient NPSH margin at current operating point
- Suction strainer blockage (see `SUCT_STRAIN_15`)
- Excessive suction lift or low supply tank level
- Air entrainment at the suction source
- Operating significantly to the right of the pump's best efficiency point (high flow, low head)

**Recommended immediate steps:**
1. Reduce flow (via VFD speed) toward the best efficiency point as an immediate mitigation while the root cause is investigated.
2. Check suction strainer differential pressure and supply tank level.
3. Full diagnostic procedure: see Section 4.6.

### `MOTOR_OVLD_09` — Motor Overload / Overcurrent

**Severity:** Critical (auto-trip).

**Likely causes:**
- Mechanical binding in the pump (impeller rub, bearing seizure, foreign object)
- Voltage imbalance across phases (see `POWER_PHASE_14`)
- Fluid density or viscosity higher than design basis
- Impeller obstruction by debris
- VFD parameter misconfiguration (incorrect current limit or motor nameplate data)

**Recommended immediate steps:**
1. Do not attempt an immediate restart after an overload trip without first checking for mechanical binding by hand-rotating the shaft (with power isolated).
2. Review VFD current trend leading up to the trip.
3. Full diagnostic procedure: see Section 4.7.

### `LUBE_LOW_10` — Bearing Lubricant Level/Condition Low

**Severity:** Warning.

**Likely causes:**
- Grease fitting or bearing seal leak
- Missed scheduled lubrication interval (see Section 5.7)
- Grease degradation from sustained high bearing temperature

**Recommended immediate steps:**
1. Inspect bearing housing for external grease leakage at seals and fittings.
2. Re-grease per the schedule and quantity in Section 5.7 if the condition is simply an overdue interval.
3. If lubricant is contaminated (discolored, gritty, or emulsified with water), this indicates a bearing housing seal failure and should be escalated for bearing housing inspection rather than simply re-greased.

### `COUPL_MISALIGN_11` — Coupling Misalignment Detected

**Severity:** Warning. Detected via a persistent 1x/2x running-speed vibration signature pattern correlated between DE and NDE sensors, consistent with the alignment-drift signature characterized at commissioning.

**Likely causes:**
- Original installation alignment outside tolerance (see Section 2.6)
- Thermal growth differential between pump and motor not accounted for during cold alignment
- Foundation settling or grout degradation over time
- Worn coupling elastomer insert

**Recommended immediate steps:**
1. Schedule a laser alignment check at the next planned outage; this condition rarely requires an immediate unplanned shutdown but should not be deferred indefinitely, since it is a direct contributor to `VIB_HIGH_04` and `TEMP_HIGH_01`.
2. Inspect the coupling insert for visible wear or degradation during the same outage.

### `VFD_FAULT_12` — VFD Communication or Drive Fault

**Severity:** Critical (auto-trip, since loss of VFD control is treated as loss of speed control).

**Likely causes:**
- Damaged or disconnected Modbus communication cable between VFD and PumpGuard controller
- VFD internal overtemperature fault
- VFD firmware fault or unexpected reset
- Electromagnetic interference on the communication cable run

**Recommended immediate steps:**
1. Check the VFD's own local fault display/log for a specific internal fault code before assuming a communications-only issue.
2. Inspect the Modbus cable and connectors for damage.
3. If the standby unit (Pump-3) is available, confirm it has started per the auto-start interlock while the faulted unit is investigated.

### `SENSOR_FAIL_13` — Instrument/Sensor Signal Failure

**Severity:** Warning. Raised when any monitored instrument loop reads outside its physically valid range (open circuit, short circuit, or out-of-range signal), rather than an in-range but abnormal process value.

**Likely causes:**
- Damaged signal cable or connector corrosion (common at outdoor or wash-down-exposed junction boxes)
- Failed transmitter or sensing element
- Moisture ingress at a junction box with a compromised IP65 seal

**Recommended immediate steps:**
1. Identify which specific instrument loop is flagged from the PumpGuard alarm detail (this code is a general instrument-fault category covering all monitored loops, not a single sensor).
2. Inspect the field wiring and junction box for the affected loop before replacing the sensing element.
3. Note that a `SENSOR_FAIL_13` on a temperature or vibration input disables the corresponding protective function for that input until cleared — treat this as reducing the unit's protection coverage, not merely as a nuisance alarm.

### `POWER_PHASE_14` — Phase Loss / Voltage Imbalance

**Severity:** Critical (auto-trip).

**Likely causes:**
- Upstream breaker or fuse failure on one phase
- Loose or corroded terminal connection at the motor or VFD input
- Utility supply fault or imbalance upstream of the plant switchgear

**Recommended immediate steps:**
1. Do not attempt to restart the unit until phase voltages have been confirmed balanced and within tolerance at the motor terminals.
2. Full diagnostic procedure: see Section 4.8.

### `SUCT_STRAIN_15` — Suction Strainer Differential Pressure High

**Severity:** Warning.

**Likely causes:**
- Debris loading on the strainer basket from normal operation
- Missed strainer cleaning interval (see Section 5.5)
- Upstream process upset introducing unusual debris loading

**Recommended immediate steps:**
1. Confirm current differential pressure against the clean-strainer baseline recorded at commissioning.
2. Plan strainer cleaning before differential pressure approaches the level associated with `FLOW_LOW_05` or `CAV_DET_08` risk.

### `BEARING_WEAR_16` — Bearing Wear / Degradation Trend

**Severity:** Warning. Distinct from `VIB_HIGH_04` in that this code is raised by trend analysis of bearing-defect-frequency vibration components over time, rather than a single overall vibration amplitude threshold — it is intended as an early-warning trend indicator ahead of an amplitude-based alarm.

**Likely causes:**
- Normal end-of-life bearing wear-out
- Lubrication contamination (see `LUBE_LOW_10`)
- Extended operation with marginal misalignment (see `COUPL_MISALIGN_11`)

**Recommended immediate steps:**
1. Review the bearing-defect-frequency trend over the preceding weeks in the PumpGuard historian.
2. Schedule bearing replacement at the next planned outage rather than waiting for an amplitude-based `VIB_HIGH_04` trip.

### `LEAK_DET_17` — External Process Leak Detected

**Severity:** Critical. Raised by the baseplate drip-tray moisture sensor, indicating fluid has escaped containment at the pump base rather than being confined to the seal chamber drain.

**Likely causes:**
- Casing gasket or fitting failure
- Drain plug loose or missing
- Secondary leakage path from an unresolved `SEAL_FAIL_03` condition

**Recommended immediate steps:**
1. Visually confirm the source and severity of the leak before deciding whether to stop the unit immediately or continue to a controlled shutdown.
2. Treat as an environmental/housekeeping hazard in addition to an equipment fault — refer to Section 7 (Appendix A) for spill response guidance.

### `SPEED_DEV_18` — Speed Deviation

**Severity:** Warning. Raised when the VFD's reported actual output speed deviates from the commanded speed by more than 3% for longer than 30 seconds.

**Likely causes:**
- Speed feedback encoder or sensorless-estimation fault
- Mechanical binding limiting actual achievable speed
- VFD parameter fault

**Recommended immediate steps:**
1. Compare against motor current at the time of deviation — a speed deviation with elevated current suggests mechanical binding; a speed deviation with normal current suggests a feedback/estimation fault.
2. Cross-check against any open `VFD_FAULT_12` or `SENSOR_FAIL_13` condition.

### `ESTOP_ACT_19` — Emergency Stop Activated

**Severity:** Safety (immediate stop, no auto-trip delay).

**Likely causes:**
- Local E-Stop pushbutton manually pressed
- Safety interlock circuit fault
- Coupling guard or other safety guard interlock opened while the unit was running

**Recommended immediate steps:**
1. Do not reset or restart the unit until the cause of the E-Stop event has been positively identified.
2. Follow the lockout/tagout and restart authorization procedure in Section 7 (Appendix A) before returning the unit to service.

### `COOLANT_LOW_20` — Auxiliary Cooling / Flush Water Flow Low

**Severity:** Warning.

**Likely causes:**
- Strainer blockage in the seal flush line
- Flush line isolation valve inadvertently closed
- Loss of auxiliary supply pressure to the flush circuit

**Recommended immediate steps:**
1. Confirm flush line valve positions and sight glass flow.
2. Treat a sustained `COOLANT_LOW_20` as a precursor risk to `SEAL_FAIL_03` and prioritize correction accordingly.

## 3.4 Alarm Acknowledgement, Reset, and Escalation

All twenty alarm codes follow a common lifecycle at the PumpGuard controller, regardless of severity:

1. **Raise.** The controller detects the triggering condition and raises the alarm on the local HMI and to the plant DCS, with a timestamp and the triggering value logged to the historian.
2. **Acknowledge.** An operator or technician acknowledges the alarm at the HMI, silencing any audible annunciation. Acknowledgement does not clear the underlying condition and does not, by itself, permit a tripped unit to restart.
3. **Investigate.** The applicable procedure from Section 3.3 (summary) or Section 4 (full procedure, where available) is followed to identify and correct the root cause.
4. **Clear.** Once the underlying condition has returned to within normal operating range, the alarm clears automatically at the controller; Warning-severity alarms clear without operator action once the condition resolves, while Critical- and Safety-severity alarms that caused an auto-trip require an explicit manual reset at the HMI before a restart can be commanded, even after the underlying condition has cleared.
5. **Reset.** Manual reset of a Critical or Safety alarm should only be performed once the root cause has been identified and corrected, per the specific procedure — never as a first response to "see if it happens again," since this discards diagnostic information (the fact that the condition persisted long enough to trip) without addressing it.

**Nuisance alarm handling.** Where a specific alarm is confirmed, through the diagnostic procedures in Section 4 or the general principles in Section 4.1, to be a false trigger from a faulty sensor (`SENSOR_FAIL_13`) rather than a genuine process condition, the affected input may be temporarily forced to a safe bypass state by the site reliability engineer while the sensor is repaired or replaced. This bypass must be time-limited, documented in the maintenance record (Section 5.10), and reversed immediately once the sensor is restored — an indefinitely bypassed protective input defeats the purpose of the PumpGuard system and must not be treated as a routine or long-term state.

**Escalation criteria.** Any alarm that recurs more than twice within a rolling 7-day period on the same unit, even if each individual event was successfully cleared, should be escalated from routine maintenance handling to a formal reliability review, since a recurring alarm indicates the underlying root cause was not actually resolved by the corrective action taken, only temporarily masked.

## 3.5 Threshold Configuration and Site Customization

The default thresholds referenced throughout this section (for example, 85 °C / 100 °C for `TEMP_HIGH_01`, or ISO 10816-3 Zone C/D for `VIB_HIGH_04`) are the MP-4300 Series factory defaults loaded during commissioning per Section 2.8. Some thresholds may be adjusted within a documented engineering change process to reflect site-specific conditions:

- Thresholds tied to a published standard (ISO 10816-3 vibration zones, motor nameplate current for `MOTOR_OVLD_09`) should generally not be relaxed, since doing so directly reduces the equipment protection margin the standard is designed to preserve.
- Thresholds tied to site-specific or process-specific conditions (minimum continuous flow for `FLOW_LOW_05`, suction strainer differential pressure for `SUCT_STRAIN_15`) may reasonably be tuned once sufficient operating history exists to establish a unit-specific normal band, provided the change is reviewed and approved by the site reliability engineer and documented in the maintenance record (Section 5.10).
- Any threshold change must be applied consistently across Pump-1, Pump-2, and Pump-3, since these units share a common duty and are compared against one another (see Section 6.8) to distinguish unit-specific mechanical issues from fleet-wide ambient or process effects — inconsistent thresholds between the three units would undermine that comparison.
- Threshold changes should never be made as an undocumented workaround to stop a specific alarm from recurring; if an alarm is recurring, the correct response is the escalation path above, not a threshold relaxation that merely stops the symptom from being reported.

## 3.6 Detection Signature Reference

The table below summarizes the primary sensor input and detection logic behind each alarm code, which is useful when a technician needs to quickly judge whether a given alarm could plausibly be a sensor artifact (see `SENSOR_FAIL_13` and the general principle in Section 4.1) before beginning a full investigation.

| Code | Primary Input(s) | Detection Logic |
|---|---|---|
| `TEMP_HIGH_01` | Bearing RTDs (DE/NDE) | Threshold-and-duration: sustained above Warning/Critical setpoint for the configured dwell time |
| `TEMP_HIGH_02` | Winding PTC thermistors (3-phase) | Resistance step-change past the PTC's rated trip point on any phase |
| `SEAL_FAIL_03` | Seal chamber moisture/leak sensor | Binary moisture detection at the seal chamber drain |
| `VIB_HIGH_04` | Bearing housing accelerometers (DE/NDE) | Overall vibration amplitude classified against ISO 10816-3 zone boundaries |
| `FLOW_LOW_05` | Discharge magnetic flowmeter | Threshold-and-duration below minimum continuous stable flow |
| `PRESS_LOW_06` / `PRESS_HIGH_07` | Discharge pressure transmitter | Threshold deviation from the expected pressure band for current speed/flow |
| `CAV_DET_08` | Vibration accelerometers, spectral analysis | Pattern match against the characteristic blade-pass/broadband cavitation signature |
| `MOTOR_OVLD_09` | VFD current feedback | Threshold-and-duration above configured current limit |
| `LUBE_LOW_10` | Manual inspection entry / grease-life timer | Time-since-last-service counter combined with technician-entered condition observation |
| `COUPL_MISALIGN_11` | Vibration accelerometers, DE/NDE phase correlation | Trend analysis of correlated 1x/2x running-speed components between the two bearing housings |
| `VFD_FAULT_12` | VFD internal diagnostics via Modbus | Drive-reported fault code or loss of Modbus communication |
| `SENSOR_FAIL_13` | Any monitored instrument loop | Out-of-physical-range signal (open or short circuit) rather than an in-range abnormal value |
| `POWER_PHASE_14` | VFD input voltage sensing | Phase-to-phase voltage comparison against balance tolerance |
| `SUCT_STRAIN_15` | Strainer differential pressure transmitter | Threshold deviation from the clean-strainer baseline |
| `BEARING_WEAR_16` | Vibration accelerometers, spectral analysis | Trend analysis of bearing-defect-frequency amplitude over time |
| `LEAK_DET_17` | Baseplate drip-tray moisture sensor | Binary moisture detection, physically separate from the seal chamber sensor |
| `SPEED_DEV_18` | VFD commanded vs. actual speed feedback | Percentage deviation threshold sustained over a configured duration |
| `ESTOP_ACT_19` | Local E-Stop circuit / safety relay | Hardwired safety circuit state, independent of the PumpGuard software logic |
| `COOLANT_LOW_20` | Seal flush line flow switch | Threshold-and-duration below minimum flush flow |

Because `SENSOR_FAIL_13` and `ESTOP_ACT_19` are architecturally distinct from the process-condition alarms (the former detects a signal validity problem across any loop, the latter is a hardwired safety circuit rather than a software threshold), neither can itself be dismissed as a "nuisance" alarm caused by another sensor fault in the way that, for example, an isolated `TEMP_HIGH_01` reading might be — both should always be treated as reported.

---

# Section 4: Detailed Troubleshooting Procedures

This section expands seven of the twenty alarm codes from Section 3 into full step-by-step diagnostic procedures: `TEMP_HIGH_01`, `SEAL_FAIL_03`, `VIB_HIGH_04`, `FLOW_LOW_05`, `CAV_DET_08`, `MOTOR_OVLD_09`, and `POWER_PHASE_14`. These seven were selected because they represent the highest-frequency and highest-consequence alarm events observed across the MP-4300 Series install base, and because several of them (notably `TEMP_HIGH_01`, `VIB_HIGH_04`, and `CAV_DET_08`) are frequently root-caused to a common set of underlying mechanical conditions — misalignment, cavitation, and lubrication — so diagnosing one thoroughly often resolves or prevents another.

Each procedure assumes the technician has reviewed the corresponding summary entry in Section 3 and has basic access to the PumpGuard local HMI and historian trend data.

## 4.1 General Diagnostic Principles

Before following any of the specific procedures below, apply these general principles, which hold across nearly all alarm conditions on the MP-4300 Series:

- **Confirm before correcting.** A meaningful fraction of alarms on any rotating equipment fleet trace back to a faulty sensor rather than a genuine process condition (see `SENSOR_FAIL_13`). Always cross-check a suspect reading against a second sensor, a handheld instrument, or a physical inspection before taking corrective action on the equipment itself.
- **Check the historian trend, not just the instantaneous value.** A slowly rising trend over days or weeks points to a different class of root cause (wear, fouling, lubrication depletion) than a sudden step change (sensor fault, mechanical failure, external event).
- **Consider Pump-3's standby status.** If the affected unit is Pump-3, confirm whether the alarm occurred during an idle standby period, a scheduled exercise run (Section 5.4), or a live auto-start event, since the expected baseline behavior differs between these states.
- **Record findings against the unit's individual commissioning baseline** (Section 2.11), not against a generic specification, since minor unit-to-unit variation is normal and expected.

## 4.2 `TEMP_HIGH_01` — Bearing Temperature High: Diagnostic Procedure

1. **Verify the alarm.** At the PumpGuard HMI, note which bearing (DE or NDE) and which unit raised the alarm, the peak temperature reached, and whether the unit auto-tripped at the Critical threshold (100 °C) or remains running at the Warning threshold (85 °C).
2. **Cross-check the reading.** Compare against the opposite bearing's temperature and, where safe to approach the running or recently-stopped unit, take a handheld infrared reading at the bearing housing surface near the RTD location. A reading confirmed by two independent methods can be treated as real; a large discrepancy points toward `SENSOR_FAIL_13` on the RTD circuit.
3. **Review the trend.** Pull the last 30 days of bearing temperature history for the affected bearing from the PumpGuard historian.
   - A gradual rise over weeks suggests lubrication degradation or slow bearing wear.
   - A step change coincident with a specific event (recent maintenance, a process upset, a change in ambient conditions) points to that event as the likely trigger.
   - A rise that tracks ambient temperature (compare against Section 6 ambient monitoring data) suggests an environmental contribution rather than a purely mechanical one.
4. **Check vibration on the same bearing.** Pull the corresponding vibration trend (Section 3.3, `VIB_HIGH_04`). A coincident rise in both temperature and vibration on the same bearing strongly indicates a mechanical root cause — misalignment, imbalance, or bearing wear — rather than a purely thermal/lubrication issue.
5. **Inspect lubrication.** With the unit isolated and locked out (Section 7), remove a small grease sample from the bearing housing relief port. Check for:
   - Discoloration (dark brown/black indicates thermal degradation)
   - Grittiness (indicates contamination or bearing wear debris)
   - Emulsification or a milky appearance (indicates water ingress through a failed housing seal)
   Any of these findings indicates the bearing housing should be opened for full inspection rather than simply re-greased.
6. **Inspect for misalignment.** If lubrication is found to be in acceptable condition, perform a laser alignment check per Section 2.6 procedure. Realign if outside tolerance and re-run the unit, monitoring bearing temperature over the following 24–48 hours.
7. **If no lubrication or alignment cause is found**, schedule the bearing for replacement at the next planned outage as a precaution, and continue monitoring at increased frequency (daily rather than the standard weekly review, Section 5.3) until the outage.
8. **Document.** Record the finding, corrective action, and post-correction temperature trend in the unit's maintenance history, since this record establishes whether the corrective action was effective or whether the alarm recurs.

## 4.3 `SEAL_FAIL_03` — Mechanical Seal Failure: Diagnostic Procedure

1. **Confirm the alarm source.** The PumpGuard seal chamber sensor detects moisture/leakage at the seal chamber drain. Confirm this is the actual trigger and not a `LEAK_DET_17` from the baseplate drip tray, which indicates a different (and generally more serious) leak path.
2. **Assess leak severity visually**, from a safe position with the unit still running if conditions allow:
   - **Weep/mist** — a light film or occasional drip. Generally acceptable to continue running to a planned shutdown within the current shift.
   - **Steady drip or stream** — indicates active face damage or a flush problem. Plan for shutdown within the hour.
   - **Spray or continuous stream** — stop the unit immediately; continued operation risks bearing housing contamination and floor-level hazard.
3. **Check seal flush flow** at the sight glass installed per Section 2.5. No visible flow, or a flow rate visibly reduced from the baseline recorded at commissioning, points to a blocked flush line or orifice as the likely trigger — this is the single most common recoverable root cause of `SEAL_FAIL_03` on the MP-4300 Series and should be ruled out before assuming face damage.
4. **Check for a preceding `COOLANT_LOW_20` or `FLOW_LOW_05` event** in the historian in the hours before the seal alarm. A period of low or interrupted flush flow, or a dry-run/low-flow event, is a common precursor that damages seal faces even if it self-clears before triggering its own alarm.
5. **If flush flow is confirmed normal and leakage continues**, the seal faces or elastomers have likely reached end of life or suffered thermal/mechanical damage. Plan for seal cartridge replacement; do not attempt to "run out" a confirmed face-damaged seal, since continued operation risks bearing housing fluid ingress.
6. **During seal replacement**, inspect the old seal faces for wear pattern:
   - Uniform wear across the face suggests normal end-of-life.
   - Heat-cracking or discoloration suggests a dry-run or flush interruption event.
   - Chipped or fractured faces suggest a mechanical shock event (e.g., a hard start against a closed valve, or debris in the flush line).
7. **After replacement**, re-verify flush flow at the sight glass and monitor the seal chamber sensor closely for the first 24 hours of operation, since infant-mortality failures of a newly installed seal (from improper installation or a damaged elastomer) typically present within this window.
8. **Document** the wear pattern observed and suspected root cause, since a recurring pattern of thermal-damage seal failures on a given unit is a strong indicator of an underlying flush system or dry-run problem that needs separate correction, not just repeated seal replacement.

## 4.4 `VIB_HIGH_04` — Excessive Vibration: Diagnostic Procedure

1. **Confirm the alarm** and note which bearing housing (DE or NDE), the peak amplitude reached, and the ISO 10816-3 zone (Warning = Zone C, Critical = Zone D).
2. **Pull the vibration spectrum** (not just overall amplitude) from the PumpGuard historian and identify the dominant frequency component:
   - **1x running speed** — most consistent with imbalance or bearing misalignment.
   - **2x running speed** — most consistent with coupling misalignment specifically.
   - **Blade-pass frequency** (impeller vane count × running speed) — consistent with a hydraulic cause; check for cavitation (`CAV_DET_08`) or recirculation at off-design flow.
   - **Bearing defect frequencies** (calculated from bearing geometry) — consistent with bearing wear; cross-check against any open `BEARING_WEAR_16` trend alarm.
   - **Broadband, no clear dominant frequency** — consider loose external hardware (guards, brackets) or foundation/grout degradation before assuming a rotor-dynamic cause.
3. **Compare against the commissioning baseline spectrum** (Section 2.11) to determine whether this is a new frequency component (pointing to a new fault) or a growth in amplitude of a component that was already present at low level (pointing to progression of a known, previously acceptable condition).
4. **If 1x or 2x dominant:** perform a physical inspection walk-down, checking coupling guard security, visible coupling insert condition, and foundation bolt tightness, before scheduling a laser alignment check per Section 2.6.
5. **If blade-pass or hydraulic signature dominant:** cross-reference current operating point (flow/head) against the pump curve and suction conditions; follow the `CAV_DET_08` procedure (Section 4.6) if cavitation is suspected.
6. **If bearing-defect frequency dominant:** treat as an advanced-stage bearing condition (beyond the early-warning stage covered by `BEARING_WEAR_16`) and schedule bearing replacement promptly rather than at the next routine outage.
7. **If the unit auto-tripped at Critical (Zone D):** do not restart until at least a visual and alignment check has been completed; restarting a unit with unresolved severe vibration risks rapid progression to catastrophic bearing or shaft damage.
8. **Document** the spectral signature and corrective action for trend comparison at the next alarm event.

## 4.5 `FLOW_LOW_05` — Low Flow / Dry-Run Risk: Diagnostic Procedure

1. **Confirm the alarm** and note the flow reading at the point of trip against the minimum continuous stable flow threshold.
2. **Check valve positions first** — confirm both the suction and discharge isolation valves for the affected unit are fully open. An inadvertently left, or newly, closed valve (for example, following maintenance on an adjacent unit) is the single most common root cause and should always be checked before more invasive investigation.
3. **Check upstream supply tank level.** A low level in the source tank, especially during high-demand periods when both duty pumps are running, can reduce available NPSH below the required margin and trigger both `FLOW_LOW_05` and `CAV_DET_08` together.
4. **Check suction strainer differential pressure** (`SUCT_STRAIN_15`). A heavily loaded strainer restricts flow in the same way a closed valve does, and is a common root cause during periods of elevated debris loading upstream.
5. **Check for air entrainment.** Inspect the suction tank or sump for vortexing at low level, or for any recent air introduction into the suction piping (e.g., from maintenance work upstream that has not yet been fully vented).
6. **If valve positions, tank level, and strainer are all confirmed normal**, suspect impeller or wear-ring degradation reducing the pump's actual performance below its rated curve at the commanded speed. Compare current discharge pressure at the commanded speed against the baseline curve from commissioning (Section 2.11); a pressure shortfall at the same speed indicates a genuine performance loss requiring pump internals inspection at the next outage.
7. **Before restarting a tripped unit**, resolve the identified root cause; do not simply reset the alarm and restart without a known corrective action, since repeated dry-run events cause cumulative and eventually irreversible damage to the mechanical seal (see Section 4.3) even if no single event is long enough to cause an immediate failure.
8. **Document** the root cause and, where the cause was upstream (valve, level, strainer) rather than internal to the pump, notify operations so the upstream condition can be corrected or monitored going forward.

## 4.6 `CAV_DET_08` — Cavitation Detected: Diagnostic Procedure

1. **Confirm the alarm** and note whether it is still in the Warning stage or has escalated toward the 10-minute sustained threshold that triggers an auto-trip.
2. **Reduce flow toward the best efficiency point immediately** as a first-response mitigation, via VFD speed reduction, while the underlying cause is investigated — this is both a corrective action and a diagnostic step, since cavitation from an insufficient NPSH margin typically clears audibly and on the vibration signature within seconds of reducing flow.
3. **Check suction strainer differential pressure** (`SUCT_STRAIN_15`) and supply tank level, using the same checks as `FLOW_LOW_05` Steps 3–4, since insufficient NPSH is the most common shared root cause between the two alarms.
4. **Check for suction air entrainment**, particularly vortexing at the tank outlet if the tank level is at or near its low operating limit.
5. **If cavitation persists after flow reduction and strainer/level checks are clear**, review whether the unit is being operated significantly to the right of its best efficiency point on a sustained basis (i.e., whether the plant demand profile has shifted since commissioning); this may indicate a duty-point mismatch requiring an engineering review rather than a maintenance correction.
6. **Cross-check the vibration spectrum** for the blade-pass frequency signature described in Section 4.4 Step 2 to confirm the cavitation diagnosis independently of the acoustic detection.
7. **If the unit auto-tripped**, do not restart at the same flow condition that caused the trip; restart at reduced speed and re-approach the duty point gradually while monitoring for recurrence.
8. **Document** the operating conditions (flow, suction pressure, tank level) at the time of the event, since a recurring pattern tied to a specific time of day or production condition (e.g., peak demand periods when tank level is drawn down) points to a process-level cause rather than an equipment fault.

## 4.7 `MOTOR_OVLD_09` — Motor Overload / Overcurrent: Diagnostic Procedure

1. **Confirm the alarm** and pull the motor current trend from the VFD/PumpGuard historian for the minutes leading up to the trip, noting whether the current rose gradually or stepped up suddenly.
2. **Before any restart attempt, isolate electrical power and hand-rotate the shaft** at the coupling (with the coupling guard removed per Section 2.6 procedure) to check for mechanical binding, grinding, or abnormally high rotating resistance. Do not attempt an electrical restart to "test" a suspected mechanical bind, since this risks further damage or a repeat trip under load.
3. **If the shaft rotates freely**, review recent `POWER_PHASE_14` history for any voltage imbalance event coincident with or preceding the overload, since imbalance increases motor current draw even under normal mechanical load.
4. **If no phase imbalance is found**, verify VFD configuration parameters (current limit, motor nameplate data) against the values specified in Section 2.7 to rule out a configuration fault rather than a genuine overload condition.
5. **If the shaft does not rotate freely**, this indicates a mechanical bind requiring further disassembly to locate: common causes on the MP-4300 Series include a seized bearing (cross-check recent `TEMP_HIGH_01` or `BEARING_WEAR_16` history), impeller contact with the casing wear ring (from a dropped shaft due to bearing failure), or foreign debris that has entered through the suction piping.
6. **If a gradual current rise was observed** rather than a sudden step, consider a process-side cause: fluid density or viscosity higher than the design basis (e.g., from an upstream process change), which increases hydraulic loading and motor current at a given flow without any pump mechanical fault.
7. **Once the root cause is corrected**, restart at reduced VFD speed if possible and ramp gradually to the duty point while monitoring current, rather than commanding full speed immediately.
8. **Document** the root cause; a mechanical bind finding should trigger a full teardown inspection at the next outage even if the immediate obstruction is cleared, since the underlying cause of the bind (e.g., bearing damage) may not be fully resolved by simply freeing the shaft.

## 4.8 `POWER_PHASE_14` — Phase Loss / Voltage Imbalance: Diagnostic Procedure

1. **Confirm the alarm** and note which phase(s) were affected and the magnitude of imbalance or the specific phase reported lost.
2. **Do not restart the unit** until phase voltages have been measured and confirmed balanced and within tolerance at the motor terminals directly, since restarting into a genuine phase-loss condition risks immediate `MOTOR_OVLD_09` and potential winding damage.
3. **Check the upstream breaker or fuse** for the affected unit's motor circuit for a tripped or blown condition on a single phase — this is the most common single-unit root cause.
4. **If the breaker/fuse is intact**, check terminal connections at the motor junction box and at the VFD output terminals for looseness or corrosion, working from the motor back toward the VFD.
5. **If terminals and protective devices are confirmed sound on the affected unit alone, check whether other units (Pump-1/2/3) or other loads on the same electrical bus experienced a coincident event.** A simultaneous event across multiple units points to an upstream supply-side fault (utility or plant switchgear level) rather than a fault local to the single unit, and should be escalated to the electrical/utility team rather than pursued as a pump maintenance item.
6. **Once the fault is corrected and phase voltages confirmed balanced**, restart per the standard start-up sequence (Section 2.10), monitoring current closely through the ramp to rated speed.
7. **Document** whether the event was isolated to one unit or affected multiple units on the same bus, since this distinction determines whether the corrective action and follow-up belong to pump maintenance or to plant electrical/utility maintenance.

## 4.9 Cross-Cutting Root Cause Relationships

The seven procedures above are presented as independent alarm responses, but in practice a small number of underlying mechanical and process conditions are shared root causes across several of them. Recognizing these relationships allows a technician to investigate more efficiently, since correcting one underlying condition often resolves or prevents several alarm codes at once, and conversely, a repair that only addresses the alarm that happened to trip first may leave the shared root cause in place to trigger a different code next.

- **Misalignment** (Section 2.6) is a direct or contributing cause of `VIB_HIGH_04` (Section 4.4), `TEMP_HIGH_01` (Section 4.2), and the trend-based `COUPL_MISALIGN_11` (Section 3.3). A unit presenting any one of these should have alignment checked even if the alarm that actually triggered was a different one of the three, and a laser alignment correction performed for one should be expected to improve the trend on the others.
- **Insufficient NPSH margin** is the shared root cause behind `FLOW_LOW_05` (Section 4.5) and `CAV_DET_08` (Section 4.6), and both procedures point back to the same three checks — suction strainer differential pressure, supply tank level, and suction air entrainment — for exactly this reason. A site experiencing one of these alarms during periods of high combined demand (both duty pumps running, tank level drawn down) should treat the other as a likely near-term risk under the same conditions, not as an unrelated event.
- **Seal flush interruption** links `COOLANT_LOW_20` (Section 3.3) directly to `SEAL_FAIL_03` (Section 4.3) as a precursor-to-consequence pair. Because a brief flush interruption can damage seal faces even if it self-clears before triggering its own alarm, a technician investigating an unexplained `SEAL_FAIL_03` should always pull the flush-flow and `COOLANT_LOW_20` history for the preceding hours, per Section 4.3 Step 4, rather than assuming the seal simply reached end of life.
- **Lubrication condition** connects `LUBE_LOW_10`, `TEMP_HIGH_01` (Section 4.2), and `BEARING_WEAR_16` (Section 3.3) as a single degradation pathway: degraded or depleted lubrication first presents as a `LUBE_LOW_10` or a slow bearing temperature rise, and if not corrected, progresses to measurable bearing wear and eventually to `VIB_HIGH_04` at bearing-defect frequency (Section 4.4 Step 2). Catching this pathway at the `LUBE_LOW_10` stage is significantly less costly than catching it at the `VIB_HIGH_04` stage.
- **Electrical supply quality** connects `POWER_PHASE_14` (Section 4.8) and `MOTOR_OVLD_09` (Section 4.7): a voltage imbalance event that does not itself reach the phase-loss threshold can still elevate motor current enough to approach or trigger an overload trip. Reviewing `POWER_PHASE_14` history is accordingly an explicit step within the `MOTOR_OVLD_09` procedure (Section 4.7 Step 3), and the reverse check is equally valid — a `POWER_PHASE_14` event should prompt a review of motor current trend even if no overload trip occurred.

## 4.10 Post-Repair Verification and Return-to-Service Checklist

Regardless of which of the seven procedures above was followed, the following verification steps apply generally before returning a unit to automatic duty rotation (Pump-1/Pump-2) or standby-armed status (Pump-3) after any Critical or Safety alarm event:

1. **Confirm the specific corrective action taken** is recorded against the unit and the alarm code in the maintenance record (Section 5.10), including parts replaced, adjustments made, and any threshold or configuration changes per Section 3.5.
2. **Run the unit at reduced speed first**, where the VFD and process conditions allow, rather than commanding full rated speed immediately on restart, so that early signs of an incomplete repair (recurring vibration, temperature rise, or current draw) are observed under lower mechanical stress before the unit is loaded to its duty point.
3. **Monitor continuously, not just at shift-change intervals, for the first two hours of operation following any bearing, seal, or alignment-related repair**, since infant-mortality failures of a freshly repaired or replaced component typically present within this window (see also Section 4.3 Step 7 for the seal-specific version of this guidance).
4. **Compare post-repair readings against the unit's own commissioning baseline** (Section 2.11) rather than against a generic specification, to confirm the repair has actually returned the unit to its established normal operating band and not merely to a value that happens to sit below the alarm threshold.
5. **Re-arm all bypassed instrument inputs** (Section 3.4, nuisance alarm handling) that may have been temporarily forced to a safe state during the investigation, and confirm each shows a valid, in-range reading before the unit is released to service.
6. **For Pump-3 specifically**, confirm the standby auto-start interlock (Section 1.2) is restored and functional following any repair, since a repair sequence that leaves the unit in a manual-only or interlock-bypassed state defeats its role as the installed standby without necessarily being obvious from a simple visual inspection.

## 4.11 Tools and Instruments Required

The following tools and instruments are required to carry out the seven diagnostic procedures in this section, and should be maintained in a calibrated, ready-to-use state in the Utility Pump House tool store rather than sourced ad hoc at the time of an alarm event:

| Tool/Instrument | Used In | Notes |
|---|---|---|
| Handheld infrared thermometer | Section 4.2 (`TEMP_HIGH_01`) | For cross-checking RTD readings against a physical measurement |
| Laser shaft alignment system | Sections 4.2, 4.4, 2.6 | Primary method; dial indicators are an acceptable fallback per Section 2.6 |
| Vibration analyzer with spectral (FFT) capability | Sections 4.4, 4.6, 3.6 | Overall-amplitude-only meters are insufficient for the spectral diagnosis described in Section 4.4 Step 2 |
| Grease sampling kit | Section 4.2 Step 5 | Includes sample containers for condition inspection (discoloration, grit, emulsification) |
| Clamp-on multimeter / phase rotation tester | Sections 4.7, 4.8, 2.7 | For motor current and phase voltage/rotation verification |
| Insulation resistance tester (megohmmeter) | Section 4.7 (extended investigation) | Where a mechanical bind is ruled out and winding insulation condition needs verification |
| Portable ultrasonic leak/flow detector | Section 4.3, 4.5 | Useful for confirming flush line flow or detecting a suction-side air ingress point not visible externally |
| PumpGuard historian workstation access | All seven procedures | Required for trend review; field investigation without historian access should be considered incomplete per Section 4.1 |

Technicians dispatched to investigate any of the seven alarm codes in this section should confirm access to the relevant tools from this table before beginning the physical investigation, since an interrupted investigation (stopping partway through to retrieve a tool) increases the risk of an incomplete lockout/tagout re-verification per Section A.3.

---

# Section 5: Routine Maintenance Schedule

## 5.1 Maintenance Philosophy

The MP-4300 Series maintenance schedule combines fixed-interval preventive tasks (cleaning, lubrication, inspection) with condition-based tasks driven by PumpGuard trend data (vibration, temperature, bearing-defect frequency). Fixed intervals below are the minimum required frequency; any unit trending toward an alarm threshold ahead of schedule (per Section 4 diagnostic procedures) should have its maintenance interval shortened accordingly rather than waiting for the next scheduled date.

Because Pump-3 operates in standby for the majority of its service life rather than continuous duty, its schedule includes an additional weekly exercise-run requirement (Section 5.4) not applicable to Pump-1 and Pump-2, to prevent standby-specific failure modes such as brinelling of stationary bearings and grease channeling.

## 5.2 Daily Checks (All Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Visual walk-down | Inspect for visible leaks at seal, casing, and piping connections | `SEAL_FAIL_03`, `LEAK_DET_17` |
| Unusual noise/vibration | Listen for abnormal noise; note any change from baseline | `VIB_HIGH_04`, `CAV_DET_08` |
| PumpGuard HMI review | Confirm no active or unacknowledged alarms on any of the three units | All codes |
| Seal flush sight glass | Confirm visible flow | `COOLANT_LOW_20`, `SEAL_FAIL_03` |
| Baseplate drip tray | Visually confirm dry / no accumulated fluid | `LEAK_DET_17` |

## 5.3 Weekly Checks (All Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Vibration trend review | Review 7-day vibration trend for all three units at the PumpGuard historian | `VIB_HIGH_04`, `BEARING_WEAR_16` |
| Bearing temperature trend review | Review 7-day bearing temperature trend | `TEMP_HIGH_01` |
| Suction strainer differential pressure | Record and compare against clean-strainer baseline | `SUCT_STRAIN_15` |
| Motor current trend | Review for gradual upward drift | `MOTOR_OVLD_09` |
| Coupling guard security | Confirm guard is secure and undamaged | `VIB_HIGH_04` (false-positive prevention) |

## 5.4 Monthly Checks (All Units) and Standby-Specific Tasks

| Task | Action | Related Alarm Codes |
|---|---|---|
| Suction strainer cleaning | Isolate, open, and clean strainer basket regardless of differential pressure reading | `SUCT_STRAIN_15`, `FLOW_LOW_05` |
| Bearing grease condition sample | Extract small sample from relief port, inspect per Section 4.2 Step 5 | `LUBE_LOW_10`, `TEMP_HIGH_01` |
| Alignment visual check | Confirm coupling insert wear and guard condition | `COUPL_MISALIGN_11` |
| Instrument loop spot-check | Verify one rotating instrument loop per visit against a reference reading | `SENSOR_FAIL_13` |
| **Pump-3 only:** Standby exercise run | Auto-start Pump-3 via manual test command, run at duty point for minimum 30 minutes, verify all parameters against baseline, return to standby | All codes (functional test) |

The Pump-3 exercise run is not optional and should not be skipped even during periods when Pump-1 and Pump-2 are both healthy and fully available; a standby unit that has not been run recently is significantly more likely to fail on demand than one exercised monthly.

## 5.5 Quarterly Checks (All Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Full bearing re-grease | Purge and replenish grease per Section 5.7 quantities | `LUBE_LOW_10`, `TEMP_HIGH_01`, `BEARING_WEAR_16` |
| Laser alignment verification | Full laser alignment check per Section 2.6 procedure | `COUPL_MISALIGN_11`, `VIB_HIGH_04` |
| Vibration spectral baseline comparison | Full spectrum analysis against commissioning baseline (Section 2.11), not just overall amplitude | `VIB_HIGH_04`, `BEARING_WEAR_16` |
| Seal flush orifice inspection | Remove and inspect flush orifice for partial blockage | `SEAL_FAIL_03`, `COOLANT_LOW_20` |
| Electrical connection torque check | Verify motor and VFD terminal torque per Section 5.8 | `POWER_PHASE_14`, `MOTOR_OVLD_09` |

## 5.6 Annual Checks / Major Overhaul Planning

| Task | Action | Related Alarm Codes |
|---|---|---|
| Bearing housing full inspection | Open bearing housing, inspect bearings, replace if wear indicators present | `BEARING_WEAR_16`, `TEMP_HIGH_01` |
| Mechanical seal planned replacement | Replace seal cartridge on a planned basis regardless of current condition, per Section 4.3 wear-pattern guidance from the prior seal removal | `SEAL_FAIL_03` |
| Wear ring / impeller clearance inspection | Measure and record clearances; compare against commissioning baseline | `PRESS_LOW_06`, `FLOW_LOW_05` |
| Full performance curve verification | Re-run the commissioning performance verification (Section 2.11) at multiple flow points | All hydraulic-related codes |
| Foundation and grout inspection | Inspect for cracking, settling, or bolt looseness | `VIB_HIGH_04`, `COUPL_MISALIGN_11` |
| PumpGuard controller calibration | Full instrument loop calibration check, all inputs | `SENSOR_FAIL_13` |

## 5.7 Lubrication Schedule and Specifications

| Item | Lubricant | Quantity per Bearing Housing | Interval |
|---|---|---|---|
| Drive-end and non-drive-end bearings | NLGI Grade 2 lithium-complex grease | 45 g per relief cycle | Quarterly (Section 5.5), or immediately upon `LUBE_LOW_10` |
| Bearing grease sample check | N/A (inspection only) | N/A | Monthly (Section 5.4) |
| Coupling insert (if lubricated type — standard MP-4300 coupling is non-lubricated elastomeric) | Not applicable | Not applicable | Not applicable |

Over-greasing is as harmful as under-greasing on angular contact bearings: excess grease increases churning losses and can itself drive bearing temperature toward the `TEMP_HIGH_01` Warning threshold. Always purge the correct calculated quantity for the specific bearing size, not a generalized "fill until it appears at the relief port" approach.

## 5.8 Torque Specifications (Key Fasteners)

| Fastener | Torque |
|---|---|
| Casing bolts (M20) | 285 N·m |
| Bearing housing cap bolts (M12) | 75 N·m |
| Coupling hub set screws | 35 N·m |
| Motor foot bolts (M16) | 175 N·m |
| Baseplate anchor bolts (M24) | 450 N·m |
| Motor terminal box lugs | Per motor manufacturer nameplate/data sheet — verify at each quarterly electrical check (Section 5.5) |

## 5.9 Recommended Spare Parts and Insurance Spares

To minimize downtime across the three-unit set, the following spares are recommended to be held on site rather than ordered on demand:

| Part | Recommended Quantity On-Hand | Rationale |
|---|---|---|
| Mechanical seal cartridge, complete | 1 per unit (3 total) | `SEAL_FAIL_03` is the leading cause of unplanned downtime; lead time on this component historically exceeds acceptable downtime |
| Bearing set (DE + NDE), matched pair | 1 set, shared across the fleet | Bearings are interchangeable across all three units |
| Coupling insert | 2 | Low cost, consumable wear item |
| Suction strainer basket | 1 spare basket per unit | Allows immediate swap during cleaning (Section 5.4) without downtime |
| PumpGuard controller (spare unit) | 1, shared across the fleet | Minimizes downtime from a `VFD_FAULT_12`-adjacent controller hardware fault |
| RTD and thermistor sensor sets | 1 spare set per sensor type | Addresses `SENSOR_FAIL_13` events without waiting on procurement |

The recommended on-hand quantities above are sized against typical procurement lead times for each component class, summarized below. Where actual site-specific lead times are longer than shown — for example, due to a change in supplier or a component obsolescence issue — the recommended on-hand quantity should be increased proportionally rather than left at the default value in the table above.

| Part Category | Typical Procurement Lead Time | Consequence of Stock-Out |
|---|---|---|
| Mechanical seal cartridge | 3–6 weeks | Extended unplanned downtime on any unit experiencing `SEAL_FAIL_03`; with only Pump-3 as standby, a second concurrent seal failure on a duty unit would leave the installation running on a single pump |
| Bearing set | 2–4 weeks | Delays return to service following any Section 4.2 or Section 5.6 bearing finding |
| Coupling insert | 1–2 weeks | Low individual impact given low cost and simple replacement, but should not be allowed to reach zero stock given how routinely it is consumed |
| Suction strainer basket | 1 week | Delays the strainer-swap approach described in Section 5.4 for zero-downtime cleaning; without a spare basket, cleaning requires a brief unit outage instead |
| PumpGuard controller | 6–10 weeks | The longest lead-time item on this list; a controller hardware fault without a spare on hand risks extended loss of protective monitoring on the affected unit, which is a materially different and more serious risk than loss of the pump itself |
| RTD/thermistor sensor sets | 1–2 weeks | Delays clearing a `SENSOR_FAIL_13` condition, during which the corresponding protective function remains degraded per the note in Section 3.3 |

Given the long lead time on the PumpGuard controller itself relative to other components, and the fact that a controller fault removes protective monitoring rather than merely stopping the pump, the spare controller should be treated as the highest-priority item on this list to keep in stock and periodically function-tested on the bench, not merely stored as a sealed spare of unverified condition.

## 5.10 Maintenance Record Keeping

All maintenance actions, whether scheduled or triggered by an alarm event under Section 4, must be logged against the specific unit tag (Pump-1, Pump-2, or Pump-3) in the site CMMS, cross-referenced to the relevant alarm code where applicable. This record-keeping discipline is what allows the trend-based codes — `BEARING_WEAR_16`, `LUBE_LOW_10`, `COUPL_MISALIGN_11` — to function as genuine early-warning indicators rather than one-off events, since their value depends on comparing each new reading against an accurate history of prior findings and corrective actions for that specific unit.

## 5.11 Consumables, Waste Handling, and Disposal

Routine and corrective maintenance on Pump-1, Pump-2, and Pump-3 generates several categories of waste material that must be handled per the site's environmental procedures, in addition to the equipment-focused tasks described elsewhere in this section:

- **Used bearing grease**, whether from the quarterly full re-grease (Section 5.5) or a condition sample taken during a `TEMP_HIGH_01` investigation (Section 4.2 Step 5), should be collected and disposed of as the site's lubricant waste stream specifies, not washed down a floor drain — this is particularly relevant if the sample shows signs of water emulsification, which may itself be subject to different handling requirements than normal used grease.
- **Removed mechanical seal cartridges** (Section 4.3, Section 5.6) contain elastomer, carbide, and carbon components; segregate for the site's mixed-materials waste stream and inspect for the wear-pattern indicators described in Section 4.3 Step 6 before disposal, since this inspection is only possible before the component leaves site.
- **Suction strainer debris** (Section 5.4) should be characterized before disposal if an upstream process upset is suspected as the cause of an unusual debris load, since the debris itself may be diagnostic evidence of an upstream issue that is otherwise difficult to trace after the fact.
- **Spill or leak response materials** used following a `SEAL_FAIL_03` or `LEAK_DET_17` event (Section A.7) should be disposed of per the site's procedure for the specific process fluid, and any containment or barricade materials should be logged as part of the event's maintenance record even though they are not equipment components themselves.

## 5.12 Condition Monitoring Review Cadence

Beyond the fixed-interval tasks in Sections 5.2 through 5.6, the PumpGuard historian trend data for all three units should be formally reviewed by the site reliability engineer (not merely spot-checked by maintenance technicians during routine rounds) on the following cadence:

| Review | Frequency | Purpose |
|---|---|---|
| Cross-unit comparison review | Monthly | Compare bearing temperature, vibration, and motor current baselines across Pump-1, Pump-2, and Pump-3 to distinguish unit-specific drift from fleet-wide ambient or process effects (see Section 6.8) |
| Trend-code review (`BEARING_WEAR_16`, `LUBE_LOW_10`, `COUPL_MISALIGN_11`) | Monthly | Confirm these early-warning trends are being acted on before they progress to an amplitude-based Critical alarm, per the degradation pathway described in Section 4.9 |
| Alarm recurrence review | Monthly | Apply the escalation criteria in Section 3.4 across the full alarm history, not just alarms an individual technician happened to notice recurring |
| Full commissioning-baseline re-comparison | Annual, aligned with Section 5.6 | Confirm each unit's current performance and vibration/temperature baseline against its original Section 2.11 commissioning record, to catch slow multi-year drift that would not be visible in any single monthly comparison |

This cadence is what allows the fixed-interval and condition-based elements of this maintenance program to function together: fixed intervals catch known wear-out patterns on a predictable schedule, while the review cadence above catches the unpredictable or gradually emerging conditions that a fixed interval alone would not reliably surface in time.

## 5.13 Seasonal Maintenance Adjustments

The fixed-interval schedule in Sections 5.2 through 5.6 applies year-round, but the following seasonal adjustments should be made in coordination with the ambient effects discussed in Section 6.5:

- **Ahead of the summer high-ambient period**, bring forward the quarterly VFD cabinet air filter check (Section 6.7) if the preceding winter's inspection showed any debris loading, since reduced cabinet cooling margin compounds with naturally higher ambient temperature to increase `VFD_FAULT_12` risk during the warmest months.
- **Ahead of the winter low-ambient period**, review cold-start behavior expectations with operations staff per Section 6.5, so that a brief elevated-friction start-up period is not mistaken for a new `TEMP_HIGH_01` condition and investigated as an unplanned event.
- **During any period of unusually high or low ambient temperature relative to the site's normal seasonal range**, increase the frequency of the weekly bearing temperature and vibration trend review (Section 5.3) to a shorter interval until conditions return to the normal range, so that a genuine mechanical issue emerging during a period of ambient stress is not masked by, or confused with, the expected ambient-driven baseline shift described in Section 6.8.

These adjustments are coordination points between the fixed maintenance schedule in this section and the ambient/environmental considerations in Section 6 — they do not replace either the fixed schedule or the Section 6 guidance, but ensure the two are applied together rather than independently.

---

# Section 6: Thermal Management & Ambient Operating Conditions

## 6.1 Purpose and Relationship to Section 3 / Section 4

This section addresses pump thermal behavior from the perspective of the **installation environment** — ambient temperature, ventilation, enclosure design, and seasonal variation — as distinct from the **alarm-response perspective** already covered for `TEMP_HIGH_01` (Sections 3.3 and 4.2) and `TEMP_HIGH_02` (Section 3.3). Sections 3 and 4 address what to do once a bearing or winding temperature alarm has already been raised on a specific unit. This section addresses how the surrounding installation environment influences how often those alarms occur in the first place, and what site-level and installation-level conditions should be corrected so that Pump-1, Pump-2, and Pump-3 are not chronically operating close to their thermal alarm thresholds under normal, fault-free conditions.

A unit that trips `TEMP_HIGH_01` repeatedly despite passing every mechanical check in Section 4.2 (lubrication, alignment, vibration) should prompt a review of this section's ambient and installation factors before further mechanical disassembly is pursued.

## 6.2 Ambient Temperature Design Envelope

The MP-4300 Series is rated for the ambient envelope specified in Section 1.4: −10 °C to 50 °C. This envelope assumes reasonably free air circulation around the bearing housing and motor frame. It does not assume the unit is installed in an enclosed, unventilated space, nor does it assume direct solar exposure on an outdoor skid without shading — both conditions can produce a local ambient temperature at the equipment significantly above the general site ambient temperature reported by a plant weather station.

As a rule of thumb for the MP-4300 Series, every 10 °C of sustained ambient temperature rise above 30 °C reduces the effective margin to the `TEMP_HIGH_01` Warning threshold (85 °C) by approximately 3–4 °C at a given mechanical load, since the bearing housing rejects heat to the surrounding air at a rate proportional to the temperature differential between the housing and its surroundings.

## 6.3 Installation Location Considerations

Pump-1, Pump-2, and Pump-3 are installed indoors in the Utility Pump House, which provides shading and general weather protection but is not a climate-controlled space. The following installation-level factors should be periodically reviewed, particularly if any unit begins trending warmer than its sister units under equivalent load:

- **Airflow obstruction.** Stored materials, temporary equipment, or accumulated debris placed within the clearance envelope specified in Section 2.2 restrict natural convective airflow around the bearing housing and motor. Bay clearances should be re-inspected as part of the annual review (Section 5.6), not only at initial installation.
- **Radiant heat from adjacent equipment.** The Utility Pump House shares space with other process equipment; a unit installed adjacent to a hot process line or heat exchanger may run warmer than an otherwise identical unit in a different bay purely from radiant heat pickup, independent of its own mechanical condition.
- **Roof and wall solar loading.** Even an indoor installation can see meaningful ambient temperature rise in the hours following peak solar loading on an un-insulated roof, particularly in Bay 3, which has a section of exterior wall. This diurnal pattern should be considered when interpreting a `TEMP_HIGH_01` event that occurs at a consistent time of day.

## 6.4 Ventilation and Airflow Requirements

Adequate ventilation for the Utility Pump House as a whole is a facility-level responsibility, but the following pump-specific airflow requirements should be verified as part of any ventilation review:

- A minimum of the clearances specified in Section 2.2 must be maintained free of obstruction on all sides of each unit.
- The motor's own cooling fan and shroud (drawing external air across the motor frame) must have an unobstructed intake — this is a motor-level airflow path independent of, and in addition to, the general room ventilation, and its inspection is covered under `TEMP_HIGH_02` diagnostic review (Section 3.3).
- Where forced room ventilation (exhaust fans) is provided, intake and exhaust points should be positioned so that the warm air rejected by one unit's motor is not drawn directly into an adjacent unit's motor intake — a layout issue that can produce a systematic ambient-driven warm bias on the downwind unit.

## 6.5 Seasonal Considerations

Site ambient conditions vary meaningfully across the year, and the PumpGuard controller's fixed alarm thresholds (85 °C / 100 °C for bearing temperature) do not themselves adjust for season. The following seasonal patterns are relevant to interpreting thermal alarm frequency:

- **Summer / high ambient periods**: expect a modest but real reduction in margin to `TEMP_HIGH_01` and `TEMP_HIGH_02` thresholds across all three units simultaneously. A simultaneous, fleet-wide increase in bearing temperature baseline (rather than an isolated single-unit rise) is the expected signature of an ambient-driven effect and should not, by itself, be treated as a mechanical fault on any individual unit.
- **Winter / low ambient periods**: cold start-up conditions can temporarily increase bearing grease viscosity, producing a brief elevated-friction period during the first minutes of operation (see Section 2.10 start-up procedure) before the unit reaches thermal equilibrium; this is normal and distinct from a sustained `TEMP_HIGH_01` condition.
- **Humidity**: elevated ambient humidity increases the risk of moisture ingress at instrument junction boxes (contributing to `SENSOR_FAIL_13`) and at bearing housing seals (contributing to grease emulsification, see Section 4.2 Step 5), independent of the temperature effects discussed above.

## 6.6 Altitude Derating

The MP-4300 Series motor rating in Section 1.4 assumes installation at or near sea level. Where a unit is installed at elevation above approximately 1,000 m, reduced air density reduces the cooling effectiveness of the motor's self-ventilated cooling fan, and motor thermal margin should be reviewed against the motor manufacturer's altitude derating table. This is not applicable to the current Pump-1/Pump-2/Pump-3 installation as documented in this manual, but should be reviewed before this design is applied at a different site.

## 6.7 VFD Panel Thermal Management

Each unit's VFD is mounted in a dedicated motor control cabinet in the Utility Pump House, separate from the bearing/motor thermal considerations discussed above but subject to its own ambient sensitivity:

- VFD cabinets rely on internal fan-forced ventilation or, where specified, air conditioning to maintain internal temperature within the drive manufacturer's rating.
- A blocked or fouled cabinet air filter reduces internal airflow and is a common contributor to a `VFD_FAULT_12` drive-overtemperature-type fault (Section 3.3) that is entirely independent of the pump's own mechanical or process condition.
- Cabinet air filters should be inspected on the same quarterly interval as the electrical connection torque check (Section 5.5) and cleaned or replaced as needed, particularly given the general debris levels typical of an industrial utility area.

## 6.8 Effect of Ambient Conditions on Alarm Frequency

When reviewing `TEMP_HIGH_01` or `TEMP_HIGH_02` alarm frequency across the three-unit fleet (see Sections 3.3, 4.2), cross-reference against the ambient and seasonal factors in this section before concluding a mechanical root cause is responsible, particularly when:

- The alarm frequency increases across **all three units** at a similar time, rather than an isolated single unit — this pattern points to Section 6.5 seasonal or Section 6.3 installation-level effects rather than a unit-specific mechanical issue.
- The alarm recurs at a **consistent time of day**, which may point to the diurnal solar-loading pattern discussed in Section 6.3 rather than a progressive mechanical degradation, which would not typically show a daily periodicity.
- The alarm is on **Pump-3** specifically and coincides with its standby idle state rather than an active exercise run or auto-start event (Section 5.4) — a standby unit's thermal behavior on start-up can differ from a continuously duty-cycled unit's, independent of its underlying mechanical condition.

Conversely, an alarm isolated to a single unit, with no correlation to time of day or season, and not shared by its sister units under equivalent conditions, should be investigated mechanically per the Section 4.2 diagnostic procedure rather than attributed to ambient causes.

## 6.9 Recommendations for Ambient Monitoring

To support the fleet-wide-versus-isolated distinction described in Section 6.8, it is recommended that a general ambient temperature sensor be maintained in the Utility Pump House (independent of any single unit's instrumentation) and that its reading be retained in the same historian system as the PumpGuard unit data, so that ambient trend and unit bearing/winding temperature trend can be compared directly on a common timeline during any thermal alarm investigation.

## 6.10 Ambient Effects on Seal Flush Performance

Ambient conditions influence seal reliability through a pathway that is distinct from, but related to, the bearing and winding thermal effects discussed above, and is worth calling out separately because it connects Section 6's environmental perspective to the `SEAL_FAIL_03` alarm (Sections 3.3, 4.3) through the seal flush circuit rather than through the bearing housing:

- **Summer / high ambient periods** raise the temperature of the flush water drawn from the discharge tap (Section 2.5) before it ever reaches the seal chamber, reducing the flush circuit's effective cooling capacity at the seal faces precisely during the period when the seal faces are also generating the most frictional heat. Sites experiencing a seasonal increase in `SEAL_FAIL_03` frequency during summer months, with wear patterns consistent with thermal damage (Section 4.3 Step 6), should consider this ambient-driven flush temperature effect as a contributing factor rather than looking only at the seal or flush line hardware itself.
- **Winter / low ambient periods** increase the risk of localized cooling of the flush line in any unheated or poorly insulated run, which can, in an extreme case, affect flush flow consistency; this is a secondary consideration for the Utility Pump House's indoor installation but should be reviewed if any portion of the flush piping run is exposed to outdoor ambient conditions.
- **Humidity-driven condensation** on an indoor flush line running colder than the surrounding air's dew point can be mistaken for an external leak during a visual inspection; technicians should distinguish condensation on the outside of the flush line from an actual `LEAK_DET_17` or `SEAL_FAIL_03` condition before escalating a visual observation to a full alarm investigation.

## 6.11 Worked Example: Applying the Derating Rule of Thumb

To illustrate the rule of thumb given in Section 6.2, consider a unit with a stable bearing temperature baseline of 68 °C established at commissioning (Section 2.11) under a general site ambient of 22 °C. If sustained site ambient rises to 42 °C during a summer period — 20 °C above the 30 °C reference point in Section 6.2's rule of thumb — the expected ambient-driven contribution is approximately 2 × 3–4 °C, or roughly 6–8 °C, giving an expected bearing temperature in the range of 74–76 °C from ambient effects alone, with no change in mechanical condition. A reading in this range, on all three units simultaneously, is consistent with the ambient effect described in Section 6.5 and Section 6.8 and would not, by itself, justify a mechanical investigation. A reading noticeably above this range, or isolated to a single unit rather than shared across Pump-1, Pump-2, and Pump-3, falls outside what ambient effects alone would explain and should proceed to the full Section 4.2 diagnostic procedure.

---

# Section 7: Appendix A — Safety & Compliance

## A.0 How to Use This Appendix

This appendix is organized to be read in two ways. Read sequentially (A.1 through A.10), it functions as a general safety and compliance reference for anyone new to the Pump-1/Pump-2/Pump-3 installation. Read selectively via the cross-reference index in Section A.8, it functions as a fast lookup during an active alarm event — for example, a technician responding to an active `SEAL_FAIL_03` alarm can go directly from Section 3.3 or Section 4.3 to the leak/spill response guidance in Section A.7 without reading the full appendix in order. Both uses are intentional, which is why safety-critical guidance (lockout/tagout in Section A.3, PPE in Section A.4, emergency procedures in Section A.7) is written to stand on its own rather than assuming the reader has already absorbed every preceding subsection.

## A.1 Applicable Standards Framework

The MP-4300 Series and its associated PumpGuard control system are designed with reference to the following general classes of industrial standards. This manual is a synthetic reference document and does not itself constitute a certificate of compliance; site-specific compliance documentation should be maintained separately in the plant's regulatory record.

- General rotating equipment safety practice consistent with ANSI/HI (Hydraulic Institute) pump standards
- Vibration severity classification per ISO 10816-3, as referenced throughout Sections 3 and 4 for `VIB_HIGH_04` and `BEARING_WEAR_16`
- Electrical area classification and equipment protection consistent with IEC 60079-series principles, where the installation area classification requires it
- General machinery safety and guarding principles consistent with ISO 12100
- Lockout/tagout practice consistent with generally accepted hazardous energy control principles (site-specific procedures govern; the outline in Section A.3 is a minimum baseline, not a replacement for the site's own LOTO program)

## A.2 General Safety Precautions

The following hazards are present on Pump-1, Pump-2, and Pump-3 and must be considered before any inspection, maintenance, or troubleshooting activity described elsewhere in this manual:

- **Rotating equipment.** The coupling, shaft, and any exposed portion of the drive train present an entanglement hazard whenever the unit is running or capable of starting. Never remove the coupling guard (Section 2.6) while the unit is running or while an automatic start (including Pump-3's standby auto-start interlock, Section 1.2) is possible.
- **Hot surfaces.** Casing, bearing housing, and motor frame surfaces can exceed safe touch temperatures during normal operation (see the 90 °C continuous fluid rating in Section 1.4, and the 100 °C `TEMP_HIGH_01` Critical threshold in Section 3.3) and remain hot for a period after shutdown. Allow adequate cooling time before direct contact, or use appropriate PPE per Section A.4.
- **Pressurized fluid.** The casing operates up to 16 bar (Section 1.4). Do not open any casing, seal chamber, or flush line connection without first confirming the system is depressurized and isolated.
- **Electrical hazards.** The 400 V motor supply and VFD present electrical shock and arc-flash hazards. All electrical work must be performed only by personnel qualified and authorized for the applicable voltage class, following the site's electrical safety program.
- **Slip/fall hazard from leakage.** Both `SEAL_FAIL_03` (Section 3.3, 4.3) and `LEAK_DET_17` (Section 3.3) conditions can result in fluid accumulation on the floor at the pump base; treat any active leak as a housekeeping hazard requiring containment or barricading in addition to its equipment-fault handling.

## A.3 Lockout/Tagout Procedure (Baseline)

Before any activity requiring physical access to the pump, coupling, bearing housing, seal, or associated piping described in Sections 2, 4, or 5 of this manual, the following minimum hazardous energy control sequence applies. This baseline must be supplemented with the site's own documented LOTO procedure, which takes precedence where more stringent.

1. Notify affected operations personnel of the intended isolation and its expected duration.
2. Stop the unit through normal control means (not via the Emergency Stop, which is reserved for the conditions in Section A.7) and confirm zero speed.
3. Isolate and lock out the electrical supply at the motor control cabinet disconnect, applying a personal lock and tag.
4. Isolate suction and discharge valves and apply a personal lock and tag to each.
5. Relieve and confirm zero pressure in the casing via the casing vent valve (Section 2.9) before any flange or housing is opened.
6. Verify zero energy state directly at the point of work (attempt a start from the local HMI and confirm no response; confirm no residual pressure at the vent) before beginning work — do not rely solely on the lock/tag as verification.
7. On completion of work, remove locks and tags only in reverse order, and only by the person who applied each lock (or per the site's authorized alternate-removal procedure), followed by the restart authorization sequence in Section A.7.

## A.4 Personal Protective Equipment Requirements

| Activity | Minimum PPE |
|---|---|
| General area walk-down (Section 5.2 daily checks) | Standard site PPE (hard hat, safety glasses, hearing protection near running units per the 78 dB(A) rating in Section 1.4) |
| Direct contact with running or recently stopped unit | Add insulated/heat-resistant gloves |
| Seal or bearing housing disassembly (Section 4.3, 5.6) | Add face shield and chemical-resistant gloves appropriate to the process fluid |
| Electrical panel work (Section 2.7, 2.8, A.5) | Arc-flash rated PPE per the site electrical safety program and the panel's calculated incident energy category |
| Leak response (`SEAL_FAIL_03`, `LEAK_DET_17`) | PPE appropriate to the specific process fluid per the site's safety data sheet reference |

## A.5 Hazardous Energy Sources Specific to This Equipment

In addition to the general LOTO sequence in Section A.3, be aware of the following equipment-specific residual or secondary energy sources that are sometimes overlooked:

- **Stored spring energy** in the mechanical seal cartridge (Section 1.3) — the seal cartridge spring remains compressed and can release stored energy when the cartridge is removed; follow the seal manufacturer's cartridge handling procedure during Section 4.3 replacement work.
- **Residual pressure trapped between isolation valves** even after the casing vent (Section 2.9) is opened, if the vent path itself is partially blocked — confirm actual flow at the vent, not merely that the valve is open.
- **VFD DC bus residual voltage** — VFD internal capacitors can retain hazardous voltage for a period after the disconnect is opened; follow the drive manufacturer's specified discharge time before internal VFD panel work, in addition to the external disconnect lockout in Section A.3.
- **Gravity/head pressure from an elevated supply tank** — even with the pump electrically isolated and stopped, an open path from an elevated upstream tank can pressurize the casing; valve isolation (Section A.3, Step 4) addresses this, but should not be skipped on the assumption that electrical isolation alone is sufficient.

## A.6 Guarding and Access

- The coupling guard (Section 2.6) is a fixed safety guard and must never be operated with it removed or displaced, including for brief diagnostic purposes such as visual coupling inspection while running — use the vibration and thermal instrumentation described in Sections 3 and 4 for running diagnostics instead of visual/physical access to the coupling.
- Access to Bay 1, Bay 2, and Bay 3 should respect the clearance envelope in Section 2.2, which serves a dual purpose of maintenance access and safe separation between personnel and adjacent operating units during any single-unit maintenance activity.

## A.7 Emergency Procedures

**Emergency Stop (`ESTOP_ACT_19`, Section 3.3):** Any person observing an immediate hazard — abnormal noise suggesting imminent mechanical failure, a spraying leak, visible smoke, or a person at risk of contact with rotating or energized equipment — should activate the local E-Stop pushbutton without waiting for supervisory approval. Following any E-Stop activation:

1. Do not reset the E-Stop or attempt a restart until the cause has been positively identified, per the guidance already given for `ESTOP_ACT_19` in Section 3.3.
2. Treat the unit as under lockout (Section A.3) for the duration of the investigation, even though the E-Stop itself is a separate protective function from the electrical disconnect lockout.
3. Restart authorization following any Safety-severity event requires sign-off from the site reliability engineer or designated safety authority, not solely the technician who investigated the cause — this is a stricter authorization requirement than applies to routine Warning or Critical alarm clearing elsewhere in this manual.

**Leak / spill response (`SEAL_FAIL_03`, `LEAK_DET_17`):** Contain the leak using site spill-response materials, barricade the wet area to prevent slip/fall exposure, and follow the site's environmental reporting requirements for the specific process fluid, in addition to the equipment-level corrective actions already described in Section 4.3.

## A.8 Cross-Reference Index

The table below consolidates every alarm code introduced in Section 3 with the primary manual locations where it is discussed, to support rapid navigation during an active event.

| Code | Section 3 (Summary) | Section 4 (Full Procedure) | Other References |
|---|---|---|---|
| `TEMP_HIGH_01` | 3.3 | 4.2 | Section 6 (ambient contribution) |
| `TEMP_HIGH_02` | 3.3 | — | Section 6.7 (VFD/motor cooling) |
| `SEAL_FAIL_03` | 3.3 | 4.3 | Section A.7 (leak response), Section 5.6 (planned replacement) |
| `VIB_HIGH_04` | 3.3 | 4.4 | Section 2.6 (alignment), Section 5.5 (spectral baseline) |
| `FLOW_LOW_05` | 3.3 | 4.5 | Section 2.7 (VFD minimum speed floor) |
| `PRESS_LOW_06` | 3.3 | — | Section 5.6 (wear ring inspection) |
| `PRESS_HIGH_07` | 3.3 | — | — |
| `CAV_DET_08` | 3.3 | 4.6 | Section 1.4 (NPSH required) |
| `MOTOR_OVLD_09` | 3.3 | 4.7 | Section 2.7 (VFD configuration) |
| `LUBE_LOW_10` | 3.3 | — | Section 5.7 (lubrication schedule) |
| `COUPL_MISALIGN_11` | 3.3 | — | Section 2.6 (alignment procedure) |
| `VFD_FAULT_12` | 3.3 | — | Section 6.7 (VFD panel thermal) |
| `SENSOR_FAIL_13` | 3.3 | — | Section 4.1 (general diagnostic principle) |
| `POWER_PHASE_14` | 3.3 | 4.8 | Section 2.7 (electrical commissioning) |
| `SUCT_STRAIN_15` | 3.3 | — | Section 2.5 (strainer installation), Section 5.4 (cleaning) |
| `BEARING_WEAR_16` | 3.3 | — | Section 5.6 (bearing housing inspection) |
| `LEAK_DET_17` | 3.3 | — | Section A.7 (leak response) |
| `SPEED_DEV_18` | 3.3 | — | Section 2.7 (VFD setup) |
| `ESTOP_ACT_19` | 3.3 | — | Section A.7 (emergency procedures) |
| `COOLANT_LOW_20` | 3.3 | — | Section 2.5 (flush line installation) |

## A.9 Compliance Statement and Disclaimer

This manual, including all equipment identifiers (Pump-1, Pump-2, Pump-3; tags P-101/P-102/P-103; serial numbers MM-4300-1001/1002/1003), the MP-4300 Series model designation, the PumpGuard controller platform, and all specification values, alarm codes, and procedures contained herein, is a fully synthetic reference document prepared for demonstration, testing, and documentation-tooling purposes. It does not describe a real commercially available product, is not associated with any real manufacturer, and must not be relied upon as an actual equipment manual, safety certification, or regulatory compliance record for any physical installation. Any resemblance to a real product's specifications, alarm nomenclature, or procedures is coincidental.

## A.10 Training and Competency Requirements

Consistent with the graduated authorization already described for restart following a Safety-severity event (Section A.7), the following minimum competency levels apply to personnel performing the activities described elsewhere in this manual. These are stated as a baseline; the site's own training and competency management program takes precedence where more stringent.

| Activity | Minimum Competency |
|---|---|
| Daily/weekly visual checks (Sections 5.2, 5.3) | General site safety orientation; no specialized pump training required |
| Routine lubrication and strainer cleaning (Sections 5.4, 5.5) | Site-authorized maintenance technician, LOTO-qualified per Section A.3 |
| Alarm investigation per Section 4 procedures | Site-authorized maintenance technician with documented familiarity with this manual's alarm codes (Section 3) and the specific procedure being followed |
| Laser alignment (Sections 2.6, 4.2, 4.4) | Technician trained specifically on the site's laser alignment system, in addition to general mechanical competency |
| Mechanical seal replacement (Sections 4.3, 5.6) | Technician trained on cartridge-seal handling, including the stored spring energy hazard in Section A.5 |
| Electrical panel and VFD work (Sections 2.7, 2.8) | Personnel qualified and authorized for the applicable voltage class per the site electrical safety program, with specific VFD/drive training |
| Restart authorization following a Critical auto-trip | Site-authorized maintenance technician who performed or directly verified the corrective action |
| Restart authorization following a Safety-severity event (`ESTOP_ACT_19`) | Site reliability engineer or designated safety authority only, per Section A.7 — this authorization may not be delegated to the investigating technician alone |
| Threshold or configuration changes (Section 3.5) | Site reliability engineer approval required regardless of who performs the technical change |

New personnel should not perform any activity above their demonstrated competency level independently; pairing with an experienced technician for the first occurrence of each activity type is the recommended minimum, in addition to whatever formal certification the site's training program requires.

---

# Glossary of Terms and Abbreviations

| Term | Definition |
|---|---|
| API Plan 11 | A standardized mechanical seal flush arrangement in which flush fluid is piped from the pump discharge, through a flow control orifice, back to the seal chamber — used on the MP-4300 Series per Section 1.3 |
| Back pull-out | A pump construction style in which the bearing housing, seal, and impeller can be withdrawn from the drive end without disturbing the casing or piping |
| Best efficiency point (BEP) | The flow/head combination at which a centrifugal pump operates at its highest hydraulic efficiency; operating far from BEP increases risk of the conditions described under `CAV_DET_08` (Section 4.6) |
| CMMS | Computerized Maintenance Management System — the site's system of record for maintenance history, referenced throughout Section 5 |
| Cavitation | The formation and collapse of vapor bubbles in a pumped fluid due to localized pressure drop below vapor pressure, producing characteristic noise, vibration, and potential surface damage; see `CAV_DET_08` |
| DCS | Distributed Control System — the plant-level control system to which PumpGuard alarms are forwarded per Section 1.6 |
| DE / NDE | Drive End / Non-Drive End — the two bearing locations on the pump shaft, each independently monitored per Section 1.6 |
| Dry running | Pump operation without adequate fluid present in the casing/seal chamber, a primary risk factor for `FLOW_LOW_05` and a precursor to `SEAL_FAIL_03` |
| Duty/lag/standby | The operating role assignment among Pump-1, Pump-2, and Pump-3 described in Section 1.2 |
| Grout (epoxy, non-shrink) | A high-strength fill material used beneath the baseplate (Section 2.4) to permanently transfer equipment load and vibration into the foundation |
| HMI | Human-Machine Interface — the local operator display on each PumpGuard controller |
| Historian | The time-series database within the PumpGuard system that stores instrument readings and alarm events for trend analysis (Sections 4.1, 5.12) |
| IP65 | An ingress protection rating indicating a dust-tight enclosure protected against low-pressure water jets, applicable to local instrument junction boxes per Section 1.4 |
| ISO 10816-3 | The international standard used to classify mechanical vibration severity into zones (A through D) for industrial machinery, referenced throughout `VIB_HIGH_04` discussion |
| LOTO | Lockout/Tagout — the hazardous energy control procedure outlined in Section A.3 |
| Mechanical seal (cartridge type) | A pre-assembled sealing device that prevents process fluid leakage along the rotating shaft, described in Section 1.3 and serviced per Section 4.3 |
| Modbus RTU / TCP | Industrial communication protocols used between the VFD, PumpGuard controller, and plant DCS, referenced in Sections 1.6 and 2.8 |
| NPSH (Net Positive Suction Head) | The suction-side pressure margin available above the fluid's vapor pressure; insufficient NPSH margin is the primary root cause of cavitation, see Section 1.4 and `CAV_DET_08` |
| PTC thermistor | Positive Temperature Coefficient thermistor — a temperature sensing element whose resistance rises sharply past a rated threshold, used for motor winding protection (`TEMP_HIGH_02`) |
| PumpGuard™ | The local controller platform monitoring and protecting each of Pump-1, Pump-2, and Pump-3, described in Section 1.6 |
| Pt100 RTD | A platinum resistance temperature detector with a nominal 100-ohm resistance at 0 °C, used for bearing temperature monitoring (`TEMP_HIGH_01`) |
| Run-in period | The initial monitored operating period following commissioning start-up, described in Section 2.10 |
| Trend-based alarm | An alarm code (`BEARING_WEAR_16`, `LUBE_LOW_10`, `COUPL_MISALIGN_11`) raised from analysis of a value's change over time rather than a single instantaneous threshold crossing |
| VFD | Variable Frequency Drive — the motor speed control device described in Sections 1.3, 2.7, and 2.12 |
| Wear ring | A replaceable close-clearance component that controls internal recirculation within the pump casing; clearance growth from wear reduces pump performance, see `PRESS_LOW_06` |

---

# Document Revision History

| Revision | Summary of Changes |
|---|---|
| A | Initial issue covering Pump-1 only, prior to Pump-2 and Pump-3 installation |
| B | Expanded to cover all three units following Pump-2 and Pump-3 commissioning; added full Alarm Code Matrix (Section 3) |
| C (current) | Added detailed troubleshooting procedures (Section 4), Thermal Management section (Section 6), and expanded Safety & Compliance appendix (Section 7) with full cross-reference index |

*End of MechMind MP-4300 Series Technical Reference & Operations Manual — Manual Number MM-TM-4300-REV-C.*
