import React from 'react';
import { X, Printer, Download, CheckSquare, Wrench, Shield, Box, FileText, AlertTriangle } from 'lucide-react';

export default function WorkOrderModal({ isOpen, onClose, workOrder }) {
  if (!isOpen || !workOrder) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-cyan-500/40 rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden text-slate-200 font-sans">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 bg-slate-950 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-bold text-white tracking-wide font-mono">
                  {workOrder.work_order_number || 'WO-P204-2026'}
                </h2>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-rose-500 text-white">
                  {workOrder.priority || 'HIGH'} PRIORITY
                </span>
              </div>
              <p className="text-xs text-slate-400">
                {workOrder.standard_alignment || 'ISO 55000:2014 & ISO 10816-3 Aligned Work Order'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono flex items-center gap-1.5 transition-all border border-slate-700"
            >
              <Printer className="w-4 h-4 text-cyan-400" /> Print / Export
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Scrollable Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-xs">
          
          {/* Section 1: Asset & Location Summary */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-950/60 p-4 rounded-lg border border-slate-800 font-mono">
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Asset Tag</span>
              <strong className="text-cyan-400 text-sm">{workOrder.asset_id}</strong>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Equipment</span>
              <strong className="text-slate-200">Multistage Booster Pump</strong>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Plant Location</span>
              <strong className="text-slate-200">{workOrder.plant_location}</strong>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Generated Time</span>
              <strong className="text-slate-200">{workOrder.created_timestamp}</strong>
            </div>
          </div>

          {/* Section 2: Condition Trigger & Diagnostic Findings */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" /> Condition Trigger & Root Cause Hypothesis
            </h3>
            <div className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 space-y-1.5">
              <div className="text-slate-200 font-bold">
                {workOrder.condition_trigger}
              </div>
              <p className="text-slate-300 italic">
                {workOrder.diagnostic_summary?.top_mechanism}
              </p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-800/80 font-mono text-[11px]">
                <div>
                  <span className="text-slate-500">NPSH Margin: </span>
                  <span className="text-rose-400 font-bold">{workOrder.diagnostic_summary?.npsha_margin_m} m</span>
                </div>
                <div>
                  <span className="text-slate-500">Efficiency: </span>
                  <span className="text-cyan-300 font-bold">{workOrder.diagnostic_summary?.pump_efficiency_pct}%</span>
                </div>
                <div>
                  <span className="text-slate-500">Overall RMS: </span>
                  <span className="text-amber-400 font-bold">{workOrder.diagnostic_summary?.vibration_overall_rms} mm/s</span>
                </div>
                <div>
                  <span className="text-slate-500">1–5kHz Band: </span>
                  <span className="text-rose-400 font-bold">{workOrder.diagnostic_summary?.cavitation_1_5khz_energy_rms} mm/s</span>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Bill of Materials (BOM) */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <Box className="w-4 h-4 text-cyan-400" /> Required Replacement Parts & Bill of Materials (BOM)
            </h3>
            <div className="border border-slate-800 rounded-lg overflow-hidden">
              <table className="w-full text-left font-mono">
                <thead className="bg-slate-950 text-slate-400 text-[10px] uppercase border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Part Number</th>
                    <th className="p-2.5">Description</th>
                    <th className="p-2.5 text-center">Qty</th>
                    <th className="p-2.5">Warehouse Inventory Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-[11px] bg-slate-950/40">
                  {workOrder.bill_of_materials?.map((part, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/30">
                      <td className="p-2.5 font-bold text-cyan-300">{part.part_no}</td>
                      <td className="p-2.5 text-slate-200">{part.description}</td>
                      <td className="p-2.5 text-center font-bold text-white">{part.qty}</td>
                      <td className="p-2.5 text-emerald-400 font-medium">{part.stock_status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Section 4: OSHA 1910.147 LOTO Safety Procedures */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2">
              <Shield className="w-4 h-4 text-amber-400" /> OSHA 1910.147 Lockout/Tagout (LOTO) Protocol
            </h3>
            <div className="p-3 bg-amber-950/20 border border-amber-500/30 rounded-lg space-y-2">
              <div className="text-[11px] font-bold text-amber-300 font-mono">
                Standard: {workOrder.loto_safety_procedure?.standard_reference} ({workOrder.loto_safety_procedure?.procedure_id})
              </div>
              <ul className="space-y-1.5 pl-4 list-decimal text-slate-300">
                {workOrder.loto_safety_procedure?.execution_steps?.map((step, idx) => (
                  <li key={idx} className="leading-relaxed">{step}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Section 5: Technician Sign-Off */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 bg-slate-950 rounded-lg border border-slate-800 font-mono">
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Assigned Technician</span>
              <strong className="text-slate-200">{workOrder.technician_sign_off?.assigned_lead_technician}</strong>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Est. Labor Hours</span>
              <strong className="text-slate-200">{workOrder.technician_sign_off?.estimated_labor_hours} Hours</strong>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase">Work Order Status</span>
              <strong className="text-emerald-400">{workOrder.technician_sign_off?.status}</strong>
            </div>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-slate-500 text-[10px] font-mono">
          <span>HydroGuard AI Industrial Predictive Maintenance Orchestration Platform</span>
          <span>Read-Only Advisory System Boundary Enforced</span>
        </div>
      </div>
    </div>
  );
}
