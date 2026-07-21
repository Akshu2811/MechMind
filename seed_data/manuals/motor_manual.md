# MechMind MX-2200 Series Industrial Induction Motor

## Technical Reference & Operations Manual

**Covering Unit Tags: Motor-1 (M-201), Motor-2 (M-202)**

| Document Control | |
|---|---|
| Manual Number | MM-TM-2200-REV-C |
| Applicable Model Line | MX-2200 Series, TEFC Squirrel-Cage Induction Motor |
| Applicable Units | Motor-1 (Tag M-201, S/N MM-2200-2001), Motor-2 (Tag M-202, S/N MM-2200-2002) |
| Controller Platform | MotorGuard™ Local Controller, firmware 2.4.x |
| Revision | C |
| Issued By | MechMind Industrial Systems — Technical Publications |
| Status | Fully synthetic reference document for demonstration and testing purposes. No affiliation with any real manufacturer. |

> **Note on scope:** This manual documents a two-motor installation (Motor-1, Motor-2) of identical MX-2200 Series construction, each driving its own dedicated centrifugal process air blower on a shared process air header. Except where a procedure or specification explicitly calls out one unit by tag, all content applies equally to Motor-1 and Motor-2.

---

## Table of Contents

1. Overview & Technical Specifications
2. Installation & Commissioning Procedures
3. Full Alarm Code Matrix
4. Detailed Troubleshooting Procedures
5. Routine Maintenance Schedule
6. Mechanical Alignment & Balancing
7. Appendix A — Safety & Compliance
8. Glossary of Terms and Abbreviations
9. Document Revision History

---

# Section 1: Overview & Technical Specifications

## 1.1 Purpose and Scope

This manual provides the technical reference, installation, commissioning, alarm response, troubleshooting, maintenance, and safety documentation for the MechMind MX-2200 Series TEFC squirrel-cage induction motor, as installed in the two-unit configuration designated **Motor-1** and **Motor-2**. Both units are of identical mechanical and electrical construction and share a common instrumentation and control architecture built around the MotorGuard™ Local Controller. Where information in this manual differs between units — for example, differing install dates or a unit-specific finding from a prior inspection — this is called out explicitly. Otherwise, all specifications, procedures, and alarm behaviors apply uniformly across the two-motor set.

This document is intended for use by commissioning engineers, electrical and mechanical maintenance technicians, reliability engineers, and control system integrators responsible for the operation and upkeep of Motor-1 and Motor-2. It is also intended to serve as a structured knowledge source for automated maintenance-assistance tooling, including alarm-code lookup, troubleshooting guidance retrieval, and maintenance scheduling support.

## 1.2 Equipment Identification

Motor-1 and Motor-2 are each direct-coupled to a dedicated centrifugal process air blower, discharging into a common Process Air Header that supplies pneumatic conveying and drying equipment across the site. Unlike a duty/standby arrangement, both units normally run in parallel to meet combined process air demand; either unit can carry a reduced load alone for a limited period if the other is out of service, but neither is configured as an idle installed spare.

| Unit Tag | Equipment Tag | Serial Number | Driven Equipment | Install Location |
|---|---|---|---|---|
| Motor-1 | M-201 | MM-2200-2001 | Blower-1 (Tag BLR-201) | Process Air Building, Bay A |
| Motor-2 | M-202 | MM-2200-2002 | Blower-2 (Tag BLR-202) | Process Air Building, Bay B |

Because both units normally run continuously and in parallel rather than one standing idle in standby, the cross-unit comparison techniques used throughout this manual (Section 6.8-equivalent discussion in Section 6, and the condition-monitoring cadence in Section 5) rely on comparing two continuously-loaded machines against one another, rather than comparing a duty unit against an intermittently-exercised standby — a simpler comparison basis than a duty/standby fleet, but one that still depends on both units being maintained and instrumented consistently.

## 1.3 Motor Design Description

The MX-2200 Series is a totally enclosed fan-cooled (TEFC), squirrel-cage induction motor intended for continuous-duty, VFD-driven service in industrial process applications. Key construction features common to Motor-1 and Motor-2:

- **Frame**: IEC 315M cast-iron frame, foot-mounted in the IEC B3 configuration.
- **Stator winding**: Class F insulation system, with temperature rise limited by design to Class B limits, giving a thermal margin used throughout Section 3 and Section 4 alarm threshold design.
- **Rotor**: Die-cast aluminum squirrel-cage rotor, dynamically balanced to ISO 21940 Grade G2.5 — a tighter balance grade than typical driven-equipment components, reflecting the rotor's role as the balance reference for the coupled train (see Section 6.3).
- **Bearings**: Drive-end (DE) regreasable cylindrical roller bearing to carry combined radial and belt/coupling loads; non-drive-end (NDE) regreasable deep-groove ball bearing.
- **Cooling**: Integral shaft-mounted TEFC cooling fan, supplemented on both units by an independently-powered auxiliary cooling fan (Section 1.4), since sustained VFD operation at reduced speed reduces the airflow produced by the shaft-mounted fan alone.
- **Coupling**: Spacer-type flexible coupling to the driven blower, consistent with the coupling philosophy used elsewhere in the MechMind rotating equipment fleet, permitting bearing and coupling service without disturbing the blower.
- **Enclosure rating**: IP55, suitable for the indoor Process Air Building environment with incidental dust and moisture exposure.
- **Terminal box**: Side-mounted, IP55, sized for the MX-2200 Series full-load current and cable entry requirements.
- **Paint system**: Two-coat epoxy, RAL 5015 (sky blue) finish coat, consistent with the MechMind fleet-wide equipment color standard.

## 1.4 Technical Specifications

| Parameter | Value |
|---|---|
| Motor type | TEFC squirrel-cage induction motor, IE3 premium efficiency |
| Frame size | IEC 315M |
| Rated power | 250 kW (335 hp) |
| Rated voltage | 400 V, 3-phase |
| Rated frequency | 60 Hz |
| Rated speed | 1,780 rpm (nominal, 4-pole) |
| Full-load current | 410 A at 400 V |
| Locked-rotor current | Approximately 680% of full-load current (see Section 1.9) |
| Service factor | 1.15 |
| Insulation class / temperature rise | Class F insulation, temperature rise limited to Class B |
| Enclosure rating | IP55 |
| Drive | Dedicated VFD, 15–60 Hz operating range |
| Bearings | DE: regreasable cylindrical roller; NDE: regreasable deep-groove ball |
| Auxiliary cooling fan | Independently powered, 400 V single-phase, thermostatically and VFD-speed interlocked (Section 3.3, `COOLING_FAN_20`) |
| Balance grade | ISO 21940 Grade G2.5 |
| Vibration classification | ISO 10816-3 |
| Ambient design range | −20 °C to 45 °C |
| Altitude (no derating) | Up to 1,000 m |
| Sound pressure level | 82 dB(A) at 1 m, free field |
| Weight (motor only) | 1,400 kg |
| Paint system | 2-coat epoxy, RAL 5015 |

## 1.5 Nameplate Data and Identification

Each unit carries a stainless steel nameplate riveted to the frame, stamped with the equipment tag, serial number, rated electrical data, insulation class, and year of manufacture. Nameplate data must match the values recorded in the commissioning record (Section 2.11) and the asset record in the plant CMMS. As with all MechMind fleet equipment, a mismatch between nameplate serial number and CMMS record should be treated as a documentation discrepancy requiring investigation before further work is performed on the unit.

## 1.6 Control System Overview

Motor-1 and Motor-2 are each monitored and protected by an individual MotorGuard™ Local Controller, mounted in the associated motor control cabinet. Each MotorGuard controller aggregates:

- Two Pt100 RTD bearing temperature inputs (drive end and non-drive end),
- Three embedded stator winding RTD inputs (one per phase),
- Two MEMS accelerometer-based vibration sensors (drive end and non-drive end housings), ISO 10816-3 zone classification,
- An insulation/ground-fault monitoring relay on the stator winding circuit,
- Auxiliary cooling fan run-status and current sensing,
- VFD status, output current, and speed feedback via Modbus RTU,
- A starts-per-hour counter derived from VFD run commands,
- Local E-Stop and safety interlock status.

The MotorGuard controller evaluates these inputs continuously against configured thresholds and raises one of the twenty standardized alarm codes described in full in **Section 3** when a threshold is exceeded or a fault condition is detected. Alarms are surfaced on the local HMI, forwarded to the plant DCS over Modbus TCP, and logged with timestamp, unit tag, and triggering value in the MotorGuard historian, in the same architectural pattern used by the PumpGuard platform documented for the site's process pump fleet. Section 4 of this manual expands on the diagnostic and corrective procedures for the most operationally significant of these alarm codes.

## 1.7 Electrical Supply and Service Conditions

Motor-1 and Motor-2 are each supplied from a dedicated VFD fed from the plant's 400 V, 3-phase, 60 Hz distribution switchgear. The service basis assumed by the specifications in Section 1.4 is as follows:

| Parameter | Design Basis |
|---|---|
| Supply voltage tolerance | ±10% of nominal 400 V |
| Supply frequency tolerance | ±2% of nominal 60 Hz |
| Voltage imbalance limit | 1% maximum, phase-to-phase, measured at the motor terminals |
| Duty cycle | Continuous (S1), VFD-modulated speed 15–60 Hz |
| Starts per hour | 2 evenly spaced starts per hour maximum (see Section 1.9 and `STARTS_EXCEED_14`) |
| Ambient humidity | Up to 95% non-condensing; condensing conditions addressed under `MOISTURE_ING_17` (Section 3.3) |

A supply condition outside this design basis — for example, a persistent voltage imbalance from an upstream distribution issue, or a demand pattern requiring more frequent starts than the design basis allows — should be reviewed against these parameters before being accepted as normal operation, since several alarm codes in Section 3 (`PH_LOSS_04`, `UNDERVOLT_13`, `STARTS_EXCEED_14`) are directly sensitive to exactly these supply characteristics.

## 1.8 Duty Arrangement and Unit-to-Unit Comparison

Because Motor-1 and Motor-2 are of identical construction and normally run in parallel under similar load, their MotorGuard trend data is directly comparable in the same way used throughout the MechMind fleet documentation to distinguish a genuine unit-specific fault from a fleet-wide ambient or supply-side effect (see Section 6.9 for the motor-specific application of this principle). This comparability depends on both units being maintained on the same schedule (Section 5) and both being run under a broadly similar loading pattern; a site that runs Motor-1 consistently near full load while Motor-2 is throttled back for extended periods should expect some baseline divergence between the two units that reflects load rather than mechanical condition.

## 1.9 Torque-Speed and Starting Current Characteristics

The following data, expressed as a percentage of rated torque and rated full-load current, characterizes motor behavior through a direct-on-line-equivalent start (used as the reference condition even though Motor-1 and Motor-2 are normally started via VFD ramp per Section 2.7) and is the basis for the `LOCKED_ROTOR_11` and `STARTS_EXCEED_14` diagnostic procedures in Section 4:

| Condition | Speed (% of Synchronous) | Torque (% of Rated) | Current (% of Full-Load) |
|---|---|---|---|
| Locked rotor (0 speed) | 0% | 140% | 680% |
| Pull-up torque (minimum during acceleration) | ~15–20% | 120% | 620% |
| Breakdown torque (maximum during acceleration) | ~80% | 230% | 350% |
| Rated full-load point | 100% | 100% | 100% |

Because Motor-1 and Motor-2 are VFD-started with a controlled acceleration ramp (Section 2.7, Section 2.12) rather than started direct-on-line, actual starting current is normally held well below the direct-on-line locked-rotor figure shown above; this table is retained as the underlying machine characteristic that the VFD ramp is designed to manage, and is the reference used when a `VFD_FAULT_09`-adjacent event during starting is being investigated (Section 4) to judge whether the VFD successfully limited current during the event or whether the motor was exposed to something closer to the direct-on-line values shown here.

## 1.10 Relationship to the MechMind Rotating Equipment Fleet's Instrumentation Philosophy

The MotorGuard controller platform documented in this manual follows the same general architecture as the PumpGuard platform used elsewhere in the site's rotating equipment fleet (see the separate MP-4300 Series pump manual): both use per-unit local controllers aggregating temperature, vibration, and electrical instrumentation into a standardized set of severity-classified alarm codes, both forward alarms to the plant DCS over Modbus TCP, and both apply the same ISO 10816-3 vibration zone classification. This shared architecture is a deliberate site-level standardization decision, not a coincidence, and it has a practical consequence for personnel working across both equipment types: a technician trained on alarm acknowledgement, reset, and escalation procedure for one platform (Section 3.4 in this manual) can apply the same procedural logic to the other with only the specific alarm codes and thresholds differing between them.

The two platforms do differ in instrumentation emphasis in ways that reflect the different failure modes of their respective machines: the pump fleet's PumpGuard instrumentation places relatively more emphasis on seal chamber and flush-circuit monitoring (reflecting the mechanical seal as a primary pump-specific wear item), while the MotorGuard platform documented here places relatively more emphasis on winding insulation monitoring and starts-per-hour supervision (reflecting stator winding condition and starting duty as primary motor-specific concerns). A reliability engineer reviewing alarm history across the combined fleet should keep this difference in emphasis in mind rather than expecting the two alarm code sets to map one-to-one onto each other.

---

# Section 2: Installation & Commissioning Procedures

## 2.1 Pre-Installation Inspection

Before Motor-1 or Motor-2 is unpacked at its final installation location, perform the following inspection and record results in the commissioning checklist:

1. Verify the shipping crate is undamaged and any tilt/shock indicators have not been triggered.
2. Confirm nameplate data (Section 1.5) matches the purchase order and the intended install location (Bay A or Bay B).
3. Measure winding insulation resistance to ground with a megohmmeter before the motor is uncrated further; record the reading against the minimum acceptable value specified in Section 2.9. A motor that has been in long-term storage or exposed to high humidity during transit should always be checked at this stage before any electrical connection is attempted.
4. Rotate the shaft by hand at the coupling end. It should turn freely with no binding, grinding, or unusual resistance.
5. Inspect the terminal box for moisture, and confirm any shipping desiccant packs are present and not saturated.
6. Confirm bearing housing grease fittings are present and undamaged, and that shipping preservative grease has not been mistaken for a completed lubrication fill.

## 2.2 Site and Foundation Requirements

Each motor bay (Bay A, Bay B) in the Process Air Building is designed with an independent reinforced concrete foundation sized at a minimum of three times the combined motor-blower-baseplate weight, per standard practice for vibration damping of rotating machinery in this power class. Foundation top surface must be level to within 0.5 mm per meter prior to baseplate placement.

Minimum clearances around each installed unit:

| Direction | Minimum Clearance |
|---|---|
| Drive end (coupling, for future pull-apart) | 1.2 m |
| Non-drive end (terminal box access, auxiliary cooling fan) | 1.0 m |
| Sides | 0.6 m |
| Overhead (for lifting equipment access) | 2.2 m |

These clearances are required not only for maintenance access but also for the ambient airflow around the motor frame and auxiliary cooling fan discussed further in Section 3.3 (`COOLING_FAN_20`) and Section 6.

## 2.3 Rigging and Lifting

The motor (1,400 kg) must be lifted using the two lifting eyebolts fitted to the top of the frame, rated for the motor weight with an adequate safety margin. Do not lift the motor using the shaft, fan cowl, or terminal box as a lift point.

1. Use a rated 2-leg chain sling or lifting beam sized for the motor weight plus a minimum 25% safety margin.
2. Confirm no personnel are positioned beneath the suspended load at any point during the lift.
3. Lower the motor onto pre-placed leveling shims or jack screws at the foundation location, aligned to the coupling half already mounted on the driven blower where the blower has been installed first.

## 2.4 Baseplate Installation and Alignment Prefit

1. Position the motor on leveling shims and rough-level using a precision machinist's level placed on the motor's machined mounting feet.
2. Shim as required until level is within 0.1 mm per meter in both axes.
3. Confirm foundation bolt sleeves are clear of debris, then install foundation bolts finger-tight only at this stage.
4. Perform a rough (pre-grout or pre-final-torque) alignment check per Section 2.6 to confirm the motor's final position will not require excessive shimming once precision alignment begins — this rough check avoids discovering a gross positioning error only after the foundation work is otherwise complete.
5. Where the installation uses a grouted baseplate common to the motor and driven blower, follow the same non-shrink epoxy grout procedure and cure time used across the MechMind rotating equipment fleet before proceeding to final alignment and bolt torque.

## 2.5 Electrical Connections

1. Confirm motor nameplate voltage, frequency, and rotation match the supply and the VFD configuration before energizing.
2. Terminate power cables in the terminal box per the torque values in Section 5.8, and confirm cable lugs are sized correctly for the full-load current in Section 1.4.
3. Confirm the stator winding RTD and insulation monitoring circuits are landed correctly at the MotorGuard controller terminal strip, distinguishing the three winding RTD phases from the two bearing RTDs by the labeling scheme on the motor's junction box wiring diagram — a swapped winding/bearing RTD connection is a known source of confusing `WIND_TEMP_01` versus `BRG_TEMP_02` alarm behavior if made during commissioning and not caught until a later troubleshooting investigation.
4. Confirm the auxiliary cooling fan's independent single-phase supply is connected and verified separately from the main motor supply, since a fault on the main motor circuit should not also disable the auxiliary cooling fan when the motor is coasting to a stop.
5. Perform a phase rotation check with the coupling disconnected (motor solo run) to confirm rotation matches the required direction before the coupling is reconnected to the blower.

## 2.5a Driven Equipment Connections (Ductwork and Coupling Interface)

Because Motor-1 and Motor-2 each drive a dedicated centrifugal process air blower rather than a directly plumbed device, the ductwork connections at the blower — while outside this manual's scope for the blower itself — have a direct bearing on motor alignment and vibration if not properly supported:

1. Confirm that inlet and outlet ductwork at each blower is independently supported so that no ductwork weight or thermal expansion load is transmitted into the blower casing, since a load transmitted through the blower casing can shift the blower's position relative to the motor and produce an alignment condition that was correct at initial commissioning but has since drifted.
2. Confirm flexible duct connectors (where fitted) are installed per the blower manufacturer's instructions and are not over-compressed or under tension, since either condition can introduce a cyclic load at the duct connection that shows up as a vibration component at the motor bearings even though its origin is entirely on the ductwork side of the installation.
3. Re-verify motor-to-blower alignment (Section 2.6) after ductwork connections are completed, using the same logic applied to piping connections elsewhere in the MechMind rotating equipment fleet: an alignment check performed before final ductwork connection does not account for any strain the ductwork subsequently introduces.

## 2.6 Alignment Procedure

Final shaft alignment between the motor and driven blower must be performed after foundation bolt torque (and grout cure, where applicable), and again verified after any piping, ductwork, or electrical cable routing changes that could introduce strain near the machine. The full alignment methodology, target tolerances, and balance-grade rationale are given in Section 6 (Mechanical Alignment & Balancing); the summary steps below are provided here for commissioning sequencing purposes.

1. Remove the coupling guard and coupling spacer.
2. Mount a laser alignment system across the coupling hubs and measure angular and parallel offset in both vertical and horizontal planes.
3. Correct alignment using shims under the motor feet only, in accordance with Section 6.2 tolerances.
4. Re-torque motor hold-down bolts to the value in Section 5.8 after final shim adjustment and re-verify alignment did not shift during torqueing.
5. Reinstall the coupling spacer and guard, confirming the guard does not contact the rotating coupling through a full manual rotation.

## 2.7 VFD Setup and Commissioning Parameters

1. Confirm the VFD is programmed with the correct motor nameplate parameters (voltage, current, frequency, pole count, insulation class) before any run command is issued.
2. Configure the acceleration ramp so that the motor reaches rated speed over no less than 8 seconds, limiting starting current well below the direct-on-line locked-rotor value in Section 1.9 and reducing mechanical shock to the coupling.
3. Configure the minimum operating speed floor at 15 Hz; sustained operation below this floor is associated with reduced auxiliary-fan-assisted cooling effectiveness margin (Section 3.3, `COOLING_FAN_20`) and is not recommended as a continuous operating point.
4. Configure the starts-per-hour supervision function in the MotorGuard controller to the design limit in Section 1.7 (2 starts per hour), which raises `STARTS_EXCEED_14` if exceeded.
5. Confirm the VFD carrier frequency and output filtering are configured per the motor manufacturer's recommendation for the installed cable length, to minimize bearing current damage from PWM switching transients — a known long-term contributor to `BRG_WEAR_07` on VFD-driven motors if left unaddressed.

The full commissioning-time VFD parameter record, including the specific values recorded for Motor-1 and Motor-2, is documented in Section 2.12.

## 2.8 Instrumentation Wiring and MotorGuard Controller Commissioning

Each MotorGuard controller must be commissioned individually per unit tag before that unit is placed in service:

1. Confirm the controller is configured with the correct unit tag (Motor-1 / Motor-2) — a mis-tagged controller will log alarms under the wrong unit identity in the historian and DCS, complicating later maintenance record reconciliation (Section 5.10).
2. Load the standard MX-2200 alarm threshold configuration set (see Section 3 for the full list of codes and default thresholds).
3. Verify each of the following instrument loops with a simulated or physical test signal before leaving the site: bearing RTDs (DE/NDE), winding RTDs (3 phases), vibration sensors (DE/NDE), insulation/ground-fault relay, auxiliary cooling fan status and current sensing, starts-per-hour counter.
4. Confirm the local E-Stop pushbutton correctly triggers `ESTOP_ACT_18` and removes the run permissive at the VFD.
5. Confirm Modbus TCP communication to the plant DCS is established and that all 20 alarm codes map correctly to their assigned DCS alarm points.

## 2.9 Pre-Start Checks

Before the first start of any unit, confirm:

- Winding insulation resistance to ground is above the minimum acceptable value (typically 100 megohms at 500 V DC test voltage for a new or recently-serviced winding at ambient temperature, corrected per the insulation resistance temperature correction table used by the site's electrical test procedure) — a reading below this minimum should be investigated per `INSUL_FAIL_06` (Section 4) before the unit is started, not simply noted and started anyway.
- Bearing housings are filled to the correct grease level per Section 5.7.
- Auxiliary cooling fan runs and produces confirmed airflow when commanded independently of the main motor.
- Coupling guard is installed and secure.
- All temporary shipping restraints have been removed.

## 2.10 Initial Start-Up Procedure

Motor-1 and Motor-2 are commissioned sequentially so that any systemic issue (electrical supply, control logic, ductwork) is identified and resolved before the second unit is exposed to it.

1. Start the unit at minimum VFD speed (15 Hz) and confirm smooth rotation, no abnormal noise, and stable current draw for a minimum of 2 minutes.
2. Gradually ramp speed toward the rated operating point (nominally 60 Hz / 1,780 rpm) over no less than 5 minutes, monitoring bearing temperature, winding temperature, vibration, and motor current continuously.
3. Hold the unit at the process duty point for a minimum 30-minute run-in period, logging bearing temperature, winding temperature, vibration, and motor current at 5-minute intervals.
4. Confirm no MotorGuard alarms are active at the end of the run-in period.
5. Repeat for the second unit.

## 2.11 Performance Verification and Commissioning Sign-off

At the conclusion of run-in for each unit, record the following in the commissioning record and compare against the rated specifications in Section 1.4:

- Bearing temperatures, DE and NDE (must be stable and below the `BRG_TEMP_02` Warning threshold defined in Section 3)
- Winding temperatures, all three phases (must be stable and below the `WIND_TEMP_01` Warning threshold)
- Vibration levels, DE and NDE (must be within ISO 10816-3 Zone A/B for a newly commissioned machine, and consistent with the balance-grade expectations in Section 6.3)
- Motor current at duty point (must be below nameplate full-load current of 410 A)
- Winding insulation resistance, confirmed against the Section 2.9 pre-start value with no significant degradation during run-in
- Auxiliary cooling fan current draw, confirmed against its nameplate rating

Commissioning is not considered complete, and the unit should not be released to routine continuous duty, until all values above are recorded within acceptance bands and signed off by both the commissioning engineer and the site reliability engineer. Retain the signed commissioning record permanently as the baseline reference for all future vibration and temperature trending.

## 2.12 Key VFD Parameters to Verify at Commissioning

In addition to the motor nameplate parameters described in Section 2.7, the following VFD parameters should be explicitly confirmed and recorded during commissioning of each unit:

| Parameter | Typical Setting | Relevance |
|---|---|---|
| Minimum output frequency | 15 Hz | Below this floor, auxiliary-fan-assisted cooling margin is reduced (Section 3.3, `COOLING_FAN_20`) |
| Maximum output frequency | 60 Hz | Matches rated speed; increasing beyond nameplate requires an engineering review of mechanical and thermal loading |
| Acceleration ramp time | 8–12 seconds to rated speed | Limits starting current and mechanical shock, per Section 1.9 and Section 2.7 |
| Deceleration ramp time | 10–15 seconds | Reduces coupling shock load on stop |
| Current limit | Motor nameplate full-load current (410 A) plus drive-specific service factor | Misconfiguration here is a documented root cause of nuisance `OVLD_CUR_03` trips (Section 4) |
| Carrier (switching) frequency | Per motor manufacturer recommendation for the installed cable length | Excessively high carrier frequency increases motor bearing current risk, contributing to `BRG_WEAR_07` |
| Starts-per-hour supervision | 2 starts/hour maximum | Raises `STARTS_EXCEED_14` if exceeded, per Section 1.7 |
| Modbus communication timeout | Per MotorGuard controller default | A timeout set too short can produce nuisance `VFD_FAULT_09` events during normal plant network congestion |

Recording these values in the commissioning file gives future troubleshooting activity (Section 4) a documented baseline to compare against when a parameter is suspected to have drifted or been inadvertently changed during later service work.

## 2.13 Common Commissioning Pitfalls and Their Downstream Alarm Consequences

- **Skipping the pre-uncrating insulation resistance check (Section 2.1).** A motor that absorbed moisture during storage or transit but is energized without this check risks an early `INSUL_FAIL_06` event, or in a severe case, actual winding damage on first start — a check that takes only a few minutes but that is easy to skip under schedule pressure.
- **Treating alignment as a one-time task rather than a verify-after-final-connections task (Section 2.6).** Cable routing and ductwork connections completed after the initial alignment check are a common source of alignment that was correct before final connections but out of tolerance afterward, presenting later as `VIB_HIGH_05` or `MISALIGN_15`.
- **Swapping winding and bearing RTD wiring (Section 2.5 Step 3).** This is the single most common instrumentation commissioning error on the MX-2200 Series and produces confusing, internally-inconsistent alarm behavior (for example, a `WIND_TEMP_01` alarm that tracks ambient rather than load) that can consume significant troubleshooting time before the wiring error itself is identified as the root cause.
- **Mis-tagging the MotorGuard controller (Section 2.8).** As with the pump fleet's PumpGuard controllers, a controller commissioned under the wrong unit tag silently corrupts the historian record for both units involved, and is often not discovered until a maintenance history review under Section 5.10 fails to reconcile with observed physical work.
- **Omitting the auxiliary cooling fan verification (Section 2.9).** Because the auxiliary fan's contribution to cooling only becomes significant at reduced VFD speed, a fan that is not actually functional can go unnoticed during a commissioning run-in performed near rated speed, only to present later as an unexplained `COOLING_FAN_20` or `WIND_TEMP_01` event once the unit is operated at lower speed under real process conditions.

## 2.14 Documentation Handover Package

On completion of commissioning for each unit, the following documentation must be assembled into a permanent handover package and filed both in the site CMMS and in the physical or electronic equipment file for that unit tag, before the unit is released to the maintenance organization for routine operation:

| Document | Source | Purpose |
|---|---|---|
| Signed commissioning record | Section 2.11 | Performance and condition baseline for all future comparisons |
| VFD parameter record | Section 2.12 | Baseline for detecting later configuration drift |
| Alignment record (cold, and hot if performed) | Section 2.6, Section 6.2 | Baseline for future alignment verification (Section 5.5) |
| Instrument loop verification checklist | Section 2.8 | Confirms each protective input was functional at handover |
| Pre-installation and pre-start insulation resistance readings | Sections 2.1, 2.9 | Baseline for future insulation resistance trending under `INSUL_FAIL_06` |
| Nameplate and CMMS asset record cross-check | Section 1.5 | Confirms no documentation discrepancy exists at the point of handover, when it is easiest to correct |

A unit should not be released to continuous duty until this package is complete. An incomplete handover package is not merely a paperwork gap: several of the diagnostic procedures in Section 4 (notably `BRG_TEMP_02` in Section 4.3, `VIB_HIGH_05` in Section 4.6, and `INSUL_FAIL_06` in Section 4.7) depend on comparing a current reading against the specific unit's own commissioning baseline, and a missing or incomplete baseline materially weakens the diagnostic value of every future alarm investigation on that unit for the remainder of its service life.

---

# Section 3: Full Alarm Code Matrix

## 3.1 How to Use This Section

Every alarm raised by the MotorGuard controller on Motor-1 or Motor-2 is identified by one of the twenty standardized codes below. Each code is fixed across both units — the same code always means the same condition, regardless of which unit tag raised it. The summary table gives a quick-reference view; the subsections that follow give the full detail (likely causes and recommended immediate steps) for each code. Seven of these codes — `WIND_TEMP_01`, `BRG_TEMP_02`, `OVLD_CUR_03`, `PH_LOSS_04`, `VIB_HIGH_05`, `INSUL_FAIL_06`, and `LOCKED_ROTOR_11` — have full step-by-step diagnostic procedures in Section 4; this section gives the first-response summary for all twenty.

Severity levels used throughout this manual:

- **Warning** — degraded condition, unit remains in service, investigate at next opportunity.
- **Critical** — unit performance or equipment integrity at risk, investigate promptly; some Critical codes are configured to auto-trip the unit.
- **Safety** — condition involves a safety interlock or protective device; unit is stopped and will not restart until the interlock is manually cleared.

## 3.2 Summary Table

| Code | Description | Severity | Auto-Trip? |
|---|---|---|---|
| `WIND_TEMP_01` | Stator Winding Temperature High (any phase) | Warning at Class B limit / Critical at Class F limit | Yes, at Critical threshold |
| `BRG_TEMP_02` | Bearing Temperature High (DE or NDE) | Warning at 85 °C / Critical at 100 °C | Yes, at Critical threshold |
| `OVLD_CUR_03` | Overload / Overcurrent | Critical | Yes |
| `PH_LOSS_04` | Phase Loss / Voltage Imbalance | Critical | Yes |
| `VIB_HIGH_05` | Excessive Vibration (DE or NDE) | Warning at Zone C / Critical at Zone D (ISO 10816-3) | Yes, at Critical threshold |
| `INSUL_FAIL_06` | Insulation Resistance Low / Ground Fault | Critical | Yes, on confirmed ground fault |
| `BRG_WEAR_07` | Bearing Wear / Degradation Trend | Warning | No |
| `LUBE_LOW_08` | Bearing Lubricant Level/Condition Low | Warning | No |
| `VFD_FAULT_09` | VFD Communication or Drive Fault | Critical | Yes |
| `SENSOR_FAIL_10` | Instrument/Sensor Signal Failure | Warning | No |
| `LOCKED_ROTOR_11` | Locked Rotor / Failure to Start | Critical | Yes (immediate) |
| `OVERSPEED_12` | Overspeed Detected | Critical | Yes |
| `UNDERVOLT_13` | Undervoltage | Warning, escalates to Critical if sustained | Yes, if sustained |
| `STARTS_EXCEED_14` | Excessive Starts Per Hour | Warning | No (start inhibited, not a running trip) |
| `MISALIGN_15` | Coupling Misalignment Detected (trend) | Warning | No |
| `RESONANCE_16` | Structural Resonance Detected | Warning | No |
| `MOISTURE_ING_17` | Moisture Ingress / Condensation Detected | Warning | No |
| `ESTOP_ACT_18` | Emergency Stop Activated | Safety | Yes (immediate) |
| `ENCODER_FAULT_19` | Speed Feedback / Encoder Fault | Warning | No |
| `COOLING_FAN_20` | Auxiliary Cooling Fan Airflow Loss | Warning, escalates to Critical if sustained at low speed | Yes, if sustained |

## 3.3 Detailed Alarm Descriptions

### `WIND_TEMP_01` — Stator Winding Temperature High

**Severity:** Warning at the Class B temperature rise limit; Critical (auto-trip) at the Class F insulation system's rated limit, on any of the three embedded winding RTDs.

**Likely causes:**
- Sustained motor overload (see `OVLD_CUR_03`)
- Auxiliary cooling fan fault or reduced airflow at low VFD speed (see `COOLING_FAN_20`)
- Elevated ambient temperature at the motor location (see Section 6.9-equivalent ambient discussion)
- Voltage imbalance (see `PH_LOSS_04`)
- A swapped winding/bearing RTD wiring error from commissioning (see Section 2.13)

**Recommended immediate steps:**
1. Confirm the reading against the other two winding phases before assuming a genuine single-phase heating condition.
2. Check auxiliary cooling fan run status and current draw.
3. Full diagnostic procedure: see Section 4.2.

### `BRG_TEMP_02` — Bearing Temperature High

**Severity:** Warning at 85 °C sustained for 2 minutes; Critical (auto-trip) at 100 °C sustained for 30 seconds, either bearing (DE or NDE).

**Likely causes:**
- Bearing lubrication degraded, low, or contaminated
- Bearing wear or incipient failure (see `BRG_WEAR_07`)
- Shaft misalignment (see `MISALIGN_15`) inducing abnormal bearing loads
- Elevated ambient temperature around the bearing housing
- RTD sensor fault giving a false high reading (cross-check against `SENSOR_FAIL_10` history)

**Recommended immediate steps:**
1. Confirm the reading against the second bearing RTD and, if accessible, a handheld infrared reading before assuming the sensor is correct.
2. Check bearing housing grease level and condition per Section 5.7.
3. Full diagnostic procedure: see Section 4.3.

### `OVLD_CUR_03` — Overload / Overcurrent

**Severity:** Critical (auto-trip).

**Likely causes:**
- Mechanical binding in the motor or driven blower
- Voltage imbalance across phases (see `PH_LOSS_04`)
- Process air demand or blower loading higher than the design basis
- VFD parameter misconfiguration (incorrect current limit or motor nameplate data)

**Recommended immediate steps:**
1. Do not attempt an immediate restart after an overload trip without first checking for mechanical binding by hand-rotating the shaft (with power isolated).
2. Full diagnostic procedure: see Section 4.4.

### `PH_LOSS_04` — Phase Loss / Voltage Imbalance

**Severity:** Critical (auto-trip).

**Likely causes:**
- Upstream breaker or fuse failure on one phase
- Loose or corroded terminal connection at the motor or VFD input
- Utility supply fault or imbalance upstream of the plant switchgear

**Recommended immediate steps:**
1. Do not attempt to restart the unit until phase voltages have been confirmed balanced and within tolerance at the motor terminals.
2. Full diagnostic procedure: see Section 4.5.

### `VIB_HIGH_05` — Excessive Vibration

**Severity:** Warning at ISO 10816-3 Zone C; Critical (auto-trip) at Zone D, either bearing housing.

**Likely causes:**
- Shaft misalignment (see `MISALIGN_15`)
- Rotor imbalance
- Bearing wear (see `BRG_WEAR_07`)
- Structural resonance at running speed (see `RESONANCE_16`)
- Loose foundation bolts or degraded grout
- Loose coupling guard or other loose attached hardware (a frequent false-positive source)

**Recommended immediate steps:**
1. Confirm the vibration spectrum against the baseline signature recorded at commissioning (Section 2.11) to identify the dominant frequency component.
2. Full diagnostic procedure: see Section 4.6.

### `INSUL_FAIL_06` — Insulation Resistance Low / Ground Fault

**Severity:** Critical. Auto-trips on a confirmed ground fault detected by the stator ground-fault relay; a degraded-but-not-faulted insulation resistance trend is reported as a Warning-level advisory ahead of an actual trip.

**Likely causes:**
- Winding contamination from moisture ingress (see `MOISTURE_ING_17`)
- Insulation aging/degradation from sustained high winding temperature (see `WIND_TEMP_01`)
- Physical insulation damage from a foreign object or mechanical event
- A genuine ground fault within the stator winding

**Recommended immediate steps:**
1. Do not attempt to restart a unit that has tripped on a confirmed ground fault; treat this as an electrical safety event, not a routine restart candidate.
2. Full diagnostic procedure: see Section 4.7.

### `BRG_WEAR_07` — Bearing Wear / Degradation Trend

**Severity:** Warning. Raised by trend analysis of bearing-defect-frequency vibration components over time, distinct from the overall-amplitude-based `VIB_HIGH_05`, and intended as an early-warning trend indicator ahead of an amplitude-based alarm.

**Likely causes:**
- Normal end-of-life bearing wear-out
- Lubrication contamination (see `LUBE_LOW_08`)
- Extended operation with marginal misalignment (see `MISALIGN_15`)
- VFD-induced bearing current damage from switching transients (see Section 2.7 Step 5)

**Recommended immediate steps:**
1. Review the bearing-defect-frequency trend over the preceding weeks in the MotorGuard historian.
2. Schedule bearing replacement at the next planned outage rather than waiting for an amplitude-based `VIB_HIGH_05` trip.

### `LUBE_LOW_08` — Bearing Lubricant Level/Condition Low

**Severity:** Warning.

**Likely causes:**
- Grease fitting or bearing seal leak
- Missed scheduled lubrication interval (see Section 5.7)
- Grease degradation from sustained high bearing temperature

**Recommended immediate steps:**
1. Inspect bearing housing for external grease leakage at seals and fittings.
2. Re-grease per the schedule and quantity in Section 5.7 if the condition is simply an overdue interval; escalate to bearing housing inspection if lubricant is contaminated (discolored, gritty, or emulsified).

### `VFD_FAULT_09` — VFD Communication or Drive Fault

**Severity:** Critical (auto-trip, since loss of VFD control is treated as loss of speed control).

**Likely causes:**
- Damaged or disconnected Modbus communication cable between VFD and MotorGuard controller
- VFD internal overtemperature fault
- VFD firmware fault or unexpected reset
- Electromagnetic interference on the communication cable run

**Recommended immediate steps:**
1. Check the VFD's own local fault display/log for a specific internal fault code before assuming a communications-only issue.
2. Inspect the Modbus cable and connectors for damage.

### `SENSOR_FAIL_10` — Instrument/Sensor Signal Failure

**Severity:** Warning. Raised when any monitored instrument loop reads outside its physically valid range (open circuit, short circuit, or out-of-range signal), rather than an in-range but abnormal process value.

**Likely causes:**
- Damaged signal cable or connector corrosion
- Failed transmitter or sensing element
- Moisture ingress at a junction box with a compromised IP55 seal (see `MOISTURE_ING_17`)

**Recommended immediate steps:**
1. Identify which specific instrument loop is flagged from the MotorGuard alarm detail.
2. Note that a `SENSOR_FAIL_10` on a temperature or vibration input disables the corresponding protective function for that input until cleared — treat this as reducing the unit's protection coverage, not merely as a nuisance alarm.

### `LOCKED_ROTOR_11` — Locked Rotor / Failure to Start

**Severity:** Critical (immediate auto-trip).

**Likely causes:**
- Mechanical seizure of the motor or driven blower
- Foreign object obstruction in the blower
- Bearing seizure from a prior undetected `BRG_WEAR_07` progression
- VFD or control wiring fault preventing a genuine start attempt from reaching the motor

**Recommended immediate steps:**
1. Do not attempt a second start without first checking for mechanical binding by hand-rotating the shaft (with power isolated).
2. Full diagnostic procedure: see Section 4.8.

### `OVERSPEED_12` — Overspeed Detected

**Severity:** Critical (auto-trip).

**Likely causes:**
- VFD parameter fault commanding a speed beyond the configured maximum
- Speed feedback/encoder fault giving a false reading (see `ENCODER_FAULT_19`)
- An external driven-load condition (uncommon on a fan/blower load, but possible during an abnormal process transient) back-driving the motor above commanded speed

**Recommended immediate steps:**
1. Confirm actual speed via an independent method (strobe tachometer or VFD output frequency) before assuming the alarm reading itself is accurate.
2. Do not reset and restart without confirming VFD maximum-frequency configuration against the Section 2.12 commissioning record.

### `UNDERVOLT_13` — Undervoltage

**Severity:** Warning at a sustained voltage below the Section 1.7 tolerance band; escalates to Critical (auto-trip) if voltage drops further or persists beyond a configured duration.

**Likely causes:**
- Upstream plant electrical distribution disturbance
- Excessive voltage drop from an undersized or degraded supply cable
- A large coincident electrical load elsewhere on the same distribution bus

**Recommended immediate steps:**
1. Check whether the undervoltage condition is isolated to this unit's supply or affects the wider plant distribution bus.
2. Avoid commanding a fresh start into a confirmed undervoltage condition, since starting current (Section 1.9) further depresses bus voltage and can compound the problem.

### `STARTS_EXCEED_14` — Excessive Starts Per Hour

**Severity:** Warning. The MotorGuard controller inhibits a further start attempt (rather than tripping a running unit) once the configured starts-per-hour limit (Section 1.7, Section 2.12) is reached.

**Likely causes:**
- Repeated nuisance trips on another code causing repeated restart attempts
- Process control logic cycling the unit more frequently than the design basis
- An operator or automatic sequence attempting rapid restart after a trip without allowing the motor thermal margin to recover

**Recommended immediate steps:**
1. Identify and resolve the underlying cause of the repeated start attempts rather than simply waiting out the inhibit period and restarting, since the excessive-starts condition is itself evidence of an unresolved upstream problem.
2. Review recent alarm history for a recurring trip code preceding each start attempt.

### `MISALIGN_15` — Coupling Misalignment Detected

**Severity:** Warning. Detected via a persistent 1x/2x running-speed vibration signature pattern correlated between DE and NDE sensors, consistent with the alignment-drift signature characterized at commissioning.

**Likely causes:**
- Original installation alignment outside tolerance (see Section 2.6, Section 6.2)
- Thermal growth differential between motor and blower not accounted for during cold alignment
- Foundation settling over time
- Worn coupling elastomer insert

**Recommended immediate steps:**
1. Schedule a laser alignment check at the next planned outage per Section 6.2; this condition rarely requires an immediate unplanned shutdown but should not be deferred indefinitely, since it is a direct contributor to `VIB_HIGH_05` and `BRG_TEMP_02`.

### `RESONANCE_16` — Structural Resonance Detected

**Severity:** Warning. Distinct from `MISALIGN_15` and general `VIB_HIGH_05` in that this code is raised when the dominant vibration frequency corresponds to a known structural natural frequency of the foundation or baseplate rather than to the running speed or its harmonics — see Section 6.6 for the full mechanical discussion of this distinction.

**Likely causes:**
- Operating speed (particularly during VFD ramp-through at partial speed) coinciding with a structural natural frequency
- Foundation or baseplate stiffness degraded from its as-commissioned condition
- A structural modification near the machine (added platform, piping support, etc.) that has shifted a nearby natural frequency into the operating range

**Recommended immediate steps:**
1. Confirm via the vibration spectrum that the dominant frequency does not track running speed as the VFD ramps — a fixed-frequency peak regardless of running speed is the signature of resonance rather than an imbalance or misalignment condition.
2. Full discussion and mitigation approach: see Section 6.6.

### `MOISTURE_ING_17` — Moisture Ingress / Condensation Detected

**Severity:** Warning.

**Likely causes:**
- Compromised terminal box or junction box IP55 seal
- Condensation from a cold-soaked motor exposed to warm, humid ambient air (particularly relevant after an extended outage in cold weather, see Section 6.9)
- Wash-down or cleaning activity near the motor exceeding its enclosure rating

**Recommended immediate steps:**
1. Do not energize a unit with confirmed moisture ingress until winding insulation resistance has been checked per Section 2.9.
2. Inspect and restore the compromised seal before returning the unit to service.

### `ESTOP_ACT_18` — Emergency Stop Activated

**Severity:** Safety (immediate stop, no auto-trip delay).

**Likely causes:**
- Local E-Stop pushbutton manually pressed
- Safety interlock circuit fault
- Coupling guard or other safety guard interlock opened while the unit was running

**Recommended immediate steps:**
1. Do not reset or restart the unit until the cause of the E-Stop event has been positively identified.
2. Follow the lockout/tagout and restart authorization procedure in Section 7 (Appendix A) before returning the unit to service.

### `ENCODER_FAULT_19` — Speed Feedback / Encoder Fault

**Severity:** Warning. Raised when the VFD's speed feedback signal is lost, out of range, or inconsistent with the commanded output frequency for longer than a configured duration.

**Likely causes:**
- Damaged encoder cable or connector
- Encoder failure
- Electrical noise on the feedback signal from inadequate cable shielding or routing

**Recommended immediate steps:**
1. Cross-check against `OVERSPEED_12` and `VFD_FAULT_09` history, since an encoder fault can be a contributing or triggering condition for either.
2. Note that most VFD configurations on the MX-2200 Series can fall back to sensorless speed estimation on a confirmed encoder fault; confirm this fallback is functioning correctly rather than assuming the unit has simply continued operating normally.

### `COOLING_FAN_20` — Auxiliary Cooling Fan Airflow Loss

**Severity:** Warning at reduced airflow; escalates to Critical (auto-trip) if airflow loss is sustained while the unit is operating at or below the minimum speed floor (Section 2.7), since this is the operating condition where the auxiliary fan's contribution to cooling is most necessary.

**Likely causes:**
- Auxiliary fan motor fault
- Fan blade fouling or obstruction
- Loss of the fan's independent single-phase supply
- Fan run-status or current sensor fault (cross-check against `SENSOR_FAIL_10`)

**Recommended immediate steps:**
1. Confirm fan run status and current draw against nameplate.
2. If the fan is confirmed non-functional and the unit is operating at reduced speed, raise VFD speed toward the upper end of its range if process conditions allow, to restore shaft-fan-driven cooling margin while the auxiliary fan is repaired.

## 3.4 Alarm Acknowledgement, Reset, and Escalation

All twenty alarm codes follow a common lifecycle at the MotorGuard controller, regardless of severity:

1. **Raise.** The controller detects the triggering condition and raises the alarm on the local HMI and to the plant DCS, with a timestamp and the triggering value logged to the historian.
2. **Acknowledge.** An operator or technician acknowledges the alarm at the HMI, silencing any audible annunciation. Acknowledgement does not clear the underlying condition and does not, by itself, permit a tripped unit to restart.
3. **Investigate.** The applicable procedure from Section 3.3 (summary) or Section 4 (full procedure, where available) is followed to identify and correct the root cause.
4. **Clear.** Once the underlying condition returns to within normal operating range, Warning-severity alarms clear automatically, while Critical- and Safety-severity alarms that caused an auto-trip require an explicit manual reset at the HMI before a restart can be commanded.
5. **Reset.** Manual reset of a Critical or Safety alarm should only be performed once the root cause has been identified and corrected — never as a first response to "see if it happens again."

**Nuisance alarm handling.** Where a specific alarm is confirmed, through the diagnostic procedures in Section 4 or the general principles in Section 4.1, to be a false trigger from a faulty sensor (`SENSOR_FAIL_10`) rather than a genuine process condition, the affected input may be temporarily forced to a safe bypass state by the site reliability engineer while the sensor is repaired or replaced. This bypass must be time-limited, documented in the maintenance record (Section 5.10), and reversed immediately once the sensor is restored.

**Escalation criteria.** Any alarm that recurs more than twice within a rolling 7-day period on the same unit, even if each individual event was successfully cleared, should be escalated from routine maintenance handling to a formal reliability review, since a recurring alarm indicates the underlying root cause was not actually resolved, only temporarily masked.

## 3.5 Threshold Configuration and Site Customization

The default thresholds referenced throughout this section (for example, the Class B/Class F winding temperature limits for `WIND_TEMP_01`, or ISO 10816-3 Zone C/D for `VIB_HIGH_05`) are the MX-2200 Series factory defaults loaded during commissioning per Section 2.8.

- Thresholds tied to a published standard (ISO 10816-3 vibration zones, motor nameplate current for `OVLD_CUR_03`, insulation class temperature limits for `WIND_TEMP_01`) should generally not be relaxed, since doing so directly reduces the equipment protection margin the standard is designed to preserve.
- Thresholds tied to site-specific conditions (starts-per-hour limit for `STARTS_EXCEED_14`, minimum voltage tolerance for `UNDERVOLT_13`) may reasonably be tuned once sufficient operating history exists, provided the change is reviewed and approved by the site reliability engineer and documented in the maintenance record (Section 5.10).
- Any threshold change must be applied consistently across Motor-1 and Motor-2, since these units are compared against one another (Section 1.8, Section 6.9) to distinguish unit-specific mechanical issues from fleet-wide supply-side or ambient effects.
- Threshold changes should never be made as an undocumented workaround to stop a specific alarm from recurring; the correct response to a recurring alarm is the escalation path above, not a threshold relaxation that merely stops the symptom from being reported.

## 3.6 Detection Signature Reference

| Code | Primary Input(s) | Detection Logic |
|---|---|---|
| `WIND_TEMP_01` | Stator winding RTDs (3-phase) | Threshold-and-duration against insulation class limits, per phase |
| `BRG_TEMP_02` | Bearing RTDs (DE/NDE) | Threshold-and-duration against Warning/Critical setpoint |
| `OVLD_CUR_03` | VFD current feedback | Threshold-and-duration above configured current limit |
| `PH_LOSS_04` | VFD input voltage sensing | Phase-to-phase voltage comparison against balance tolerance |
| `VIB_HIGH_05` | Bearing housing accelerometers (DE/NDE) | Overall vibration amplitude classified against ISO 10816-3 zone boundaries |
| `INSUL_FAIL_06` | Stator ground-fault relay, periodic insulation resistance test | Binary ground-fault detection plus trend analysis of periodic insulation resistance readings |
| `BRG_WEAR_07` | Vibration accelerometers, spectral analysis | Trend analysis of bearing-defect-frequency amplitude over time |
| `LUBE_LOW_08` | Manual inspection entry / grease-life timer | Time-since-last-service counter combined with technician-entered condition observation |
| `VFD_FAULT_09` | VFD internal diagnostics via Modbus | Drive-reported fault code or loss of Modbus communication |
| `SENSOR_FAIL_10` | Any monitored instrument loop | Out-of-physical-range signal (open or short circuit) |
| `LOCKED_ROTOR_11` | VFD current feedback, speed feedback | Sustained high current with zero or near-zero speed feedback following a start command |
| `OVERSPEED_12` | Speed feedback / encoder | Threshold above configured maximum speed |
| `UNDERVOLT_13` | VFD input voltage sensing | Threshold-and-duration below configured minimum voltage |
| `STARTS_EXCEED_14` | VFD run-command counter | Rolling-hour start count against configured limit |
| `MISALIGN_15` | Vibration accelerometers, DE/NDE phase correlation | Trend analysis of correlated 1x/2x running-speed components |
| `RESONANCE_16` | Vibration accelerometers, spectral analysis | Fixed-frequency peak independent of running speed, matched against known structural natural frequencies |
| `MOISTURE_ING_17` | Terminal box moisture sensor | Binary moisture detection |
| `ESTOP_ACT_18` | Local E-Stop circuit / safety relay | Hardwired safety circuit state, independent of MotorGuard software logic |
| `ENCODER_FAULT_19` | VFD encoder feedback signal | Signal loss, out-of-range value, or inconsistency with commanded frequency |
| `COOLING_FAN_20` | Auxiliary fan run-status and current sensor | Threshold-and-duration loss of confirmed airflow, escalated based on current operating speed |

Because `SENSOR_FAIL_10` and `ESTOP_ACT_18` are architecturally distinct from the process-condition alarms (the former detects a signal validity problem across any loop, the latter is a hardwired safety circuit rather than a software threshold), neither can itself be dismissed as a nuisance alarm caused by another sensor fault in the way that, for example, an isolated `BRG_TEMP_02` reading might be — both should always be treated as reported.

## 3.7 Vibration-Related Codes and This Manual's Two Perspectives

Three of the twenty codes in this section — `VIB_HIGH_05`, `MISALIGN_15`, and `RESONANCE_16` — are deliberately covered from two different angles across this manual, and it is worth being explicit about the distinction so a reader is not confused when finding what looks like overlapping content in two places. This section (Section 3, together with the diagnostic procedure in Section 4.6) covers these codes from an **alarm-response perspective**: what the MotorGuard controller detected, how severe it is, and what to check once the alarm is already active. Section 6 (Mechanical Alignment & Balancing) covers the same underlying physical phenomena from an **installation and mechanical-design perspective**: how shaft alignment tolerances, rotor balance grade, soft foot, coupling condition, and structural resonance are established and maintained so that these alarms are infrequent in the first place, rather than what to do once one has already fired.

A technician responding to an active `VIB_HIGH_05` alarm should use Section 4.6 first, since it is written specifically for that in-the-moment diagnostic sequence. A reliability engineer trying to understand why a unit trends closer to the `VIB_HIGH_05` threshold than its sister unit under equivalent load, despite no single alarm event having occurred, should read Section 6, since that is where the underlying installation-quality factors are addressed. Both sections cross-reference each other for exactly this reason, and neither is a substitute for the other.

---

# Section 4: Detailed Troubleshooting Procedures

This section expands seven of the twenty alarm codes from Section 3 into full step-by-step diagnostic procedures: `WIND_TEMP_01`, `BRG_TEMP_02`, `OVLD_CUR_03`, `PH_LOSS_04`, `VIB_HIGH_05`, `INSUL_FAIL_06`, and `LOCKED_ROTOR_11`. These seven were selected because they represent the highest-frequency and highest-consequence alarm events observed across the MX-2200 Series install base, and because several of them (notably `WIND_TEMP_01`, `BRG_TEMP_02`, and `VIB_HIGH_05`) are frequently root-caused to a common set of underlying conditions — misalignment, cooling loss, and electrical supply quality — so diagnosing one thoroughly often resolves or prevents another.

Each procedure assumes the technician has reviewed the corresponding summary entry in Section 3 and has basic access to the MotorGuard local HMI and historian trend data.

## 4.1 General Diagnostic Principles

Before following any of the specific procedures below, apply these general principles, which hold across nearly all alarm conditions on the MX-2200 Series:

- **Confirm before correcting.** A meaningful fraction of alarms on any rotating equipment fleet trace back to a faulty sensor rather than a genuine process condition (see `SENSOR_FAIL_10`). Always cross-check a suspect reading against a second sensor, a handheld instrument, or a physical inspection before taking corrective action on the equipment itself.
- **Check the historian trend, not just the instantaneous value.** A slowly rising trend over days or weeks points to a different class of root cause (wear, fouling, lubrication depletion) than a sudden step change (sensor fault, mechanical failure, external event).
- **Compare against the sister unit.** Because Motor-1 and Motor-2 are of identical construction and normally run in parallel (Section 1.8), a condition shared by both units at the same time points toward a shared supply-side, ambient, or process cause, while a condition isolated to one unit points toward a unit-specific mechanical or electrical fault.
- **Record findings against the unit's individual commissioning baseline** (Section 2.11), not against a generic specification, since minor unit-to-unit variation is normal and expected.

## 4.2 `WIND_TEMP_01` — Stator Winding Temperature High: Diagnostic Procedure

1. **Verify the alarm.** At the MotorGuard HMI, note which winding phase (or phases) raised the alarm, the peak temperature reached, and whether the unit auto-tripped at the Critical threshold or remains running at the Warning threshold.
2. **Cross-check the reading.** Compare against the other two winding phases. A single-phase-only reading that is dramatically higher than the other two, with no corresponding current imbalance, should raise suspicion of a wiring error (see Section 2.13) or a failed RTD before a genuine single-phase heating cause is pursued.
3. **Review the trend.** Pull the last 30 days of winding temperature history for the affected phase from the MotorGuard historian.
   - A gradual rise over weeks suggests a developing cooling deficiency (fouled fan, degrading auxiliary fan) or a slow process load increase.
   - A step change coincident with a specific event (a recent VFD parameter change, a process upset, an auxiliary fan fault) points to that event as the likely trigger.
4. **Check auxiliary cooling fan status and current draw** against nameplate (`COOLING_FAN_20`, Section 3.3). A fan that is running but drawing reduced current, or producing reduced measured airflow, may be mechanically degraded (fouled blades, worn fan bearing) without having tripped its own alarm yet.
5. **Check motor current trend** for the same period (`OVLD_CUR_03`, Section 4.4). Elevated current at a stable process load points toward a genuine overload condition contributing to winding heating, rather than a cooling-side deficiency.
6. **Check for a voltage imbalance history** (`PH_LOSS_04`, Section 4.5) in the preceding hours or days, since imbalance increases winding losses and heating even under otherwise normal load.
7. **Compare against Motor-2 (or Motor-1) under similar load and speed.** A simultaneous rise on both units suggests an ambient or supply-side cause; a rise isolated to one unit points to a unit-specific cooling or electrical fault.
8. **If no cooling, load, or electrical cause is found**, and the winding temperature remains elevated, consider that the insulation system itself may be degrading (age, prior thermal events) and schedule an insulation resistance and polarization index test at the next planned outage (Section 4.7 methodology) even in the absence of a confirmed `INSUL_FAIL_06` event.
9. **Document** the finding, corrective action, and post-correction temperature trend in the unit's maintenance history.

## 4.3 `BRG_TEMP_02` — Bearing Temperature High: Diagnostic Procedure

1. **Verify the alarm.** Note which bearing (DE or NDE), the peak temperature reached, and whether the unit auto-tripped at the Critical threshold (100 °C) or remains running at the Warning threshold (85 °C).
2. **Cross-check the reading.** Compare against the opposite bearing's temperature and, where safe, take a handheld infrared reading at the bearing housing surface near the RTD location.
3. **Review the trend.** A gradual rise over weeks suggests lubrication degradation or slow bearing wear; a step change coincident with a specific event points to that event as the likely trigger.
4. **Check vibration on the same bearing** (`VIB_HIGH_05`, Section 4.6). A coincident rise in both temperature and vibration on the same bearing strongly indicates a mechanical root cause — misalignment, imbalance, or bearing wear — rather than a purely thermal/lubrication issue.
5. **Inspect lubrication.** With the unit isolated and locked out (Section 7), remove a small grease sample from the bearing housing relief port. Check for discoloration (thermal degradation), grittiness (contamination or wear debris), or emulsification (water ingress through a failed housing seal). Any of these findings indicates the bearing housing should be opened for full inspection rather than simply re-greased.
6. **Inspect for misalignment.** If lubrication is acceptable, perform a laser alignment check per Section 6.2. Realign if outside tolerance and re-run the unit, monitoring bearing temperature over the following 24–48 hours.
7. **If no lubrication or alignment cause is found**, schedule the bearing for replacement at the next planned outage as a precaution, and increase monitoring frequency until then.
8. **Document** the finding, corrective action, and post-correction temperature trend.

## 4.4 `OVLD_CUR_03` — Overload / Overcurrent: Diagnostic Procedure

1. **Confirm the alarm** and pull the motor current trend from the VFD/MotorGuard historian for the minutes leading up to the trip, noting whether current rose gradually or stepped up suddenly.
2. **Before any restart attempt, isolate electrical power and hand-rotate the shaft** at the coupling (with the coupling guard removed per Section 2.6) to check for mechanical binding, grinding, or abnormally high rotating resistance. Do not attempt an electrical restart to "test" a suspected mechanical bind.
3. **If the shaft rotates freely**, review recent `PH_LOSS_04` history for any voltage imbalance event coincident with or preceding the overload, since imbalance increases motor current draw even under normal mechanical load.
4. **If no phase imbalance is found**, verify VFD configuration parameters (current limit, motor nameplate data) against the values specified in Section 2.12 to rule out a configuration fault rather than a genuine overload condition.
5. **If the shaft does not rotate freely**, this indicates a mechanical bind requiring further disassembly to locate: common causes on the MX-2200 Series include a seized bearing (cross-check recent `BRG_TEMP_02` or `BRG_WEAR_07` history) or an obstruction within the driven blower.
6. **If a gradual current rise was observed** rather than a sudden step, consider a process-side cause: process air demand or system resistance higher than the design basis, increasing blower loading and motor current at a given speed without any motor mechanical fault.
7. **Once the root cause is corrected**, restart at reduced VFD speed if possible and ramp gradually to the duty point while monitoring current.
8. **Document** the root cause; a mechanical bind finding should trigger a full inspection at the next outage even if the immediate obstruction is cleared.

## 4.5 `PH_LOSS_04` — Phase Loss / Voltage Imbalance: Diagnostic Procedure

1. **Confirm the alarm** and note which phase(s) were affected and the magnitude of imbalance or the specific phase reported lost.
2. **Do not restart the unit** until phase voltages have been measured and confirmed balanced and within tolerance at the motor terminals directly, since restarting into a genuine phase-loss condition risks immediate `OVLD_CUR_03` and potential winding damage.
3. **Check the upstream breaker or fuse** for the affected unit's motor circuit for a tripped or blown condition on a single phase — this is the most common single-unit root cause.
4. **If the breaker/fuse is intact**, check terminal connections at the motor junction box and at the VFD output terminals for looseness or corrosion.
5. **Check whether the sister unit (Motor-1 or Motor-2) or other loads on the same electrical bus experienced a coincident event.** A simultaneous event across multiple units points to an upstream supply-side fault rather than a fault local to the single unit, and should be escalated to the electrical/utility team.
6. **Once the fault is corrected and phase voltages confirmed balanced**, restart per the standard start-up sequence (Section 2.10), monitoring current closely through the ramp to rated speed.
7. **Document** whether the event was isolated to one unit or affected multiple units on the same bus.

## 4.6 `VIB_HIGH_05` — Excessive Vibration: Diagnostic Procedure

1. **Confirm the alarm** and note which bearing housing (DE or NDE), the peak amplitude reached, and the ISO 10816-3 zone (Warning = Zone C, Critical = Zone D).
2. **Pull the vibration spectrum** (not just overall amplitude) from the MotorGuard historian and identify the dominant frequency component:
   - **1x running speed** — most consistent with rotor imbalance.
   - **2x running speed** — most consistent with coupling misalignment specifically (`MISALIGN_15`).
   - **Bearing defect frequencies** — consistent with bearing wear; cross-check against any open `BRG_WEAR_07` trend alarm.
   - **A fixed frequency that does not track running speed as the VFD ramps** — consistent with structural resonance; see `RESONANCE_16` and the full mechanical discussion in Section 6.6, not a rotor-dynamic cause.
   - **Broadband, no clear dominant frequency** — consider loose external hardware (guards, brackets) or foundation degradation.
3. **Compare against the commissioning baseline spectrum** (Section 2.11) to determine whether this is a new frequency component or a growth in amplitude of a component already present at low level.
4. **If 1x or 2x dominant:** perform a physical inspection walk-down, checking coupling guard security and foundation bolt tightness, before scheduling a laser alignment check per Section 6.2.
5. **If a fixed, speed-independent frequency dominant:** proceed to the Section 6.6 resonance investigation rather than pursuing an alignment or balance correction, since neither will resolve a genuinely resonant condition.
6. **If bearing-defect frequency dominant:** treat as an advanced-stage bearing condition and schedule bearing replacement promptly rather than at the next routine outage.
7. **If the unit auto-tripped at Critical (Zone D):** do not restart until at least a visual and alignment check has been completed.
8. **Document** the spectral signature and corrective action for trend comparison at the next alarm event.

## 4.7 `INSUL_FAIL_06` — Insulation Resistance Low / Ground Fault: Diagnostic Procedure

1. **Confirm the alarm** and distinguish between a confirmed ground-fault trip (Critical, auto-tripped) and a Warning-level advisory based on a declining insulation resistance trend without an actual fault.
2. **For a confirmed ground fault:** treat as an electrical safety event. Do not attempt to restart. Lock out and tag out the unit per Section 7 before any further work, and notify qualified electrical personnel.
3. **Perform a megohmmeter insulation resistance test** at the motor terminals, with the unit isolated, and compare the reading against the minimum acceptable value used at commissioning (Section 2.9) and any subsequent periodic test recorded in the maintenance history.
4. **Check for a recent `MOISTURE_ING_17` event** in the days preceding the alarm; moisture-related insulation degradation often presents first as a declining trend before an outright fault, and confirming a prior moisture event helps distinguish a recoverable contamination issue from a permanent winding failure.
5. **Check for a sustained `WIND_TEMP_01` history** preceding the event; thermal aging of the insulation system from prior sustained high-temperature operation is a plausible long-term contributing cause even if the immediate trigger was something else.
6. **Perform a polarization index test** (ratio of the 10-minute to 1-minute insulation resistance reading) where the initial megohmmeter reading is ambiguous, since this test better distinguishes surface contamination (which a simple resistance reading can mistake for genuine insulation degradation) from true insulation aging.
7. **If insulation resistance is confirmed low but no ground fault has occurred**, the winding may be dried out and returned to service (for contamination-related low readings) or may require rewind/replacement (for confirmed aging-related degradation) — this determination should be made by qualified electrical personnel based on the specific test results, not assumed from the alarm alone.
8. **Document** the test results and determination, since a winding that is dried out and returned to service should be tracked with more frequent insulation resistance testing for a period afterward to confirm the condition does not recur.

**Worked example.** Suppose Motor-1's quarterly insulation resistance readings (Section 5.13) over the preceding year were 420, 380, 290, and 210 megohms, each individually well above the 100-megohm minimum, but showing a clear and accelerating downward trend rather than the flat trend typical of a healthy winding. Under Step 8 of this procedure, this pattern should trigger a polarization index test even though no individual reading has approached the acceptance minimum and no `INSUL_FAIL_06` alarm has actually fired. If the polarization index test returns a ratio of 2.3, this is above the 2.0 minimum in Section 5.13 and indicates the winding, while trending downward, does not yet show the specific signature of aging-related degradation and may reflect a slower, more benign contamination buildup instead; a ratio below 2.0 under the same trend would instead point toward genuine aging and justify escalating the outage priority for a full winding evaluation ahead of the next scheduled annual test. This example illustrates why the trend-based interpretation in Section 5.13 is treated as complementary to, not a replacement for, the polarization index test in this procedure — the trend flags that something is changing, while the polarization index test helps characterize what kind of change it is.

## 4.8 `LOCKED_ROTOR_11` — Locked Rotor / Failure to Start: Diagnostic Procedure

1. **Confirm the alarm** and note the current profile during the failed start attempt from the MotorGuard historian — a current that reached and held near the locked-rotor value in Section 1.9 without any corresponding speed feedback indicates a genuine mechanical lock rather than a control fault.
2. **Isolate electrical power and lock out the unit (Section 7) before any physical investigation.**
3. **Attempt to hand-rotate the shaft** at the coupling. If the shaft will not rotate by hand, this confirms a mechanical seizure requiring disassembly to locate — common causes include a seized bearing (cross-check recent `BRG_TEMP_02` or `BRG_WEAR_07` trend history) or an obstruction within the driven blower that should be inspected before the motor itself is disassembled.
4. **If the shaft rotates freely by hand**, the failure to start is not a genuine mechanical lock; review the VFD and MotorGuard control wiring for a fault that may have prevented a genuine start command from reaching the motor, or an encoder/feedback fault (`ENCODER_FAULT_19`) that caused the controller to interpret a successful start as a failed one.
5. **Check for a preceding `UNDERVOLT_13` event** at the moment of the start attempt; a supply voltage sag during a high-current start attempt can prevent the motor from developing sufficient torque to accelerate away from zero speed even with no mechanical fault present, particularly if another large load started on the same bus at a similar time.
6. **Review the `STARTS_EXCEED_14` history** for the unit; multiple recent failed start attempts in quick succession compound thermal stress on the winding even if each individual attempt was correctly tripped before reaching a damaging duration, and the unit should not be subjected to a further start attempt until the underlying cause is identified.
7. **Once the root cause is corrected**, and only after confirming the shaft rotates freely and electrical supply is confirmed within tolerance, attempt a further start with close monitoring of current and speed feedback from the first instant of the start command.
8. **Document** the root cause; any mechanical seizure finding should trigger a full bearing and coupling inspection at the next outage even if the immediate obstruction is cleared, since the underlying cause of the seizure may not be fully resolved by simply freeing the shaft.

## 4.9 Cross-Cutting Root Cause Relationships

The seven procedures above are presented as independent alarm responses, but in practice a small number of underlying conditions are shared root causes across several of them. Recognizing these relationships allows a technician to investigate more efficiently, since correcting one underlying condition often resolves or prevents several alarm codes at once.

- **Misalignment** (Section 6.2) is a direct or contributing cause of `VIB_HIGH_05` (Section 4.6), `BRG_TEMP_02` (Section 4.3), and the trend-based `MISALIGN_15` (Section 3.3). A unit presenting any one of these should have alignment checked even if the alarm that actually triggered was a different one of the three.
- **Cooling deficiency** links `COOLING_FAN_20` (Section 3.3) directly to `WIND_TEMP_01` (Section 4.2) as a precursor-to-consequence pair, particularly at reduced VFD speed where the auxiliary fan's contribution is most significant. A technician investigating an unexplained `WIND_TEMP_01` should always check auxiliary fan status per Section 4.2 Step 4 before assuming a purely electrical or process cause.
- **Lubrication condition** connects `LUBE_LOW_08`, `BRG_TEMP_02` (Section 4.3), and `BRG_WEAR_07` (Section 3.3) as a single degradation pathway: degraded or depleted lubrication first presents as a `LUBE_LOW_08` or a slow bearing temperature rise, and if not corrected, progresses to measurable bearing wear and eventually to `VIB_HIGH_05` at bearing-defect frequency.
- **Electrical supply quality** connects `PH_LOSS_04` (Section 4.5), `OVLD_CUR_03` (Section 4.4), `UNDERVOLT_13`, and `LOCKED_ROTOR_11` (Section 4.8): a voltage imbalance or undervoltage event that does not itself reach the phase-loss threshold can still elevate motor current enough to approach an overload trip, or prevent adequate starting torque during a start attempt. Reviewing electrical supply history is accordingly an explicit step within both the `OVLD_CUR_03` and `LOCKED_ROTOR_11` procedures.
- **Thermal history** connects `WIND_TEMP_01` (Section 4.2) to `INSUL_FAIL_06` (Section 4.7): sustained operation at elevated winding temperature accelerates insulation aging, so a unit with a history of `WIND_TEMP_01` events should be considered at elevated risk for a future `INSUL_FAIL_06` finding even in the absence of any single acute triggering event.

## 4.10 Post-Repair Verification and Return-to-Service Checklist

Regardless of which of the seven procedures above was followed, the following verification steps apply generally before returning a unit to continuous duty after any Critical or Safety alarm event:

1. **Confirm the specific corrective action taken** is recorded against the unit and the alarm code in the maintenance record (Section 5.10), including parts replaced, adjustments made, and any threshold or configuration changes per Section 3.5.
2. **Run the unit at reduced speed first**, where process conditions allow, rather than commanding full rated speed immediately on restart, so that early signs of an incomplete repair are observed under lower mechanical and thermal stress.
3. **Monitor continuously for the first two hours of operation following any bearing, insulation, or alignment-related repair**, since infant-mortality failures of a freshly repaired or replaced component typically present within this window.
4. **Compare post-repair readings against the unit's own commissioning baseline** (Section 2.11) rather than against a generic specification.
5. **Re-arm all bypassed instrument inputs** (Section 3.4, nuisance alarm handling) that may have been temporarily forced to a safe state during the investigation, and confirm each shows a valid, in-range reading before the unit is released to service.
6. **Following any `LOCKED_ROTOR_11` or `INSUL_FAIL_06` event specifically**, confirm the starts-per-hour counter (`STARTS_EXCEED_14`) has not been left in an inhibited state that would prevent a legitimate subsequent start once the unit is actually ready for service.

## 4.11 Tools and Instruments Required

| Tool/Instrument | Used In | Notes |
|---|---|---|
| Handheld infrared thermometer | Sections 4.2, 4.3 | For cross-checking RTD readings against a physical measurement |
| Laser shaft alignment system | Sections 4.3, 4.6, 6.2 | Primary method; dial indicators are an acceptable fallback |
| Vibration analyzer with spectral (FFT) capability | Sections 4.6, 3.6, 6.6 | Overall-amplitude-only meters are insufficient for the spectral diagnosis described in Section 4.6 Step 2 |
| Grease sampling kit | Section 4.3 Step 5 | Includes sample containers for condition inspection |
| Clamp-on multimeter / phase rotation tester | Sections 4.4, 4.5, 2.5 | For motor current and phase voltage/rotation verification |
| Megohmmeter (insulation resistance tester) | Sections 4.7, 2.1, 2.9 | Primary instrument for insulation and ground-fault investigation |
| Polarization index test capability (typically integral to a modern megohmmeter) | Section 4.7 Step 6 | Distinguishes surface contamination from true insulation aging |
| Strobe tachometer | Section 3.3 (`OVERSPEED_12`) | For independent speed confirmation |
| MotorGuard historian workstation access | All seven procedures | Required for trend review; field investigation without historian access should be considered incomplete per Section 4.1 |

## 4.12 Common Diagnostic Mistakes to Avoid

The following mistakes recur often enough across the seven procedures in this section to call out explicitly, since each one has been observed to significantly extend investigation time or, in some cases, to cause a repeat failure of the same alarm shortly after an apparently successful correction:

- **Resetting and restarting a Critical alarm without a specific corrective action.** This is addressed in Section 3.4, but bears repeating here in the troubleshooting context: an `OVLD_CUR_03` or `LOCKED_ROTOR_11` trip that is reset and restarted purely because "it might not happen again" discards the diagnostic value of the trip and risks a repeat event under load, or worse, a repeat event that causes actual damage where the first trip did not.
- **Treating a single-phase winding temperature reading as automatically indicating a real electrical fault**, without first ruling out the RTD wiring error described in Section 2.13 Step 3. This specific commissioning error is common enough on the MX-2200 Series that it should be the first thing checked, not the last, when a `WIND_TEMP_01` reading looks inconsistent with the current and vibration data on the same unit.
- **Performing an alignment correction without first checking for soft foot** (Section 6.4). Correcting alignment on a motor with an uncorrected soft foot condition often produces a result that appears correct immediately after the correction but drifts back out of tolerance within days or weeks as the frame relaxes, which is easily misread as a fresh `MISALIGN_15` recurrence rather than as an incomplete original correction.
- **Assuming a vibration alarm is rotor-dynamic (imbalance or misalignment) without checking whether the dominant frequency tracks running speed.** As described in Section 4.6 Step 2 and Section 6.6, a fixed, speed-independent frequency is a resonance signature, and no amount of alignment or balancing work will resolve it — misdiagnosing resonance as misalignment leads to repeated, ineffective alignment corrections.
- **Investigating `INSUL_FAIL_06` using only a single-point resistance reading** rather than the polarization index comparison in Section 4.7 Step 6, which risks either scrapping a winding that only has recoverable surface contamination, or returning to service a winding with genuine aging-related degradation that a single reading did not clearly distinguish from contamination.

---

# Section 5: Routine Maintenance Schedule

## 5.1 Maintenance Philosophy

The MX-2200 Series maintenance schedule combines fixed-interval preventive tasks (cleaning, lubrication, inspection, electrical testing) with condition-based tasks driven by MotorGuard trend data (vibration, temperature, bearing-defect frequency, insulation resistance trend). Fixed intervals below are the minimum required frequency; any unit trending toward an alarm threshold ahead of schedule (per Section 4 diagnostic procedures) should have its maintenance interval shortened accordingly rather than waiting for the next scheduled date.

Because Motor-1 and Motor-2 both run continuously under normal operation rather than one standing idle in standby, this schedule does not include a standby-exercise requirement analogous to the pump fleet's Pump-3, but does place correspondingly greater emphasis on the cross-unit comparison techniques in Section 4.1 and Section 4.9, since there is no idle reference unit against which a running unit's condition can be checked at will.

## 5.2 Daily Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Visual walk-down | Inspect for visible leaks at bearing housings, unusual discoloration, or debris accumulation | `LUBE_LOW_08`, `MOISTURE_ING_17` |
| Unusual noise/vibration | Listen for abnormal noise; note any change from baseline | `VIB_HIGH_05`, `RESONANCE_16` |
| MotorGuard HMI review | Confirm no active or unacknowledged alarms on either unit | All codes |
| Auxiliary cooling fan | Visually confirm fan is running and unobstructed | `COOLING_FAN_20` |
| Terminal box condition | Visually confirm no signs of moisture or overheating discoloration | `MOISTURE_ING_17`, `WIND_TEMP_01` |

## 5.3 Weekly Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Vibration trend review | Review 7-day vibration trend for both units at the MotorGuard historian | `VIB_HIGH_05`, `BRG_WEAR_07` |
| Bearing and winding temperature trend review | Review 7-day temperature trend for both bearings and all three winding phases | `BRG_TEMP_02`, `WIND_TEMP_01` |
| Motor current trend | Review for gradual upward drift | `OVLD_CUR_03` |
| Coupling guard security | Confirm guard is secure and undamaged | `VIB_HIGH_05` (false-positive prevention) |
| Cross-unit comparison | Compare Motor-1 and Motor-2 readings under similar load | Section 4.1, Section 4.9 |

## 5.4 Monthly Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Bearing grease condition sample | Extract small sample from relief port, inspect per Section 4.3 Step 5 | `LUBE_LOW_08`, `BRG_TEMP_02` |
| Alignment visual check | Confirm coupling insert wear and guard condition | `MISALIGN_15` |
| Instrument loop spot-check | Verify one rotating instrument loop per visit against a reference reading | `SENSOR_FAIL_10` |
| Auxiliary cooling fan current draw | Compare against nameplate and commissioning baseline | `COOLING_FAN_20` |
| Starts-per-hour history review | Confirm no unit is approaching the `STARTS_EXCEED_14` limit as a matter of routine operation rather than a rare event | `STARTS_EXCEED_14` |

## 5.5 Quarterly Checks (Both Units)

| Task | Action | Related Alarm Codes |
|---|---|---|
| Full bearing re-grease | Purge and replenish grease per Section 5.7 quantities | `LUBE_LOW_08`, `BRG_TEMP_02`, `BRG_WEAR_07` |
| Laser alignment verification | Full laser alignment check per Section 6.2 procedure | `MISALIGN_15`, `VIB_HIGH_05` |
| Vibration spectral baseline comparison | Full spectrum analysis against commissioning baseline (Section 2.11), not just overall amplitude | `VIB_HIGH_05`, `BRG_WEAR_07`, `RESONANCE_16` |
| Insulation resistance test | Megohmmeter test at motor terminals, unit isolated, compared against commissioning and prior quarterly readings | `INSUL_FAIL_06` |
| Electrical connection torque check | Verify motor and VFD terminal torque per Section 5.8 | `PH_LOSS_04`, `OVLD_CUR_03` |

## 5.6 Annual Checks / Major Overhaul Planning

| Task | Action | Related Alarm Codes |
|---|---|---|
| Bearing full inspection | Open bearing housing, inspect bearings, replace if wear indicators present | `BRG_WEAR_07`, `BRG_TEMP_02` |
| Full winding insulation test including polarization index | Comprehensive electrical test per Section 4.7 methodology | `INSUL_FAIL_06`, `WIND_TEMP_01` |
| Auxiliary cooling fan full inspection | Inspect fan blades, bearing, and mounting for wear or fouling | `COOLING_FAN_20` |
| Foundation and grout inspection | Inspect for cracking, settling, or bolt looseness | `VIB_HIGH_05`, `MISALIGN_15`, `RESONANCE_16` |
| MotorGuard controller calibration | Full instrument loop calibration check, all inputs | `SENSOR_FAIL_10` |
| VFD parameter audit | Confirm all Section 2.12 parameters remain as commissioned | `OVLD_CUR_03`, `OVERSPEED_12`, `STARTS_EXCEED_14` |

## 5.7 Lubrication Schedule and Specifications

| Item | Lubricant | Quantity per Bearing Housing | Interval |
|---|---|---|---|
| Drive-end roller bearing | NLGI Grade 2 lithium-complex grease | 60 g per relief cycle | Quarterly (Section 5.5), or immediately upon `LUBE_LOW_08` |
| Non-drive-end ball bearing | NLGI Grade 2 lithium-complex grease | 35 g per relief cycle | Quarterly (Section 5.5), or immediately upon `LUBE_LOW_08` |
| Bearing grease sample check | N/A (inspection only) | N/A | Monthly (Section 5.4) |

Over-greasing is as harmful as under-greasing on rolling-element bearings: excess grease increases churning losses and can itself drive bearing temperature toward the `BRG_TEMP_02` Warning threshold. Always purge the correct calculated quantity for the specific bearing size, not a generalized "fill until it appears at the relief port" approach.

## 5.8 Torque Specifications (Key Fasteners)

| Fastener | Torque |
|---|---|
| Motor foot bolts (M20) | 285 N·m |
| Bearing housing cap bolts (M10) | 55 N·m |
| Coupling hub set screws | 35 N·m |
| Terminal box lugs (main power) | Per motor manufacturer nameplate/data sheet — verify at each quarterly electrical check (Section 5.5) |
| Terminal box ground lug | 25 N·m |

## 5.9 Recommended Spare Parts and Insurance Spares

| Part | Recommended Quantity On-Hand | Rationale |
|---|---|---|
| Bearing set (DE + NDE), matched pair | 1 set, shared across the fleet | Bearings are interchangeable across both units |
| Coupling insert | 2 | Low cost, consumable wear item |
| Auxiliary cooling fan assembly | 1, shared across the fleet | Directly tied to `COOLING_FAN_20` and downstream `WIND_TEMP_01` risk, particularly at reduced VFD speed |
| MotorGuard controller (spare unit) | 1, shared across the fleet | Minimizes downtime from a `VFD_FAULT_09`-adjacent controller hardware fault |
| RTD sensor sets (bearing and winding) | 1 spare set per sensor type | Addresses `SENSOR_FAIL_10` events without waiting on procurement |

Typical procurement lead times mirror those of comparable rotating equipment components elsewhere in the MechMind fleet: bearing sets and coupling inserts are generally available within 2–4 weeks, while the MotorGuard controller carries a longer 6–10 week lead time and should be treated as a priority stocking item and periodically bench-tested rather than stored indefinitely as an unverified spare, since a controller fault removes protective monitoring rather than merely stopping the motor.

## 5.10 Maintenance Record Keeping

All maintenance actions, whether scheduled or triggered by an alarm event under Section 4, must be logged against the specific unit tag (Motor-1 or Motor-2) in the site CMMS, cross-referenced to the relevant alarm code where applicable. This record-keeping discipline is what allows the trend-based codes — `BRG_WEAR_07`, `LUBE_LOW_08`, `MISALIGN_15` — to function as genuine early-warning indicators rather than one-off events, since their value depends on comparing each new reading against an accurate history of prior findings and corrective actions for that specific unit.

## 5.11 Consumables, Waste Handling, and Disposal

- **Used bearing grease** should be collected and disposed of per the site's lubricant waste stream, particularly if a sample shows signs of water emulsification.
- **Removed bearings** from a wear-related replacement (Section 4.3, Section 5.6) should be retained briefly for failure-mode inspection before disposal, since the wear pattern is diagnostic evidence relevant to the Section 4.9 root-cause relationships.
- **Insulation test byproducts** (none directly generated, but any winding material removed during a rewind or repair) should be handled per the site's electrical component waste procedure.

## 5.12 Condition Monitoring Review Cadence

| Review | Frequency | Purpose |
|---|---|---|
| Cross-unit comparison review | Monthly | Compare bearing/winding temperature, vibration, and motor current baselines between Motor-1 and Motor-2 to distinguish unit-specific drift from fleet-wide supply-side or ambient effects |
| Trend-code review (`BRG_WEAR_07`, `LUBE_LOW_08`, `MISALIGN_15`) | Monthly | Confirm these early-warning trends are being acted on before they progress to an amplitude-based Critical alarm, per the degradation pathway described in Section 4.9 |
| Alarm recurrence review | Monthly | Apply the escalation criteria in Section 3.4 across the full alarm history |
| Full commissioning-baseline re-comparison | Annual, aligned with Section 5.6 | Confirm each unit's current performance and vibration/temperature baseline against its original Section 2.11 commissioning record |

## 5.13 Electrical Testing Program Detail

The quarterly insulation resistance test (Section 5.5) and annual full winding test (Section 5.6) together form the electrical condition-monitoring program for Motor-1 and Motor-2, feeding directly into `INSUL_FAIL_06` trend evaluation (Section 3.3, Section 4.7). The following pass/trend criteria apply:

| Test | Interval | Acceptance / Trend Criteria |
|---|---|---|
| Insulation resistance (megohmmeter, 500 V DC test) | Quarterly | Minimum 100 megohms at ambient, temperature-corrected per the site's standard correction table; a reading trending downward across three consecutive quarters should be escalated for a polarization index test even if each individual reading remains above the minimum |
| Polarization index | Annual, or triggered by a declining insulation resistance trend | Ratio of 10-minute to 1-minute reading; a ratio below 2.0 indicates likely contamination or aging requiring further evaluation before continued service |
| Ground-fault relay function test | Annual | Confirm the relay correctly trips a simulated fault injection at the configured sensitivity |
| Winding resistance balance (phase-to-phase) | Annual | Maximum 2% deviation between phases; greater deviation indicates a developing winding fault even in the absence of an active `INSUL_FAIL_06` or `WIND_TEMP_01` condition |

Recording each quarterly and annual result against the unit's own historical series, rather than checking only against the pass/fail minimum, is what allows a slow insulation degradation trend to be caught and scheduled for correction well before it reaches the point of an unplanned `INSUL_FAIL_06` trip — this is the same trend-based philosophy applied to `BRG_WEAR_07` and `MISALIGN_15` elsewhere in this manual, applied here to the electrical condition of the winding.

---

# Section 6: Mechanical Alignment & Balancing

## 6.1 Purpose and Relationship to Section 3 / Section 4

This section addresses vibration and rotor-dynamic behavior from the perspective of **installation, alignment, and balance quality** — as distinct from the **alarm-response perspective** already covered for `VIB_HIGH_05` (Sections 3.3 and 4.6), `MISALIGN_15` (Section 3.3), and `RESONANCE_16` (Section 3.3). Sections 3 and 4 address what to do once a vibration-related alarm has already been raised on a specific unit. This section addresses the installation practices and mechanical design factors that determine how much margin exists between normal operation and those alarm thresholds in the first place, so that Motor-1 and Motor-2 are not chronically operating close to their vibration alarm thresholds under normal, fault-free conditions.

A unit that trips `VIB_HIGH_05` repeatedly despite passing every check in the Section 4.6 alarm-response procedure should prompt a review of this section's alignment, balance, and resonance factors before further component-level disassembly is pursued.

## 6.2 Shaft Alignment Methodology and Tolerances

Precision shaft alignment between the motor and its driven blower is the single largest controllable factor in long-term vibration and bearing life on the MX-2200 Series. The following methodology and tolerances apply to both the initial commissioning alignment (Section 2.6) and any subsequent alignment check performed under Section 4.3, Section 4.6, or the quarterly schedule (Section 5.5):

1. **Cold alignment measurement.** With the machine at ambient (non-running) temperature, mount a laser alignment system across the coupling hubs and measure angular and parallel offset in both the vertical and horizontal planes.
2. **Target tolerances.** Parallel offset ≤ 0.05 mm; angular offset ≤ 0.05 mm per 100 mm of coupling spacer length. These values are tighter than the coupling manufacturer's maximum allowable values by design margin, since alignment drift is a leading long-term contributor to `VIB_HIGH_05` and `BRG_TEMP_02` over the service life of the unit.
3. **Thermal growth compensation.** Because the motor frame and the driven blower's bearing structure grow differently as each reaches its own operating temperature, a cold alignment target that ignores this differential growth will not remain in tolerance once the machine train reaches thermal equilibrium. For the MX-2200 Series driving a centrifugal blower of the type used in this installation, the standard cold-alignment offset target compensates for an expected vertical differential growth of approximately 0.08 mm at the motor relative to the blower once both reach steady-state operating temperature; sites with a different driven-equipment thermal growth characteristic should have this compensation value re-derived rather than assumed.
4. **Correction method.** Correct alignment using shims under the motor feet only — never shim under the driven blower's feet, as the blower centerline is the fixed reference for the coupled train.
5. **Verification after torque.** Re-torque motor hold-down bolts to the Section 5.8 value after final shim adjustment and re-verify alignment did not shift during torqueing; a measurable shift here often indicates a soft-foot condition (Section 6.4) that has not yet been corrected.
6. **Hot alignment check (recommended, not mandatory).** Where a unit has a history of vibration or bearing temperature trending upward after several hours of run time despite passing a cold alignment check, a hot alignment check — repeating the laser measurement after the unit has reached thermal equilibrium at operating speed — can reveal a thermal growth compensation error that a cold-only check would not detect.

## 6.3 Rotor Balance Grade and Its Role in the Coupled Train

The MX-2200 Series rotor is balanced to ISO 21940 Grade G2.5 (Section 1.3) — a notably tighter balance grade than is typical for many driven-equipment rotating components, including the centrifugal blower impellers coupled to Motor-1 and Motor-2. This is a deliberate design choice: because the motor rotor is the higher-speed, more balance-sensitive half of the coupled train and is also the half of the train most directly instrumented by the MotorGuard vibration sensors (Section 1.6), holding the motor rotor to a tight balance grade maximizes the diagnostic value of the vibration data described throughout Sections 3 and 4 — a 1x running-speed vibration component seen at the motor bearing housings can be attributed with higher confidence to the driven-equipment side of the train (misalignment, coupling condition, or blower impeller imbalance) precisely because the motor rotor itself is known to be well within its own tight balance tolerance.

This has a practical consequence for troubleshooting: if a 1x running-speed vibration component is observed and a subsequent alignment check (Section 6.2) is confirmed within tolerance, the next most likely source is imbalance on the driven blower side of the coupling rather than the motor rotor itself, since the motor rotor's balance grade makes it a comparatively unlikely contributor to a new imbalance-type vibration signature once it has passed its own commissioning balance verification.

## 6.4 Soft Foot Detection and Correction

A "soft foot" condition — where one or more of the motor's mounting feet does not sit flush against the baseplate before bolt torque, causing the frame to distort slightly when the hold-down bolts are tightened — is a common and frequently overlooked contributor to vibration and to the apparent alignment shift sometimes observed after bolt torque (Section 6.2 Step 5).

1. With the motor aligned and shimmed per Section 6.2 but before final bolt torque, loosen each hold-down bolt individually while monitoring a dial indicator mounted to read vertical movement at that foot.
2. A movement greater than approximately 0.05 mm at any single foot as its bolt is loosened indicates a soft foot condition at that location.
3. Correct by adding or adjusting shims at the affected foot until the movement measured in Step 2 falls within tolerance, then repeat the full alignment check per Section 6.2, since correcting a soft foot at one location can shift the overall alignment result.
4. A soft foot condition that recurs after correction, or that appears at a different foot each time it is checked, may indicate baseplate distortion or foundation degradation rather than a simple shimming issue, and should be escalated for a foundation inspection per Section 5.6.

## 6.5 Coupling Selection and Inspection

Motor-1 and Motor-2 use a spacer-type flexible coupling (Section 1.3) selected specifically to permit bearing and seal-equivalent service without disturbing the driven blower, consistent with the coupling philosophy used across the MechMind rotating equipment fleet. Beyond its alignment role, the coupling's elastomeric insert is a wear item whose condition directly affects the vibration signature discussed in Section 4.6:

- A worn or degraded coupling insert typically presents as an increased 2x running-speed vibration component, similar in signature to (and easily confused with) angular misalignment — visual inspection of the insert during the monthly check (Section 5.4) is the most reliable way to distinguish the two, since a worn insert will show visible cracking, compression set, or material loss that an alignment measurement alone would not reveal.
- Coupling inserts should be replaced proactively at the interval recommended by the coupling manufacturer for the installed duty cycle, rather than run to visible failure, since a failed insert in service risks a sudden, severe vibration event rather than the gradual trend that would otherwise give advance warning through `MISALIGN_15`.

## 6.6 Structural Resonance: Identification and Mitigation

Structural resonance — where a structural natural frequency of the foundation, baseplate, or an attached structure coincides with the motor's running speed or a multiple of it — produces a vibration signature that can superficially resemble imbalance or misalignment but does not respond to correcting either, which is why `RESONANCE_16` (Section 3.3) is tracked as a distinct alarm code from `VIB_HIGH_05` and `MISALIGN_15`.

**Identification.** The defining diagnostic signature of resonance is that the dominant vibration frequency remains fixed regardless of running speed, rather than scaling with it. Because Motor-1 and Motor-2 operate across a VFD speed range of 15–60 Hz (Section 1.4), any speed within that range that produces a disproportionate vibration response relative to adjacent speeds — a "resonance peak" during a slow speed sweep — should be treated as a strong indicator of a structural natural frequency within the operating range, even if the peak amplitude at that specific speed does not itself reach the `VIB_HIGH_05` alarm threshold during a brief transit through it.

**Mitigation approaches**, in order of typical practicality:

1. **Avoid the resonant speed operationally**, by configuring the VFD to skip through the affected speed band rapidly during acceleration/deceleration (a "skip frequency" or "critical frequency avoidance" band) rather than allowing sustained operation at that specific speed — the most common and least invasive mitigation where the resonant speed is not required as a steady operating point.
2. **Stiffen the structure**, by adding bracing, gusseting, or additional foundation mass, where the resonant frequency is low enough that a modest stiffness increase shifts it clear of the operating range — this requires an engineering evaluation of the specific structure and is not a routine maintenance task.
3. **Add damping**, where neither avoidance nor stiffening is practical, to reduce the amplitude of the resonant response even if the natural frequency itself remains within the operating range — generally the least preferred option since it manages the symptom rather than removing the underlying coincidence.

A resonance condition should never be "corrected" by relaxing the `VIB_HIGH_05` alarm threshold per Section 3.5; doing so would mask the alarm without addressing the underlying structural condition, which typically continues to accelerate bearing and coupling wear at the resonant speed even if the vibration amplitude is no longer being reported as an active alarm.

## 6.7 Field Balancing Procedure (Single-Plane, In Situ)

Where a 1x running-speed vibration component is confirmed, per Section 6.3, to originate from imbalance on the driven blower side of the coupling rather than from the motor rotor or from misalignment, a single-plane field balancing procedure may be performed without removing the blower from service for a full shop balance:

1. Record baseline vibration amplitude and phase angle at the affected bearing housing at running speed.
2. Attach a trial weight of a known mass at a known radius on the accessible balance plane (typically the blower's outboard balance ring, per the blower manufacturer's procedure — this manual covers the motor-side vibration measurement and interpretation, not the blower-specific balance plane details, which are outside this manual's scope).
3. Re-run and record the resulting amplitude and phase change caused by the trial weight.
4. Calculate the correction weight and angular position required to bring the residual imbalance within the target vibration zone (ISO 10816-3 Zone A/B) using standard single-plane balancing vector calculation.
5. Install the calculated correction weight and re-verify the resulting vibration level before returning the unit to full continuous duty.

This procedure should only be performed by personnel trained in field balancing technique; an incorrectly calculated or installed correction weight can increase vibration rather than reduce it, and repeated trial-and-error balancing attempts subject the bearings to unnecessary additional stress from each intermediate, still-imbalanced running condition.

## 6.8 Vibration Trend Interpretation Across the Two-Unit Fleet

Because Motor-1 and Motor-2 are of identical construction, installed on comparable foundations, and normally run in parallel under similar load (Section 1.8), their vibration baselines established at commissioning (Section 2.11) should be broadly comparable to one another, and a meaningful divergence between the two over time is diagnostically useful in the same way described for temperature trending in Section 4.1 and Section 4.9:

- **Both units trending upward together**, at a similar rate and without either unit showing a clear spectral signature pointing to a specific mechanical cause (Section 4.6 Step 2), suggests a shared installation-level factor — for example, gradual foundation or grout degradation affecting both bays similarly, or a structural resonance condition (Section 6.6) that happens to affect both machine trains due to a shared structural element between Bay A and Bay B.
- **One unit trending upward while the other remains stable** under equivalent load points to a unit-specific cause on the diverging unit — misalignment (Section 6.2), a developing bearing condition (Section 3.3, `BRG_WEAR_07`), or a coupling insert nearing end of life (Section 6.5) — and should be investigated on that unit specifically rather than assumed to reflect a fleet-wide condition.
- **A step change on one unit coincident with a specific maintenance activity** (a bearing replacement, an alignment correction, a coupling insert replacement) should be evaluated against the expected direction of change: an alignment correction should reduce 1x/2x vibration components, and a step change in the wrong direction following such an activity indicates the corrective work itself may not have been completed correctly (see also the soft-foot-related alignment drift discussion in Section 6.4) rather than an unrelated new fault coincidentally appearing at the same time.

This two-unit comparison is a lower-resolution tool than the three-unit comparison available to the site's pump fleet (which additionally has an idle standby unit available for reference, see Section 1.8), and should be applied with correspondingly more caution — with only two continuously-loaded units to compare, a shared fleet-wide effect and a coincidental simultaneous unit-specific fault on both machines cannot always be distinguished from vibration trend data alone, and may require the additional context of maintenance history (Section 5.10) or a direct physical inspection of both units to resolve.

## 6.9 Vibration Measurement Locations and Directions

Consistent measurement location and direction is a precondition for any of the trend comparisons described elsewhere in this manual (Section 4.1, Section 4.9, Section 6.8) — a vibration reading taken from a slightly different point on the bearing housing, or in a different direction, is not reliably comparable to a prior reading even on the same unit. The MotorGuard permanently-mounted accelerometers (Section 1.6) fix this problem for continuous monitoring by measuring from the same physical location at all times, but any supplementary handheld measurement (for example, during the Section 4.6 investigation or a Section 6.7 field balancing procedure) must follow the same convention to remain comparable to the permanently-mounted sensor data:

| Location | Directions Measured | Primary Use |
|---|---|---|
| Drive-end (DE) bearing housing | Horizontal, vertical, axial | Primary location for coupling-side rotor-dynamic conditions (imbalance, misalignment); axial direction specifically useful for distinguishing misalignment (elevated axial component) from pure imbalance (predominantly radial) |
| Non-drive-end (NDE) bearing housing | Horizontal, vertical, axial | Secondary location; a DE/NDE amplitude ratio that shifts over time can itself be diagnostic of a developing condition localized to one bearing |
| Motor frame (mid-span, if a supplementary reading is taken) | Horizontal only, typically | Used only to help distinguish a bearing-housing-localized condition from a broader structural resonance response (Section 6.6) affecting the whole frame |

Horizontal readings are generally the most sensitive to imbalance and misalignment on a horizontally-mounted machine of this type, since the mounting arrangement is typically stiffer in the vertical direction; vertical readings that are unexpectedly high relative to horizontal readings at the same location can themselves be a useful clue pointing toward a foundation or soft-foot condition (Section 6.4) rather than a purely rotor-dynamic cause. Axial readings, while normally the lowest-amplitude of the three directions on a healthy machine, are disproportionately informative for angular misalignment specifically, and a rising axial trend with stable horizontal and vertical readings should be treated as a stronger misalignment indicator than an equivalent rise in the horizontal or vertical direction alone.

---

# Section 7: Appendix A — Safety & Compliance

## A.0 How to Use This Appendix

This appendix is organized to be read in two ways. Read sequentially (A.1 through A.10), it functions as a general safety and compliance reference for anyone new to the Motor-1/Motor-2 installation. Read selectively via the cross-reference index in Section A.8, it functions as a fast lookup during an active alarm event — for example, a technician responding to an active `INSUL_FAIL_06` alarm can go directly from Section 3.3 or Section 4.7 to the electrical safety guidance in Section A.5 without reading the full appendix in order. Both uses are intentional, which is why safety-critical guidance (lockout/tagout in Section A.3, PPE in Section A.4, emergency procedures in Section A.7) is written to stand on its own rather than assuming the reader has already absorbed every preceding subsection.

## A.1 Applicable Standards Framework

The MX-2200 Series and its associated MotorGuard control system are designed with reference to the following general classes of industrial standards. This manual is a synthetic reference document and does not itself constitute a certificate of compliance; site-specific compliance documentation should be maintained separately in the plant's regulatory record.

- General rotating electrical machine safety practice consistent with IEC 60034-series principles
- Vibration severity classification per ISO 10816-3, as referenced throughout Sections 3, 4, and 6 for `VIB_HIGH_05`, `BRG_WEAR_07`, and `MISALIGN_15`
- Rotor balance quality classification per ISO 21940, as referenced in Section 6.3
- Electrical area classification and equipment protection consistent with IEC 60079-series principles, where the installation area classification requires it
- General machinery safety and guarding principles consistent with ISO 12100
- Lockout/tagout practice consistent with generally accepted hazardous energy control principles (site-specific procedures govern; the outline in Section A.3 is a minimum baseline, not a replacement for the site's own LOTO program)

## A.2 General Safety Precautions

The following hazards are present on Motor-1 and Motor-2 and must be considered before any inspection, maintenance, or troubleshooting activity described elsewhere in this manual:

- **Rotating equipment.** The coupling, shaft, and any exposed portion of the drive train present an entanglement hazard whenever the unit is running or capable of starting. Never remove the coupling guard (Section 2.6, Section 6.2) while the unit is running or while an automatic start is possible.
- **Hot surfaces.** Frame and bearing housing surfaces can exceed safe touch temperatures during normal operation, particularly near the 85 °C `BRG_TEMP_02` Warning threshold (Section 3.3), and remain hot for a period after shutdown.
- **Electrical hazards.** The 400 V motor supply, VFD, and auxiliary cooling fan circuit present electrical shock and arc-flash hazards. All electrical work must be performed only by personnel qualified and authorized for the applicable voltage class, following the site's electrical safety program — this is particularly relevant for `INSUL_FAIL_06` (Section 4.7) investigation, which involves direct electrical testing of the stator winding.
- **Stored electrical energy.** VFD internal DC bus capacitors and, in some fault conditions, the stator winding itself can retain hazardous voltage after the supply disconnect is opened; see Section A.5 for the specific discharge time and testing requirements before any internal work.
- **Rotating machinery noise.** Sound pressure levels up to 82 dB(A) at 1 m (Section 1.4) require hearing protection per the site's general PPE program during any extended presence near a running unit.

## A.3 Lockout/Tagout Procedure (Baseline)

Before any activity requiring physical access to the motor, coupling, bearing housing, terminal box, or associated electrical circuits described in Sections 2, 4, or 5 of this manual, the following minimum hazardous energy control sequence applies. This baseline must be supplemented with the site's own documented LOTO procedure, which takes precedence where more stringent.

1. Notify affected operations personnel of the intended isolation and its expected duration.
2. Stop the unit through normal control means (not via the Emergency Stop, which is reserved for the conditions in Section A.7) and confirm zero speed.
3. Isolate and lock out the electrical supply at the motor control cabinet disconnect, applying a personal lock and tag. Isolate the auxiliary cooling fan's independent supply separately, since it is fed from a different circuit than the main motor supply (Section 2.5).
4. Verify zero energy state directly at the point of work: confirm zero voltage at the motor terminals with a rated voltage tester before beginning any electrical work, and attempt a start from the local HMI to confirm no response before beginning any mechanical work.
5. Where internal VFD panel work is required, observe the drive manufacturer's specified DC bus discharge time in addition to the external disconnect lockout, per Section A.5.
6. On completion of work, remove locks and tags only in reverse order, and only by the person who applied each lock (or per the site's authorized alternate-removal procedure), followed by the restart authorization sequence in Section A.7.

## A.4 Personal Protective Equipment Requirements

| Activity | Minimum PPE |
|---|---|
| General area walk-down (Section 5.2 daily checks) | Standard site PPE (hard hat, safety glasses, hearing protection near running units per the 82 dB(A) rating in Section 1.4) |
| Direct contact with running or recently stopped unit | Add insulated/heat-resistant gloves |
| Bearing housing disassembly (Section 4.3, 5.6) | Add face shield and mechanical-hazard gloves |
| Electrical panel, terminal box, or VFD work (Sections 2.5, 2.7, A.5) | Arc-flash rated PPE per the site electrical safety program and the panel's calculated incident energy category |
| Insulation resistance / ground-fault testing (Section 4.7) | Arc-flash rated PPE plus insulated tools rated for the test voltage used |

## A.5 Hazardous Energy Sources Specific to This Equipment

- **VFD DC bus residual voltage.** VFD internal capacitors can retain hazardous voltage for a period after the disconnect is opened; follow the drive manufacturer's specified discharge time before internal VFD panel work, in addition to the external disconnect lockout in Section A.3.
- **Residual stator winding charge.** Following certain insulation resistance test procedures (Section 4.7), the winding itself can retain a capacitive charge; discharge the winding to ground per the megohmmeter manufacturer's procedure before disconnecting test leads or handling terminals.
- **Auxiliary cooling fan independent supply.** Because the auxiliary fan (Section 1.3, Section 2.5) is fed from a separate circuit from the main motor, isolating the main motor supply alone does not de-energize the fan; both circuits must be locked out per Section A.3 Step 3 before any work near the fan.
- **Stored mechanical energy in a partially disassembled coupling.** Where a coupling insert is compressed or under tension during removal (Section 6.5), follow the coupling manufacturer's disassembly procedure to avoid a sudden release of stored mechanical energy.

## A.6 Guarding and Access

- The coupling guard (Section 2.6, Section 6.2) is a fixed safety guard and must never be operated with it removed or displaced, including for brief diagnostic purposes such as visual coupling inspection while running — use the vibration and thermal instrumentation described in Sections 3 and 4 for running diagnostics instead of visual/physical access to the coupling.
- Access to Bay A and Bay B should respect the clearance envelope in Section 2.2, which serves a dual purpose of maintenance access and safe separation between personnel and the adjacent operating unit during any single-unit maintenance activity.

## A.7 Emergency Procedures

**Emergency Stop (`ESTOP_ACT_18`, Section 3.3):** Any person observing an immediate hazard — abnormal noise suggesting imminent mechanical failure, visible smoke or arcing, or a person at risk of contact with rotating or energized equipment — should activate the local E-Stop pushbutton without waiting for supervisory approval. Following any E-Stop activation:

1. Do not reset the E-Stop or attempt a restart until the cause has been positively identified, per the guidance already given for `ESTOP_ACT_18` in Section 3.3.
2. Treat the unit as under lockout (Section A.3) for the duration of the investigation, even though the E-Stop itself is a separate protective function from the electrical disconnect lockout.
3. Restart authorization following any Safety-severity event requires sign-off from the site reliability engineer or designated safety authority, not solely the technician who investigated the cause.

**Confirmed ground fault (`INSUL_FAIL_06`):** Treat as an electrical safety event per Section 4.7 Step 2. Lock out and tag out the unit before any further work, and notify qualified electrical personnel; do not attempt a restart under any circumstances until the winding has been tested and cleared by qualified electrical personnel.

## A.7a Arc-Flash and Electrical Safety Program Interface

The electrical panel and terminal box work described in Sections 2.5, 2.7, and 4.7 of this manual must be performed within the boundaries of the site's own arc-flash hazard analysis and electrical safety program, which this manual does not replace or supersede. Specifically:

- The arc-flash PPE category referenced in Section A.4 for a given panel or terminal box is determined by the site's arc-flash study for that specific piece of equipment, not by a fixed value in this manual, since incident energy depends on upstream protective device settings and available fault current that are specific to the installation and can change if upstream equipment is modified.
- Arc-flash labeling on the motor control cabinets for Motor-1 and Motor-2 should be treated as authoritative for PPE category at the time of any electrical work; if this manual's general guidance in Section A.4 appears inconsistent with the current label, the label and the site's underlying study take precedence, and the discrepancy should be reported for correction of whichever document is out of date.
- Any modification to the electrical distribution upstream of Motor-1 or Motor-2 — a breaker setting change, a transformer resizing, or similar — should trigger a review of the arc-flash study for both units' panels, since such changes can alter available fault current and therefore the required PPE category, independent of anything described in this manual.

## A.8 Cross-Reference Index

The table below consolidates every alarm code introduced in Section 3 with the primary manual locations where it is discussed, to support rapid navigation during an active event.

| Code | Section 3 (Summary) | Section 4 (Full Procedure) | Other References |
|---|---|---|---|
| `WIND_TEMP_01` | 3.3 | 4.2 | Section 2.13 (RTD wiring pitfall), Section 4.9 |
| `BRG_TEMP_02` | 3.3 | 4.3 | Section 6.2 (alignment), Section 5.7 (lubrication) |
| `OVLD_CUR_03` | 3.3 | 4.4 | Section 2.12 (VFD current limit) |
| `PH_LOSS_04` | 3.3 | 4.5 | Section 1.7 (supply conditions) |
| `VIB_HIGH_05` | 3.3 | 4.6 | Section 6 (full alignment/balance/resonance discussion) |
| `INSUL_FAIL_06` | 3.3 | 4.7 | Section 2.1 (pre-installation test), Section A.5 |
| `BRG_WEAR_07` | 3.3 | — | Section 5.6 (bearing full inspection), Section 4.9 |
| `LUBE_LOW_08` | 3.3 | — | Section 5.7 (lubrication schedule) |
| `VFD_FAULT_09` | 3.3 | — | Section 2.12 (VFD parameters) |
| `SENSOR_FAIL_10` | 3.3 | — | Section 4.1 (general diagnostic principle) |
| `LOCKED_ROTOR_11` | 3.3 | 4.8 | Section 1.9 (starting characteristics) |
| `OVERSPEED_12` | 3.3 | — | Section 2.12 (VFD maximum frequency) |
| `UNDERVOLT_13` | 3.3 | — | Section 1.7 (supply tolerance) |
| `STARTS_EXCEED_14` | 3.3 | — | Section 1.7, Section 2.12 (starts-per-hour) |
| `MISALIGN_15` | 3.3 | — | Section 6.2 (alignment methodology) |
| `RESONANCE_16` | 3.3 | — | Section 6.6 (resonance identification/mitigation) |
| `MOISTURE_ING_17` | 3.3 | — | Section 2.9 (pre-start insulation check) |
| `ESTOP_ACT_18` | 3.3 | — | Section A.7 (emergency procedures) |
| `ENCODER_FAULT_19` | 3.3 | — | Section 4.8 (locked rotor cross-check) |
| `COOLING_FAN_20` | 3.3 | — | Section 1.3, Section 4.9 (cooling deficiency pathway) |

## A.9 Compliance Statement and Disclaimer

This manual, including all equipment identifiers (Motor-1, Motor-2; tags M-201/M-202; serial numbers MM-2200-2001/2002), the MX-2200 Series model designation, the MotorGuard controller platform, and all specification values, alarm codes, and procedures contained herein, is a fully synthetic reference document prepared for demonstration, testing, and documentation-tooling purposes. It does not describe a real commercially available product, is not associated with any real manufacturer, and must not be relied upon as an actual equipment manual, safety certification, or regulatory compliance record for any physical installation. Any resemblance to a real product's specifications, alarm nomenclature, or procedures is coincidental.

## A.10 Training and Competency Requirements

| Activity | Minimum Competency |
|---|---|
| Daily/weekly visual checks (Sections 5.2, 5.3) | General site safety orientation; no specialized motor training required |
| Routine lubrication (Section 5.4, 5.5) | Site-authorized maintenance technician, LOTO-qualified per Section A.3 |
| Alarm investigation per Section 4 procedures | Site-authorized maintenance technician with documented familiarity with this manual's alarm codes (Section 3) and the specific procedure being followed |
| Laser alignment and field balancing (Section 6) | Technician trained specifically on the site's laser alignment system and, for field balancing, on vector balancing calculation |
| Insulation resistance / ground-fault testing (Section 4.7) | Personnel qualified and authorized for the applicable voltage class per the site electrical safety program |
| Electrical panel and VFD work (Sections 2.5, 2.7) | Personnel qualified and authorized for the applicable voltage class, with specific VFD/drive training |
| Restart authorization following a Critical auto-trip | Site-authorized maintenance technician who performed or directly verified the corrective action |
| Restart authorization following a Safety-severity event (`ESTOP_ACT_18`) or confirmed ground fault (`INSUL_FAIL_06`) | Site reliability engineer or designated safety authority only, per Section A.7 |
| Threshold or configuration changes (Section 3.5) | Site reliability engineer approval required regardless of who performs the technical change |

---

# Section 8: Glossary of Terms and Abbreviations

| Term | Definition |
|---|---|
| Balance grade (ISO 21940) | A classification of the maximum permissible residual rotor imbalance for a given machine speed; the MX-2200 Series rotor is balanced to Grade G2.5, see Section 1.3 and Section 6.3 |
| Bearing defect frequency | A vibration frequency component calculated from bearing geometry, used to detect bearing wear before it produces a general overall-amplitude alarm; see `BRG_WEAR_07` |
| CMMS | Computerized Maintenance Management System — the site's system of record for maintenance history, referenced throughout Section 5 |
| Cold alignment | A shaft alignment measurement taken at ambient (non-running) temperature, before thermal growth compensation is applied; see Section 6.2 |
| DCS | Distributed Control System — the plant-level control system to which MotorGuard alarms are forwarded per Section 1.6 |
| DE / NDE | Drive End / Non-Drive End — the two bearing locations on the motor shaft, each independently monitored per Section 1.6 |
| Ground fault | A fault condition in which the stator winding insulation has failed sufficiently to allow current to flow to the frame or ground; see `INSUL_FAIL_06` |
| Historian | The time-series database within the MotorGuard system that stores instrument readings and alarm events for trend analysis |
| HMI | Human-Machine Interface — the local operator display on each MotorGuard controller |
| Hot alignment | A shaft alignment measurement taken after the machine train has reached thermal equilibrium at operating speed, used to verify cold-alignment thermal growth compensation; see Section 6.2 |
| IP55 | An ingress protection rating indicating protection against dust ingress (limited) and low-pressure water jets, applicable to the motor enclosure and terminal box per Section 1.4 |
| ISO 10816-3 | The international standard used to classify mechanical vibration severity into zones (A through D) for industrial machinery |
| Locked rotor | A condition in which the motor rotor fails to turn despite a start command and applied voltage, drawing very high current; see `LOCKED_ROTOR_11` and Section 1.9 |
| LOTO | Lockout/Tagout — the hazardous energy control procedure outlined in Section A.3 |
| Megohmmeter | A test instrument used to measure winding insulation resistance to ground; see Section 4.7 |
| Modbus RTU / TCP | Industrial communication protocols used between the VFD, MotorGuard controller, and plant DCS |
| MotorGuard™ | The local controller platform monitoring and protecting each of Motor-1 and Motor-2, described in Section 1.6 |
| Polarization index | The ratio of a 10-minute to 1-minute insulation resistance reading, used to distinguish surface contamination from true insulation aging; see Section 4.7 Step 6 |
| Pt100 RTD | A platinum resistance temperature detector with a nominal 100-ohm resistance at 0 °C, used for bearing and winding temperature monitoring |
| Soft foot | A condition in which one or more motor mounting feet does not sit flush against the baseplate, causing frame distortion when bolts are torqued; see Section 6.4 |
| Structural resonance | A condition in which a structural natural frequency coincides with running speed or a multiple of it, producing a vibration signature independent of speed; see `RESONANCE_16` and Section 6.6 |
| Trend-based alarm | An alarm code (`BRG_WEAR_07`, `LUBE_LOW_08`, `MISALIGN_15`) raised from analysis of a value's change over time rather than a single instantaneous threshold crossing |
| VFD | Variable Frequency Drive — the motor speed control device described in Sections 1.3, 2.7, and 2.12 |

---

# Section 9: Document Revision History

| Revision | Summary of Changes |
|---|---|
| A | Initial issue covering Motor-1 only, prior to Motor-2 installation |
| B | Expanded to cover both units following Motor-2 commissioning; added full Alarm Code Matrix (Section 3) |
| C (current) | Added detailed troubleshooting procedures (Section 4), Mechanical Alignment & Balancing section (Section 6), and expanded Safety & Compliance appendix (Section 7) with full cross-reference index |

*End of MechMind MX-2200 Series Technical Reference & Operations Manual — Manual Number MM-TM-2200-REV-C.*
