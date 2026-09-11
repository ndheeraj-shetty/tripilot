import React from 'react';
import {
  CpuChipIcon,
  ClockIcon,
  AcademicCapIcon,
  CircleStackIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';

interface TrainingProcessCardProps {
  status: string;
  pid: number | null;
  currentEpoch: number;
  totalEpochs: number;
  currentBatch: number;
  totalBatches: number;
  progressPct: number;
  etaSec: number;
  elapsedSec: number;
  loss?: number;
  valLoss?: number;
  accuracy?: number;
  learningRate?: number;
}

export const TrainingProcessCard: React.FC<TrainingProcessCardProps> = ({
  status,
  pid,
  currentEpoch,
  totalEpochs,
  currentBatch,
  totalBatches,
  progressPct,
  etaSec,
  elapsedSec,
  loss,
  valLoss,
  accuracy,
  learningRate,
}) => {
  const getStatusBadge = () => {
    switch (status.toUpperCase()) {
      case 'RUNNING':
      case 'TRAINING':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/40 animate-pulse';
      case 'VALIDATING':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/40 animate-pulse';
      case 'SAVING MODEL':
      case 'SAVING_MODEL':
        return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
      case 'COMPLETED':
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
      case 'FAILED':
      case 'CANCELLED':
        return 'bg-rose-500/20 text-rose-400 border-rose-500/40';
      case 'PAUSED':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  const formatTime = (sec: number) => {
    const mins = Math.floor(sec / 60);
    const secs = Math.floor(sec % 60);
    return `${mins}m ${secs}s`;
  };

  return (
    <div className="glass-panel p-5 rounded-2xl space-y-4 border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <CpuChipIcon className="w-5 h-5 text-blue-400" />
          <h3 className="font-bold text-white text-sm tracking-tight">Real-Time Training Process Monitor</h3>
        </div>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className={`px-2.5 py-1 rounded-full border text-[11px] font-bold ${getStatusBadge()}`}>
            {status}
          </span>
          <span className="bg-slate-900 border border-slate-800 px-2 py-1 rounded-md text-slate-400">
            PID: {pid || 'N/A'}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs font-mono text-slate-300">
          <span>Overall Training Progress</span>
          <span className="font-bold text-blue-400">{progressPct}%</span>
        </div>
        <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
          <div
            className="bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400 h-full rounded-full transition-all duration-500"
            style={{ width: `${Math.min(100, Math.max(0, progressPct))}%` }}
          />
        </div>
      </div>

      {/* Key Metric Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2 text-xs font-mono">
        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-slate-400 text-[10px] uppercase flex items-center gap-1">
            <AcademicCapIcon className="w-3.5 h-3.5 text-blue-400" /> Current Epoch
          </div>
          <div className="text-base font-bold text-white mt-1">
            {currentEpoch} <span className="text-slate-500 text-xs">/ {totalEpochs}</span>
          </div>
        </div>

        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-slate-400 text-[10px] uppercase flex items-center gap-1">
            <CircleStackIcon className="w-3.5 h-3.5 text-purple-400" /> Current Batch
          </div>
          <div className="text-base font-bold text-white mt-1">
            {currentBatch} <span className="text-slate-500 text-xs">/ {totalBatches}</span>
          </div>
        </div>

        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-slate-400 text-[10px] uppercase flex items-center gap-1">
            <ClockIcon className="w-3.5 h-3.5 text-amber-400" /> Elapsed / ETA
          </div>
          <div className="text-base font-bold text-white mt-1">
            {formatTime(elapsedSec)} <span className="text-slate-500 text-xs">/ {formatTime(etaSec)}</span>
          </div>
        </div>

        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-slate-400 text-[10px] uppercase flex items-center gap-1">
            <SparklesIcon className="w-3.5 h-3.5 text-emerald-400" /> Accuracy / LR
          </div>
          <div className="text-base font-bold text-emerald-400 mt-1">
            {accuracy !== undefined ? `${(accuracy * 100).toFixed(1)}%` : 'N/A'}{' '}
            <span className="text-slate-500 text-[10px]">({learningRate || 0.001})</span>
          </div>
        </div>
      </div>
    </div>
  );
};
