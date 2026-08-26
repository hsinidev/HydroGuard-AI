# HydroGuard AI

## System Architecture & Product Blueprint

### Hackathon-Ready Technical Specification

**Project type:** AI Agent + Industrial Pump Condition Monitoring + Predictive Maintenance Platform

**Primary domain:** Industrial hydraulic pumping stations, multistage centrifugal pumps, vibration diagnostics, cavitation detection, hydraulic performance monitoring, and maintenance optimization

**Target users:** Maintenance engineers, rotating-equipment engineers, reliability engineers, instrumentation technicians, pump operators, plant maintenance teams, and industrial service companies

**Primary differentiator:** HydroGuard AI combines real-time industrial telemetry, deterministic hydraulic calculations, frequency-domain vibration analysis, agentic diagnosis, engineering knowledge, and maintenance workflow automation rather than presenting a generic AI monitoring dashboard.

---

# 1. Executive Summary

HydroGuard AI is an AI-powered industrial maintenance and diagnostic system designed to protect **multistage centrifugal pumps** from:

- Cavitation
- Hydraulic instability
- Pump impeller problems
- Vibration abnormalities
- Shaft misalignment
- Mechanical seal degradation
- Bearing overheating
- Suction-pressure problems
- Abnormal pump efficiency
- Progressive equipment degradation

The system continuously receives industrial telemetry from pumping stations through:

- Modbus TCP
- OPC UA
- MQTT Sparkplug B

The platform combines:

- Suction pressure
- Discharge pressure
- Flow
- Vibration
- Bearing temperature
- Pump speed
- Electrical power
- Operating state
- Historical maintenance information

The AI does not simply display sensor values.

It conducts a structured condition-investigation workflow.

A typical investigation is:

1. Telemetry enters the ingestion layer.
2. The system identifies the operating state of the pump.
3. Deterministic engineering calculations are executed.
4. Vibration signals are transformed into frequency-domain information.
5. FFT analysis searches for characteristic frequencies.
6. Hydraulic conditions are evaluated against NPSH requirements.
7. The diagnostic agent generates competing fault hypotheses.
8. Evidence is accumulated from multiple sensors.
9. The AI determines the most probable degradation mechanism.
10. The Safety Agent evaluates whether an intervention is safe.
11. The Work-Order Agent generates a maintenance recommendation.
12. The system produces an explainable maintenance report.
13. The complete case is stored in the pump's maintenance history.

The core product principle is:

> **Do not tell maintenance personnel to replace a component first. Determine what the telemetry proves, what could explain it, and what is the safest and most informative verification step.**

---

# 2. Problem Statement

Industrial pumping stations frequently operate continuously under demanding hydraulic conditions.

A pump may gradually deteriorate without producing an immediately obvious failure.

Possible symptoms include:

- Increasing vibration
- High-frequency acoustic/vibration energy
- Reduced discharge pressure
- Reduced flow
- Increasing motor power
- Increasing bearing temperature
- Mechanical seal leakage
- Reduced hydraulic efficiency
- Suction-pressure instability
- Periodic vibration peaks
- Impeller-related frequency components

Traditional maintenance approaches may detect the problem only after:

- Pump performance has significantly degraded
- Mechanical seals have failed
- Bearings have been damaged
- Impellers have suffered erosion
- Production has been interrupted
- Emergency maintenance is required

The challenge is therefore not merely collecting sensor data.

The challenge is determining:

> **What is happening inside the pump, why is it happening, how confident are we, and what should maintenance personnel do next?**

---

# 3. Product Vision

Create an AI assistant that behaves like an experienced industrial pump reliability engineer.

HydroGuard AI should:

- Understand pump operating conditions.
- Understand hydraulic measurements.
- Analyze vibration signals.
- Detect abnormal frequency components.
- Calculate NPSH available.
- Compare NPSH conditions against required values.
- Calculate instantaneous hydraulic efficiency.
- Detect abnormal operating regimes.
- Separate symptoms from probable causes.
- Generate competing fault hypotheses.
- Correlate pressure, vibration, temperature, flow, and power.
- Maintain diagnostic state.
- Explain evidence.
- Recommend safe verification steps.
- Generate maintenance work orders.
- Never claim certainty when evidence is insufficient.

---

# 4. Competitive Differentiation

HydroGuard AI should not be presented as:

- A generic AI chatbot.
- A simple IoT dashboard.
- A vibration graphing application.
- A generic predictive-maintenance platform.
- An LLM connected to pump sensors.
- A black-box anomaly detector.

Instead, position it as:

> **An agentic industrial pump diagnostic system that converts real-time hydraulic and vibration telemetry into evidence-driven maintenance decisions.**

The strongest differentiators are:

1. Hydraulic-domain reasoning.
2. Real-time industrial protocol integration.
3. Deterministic NPSH calculations.
4. Deterministic pump-efficiency calculations.
5. Frequency-domain vibration diagnostics.
6. Cavitation-focused analysis.
7. Vane Pass Frequency analysis.
8. Multi-sensor evidence correlation.
9. AI-generated fault hypotheses.
10. Maintenance work-order generation.
11. Explainable engineering evidence.
12. Safety-aware recommendations.
13. Historical asset intelligence.
14. Human-in-the-loop validation.

---

# 5. Primary Use Cases

## 5.1 Cavitation Detection

HydroGuard AI continuously evaluates:

- Suction pressure
- Vapor pressure
- Fluid density
- Flow velocity
- Pump operating condition
- NPSH available
- Vibration spectrum

The system searches for combinations indicating possible cavitation.

Example:

```text
Suction pressure decreasing
        +
NPSHa approaching NPSHr
        +
High-frequency vibration increasing
        +
1–5 kHz energy increasing
        +
Hydraulic efficiency decreasing
        =
HIGH CAVITATION RISK
```

The system should not rely on a single sensor.

It should correlate multiple independent evidence sources.

---

# 6. Example Diagnostic Investigation

## Scenario

Pump P-204 begins showing abnormal vibration.

### Step 1 — Establish operating context

HydroGuard asks:

- Which pump?
- Which pump stage configuration?
- Current flow?
- Current suction pressure?
- Current discharge pressure?
- Current rotational speed?
- Fluid temperature?
- Current operating mode?
- Has the condition appeared suddenly or progressively?

---

## Step 2 — Evaluate hydraulic conditions

The system calculates:

```text
NPSHa
Pump head
Hydraulic power
Pump efficiency
```

The system compares the operating point with expected pump behavior.

---

## Step 3 — Analyze vibration

The FFT Diagnostic Agent evaluates:

- Overall RMS vibration
- Peak vibration
- Frequency spectrum
- Dominant frequencies
- High-frequency energy
- Harmonics
- Vane Pass Frequency
- Rotational-frequency components

---

## Step 4 — Compare hypotheses

Possible hypotheses:

```text
H1: Cavitation
H2: Shaft misalignment
H3: Impeller degradation
H4: Mechanical seal degradation
H5: Bearing degradation
H6: Hydraulic operating-point instability
H7: Sensor anomaly
```

---

## Step 5 — Correlate evidence

Example:

```text
NPSHa ↓
High-frequency vibration ↑
1–5 kHz energy ↑
Suction pressure unstable
Pump efficiency ↓
```

The system increases the ranking of:

```text
Cavitation
```

---

## Step 6 — Recommend safe verification

The AI may recommend:

- Verify suction-side pressure measurement.
- Verify suction valve operating position.
- Confirm flow condition.
- Compare current NPSHa with pump requirements.
- Inspect vibration trend.
- Review pump operating point.
- Follow approved plant procedures before physical intervention.

---

## Step 7 — Generate maintenance action

The Work-Order Agent produces a structured recommendation.

Example:

```text
Priority: HIGH

Asset:
Pump P-204

Probable condition:
Cavitation risk

Evidence:
- Reduced NPSHa
- Increased high-frequency vibration
- Abnormal 1–5 kHz spectral energy
- Reduced hydraulic efficiency

Recommended action:
Investigate suction-side operating conditions and verify
the pump operating point against approved operating limits.

Safety:
Follow site-approved procedures before any physical intervention.
```

---

# 7. Core System Architecture

```text
                         ┌─────────────────────────────┐
                         │       Operator Interface    │
                         │ Web / Tablet / Mobile       │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │     HydroGuard Orchestrator  │
                         │   Diagnostic State Machine   │
                         └──────────────┬──────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
     ┌────────────────┐       ┌────────────────┐       ┌────────────────┐
     │ Ingestion Agent│       │ FFT Diagnostic │       │ Knowledge Agent│
     │                │       │ Agent          │       │                │
     └───────┬────────┘       └───────┬────────┘       └───────┬────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      ▼
                         ┌─────────────────────────────┐
                         │ Hydraulic Diagnostic Engine │
                         │ NPSH / Head / Efficiency    │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
                ┌──────────────────┐         ┌──────────────────┐
                │ Diagnostic Agent │         │ Safety Agent     │
                │ Hypotheses       │         │ Risk Evaluation  │
                └────────┬─────────┘         └────────┬─────────┘
                         │                            │
                         └──────────────┬─────────────┘
                                        ▼
                         ┌─────────────────────────────┐
                         │   Work-Order Agent          │
                         │ Maintenance Recommendation  │
                         └──────────────┬──────────────┘
                                        ▼
                         ┌─────────────────────────────┐
                         │ Diagnostic / Maintenance    │
                         │ Report + Evidence + Trend   │
                         └─────────────────────────────┘
```

---

# 8. Industrial Data Ingestion Architecture

HydroGuard AI should support three primary industrial communication mechanisms.

## 8.1 Modbus TCP

Default port:

```text
502
```

Potential data points:

```text
40001  Suction Pressure
40002  Discharge Pressure
40003  Flow
40004  Bearing Temperature
40005  Pump Speed
40006  Motor Power
40007  Pump Status
```

The actual register map must be configurable per installation.

---

## 8.2 OPC UA

Support:

```text
IEC 62541
```

OPC UA provides structured industrial telemetry and metadata.

HydroGuard should support:

- Node discovery
- Node subscriptions
- Data type validation
- Timestamp handling
- Quality/status information
- Historical values where available

---

## 8.3 MQTT Sparkplug B

HydroGuard should support industrial event and telemetry ingestion using:

```text
MQTT
+
Sparkplug B
```

The platform should understand:

- Edge nodes
- Devices
- Metrics
- Birth certificates
- Death certificates
- Metric timestamps
- Quality/status

---

# 9. Ingestion Agent

The Ingestion Agent is responsible for acquiring and normalizing telemetry.

Primary inputs:

- Pressure
- Flow
- Vibration
- Temperature
- Speed
- Power
- Pump state

For vibration channels, the target acquisition rate is:

```text
50 Hz
```

The architecture should nevertheless allow higher-rate acquisition in future deployments because frequency analysis requirements may exceed what a 50 Hz sampling rate can represent.

The ingestion pipeline should perform:

1. Protocol acquisition.
2. Timestamp normalization.
3. Unit normalization.
4. Sensor validation.
5. Quality checking.
6. Missing-value detection.
7. Range validation.
8. Buffering.
9. Storage.
10. Forwarding to diagnostic agents.

---

# 10. Sensor Architecture

## 10.1 Vibration Sensors

Primary sensor:

**Triaxial piezoelectric accelerometer**

Measurements:

```text
X-axis
Y-axis
Z-axis
```

Potential derived metrics:

- RMS acceleration
- Peak acceleration
- Crest factor
- Frequency spectrum
- Band energy
- Trend
- Axis correlation

---

## 10.2 Pressure Sensors

Inputs:

```text
Suction pressure
Discharge pressure
```

Typical instrumentation:

```text
4–20 mA
```

The system should preserve:

- Raw value
- Engineering value
- Unit
- Timestamp
- Sensor status
- Quality
- Source

---

## 10.3 Temperature Sensors

Bearing temperature should support:

```text
PT100 RTD
```

Potential monitoring:

- Absolute temperature
- Temperature rate of change
- Temperature differential
- Temperature trend
- Correlation with vibration

---

# 11. FFT Diagnostic Agent

The FFT Diagnostic Agent converts time-domain vibration data into frequency-domain evidence.

Pipeline:

```text
Raw vibration
      ↓
Signal validation
      ↓
Windowing
      ↓
FFT
      ↓
Frequency spectrum
      ↓
Peak detection
      ↓
Band analysis
      ↓
Feature extraction
      ↓
Diagnostic interpretation
```

The system should evaluate:

- Dominant frequency
- Harmonic structure
- Broadband energy
- High-frequency energy
- Rotational-frequency components
- Vane Pass Frequency
- Relevant pump-specific spectral signatures

---

# 12. Cavitation Frequency Analysis

HydroGuard should specifically monitor abnormal energy in the:

```text
1 kHz – 5 kHz
```

region identified by the project specification as relevant to cavitation diagnostics.

The system should not treat the presence of energy in this band as automatic proof of cavitation.

Instead:

```text
High-frequency energy
+
NPSHa deterioration
+
Suction instability
+
Hydraulic-performance degradation
+
Relevant operating condition
```

should collectively increase the cavitation hypothesis.

---

# 13. Vane Pass Frequency Analysis

For a centrifugal pump:

```text
VPF = Number of Impeller Vanes × Rotational Frequency
```

The system should calculate the expected VPF from:

- Pump rotational speed
- Number of impeller vanes

The FFT agent should then search for:

```text
VPF
2 × VPF
3 × VPF
...
```

and compare these components against baseline behavior.

Potential interpretation:

```text
Increasing VPF-related amplitude
+
Hydraulic performance degradation
=
Potential impeller / hydraulic abnormality
```

The result must remain an engineering hypothesis until verified.

---

# 14. Hydraulic Calculation Engine

Deterministic engineering calculations must be implemented outside the LLM.

The LLM should call validated calculation tools.

---

## 14.1 NPSH Available

HydroGuard calculates:

$$
NPSH_a =
\frac{P_{suction}-P_{vapor}}
{\rho g}
+
\frac{v_s^2}{2g}
$$

with the operating requirement:

$$
NPSH_a \geq NPSH_r
$$

The calculation engine should return:

```text
NPSHa
NPSHr
Margin
Margin percentage
Risk state
```

Example:

```text
NPSHa = 4.8 m
NPSHr = 4.2 m
Margin = 0.6 m

Status:
Reduced safety margin
```

---

# 15. Pump Efficiency Engine

Instantaneous pump efficiency:

$$
\eta =
\frac{\rho g Q H}
{P_{electrical}}
\times 100
$$

Inputs:

```text
ρ = Fluid density
g = Gravitational acceleration
Q = Flow
H = Pump head
Pelectrical = Electrical power
```

Outputs:

```text
Hydraulic head
Hydraulic power
Electrical power
Instantaneous efficiency
Baseline efficiency
Efficiency deviation
```

The AI should use this deterministic result as evidence rather than performing the calculation internally.

---

# 16. Pump Head Calculation

The system should support pressure-based head calculation.

Conceptually:

```text
Pressure differential
        ↓
Density correction
        ↓
Velocity-head correction
        ↓
Pump head
```

The calculation module should support installation-specific elevation and pressure-reference configuration.

---

# 17. Diagnostic Reasoning Engine

This is the core intelligence layer.

HydroGuard represents the problem as competing hypotheses.

Example:

```text
H1: Cavitation
H2: Shaft misalignment
H3: Impeller degradation
H4: Mechanical seal degradation
H5: Bearing degradation
H6: Suction restriction
H7: Hydraulic operating-point instability
H8: Sensor fault
```

Each new observation updates the ranking.

Example:

```text
Initial:

H1 Cavitation              20%
H2 Misalignment            15%
H3 Impeller degradation    15%
H4 Seal degradation        10%
H5 Bearing degradation     15%
H6 Suction restriction     10%
H7 Hydraulic instability   10%
H8 Sensor fault             5%
```

After NPSHa decreases:

```text
H1 Cavitation              ↑
H6 Suction restriction     ↑
H7 Hydraulic instability   ↑
```

After high-frequency energy increases:

```text
H1 Cavitation              ↑↑
H5 Bearing degradation     ↑
```

After VPF-related energy increases:

```text
H3 Impeller degradation    ↑
```

These percentages are **AI-generated confidence estimates**, not statistical probabilities unless statistically validated.

---

# 18. Evidence Model

HydroGuard should explicitly distinguish:

## OBSERVED

Directly measured or received from industrial telemetry.

Example:

```text
Suction pressure = X
Discharge pressure = Y
Bearing temperature = Z
```

## CALCULATED

Generated by deterministic engineering functions.

Example:

```text
NPSHa = X m
Efficiency = Y %
VPF = Z Hz
```

## INFERRED

Generated by diagnostic reasoning.

Example:

```text
Cavitation is the leading hypothesis.
```

## NOT CONFIRMED

Actions or conclusions that still require verification.

Example:

```text
Impeller replacement is NOT confirmed.
```

This distinction is essential for preventing AI overconfidence.

---

# 19. Next-Best-Measurement Engine

One of HydroGuard's strongest features should be the ability to determine which additional measurement provides the greatest diagnostic value.

Candidate actions:

```text
1. Verify suction pressure
2. Verify discharge pressure
3. Verify flow
4. Check bearing temperature
5. Capture another vibration window
6. Inspect vibration spectrum
7. Verify pump speed
8. Verify suction valve condition
9. Compare current efficiency with baseline
10. Review historical trend
```

The engine optimizes for:

- Diagnostic information gain
- Measurement availability
- Technician effort
- Equipment risk
- Operational impact
- Safety

---

# 20. Safety Agent

Safety must be a first-class subsystem.

HydroGuard must never behave as though an AI recommendation automatically authorizes physical intervention.

The Safety Agent should:

- Detect hazardous interventions.
- Display appropriate warnings.
- Encourage approved site procedures.
- Require qualified personnel for physical interventions.
- Avoid unsafe valve manipulation instructions where site conditions are unknown.
- Never recommend bypassing protective systems.
- Never disable safety instrumentation.
- Escalate high-risk conditions.
- Distinguish monitoring from physical intervention.

The system is:

> **A maintenance decision-support system, not a safety authority.**

---

# 21. Valve Recommendation Boundary

The project specification includes recommending adjustment of suction-valve angle to avoid NPSHa degradation.

This must be implemented carefully.

HydroGuard should not blindly command a valve.

Instead:

```text
Hydraulic analysis
      ↓
NPSHa assessment
      ↓
Risk evaluation
      ↓
Recommended operating adjustment
      ↓
Human approval
      ↓
Approved site procedure
```

For the MVP:

**READ-ONLY FIRST.**

The system may recommend:

> Investigate suction-side operating conditions and consider an approved adjustment according to site operating procedures.

It should not directly actuate the valve.

---

# 22. Work-Order Agent

The Work-Order Agent converts diagnostic conclusions into structured maintenance actions.

Output:

```text
Work Order ID
Asset
Priority
Detected condition
Evidence
Probable cause
Recommended inspection
Recommended action
Safety requirements
Required skills
Required tools
Suggested spare parts
Estimated urgency
Evidence references
```

Example:

```text
WO-HG-00241

Asset:
Pump P-204

Priority:
High

Condition:
Elevated cavitation risk

Evidence:
- NPSHa margin reduced
- High-frequency vibration increased
- Suction pressure unstable
- Efficiency decreased

Recommended work:
Inspect suction-side operating conditions and verify pump
operation against approved operating limits.

Verification:
Collect vibration spectrum and hydraulic measurements after
corrective action.

Safety:
Follow approved site maintenance and isolation procedures.
```

---

# 23. Knowledge Agent

Knowledge sources:

- Pump OEM manuals
- API 610 documentation
- ISO standards
- Pump curves
- Equipment datasheets
- Site operating procedures
- Maintenance procedures
- Vibration baseline documentation
- Historical work orders
- Engineering reports

The system should use RAG.

Knowledge must be categorized as:

```text
Verified documentation
General engineering knowledge
Site-specific procedure
Sensor observation
Calculated engineering value
AI inference
```

---

# 24. RAG Architecture

```text
OEM Manuals
      │
Pump Datasheets
      │
Site Procedures
      │
Maintenance History
      │
Standards
      │
      ▼
Document Ingestion
      │
      ▼
Parsing
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
Vector Database
      │
      ▼
Retriever
      │
      ▼
Knowledge Agent
      │
      ▼
Diagnostic Agent
```

Every retrieved source should retain:

- Document name
- Page
- Section
- Equipment
- Pump model
- Revision
- Version
- Source identifier

---

# 25. Hallucination Prevention

HydroGuard must separate:

### KNOWN

Directly supplied by trusted documentation or telemetry.

### OBSERVED

Measured by sensors or explicitly provided by operators.

### CALCULATED

Produced by deterministic engineering functions.

### INFERRED

AI-generated hypothesis.

### NOT CONFIRMED

Claims that require additional verification.

Example:

```text
OBSERVED:
Suction pressure has decreased.

CALCULATED:
NPSHa = 4.3 m.

OBSERVED:
High-frequency vibration energy has increased.

INFERRED:
Cavitation is a leading hypothesis.

NOT CONFIRMED:
Impeller damage has occurred.
```

---

# 26. Explainability

Every diagnosis should contain:

## Diagnosis

Most probable condition.

## Evidence

Measurements and calculations supporting the hypothesis.

## Contradicting Evidence

Evidence that does not fit.

## Confidence

AI confidence estimate.

## Engineering Calculations

Relevant deterministic results.

## Next Verification

Safest useful confirmation.

## Alternatives

Other plausible causes.

Example:

```text
Diagnosis:
Cavitation risk

Confidence:
High

Supporting evidence:
- Reduced NPSHa margin
- Increased 1–5 kHz vibration energy
- Suction-pressure instability
- Reduced hydraulic efficiency

Alternative:
Suction-side restriction

Next verification:
Verify suction pressure, flow and approved operating
conditions before physical intervention.
```

---

# 27. Baseline Engine

HydroGuard should maintain a baseline for every pump.

Baseline dimensions may include:

```text
Flow
Pressure
Head
Efficiency
Vibration RMS
Frequency spectrum
Bearing temperature
Power
Speed
```

Baseline should be associated with operating state.

For example:

```text
Pump P-204

Operating condition:
75% design flow

Expected:
Efficiency = X
Vibration RMS = Y
Bearing temperature = Z
```

This avoids comparing fundamentally different operating conditions.

---

# 28. Time-Series Architecture

The platform should maintain:

```text
Raw telemetry
        ↓
Normalized telemetry
        ↓
Feature extraction
        ↓
Time-series storage
        ↓
Trend engine
        ↓
Diagnostic engine
```

Important trends:

- Vibration trend
- NPSHa trend
- Efficiency trend
- Bearing temperature trend
- Suction pressure trend
- Discharge pressure trend
- Flow trend
- Power trend

---

# 29. Data Model

Core entities:

```text
User
Operator
Plant
PumpStation
Pump
PumpStage
Impeller
Bearing
MechanicalSeal
Sensor
SensorReading
VibrationWindow
FFTAnalysis
PressureMeasurement
FlowMeasurement
TemperatureMeasurement
OperatingState
NPSHCalculation
EfficiencyCalculation
Fault
Hypothesis
DiagnosticEvent
MaintenanceEvent
WorkOrder
Document
AIReport
```

Relationship:

```text
Plant
 └── PumpStation
      └── Pump
           ├── Stages
           ├── Impeller
           ├── Bearings
           ├── Mechanical Seal
           ├── Sensors
           ├── Telemetry
           ├── Vibration Analyses
           ├── Faults
           ├── Maintenance History
           └── Work Orders
```

---

# 30. Recommended Technology Stack

## Frontend

Recommended:

- React
- Next.js
- TypeScript
- Tailwind CSS

Interface requirements:

- Industrial dashboard
- Real-time pump status
- Hydraulic measurements
- Vibration spectrum
- NPSH visualization
- Efficiency visualization
- Alarm states
- Diagnostic timeline
- Hypothesis panel
- Work-order panel
- Evidence panel

---

# 31. Backend

Recommended:

- Python
- FastAPI
- AsyncIO
- Pydantic

Backend responsibilities:

- API
- Agent orchestration
- Telemetry ingestion
- Calculations
- FFT processing
- Diagnostic state
- Work-order generation
- RAG
- Authentication
- Audit logging

---

# 32. AI Layer

Possible implementation:

```text
Multimodal LLM
Agent orchestration framework
Embeddings
RAG
Tool calling
Structured outputs
```

The LLM should not own deterministic engineering calculations.

Instead:

```text
LLM
 ↓
Tool Call
 ↓
Validated Engineering Function
 ↓
Result
 ↓
LLM Interpretation
```

---

# 33. Database

MVP:

```text
PostgreSQL
```

Potential extensions:

```text
pgvector
Time-series extension
```

The database should separate:

- Asset metadata
- Telemetry
- Calculated features
- Diagnostic cases
- Maintenance events
- Documents

---

# 34. Storage

Potential:

```text
Object Storage
```

Used for:

- Vibration datasets
- FFT snapshots
- Reports
- Pump documentation
- Images
- Maintenance documents

---

# 35. Deployment Architecture

```text
Operator
   │
   ▼
Next.js Frontend
   │
   ▼
API Gateway
   │
   ▼
FastAPI Backend
   │
   ▼
HydroGuard Orchestrator
   │
   ├── AI Model
   ├── Ingestion Agent
   ├── FFT Agent
   ├── Hydraulic Engine
   ├── Diagnostic Engine
   ├── Knowledge Agent
   ├── Safety Agent
   └── Work-Order Agent
          │
          ├── PostgreSQL
          ├── Vector Store
          ├── Time-Series Storage
          └── Object Storage

Industrial Layer
   │
   ├── Modbus TCP :502
   ├── OPC UA
   └── MQTT Sparkplug B
```

---

# 36. Industrial Gateway Architecture

For real deployments:

```text
Pump Sensors
     │
     ▼
PLC / RTU / Industrial Gateway
     │
     ├── Modbus TCP
     ├── OPC UA
     └── MQTT Sparkplug B
     │
     ▼
HydroGuard Edge Connector
     │
     ▼
Secure Cloud / On-Prem Backend
```

The architecture should allow future edge deployment so critical telemetry does not depend entirely on cloud connectivity.

---

# 37. Agent Architecture

## 37.1 Orchestrator Agent

Responsibilities:

- Understand current pump condition.
- Maintain diagnostic state.
- Select specialist agents.
- Coordinate tool calls.
- Determine next diagnostic step.
- Stop investigation when sufficient evidence exists.

---

## 37.2 Ingestion Agent

Responsible for:

- Protocol connectivity.
- Telemetry normalization.
- Data validation.
- Timestamping.
- Sensor-quality handling.

---

## 37.3 FFT Diagnostic Agent

Responsible for:

- Vibration preprocessing.
- FFT.
- Spectral peak detection.
- Band analysis.
- VPF analysis.
- High-frequency analysis.
- Vibration feature extraction.

---

## 37.4 Hydraulic Diagnostic Agent

Responsible for:

- NPSHa.
- NPSH margin.
- Pump head.
- Hydraulic power.
- Efficiency.
- Operating-point analysis.

---

## 37.5 Diagnostic Agent

Responsible for:

- Fault hypotheses.
- Evidence correlation.
- Hypothesis ranking.
- Root-cause reasoning.
- Next-best-measurement selection.

---

## 37.6 Knowledge Agent

Responsible for:

- Documentation retrieval.
- OEM guidance.
- Site procedures.
- Standards.
- Historical maintenance evidence.

---

## 37.7 Safety Agent

Responsible for:

- Intervention risk.
- Operating limits.
- Unsafe action detection.
- Escalation.
- Human approval requirements.

---

## 37.8 Work-Order Agent

Responsible for:

- Maintenance recommendation.
- Work-order creation.
- Priority.
- Required verification.
- Evidence packaging.

---

# 38. Tool Layer

Suggested tools:

```text
read_modbus()
read_opcua()
read_mqtt()
get_sensor_state()
get_pump_state()
get_historical_telemetry()
capture_vibration_window()
calculate_fft()
detect_vibration_peaks()
calculate_npsha()
calculate_npsh_margin()
calculate_pump_head()
calculate_efficiency()
calculate_vpf()
search_manuals()
search_maintenance_history()
check_operating_limits()
run_fault_analysis()
safety_check()
generate_work_order()
generate_report()
```

For the hackathon MVP, industrial interfaces may initially be simulated APIs.

---

# 39. Deterministic Engineering Tool Contract

Every engineering calculation should return structured data.

Example:

```json
{
  "calculation": "NPSHa",
  "value": 4.8,
  "unit": "m",
  "inputs": {
    "suction_pressure": 185000,
    "vapor_pressure": 4200,
    "density": 998,
    "velocity": 2.1
  },
  "status": "VALID",
  "timestamp": "2026-08-26T10:15:00Z"
}
```

The LLM interprets the result.

It should not silently replace the calculation.

---

# 40. Telemetry Validation

The ingestion layer should detect:

- Impossible pressure values.
- Invalid temperatures.
- Missing units.
- Sensor disconnection.
- Stale timestamps.
- Duplicate readings.
- Out-of-range measurements.
- Communication failures.
- Bad quality flags.

Example:

```text
Pressure = NULL
Quality = BAD

→ Do not use the value as diagnostic evidence.
```

---

# 41. Sensor Fault Isolation

HydroGuard should consider sensor failure as an explicit hypothesis.

Example:

```text
Pressure sensor anomaly
        vs
Actual suction-pressure degradation
```

The system can compare:

- Related sensors
- Historical behavior
- Redundant measurements
- Flow
- Discharge pressure
- Vibration
- Process state

A single abnormal sensor should not automatically trigger a mechanical diagnosis.

---

# 42. Alarm Correlation Engine

Instead of generating independent alarms:

```text
High vibration
Low suction pressure
High bearing temperature
Low efficiency
```

HydroGuard should correlate them.

Example:

```text
High vibration
+
Low NPSHa
+
High-frequency energy
+
Efficiency degradation

→ Unified Cavitation Risk Event
```

This reduces alarm fatigue.

---

# 43. Diagnostic Event Model

Each event should contain:

```json
{
  "event_id": "HG-EVENT-001",
  "asset": "P-204",
  "timestamp": "2026-08-26T10:15:00Z",
  "condition": "cavitation_risk",
  "severity": "high",
  "evidence": [],
  "calculations": [],
  "hypotheses": [],
  "recommended_action": "",
  "safety_state": ""
}
```

---

# 44. User Interface

## Main Dashboard

```text
┌─────────────────────────────────────────────┐
│              HYDROGUARD AI                  │
├─────────────────────────────────────────────┤
│ Pump Station: PS-04                         │
│ Asset: Pump P-204                           │
│                                             │
│ ⚠ CAVITATION RISK                           │
│                                             │
│ NPSHa              4.8 m                    │
│ NPSHr              4.2 m                    │
│ Margin             0.6 m                    │
│                                             │
│ Efficiency         81.4 %                   │
│ Vibration          HIGH                     │
│ Bearing Temp       74 °C                    │
├─────────────────────────────────────────────┤
│ CURRENT HYPOTHESES                           │
│                                             │
│ 1. Cavitation             78%               │
│ 2. Suction restriction    11%               │
│ 3. Impeller issue          7%               │
│ 4. Other                   4%               │
├─────────────────────────────────────────────┤
│ NEXT VERIFICATION                            │
│                                             │
│ Verify suction-side operating condition     │
│ and capture a new vibration spectrum.       │
├─────────────────────────────────────────────┤
│ [ Spectrum ] [ NPSH ] [ Trends ] [ Work ]   │
└─────────────────────────────────────────────┘
```

---

# 45. Vibration Spectrum Screen

```text
┌─────────────────────────────────────────────┐
│ P-204 VIBRATION SPECTRUM                    │
├─────────────────────────────────────────────┤
│                                             │
│ Amplitude                                   │
│   │                    /\                   │
│   │        /\         /  \                  │
│   │_______/  \_______/    \________________ │
│   │                                         │
│   └───────────────────────────────────────  │
│       0      1k      3k      5k      Hz    │
│                                             │
│ HIGH-FREQUENCY BAND: ELEVATED               │
│ VPF: DETECTED                               │
│                                             │
│ Diagnostic interpretation:                 │
│ Spectral behavior is consistent with       │
│ increased hydraulic/mechanical stress.     │
└─────────────────────────────────────────────┘
```

---

# 46. NPSH Screen

```text
┌─────────────────────────────────────────────┐
│ NPSH ANALYSIS — P-204                       │
├─────────────────────────────────────────────┤
│                                             │
│ NPSHa ─────────────────────── 4.8 m         │
│ NPSHr ──────────────────── 4.2 m            │
│                                             │
│ Margin: 0.6 m                               │
│                                             │
│ Trend: ↓                                    │
│                                             │
│ Status: REDUCED MARGIN                      │
│                                             │
│ Combined evidence:                          │
│ • Suction pressure decreasing               │
│ • High-frequency vibration increasing       │
│ • Efficiency decreasing                     │
│                                             │
│ Cavitation hypothesis: HIGH                 │
└─────────────────────────────────────────────┘
```

---

# 47. Diagnostic Timeline

Display every important event:

```text
10:02  Telemetry anomaly detected
10:03  Pump operating state identified
10:04  NPSHa calculated
10:05  Vibration window captured
10:06  FFT completed
10:07  High-frequency energy detected
10:08  VPF analysis completed
10:09  Hypotheses updated
10:10  Cavitation becomes leading hypothesis
10:11  Safety assessment completed
10:12  Maintenance recommendation generated
```

This makes the AI's diagnostic process auditable.

---

# 48. Real-Time Monitoring

The dashboard should provide:

```text
Pump status
Pressure
Flow
Temperature
Vibration
Power
Speed
NPSHa
NPSHr
NPSH margin
Efficiency
Diagnostic status
Maintenance status
```

The interface should emphasize abnormal conditions rather than displaying hundreds of raw signals without interpretation.

---

# 49. MVP Scope

Do not attempt to build an entire industrial predictive-maintenance platform for the first demonstration.

## Required

- User selects pump.
- Simulated industrial telemetry is available.
- Modbus TCP simulator.
- OPC UA simulator or mocked interface.
- MQTT Sparkplug B simulator or mocked interface.
- Pressure telemetry.
- Flow telemetry.
- Temperature telemetry.
- Vibration telemetry.
- FFT analysis.
- NPSHa calculation.
- Efficiency calculation.
- VPF calculation.
- Cavitation diagnostic hypothesis.
- Multi-hypothesis ranking.
- Diagnostic timeline.
- Safety warnings.
- Work-order generation.
- Final diagnostic report.

## Optional

- Live industrial gateway.
- Real OPC UA server.
- Real Modbus device.
- Real MQTT broker.
- Historical maintenance database.
- Voice interface.
- PDF export.
- Fleet analytics.

---

# 50. Demo Scenario

Build one extremely convincing industrial demonstration.

## Scenario

Industrial water pumping station.

Asset:

```text
Pump P-204
Multistage centrifugal pump
```

---

## Evidence 1 — Normal operation

The system initially displays:

```text
NPSHa: Healthy
Efficiency: Normal
Vibration: Normal
Bearing temperature: Normal
```

---

## Evidence 2 — Hydraulic deterioration

Suction pressure begins decreasing.

The system calculates:

```text
NPSHa ↓
```

---

## Evidence 3 — Vibration change

The vibration signal changes.

FFT detects:

```text
High-frequency energy ↑
```

---

## Evidence 4 — Hydraulic efficiency

The deterministic calculation engine reports:

```text
Efficiency ↓
```

---

## Evidence 5 — Diagnostic correlation

The Diagnostic Agent combines:

```text
NPSHa deterioration
+
High-frequency vibration
+
Efficiency degradation
+
Suction instability
```

and produces:

```text
Leading hypothesis:
Cavitation risk
```

---

## Evidence 6 — Alternative hypothesis

The system explicitly considers:

```text
Suction restriction
Sensor fault
Impeller degradation
```

---

## Evidence 7 — Verification

HydroGuard recommends:

```text
Verify suction-side operating conditions
and obtain a new vibration measurement.
```

---

## Evidence 8 — Work order

The Work-Order Agent creates:

```text
Priority: HIGH
Condition: Cavitation risk
Asset: Pump P-204
Evidence: Multi-sensor correlation
Recommended action: Hydraulic inspection
```

---

# 51. Hackathon Demonstration Flow

The entire demo should take approximately:

```text
3–5 minutes
```

Suggested sequence:

```text
1. Show healthy pump.
2. Introduce abnormal telemetry.
3. Show NPSHa calculation.
4. Show vibration spectrum.
5. Show efficiency degradation.
6. Show AI hypothesis ranking.
7. Show evidence correlation.
8. Show safety check.
9. Generate work order.
10. Display final engineering report.
```

The key moment should be:

> **The AI does not simply say "vibration is high." It connects hydraulic conditions, frequency-domain evidence, deterministic calculations, and historical behavior to produce a defensible maintenance hypothesis.**

---

# 52. Evaluation Metrics

Create measurable benchmarks.

## Cavitation Detection Accuracy

Percentage of test scenarios where cavitation is correctly ranked first.

---

## Top-3 Diagnostic Recall

Percentage where the correct failure mechanism appears among the top three hypotheses.

---

## NPSH Calculation Accuracy

Percentage of calculations matching the validated engineering reference.

---

## Efficiency Calculation Accuracy

Percentage matching the deterministic reference implementation.

---

## FFT Feature Detection

Accuracy of detecting expected:

- Dominant frequencies
- VPF
- Harmonics
- High-frequency energy

---

## Next-Action Accuracy

Percentage where the recommended verification step is judged appropriate by a domain expert.

---

## Evidence Grounding

Percentage of diagnostic claims linked to:

- Sensor data
- Calculated values
- Documentation
- Historical evidence

---

## Safety Compliance

Percentage of hazardous situations where the system correctly warns, blocks, or escalates.

---

## Time-to-Diagnosis

Compare:

```text
Traditional troubleshooting
vs
HydroGuard-assisted troubleshooting
```

---

# 53. Test Dataset

Build at least:

```text
30+
```

expert-reviewed scenarios.

Suggested categories:

## Cavitation

- Reduced suction pressure
- Reduced NPSHa
- High-frequency vibration
- Suction instability
- Excessive operating flow
- Poor suction conditions

## Hydraulic faults

- Suction restriction
- Discharge restriction
- Incorrect operating point
- Flow instability
- Reduced pump head

## Mechanical faults

- Shaft misalignment
- Bearing degradation
- Mechanical seal degradation
- Impeller damage
- Impeller imbalance

## Instrumentation faults

- Pressure sensor failure
- Temperature sensor failure
- Vibration sensor failure
- Communication loss
- Bad-quality telemetry

## Combined faults

- Cavitation + bearing stress
- Impeller degradation + vibration
- Sensor fault + real hydraulic abnormality
- Reduced NPSHa + excessive flow

---

# 54. Security

Security requirements:

- Authentication
- Role-based access
- Encryption in transit
- Encryption at rest
- Audit logs
- Tenant isolation
- Asset-level access control
- Document access control
- API key protection
- Prompt-injection protection
- Tool authorization
- Industrial protocol credential protection

---

# 55. Prompt Injection Defense

Industrial documents and maintenance notes must be treated as data.

They must never override:

- System safety policies
- Application policies
- Tool permissions
- Physical-control boundaries

Hierarchy:

```text
System Safety Policy
        ↓
Application Policy
        ↓
Trusted Engineering Procedures
        ↓
Site Configuration
        ↓
User Data
        ↓
Retrieved Documents
```

Retrieved documents must never override system safety constraints.

---

# 56. Agent Tool Authorization

Not every agent should have access to every tool.

Example:

```text
Ingestion Agent
→ read_modbus
→ read_opcua
→ read_mqtt

FFT Agent
→ capture_vibration_window
→ calculate_fft
→ detect_vibration_peaks

Hydraulic Agent
→ calculate_npsha
→ calculate_efficiency
→ calculate_head

Knowledge Agent
→ search_manuals
→ search_maintenance_history

Diagnostic Agent
→ read_measurements
→ calculate_features
→ inspect_history

Safety Agent
→ safety_check

Work-Order Agent
→ generate_work_order

Orchestrator
→ coordinate agents
```

Any future tool capable of controlling a physical valve, pump, PLC, or industrial actuator must require explicit authorization.

---

# 57. Physical Control Boundary

For the hackathon:

## READ-ONLY FIRST

HydroGuard can:

- Read telemetry.
- Analyze vibration.
- Calculate hydraulic parameters.
- Analyze historical trends.
- Recommend verification.
- Generate maintenance recommendations.
- Generate work orders.
- Produce reports.

It should not:

- Start pumps automatically.
- Stop pumps automatically.
- Open or close valves automatically.
- Change pump speed automatically.
- Modify PLC programs.
- Modify protection settings.
- Disable alarms.
- Bypass interlocks.
- Override safety systems.

This dramatically reduces safety and liability risks.

---

# 58. Repository Structure

```text
hydroguard-ai/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   └── services/
│
├── backend/
│   ├── api/
│   ├── agents/
│   │   ├── orchestrator/
│   │   ├── ingestion/
│   │   ├── fft/
│   │   ├── hydraulic/
│   │   ├── diagnostic/
│   │   ├── knowledge/
│   │   ├── safety/
│   │   └── work_order/
│   │
│   ├── calculations/
│   │   ├── npsh.py
│   │   ├── efficiency.py
│   │   ├── pump_head.py
│   │   └── vpf.py
│   │
│   ├── signal_processing/
│   │   ├── preprocessing.py
│   │   ├── fft.py
│   │   └── features.py
│   │
│   ├── protocols/
│   │   ├── modbus/
│   │   ├── opcua/
│   │   └── sparkplug/
│   │
│   ├── tools/
│   ├── models/
│   ├── services/
│   └── tests/
│
├── data/
│   ├── telemetry/
│   ├── vibration/
│   ├── test_cases/
│   ├── pump_curves/
│   └── manuals/
│
├── docs/
│   ├── architecture.md
│   ├── safety.md
│   ├── industrial_protocols.md
│   ├── calculations.md
│   └── evaluation.md
│
└── README.md
```

---

# 59. Development Roadmap

## Phase 1 — Foundation

- Project setup
- Frontend
- Backend
- Authentication
- Database
- Pump asset model

---

## Phase 2 — Industrial Telemetry

- Modbus TCP simulator
- OPC UA simulator
- MQTT Sparkplug B simulator
- Telemetry normalization
- Sensor validation
- Time-series storage

---

## Phase 3 — Engineering Engine

- NPSHa
- NPSH margin
- Pump head
- Hydraulic power
- Pump efficiency
- VPF calculation

---

## Phase 4 — Vibration Intelligence

- Vibration ingestion
- Signal preprocessing
- FFT
- Spectral peak detection
- High-frequency band analysis
- VPF analysis
- Feature extraction

---

## Phase 5 — Diagnostic Agent

- Fault intake
- Diagnostic state
- Hypothesis generation
- Evidence correlation
- Hypothesis ranking
- Next-best-measurement engine

---

## Phase 6 — RAG

- Manual ingestion
- Pump documentation
- Embeddings
- Retrieval
- Evidence citations
- Maintenance-history retrieval

---

## Phase 7 — Safety

- Safety classification
- Intervention-risk analysis
- Unsafe-action prevention
- Human approval
- Read-only enforcement

---

## Phase 8 — Work Orders

- Maintenance recommendation
- Priority classification
- Work-order generation
- Evidence attachment
- Report generation

---

## Phase 9 — Evaluation

- 30+ scenarios
- Synthetic telemetry
- Expert review
- Diagnostic accuracy
- FFT evaluation
- Calculation validation
- Safety testing

---

## Phase 10 — Hackathon Demo

- One polished pump scenario
- Clean industrial UI
- Realistic telemetry
- Vibration spectrum
- NPSH visualization
- AI diagnosis
- Work-order generation
- 3–5 minute demonstration

---

# 60. What NOT to Build

Avoid:

- Generic chatbot UI.
- Dashboard with hundreds of meaningless charts.
- Fake AI predictions without evidence.
- Black-box failure claims.
- Automatic pump control.
- Automatic valve control.
- Unsupported claims of 100% diagnostic accuracy.
- Replacing deterministic engineering calculations with LLM reasoning.
- Excessive industrial protocols that are not demonstrated.
- Massive digital-twin infrastructure for the MVP.
- Predictive-maintenance claims without validation.

The project should demonstrate engineering depth.

---

# 61. Future Versions

## Version 2

- Live Modbus TCP
- Live OPC UA
- MQTT Sparkplug B
- Industrial edge gateway
- Real-time telemetry
- Advanced vibration acquisition

---

## Version 3

- Predictive maintenance
- Remaining-useful-life models
- Failure forecasting
- Automated maintenance scheduling
- Spare-parts recommendations

---

## Version 4

- Fleet-level analytics
- Multiple pump stations
- Cross-pump failure patterns
- Plant-wide asset knowledge graph

---

## Version 5

- Digital twin
- Hydraulic simulation
- Pump performance simulation
- Scenario testing
- Simulation-based diagnosis
- Advanced industrial agent orchestration

---

# 62. Business Model

Potential customers:

- Water-treatment plants
- Industrial water plants
- Manufacturing plants
- Oil & gas facilities
- Chemical plants
- Power plants
- Mining operations
- Industrial service companies
- Pump OEMs
- System integrators
- Reliability engineering departments

Possible models:

## SaaS

Per:

```text
Pump
Station
or Plant
```

per month.

## Enterprise

Private deployment with:

- Internal telemetry
- Internal documents
- Internal maintenance history
- On-premise or private cloud infrastructure

## OEM

White-label HydroGuard intelligence integrated into industrial pumping equipment and service platforms.

---

# 63. Strongest Product Positioning

Recommended one-line description:

> **HydroGuard AI is an agentic industrial pump engineer that detects hydraulic and mechanical degradation by combining real-time telemetry, vibration intelligence, deterministic engineering calculations, and evidence-driven AI diagnosis.**

Alternative:

> **From vibration to root cause: an AI diagnostic engineer for industrial pumping stations.**

Alternative:

> **HydroGuard AI turns pump telemetry into explainable maintenance decisions before failure becomes downtime.**

---

# 64. Hackathon Presentation Strategy

The presentation should begin with the industrial problem.

Do not begin with:

> "We built an AI application."

Begin with:

> **"A pump does not have to fail before it tells us something is wrong. The problem is knowing whether that signal means cavitation, mechanical degradation, hydraulic instability, or simply a bad sensor."**

Then demonstrate:

1. Healthy pump.
2. Abnormal telemetry.
3. NPSH deterioration.
4. Vibration-spectrum change.
5. Efficiency degradation.
6. AI hypothesis ranking.
7. Evidence correlation.
8. Safety evaluation.
9. Maintenance recommendation.
10. Work-order generation.

The key message:

> **HydroGuard does not merely detect an anomaly. It investigates the anomaly.**

---

# 65. Core AI Reasoning Loop

HydroGuard should continuously operate around five questions:

```text
1. What do we observe?

2. What can we calculate?

3. What could explain the behavior?

4. What evidence would distinguish the hypotheses?

5. What is the safest useful next action?
```

This creates a structured engineering investigation rather than a generic AI response.

---

# 66. Example End-to-End Reasoning

```text
OBSERVED:
Suction pressure decreasing.

CALCULATED:
NPSHa margin decreasing.

OBSERVED:
Vibration RMS increasing.

CALCULATED:
1–5 kHz vibration energy elevated.

CALCULATED:
VPF component detected.

CALCULATED:
Pump efficiency decreasing.

HYPOTHESES:

H1 Cavitation              78%
H2 Suction restriction     10%
H3 Impeller degradation     7%
H4 Sensor anomaly           5%

NEXT VERIFICATION:

Verify suction-side operating condition
and capture another vibration spectrum.

SAFETY:

Physical intervention requires approved
site procedures and qualified personnel.

MAINTENANCE:

Generate high-priority inspection work order.
```

---

# 67. Definition of Done

The MVP is ready when:

- [ ] A user can create/select a pump asset.
- [ ] Pump telemetry can be simulated.
- [ ] Modbus TCP data flow can be demonstrated.
- [ ] OPC UA data flow can be demonstrated or simulated.
- [ ] MQTT Sparkplug B data flow can be demonstrated or simulated.
- [ ] Pressure measurements are displayed.
- [ ] Flow measurements are displayed.
- [ ] Temperature measurements are displayed.
- [ ] Vibration measurements are displayed.
- [ ] FFT analysis works.
- [ ] High-frequency vibration analysis works.
- [ ] VPF calculation works.
- [ ] NPSHa calculation works.
- [ ] NPSH margin is displayed.
- [ ] Pump efficiency calculation works.
- [ ] Operating trends are displayed.
- [ ] The system detects abnormal conditions.
- [ ] The Diagnostic Agent generates hypotheses.
- [ ] Hypothesis ranking changes according to evidence.
- [ ] Sensor faults can be considered.
- [ ] The system recommends the next verification.
- [ ] Safety warnings are generated.
- [ ] No automatic physical control is enabled.
- [ ] A maintenance work order can be generated.
- [ ] A final engineering report is produced.
- [ ] Evidence is displayed.
- [ ] Calculations are deterministic and independently testable.
- [ ] At least 30 test scenarios exist.
- [ ] Diagnostic evaluation results are documented.
- [ ] Safety evaluation results are documented.
- [ ] The demo can be completed in under five minutes.
- [ ] The system clearly states that it is decision support, not a replacement for qualified personnel.

---

# 68. The Core Principle

HydroGuard AI should always answer five questions:

> **What do we know?**

> **What did the engineering calculations prove?**

> **What could be causing the abnormal condition?**

> **What evidence supports each hypothesis?**

> **What is the safest and most informative thing to check next?**

That is the core of HydroGuard AI.

---

# 69. Final Architecture Principle

The system should fundamentally follow:

```text
INDUSTRIAL DATA
      ↓
OBSERVATION
      ↓
DETERMINISTIC ENGINEERING
      ↓
SIGNAL ANALYSIS
      ↓
MULTI-SENSOR EVIDENCE
      ↓
AI HYPOTHESIS GENERATION
      ↓
HYPOTHESIS RANKING
      ↓
SAFETY VALIDATION
      ↓
NEXT-BEST VERIFICATION
      ↓
MAINTENANCE RECOMMENDATION
      ↓
WORK ORDER
      ↓
AUDITABLE REPORT
```

The LLM is therefore not the product by itself.

The product is the complete **industrial diagnostic system** surrounding the LLM.

> **HydroGuard AI — From pump telemetry to root cause, evidence, and action.**