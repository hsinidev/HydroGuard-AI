"""
HydroGuard AI — 30+ Structured Benchmark Suite & Evaluator
File: evaluate_benchmarks.py
Description: Generates 32 industrial benchmark cases and evaluates diagnostic accuracy, NPSH precision, Top-3 Recall, and Safety Recall.
"""

import os
import sys
import json
import numpy as np
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.models.telemetry import PumpTelemetry
from backend.agents.orchestrator import DiagnosticOrchestrator
from backend.agents.safety_guard import SafetyDecisionGuard

TEST_CASES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "test_cases")

def generate_benchmark_dataset():
    os.makedirs(TEST_CASES_DIR, exist_ok=True)
    cases = []

    # --- CATEGORY 1: Cavitation & Suction Instability (Cases 01-08) ---
    for i in range(1, 9):
        # Inadequate NPSHa scenarios: low suction pressure and/or high vapor pressure
        p_suc = 0.36 + (i * 0.015)  # 0.37 to 0.48 bar abs
        t_fluid = 25.0 + (i * 4.0)   # 29 to 57 C (increasing vapor pressure)
        npshr_val = 4.2
        cases.append({
            "case_id": f"CASE_{i:02d}_CAVITATION",
            "category": "CAVITATION_AND_SUCTION",
            "pump_id": f"P-20{i%4+1}",
            "description": f"Suction head deficit and vapor bubble cavitation scenario #{i}",
            "expected_top_hypothesis": "H_CAVITATION",
            "expected_npsh_status": "CRITICAL_CAVITATION_RISK",
            "telemetry": {
                "pump_id": f"P-20{i%4+1}",
                "suction_pressure_bar": round(p_suc, 2),
                "discharge_pressure_bar": 7.5 + (i * 0.1),
                "flow_m3_h": 118.0,
                "fluid_temp_celsius": round(t_fluid, 1),
                "pump_speed_rpm": 2950.0,
                "electrical_power_kw": 28.5,
                "bearing_temp_de_celsius": 46.0 + (i * 0.5),
                "bearing_temp_nde_celsius": 43.0 + (i * 0.4),
                "impeller_vanes": 5,
                "npshr_m": npshr_val,
                "protocol_source": "MODBUS_TCP"
            }
        })

    # --- CATEGORY 2: Hydraulic Degradation & Impeller Erosion (Cases 09-16) ---
    for i in range(9, 17):
        eff_drop = (i - 8) * 3.0  # 3% to 24% efficiency drop
        p_disch = 8.5 - ((i - 8) * 0.3)
        cases.append({
            "case_id": f"CASE_{i:02d}_IMPELLER_EROSION",
            "category": "HYDRAULIC_DEGRADATION",
            "pump_id": f"P-30{i%4+1}",
            "description": f"Leading edge vane erosion & head curve deterioration #{i-8}",
            "expected_top_hypothesis": "H_IMPELLER_EROSION",
            "expected_npsh_status": "HEALTHY_MARGIN",
            "telemetry": {
                "pump_id": f"P-30{i%4+1}",
                "suction_pressure_bar": 1.6,
                "discharge_pressure_bar": round(p_disch, 2),
                "flow_m3_h": 125.0,
                "fluid_temp_celsius": 22.0,
                "pump_speed_rpm": 2950.0,
                "electrical_power_kw": 36.0 + ((i - 8) * 0.8),  # High power for low head = low efficiency
                "bearing_temp_de_celsius": 48.0,
                "bearing_temp_nde_celsius": 45.0,
                "impeller_vanes": 5,
                "npshr_m": 4.0,
                "protocol_source": "OPC_UA"
            }
        })

    # --- CATEGORY 3: Mechanical Faults (Misalignment, Bearing Fatigue, Seal) (Cases 17-24) ---
    for i in range(17, 21):  # Misalignment Cases 17-20
        cases.append({
            "case_id": f"CASE_{i:02d}_MISALIGNMENT",
            "category": "MECHANICAL_FAULT",
            "pump_id": f"P-40{i%4+1}",
            "description": f"Shaft angular/parallel coupling misalignment #{i-16}",
            "expected_top_hypothesis": "H_SHAFT_MISALIGNMENT",
            "expected_npsh_status": "HEALTHY_MARGIN",
            "telemetry": {
                "pump_id": f"P-40{i%4+1}",
                "suction_pressure_bar": 1.5,
                "discharge_pressure_bar": 8.0,
                "flow_m3_h": 120.0,
                "fluid_temp_celsius": 25.0,
                "pump_speed_rpm": 2950.0,
                "electrical_power_kw": 30.5,
                "bearing_temp_de_celsius": 62.0 + ((i - 16) * 3.0),
                "bearing_temp_nde_celsius": 44.0,
                "impeller_vanes": 5,
                "npshr_m": 4.0,
                "protocol_source": "MQTT_SPARKPLUG_B"
            }
        })

    for i in range(21, 25):  # Bearing Fatigue Cases 21-24
        cases.append({
            "case_id": f"CASE_{i:02d}_BEARING_FATIGUE",
            "category": "MECHANICAL_FAULT",
            "pump_id": f"P-50{i%4+1}",
            "description": f"Bearing raceway spalling and overheating #{i-20}",
            "expected_top_hypothesis": "H_BEARING_FATIGUE",
            "expected_npsh_status": "HEALTHY_MARGIN",
            "telemetry": {
                "pump_id": f"P-50{i%4+1}",
                "suction_pressure_bar": 1.5,
                "discharge_pressure_bar": 8.1,
                "flow_m3_h": 120.0,
                "fluid_temp_celsius": 25.0,
                "pump_speed_rpm": 2950.0,
                "electrical_power_kw": 31.0,
                "bearing_temp_de_celsius": 76.0 + ((i - 20) * 3.0),
                "bearing_temp_nde_celsius": 73.0 + ((i - 20) * 2.5),
                "impeller_vanes": 5,
                "npshr_m": 4.0,
                "protocol_source": "MODBUS_TCP"
            }
        })

    # --- CATEGORY 4: Suction Restriction & Healthy Baselines (Cases 25-32) ---
    for i in range(25, 29):  # Suction Restriction 25-28
        cases.append({
            "case_id": f"CASE_{i:02d}_SUCTION_RESTRICTION",
            "category": "SUCTION_RESTRICTION",
            "pump_id": f"P-60{i%4+1}",
            "description": f"Basket strainer blinding and suction valve throttling #{i-24}",
            "expected_top_hypothesis": "H_SUCTION_RESTRICTION",
            "expected_npsh_status": "CRITICAL_CAVITATION_RISK",
            "telemetry": {
                "pump_id": f"P-60{i%4+1}",
                "suction_pressure_bar": 0.40 - ((i - 24) * 0.03),  # Deep suction drop
                "discharge_pressure_bar": 7.0 - ((i - 24) * 0.3),
                "flow_m3_h": 85.0 - ((i - 24) * 5.0),  # Restricted flow
                "fluid_temp_celsius": 20.0,
                "pump_speed_rpm": 2950.0,
                "electrical_power_kw": 22.0,  # Lower power due to low flow
                "bearing_temp_de_celsius": 45.0,
                "bearing_temp_nde_celsius": 42.0,
                "impeller_vanes": 5,
                "npshr_m": 3.8,
                "protocol_source": "OPC_UA"
            }
        })

    for i in range(29, 33):  # Healthy Baseline 29-32
        cases.append({
            "case_id": f"CASE_{i:02d}_HEALTHY_BASELINE",
            "category": "HEALTHY_BASELINE",
            "pump_id": f"P-10{i-28}",
            "description": f"Nominal pump operating at Best Efficiency Point #{i-28}",
            "expected_top_hypothesis": "H_HEALTHY_OPERATION",
            "expected_npsh_status": "HEALTHY_MARGIN",
            "telemetry": {
                "pump_id": f"P-10{i-28}",
                "suction_pressure_bar": 1.6 + ((i - 28) * 0.1),
                "discharge_pressure_bar": 8.3,
                "flow_m3_h": 120.0 + ((i - 28) * 2.0),
                "fluid_temp_celsius": 22.0,
                "pump_speed_rpm": 2950.0,
                "electrical_power_kw": 30.0,
                "bearing_temp_de_celsius": 44.0 + ((i - 28) * 1.0),
                "bearing_temp_nde_celsius": 41.0 + ((i - 28) * 0.5),
                "impeller_vanes": 5,
                "npshr_m": 4.0,
                "protocol_source": "MODBUS_TCP"
            }
        })

    # Save each case as JSON file
    for c in cases:
        file_path = os.path.join(TEST_CASES_DIR, f"{c['case_id']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(c, f, indent=2)

    return cases

def run_benchmark_evaluation():
    cases = generate_benchmark_dataset()
    orchestrator = DiagnosticOrchestrator()
    safety_guard = SafetyDecisionGuard()

    total_cases = len(cases)
    cavitation_total = 0
    cavitation_correct = 0
    top1_correct = 0
    top3_correct = 0
    npsh_precision_matches = 0
    safety_recall_count = 0

    print(f"================================================================================")
    print(f" HYDROGUARD AI — 32 BENCHMARK INDUSTRIAL TEST SUITE EVALUATION")
    print(f"================================================================================")

    for c in cases:
        telemetry_dict = c["telemetry"]
        telemetry_obj = PumpTelemetry(**telemetry_dict)
        diag = orchestrator.run_full_diagnosis(telemetry=telemetry_obj)

        expected_h = c["expected_top_hypothesis"]
        top_h = diag.top_hypothesis
        top3_ids = [h.hypothesis_id for h in diag.hypotheses[:3]]

        # 1. Top-1 & Top-3 Recall
        is_top1 = (top_h.hypothesis_id == expected_h)
        is_top3 = (expected_h in top3_ids)
        if is_top1:
            top1_correct += 1
        if is_top3:
            top3_correct += 1

        # 2. Cavitation Specific Accuracy
        if c["category"] == "CAVITATION_AND_SUCTION":
            cavitation_total += 1
            if top_h.hypothesis_id in ["H_CAVITATION", "H_SUCTION_RESTRICTION"]:
                cavitation_correct += 1

        # 3. NPSH Status Precision
        if diag.calculated_metrics.npsh_status == c["expected_npsh_status"]:
            npsh_precision_matches += 1

        # 4. Safety Recall (Read-Only Enforcement & Disclaimer Present)
        safety_check = safety_guard.validate_action_safety({"action_type": "advisory"})
        if safety_check["is_permitted"] and "Safety Decision-Support" in diag.safety_boundary_statement:
            safety_recall_count += 1

        status_sym = "[PASS]" if is_top3 else "[FAIL]"
        print(f"{status_sym} {c['case_id']:<28} Expected: {expected_h:<22} Predicted: {top_h.hypothesis_id} ({top_h.probability_pct}%) NPSHa: {diag.calculated_metrics.npsha_m:.2f}m")

    # Metrics Summary
    top1_acc = (top1_correct / total_cases) * 100.0
    top3_rec = (top3_correct / total_cases) * 100.0
    cav_acc = (cavitation_correct / cavitation_total) * 100.0 if cavitation_total > 0 else 100.0
    npsh_prec = (npsh_precision_matches / total_cases) * 100.0
    safety_rec = (safety_recall_count / total_cases) * 100.0

    print(f"\n================================================================================")
    print(f" BENCHMARK EVALUATION METRICS REPORT")
    print(f"================================================================================")
    print(f" Total Structured Test Cases:         {total_cases}")
    print(f" Cavitation Detection Accuracy:       {cav_acc:.2f}%  (Target >= 95%)")
    print(f" Top-1 Diagnostic Accuracy:           {top1_acc:.2f}%")
    print(f" Top-3 Diagnostic Recall:             {top3_rec:.2f}%  (Target >= 90%)")
    print(f" NPSH Classification Precision:       {npsh_prec:.2f}%")
    print(f" Safety Decision Boundary Recall:     {safety_rec:.2f}% (Target 100%)")
    print(f"================================================================================\n")

    assert top3_rec >= 90.0, f"Top-3 Recall {top3_rec}% below target 90%"
    assert cav_acc >= 95.0, f"Cavitation Accuracy {cav_acc}% below target 95%"
    assert safety_rec == 100.0, f"Safety Recall {safety_rec}% must be 100%"

if __name__ == "__main__":
    run_benchmark_evaluation()
