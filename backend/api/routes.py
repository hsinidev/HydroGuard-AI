"""
HydroGuard AI — FastAPI Application Router
Module: routes.py
"""

from fastapi import APIRouter, HTTPException, Header, Query
from typing import Dict, Any, List, Optional
import os
import json

from backend.models.telemetry import PumpTelemetry, DiagnosticResult
from backend.agents.orchestrator import DiagnosticOrchestrator
from backend.agents.safety_guard import SafetyDecisionGuard, SAFETY_LEGAL_DISCLAIMER
from backend.protocols.modbus import ModbusTCPSimulator
from backend.protocols.opc_ua import OPCUASimulator
from backend.protocols.sparkplug_b import SparkplugBSimulator

router = APIRouter()
orchestrator = DiagnosticOrchestrator()
safety_guard = SafetyDecisionGuard()
modbus_sim = ModbusTCPSimulator()
opc_sim = OPCUASimulator()
sparkplug_sim = SparkplugBSimulator()

TEST_CASES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "test_cases"))

@router.get("/health")
def get_health():
    return {
        "status": "ONLINE",
        "service": "HydroGuard AI Industrial Condition Monitoring Core",
        "version": "2.4.0-PROD",
        "safety_mode": "READ_ONLY_DECISION_SUPPORT",
        "supported_models": ["gemini-3.5-flash", "gemini-3.5-pro", "gemini-2.5-flash"]
    }

@router.post("/diagnose", response_model=DiagnosticResult)
def run_diagnosis(
    telemetry: PumpTelemetry,
    x_gemini_api_key: Optional[str] = Header(default=None, alias="X-Gemini-API-Key"),
    x_gemini_model: Optional[str] = Header(default=None, alias="X-Gemini-Model")
):
    """
    Execute full deterministic hydraulic calculations, FFT vibration spectrum analysis,
    Bayesian multi-hypothesis re-weighting, and Gemini LLM engineering synthesis.
    """
    try:
        res = orchestrator.run_full_diagnosis(
            telemetry=telemetry,
            gemini_api_key=x_gemini_api_key,
            selected_model=x_gemini_model
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Diagnostic error: {str(e)}")

@router.get("/cases")
def list_test_cases():
    """
    List all available benchmark industrial test cases.
    """
    if not os.path.exists(TEST_CASES_DIR):
        return []
    
    files = sorted([f for f in os.listdir(TEST_CASES_DIR) if f.endswith(".json")])
    case_list = []
    for f in files:
        path = os.path.join(TEST_CASES_DIR, f)
        with open(path, "r", encoding="utf-8") as jf:
            data = json.load(jf)
            case_list.append({
                "case_id": data.get("case_id"),
                "category": data.get("category"),
                "pump_id": data.get("pump_id"),
                "description": data.get("description"),
                "expected_top_hypothesis": data.get("expected_top_hypothesis")
            })
    return case_list

@router.get("/cases/{case_id}")
def get_test_case(case_id: str):
    """
    Retrieve full telemetry profile and metadata for a specific test case.
    """
    file_path = os.path.join(TEST_CASES_DIR, f"{case_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.post("/work-order")
def create_work_order(payload: Dict[str, Any]):
    """
    Generate an ISO 55000 / ISO 10816-aligned Maintenance Work Order with full parts BOM & LOTO.
    """
    telemetry_data = payload.get("telemetry", {})
    telemetry_obj = PumpTelemetry(**telemetry_data)
    diag = orchestrator.run_full_diagnosis(telemetry=telemetry_obj)
    
    loto_sop = safety_guard.get_loto_procedure(telemetry_obj.pump_id)
    wo = orchestrator.work_order_generator.generate_work_order(
        telemetry=telemetry_obj,
        metrics=diag.calculated_metrics,
        top_hypothesis=diag.top_hypothesis,
        next_step=diag.next_verification_action,
        loto_sop=loto_sop
    )
    return wo

@router.post("/next-verification/feedback")
def submit_field_verification_feedback(payload: Dict[str, Any]):
    """
    Process field technician measurement feedback (e.g. strainer delta-P, coupling offset)
    and update hypothesis certainty.
    """
    step_id = payload.get("step_id")
    measured_value = payload.get("measured_value")
    telemetry_data = payload.get("telemetry", {})
    
    telemetry_obj = PumpTelemetry(**telemetry_data)
    diag = orchestrator.run_full_diagnosis(telemetry=telemetry_obj)
    
    # Dynamic Bayes update based on technician field measurement
    updated_hypotheses = []
    if step_id == "NBV-101":  # Strainer Delta-P check
        try:
            val = float(measured_value)
            for h in diag.hypotheses:
                h_copy = h.model_copy()
                if val > 0.35:
                    if h_copy.hypothesis_id == "H_SUCTION_RESTRICTION":
                        h_copy.probability_pct = min(98.5, h_copy.probability_pct + 25.0)
                        h_copy.supporting_evidence.append(f"Technician verified high strainer Delta-P ({val:.2f} bar > 0.35 bar limit). Blockage confirmed.")
                    elif h_copy.hypothesis_id == "H_CAVITATION":
                        h_copy.probability_pct = max(1.5, h_copy.probability_pct - 20.0)
                        h_copy.conflicting_evidence.append(f"Primary cause isolated to upstream strainer blinding ({val:.2f} bar).")
                else:
                    if h_copy.hypothesis_id == "H_SUCTION_RESTRICTION":
                        h_copy.probability_pct = max(1.0, h_copy.probability_pct - 35.0)
                        h_copy.conflicting_evidence.append(f"Strainer Delta-P clean ({val:.2f} bar < 0.20 bar). Upstream strainer blockage discarded.")
                    elif h_copy.hypothesis_id == "H_CAVITATION":
                        h_copy.probability_pct = min(98.0, h_copy.probability_pct + 15.0)
                        h_copy.supporting_evidence.append(f"Strainer is clean ({val:.2f} bar). Cavitation stems from suction liquid temperature/tank level.")
                updated_hypotheses.append(h_copy)
        except Exception:
            updated_hypotheses = diag.hypotheses
    else:
        updated_hypotheses = diag.hypotheses

    updated_hypotheses.sort(key=lambda x: x.probability_pct, reverse=True)
    diag.hypotheses = updated_hypotheses
    diag.top_hypothesis = updated_hypotheses[0]
    return diag

@router.get("/protocols/modbus/poll")
def poll_modbus_registers(
    p_suc: float = Query(0.45),
    p_disch: float = Query(7.8),
    flow: float = Query(118.0)
):
    sample = {
        "suction_pressure_bar": p_suc,
        "discharge_pressure_bar": p_disch,
        "flow_m3_h": flow,
        "pump_speed_rpm": 2950.0,
        "electrical_power_kw": 28.5,
        "bearing_temp_de_celsius": 48.0,
        "bearing_temp_nde_celsius": 44.0,
        "fluid_temp_celsius": 25.0,
        "vibration_rms": 2.85,
        "quality_flag": "GOOD"
    }
    regs = modbus_sim.encode_telemetry_registers(sample)
    decoded = modbus_sim.decode_telemetry_registers(regs)
    return {
        "protocol": "MODBUS_TCP",
        "holding_registers": regs,
        "decoded_telemetry": decoded
    }

@router.get("/protocols/opc-ua/nodes")
def poll_opc_ua_nodes():
    sample = {
        "suction_pressure_bar": 1.5,
        "discharge_pressure_bar": 8.2,
        "flow_m3_h": 120.0,
        "pump_speed_rpm": 2950.0,
        "electrical_power_kw": 30.0,
        "bearing_temp_de_celsius": 45.0,
        "bearing_temp_nde_celsius": 42.0,
        "fluid_temp_celsius": 25.0,
        "vibration_rms": 1.2
    }
    payload = opc_sim.build_monitored_items_payload(sample)
    return payload

@router.get("/protocols/sparkplug-b/ddata")
def poll_sparkplug_b():
    sample = {
        "suction_pressure_bar": 1.5,
        "discharge_pressure_bar": 8.2,
        "flow_m3_h": 120.0,
        "pump_speed_rpm": 2950.0,
        "electrical_power_kw": 30.0,
        "bearing_temp_de_celsius": 45.0,
        "bearing_temp_nde_celsius": 42.0,
        "fluid_temp_celsius": 25.0,
        "vibration_rms": 1.2
    }
    return sparkplug_sim.generate_ddata_payload(sample)
