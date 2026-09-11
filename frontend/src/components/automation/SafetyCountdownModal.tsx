import React from 'react';
import { ExclamationTriangleIcon, XMarkIcon, PowerIcon } from '@heroicons/react/24/outline';

interface SafetyCountdownModalProps {
  actionName: string;
  remainingSec: number;
  onCancel: () => void;
}

export const SafetyCountdownModal: React.FC<SafetyCountdownModalProps> = ({
  actionName,
  remainingSec,
  onCancel,
}) => {
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 z-50">
      <div className="glass-panel w-full max-w-md p-6 rounded-2xl space-y-5 border-2 border-rose-500/50 bg-rose-950/30 text-center animate-bounce-short">
        <div className="p-3 bg-rose-600/20 text-rose-400 rounded-full w-14 h-14 mx-auto flex items-center justify-center border border-rose-500/40">
          <PowerIcon className="w-8 h-8 animate-pulse" />
        </div>

        <div>
          <h2 className="text-xl font-extrabold text-white tracking-tight uppercase">
            Computer {actionName} Scheduled
          </h2>
          <p className="text-xs text-rose-200 mt-1">
            Zombie Run Cost Killer is preparing to execute scheduled power action.
          </p>
        </div>

        {/* Big Countdown Display */}
        <div className="p-6 rounded-2xl bg-slate-950/80 border border-rose-500/30">
          <div className="text-5xl font-black text-rose-400 font-mono tracking-widest">
            00:{remainingSec < 10 ? `0${remainingSec}` : remainingSec}
          </div>
          <span className="text-[11px] text-slate-400 font-mono mt-1 block">Seconds Remaining</span>
        </div>

        <button
          onClick={onCancel}
          className="w-full py-3 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-sm tracking-wide shadow-lg shadow-rose-600/30 transition flex items-center justify-center gap-2"
        >
          <XMarkIcon className="w-5 h-5" /> CANCEL COMPUTER {actionName.toUpperCase()}
        </button>
      </div>
    </div>
  );
};
