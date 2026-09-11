import React from 'react';
import { PowerIcon, XMarkIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

interface AutoShutdownModuleProps {
  enabled: boolean;
  countdownSec: number | null;
  onToggleEnabled: (enabled: boolean) => void;
  onCancelShutdown: () => void;
  onShutdownNow: () => void;
}

export const AutoShutdownModule: React.FC<AutoShutdownModuleProps> = ({
  enabled,
  countdownSec,
  onToggleEnabled,
  onCancelShutdown,
  onShutdownNow,
}) => {
  return (
    <div className="glass-panel p-5 rounded-2xl space-y-4 border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <PowerIcon className="w-5 h-5 text-rose-400" />
          <div>
            <h3 className="font-bold text-white text-sm tracking-tight">Auto Shutdown Module</h3>
            <p className="text-[11px] text-slate-400 font-mono">Post-training automated system power action</p>
          </div>
        </div>

        {/* Enabled Toggle Switch */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-slate-400">
            Status: <strong className={enabled ? 'text-emerald-400' : 'text-slate-500'}>{enabled ? 'Enabled' : 'Disabled'}</strong>
          </span>
          <button
            onClick={() => onToggleEnabled(!enabled)}
            className={`w-11 h-6 rounded-full transition-colors p-1 flex items-center ${
              enabled ? 'bg-emerald-600 justify-end' : 'bg-slate-800 justify-start'
            }`}
          >
            <div className="w-4 h-4 bg-white rounded-full shadow-md" />
          </button>
        </div>
      </div>

      {/* Countdown Card when active */}
      {countdownSec !== null ? (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/50 flex flex-col md:flex-row items-center justify-between gap-4 animate-bounce-short">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-rose-600/30 text-rose-400 border border-rose-500 flex items-center justify-center">
              <PowerIcon className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="text-xs font-bold text-rose-200 uppercase tracking-wide">Automatic System Shutdown Scheduled</div>
              <div className="text-[11px] text-slate-300">Shutting down workstation to minimize cloud & energy costs...</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-3xl font-black text-rose-400 font-mono tracking-widest bg-slate-950 px-4 py-1.5 rounded-xl border border-rose-500/40">
              00:{countdownSec < 10 ? `0${countdownSec}` : countdownSec}
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={onCancelShutdown}
                className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold font-mono flex items-center gap-1 border border-slate-700 transition"
              >
                <XMarkIcon className="w-4 h-4" /> Cancel Shutdown
              </button>
              <button
                onClick={onShutdownNow}
                className="px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold font-mono shadow-lg shadow-rose-600/30 flex items-center gap-1 transition"
              >
                <PowerIcon className="w-4 h-4" /> Shutdown Now
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs font-mono text-slate-400">
          <span className="flex items-center gap-1.5">
            <ShieldCheckIcon className="w-4 h-4 text-emerald-400" />
            {enabled
              ? 'Workstation will automatically trigger 30s countdown upon training completion.'
              : 'Auto Shutdown is disabled. Workstation will remain powered on post-training.'}
          </span>
          {enabled && (
            <button
              onClick={onShutdownNow}
              className="px-3 py-1 rounded-lg bg-rose-600/20 text-rose-300 border border-rose-500/30 hover:bg-rose-600/40 transition"
            >
              Test Shutdown
            </button>
          )}
        </div>
      )}
    </div>
  );
};
