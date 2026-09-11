import React from 'react';
import {
  CpuChipIcon,
  ServerIcon,
  FireIcon,
  BoltIcon,
  FolderIcon,
  PlayIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

export const DashboardPage: React.FC = () => {
  // Phase 1 Mock Data (No backend telemetry integration in Phase 1)
  const mockStats = {
    cpu: '45%',
    gpu: 'RTX 4090 - 88%',
    ram: '16.4 / 32.0 GB',
    temperature: '72°C',
    trainingStatus: 'IDLE (Ready)',
    todaysSessions: 3,
    recentProjects: 2,
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Executive Dashboard</h1>
        <p className="text-slate-400 text-xs mt-1">Single-computer system foundation and ML training overview.</p>
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        {/* CPU Card */}
        <div className="glass-panel p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">CPU Utilization</span>
            <CpuChipIcon className="w-5 h-5 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white">{mockStats.cpu}</div>
          <div className="text-[11px] text-slate-400 font-mono">16 Cores / 32 Threads</div>
        </div>

        {/* GPU Card */}
        <div className="glass-panel p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">GPU Compute</span>
            <BoltIcon className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white">88%</div>
          <div className="text-[11px] text-slate-400 font-mono">{mockStats.gpu}</div>
        </div>

        {/* RAM Card */}
        <div className="glass-panel p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">RAM Usage</span>
            <ServerIcon className="w-5 h-5 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-white">51%</div>
          <div className="text-[11px] text-slate-400 font-mono">{mockStats.ram}</div>
        </div>

        {/* Temperature Card */}
        <div className="glass-panel p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">GPU Temp</span>
            <FireIcon className="w-5 h-5 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-white">{mockStats.temperature}</div>
          <div className="text-[11px] text-slate-400 font-mono">Optimal Thermal Range</div>
        </div>
      </div>

      {/* Summary Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-2xl space-y-2">
          <div className="flex items-center gap-2 text-blue-400 font-semibold text-sm">
            <PlayIcon className="w-4 h-4" /> Training Status
          </div>
          <p className="text-xl font-bold text-white">{mockStats.trainingStatus}</p>
          <p className="text-xs text-slate-400">Phase 1 Foundation ready for session launches.</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl space-y-2">
          <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
            <CheckCircleIcon className="w-4 h-4" /> Today's Sessions
          </div>
          <p className="text-xl font-bold text-white">{mockStats.todaysSessions} Completed</p>
          <p className="text-xs text-slate-400">Recorded in PostgreSQL session logs.</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl space-y-2">
          <div className="flex items-center gap-2 text-purple-400 font-semibold text-sm">
            <FolderIcon className="w-4 h-4" /> Registered Projects
          </div>
          <p className="text-xl font-bold text-white">{mockStats.recentProjects} Active Projects</p>
          <p className="text-xs text-slate-400">Stored in database project registry.</p>
        </div>
      </div>
    </div>
  );
};
