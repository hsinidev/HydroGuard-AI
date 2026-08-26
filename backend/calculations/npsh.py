"""
HydroGuard AI — Deterministic Hydraulic Calculations
Module: npsh.py
Description: NPSHa, NPSH Margin, and physical state evaluation.
"""

from typing import Dict, Any, Optional
import math

# Standard physical constants
GRAVITY_ACCEL = 9.80665  # m/s^2
WATER_DENSITY_STANDARD = 998.2  # kg/m^3 at 20 C

def water_vapor_pressure_antoine(temp_celsius: float) -> float:
    """
    Calculate saturation vapor pressure of water (in Pascals) using Antoine equation.
    T in Celsius: valid 1 - 100 C.
    P in mmHg: log10(P) = A - (B / (T + C))
    A = 8.07131, B = 1730.63, C = 233.426
    1 mmHg = 133.322 Pa
    """
    if temp_celsius < 0.0 or temp_celsius > 150.0:
        raise ValueError(f"Fluid temperature {temp_celsius}°C is outside realistic water operating range (0-150°C)")
    
    A = 8.07131
    B = 1730.63
    C = 233.426
    log10_p_mmhg = A - (B / (temp_celsius + C))
    p_mmhg = 10.0 ** log10_p_mmhg
    p_pascals = p_mmhg * 133.322387415
    return p_pascals

def calculate_npsha(
    p_suction_abs: float,
    p_vapor: Optional[float] = None,
    temp_celsius: float = 20.0,
    flow_m3_h: float = 120.0,
    suction_pipe_diam_m: float = 0.15,
    density_kg_m3: float = WATER_DENSITY_STANDARD,
    g: float = GRAVITY_ACCEL
) -> Dict[str, Any]:
    """
    Calculate Net Positive Suction Head Available (NPSHa).
    Formula:
        NPSHa = (P_suction_abs - P_vapor) / (rho * g) + (v_s^2 / (2 * g))

    Parameters:
        p_suction_abs: Absolute suction pressure at pump inlet in Pascals (Pa). Must be > 0.
        p_vapor: Fluid vapor pressure in Pa. If None, computed from water temperature.
        temp_celsius: Fluid temperature in °C (used if p_vapor is None).
        flow_m3_h: Volumetric flow rate in m^3/h.
        suction_pipe_diam_m: Inner diameter of suction nozzle in meters. Must be > 0.
        density_kg_m3: Fluid density in kg/m^3. Must be > 0.
        g: Gravitational acceleration in m/s^2.

    Returns:
        Dictionary containing NPSHa (m), static head component (m), velocity head component (m),
        and velocity (m/s).
    """
    if p_suction_abs <= 0:
        raise ValueError(f"Absolute suction pressure must be positive. Received {p_suction_abs} Pa")
    if density_kg_m3 <= 0:
        raise ValueError(f"Fluid density must be positive. Received {density_kg_m3} kg/m^3")
    if suction_pipe_diam_m <= 0:
        raise ValueError(f"Suction pipe diameter must be positive. Received {suction_pipe_diam_m} m")
    if flow_m3_h < 0:
        raise ValueError(f"Flow rate cannot be negative. Received {flow_m3_h} m^3/h")

    # Determine vapor pressure
    if p_vapor is None:
        p_vapor = water_vapor_pressure_antoine(temp_celsius)

    # Suction velocity v_s = Q / A
    flow_m3_s = flow_m3_h / 3600.0
    pipe_area_m2 = math.pi * ((suction_pipe_diam_m / 2.0) ** 2)
    velocity_suction = flow_m3_s / pipe_area_m2

    # Static head component
    head_static = (p_suction_abs - p_vapor) / (density_kg_m3 * g)
    
    # Velocity head component
    head_velocity = (velocity_suction ** 2) / (2.0 * g)

    npsha = head_static + head_velocity

    return {
        "npsha_m": round(npsha, 4),
        "head_static_m": round(head_static, 4),
        "head_velocity_m": round(head_velocity, 4),
        "suction_velocity_m_s": round(velocity_suction, 4),
        "p_suction_abs_pa": p_suction_abs,
        "p_vapor_pa": round(p_vapor, 2),
        "density_kg_m3": density_kg_m3,
        "is_flashing": p_suction_abs <= p_vapor
    }

def evaluate_npsh_margin(
    npsha_m: float,
    npshr_m: float,
    recommended_safety_margin_m: float = 1.5
) -> Dict[str, Any]:
    """
    Evaluate NPSH margin against pump required NPSHr.
    Status classifications:
      - 'CRITICAL_CAVITATION_RISK': margin < 0.5m
      - 'WARNING_LOW_MARGIN': 0.5m <= margin < recommended_safety_margin_m (1.5m)
      - 'HEALTHY_MARGIN': margin >= recommended_safety_margin_m
    """
    if npshr_m < 0:
        raise ValueError(f"NPSHr cannot be negative. Received {npshr_m} m")

    margin = npsha_m - npshr_m
    ratio = npsha_m / npshr_m if npshr_m > 0 else float("inf")

    if margin < 0.5:
        status = "CRITICAL_CAVITATION_RISK"
        severity = "HIGH"
        risk_score = min(1.0, max(0.7, 1.0 - (margin / 1.5)))
        message = f"NPSHa ({npsha_m:.2f} m) is critically close to or below NPSHr ({npshr_m:.2f} m). Severe sheet/cloud cavitation probable."
    elif margin < recommended_safety_margin_m:
        status = "WARNING_LOW_MARGIN"
        severity = "MEDIUM"
        risk_score = 0.4 + (0.3 * (1.5 - margin))
        message = f"NPSHa margin ({margin:.2f} m) is below recommended safety threshold of {recommended_safety_margin_m:.1f} m."
    else:
        status = "HEALTHY_MARGIN"
        severity = "NORMAL"
        risk_score = max(0.0, 0.2 - (margin / 10.0))
        message = f"Adequate NPSH margin ({margin:.2f} m). Hydraulic suction flow stable."

    return {
        "npsha_m": round(npsha_m, 3),
        "npshr_m": round(npshr_m, 3),
        "npsh_margin_m": round(margin, 3),
        "npsh_ratio": round(ratio, 3),
        "status": status,
        "severity": severity,
        "cavitation_risk_index": round(risk_score, 3),
        "message": message
    }
