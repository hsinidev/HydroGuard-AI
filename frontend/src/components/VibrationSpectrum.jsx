import React, { useState } from 'react';
import { Activity, Zap, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function VibrationSpectrum({
  spectrumData,
  metrics,
  width = 640,
  height = 220
}) {
  const [hoveredPoint, setHoveredPoint] = useState(null);

  const freqs = spectrumData?.frequencies || [];
  const amps = spectrumData?.amplitudes || [];

  const maxFreq = 5000;
  const maxAmp = Math.max(3.5, ...(amps.length > 0 ? amps : [3.0]));

  const paddingLeft = 45;
  const paddingRight = 20;
  const paddingTop = 25;
  const paddingBottom = 30;

  const graphWidth = width - paddingLeft - paddingRight;
  const graphHeight = height - paddingTop - paddingBottom;

  // Scale functions
  const getX = (f) => paddingLeft + (Math.min(f, maxFreq) / maxFreq) * graphWidth;
  const getY = (a) => paddingTop + graphHeight - (Math.min(a, maxAmp) / maxAmp) * graphHeight;

  // Path generator
  let pathD = '';
  if (freqs.length > 0) {
    pathD = `M ${getX(freqs[0])} ${getY(amps[0])}`;
    for (let i = 1; i < freqs.length; i++) {
      pathD += ` L ${getX(freqs[i])} ${getY(amps[i])}`;
    }
  }

  // Cavitation zone coordinates (1000 Hz to 5000 Hz)
  const cavXStart = getX(1000);
  const cavXEnd = getX(5000);
  const cavWidth = cavXEnd - cavXStart;

  const f1x = metrics?.f_1x_hz || 49.17;
  const f2x = f1x * 2.0;
  const fVpf = metrics?.f_vpf_hz || 245.83;

  return (
    <div className="scada-panel p-4 flex flex-col justify-between">
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          <h3 className="text-sm font-bold tracking-wide uppercase text-white">
            Vibration FFT Frequency Spectrum (0 – 5.0 kHz)
          </h3>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="flex items-center gap-1 text-slate-300">
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
            Overall RMS: <strong className="text-cyan-300">{metrics?.overall_rms_mm_s || '0.00'} mm/s</strong>
          </span>
          <span className="flex items-center gap-1 text-slate-300">
            <span className={`w-2 h-2 rounded-full ${metrics?.is_cavitation_spectral_elevated ? 'bg-red-500 animate-pulse' : 'bg-emerald-400'}`}></span>
            1–5 kHz Cavitation Band: <strong className={metrics?.is_cavitation_spectral_elevated ? 'text-red-400 font-bold' : 'text-emerald-400'}>{metrics?.cavitation_1_5khz_energy_rms || '0.00'} mm/s</strong>
          </span>
        </div>
      </div>

      {/* SVG Canvas Graph */}
      <div className="relative w-full overflow-hidden bg-slate-950/90 rounded-lg border border-slate-800 p-1">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto"
          style={{ minHeight: '180px' }}
        >
          <defs>
            {/* Cavitation High Frequency Glow Gradient */}
            <linearGradient id="cavitationZoneGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={metrics?.is_cavitation_spectral_elevated ? "#ef4444" : "#06b6d4"} stopOpacity="0.25" />
              <stop offset="100%" stopColor={metrics?.is_cavitation_spectral_elevated ? "#ef4444" : "#06b6d4"} stopOpacity="0.02" />
            </linearGradient>

            <linearGradient id="spectrumLineGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="20%" stopColor="#06b6d4" />
              <stop offset="40%" stopColor="#818cf8" />
              <stop offset="80%" stopColor={metrics?.is_cavitation_spectral_elevated ? "#ef4444" : "#2dd4bf"} />
            </linearGradient>
          </defs>

          {/* Grid lines horizontal */}
          {[0.25, 0.5, 0.75, 1.0].map((fraction, idx) => {
            const y = paddingTop + graphHeight * (1 - fraction);
            const val = (maxAmp * fraction).toFixed(1);
            return (
              <g key={idx}>
                <line
                  x1={paddingLeft}
                  y1={y}
                  x2={width - paddingRight}
                  y2={y}
                  stroke="#1e293b"
                  strokeDasharray="3 3"
                />
                <text
                  x={paddingLeft - 8}
                  y={y + 3}
                  textAnchor="end"
                  fill="#64748b"
                  fontSize="9"
                  fontFamily="monospace"
                >
                  {val}
                </text>
              </g>
            );
          })}

          {/* Highlighted Cavitation Band Zone (1000 - 5000 Hz) */}
          <rect
            x={cavXStart}
            y={paddingTop}
            width={cavWidth}
            height={graphHeight}
            fill="url(#cavitationZoneGrad)"
            stroke={metrics?.is_cavitation_spectral_elevated ? "#ef444466" : "#06b6d433"}
            strokeDasharray="2 2"
          />

          <text
            x={cavXStart + 10}
            y={paddingTop + 14}
            fill={metrics?.is_cavitation_spectral_elevated ? "#f87171" : "#38bdf8"}
            fontSize="10"
            fontWeight="bold"
            fontFamily="monospace"
          >
            1.0 – 5.0 kHz CAVITATION BAND ({metrics?.cavitation_spectral_ratio ? (metrics.cavitation_spectral_ratio * 100).toFixed(0) : '0'}% Power)
          </text>

          {/* Frequency Grid & Ticks (0, 1k, 2k, 3k, 4k, 5k) */}
          {[0, 1000, 2000, 3000, 4000, 5000].map((f) => {
            const x = getX(f);
            return (
              <g key={f}>
                <line
                  x1={x}
                  y1={paddingTop}
                  x2={x}
                  y2={paddingTop + graphHeight}
                  stroke="#1e293b"
                  strokeDasharray="3 3"
                />
                <text
                  x={x}
                  y={paddingTop + graphHeight + 16}
                  textAnchor="middle"
                  fill="#64748b"
                  fontSize="9"
                  fontFamily="monospace"
                >
                  {f >= 1000 ? `${f / 1000}k` : `${f}Hz`}
                </text>
              </g>
            );
          })}

          {/* Characteristic Frequency Markers */}
          {/* 1X RPM */}
          {f1x <= maxFreq && (
            <g>
              <line
                x1={getX(f1x)}
                y1={paddingTop}
                x2={getX(f1x)}
                y2={paddingTop + graphHeight}
                stroke="#38bdf8"
                strokeWidth="1.5"
                strokeDasharray="2 2"
              />
              <text
                x={getX(f1x)}
                y={paddingTop + 28}
                textAnchor="middle"
                fill="#38bdf8"
                fontSize="8"
                fontWeight="bold"
                fontFamily="monospace"
              >
                1X ({f1x.toFixed(0)}Hz)
              </text>
            </g>
          )}

          {/* 2X RPM */}
          {f2x <= maxFreq && (
            <g>
              <line
                x1={getX(f2x)}
                y1={paddingTop}
                x2={getX(f2x)}
                y2={paddingTop + graphHeight}
                stroke="#818cf8"
                strokeWidth="1.5"
                strokeDasharray="2 2"
              />
              <text
                x={getX(f2x)}
                y={paddingTop + 40}
                textAnchor="middle"
                fill="#818cf8"
                fontSize="8"
                fontWeight="bold"
                fontFamily="monospace"
              >
                2X ({f2x.toFixed(0)}Hz)
              </text>
            </g>
          )}

          {/* VPF Vane Pass Frequency */}
          {fVpf <= maxFreq && (
            <g>
              <line
                x1={getX(fVpf)}
                y1={paddingTop}
                x2={getX(fVpf)}
                y2={paddingTop + graphHeight}
                stroke="#fbbf24"
                strokeWidth="1.5"
                strokeDasharray="2 2"
              />
              <text
                x={getX(fVpf)}
                y={paddingTop + 52}
                textAnchor="middle"
                fill="#fbbf24"
                fontSize="8"
                fontWeight="bold"
                fontFamily="monospace"
              >
                VPF ({fVpf.toFixed(0)}Hz)
              </text>
            </g>
          )}

          {/* Spectrum Waveform Line */}
          {pathD && (
            <path
              d={pathD}
              fill="none"
              stroke="url(#spectrumLineGrad)"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}

          {/* Axis Labels */}
          <text
            x={12}
            y={height / 2}
            textAnchor="middle"
            fill="#94a3b8"
            fontSize="9"
            fontFamily="monospace"
            transform={`rotate(-90 12 ${height / 2})`}
          >
            Velocity (mm/s RMS)
          </text>
        </svg>
      </div>

      {/* Legend and Diagnostic Callout */}
      <div className="flex flex-wrap items-center justify-between mt-2 pt-2 border-t border-slate-800 text-[11px]">
        <div className="flex items-center gap-4 text-slate-400">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-sky-400"></span> 1X Motor Speed
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-indigo-400"></span> 2X Misalignment
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-amber-400"></span> VPF (Vanes: 5)
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-2 bg-red-500/30 border border-red-500/50 rounded-sm"></span> 1–5 kHz Cavitation Band
          </span>
        </div>
        <div className="font-mono text-slate-400">
          ISO 10816-3 Severity: <span className="text-white font-bold">{metrics?.overall_rms_mm_s > 4.5 ? 'Zone D (Unacceptable)' : metrics?.overall_rms_mm_s > 2.8 ? 'Zone C (Warning)' : 'Zone A/B (Normal)'}</span>
        </div>
      </div>
    </div>
  );
}
