import React, { useState, useEffect } from 'react';
import { CheckCircleIcon, PowerIcon, ArrowPathIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface ShutdownConfirmationModalProps {
  isOpen: boolean;
  remainingSec: number | null;
  totalSec?: number;
  isInitiating?: boolean;
  onShutdownNow: () => void;
  onCancelShutdown: () => void;
}

export const ShutdownConfirmationModal: React.FC<ShutdownConfirmationModalProps> = ({
  isOpen,
  remainingSec,
  totalSec = 30,
  isInitiating = false,
  onShutdownNow,
  onCancelShutdown,
}) => {
  const [loadingAction, setLoadingAction] = useState<boolean>(false);

  useEffect(() => {
    if (isInitiating) {
      setLoadingAction(true);
    }
  }, [isInitiating]);

  if (!isOpen) return null;

  const currentSec = remainingSec !== null ? Math.max(0, remainingSec) : totalSec;
  const isTimeExpired = currentSec === 0 || isInitiating;
  const progressPct = Math.min(100, Math.max(0, (currentSec / totalSec) * 100));

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    const pad = (n: number) => (n < 10 ? `0${n}` : `${n}`);
    return `${pad(mins)}:${pad(secs)}`;
  };

  const handleShutdownClick = () => {
    setLoadingAction(true);
    onShutdownNow();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md transition-opacity animate-fade-in"
      onClick={(e) => e.stopPropagation()} // Prevent closing on outside click
    >
      <div
        className="w-full max-w-lg bg-slate-900 border border-slate-700/60 rounded-3xl p-6 md:p-8 shadow-2xl shadow-rose-950/30 space-y-6 text-center transform transition-all scale-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header Icon & Title */}
        <div className="flex flex-col items-center gap-3">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shadow-lg shadow-emerald-500/10">
            <CheckCircleIcon className="w-10 h-10 animate-bounce-short" />
          </div>
          <div>
            <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
              Training Completed Successfully
            </h2>
            <p className="text-xs text-emerald-400 font-medium mt-1 flex items-center justify-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping inline-block" />
              GPU resources released & model saved
            </p>
          </div>
        </div>

        {/* Dynamic Status / Message Box */}
        {isTimeExpired ? (
          <div className="p-4 rounded-2xl bg-rose-950/60 border border-rose-500/50 text-rose-200 text-sm space-y-2 animate-pulse">
            <div className="flex items-center justify-center gap-2 font-semibold">
              <ExclamationTriangleIcon className="w-5 h-5 text-rose-400" />
              <span>No response received.</span>
            </div>
            <p className="text-xs opacity-90">Initiating automatic shutdown...</p>
          </div>
        ) : (
          <div className="text-slate-300 text-xs md:text-sm leading-relaxed space-y-1 bg-slate-950/50 p-4 rounded-2xl border border-slate-800">
            <p>Training has finished successfully.</p>
            <p>GPU resources have been released.</p>
            <p className="text-slate-400 text-xs mt-1">
              The system will automatically shut down in <strong>30 seconds</strong> unless you choose an option below.
            </p>
          </div>
        )}

        {/* Large Countdown Timer Display */}
        <div className="space-y-2 py-2">
          <span className="text-xs font-mono uppercase tracking-widest text-slate-400 font-semibold">
            {isTimeExpired ? 'Shutdown Status' : 'Automatic Shutdown In'}
          </span>
          <div className="text-4xl md:text-5xl font-black font-mono tracking-wider text-rose-400 bg-slate-950 py-3 px-6 rounded-2xl border border-rose-500/30 shadow-inner flex items-center justify-center gap-3">
            {loadingAction || isInitiating ? (
              <div className="flex items-center gap-3 text-2xl text-rose-300">
                <ArrowPathIcon className="w-7 h-7 animate-spin text-rose-400" />
                <span>Initiating...</span>
              </div>
            ) : (
              formatTimer(currentSec)
            )}
          </div>
        </div>

        {/* Animated Progress Bar decreasing over 30s */}
        <div className="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden p-0.5 border border-slate-800">
          <div
            className={`h-full rounded-full transition-all duration-1000 ease-linear ${
              progressPct < 30 ? 'bg-rose-500' : progressPct < 60 ? 'bg-amber-500' : 'bg-emerald-500'
            }`}
            style={{ width: `${progressPct}%` }}
          />
        </div>

        {/* Interactive Buttons */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
          {/* Shutdown Now (Red) */}
          <button
            onClick={handleShutdownClick}
            disabled={loadingAction}
            className="w-full py-3 px-4 rounded-2xl bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white text-xs md:text-sm font-bold font-mono shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 border border-rose-500 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            {loadingAction ? (
              <>
                <ArrowPathIcon className="w-4 h-4 animate-spin" />
                <span>Initiating...</span>
              </>
            ) : (
              <>
                <PowerIcon className="w-4 h-4" />
                <span>Shutdown Now</span>
              </>
            )}
          </button>

          {/* Cancel Shutdown (Gray / Blue) */}
          <button
            onClick={onCancelShutdown}
            disabled={loadingAction}
            className="w-full py-3 px-4 rounded-2xl bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-slate-200 text-xs md:text-sm font-bold font-mono border border-slate-700 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            <span>Cancel Shutdown</span>
          </button>
        </div>
      </div>
    </div>
  );
};
