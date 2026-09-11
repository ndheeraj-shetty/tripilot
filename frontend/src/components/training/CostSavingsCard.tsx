import React from 'react';
import { CurrencyDollarIcon, BanknotesIcon, ClockIcon, BoltIcon, ArrowTrendingUpIcon } from '@heroicons/react/24/outline';

interface CostSavingsCardProps {
  currentSessionCost: number;
  estimatedUnoptimizedCost: number;
  moneySaved: number;
  gpuHoursSaved: number;
  gpuReleasesCount: number;
}

export const CostSavingsCard: React.FC<CostSavingsCardProps> = ({
  currentSessionCost,
  estimatedUnoptimizedCost,
  moneySaved,
  gpuHoursSaved,
  gpuReleasesCount,
}) => {
  return (
    <div className="glass-panel p-5 rounded-2xl space-y-4 border border-slate-800 shadow-xl bg-gradient-to-br from-slate-900/90 via-slate-900/60 to-emerald-950/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BanknotesIcon className="w-5 h-5 text-emerald-400" />
          <h3 className="font-bold text-white text-sm tracking-tight">Cost Saving Analytics</h3>
        </div>
        <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono text-[11px] font-bold">
          Configured Rate: $2.50 / GPU Hr
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 font-mono text-xs">
        <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
          <div className="text-slate-400 text-[10px] uppercase">Current Session Cost</div>
          <div className="text-lg font-bold text-white mt-1">${currentSessionCost.toFixed(2)}</div>
        </div>

        <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
          <div className="text-slate-400 text-[10px] uppercase">Estimated Unoptimized</div>
          <div className="text-lg font-bold text-rose-400 mt-1">${estimatedUnoptimizedCost.toFixed(2)}</div>
        </div>

        <div className="bg-emerald-950/30 p-3 rounded-xl border border-emerald-500/30">
          <div className="text-emerald-400 text-[10px] uppercase font-bold flex items-center gap-1">
            <CurrencyDollarIcon className="w-3.5 h-3.5" /> Total Money Saved
          </div>
          <div className="text-lg font-extrabold text-emerald-400 mt-1">${moneySaved.toFixed(2)}</div>
        </div>

        <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
          <div className="text-slate-400 text-[10px] uppercase flex items-center gap-1">
            <ClockIcon className="w-3.5 h-3.5 text-blue-400" /> GPU Hours Saved
          </div>
          <div className="text-lg font-bold text-blue-300 mt-1">{gpuHoursSaved} hrs</div>
        </div>

        <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
          <div className="text-slate-400 text-[10px] uppercase flex items-center gap-1">
            <BoltIcon className="w-3.5 h-3.5 text-amber-400" /> Auto GPU Releases
          </div>
          <div className="text-lg font-bold text-amber-400 mt-1">{gpuReleasesCount}</div>
        </div>
      </div>
    </div>
  );
};
