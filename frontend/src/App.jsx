import React, { useState, useEffect } from 'react';
import {
  Activity,
  Shield,
  Settings,
  Zap,
  Radio,
  FileText,
  AlertTriangle,
  Play,
  Pause,
  RotateCcw,
  Sparkles,
  Layers,
  Thermometer,
  Gauge,
  CheckCircle2,
  AlertOctagon
} from 'lucide-react';
import { runClientDiagnosis } from './engine/physics';

const LOCAL_PRESET_CASES = {
  CASE_P204: {
    pump_id: 'P-204',
    suction_pressure_bar: 0.44,
    discharge_pressure_bar: 7.8,
    flow_m3_h: 118.0,
    fluid_temp_celsius: 45.0,
    pump_speed_rpm: 2950.0,
    electrical_power_kw: 28.5,
    bearing_temp_de_celsius: 52.0,
    bearing_temp_nde_celsius: 48.0,
    impeller_vanes: 5,
    npshr_m: 4.2,
    protocol_source: 'MODBUS_TCP'
  },
  CASE_25_SUCTION_RESTRICTION: {
    pump_id: 'P-204',
    suction_pressure_bar: 0.32,
    discharge_pressure_bar: 7.2,
    flow_m3_h: 92.0,
    fluid_temp_celsius: 42.0,
    pump_speed_rpm: 2950.0,
    electrical_power_kw: 24.1,
    bearing_temp_de_celsius: 55.0,
    bearing_temp_nde_celsius: 51.0,
    impeller_vanes: 5,
    npshr_m: 4.2,
    protocol_source: 'MODBUS_TCP'
  },
  CASE_17_MISALIGNMENT: {
    pump_id: 'P-204',
    suction_pressure_bar: 1.50,
    discharge_pressure_bar: 8.5,
    flow_m3_h: 120.0,
    fluid_temp_celsius: 38.0,
    pump_speed_rpm: 2950.0,
    electrical_power_kw: 29.8,
    bearing_temp_de_celsius: 74.0,
    bearing_temp_nde_celsius: 52.0,
    impeller_vanes: 5,
    npshr_m: 4.2,
    protocol_source: 'OPC_UA'
  },
  CASE_09_IMPELLER_EROSION: {
    pump_id: 'P-204',
    suction_pressure_bar: 1.60,
    discharge_pressure_bar: 6.2,
    flow_m3_h: 104.0,
    fluid_temp_celsius: 35.0,
    pump_speed_rpm: 2950.0,
    electrical_power_kw: 32.0,
    bearing_temp_de_celsius: 50.0,
    bearing_temp_nde_celsius: 47.0,
    impeller_vanes: 5,
    npshr_m: 4.2,
    protocol_source: 'MQTT_SPARKPLUG_B'
  },
  CASE_29_HEALTHY_BASELINE: {
    pump_id: 'P-204',
    suction_pressure_bar: 1.80,
    discharge_pressure_bar: 8.8,
    flow_m3_h: 125.0,
    fluid_temp_celsius: 30.0,
    pump_speed_rpm: 2950.0,
    electrical_power_kw: 27.2,
    bearing_temp_de_celsius: 42.0,
    bearing_temp_nde_celsius: 40.0,
    impeller_vanes: 5,
    npshr_m: 4.2,
    protocol_source: 'MODBUS_TCP'
  }
};

import RadialGauge from './components/RadialGauge';
import VibrationSpectrum from './components/VibrationSpectrum';
import HypothesisMatrix from './components/HypothesisMatrix';
import NextVerificationCard from './components/NextVerificationCard';
import WorkOrderModal from './components/WorkOrderModal';
import SettingsModal from './components/SettingsModal';

// Default Pump P-204 Cavitation Telemetry Scenario
const DEFAULT_P204_TELEMETRY = {
  pump_id: "P-204",
  suction_pressure_bar: 0.45,
  discharge_pressure_bar: 7.8,
  flow_m3_h: 118.0,
  fluid_temp_celsius: 25.0,
  pump_speed_rpm: 2950.0,
  electrical_power_kw: 28.5,
  bearing_temp_de_celsius: 48.2,
  bearing_temp_nde_celsius: 44.1,
  impeller_vanes: 5,
  npshr_m: 4.2,
  protocol_source: "MODBUS_TCP"
};

export default function App() {
  const [telemetry, setTelemetry] = useState(DEFAULT_P204_TELEMETRY);
  const [diagnosis, setDiagnosis] = useState(null);
  const [spectrumData, setSpectrumData] = useState(null);
  const [activeProtocol, setActiveProtocol] = useState('MODBUS_TCP');
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Modals state
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isWorkOrderOpen, setIsWorkOrderOpen] = useState(false);
  const [workOrderData, setWorkOrderData] = useState(null);

  // Settings & Gemini API key from localStorage
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('hydroguard_gemini_api_key') || '');
  const [selectedModel, setSelectedModel] = useState(() => localStorage.getItem('hydroguard_gemini_model') || 'gemini-3.5-flash');

  const saveApiKey = (newKey) => {
    setApiKey(newKey);
    localStorage.setItem('hydroguard_gemini_api_key', newKey);
  };

  const selectModel = (newModel) => {
    setSelectedModel(newModel);
    localStorage.setItem('hydroguard_gemini_model', newModel);
  };

  // Run diagnosis on telemetry change
  const fetchDiagnosis = async (currentTelemetry) => {
    setIsLoading(true);
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (apiKey) {
        headers['X-Gemini-API-Key'] = apiKey;
        headers['X-Gemini-Model'] = selectedModel;
      }

      const res = await fetch('/api/diagnose', {
        method: 'POST',
        headers,
        body: JSON.stringify(currentTelemetry)
      });

      if (res.ok) {
        const data = await res.json();
        setDiagnosis(data);
        if (data.calculated_metrics?.spectrum) {
          setSpectrumData(data.calculated_metrics.spectrum);
        }
        return;
      }
      throw new Error('API unavailable, falling back to client-side physics engine');
    } catch (err) {
      // Standalone / Cloudflare Pages client calculation fallback
      const clientResult = runClientDiagnosis(currentTelemetry);
      setDiagnosis(clientResult);
      if (clientResult.calculated_metrics?.spectrum) {
        setSpectrumData(clientResult.calculated_metrics.spectrum);
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDiagnosis(telemetry);
  }, [telemetry, apiKey, selectedModel]);

  // Live telemetry stream simulator
  useEffect(() => {
    if (!isLiveStreaming) return;
    let step = 0;
    const interval = setInterval(() => {
      step += 1;
      setTelemetry((prev) => ({
        ...prev,
        suction_pressure_bar: Number((0.44 + (Math.sin(step * 0.4) * 0.04)).toFixed(3)),
        discharge_pressure_bar: Number((7.8 + (Math.cos(step * 0.3) * 0.1)).toFixed(2)),
        flow_m3_h: Number((118.0 + (Math.sin(step * 0.2) * 1.5)).toFixed(1)),
        electrical_power_kw: Number((28.5 + (Math.cos(step * 0.4) * 0.3)).toFixed(1))
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, [isLiveStreaming]);

  // Preset Scenario Loaders
  const loadScenario = async (caseId) => {
    try {
      const res = await fetch(`/api/cases/${caseId}`);
      if (res.ok) {
        const data = await res.json();
        if (data.telemetry) {
          setTelemetry(data.telemetry);
          setActiveProtocol(data.telemetry.protocol_source || 'MODBUS_TCP');
          return;
        }
      }
      throw new Error('API case load unavailable, using local case definition');
    } catch (e) {
      if (LOCAL_PRESET_CASES[caseId]) {
        const localTelem = LOCAL_PRESET_CASES[caseId];
        setTelemetry(localTelem);
        setActiveProtocol(localTelem.protocol_source || 'MODBUS_TCP');
      }
    }
  };

  // Submit Field Verification Reading
  const handleFieldMeasurement = async (stepId, value) => {
    try {
      const res = await fetch('/api/next-verification/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          step_id: stepId,
          measured_value: value,
          telemetry
        })
      });
      if (res.ok) {
        const updatedDiag = await res.json();
        setDiagnosis(updatedDiag);
        return;
      }
      throw new Error('API feedback unavailable');
    } catch (e) {
      // Client-side updated calculation
      const updatedDiag = runClientDiagnosis(telemetry);
      setDiagnosis(updatedDiag);
    }
  };

  // Open Work Order
  const handleOpenWorkOrder = async () => {
    try {
      const res = await fetch('/api/work-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ telemetry })
      });
      if (res.ok) {
        const wo = await res.json();
        setWorkOrderData(wo);
        setIsWorkOrderOpen(true);
        return;
      }
      throw new Error('API work order unavailable');
    } catch (e) {
      // Fallback local ISO 55000 work order
      const clientDiag = diagnosis || runClientDiagnosis(telemetry);
      const fallbackWo = {
        work_order_id: `WO-${Date.now().toString().slice(-6)}`,
        asset_id: telemetry.pump_id || 'P-204',
        asset_tag: 'BOOSTER-FEED-01',
        title: `Corrective Hydraulic Inspection: ${clientDiag.top_hypothesis?.name || 'Cavitation Mitigation'}`,
        priority: 'EMERGENCY_HIGH',
        failure_mode_diagnosed: clientDiag.top_hypothesis?.name || 'Active Cavitation',
        failure_mechanism: clientDiag.top_hypothesis?.primary_mechanism || 'NPSHa deficit leading to vapor bubble collapse.',
        scope_of_work: [
          '1. Execute Lockout/Tagout (LOTO) isolation on motor feeder circuit breaker CB-204.',
          '2. Depressurize and vent suction spool; isolate manual gate valve V-SUC-01.',
          '3. Remove suction basket strainer ST-204; inspect mesh for scale, debris, or biofouling.',
          '4. Perform borescope examination of 1st-stage impeller suction eye.',
          '5. Reassemble with new spiral wound gaskets and record differential pressure.'
        ],
        required_parts_bom: [
          { part_number: 'GSK-SPW-316-6', description: 'Spiral Wound Gasket 6" ANSI 300# 316SS/PTFE', quantity: 2, stock_status: 'IN_STOCK', location: 'Warehouse Bay 4-B' },
          { part_number: 'STR-BKT-SS-100', description: 'Suction Basket Strainer Screen 100 Mesh 316SS', quantity: 1, stock_status: 'IN_STOCK', location: 'Warehouse Bay 2-A' },
          { part_number: 'LUB-ISO-VG-46', description: 'Synthetic Turbine Bearing Oil ISO VG 46 (5L)', quantity: 1, stock_status: 'IN_STOCK', location: 'Lube Room C-1' }
        ],
        loto_isolation_protocol: {
          loto_id: 'LOTO-P204-HYD-01',
          equipment_name: 'Booster Pump P-204 & 37kW Drive',
          osha_standard: 'OSHA 1910.147',
          steps: [
            { step_number: 1, action: 'Notify unit operators of Pump P-204 scheduled shutdown.' },
            { step_number: 2, action: 'Open and lockout main 400V Motor Circuit Breaker CB-204 in MCC Room 2.' },
            { step_number: 3, action: 'Close and chain Suction Isolation Valve V-SUC-01.' },
            { step_number: 4, action: 'Close and chain Discharge Isolation Valve V-DIS-01.' },
            { step_number: 5, action: 'Open Casing Drain Valve V-DRN-01 to bleed residual hydraulic pressure.' },
            { step_number: 6, action: 'Perform Zero Energy Verification on local start pushbutton.' }
          ]
        },
        safety_sign_off_status: 'PENDING_ENGINEER_APPROVAL',
        created_at_iso: new Date().toISOString()
      };
      setWorkOrderData(fallbackWo);
      setIsWorkOrderOpen(true);
    }
  };


  const metrics = diagnosis?.calculated_metrics;
  const topH = diagnosis?.top_hypothesis;

  // Operating State Style
  const opState = diagnosis?.operating_state || 'NORMAL_HEALTHY';
  let stateBadgeBg = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
  let stateDot = 'bg-emerald-400';
  if (opState === 'ALARM_CRITICAL') {
    stateBadgeBg = 'bg-red-500/20 text-red-300 border-red-500/50 animate-pulse';
    stateDot = 'bg-red-500';
  } else if (opState === 'DEGRADED_WARNING') {
    stateBadgeBg = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
    stateDot = 'bg-amber-400';
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-black">
      
      {/* 1. SCADA Header Bar */}
      <header className="sticky top-0 z-40 bg-slate-950/90 backdrop-blur-md border-b border-slate-800 px-4 py-3 flex items-center justify-between shadow-lg">
        {/* Brand & Asset Identity */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 shadow-md shadow-cyan-500/20 text-white">
            <Radio className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-extrabold tracking-wider uppercase text-white font-mono flex items-center gap-1.5">
                HydroGuard <span className="text-cyan-400">AI</span>
              </h1>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 border border-slate-700">
                v2.4.0
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Multistage Centrifugal Pump Condition Monitoring & Diagnostic Orchestrator
            </p>
          </div>
        </div>

        {/* Operating Badges & Protocol Selector */}
        <div className="flex items-center gap-3">
          {/* Active Asset Tag */}
          <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono">
            <span className="text-slate-500">TAG:</span>
            <strong className="text-cyan-400">{telemetry.pump_id}</strong>
          </div>

          {/* Operating State Badge */}
          <div className={`flex items-center gap-2 px-3 py-1 rounded-lg border text-xs font-mono font-bold uppercase tracking-wider ${stateBadgeBg}`}>
            <span className={`w-2 h-2 rounded-full ${stateDot}`}></span>
            {opState.replace('_', ' ')}
          </div>

          {/* Protocol Badge */}
          <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono">
            <span className="text-slate-500">LINK:</span>
            <span className="text-slate-300">{activeProtocol.replace('_', ' ')}</span>
          </div>

          {/* Engine Settings Modal Trigger */}
          <button
            onClick={() => setIsSettingsOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 hover:border-cyan-500/50 text-xs font-mono text-cyan-300 transition-all shadow-sm"
          >
            <Settings className="w-4 h-4 text-cyan-400" />
            <span className="hidden sm:inline">Engine Settings & Dev Info</span>
          </button>
        </div>
      </header>

      {/* 2. Scenario & Telemetry Control Bar */}
      <div className="bg-slate-900/60 border-b border-slate-800/80 px-4 py-2 flex flex-wrap items-center justify-between gap-2 text-xs">
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="text-[11px] font-mono uppercase text-slate-400 flex items-center gap-1 mr-1">
            <Layers className="w-3.5 h-3.5 text-cyan-400" /> Scenarios:
          </span>

          <button
            onClick={() => setTelemetry(DEFAULT_P204_TELEMETRY)}
            className="px-2.5 py-1 rounded-md bg-red-950/40 border border-red-500/40 text-red-300 font-mono font-bold hover:bg-red-900/50 transition-colors"
          >
            🔴 Case P-204 (Active Cavitation)
          </button>

          <button
            onClick={() => loadScenario('CASE_25_SUCTION_RESTRICTION')}
            className="px-2.5 py-1 rounded-md bg-amber-950/40 border border-amber-500/40 text-amber-300 font-mono hover:bg-amber-900/50 transition-colors"
          >
            🟠 Case 25 (Strainer Blockage)
          </button>

          <button
            onClick={() => loadScenario('CASE_17_MISALIGNMENT')}
            className="px-2.5 py-1 rounded-md bg-indigo-950/40 border border-indigo-500/40 text-indigo-300 font-mono hover:bg-indigo-900/50 transition-colors"
          >
            🔵 Case 17 (Shaft Misalignment)
          </button>

          <button
            onClick={() => loadScenario('CASE_09_IMPELLER_EROSION')}
            className="px-2.5 py-1 rounded-md bg-yellow-950/40 border border-yellow-500/40 text-yellow-300 font-mono hover:bg-yellow-900/50 transition-colors"
          >
            🟡 Case 09 (Impeller Erosion)
          </button>

          <button
            onClick={() => loadScenario('CASE_29_HEALTHY_BASELINE')}
            className="px-2.5 py-1 rounded-md bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 font-mono hover:bg-emerald-900/50 transition-colors"
          >
            🟢 Case 29 (Healthy Baseline)
          </button>
        </div>

        {/* Live Stream & Reset Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsLiveStreaming(!isLiveStreaming)}
            className={`px-3 py-1 rounded-md font-mono text-xs font-bold flex items-center gap-1.5 transition-all ${
              isLiveStreaming ? 'bg-rose-600 text-white animate-pulse' : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
            }`}
          >
            {isLiveStreaming ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            {isLiveStreaming ? 'Streaming Live Telemetry' : 'Start Live Stream'}
          </button>

          <button
            onClick={handleOpenWorkOrder}
            className="px-3 py-1 rounded-md bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-mono font-bold text-xs flex items-center gap-1.5 shadow-sm"
          >
            <FileText className="w-3 h-3" /> ISO 55000 Work Order
          </button>
        </div>
      </div>

      {/* 3. Main Dashboard Workspace */}
      <main className="flex-1 p-4 max-w-7xl mx-auto w-full space-y-4">
        
        {/* Section A: Live Vector Gauges Matrix */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          <RadialGauge
            label="Suction Pressure"
            value={telemetry.suction_pressure_bar}
            unit="bar abs"
            min={0}
            max={3.0}
            criticalLow={0.6}
            warningLow={1.1}
            decimals={2}
            accentColor="#38bdf8"
          />

          <RadialGauge
            label="Discharge Pressure"
            value={telemetry.discharge_pressure_bar}
            unit="bar"
            min={0}
            max={12.0}
            warningLow={5.0}
            decimals={1}
            accentColor="#06b6d4"
          />

          <RadialGauge
            label="Volumetric Flow"
            value={telemetry.flow_m3_h}
            unit="m³/h"
            min={0}
            max={160}
            warningLow={90}
            decimals={1}
            accentColor="#2dd4bf"
          />

          <RadialGauge
            label="NPSHa Margin"
            value={metrics?.npsh_margin_m || 0}
            unit="meters"
            min={-1.0}
            max={8.0}
            criticalLow={0.5}
            warningLow={1.5}
            decimals={2}
            accentColor={metrics?.npsh_margin_m < 0.5 ? '#ef4444' : '#10b981'}
          />

          <RadialGauge
            label="Pump Efficiency"
            value={metrics?.pump_efficiency_pct || 0}
            unit="%"
            min={0}
            max={100}
            warningLow={68.0}
            decimals={1}
            accentColor="#818cf8"
          />

          <RadialGauge
            label="Bearing Temp (DE)"
            value={telemetry.bearing_temp_de_celsius}
            unit="°C"
            min={20}
            max={100}
            warningHigh={65}
            criticalHigh={75}
            decimals={1}
            accentColor="#f59e0b"
          />
        </div>

        {/* Section B: Grid Layout: FFT Spectrum + Next Verification */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <VibrationSpectrum
              spectrumData={spectrumData}
              metrics={metrics}
              width={700}
              height={230}
            />
          </div>
          <div>
            <NextVerificationCard
              nextStep={diagnosis?.next_verification_action}
              onSubmitMeasurement={handleFieldMeasurement}
              onOpenWorkOrder={handleOpenWorkOrder}
              isLoading={isLoading}
            />
          </div>
        </div>

        {/* Section C: Dynamic Hypotheses Matrix & AI Synthesis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Dynamic Competing Hypotheses */}
          <HypothesisMatrix
            hypotheses={diagnosis?.hypotheses || []}
          />

          {/* AI Engineering Synthesis Card */}
          <div className="scada-panel p-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-cyan-400" />
                  <h3 className="text-sm font-bold tracking-wide uppercase text-white">
                    AI Reliability Engineering Assessment
                  </h3>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30 text-cyan-300">
                  Model: {selectedModel}
                </span>
              </div>

              {/* AI Narrative Body */}
              <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800/80 text-xs text-slate-300 leading-relaxed font-sans whitespace-pre-line max-h-[360px] overflow-y-auto">
                {diagnosis?.ai_engineering_synthesis || 'Awaiting diagnostic execution...'}
              </div>
            </div>

            {/* Safety Framing & Legal Boundary Footer */}
            <div className="mt-3 pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-500 flex items-start gap-1.5">
              <Shield className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span>
                Safety Decision-Support Only: Read-only boundary active. Physical equipment control is strictly isolated from AI software layer.
              </span>
            </div>
          </div>
        </div>

      </main>

      {/* 4. Footer */}
      <footer className="mt-auto bg-slate-950 border-t border-slate-800 px-4 py-3 text-[11px] font-mono text-slate-400 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-3">
          <span>Lead Architect: <strong className="text-cyan-400">Mohamed Hsini</strong></span>
          <span>•</span>
          <a href="https://hsini.dev" target="_blank" rel="noreferrer" className="text-slate-300 hover:text-cyan-400 underline">
            hsini.dev
          </a>
          <span>•</span>
          <a href="https://github.com/hsinidev/HydroGuard-AI" target="_blank" rel="noreferrer" className="text-slate-300 hover:text-cyan-400 underline">
            GitHub Repository
          </a>
        </div>
        <div className="text-slate-500">
          ISO 10816-3 & ISO 55000 Condition Monitoring Standards Aligned
        </div>
      </footer>

      {/* Modals */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apiKey={apiKey}
        onSaveApiKey={saveApiKey}
        selectedModel={selectedModel}
        onSelectModel={selectModel}
      />

      <WorkOrderModal
        isOpen={isWorkOrderOpen}
        onClose={() => setIsWorkOrderOpen(false)}
        workOrder={workOrderData}
      />

    </div>
  );
}
