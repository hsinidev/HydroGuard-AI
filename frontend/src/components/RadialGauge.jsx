import React from 'react';

export default function RadialGauge({
  label,
  value,
  unit,
  min = 0,
  max = 100,
  warningLow = null,
  warningHigh = null,
  criticalLow = null,
  criticalHigh = null,
  decimals = 1,
  size = 150,
  accentColor = '#06b6d4'
}) {
  const radius = (size / 2) - 16;
  const circumference = 2 * Math.PI * radius;
  const arcLength = circumference * 0.75; // 270 degree arc
  const strokeDashoffsetArc = circumference * 0.25;

  // Clamped percentage (0 to 1)
  const normalizedVal = Math.min(Math.max(value, min), max);
  const pct = (normalizedVal - min) / (max - min);
  const progressOffset = arcLength * (1 - pct);

  // Status color evaluation
  let statusColor = accentColor;
  let statusBadge = 'NORMAL';

  if (criticalLow !== null && value <= criticalLow) {
    statusColor = '#ef4444';
    statusBadge = 'CRITICAL LOW';
  } else if (criticalHigh !== null && value >= criticalHigh) {
    statusColor = '#ef4444';
    statusBadge = 'CRITICAL HIGH';
  } else if (warningLow !== null && value <= warningLow) {
    statusColor = '#f59e0b';
    statusBadge = 'WARNING LOW';
  } else if (warningHigh !== null && value >= warningHigh) {
    statusColor = '#f59e0b';
    statusBadge = 'WARNING HIGH';
  }

  // Pointer angle: -135 deg to +135 deg
  const pointerAngle = -135 + (pct * 270);

  return (
    <div className="flex flex-col items-center justify-between p-3 rounded-xl bg-slate-900/80 border border-slate-800 shadow-lg relative group hover:border-cyan-500/30 transition-all">
      <div className="text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-1">
        {label}
      </div>

      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform rotate-[135deg]">
          {/* Background Track Arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="#1e293b"
            strokeWidth="8"
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeLinecap="round"
          />

          {/* Active Value Arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={statusColor}
            strokeWidth="8"
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeDashoffset={progressOffset}
            strokeLinecap="round"
            style={{
              transition: 'stroke-dashoffset 0.6s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.4s ease',
              filter: `drop-shadow(0 0 6px ${statusColor}88)`
            }}
          />
        </svg>

        {/* Center Digital Display */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-xl font-bold font-mono tracking-tight text-white" style={{ color: statusColor }}>
            {typeof value === 'number' ? value.toFixed(decimals) : value}
          </span>
          <span className="text-[10px] font-mono text-slate-400 -mt-0.5">
            {unit}
          </span>
        </div>
      </div>

      {/* Min / Max & Badge */}
      <div className="w-full flex items-center justify-between px-1 text-[9px] font-mono text-slate-500 mt-1">
        <span>{min}</span>
        <span
          className="px-1.5 py-0.5 rounded font-bold uppercase tracking-wider text-[8px]"
          style={{
            backgroundColor: `${statusColor}20`,
            color: statusColor,
            border: `1px solid ${statusColor}40`
          }}
        >
          {statusBadge}
        </span>
        <span>{max}</span>
      </div>
    </div>
  );
}
