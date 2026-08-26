"""
HydroGuard AI — ISO 55000 Maintenance Work Order Generator
Module: work_order.py
Description: Generates structured, printable industrial work orders with BOM, LOTO, and diagnostic logs.
"""

from typing import Dict, Any, List
import datetime
from backend.models.telemetry import HypothesisItem, CalculatedMetrics, PumpTelemetry

class WorkOrderGenerator:
    def generate_work_order(
        self,
        telemetry: PumpTelemetry,
        metrics: CalculatedMetrics,
        top_hypothesis: HypothesisItem,
        next_step: Dict[str, Any],
        loto_sop: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive ISO 55000 asset management compliant maintenance work order.
        """
        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        wo_number = f"WO-{telemetry.pump_id}-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}"

        # Determine parts BOM based on failure hypothesis
        bom = []
        if top_hypothesis.hypothesis_id in ["H_CAVITATION", "H_SUCTION_RESTRICTION"]:
            bom = [
                {"part_no": "STR-FLT-204", "description": "316SS Basket Strainer Replacement Element (40 Mesh)", "qty": 1, "stock_status": "In Stock (Bay 4, Bin 12)"},
                {"part_no": "GSK-SUC-6IN", "description": "6-inch ANSI 150# Spiral Wound Suction Flange Gasket (PTFE/Graphite)", "qty": 2, "stock_status": "In Stock (Aisle 2)"},
                {"part_no": "VLV-SEAL-PKG", "description": "Suction Valve Stem Packing Set (Braided Graphite)", "qty": 1, "stock_status": "In Stock"}
            ]
        elif top_hypothesis.hypothesis_id == "H_SHAFT_MISALIGNMENT":
            bom = [
                {"part_no": "CPL-SPD-204", "description": "Flexible Coupling Elastomeric Spider Element (95 Shore A)", "qty": 1, "stock_status": "In Stock (Bin C-4)"},
                {"part_no": "SHM-SS-KIT", "description": "Precision Stainless Steel Pre-Cut Shim Assortment (0.05 - 1.0mm)", "qty": 1, "stock_status": "In Stock"},
                {"part_no": "BLT-GR8-M16", "description": "Grade 8.8 High-Strength Motor Hold-Down Foundation Bolts M16x80", "qty": 4, "stock_status": "In Stock"}
            ]
        elif top_hypothesis.hypothesis_id == "H_BEARING_FATIGUE":
            bom = [
                {"part_no": "BRG-SKF-6312", "description": "SKF 6312-2Z Deep Groove Radial Ball Bearing (Drive End)", "qty": 1, "stock_status": "In Stock (Aisle 8)"},
                {"part_no": "BRG-SKF-7312", "description": "SKF 7312-BECBM Angular Contact Thrust Bearing Pair (Non-Drive End)", "qty": 1, "stock_status": "In Stock"},
                {"part_no": "OIL-ISO-VG46", "description": "Mobil DTE Heavy Medium ISO VG 46 Synthetic Turbine/Pump Oil (5L)", "qty": 2, "stock_status": "In Stock"}
            ]
        elif top_hypothesis.hypothesis_id == "H_IMPELLER_EROSION":
            bom = [
                {"part_no": "IMP-SS316-P204", "description": "Enclosed 5-Vane SS316 Impeller Assembly (210mm Trim)", "qty": 1, "stock_status": "Available via Central Warehouse (24h Delivery)"},
                {"part_no": "RNG-WEAR-P204", "description": "Bronze Casing Case Wear Ring Set (Front & Back)", "qty": 2, "stock_status": "In Stock"},
                {"part_no": "GSK-CAS-P204", "description": "Precision O-Ring Casing Split Flange Gasket Set", "qty": 1, "stock_status": "In Stock"}
            ]
        else:
            bom = [
                {"part_no": "PM-KIT-ANNUAL", "description": "Routine Annual Inspection and Fastener Kit", "qty": 1, "stock_status": "In Stock"}
            ]

        return {
            "work_order_number": wo_number,
            "standard_alignment": "ISO 55000:2014 Asset Management & ISO 10816-3 Vibration Evaluation",
            "asset_id": telemetry.pump_id,
            "asset_description": "Multistage Centrifugal Booster Pump (30 kW, 2950 RPM)",
            "plant_location": "Main Hydraulic Pumping Station — Bay B",
            "created_timestamp": now_str,
            "priority": "HIGH" if top_hypothesis.severity in ["CRITICAL", "HIGH"] else "ROUTINE",
            "condition_trigger": f"{top_hypothesis.name} (Diagnostic Probability: {top_hypothesis.probability_pct}%)",
            "diagnostic_summary": {
                "top_mechanism": top_hypothesis.primary_mechanism,
                "npsha_margin_m": metrics.npsh_margin_m,
                "pump_efficiency_pct": metrics.pump_efficiency_pct,
                "vibration_overall_rms": metrics.overall_rms_mm_s,
                "cavitation_1_5khz_energy_rms": metrics.cavitation_1_5khz_energy_rms
            },
            "next_best_verification": next_step,
            "bill_of_materials": bom,
            "loto_safety_procedure": loto_sop,
            "technician_sign_off": {
                "assigned_lead_technician": "Unassigned (Reliability Team)",
                "estimated_labor_hours": 3.5,
                "status": "APPROVED_FOR_DISPATCH"
            }
        }
