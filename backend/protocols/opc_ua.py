"""
HydroGuard AI — Protocol Bridge: OPC UA (IEC 62541) Node Subscription Simulator
Module: opc_ua.py
"""

from typing import Dict, Any, List
import datetime

# Standard OPC UA Information Model for Industrial Pumps (ns=2;s=...)
OPC_UA_NODE_MAP = {
    "ns=2;s=Pump.P204.SuctionPressure": "suction_pressure_bar",
    "ns=2;s=Pump.P204.DischargePressure": "discharge_pressure_bar",
    "ns=2;s=Pump.P204.FlowRate": "flow_m3_h",
    "ns=2;s=Pump.P204.Speed": "pump_speed_rpm",
    "ns=2;s=Pump.P204.ElectricalPower": "electrical_power_kw",
    "ns=2;s=Pump.P204.BearingTemperatureDE": "bearing_temp_de_celsius",
    "ns=2;s=Pump.P204.BearingTemperatureNDE": "bearing_temp_nde_celsius",
    "ns=2;s=Pump.P204.FluidTemperature": "fluid_temp_celsius",
    "ns=2;s=Pump.P204.VibrationRMS": "vibration_rms"
}

class OPCUASimulator:
    def __init__(self, namespace_index: int = 2, pump_id: str = "P-204"):
        self.namespace_index = namespace_index
        self.pump_id = pump_id

    def build_monitored_items_payload(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate standard IEC 62541 DataValue notifications for monitored nodes.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        nodes_data = []

        mapping = {
            "SuctionPressure": ("Double", telemetry.get("suction_pressure_bar", 1.5), "bar"),
            "DischargePressure": ("Double", telemetry.get("discharge_pressure_bar", 8.2), "bar"),
            "FlowRate": ("Double", telemetry.get("flow_m3_h", 120.0), "m3/h"),
            "Speed": ("Double", telemetry.get("pump_speed_rpm", 2950.0), "RPM"),
            "ElectricalPower": ("Double", telemetry.get("electrical_power_kw", 30.0), "kW"),
            "BearingTemperatureDE": ("Double", telemetry.get("bearing_temp_de_celsius", 45.0), "°C"),
            "BearingTemperatureNDE": ("Double", telemetry.get("bearing_temp_nde_celsius", 42.0), "°C"),
            "FluidTemperature": ("Double", telemetry.get("fluid_temp_celsius", 25.0), "°C"),
            "VibrationRMS": ("Double", telemetry.get("vibration_rms", 1.2), "mm/s")
        }

        for name, (datatype, val, unit) in mapping.items():
            nodes_data.append({
                "node_id": f"ns={self.namespace_index};s=Pump.{self.pump_id}.{name}",
                "datatype": datatype,
                "engineering_unit": unit,
                "source_timestamp": now,
                "server_timestamp": now,
                "status_code": "Good (0x00000000)",
                "value": val
            })

        return {
            "subscription_id": 1042,
            "publish_time": now,
            "pump_id": self.pump_id,
            "monitored_nodes": nodes_data
        }

    def decode_opc_ua_notification(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert OPC UA monitored items payload into HydroGuard telemetry format.
        """
        telemetry = {
            "pump_id": payload.get("pump_id", self.pump_id),
            "timestamp_iso": payload.get("publish_time", datetime.datetime.now(datetime.timezone.utc).isoformat()),
            "protocol_source": "OPC_UA",
            "quality_flag": "GOOD"
        }

        for item in payload.get("monitored_nodes", []):
            node_id = item.get("node_id", "")
            val = item.get("value", 0.0)
            if node_id in OPC_UA_NODE_MAP:
                field = OPC_UA_NODE_MAP[node_id]
                telemetry[field] = val

        return telemetry
