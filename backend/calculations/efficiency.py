"""
HydroGuard AI — Deterministic Hydraulic Calculations
Module: efficiency.py
Description: Total Dynamic Head (TDH), Hydraulic Power, and Instantaneous Pump Efficiency.
"""

from typing import Dict, Any, Optional
import math
from backend.calculations.npsh import GRAVITY_ACCEL, WATER_DENSITY_STANDARD

def calculate_total_dynamic_head(
    p_discharge_pa: float,
    p_suction_pa: float,
    flow_m3_h: float,
    suction_diam_m: float = 0.15,
    discharge_diam_m: float = 0.10,
    delta_z_m: float = 0.0,
    density_kg_m3: float = WATER_DENSITY_STANDARD,
    g: float = GRAVITY_ACCEL
) -> Dict[str, Any]:
    """
    Calculate Total Dynamic Head (TDH) in meters:
    H = (P_d - P_s) / (rho * g) + delta_z + (v_d^2 - v_s^2) / (2 * g)
    """
    if p_discharge_pa < 0 or p_suction_pa < 0:
        raise ValueError(f"Pressures must be non-negative. Received P_s={p_suction_pa} Pa, P_d={p_discharge_pa} Pa")
    if p_discharge_pa < p_suction_pa:
        # Pump is operating in unpressurized or reverse differential state
        pass
    if density_kg_m3 <= 0 or suction_diam_m <= 0 or discharge_diam_m <= 0:
        raise ValueError("Physical dimensions and density must be positive.")
    if flow_m3_h < 0:
        raise ValueError(f"Flow rate cannot be negative. Received {flow_m3_h}")

    flow_m3_s = flow_m3_h / 3600.0
    area_s = math.pi * ((suction_diam_m / 2.0) ** 2)
    area_d = math.pi * ((discharge_diam_m / 2.0) ** 2)

    v_s = flow_m3_s / area_s
    v_d = flow_m3_s / area_d

    head_pressure = (p_discharge_pa - p_suction_pa) / (density_kg_m3 * g)
    head_velocity = ((v_d ** 2) - (v_s ** 2)) / (2.0 * g)
    total_head = head_pressure + delta_z_m + head_velocity

    return {
        "total_head_m": round(total_head, 3),
        "pressure_head_m": round(head_pressure, 3),
        "velocity_head_diff_m": round(head_velocity, 4),
        "elevation_head_m": round(delta_z_m, 3),
        "suction_velocity_m_s": round(v_s, 3),
        "discharge_velocity_m_s": round(v_d, 3),
        "differential_pressure_kpa": round((p_discharge_pa - p_suction_pa) / 1000.0, 2)
    }

def calculate_pump_efficiency(
    p_discharge_pa: float,
    p_suction_pa: float,
    flow_m3_h: float,
    electrical_power_kw: float,
    motor_efficiency_factor: float = 0.95,
    suction_diam_m: float = 0.15,
    discharge_diam_m: float = 0.10,
    delta_z_m: float = 0.0,
    density_kg_m3: float = WATER_DENSITY_STANDARD,
    g: float = GRAVITY_ACCEL
) -> Dict[str, Any]:
    """
    Calculate Instantaneous Pump Efficiency (eta):
    P_hydraulic (W) = rho * g * Q (m^3/s) * H (m)
    P_shaft (W) = P_electrical (W) * motor_efficiency
    eta_pump (%) = (P_hydraulic / P_shaft) * 100
    """
    if electrical_power_kw <= 0:
        raise ValueError(f"Electrical power must be strictly positive. Received {electrical_power_kw} kW")
    if not (0.5 <= motor_efficiency_factor <= 1.0):
        raise ValueError(f"Motor efficiency factor out of plausible range: {motor_efficiency_factor}")

    head_res = calculate_total_dynamic_head(
        p_discharge_pa=p_discharge_pa,
        p_suction_pa=p_suction_pa,
        flow_m3_h=flow_m3_h,
        suction_diam_m=suction_diam_m,
        discharge_diam_m=discharge_diam_m,
        delta_z_m=delta_z_m,
        density_kg_m3=density_kg_m3,
        g=g
    )

    total_head_m = max(0.0, head_res["total_head_m"])
    flow_m3_s = flow_m3_h / 3600.0

    hydraulic_power_w = density_kg_m3 * g * flow_m3_s * total_head_m
    hydraulic_power_kw = hydraulic_power_w / 1000.0
    shaft_power_kw = electrical_power_kw * motor_efficiency_factor

    if shaft_power_kw > 0:
        efficiency_pct = (hydraulic_power_kw / shaft_power_kw) * 100.0
    else:
        efficiency_pct = 0.0

    # Physical validity clamping & anomaly detection
    is_anomaly = False
    anomaly_reason = None
    if efficiency_pct > 96.0:
        is_anomaly = True
        anomaly_reason = f"Efficiency ({efficiency_pct:.1f}%) exceeds physical thermodynamic upper bounds for centrifugal pumps. Check flow or power sensor calibration."
        efficiency_pct = min(100.0, efficiency_pct)
    elif efficiency_pct < 20.0 and flow_m3_h > 10.0:
        is_anomaly = True
        anomaly_reason = f"Severely depressed efficiency ({efficiency_pct:.1f}%). Possible internal recirculation, severe impeller wear, or flow bypassed."

    # BEP degradation classification (assuming nominal design efficiency is ~78-85%)
    nominal_bep_efficiency = 82.0
    efficiency_degradation_pct = max(0.0, nominal_bep_efficiency - efficiency_pct)

    return {
        "efficiency_pct": round(efficiency_pct, 2),
        "hydraulic_power_kw": round(hydraulic_power_kw, 2),
        "shaft_power_kw": round(shaft_power_kw, 2),
        "electrical_power_kw": round(electrical_power_kw, 2),
        "total_head_m": round(total_head_m, 2),
        "flow_m3_h": round(flow_m3_h, 2),
        "efficiency_degradation_pct": round(efficiency_degradation_pct, 2),
        "is_efficiency_anomaly": is_anomaly,
        "anomaly_reason": anomaly_reason
    }
