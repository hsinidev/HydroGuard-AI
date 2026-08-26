"""
HydroGuard AI — Protocol Bridge: MQTT Sparkplug B Telemetry Stream
Module: sparkplug_b.py
"""

from typing import Dict, Any, List
import datetime

class SparkplugBSimulator:
    def __init__(self, group_id: str = "PumpingStation-01", edge_node_id: str = "HydraulicBay-B", device_id: str = "P-204"):
        self.group_id = group_id
        self.edge_node_id = edge_node_id
        self.device_id = device_id
        self.seq = 0

    def generate_ddata_payload(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate standard Sparkplug B DDATA payload with typed metrics.
        Topic: spBv1.0/{group_id}/DDATA/{edge_node_id}/{device_id}
        """
        self.seq = (self.seq + 1) % 256
        now_ms = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)

        metrics = [
            {"name": "Suction/Pressure", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("suction_pressure_bar", 1.5)},
            {"name": "Discharge/Pressure", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("discharge_pressure_bar", 8.2)},
            {"name": "Flow/Volumetric", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("flow_m3_h", 120.0)},
            {"name": "Motor/Speed", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("pump_speed_rpm", 2950.0)},
            {"name": "Motor/Power", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("electrical_power_kw", 30.0)},
            {"name": "Bearing/TempDE", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("bearing_temp_de_celsius", 45.0)},
            {"name": "Bearing/TempNDE", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("bearing_temp_nde_celsius", 42.0)},
            {"name": "Fluid/Temperature", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("fluid_temp_celsius", 25.0)},
            {"name": "Vibration/OverallRMS", "timestamp": now_ms, "datatype": "Float", "value": telemetry.get("vibration_rms", 1.2)}
        ]

        topic = f"spBv1.0/{self.group_id}/DDATA/{self.edge_node_id}/{self.device_id}"

        return {
            "topic": topic,
            "timestamp": now_ms,
            "seq": self.seq,
            "metrics": metrics
        }

    def decode_ddata_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Sparkplug B metric payload back into HydroGuard telemetry fields.
        """
        metric_lookup = {
            "Suction/Pressure": "suction_pressure_bar",
            "Discharge/Pressure": "discharge_pressure_bar",
            "Flow/Volumetric": "flow_m3_h",
            "Motor/Speed": "pump_speed_rpm",
            "Motor/Power": "electrical_power_kw",
            "Bearing/TempDE": "bearing_temp_de_celsius",
            "Bearing/TempNDE": "bearing_temp_nde_celsius",
            "Fluid/Temperature": "fluid_temp_celsius",
            "Vibration/OverallRMS": "vibration_rms"
        }

        telemetry = {
            "pump_id": self.device_id,
            "timestamp_iso": datetime.datetime.fromtimestamp(payload.get("timestamp", 0) / 1000.0, datetime.timezone.utc).isoformat(),
            "protocol_source": "MQTT_SPARKPLUG_B",
            "quality_flag": "GOOD"
        }

        for m in payload.get("metrics", []):
            name = m.get("name")
            val = m.get("value")
            if name in metric_lookup:
                telemetry[metric_lookup[name]] = val

        return telemetry
