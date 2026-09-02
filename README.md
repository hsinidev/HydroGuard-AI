# 🌊 HydroGuard AI — Industrial Hydraulic Pump Diagnostic Workstation

[![Live Demo: Cloudflare Pages](https://img.shields.io/badge/🚀_LIVE_DEMO-Cloudflare_Pages-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://hydroguardai.pages.dev/)
[![Build & Test Status](https://img.shields.io/badge/pytest-100%25%20pass-emerald?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/hsinidev/HydroGuard-AI)
[![Evaluation Benchmarks](https://img.shields.io/badge/benchmarks-32%20cases%20%7C%20100%25%20accuracy-cyan?style=for-the-badge)](https://github.com/hsinidev/HydroGuard-AI)
[![ISO Alignment](https://img.shields.io/badge/Standards-ISO_10816--3_%7C_ISO_55000-blue?style=for-the-badge)](https://github.com/hsinidev/HydroGuard-AI)
[![Safety Boundary](https://img.shields.io/badge/Safety-Read--Only%20Decision--Support-rose?style=for-the-badge)](https://github.com/hsinidev/HydroGuard-AI)

> 🌐 **Live Cloudflare Workstation:** **[https://hydroguardai.pages.dev/](https://hydroguardai.pages.dev/)**  
> **HydroGuard AI** combines real-time industrial telemetry (Modbus TCP, OPC UA, MQTT Sparkplug B), pure deterministic hydraulic equations, frequency-domain FFT vibration signal processing (1–5 kHz cavitation band detection), and dynamic Bayesian multi-hypothesis reasoning to protect high-criticality industrial centrifugal pumps from cavitation, impeller erosion, and catastrophic mechanical breakdown.


---

## 📌 Lead Architect & Engineering Accreditation

- **Lead Architect:** **Mohamed Hsini**
- **GitHub Repository:** [https://github.com/hsinidev/HydroGuard-AI](https://github.com/hsinidev/HydroGuard-AI)
- **Portfolio & Website:** [https://hsini.dev](https://hsini.dev)
- **Direct Contact:** [contact@hsini.dev](mailto:contact@hsini.dev)

---

## 📐 1. Deterministic First Principle & Physics Core

All physical, hydraulic, and vibration equations are executed outside the LLM in pure, deterministic Python modules rejecting invalid physical units or negative absolute pressures:

1. **Net Positive Suction Head Available ($NPSH_a$) & Margin:**
   $$NPSH_a = \frac{P_{suction} - P_{vapor}(T)}{\rho \cdot g} + \frac{v_s^2}{2g}$$
   $$NPSH_{margin} = NPSH_a - NPSH_r$$
   - Critical Cavitation Alarm: $NPSH_{margin} < 0.5\text{ m}$
   - Warning Low Margin: $0.5\text{ m} \le NPSH_{margin} < 1.5\text{ m}$
   - Normal Healthy State: $NPSH_{margin} \ge 1.5\text{ m}$

2. **Total Dynamic Head ($H$) & Instantaneous Efficiency ($\eta$):**
   $$H = \frac{P_d - P_s}{\rho \cdot g} + \Delta z + \frac{v_d^2 - v_s^2}{2g}$$
   $$\eta = \frac{\rho \cdot g \cdot Q \cdot H}{P_{shaft}} \times 100\%$$

3. **FFT Vibration Frequency Processing & Cavitation Energy Band:**
   - Real FFT with Hanning windowing and coherent gain correction.
   - Harmonic extraction: $1\times RPM$, $2\times$ Misalignment harmonic, $VPF = Z \times 1\times RPM$ (Vane Pass Frequency).
   - High-Frequency Broadband Band Energy: Integrated power across $1000\text{ Hz} - 5000\text{ Hz}$ cavitation bubble collapse zone.

---

## 🔬 2. Benchmark Evaluation Suite (32 Structured Industrial Scenarios)

The test suite evaluates 32 distinct real-world pump degradation scenarios across 4 key failure domains:

| Category | Cases | Primary Failure Mechanism | Detection Accuracy |
| :--- | :---: | :--- | :---: |
| **Cavitation & Suction Instability** | 01–08 | Vapor bubble implosion, suction head deficit, fluid boiling | **100%** |
| **Hydraulic Degradation** | 09–16 | Impeller vane leading-edge erosion, head curve drop | **100%** |
| **Mechanical Faults** | 17–24 | 2X shaft misalignment, bearing raceway spalling | **100%** |
| **Suction Restriction & Baseline** | 25–32 | Strainer blinding, Best Efficiency Point (BEP) operation | **100%** |

```bash
# Execute evaluation suite
python backend/tests/evaluate_benchmarks.py
```

---

## 🛡️ 3. Safety Guardrails & Legal Boundary

- **Read-Only Physical Boundary:** HydroGuard AI operates strictly across a read-only telemetry boundary and has no physical write access to pump motor starters, VFDs, or valves.
- **Standards Alignment:**
  - **ISO 10816-3:** Mechanical vibration evaluation by measurement on non-rotating parts.
  - **ISO 55000:2014:** Asset Management maintenance workflows and digital work-order schema.
  - **OSHA 29 CFR 1910.147 / NFPA 70E:** The Control of Hazardous Energy (Lockout/Tagout - LOTO).

---

## 🚀 4. Quick Start & Local Setup

### Backend (FastAPI + Uvicorn)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (React + Vite SCADA Workstation)
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🐳 5. Docker & Cloud Deployment

```bash
# Build multi-stage Docker container
docker build -t hydroguard-ai .

# Run container locally
docker run -p 8000:8000 hydroguard-ai

# Deploy to Google Cloud Run
gcloud run deploy hydroguard-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```
