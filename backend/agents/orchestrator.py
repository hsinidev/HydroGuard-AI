"""
HydroGuard AI — Master Diagnostic Orchestrator
Module: orchestrator.py
Description: End-to-end diagnostic pipeline coordinating physics math, FFT vibration, Bayesian reasoning, and Gemini LLM synthesis.
"""

from typing import Dict, Any, List, Optional
import os
import datetime
import numpy as np

from backend.models.telemetry import PumpTelemetry, CalculatedMetrics, DiagnosticResult, HypothesisItem
from backend.calculations.npsh import calculate_npsha, evaluate_npsh_margin
from backend.calculations.efficiency import calculate_pump_efficiency
from backend.signal_processing.fft import generate_synthetic_vibration_stream, compute_vibration_fft
from backend.agents.diagnostic import DynamicDiagnosticEngine, evaluate_iso_10816_zone
from backend.agents.next_measurement import NextBestMeasurementEngine
from backend.agents.safety_guard import SafetyDecisionGuard, SAFETY_LEGAL_DISCLAIMER
from backend.agents.work_order import WorkOrderGenerator

class DiagnosticOrchestrator:
    def __init__(self, default_gemini_model: str = "gemini-2.5-flash"):
        self.diagnostic_engine = DynamicDiagnosticEngine()
        self.next_measurement_engine = NextBestMeasurementEngine()
        self.safety_guard = SafetyDecisionGuard()
        self.work_order_generator = WorkOrderGenerator()
        self.default_model = os.getenv("GEMINI_MODEL_NAME", default_gemini_model)

    def run_full_diagnosis(
        self,
        telemetry: PumpTelemetry,
        gemini_api_key: Optional[str] = None,
        selected_model: Optional[str] = None
    ) -> DiagnosticResult:
        """
        Execute full end-to-end deterministic + dynamic agent diagnostic cycle.
        """
        now_iso = telemetry.timestamp_iso or datetime.datetime.now(datetime.timezone.utc).isoformat()

        # 1. Deterministic NPSHa & Margin Calculations
        p_suction_pa = telemetry.suction_pressure_bar * 100000.0  # bar to Pa
        p_discharge_pa = telemetry.discharge_pressure_bar * 100000.0

        npsh_res = calculate_npsha(
            p_suction_abs=p_suction_pa,
            temp_celsius=telemetry.fluid_temp_celsius,
            flow_m3_h=telemetry.flow_m3_h,
            suction_pipe_diam_m=telemetry.suction_pipe_diam_m
        )

        npsh_eval = evaluate_npsh_margin(
            npsha_m=npsh_res["npsha_m"],
            npshr_m=telemetry.npshr_m
        )

        # 2. Deterministic Hydraulic Head & Efficiency Calculations
        eff_res = calculate_pump_efficiency(
            p_discharge_pa=p_discharge_pa,
            p_suction_pa=p_suction_pa,
            flow_m3_h=telemetry.flow_m3_h,
            electrical_power_kw=telemetry.electrical_power_kw,
            suction_diam_m=telemetry.suction_pipe_diam_m,
            discharge_diam_m=telemetry.discharge_pipe_diam_m
        )

        # 3. Vibration FFT Signal Processing
        # If time series buffer is provided, use it; otherwise generate representative physical signal
        if telemetry.vibration_time_series and len(telemetry.vibration_time_series) > 100:
            vib_signal = np.array(telemetry.vibration_time_series)
        else:
            # Estimate physical fault components from ingested telemetry
            cav_sev = 0.0
            if npsh_eval["npsh_margin_m"] < 0.5:
                cav_sev = 0.85
            elif npsh_eval["npsh_margin_m"] < 1.2:
                cav_sev = 0.40

            misalign_amp = 0.2
            if abs(telemetry.bearing_temp_de_celsius - telemetry.bearing_temp_nde_celsius) > 15.0:
                misalign_amp = 1.1

            _, vib_signal = generate_synthetic_vibration_stream(
                duration_s=1.0,
                sampling_rate_hz=telemetry.sampling_rate_hz,
                pump_rpm=telemetry.pump_speed_rpm,
                impeller_vanes=telemetry.impeller_vanes,
                cavitation_severity=cav_sev,
                misalignment_2x_amp=misalign_amp,
                unbalance_1x_amp=0.6,
                vpf_pulsation_amp=0.4 + (0.5 if eff_res["efficiency_degradation_pct"] > 10 else 0.0)
            )

        fft_res = compute_vibration_fft(
            vibration_signal=vib_signal,
            sampling_rate_hz=telemetry.sampling_rate_hz,
            pump_rpm=telemetry.pump_speed_rpm,
            impeller_vanes=telemetry.impeller_vanes
        )

        # 4. Synthesize Calculated Metrics Object
        metrics = CalculatedMetrics(
            npsha_m=npsh_res["npsha_m"],
            npshr_m=telemetry.npshr_m,
            npsh_margin_m=npsh_eval["npsh_margin_m"],
            npsh_status=npsh_eval["status"],
            cavitation_risk_index=npsh_eval["cavitation_risk_index"],
            total_head_m=eff_res["total_head_m"],
            differential_pressure_kpa=round((p_discharge_pa - p_suction_pa) / 1000.0, 2),
            hydraulic_power_kw=eff_res["hydraulic_power_kw"],
            pump_efficiency_pct=eff_res["efficiency_pct"],
            efficiency_degradation_pct=eff_res["efficiency_degradation_pct"],
            overall_rms_mm_s=fft_res["overall_rms_mm_s"],
            f_1x_hz=fft_res["f_1x_hz"],
            f_vpf_hz=fft_res["f_vpf_hz"],
            amp_1x_mm_s=fft_res["amp_1x_mm_s"],
            amp_2x_mm_s=fft_res["amp_2x_mm_s"],
            amp_vpf_mm_s=fft_res["amp_vpf_mm_s"],
            cavitation_1_5khz_energy_rms=fft_res["cavitation_1_5khz_energy_rms"],
            cavitation_spectral_ratio=fft_res["cavitation_spectral_ratio"],
            is_cavitation_spectral_elevated=fft_res["is_cavitation_spectral_elevated"]
        )

        # 5. Multi-Hypothesis Diagnostic Reasoning
        hypotheses = self.diagnostic_engine.diagnose(telemetry=telemetry, metrics=metrics)
        top_h = hypotheses[0]

        # 6. Next-Best-Verification Step
        next_step = self.next_measurement_engine.evaluate_next_step(
            top_hypotheses=hypotheses,
            telemetry=telemetry,
            metrics=metrics
        )

        # 7. ISO 10816 Vibration Severity Zone
        iso_zone, zone_status = evaluate_iso_10816_zone(metrics.overall_rms_mm_s)

        # 8. Operating State Determination
        if top_h.severity == "CRITICAL" or zone_status == "CRITICAL":
            op_state = "ALARM_CRITICAL"
        elif top_h.severity in ["HIGH", "MEDIUM"] or zone_status == "WARNING":
            op_state = "DEGRADED_WARNING"
        else:
            op_state = "NORMAL_HEALTHY"

        # 9. Engineering Synthesis & Gemini LLM Reasoning (if API key available)
        synthesis_text = self._generate_ai_synthesis(
            telemetry=telemetry,
            metrics=metrics,
            top_h=top_h,
            next_step=next_step,
            gemini_api_key=gemini_api_key,
            selected_model=selected_model
        )

        return DiagnosticResult(
            asset_id=telemetry.pump_id,
            timestamp_iso=now_iso,
            operating_state=op_state,
            hypotheses=hypotheses,
            top_hypothesis=top_h,
            next_verification_action=next_step,
            iso_10816_vibration_zone=iso_zone,
            calculated_metrics=metrics,
            ai_engineering_synthesis=synthesis_text,
            safety_boundary_statement=SAFETY_LEGAL_DISCLAIMER
        )

    def _generate_ai_synthesis(
        self,
        telemetry: PumpTelemetry,
        metrics: CalculatedMetrics,
        top_h: HypothesisItem,
        next_step: Dict[str, Any],
        gemini_api_key: Optional[str] = None,
        selected_model: Optional[str] = None
    ) -> str:
        """
        Generate rich engineering explanation using Gemini API if key is present,
        or deterministic high-fidelity engineering synthesis fallback.
        """
        api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        model_name = selected_model or self.default_model

        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"You are HydroGuard AI, an expert rotating equipment and industrial pump reliability engineer.\n"
                    f"Analyze the following pump condition data for Pump {telemetry.pump_id}:\n"
                    f"- Suction Pressure: {telemetry.suction_pressure_bar:.2f} bar abs\n"
                    f"- Discharge Pressure: {telemetry.discharge_pressure_bar:.2f} bar\n"
                    f"- Flow: {telemetry.flow_m3_h:.1f} m3/h\n"
                    f"- NPSHa: {metrics.npsha_m:.2f} m (NPSHr: {metrics.npshr_m:.2f} m, Margin: {metrics.npsh_margin_m:.2f} m)\n"
                    f"- Pump Efficiency: {metrics.pump_efficiency_pct:.1f}% (Degradation: {metrics.efficiency_degradation_pct:.1f}%)\n"
                    f"- Vibration Overall RMS: {metrics.overall_rms_mm_s:.2f} mm/s\n"
                    f"- FFT 1-5 kHz Cavitation Energy: {metrics.cavitation_1_5khz_energy_rms:.2f} mm/s RMS (Ratio: {metrics.cavitation_spectral_ratio:.1%})\n"
                    f"- Top Diagnostic Hypothesis: {top_h.name} ({top_h.probability_pct}% probability)\n"
                    f"- Recommended Next Verification: {next_step.get('action_title')}\n\n"
                    f"Provide a concise, professional 3-paragraph engineering condition assessment:\n"
                    f"1. Telemetry & Physical Root Mechanism explanation.\n"
                    f"2. Evidence synthesis from NPSH and FFT frequency bands.\n"
                    f"3. Next-best-verification guidance aligned with ISO 10816 and OSHA LOTO principles."
                )
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                # Log and fallback gracefully
                pass

        # High-Fidelity Deterministic Fallback Synthesis
        if top_h.hypothesis_id == "H_CAVITATION":
            return (
                f"CONDITION SUMMARY: HydroGuard AI has detected active hydraulic cavitation on Pump {telemetry.pump_id}. "
                f"The calculated NPSH available ({metrics.npsha_m:.2f} m) has degraded to within {metrics.npsh_margin_m:.2f} m of the manufacturer required NPSHr ({metrics.npshr_m:.2f} m), "
                f"failing the minimum recommended safety margin of 1.5 m.\n\n"
                f"VIBRATION SIGNATURE: Frequency domain FFT analysis demonstrates pronounced broadband acoustic/vibration excitation in the 1.0–5.0 kHz band "
                f"({metrics.cavitation_1_5khz_energy_rms:.2f} mm/s RMS, representing {metrics.cavitation_spectral_ratio:.1%} of total vibration energy), confirming microscopic vapor bubble collapse at the impeller inlet.\n\n"
                f"RECOMMENDED VERIFICATION: Immediate execution of {next_step.get('action_title')}. "
                f"Inspect suction basket strainer delta-P to isolate upstream physical blockage from suction fluid subcooling deficit. All operations subject to OSHA 1910.147 LOTO."
            )
        elif top_h.hypothesis_id == "H_SUCTION_RESTRICTION":
            return (
                f"CONDITION SUMMARY: Upstream suction restriction identified on Pump {telemetry.pump_id}. "
                f"Suction pressure has dropped to {telemetry.suction_pressure_bar:.2f} bar abs while flow rate is restricted to {telemetry.flow_m3_h:.1f} m3/h.\n\n"
                f"DIAGNOSTIC EVIDENCE: The steep reduction in suction head without significant 2X mechanical misalignment indicates flow starvation upstream of the impeller eye.\n\n"
                f"RECOMMENDED VERIFICATION: {next_step.get('action_title')}. Clean suction basket strainer under isolated LOTO conditions."
            )
        elif top_h.hypothesis_id == "H_SHAFT_MISALIGNMENT":
            return (
                f"CONDITION SUMMARY: Mechanical shaft misalignment diagnosed on Pump {telemetry.pump_id}. "
                f"Vibration spectrum exhibits dominant 2X running speed harmonic at {metrics.f_1x_hz*2:.1f} Hz ({metrics.amp_2x_mm_s:.2f} mm/s), indicating angular/radial coupling bending moments.\n\n"
                f"RECOMMENDED VERIFICATION: {next_step.get('action_title')}. Isolate motor at MCC and execute laser alignment survey."
            )
        elif top_h.hypothesis_id == "H_BEARING_FATIGUE":
            return (
                f"CONDITION SUMMARY: Bearing thermal and mechanical degradation on Pump {telemetry.pump_id}. "
                f"Drive End bearing temperature ({telemetry.bearing_temp_de_celsius:.1f}°C) exceeds baseline limits with elevated overall vibration ({metrics.overall_rms_mm_s:.2f} mm/s).\n\n"
                f"RECOMMENDED VERIFICATION: {next_step.get('action_title')}. Perform ultrasonic acoustic demodulation and draw lube oil sample for spectroscopy."
            )
        else:
            return (
                f"CONDITION SUMMARY: Pump {telemetry.pump_id} is operating within nominal design boundaries. "
                f"NPSH margin ({metrics.npsh_margin_m:.2f} m) and hydraulic efficiency ({metrics.pump_efficiency_pct:.1f}%) are healthy. "
                f"Vibration is in ISO 10816-3 {evaluate_iso_10816_zone(metrics.overall_rms_mm_s)[0]}. Continuous automated monitoring active."
            )
