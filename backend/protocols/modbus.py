"""
HydroGuard AI — Protocol Bridge: Modbus TCP Simulator & Decoder
Module: modbus.py
Port 502 Register Mapping for Industrial Centrifugal Pumps.
"""

from typing import Dict, Any, List
import struct
import datetime

# Standard Modbus Holding Register Map (40001 - 40020)
# Scaled integers / 32-bit floats
MODBUS_REGISTER_MAP = {
    40001: ("SUCTION_PRESSURE_BAR_X100", "uint16", 0.01),
    40002: ("DISCHARGE_PRESSURE_BAR_X100", "uint16", 0.01),
    40003: ("FLOW_M3_H_X10", "uint16", 0.1),
    40004: ("PUMP_SPEED_RPM", "uint16", 1.0),
    40005: ("ELECTRICAL_POWER_KW_X10", "uint16", 0.1),
    40006: ("BEARING_TEMP_DE_C_X10", "uint16", 0.1),
    40007: ("BEARING_TEMP_NDE_C_X10", "uint16", 0.1),
    40008: ("FLUID_TEMP_C_X10", "uint16", 0.1),
    40009: ("VIBRATION_RMS_MM_S_X100", "uint16", 0.01),
    40010: ("QUALITY_AND_STATUS_FLAGS", "uint16", 1.0)
}

class ModbusTCPSimulator:
    def __init__(self, unit_id: int = 1):
        self.unit_id = unit_id

    def encode_telemetry_registers(self, telemetry: Dict[str, Any]) -> List[int]:
        """
        Encode engineering telemetry values into Modbus 16-bit register array.
        """
        registers = [0] * 10
        registers[0] = int(round(telemetry.get("suction_pressure_bar", 1.5) * 100))
        registers[1] = int(round(telemetry.get("discharge_pressure_bar", 8.2) * 100))
        registers[2] = int(round(telemetry.get("flow_m3_h", 120.0) * 10))
        registers[3] = int(round(telemetry.get("pump_speed_rpm", 2950.0)))
        registers[4] = int(round(telemetry.get("electrical_power_kw", 30.0) * 10))
        registers[5] = int(round(telemetry.get("bearing_temp_de_celsius", 45.0) * 10))
        registers[6] = int(round(telemetry.get("bearing_temp_nde_celsius", 42.0) * 10))
        registers[7] = int(round(telemetry.get("fluid_temp_celsius", 25.0) * 10))
        registers[8] = int(round(telemetry.get("vibration_rms", 1.2) * 100))
        registers[9] = 1 if telemetry.get("quality_flag", "GOOD") == "GOOD" else 0
        return registers

    def decode_telemetry_registers(self, registers: List[int], pump_id: str = "P-204") -> Dict[str, Any]:
        """
        Decode Modbus 16-bit holding registers into HydroGuard telemetry dictionary.
        """
        if len(registers) < 10:
            raise ValueError(f"Expected at least 10 Modbus registers, got {len(registers)}")

        return {
            "pump_id": pump_id,
            "timestamp_iso": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "suction_pressure_bar": registers[0] * 0.01,
            "discharge_pressure_bar": registers[1] * 0.01,
            "flow_m3_h": registers[2] * 0.1,
            "pump_speed_rpm": float(registers[3]),
            "electrical_power_kw": registers[4] * 0.1,
            "bearing_temp_de_celsius": registers[5] * 0.1,
            "bearing_temp_nde_celsius": registers[6] * 0.1,
            "fluid_temp_celsius": registers[7] * 0.1,
            "vibration_rms": registers[8] * 0.01,
            "quality_flag": "GOOD" if registers[9] == 1 else "BAD",
            "protocol_source": "MODBUS_TCP"
        }
