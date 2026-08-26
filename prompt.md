You are an expert Principal Industrial Software Architect, AI Engineer, and DevOps Specialist.
Workspace Baseline Document: `HydroGuard_AI_System_Architecture_Blueprint.md`

================================================================================

### 0. IMPLEMENTATION INTEGRITY RULES & CONSTRAINTS (STRICT)

================================================================================

1. Deterministic Core First: All physical, hydraulic, and vibration equations (NPSHa, NPSH margin, pump efficiency, head, VPF frequency, and FFT 1–5 kHz energy band detection) MUST be implemented in pure, deterministic Python functions outside the LLM in `backend/calculations/` and `backend/signal_processing/`. Reject invalid physical units, negative pressures, or impossible values.
2. Dynamic Reasoning (No Hardcoding): Diagnostic outputs, hypothesis probabilities (e.g., Cavitation risk, Impeller wear, Bearing fatigue), and next-best verification steps must be dynamically computed by the diagnostic reasoning engine based on ingested sensor streams. Never hardcode outcomes for the demo.
3. Safety Framing & Legal Boundary: System operates strictly as a "Safety Decision-Support & Diagnostic Orchestration System". Use "aligned with standard principles" (e.g., ISO 10816-3-aligned, ISO 55000-aligned, OSHA 1910.147-informed) rather than claiming certified legal compliance.
4. Read-Only Physical Boundary: The system operates strictly as read-only. It MUST NOT execute physical valve manipulation, pump energization, or safety interlock overrides.
5. Model Dynamic Discovery & Local Storage Key Vault: Ingest Gemini models via environment variable `GEMINI_MODEL_NAME` (defaulting to `gemini-3.5-flash` with fallback to `gemini-3.5-pro`). Store API keys securely in browser localStorage.
6. Developer Accreditation & Settings Modal: Embed a top-header "⚙️ Engine Settings & Developer Info" control modal allowing users to enter/hide Gemini API keys, toggle models (`gemini-3.5-flash` / `gemini-3.5-pro`), and inspect Lead Architect credentials:
   - Lead Architect: Mohamed Hsini
   - GitHub Repository: https://github.com/hsinidev/HydroGuard-AI
   - Website: https://hsini.dev
   - Contact: contact@hsini.dev
7. Automated Repository & Cloud Deploy: Automatically initialize Git, create GitHub repository `hsinidev/HydroGuard-AI`, push main branch, and deploy to Google Cloud Run in `us-central1`.
8. Media Pipeline: Ensure recorded video from Playwright (WebM) is post-processed via FFmpeg into standard 1080p MP4 with synchronized AI voiceover narration inside `./demo_video_output/`.

================================================================================

### 1. PHASED IMPLEMENTATION EXECUTION ROADMAP

================================================================================

--- PHASE 0: DEPENDENCY VALIDATION & ENVIRONMENT SETUP ---

- Set up standard project structure:
  backend/ (api/, agents/, calculations/, signal_processing/, protocols/, models/, tests/)
  frontend/ (src/components/, src/hooks/, App.jsx)
  data/ (test_cases/, telemetry/, schematics/)
- Configure dependencies: fastapi, pydantic, uvicorn, google-genai, numpy, scipy, playwright, edge-tts.
- Document setup decisions in `IMPLEMENTATION_DECISIONS.md`.

--- PHASE 1: DETERMINISTIC HYDRAULIC & VIBRATION MATH ENGINES ---

- Build `backend/calculations/npsh.py`: NPSHa calculation:
  $$
  NPSH_a = \frac{P_{suction} - P_{vapor}}{\rho \cdot g} + \frac{v_s^2}{2g}
  $$

  Compute NPSH margin ($NPSH_a - NPSH_r$) and status classification.
- Build `backend/calculations/efficiency.py`: Instantaneous pump efficiency:
  $$
  \eta = \frac{\rho \cdot g \cdot Q \cdot H}{P_{electrical}} \times 100
  $$
- Build `backend/signal_processing/fft.py`: FFT time-to-frequency domain converter, Vane Pass Frequency ($VPF = Z \times f_{rotation}$), and 1–5 kHz high-frequency cavitation band energy extractor.
- Write unit tests in `backend/tests/test_hydraulic_math.py` (ensure 100% pass rate).

--- PHASE 2: PROTOCOL TELEMETRY BRIDGES & AGENT CORE ---

- Build protocol simulators in `backend/protocols/`:
  - Modbus TCP (Port 502 register mapping: Suction P, Discharge P, Flow, Bearing Temp, Speed, Power).
  - OPC UA (IEC 62541 node subscriptions).
  - MQTT Sparkplug B telemetry stream.
- Build `backend/agents/orchestrator.py`: Diagnostic state machine (Pump Asset ID, Telemetry Stream, Hypothesis Tree, Evidence Trail, Safety State).
- Build `backend/agents/diagnostic.py`: Dynamic hypothesis probability re-weighting matrix (Cavitation risk, Suction restriction, Shaft misalignment, Impeller erosion, Mechanical seal degradation).
- Build `backend/agents/next_measurement.py`: Next-Best-Verification engine optimizing information gain vs technician risk.
- Validate primary scenario (Pump P-204 Cavitation case) in `backend/tests/test_case_p204.py`.

--- PHASE 3: 30+ STRUCTURED BENCHMARK EVALUATION SUITE ---

- Generate 30+ structured test cases in `data/test_cases/` across:
  * Cavitation & Suction Instability Scenarios
  * Hydraulic Degradation & Impeller Erosion
  * Mechanical Faults (Bearing fatigue, misalignment, mechanical seal leak)
  * Telemetry & Sensor Fault Isolation (Bad quality flags, pressure sensor drift)
- Build `backend/tests/evaluate_benchmarks.py` calculating Cavitation Detection Accuracy, NPSH Calculation Precision, Top-3 Recall, and Safety Recall.

--- PHASE 4: PUMP RELIABILITY OPERATOR WORKSTATION UI ---

- Build high-visibility industrial SCADA workstation interface in `frontend/src/App.jsx`:
  * Top Bar: Title "HydroGuard AI", Live Telemetry Status Badges, [⚙️ Engine Settings & Developer Info] modal trigger button.
  * Live Telemetry & Vector Gauge Matrix: Real-time gauges for Suction/Discharge Pressure, Flow, NPSHa Margin, Efficiency (%), and Bearing Temperature (°C).
  * FFT Vibration Spectrum Viewer: 2D SVG spectral graph displaying 1–5 kHz cavitation energy band and VPF peaks.
  * Interactive Dynamic Hypothesis Matrix: Live animated percentage bars for competing failure mechanisms.
  * Next-Best-Verification Action Card: Clear prompt with value/unit input controls.
  * Exportable ISO 55000 / ISO 10816-Aligned Work Order Modal with printable parts BOM and OSHA LOTO safety precautions.
  * Settings Modal: API Key input (with show/hide toggle, localStorage persistence), Model Selector (`gemini-3.5-flash` / `gemini-3.5-pro`), and Lead Architect Info Card (Mohamed Hsini).

--- PHASE 5: GITHUB AUTOMATION & CLOUD RUN DEPLOYMENT ---

- Create multi-stage `Dockerfile` (FastAPI backend + static frontend build) and `cloudbuild.yaml`.
- Automated Git & GitHub Push:
  Execute `gh repo create hsinidev/HydroGuard-AI --public --source=. --remote=origin --push` to create and push repository to GitHub (`https://github.com/hsinidev/HydroGuard-AI.git`).
- Automated Cloud Run Deployment:
  Deploy container live using `gcloud run deploy hydroguard-ai --source . --platform managed --region us-central1 --allow-unauthenticated`.

--- PHASE 6: AUTOMATED PLAYWRIGHT RECORDING & AI VOICEOVER ---

- Build and run `record_demo.py` using `playwright` and `edge-tts`:
  1. Synthesize audio narration clips using `edge-tts` (`en-US-ChristopherNeural`).
  2. Launch Playwright Chromium at 1920x1080 resolution targeting the live app.
  3. Automate Pump P-204 Cavitation scenario: open Settings modal, inspect API key/Architect card, ingest abnormal suction telemetry, view FFT spectrum, trigger diagnostic re-weighting to 78% Cavitation risk, and export ISO Work Order.
  4. Post-process WebM recording and audio tracks with FFmpeg into a 1080p MP4 inside `./demo_video_output/demo.mp4`.

================================================================================
Begin execution strictly starting with Phase 0 and Phase 1. Validate Phase 2 Case P-204 before advancing to frontend and deployment phases.
