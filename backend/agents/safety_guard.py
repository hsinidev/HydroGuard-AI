"""
HydroGuard AI — Safety Decision-Support & Legal Boundary Guard
Module: safety_guard.py
Description: Enforces strict Read-Only boundary, OSHA 1910.147 LOTO procedures, and ISO compliance framing.
"""

from typing import Dict, Any, List

SAFETY_LEGAL_DISCLAIMER = (
    "HydroGuard AI operates strictly as a Safety Decision-Support and Predictive Maintenance Advisory System. "
    "The software operates across a read-only physical boundary and has no write-access to pump starters, "
    "variable frequency drives (VFDs), motor control centers (MCC), or actuated valves. "
    "All physical interventions must be authorized by licensed plant rotating-equipment engineers "
    "and executed in accordance with OSHA 1910.147 (The Control of Hazardous Energy / LOTO) and site safety procedures."
)

class SafetyDecisionGuard:
    def get_loto_procedure(self, equipment_tag: str = "P-204") -> Dict[str, Any]:
        """
        Generate OSHA 1910.147 compliant Lockout/Tagout (LOTO) safety steps for pump isolation.
        """
        return {
            "equipment_tag": equipment_tag,
            "standard_reference": "OSHA 29 CFR 1910.147 / NFPA 70E",
            "procedure_id": f"LOTO-SOP-{equipment_tag}",
            "energy_sources_to_isolate": [
                {"type": "Electrical", "source": f"{equipment_tag} 480V 3-Phase Motor Feeder Breaker at MCC-02", "isolation_device": "Padlock with Danger Tag & Hasps"},
                {"type": "Hydraulic Pressure", "source": "Suction Isolation Gate Valve (HV-204-S)", "isolation_device": "Chain & Padlock in Closed Position"},
                {"type": "Hydraulic Pressure", "source": "Discharge Check & Isolation Valve (HV-204-D)", "isolation_device": "Chain & Padlock in Closed Position"},
                {"type": "Thermal / Residual Fluid", "source": "Casing Drain & Seal Flush Line", "isolation_device": "Bleed valve opened to depressurize casing into sump"}
            ],
            "execution_steps": [
                "1. NOTIFY: Notify operations control room and area supervisor of intention to isolate pump.",
                "2. SHUTDOWN: Execute normal sequence stop command from DCS / SCADA control desk.",
                "3. ELECTRICAL ISOLATION: Open 480V breaker at MCC-02, rack out breaker, apply padlock and personalized Danger Tag.",
                "4. ZERO-ENERGY VERIFICATION: Test motor start push-button locally to verify zero movement; perform electrical voltage meter test (Live-Dead-Live test).",
                "5. HYDRAULIC ISOLATION: Close suction and discharge isolation valves fully; apply lockouts.",
                "6. DEPRESSURIZATION: Open casing drain needle valve into drain pan until pressure drops to 0.0 bar gauge.",
                "7. PROCEED: Maintenance technician verifies zero pressure gauge reading before unbolting components."
            ]
        }

    def validate_action_safety(self, action_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify that proposed recommendation adheres to the strict Read-Only boundary.
        """
        forbidden_keywords = ["actuate_valve", "start_motor", "stop_motor", "override_interlock", "write_modbus_register", "energize"]
        action_name = str(action_request.get("action_type", "")).lower()

        for kw in forbidden_keywords:
            if kw in action_name:
                return {
                    "is_permitted": False,
                    "reason": f"Action '{action_name}' violates the strict Read-Only Safety Boundary. Automated physical control manipulation is prohibited.",
                    "boundary_enforcement": "INTERVENTION_REJECTED"
                }

        return {
            "is_permitted": True,
            "reason": "Diagnostic advisory action conforms to Read-Only Decision-Support constraints.",
            "boundary_enforcement": "PERMITTED_ADVISORY"
        }
