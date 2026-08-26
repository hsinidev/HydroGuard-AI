# HydroGuard AI — Implementation Decisions & Architectural Blueprint

## 1. Deterministic First Principle
- All hydraulic and physical calculations (NPSHa, NPSH margin, Total Dynamic Head, Pump Hydraulic Efficiency, Vane Pass Frequency, FFT Spectral Energy) are executed strictly in pure Python deterministic modules outside LLMs.
- Physical units are enforced (SI standard: Pascals/bar for pressure, $m^3/h$ and $m^3/s$ for flow, meters for head, kW and Watts for power, Hz for frequencies). Out-of-bounds or physically impossible values (e.g. negative absolute pressures, efficiency $> 100\%$, flow $< 0$) raise explicit validation exceptions or are flagged as bad telemetry quality.

## 2. Dynamic Bayesian-like Diagnostic Reasoning
- Diagnostic hypotheses (Cavitation, Suction Restriction, Impeller Vane Erosion, Shaft Misalignment, Mechanical Seal Degradation, Bearing Fatigue) are computed dynamically from normalized evidence vectors across pressure gradients, NPSH margins, FFT frequency spectra (VPF harmonics, 1–5 kHz high-frequency broadband noise), and thermal signatures.
- Telemetry streams can be driven by live Modbus TCP, OPC UA, MQTT Sparkplug B bridges or synthetic historical test cases.

## 3. Safety Decision-Support & Legal Boundary
- HydroGuard AI operates strictly as an advisory Decision-Support System.
- Aligned with ISO 10816-3 (Mechanical vibration evaluation), ISO 55000 (Asset management), and OSHA 1910.147 (Lockout/Tagout - LOTO) protocols.
- The system is architected as strictly **Read-Only** on physical control networks: it cannot actuate valves, start/stop motors, or override emergency shutdowns.

## 4. Frontend & Workstation Experience
- React + Vite + Tailwind CSS industrial SCADA aesthetic.
- Custom SVG radial vector gauges for real-time telemetry ($P_s, P_d, Q, H, \eta$, NPSH margin, Temperature).
- Interactive 2D FFT vibration spectrum viewer highlighting key operating frequency bands and cavitation zones.
- Exportable ISO 55000 Maintenance Work Order with full parts BOM, LOTO safety guidelines, and diagnostic evidence trail.
- Integrated Engine Settings & Developer Info modal featuring Lead Architect Mohamed Hsini accreditation, Gemini API Key storage in browser localStorage, and model switching (`gemini-3.5-flash`, `gemini-3.5-pro`, `gemini-2.5-flash`).
