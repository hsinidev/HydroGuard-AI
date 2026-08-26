"""
HydroGuard AI Calculations Package
Deterministic hydraulic equations and physics validation.
"""
from backend.calculations.npsh import (
    calculate_npsha,
    evaluate_npsh_margin,
    water_vapor_pressure_antoine,
    GRAVITY_ACCEL,
    WATER_DENSITY_STANDARD
)
from backend.calculations.efficiency import (
    calculate_total_dynamic_head,
    calculate_pump_efficiency
)

__all__ = [
    "calculate_npsha",
    "evaluate_npsh_margin",
    "water_vapor_pressure_antoine",
    "calculate_total_dynamic_head",
    "calculate_pump_efficiency",
    "GRAVITY_ACCEL",
    "WATER_DENSITY_STANDARD"
]
