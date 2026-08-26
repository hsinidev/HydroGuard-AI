import React, { useState } from 'react';
import { Target, CheckCircle2, ShieldAlert, Send, Wrench, FileText } from 'lucide-react';

export default function NextVerificationCard({
  nextStep,
  onSubmitMeasurement,
  onOpenWorkOrder,
  isLoading = false
}) {
  const [fieldValue, setFieldValue] = useState('');
  const [submittedStatus, setSubmittedStatus] = useState(null);

  if (!nextStep) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!fieldValue) return;
    onSubmitMeasurement(nextStep.step_id, fieldValue);
    setSubmittedStatus(`Reading '${fieldValue} ${nextStep.input_unit || ''}' logged. Hypotheses dynamically re-weighted.`);
    setTimeout(() => setSubmittedStatus(null), 5000);
  };

  return (
    <div className="scada-panel p-4 flex flex-col justify-between border-cyan-500/30">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Target className="w-5 h-5 text-cyan-400" />
          <h3 className="text-sm font-bold tracking-wide uppercase text-white">
            Next-Best-Verification Action
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-rose-500/20 text-rose-300 border border-rose-500/40">
            PRIORITY: {nextStep.priority}
          </span>
          <span className="text-[10px] font-mono text-cyan-400">
            Gain: +{nextStep.expected_information_gain_pct}% Info
          </span>
        </div>
      </div>

      {/* Action Title & Field Instruction */}
      <div className="bg-slate-950/70 p-3 rounded-lg border border-slate-800/80 mb-3 space-y-2">
        <h4 className="text-sm font-bold text-white flex items-center gap-2">
          <Wrench className="w-4 h-4 text-cyan-400 flex-shrink-0" />
          {nextStep.action_title}
        </h4>
        <p className="text-xs text-slate-300 leading-relaxed">
          {nextStep.field_instruction}
        </p>

        {/* Safety and LOTO Requirements */}
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold flex items-center gap-1 ${
            nextStep.loto_required ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
          }`}>
            <ShieldAlert className="w-3 h-3" />
            {nextStep.loto_required ? 'OSHA LOTO Required' : 'No LOTO Required (Online Gauge)'}
          </span>
          <span className="text-[10px] font-mono text-slate-400">
            Safety Risk: <strong className="text-slate-200">{nextStep.safety_risk_level}</strong>
          </span>
        </div>
      </div>

      {/* Interactive Technician Field Input Form */}
      <form onSubmit={handleSubmit} className="space-y-2">
        <div className="flex items-center gap-2">
          <div className="flex-1 relative">
            <input
              type={nextStep.input_type || 'number'}
              step="any"
              placeholder={`Enter field measurement (${nextStep.target_parameter || ''})`}
              value={fieldValue}
              onChange={(e) => setFieldValue(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-sm font-mono text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
            />
            {nextStep.input_unit && (
              <span className="absolute right-3 top-2 text-xs font-mono text-slate-400 pointer-events-none">
                {nextStep.input_unit}
              </span>
            )}
          </div>
          <button
            type="submit"
            disabled={!fieldValue || isLoading}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold font-mono tracking-wider uppercase transition-all shadow-md hover:shadow-cyan-500/25 flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-3.5 h-3.5" />
            Submit
          </button>
        </div>

        {/* Expected nominal range hint */}
        <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 px-1">
          <span>Expected Range: {nextStep.expected_range || 'Nominal'}</span>
          <button
            type="button"
            onClick={onOpenWorkOrder}
            className="text-cyan-400 hover:text-cyan-300 underline flex items-center gap-1 font-semibold"
          >
            <FileText className="w-3 h-3" /> View ISO Work Order
          </button>
        </div>

        {/* Feedback Alert */}
        {submittedStatus && (
          <div className="p-2 rounded bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-xs font-mono flex items-center gap-2 animate-fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>{submittedStatus}</span>
          </div>
        )}
      </form>
    </div>
  );
}
