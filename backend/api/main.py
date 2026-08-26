"""
HydroGuard AI — FastAPI Application Entrypoint
Module: main.py
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import json
import asyncio
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.api.routes import router as api_router
from backend.models.telemetry import PumpTelemetry
from backend.agents.orchestrator import DiagnosticOrchestrator

app = FastAPI(
    title="HydroGuard AI — Industrial Hydraulic Pump Diagnostic Engine",
    description="Deterministic physics, frequency-domain FFT vibration, and agentic maintenance orchestration for multistage centrifugal pumps.",
    version="2.4.0-PROD"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# WebSocket for real-time SCADA telemetry streaming
orchestrator = DiagnosticOrchestrator()

@app.websocket("/ws/telemetry")
async def websocket_telemetry_stream(websocket: WebSocket):
    await websocket.accept()
    # Continuous simulated telemetry stream with realistic variations
    t_step = 0
    try:
        while True:
            t_step += 1
            # Default to Pump P-204 condition with slight dynamic oscillation
            p_suc = 0.45 + (0.02 * (t_step % 5 - 2))
            p_disch = 7.8 + (0.05 * (t_step % 3 - 1))
            flow = 118.0 + (0.8 * (t_step % 4 - 2))
            
            telemetry = PumpTelemetry(
                pump_id="P-204",
                timestamp_iso=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                suction_pressure_bar=round(p_suc, 3),
                discharge_pressure_bar=round(p_disch, 2),
                flow_m3_h=round(flow, 1),
                fluid_temp_celsius=25.0,
                pump_speed_rpm=2950.0,
                electrical_power_kw=28.5,
                bearing_temp_de_celsius=48.2,
                bearing_temp_nde_celsius=44.1,
                impeller_vanes=5,
                npshr_m=4.2,
                protocol_source="MODBUS_TCP"
            )
            
            diag = orchestrator.run_full_diagnosis(telemetry=telemetry)
            
            payload = {
                "telemetry": telemetry.model_dump(),
                "diagnosis": diag.model_dump()
            }
            await websocket.send_json(payload)
            await asyncio.sleep(2.0)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass

# Mount static frontend build if present
frontend_dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist_dir):
    app.mount("/", StaticFiles(directory=frontend_dist_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
