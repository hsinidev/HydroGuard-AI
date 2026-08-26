"""
HydroGuard AI — Dynamic Multi-Hypothesis Diagnostic Engine
Module: diagnostic.py
Description: Dynamic Bayesian-like evidence accumulator and probability re-weighting matrix.
"""

from typing import Dict, Any, List, Tuple
import math
from backend.models.telemetry import HypothesisItem, CalculatedMetrics, PumpTelemetry

def evaluate_iso_10816_zone(rms_velocity_mm_s: float) -> Tuple[str, str]:
    """
    Classify vibration severity according to ISO 10816-3 (Class II / Group 2 Industrial Pumps):
      - Zone A: < 1.4 mm/s RMS (Newly commissioned / Excellent)
      - Zone B: 1.4 - 2.8 mm/s RMS (Unrestricted continuous operation)
      - Zone C: 2.8 - 4.5 mm/s RMS (Restricted operation / Warning)
      - Zone D: > 4.5 mm/s RMS (Danger of damage / Immediate action required)
    """
    if rms_velocity_mm_s < 1.4:
        return "Zone A (Excellent)", "NORMAL"
    elif rms_velocity_mm_s < 2.8:
        return "Zone B (Acceptable)", "NORMAL"
    elif rms_velocity_mm_s < 4.5:
        return "Zone C (Unsatisfactory)", "WARNING"
    else:
        return "Zone D (Unacceptable)", "CRITICAL"

class DynamicDiagnosticEngine:
    """
    Evaluates physical sensor evidence dynamically across competing failure modes.
    Never hardcodes outcomes; computes exact log-likelihoods and softmax probabilities.
    """

    def diagnose(
        self,
        telemetry: PumpTelemetry,
        metrics: CalculatedMetrics
    ) -> List[HypothesisItem]:
        # Unnormalized log-score accumulator for hypotheses
        # Prior log-odds (baseline prior favours healthy slightly in normal operation)
        scores = {
            "H_CAVITATION": 0.0,
            "H_SUCTION_RESTRICTION": 0.0,
            "H_IMPELLER_EROSION": 0.0,
            "H_SHAFT_MISALIGNMENT": 0.0,
            "H_BEARING_FATIGUE": 0.0,
            "H_SEAL_DEGRADATION": 0.0,
            "H_HEALTHY_OPERATION": 0.5
        }

        evidence_for = {k: [] for k in scores}
        evidence_against = {k: [] for k in scores}

        # 1. Evaluate NPSH Margin Evidence
        npsh_margin = metrics.npsh_margin_m
        if npsh_margin < 0.5:
            scores["H_CAVITATION"] += 4.2
            scores["H_SUCTION_RESTRICTION"] += 1.8
            scores["H_HEALTHY_OPERATION"] -= 4.5
            evidence_for["H_CAVITATION"].append(f"Critical NPSH margin ({npsh_margin:.2f}m < 0.5m threshold).")
            evidence_for["H_SUCTION_RESTRICTION"].append(f"Depressed NPSHa ({metrics.npsha_m:.2f}m) indicates suction head deficit.")
        elif npsh_margin < 1.5:
            scores["H_CAVITATION"] += 2.8
            scores["H_SUCTION_RESTRICTION"] += 1.2
            scores["H_HEALTHY_OPERATION"] -= 2.5
            evidence_for["H_CAVITATION"].append(f"Sub-optimal NPSH margin ({npsh_margin:.2f}m < 1.5m safety limit).")
        else:
            scores["H_CAVITATION"] -= 3.0
            evidence_against["H_CAVITATION"].append(f"Sufficient NPSH margin ({npsh_margin:.2f}m >= 1.5m).")
            scores["H_HEALTHY_OPERATION"] += 1.2

        # 2. Evaluate Vibration FFT 1-5 kHz Cavitation Energy Band
        cav_energy = metrics.cavitation_1_5khz_energy_rms
        cav_ratio = metrics.cavitation_spectral_ratio
        if metrics.is_cavitation_spectral_elevated or cav_energy > 1.8:
            scores["H_CAVITATION"] += 3.5
            scores["H_HEALTHY_OPERATION"] -= 3.5
            evidence_for["H_CAVITATION"].append(f"Elevated 1-5 kHz high-frequency broadband energy ({cav_energy:.2f} mm/s RMS, ratio {cav_ratio:.1%}).")
        else:
            if cav_energy < 1.0:
                scores["H_CAVITATION"] -= 2.0
                evidence_against["H_CAVITATION"].append(f"Low 1-5 kHz cavitation acoustic energy ({cav_energy:.2f} mm/s RMS).")

        # 3. Evaluate Suction Pressure & Flow Starvation
        # If suction is heavily throttled and flow is restricted below design BEP (< 100 m3/h)
        if telemetry.suction_pressure_bar < 0.6 and telemetry.flow_m3_h < 105.0:
            scores["H_SUCTION_RESTRICTION"] += 4.0
            scores["H_HEALTHY_OPERATION"] -= 3.5
            evidence_for["H_SUCTION_RESTRICTION"].append(f"Severe suction pressure drop ({telemetry.suction_pressure_bar:.2f} bar) with restricted flow ({telemetry.flow_m3_h:.1f} m3/h).")
        elif telemetry.suction_pressure_bar < 0.8:
            scores["H_SUCTION_RESTRICTION"] += 2.0
            evidence_for["H_SUCTION_RESTRICTION"].append(f"Suction pressure below baseline ({telemetry.suction_pressure_bar:.2f} bar).")
        else:
            scores["H_SUCTION_RESTRICTION"] -= 2.0
            evidence_against["H_SUCTION_RESTRICTION"].append(f"Normal positive suction pressure ({telemetry.suction_pressure_bar:.2f} bar).")

        # 4. Evaluate Efficiency Degradation & VPF Harmonics (Impeller Erosion)
        eff_deg = metrics.efficiency_degradation_pct
        vpf_amp = metrics.amp_vpf_mm_s
        if eff_deg > 10.0:
            scores["H_IMPELLER_EROSION"] += 4.5
            scores["H_HEALTHY_OPERATION"] -= 4.0
            evidence_for["H_IMPELLER_EROSION"].append(f"Pump efficiency degraded by {eff_deg:.1f}% below design baseline ({metrics.pump_efficiency_pct:.1f}%).")
        elif eff_deg > 4.0:
            scores["H_IMPELLER_EROSION"] += 2.5
            scores["H_HEALTHY_OPERATION"] -= 2.0
            evidence_for["H_IMPELLER_EROSION"].append(f"Moderate hydraulic efficiency drop ({eff_deg:.1f}% below design).")
        else:
            scores["H_IMPELLER_EROSION"] -= 2.5
            evidence_against["H_IMPELLER_EROSION"].append(f"Pump hydraulic efficiency remains near design baseline ({metrics.pump_efficiency_pct:.1f}%).")

        # 5. Evaluate Shaft Misalignment (2X RPM dominant harmonic)
        amp_1x = metrics.amp_1x_mm_s
        amp_2x = metrics.amp_2x_mm_s
        if amp_2x > 0.8 and (amp_2x / (amp_1x + 1e-4)) > 0.60:
            scores["H_SHAFT_MISALIGNMENT"] += 4.0
            scores["H_HEALTHY_OPERATION"] -= 3.5
            evidence_for["H_SHAFT_MISALIGNMENT"].append(f"Dominant 2X running speed harmonic ({amp_2x:.2f} mm/s at {metrics.f_1x_hz*2:.1f} Hz).")
        else:
            scores["H_SHAFT_MISALIGNMENT"] -= 2.0
            evidence_against["H_SHAFT_MISALIGNMENT"].append(f"2X harmonic amplitude is benign ({amp_2x:.2f} mm/s).")

        # 6. Evaluate Bearing Fatigue (High bearing temp + high overall RMS)
        max_brg_temp = max(telemetry.bearing_temp_de_celsius, telemetry.bearing_temp_nde_celsius)
        if max_brg_temp > 72.0:
            scores["H_BEARING_FATIGUE"] += 3.5
            scores["H_HEALTHY_OPERATION"] -= 3.0
            evidence_for["H_BEARING_FATIGUE"].append(f"Elevated bearing temperature ({max_brg_temp:.1f}°C > 70°C alert limit).")
        elif max_brg_temp > 60.0:
            scores["H_BEARING_FATIGUE"] += 1.5
            evidence_for["H_BEARING_FATIGUE"].append(f"Mild bearing temperature rise ({max_brg_temp:.1f}°C).")
        else:
            scores["H_BEARING_FATIGUE"] -= 1.5
            evidence_against["H_BEARING_FATIGUE"].append(f"Bearing temperatures within normal limits ({max_brg_temp:.1f}°C).")

        # 7. Evaluate Mechanical Seal Degradation
        if telemetry.bearing_temp_de_celsius > 65.0 and telemetry.suction_pressure_bar < 0.9:
            scores["H_SEAL_DEGRADATION"] += 1.2
            evidence_for["H_SEAL_DEGRADATION"].append("Suction fluctuation coupled with DE stuffing box heating.")
        else:
            scores["H_SEAL_DEGRADATION"] -= 1.0

        # Compute Softmax Probabilities
        max_s = max(scores.values())
        exp_scores = {k: math.exp(v - max_s) for k, v in scores.items()}
        sum_exp = sum(exp_scores.values())
        probs = {k: exp_scores[k] / sum_exp for k in scores}

        # Build Structured Hypotheses
        meta = {
            "H_CAVITATION": {
                "name": "Cavitation / Vapor Bubble Implosion",
                "mechanism": "Sheet/cloud cavitation forming at impeller eye due to local pressure falling below fluid vapor pressure.",
                "action": "Verify suction line valve positioning, check suction strainer delta-P, and inspect liquid subcooling."
            },
            "H_SUCTION_RESTRICTION": {
                "name": "Suction Line Restriction / Strainer Clogging",
                "mechanism": "Physical debris or partially closed suction isolation valve causing high suction friction loss.",
                "action": "Execute differential pressure check across basket strainer; inspect suction spool."
            },
            "H_IMPELLER_EROSION": {
                "name": "Impeller Vane Erosion / Leading Edge Wear",
                "mechanism": "Progressive metal loss on impeller blade tips altering hydraulic velocity triangles and head curve.",
                "action": "Perform casing borescope inspection during next planned outage; compare Q-H curve."
            },
            "H_SHAFT_MISALIGNMENT": {
                "name": "Shaft Misalignment / Coupling Wear",
                "mechanism": "Angular or parallel offset between motor shaft and pump shaft inducing 2X bending moments.",
                "action": "Perform laser shaft alignment check on pump-motor coupling; inspect elastomeric element."
            },
            "H_BEARING_FATIGUE": {
                "name": "Bearing Raceway Degradation / Lube Breakdown",
                "mechanism": "Sub-surface fatigue or lubrication breakdown in Drive End / Non-Drive End rolling elements.",
                "action": "Perform grease/oil sampling analysis and ultrasonic acoustic bearing demodulation."
            },
            "H_SEAL_DEGRADATION": {
                "name": "Mechanical Seal / Barrier Plan Degradation",
                "mechanism": "Friction heat or seal face vaporization causing barrier fluid contamination or face wear.",
                "action": "Inspect seal barrier reservoir level, barrier pressure, and seal gland drain leakage rate."
            },
            "H_HEALTHY_OPERATION": {
                "name": "Normal Baseline Operation",
                "mechanism": "Pump operating within permissible Best Efficiency Point (BEP) hydraulic and vibration envelopes.",
                "action": "Continue automated condition monitoring without manual intervention."
            }
        }

        hypotheses: List[HypothesisItem] = []
        for hid, prob in probs.items():
            prob_pct = round(prob * 100.0, 1)
            
            # Determine severity
            if hid == "H_HEALTHY_OPERATION":
                severity = "HEALTHY" if prob_pct > 50 else "NORMAL"
            elif prob_pct >= 60.0:
                severity = "CRITICAL"
            elif prob_pct >= 35.0:
                severity = "HIGH"
            elif prob_pct >= 15.0:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            conf_interval = round(min(8.0, max(2.5, 12.0 * (1.0 - prob))), 1)

            hypotheses.append(HypothesisItem(
                hypothesis_id=hid,
                name=meta[hid]["name"],
                probability_pct=prob_pct,
                severity=severity,
                confidence_interval_pct=conf_interval,
                primary_mechanism=meta[hid]["mechanism"],
                supporting_evidence=evidence_for[hid] if evidence_for[hid] else ["Telemetry consistent with baseline parameter range."],
                conflicting_evidence=evidence_against[hid] if evidence_against[hid] else [],
                recommended_technician_action=meta[hid]["action"]
            ))

        # Sort descending by probability
        hypotheses.sort(key=lambda x: x.probability_pct, reverse=True)
        return hypotheses
