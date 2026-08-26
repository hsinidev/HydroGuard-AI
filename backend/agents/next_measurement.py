"""
HydroGuard AI — Next-Best-Verification Engine
Module: next_measurement.py
Description: Determines optimal verification step balancing Information Gain vs Technician Safety Risk.
"""

from typing import Dict, Any, List
from backend.models.telemetry import HypothesisItem, CalculatedMetrics, PumpTelemetry

class NextBestMeasurementEngine:
    def evaluate_next_step(
        self,
        top_hypotheses: List[HypothesisItem],
        telemetry: PumpTelemetry,
        metrics: CalculatedMetrics
    ) -> Dict[str, Any]:
        """
        Compute the highest information-gain, lowest-risk field verification step.
        """
        top_h = top_hypotheses[0] if top_hypotheses else None
        second_h = top_hypotheses[1] if len(top_hypotheses) > 1 else None

        if not top_h or top_h.hypothesis_id == "H_HEALTHY_OPERATION":
            return {
                "step_id": "NBV-000",
                "action_title": "Routine Visual & Telemetry Walkdown",
                "priority": "LOW",
                "safety_risk_level": "NEGLIGIBLE",
                "required_ppe": ["Safety Glasses", "Steel-Toe Boots", "Hearing Protection"],
                "loto_required": False,
                "target_parameter": "None (System Healthy)",
                "field_instruction": "Perform standard visual inspection of pump skid for leaks, packing weeping, and foundation anchor tightness. No active intervention needed.",
                "tools_required": ["Flashlight", "Vibration Pen (optional)"],
                "expected_information_gain_pct": 10.0,
                "input_type": "text",
                "expected_range": "N/A"
            }

        if top_h.hypothesis_id in ["H_CAVITATION", "H_SUCTION_RESTRICTION"]:
            # Need to separate whether suction pressure drop is caused by upstream strainer or vapor pressure
            return {
                "step_id": "NBV-101",
                "action_title": "Verify Suction Basket Strainer Differential Pressure (Delta-P)",
                "priority": "IMMEDIATE",
                "safety_risk_level": "LOW (External gauge reading)",
                "required_ppe": ["Safety Glasses", "Thermal Gloves", "High-Vis Vest", "Steel-Toe Boots"],
                "loto_required": False,
                "target_parameter": "Strainer Differential Pressure (Delta-P in bar)",
                "field_instruction": "Connect calibrated differential pressure gauge across suction strainer taps ST-204-A and ST-204-B. If Delta-P > 0.35 bar, strainer is blinded with debris causing suction starvation.",
                "tools_required": ["Handheld Digital DP Gauge (0-2 bar range)", "Infrared Thermometer"],
                "expected_information_gain_pct": 88.0,
                "input_type": "number",
                "input_unit": "bar",
                "expected_range": "0.05 - 0.60 bar (Normal < 0.20 bar)",
                "decision_logic": {
                    "high_reading_outcome": "If Delta-P > 0.35 bar: Confirms upstream Suction Restriction. Schedule offline strainer basket cleaning under LOTO.",
                    "low_reading_outcome": "If Delta-P < 0.20 bar: Discards strainer blockage; confirms hydraulic cavitation caused by high suction temperature or tank level drop."
                }
            }

        elif top_h.hypothesis_id == "H_SHAFT_MISALIGNMENT":
            return {
                "step_id": "NBV-202",
                "action_title": "Laser Optical Shaft Alignment & Soft Foot Check",
                "priority": "HIGH",
                "safety_risk_level": "MEDIUM (Requires Lockout/Tagout)",
                "required_ppe": ["OSHA LOTO Kit", "Electrical Safety PPE", "Safety Glasses", "Mechanic Gloves"],
                "loto_required": True,
                "target_parameter": "Radial & Angular Coupling Offset (mm / mrad)",
                "field_instruction": "Isolate motor breaker P-204-CB1 with Lockout/Tagout. Remove coupling guard. Attach laser alignment heads to motor and pump shafts. Measure parallel and angular misalignment.",
                "tools_required": ["Laser Shaft Alignment Kit", "Dial Indicators", "Shim Pack", "Torque Wrench"],
                "expected_information_gain_pct": 92.0,
                "input_type": "number",
                "input_unit": "mm",
                "expected_range": "0.00 - 0.50 mm (Max allowable: 0.05 mm)",
                "decision_logic": {
                    "high_reading_outcome": "If Offset > 0.08 mm: Re-shim motor feet and re-align coupling to < 0.05 mm tolerance.",
                    "low_reading_outcome": "If Offset < 0.05 mm: Misalignment discarded; inspect coupling spider or gear sleeve for mechanical wear."
                }
            }

        elif top_h.hypothesis_id == "H_BEARING_FATIGUE":
            return {
                "step_id": "NBV-303",
                "action_title": "Acoustic Ultrasonic Demodulation & Lube Oil Sampling",
                "priority": "HIGH",
                "safety_risk_level": "LOW (External contact probe)",
                "required_ppe": ["Safety Glasses", "Hearing Protection", "Nitrile Gloves", "Steel-Toe Boots"],
                "loto_required": False,
                "target_parameter": "Bearing High Frequency Decibel (dB) & Particle Count",
                "field_instruction": "Apply contact ultrasonic probe to Drive End bearing housing. Note dB level and listen for metallic impacts. Draw 100ml oil sample from drain port for lab wear-debris analysis.",
                "tools_required": ["Ultrasonic Contact Probe", "Clean Oil Sampling Bottle", "Strobe Light"],
                "expected_information_gain_pct": 85.0,
                "input_type": "number",
                "input_unit": "dB / ISO Code",
                "expected_range": "15 - 65 dB",
                "decision_logic": {
                    "high_reading_outcome": "If Acoustic dB > 45: Confirms subsurface bearing raceway spalling. Plan bearing replacement.",
                    "low_reading_outcome": "If Acoustic dB < 25: Bearing surfaces healthy; temperature rise likely due to over-greasing or cooling jacket restriction."
                }
            }

        elif top_h.hypothesis_id == "H_IMPELLER_EROSION":
            return {
                "step_id": "NBV-404",
                "action_title": "Head-Capacity Verification & Suction Eye Borescope Inspection",
                "priority": "MEDIUM",
                "safety_risk_level": "LOW",
                "required_ppe": ["Safety Glasses", "Steel-Toe Boots"],
                "loto_required": False,
                "target_parameter": "Q-H Head Curve Deficit (%)",
                "field_instruction": "Throttling discharge valve to 80%, 100%, and 110% BEP flow while logging discharge pressure. Compare against OEM factory test curve.",
                "tools_required": ["Calibrated Pressure Calibrator", "Ultrasonic Clamp-on Flowmeter", "Borescope"],
                "expected_information_gain_pct": 80.0,
                "input_type": "number",
                "input_unit": "% deficit",
                "expected_range": "0 - 25%",
                "decision_logic": {
                    "high_reading_outcome": "If Head Deficit > 8%: Confirms severe impeller vane erosion and ring clearance enlargement.",
                    "low_reading_outcome": "If Head matches curve: Impeller intact; efficiency loss stems from motor electrical degradation."
                }
            }

        return {
            "step_id": "NBV-505",
            "action_title": "Multi-Point Ultrasonic & Thermal Survey",
            "priority": "MEDIUM",
            "safety_risk_level": "LOW",
            "required_ppe": ["Safety Glasses", "Steel-Toe Boots"],
            "loto_required": False,
            "target_parameter": "Thermographic Profile (°C)",
            "field_instruction": "Perform thermal imaging survey across motor housing, coupling, bearing brackets, and mechanical seal flush piping.",
            "tools_required": ["FLIR Thermal Imaging Camera"],
            "expected_information_gain_pct": 75.0,
            "input_type": "text",
            "expected_range": "30 - 80 °C"
        }
