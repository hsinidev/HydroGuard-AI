"""
HydroGuard AI — Validation Test for Case P-204 (Cavitation Diagnostic Pipeline)
File: test_case_p204.py
"""

import pytest
from backend.models.telemetry import PumpTelemetry
from backend.agents.orchestrator import DiagnosticOrchestrator
from backend.agents.safety_guard import SafetyDecisionGuard

def test_pump_p204_cavitation_diagnostic_flow():
    # 1. Instantiate orchestrator
    orchestrator = DiagnosticOrchestrator()

    # 2. Build Pump P-204 telemetry under suction starvation / cavitation
    telemetry_p204 = PumpTelemetry(
        pump_id="P-204",
        suction_pressure_bar=0.45,  # 0.45 bar abs (45 kPa)
        discharge_pressure_bar=7.8,
        flow_m3_h=118.0,
        fluid_temp_celsius=25.0,
        pump_speed_rpm=2950.0,
        electrical_power_kw=28.5,
        bearing_temp_de_celsius=48.0,
        bearing_temp_nde_celsius=44.0,
        impeller_vanes=5,
        npshr_m=4.2,
        suction_pipe_diam_m=0.15,
        discharge_pipe_diam_m=0.10,
        protocol_source="MODBUS_TCP"
    )

    # 3. Execute full diagnosis
    result = orchestrator.run_full_diagnosis(telemetry=telemetry_p204)

    # 4. Assertions on deterministic calculations
    metrics = result.calculated_metrics
    assert metrics.npsha_m < 5.0  # Approx 4.3 m
    assert metrics.npsh_margin_m < 0.5  # Critical margin
    assert metrics.npsh_status == "CRITICAL_CAVITATION_RISK"
    assert metrics.is_cavitation_spectral_elevated is True
    assert metrics.cavitation_1_5khz_energy_rms > 2.0

    # 5. Assertions on Bayesian Multi-Hypothesis Engine
    top_h = result.top_hypothesis
    assert top_h.hypothesis_id in ["H_CAVITATION", "H_SUCTION_RESTRICTION"]
    assert top_h.probability_pct >= 60.0  # High confidence
    assert top_h.severity in ["CRITICAL", "HIGH"]
    assert len(top_h.supporting_evidence) > 0

    # 6. Assertions on Next-Best-Verification Step
    nbv = result.next_verification_action
    assert nbv["step_id"] == "NBV-101"
    assert "Strainer" in nbv["action_title"] or "Delta-P" in nbv["action_title"]
    assert nbv["expected_information_gain_pct"] >= 80.0

    # 7. Assertions on Safety & Read-Only Bounds
    safety_guard = SafetyDecisionGuard()
    read_only_check = safety_guard.validate_action_safety({"action_type": "advisory_inspection"})
    assert read_only_check["is_permitted"] is True

    illegal_control_check = safety_guard.validate_action_safety({"action_type": "actuate_valve_open"})
    assert illegal_control_check["is_permitted"] is False
    assert illegal_control_check["boundary_enforcement"] == "INTERVENTION_REJECTED"

    # 8. Assertions on Work Order Generation
    loto = safety_guard.get_loto_procedure("P-204")
    wo = orchestrator.work_order_generator.generate_work_order(
        telemetry=telemetry_p204,
        metrics=metrics,
        top_hypothesis=top_h,
        next_step=nbv,
        loto_sop=loto
    )
    assert wo["asset_id"] == "P-204"
    assert wo["priority"] == "HIGH"
    assert len(wo["bill_of_materials"]) >= 2
    assert "LOTO-SOP-P-204" in wo["loto_safety_procedure"]["procedure_id"]
