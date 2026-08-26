"""
HydroGuard AI — Core Data Models & Schemas
Module: telemetry.py
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class PumpTelemetry(BaseModel):
    pump_id: str = Field(default="P-204", description="Pump asset identifier")
    timestamp_iso: str = Field(default="", description="ISO 8601 timestamp")
    
    # Hydraulic sensors
    suction_pressure_bar: float = Field(..., description="Suction pressure in bar gauge/abs")
    discharge_pressure_bar: float = Field(..., description="Discharge pressure in bar gauge/abs")
    flow_m3_h: float = Field(..., description="Volumetric flow rate in m^3/h")
    fluid_temp_celsius: float = Field(default=25.0, description="Fluid operating temperature in °C")
    
    # Mechanical / Electrical sensors
    pump_speed_rpm: float = Field(default=2950.0, description="Rotational speed in RPM")
    electrical_power_kw: float = Field(..., description="Motor active electrical power in kW")
    bearing_temp_de_celsius: float = Field(default=45.0, description="Drive End bearing temperature °C")
    bearing_temp_nde_celsius: float = Field(default=42.0, description="Non-Drive End bearing temperature °C")
    motor_current_a: Optional[float] = Field(default=45.0, description="Motor current in Amperes")
    
    # Physical / Design parameters
    impeller_vanes: int = Field(default=5, description="Number of impeller vanes")
    npshr_m: float = Field(default=4.2, description="Pump manufacturer required NPSHr in meters")
    suction_pipe_diam_m: float = Field(default=0.15, description="Suction nozzle inner diameter (m)")
    discharge_pipe_diam_m: float = Field(default=0.10, description="Discharge nozzle inner diameter (m)")
    
    # Raw or simulated vibration time-series (optional)
    vibration_time_series: Optional[List[float]] = Field(default=None, description="Vibration signal buffer")
    sampling_rate_hz: int = Field(default=12000, description="Vibration sampling rate")

    # Protocol metadata
    protocol_source: str = Field(default="MODBUS_TCP", description="MODBUS_TCP, OPC_UA, MQTT_SPARKPLUG_B, MANUAL")
    quality_flag: str = Field(default="GOOD", description="GOOD, UNCERTAIN, BAD")

class CalculatedMetrics(BaseModel):
    npsha_m: float
    npshr_m: float
    npsh_margin_m: float
    npsh_status: str
    cavitation_risk_index: float
    total_head_m: float
    differential_pressure_kpa: float
    hydraulic_power_kw: float
    pump_efficiency_pct: float
    efficiency_degradation_pct: float
    
    # Vibration features
    overall_rms_mm_s: float
    f_1x_hz: float
    f_vpf_hz: float
    amp_1x_mm_s: float
    amp_2x_mm_s: float
    amp_vpf_mm_s: float
    cavitation_1_5khz_energy_rms: float
    cavitation_spectral_ratio: float
    is_cavitation_spectral_elevated: bool

class HypothesisItem(BaseModel):
    hypothesis_id: str
    name: str
    probability_pct: float
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, HEALTHY
    confidence_interval_pct: float
    primary_mechanism: str
    supporting_evidence: List[str]
    conflicting_evidence: List[str]
    recommended_technician_action: str

class DiagnosticResult(BaseModel):
    asset_id: str
    timestamp_iso: str
    operating_state: str  # NORMAL, TRANSIENT, DEGRADED, ALARM, CRITICAL
    hypotheses: List[HypothesisItem]
    top_hypothesis: HypothesisItem
    next_verification_action: Dict[str, Any]
    iso_10816_vibration_zone: str  # Zone A, Zone B, Zone C, Zone D
    calculated_metrics: CalculatedMetrics
    ai_engineering_synthesis: str
    safety_boundary_statement: str
