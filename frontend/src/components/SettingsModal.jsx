import React, { useState, useEffect } from 'react';
import { X, Key, Eye, EyeOff, Sparkles, User, Globe, Github, Mail, ShieldCheck, Check, Cpu } from 'lucide-react';

export default function SettingsModal({
  isOpen,
  onClose,
  apiKey,
  onSaveApiKey,
  selectedModel,
  onSelectModel
}) {
  const [keyInput, setKeyInput] = useState(apiKey || '');
  const [showKey, setShowKey] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    setKeyInput(apiKey || '');
  }, [apiKey]);

  if (!isOpen) return null;

  const handleSave = (e) => {
    e.preventDefault();
    onSaveApiKey(keyInput.trim());
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const models = [
    { id: 'gemini-3.5-flash', name: 'Gemini 3.5 Flash', tag: 'Fastest / Real-Time Reasoning (Recommended)' },
    { id: 'gemini-3.5-pro', name: 'Gemini 3.5 Pro', tag: 'Deep Engineering & Failure Mode Synthesis' },
    { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', tag: 'Standard Production Model' }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-cyan-500/40 rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden text-slate-200">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 bg-slate-950 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-wide font-mono">
                Engine Settings & Developer Info
              </h2>
              <p className="text-xs text-slate-400">
                Configure Gemini LLM orchestration and review Lead Architect credentials
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-xs font-sans">
          
          {/* Section 1: Gemini API Key Management */}
          <div className="space-y-3 bg-slate-950/70 p-4 rounded-xl border border-slate-800">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                <Key className="w-4 h-4 text-cyan-400" /> Gemini API Key Vault (Stored in Browser LocalStorage)
              </label>
              {isSaved && (
                <span className="text-emerald-400 text-xs font-mono font-bold flex items-center gap-1">
                  <Check className="w-3.5 h-3.5" /> Key Saved!
                </span>
              )}
            </div>

            <form onSubmit={handleSave} className="space-y-3">
              <div className="relative">
                <input
                  type={showKey ? 'text' : 'password'}
                  placeholder="Enter your Google Gemini API Key (AIzaSy...)"
                  value={keyInput}
                  onChange={(e) => setKeyInput(e.target.value)}
                  className="w-full pl-3 pr-10 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs font-mono text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
                />
                <button
                  type="button"
                  onClick={() => setShowKey(!showKey)}
                  className="absolute right-3 top-2.5 text-slate-400 hover:text-white"
                >
                  {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-[11px] text-slate-400">
                  Keys are stored exclusively in your local browser storage and never logged.
                </p>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-mono font-bold text-xs transition-colors shadow-md shadow-cyan-600/20"
                >
                  Save API Key
                </button>
              </div>
            </form>
          </div>

          {/* Section 2: Gemini Model Dynamic Selector */}
          <div className="space-y-3 bg-slate-950/70 p-4 rounded-xl border border-slate-800">
            <label className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" /> Active Reasoning Model
            </label>
            <div className="space-y-2">
              {models.map((m) => (
                <div
                  key={m.id}
                  onClick={() => onSelectModel(m.id)}
                  className={`p-3 rounded-lg border cursor-pointer transition-all flex items-center justify-between ${
                    selectedModel === m.id
                      ? 'bg-cyan-950/40 border-cyan-500/60 shadow-md shadow-cyan-500/10'
                      : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div>
                    <div className="font-mono font-bold text-xs text-white">
                      {m.name}
                    </div>
                    <div className="text-[11px] text-slate-400">
                      {m.tag}
                    </div>
                  </div>
                  {selectedModel === m.id && (
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400"></span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Section 3: Developer & Lead Architect Accreditation Card */}
          <div className="space-y-3 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4 rounded-xl border border-cyan-500/30">
            <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <User className="w-4 h-4 text-cyan-400" /> Lead Architect & Engineering Accreditation
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="flex items-center gap-2.5 p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                <User className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                <div>
                  <span className="text-[10px] text-slate-500 uppercase block font-mono">Lead Architect</span>
                  <strong className="text-white">Mohamed Hsini</strong>
                </div>
              </div>

              <div className="flex items-center gap-2.5 p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                <Globe className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                <div>
                  <span className="text-[10px] text-slate-500 uppercase block font-mono">Portfolio / Website</span>
                  <a
                    href="https://hsini.dev"
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:underline font-mono"
                  >
                    https://hsini.dev
                  </a>
                </div>
              </div>

              <div className="flex items-center gap-2.5 p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                <Github className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                <div>
                  <span className="text-[10px] text-slate-500 uppercase block font-mono">GitHub Repository</span>
                  <a
                    href="https://github.com/hsinidev/HydroGuard-AI"
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:underline font-mono"
                  >
                    hsinidev/HydroGuard-AI
                  </a>
                </div>
              </div>

              <div className="flex items-center gap-2.5 p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                <Mail className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                <div>
                  <span className="text-[10px] text-slate-500 uppercase block font-mono">Direct Contact</span>
                  <a
                    href="mailto:contact@hsini.dev"
                    className="text-cyan-400 hover:underline font-mono"
                  >
                    contact@hsini.dev
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Section 4: Safety & System Boundaries */}
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-[11px] text-slate-400 flex items-start gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
            <span>
              <strong>Safety Guardrail:</strong> HydroGuard AI is strictly read-only and will never actuate physical valves or energize equipment. Aligned with ISO 55000, ISO 10816-3, and OSHA 1910.147.
            </span>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-slate-500 text-[10px] font-mono">
          <span>HydroGuard AI v2.4.0 (Enterprise SCADA Edition)</span>
          <button
            onClick={onClose}
            className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
