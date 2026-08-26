import React, { useState } from 'react';
import { Cpu, ChevronDown, ChevronUp, CheckCircle, XCircle, AlertOctagon, Info } from 'lucide-react';

export default function HypothesisMatrix({ hypotheses = [], onSelectHypothesis }) {
  const [expandedId, setExpandedId] = useState(null);

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const getSeverityStyle = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return {
          barColor: 'from-red-600 to-rose-500',
          badgeBg: 'bg-red-500/20 text-red-400 border-red-500/40',
          borderColor: 'border-red-500/40'
        };
      case 'HIGH':
        return {
          barColor: 'from-amber-600 to-orange-500',
          badgeBg: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
          borderColor: 'border-amber-500/40'
        };
      case 'MEDIUM':
        return {
          barColor: 'from-yellow-600 to-amber-400',
          badgeBg: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40',
          borderColor: 'border-yellow-500/30'
        };
      case 'HEALTHY':
        return {
          barColor: 'from-emerald-600 to-teal-400',
          badgeBg: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
          borderColor: 'border-emerald-500/30'
        };
      default:
        return {
          barColor: 'from-cyan-600 to-blue-500',
          badgeBg: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/40',
          borderColor: 'border-slate-800'
        };
    }
  };

  return (
    <div className="scada-panel p-4 flex flex-col justify-between">
      {/* Title */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-indigo-400" />
          <h3 className="text-sm font-bold tracking-wide uppercase text-white">
            Dynamic Competing Hypothesis Matrix
          </h3>
        </div>
        <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1">
          <Info className="w-3.5 h-3.5 text-slate-500" /> Bayesian Re-weighting
        </span>
      </div>

      {/* Hypothesis List */}
      <div className="space-y-2.5 max-h-[460px] overflow-y-auto pr-1">
        {hypotheses.map((item, index) => {
          const style = getSeverityStyle(item.severity);
          const isExpanded = expandedId === item.hypothesis_id;
          const isTop = index === 0;

          return (
            <div
              key={item.hypothesis_id}
              className={`rounded-lg border transition-all duration-300 ${
                isTop ? `${style.borderColor} bg-slate-900/90 shadow-md` : 'border-slate-800/80 bg-slate-950/60 hover:border-slate-700'
              }`}
            >
              {/* Main Summary Row */}
              <div
                className="p-3 cursor-pointer select-none"
                onClick={() => toggleExpand(item.hypothesis_id)}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-slate-400">
                      #{index + 1}
                    </span>
                    <h4 className="text-xs font-bold text-slate-200 hover:text-white transition-colors">
                      {item.name}
                    </h4>
                    {isTop && (
                      <span className="px-1.5 py-0.2 rounded text-[9px] font-extrabold uppercase tracking-wider bg-rose-500 text-white animate-pulse">
                        TOP HYPOTHESIS
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${style.badgeBg}`}>
                      {item.severity}
                    </span>
                    <span className="text-sm font-mono font-bold text-white min-w-[50px] text-right">
                      {item.probability_pct.toFixed(1)}%
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-400" />
                    )}
                  </div>
                </div>

                {/* Animated Probability Progress Bar */}
                <div className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden relative">
                  <div
                    className={`h-full bg-gradient-to-r ${style.barColor} transition-all duration-700 ease-out`}
                    style={{ width: `${Math.max(2, item.probability_pct)}%` }}
                  />
                </div>
              </div>

              {/* Expandable Physical Evidence Details */}
              {isExpanded && (
                <div className="px-3 pb-3 pt-1 border-t border-slate-800/80 text-[11px] space-y-2 bg-slate-950/40">
                  <div>
                    <span className="text-slate-400 font-semibold block mb-0.5">Physical Mechanism:</span>
                    <p className="text-slate-300 italic">{item.primary_mechanism}</p>
                  </div>

                  {/* Supporting Evidence */}
                  {item.supporting_evidence?.length > 0 && (
                    <div>
                      <span className="text-emerald-400 font-semibold flex items-center gap-1 mb-1">
                        <CheckCircle className="w-3 h-3 text-emerald-400" /> Supporting Telemetry Evidence:
                      </span>
                      <ul className="space-y-1 pl-4 list-disc text-slate-300">
                        {item.supporting_evidence.map((ev, i) => (
                          <li key={i}>{ev}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Conflicting Evidence */}
                  {item.conflicting_evidence?.length > 0 && (
                    <div>
                      <span className="text-rose-400 font-semibold flex items-center gap-1 mb-1">
                        <XCircle className="w-3 h-3 text-rose-400" /> Conflicting Evidence:
                      </span>
                      <ul className="space-y-1 pl-4 list-disc text-slate-300">
                        {item.conflicting_evidence.map((ev, i) => (
                          <li key={i}>{ev}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Technician Recommended Action */}
                  <div className="mt-2 pt-2 border-t border-slate-800/60 flex items-start gap-1.5 text-cyan-300 font-mono">
                    <span className="font-bold">Next Action:</span>
                    <span>{item.recommended_technician_action}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
