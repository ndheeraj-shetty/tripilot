import React from 'react';
import { BoltIcon, FireIcon, CheckCircleIcon, SparklesIcon } from '@heroicons/react/24/outline';

interface GPULifecycleCardProps {
  gpuState?: 'Active' | 'Idle' | 'Released';
  gpuUtilization?: number;
  gpuMemoryUsedMb?: number;
  gpuMemoryTotalMb?: number;
  gpuTemperatureC?: number;
  gpuPowerDrawWatts?: number;
  gpuName?: string;
  onReleaseGpu?: () => void;
}

export const GPULifecycleCard: React.FC<GPULifecycleCardProps> = ({
  gpuState = 'Active',
  gpuUtilization = 0,
  gpuMemoryUsedMb = 0,
  gpuMemoryTotalMb = 24576,
  gpuTemperatureC = 0,
  gpuPowerDrawWatts = 0,
  gpuName = 'NVIDIA GeForce RTX 4090',
  onReleaseGpu,
}) => {
  const getGpuStateBadge = () => {
    switch (gpuState) {
      case 'Active':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse';
      case 'Released':
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
      case 'Idle':
      default:
        return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  const memFreeMb = Math.max(0, gpuMemoryTotalMb - gpuMemoryUsedMb);
  const memUsedGb = (gpuMemoryUsedMb / 1024).toFixed(1);
  const memTotalGb = (gpuMemoryTotalMb / 1024).toFixed(1);

  return (
    <div className="glass-panel p-5 rounded-2xl space-y-4 border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BoltIcon className="w-5 h-5 text-amber-400" />
          <div>
            <h3 className="font-bold text-white text-sm tracking-tight">GPU Lifecycle & Hardware Monitor</h3>
            <p className="text-[11px] text-slate-400 font-mono">{gpuName}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`px-2.5 py-1 rounded-full border text-xs font-mono font-bold ${getGpuStateBadge()}`}>
            Status: {gpuState}
          </span>
          {gpuState === 'Active' && onReleaseGpu && (
            <button
              onClick={onReleaseGpu}
              className="px-2.5 py-1 rounded-lg bg-rose-600/20 text-rose-300 border border-rose-500/30 text-xs font-mono hover:bg-rose-600/40 transition"
              title="Manually release GPU memory allocation"
            >
              Release GPU
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80 space-y-1">
          <div className="text-slate-400 text-[10px] uppercase">GPU Utilization</div>
          <div className="text-lg font-bold text-amber-400">{gpuUtilization}%</div>
          <div className="w-full bg-slate-950 h-1.5 rounded-full overflow-hidden">
            <div className="bg-amber-500 h-full" style={{ width: `${gpuUtilization}%` }} />
          </div>
        </div>

        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80 space-y-1">
          <div className="text-slate-400 text-[10px] uppercase">VRAM Used / Total</div>
          <div className="text-lg font-bold text-purple-400">
            {memUsedGb} <span className="text-slate-500 text-xs">/ {memTotalGb} GB</span>
          </div>
          <div className="w-full bg-slate-950 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-purple-500 h-full"
              style={{ width: `${Math.min(100, (gpuMemoryUsedMb / gpuMemoryTotalMb) * 100)}%` }}
            />
          </div>
        </div>

        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80 space-y-1">
          <div className="text-slate-400 text-[10px] uppercase">GPU Temp / Power</div>
          <div className="text-lg font-bold text-rose-400">
            {gpuTemperatureC}°C <span className="text-slate-500 text-xs">/ {gpuPowerDrawWatts}W</span>
          </div>
          <div className="w-full bg-slate-950 h-1.5 rounded-full overflow-hidden">
            <div className="bg-rose-500 h-full" style={{ width: `${(gpuTemperatureC / 100) * 100}%` }} />
          </div>
        </div>

        <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80 space-y-1">
          <div className="text-slate-400 text-[10px] uppercase">Automatic Release</div>
          <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5 mt-1">
            <CheckCircleIcon className="w-4 h-4" /> Enabled
          </div>
          <span className="text-[10px] text-slate-500 block">VRAM auto-freed on finish</span>
        </div>
      </div>
    </div>
  );
};
