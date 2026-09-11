import React from 'react';
import { ChartBarIcon } from '@heroicons/react/24/outline';

export const AnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Analytics & Historical Trends</h1>
        <p className="text-slate-400 text-xs mt-1">Resource utilization history and cost savings estimation.</p>
      </div>

      <div className="glass-panel p-8 rounded-2xl text-center space-y-4 border border-purple-500/20 bg-purple-950/10">
        <div className="p-3 bg-purple-600/20 text-purple-400 rounded-full w-12 h-12 mx-auto flex items-center justify-center">
          <ChartBarIcon className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-bold text-white">Historical Analytics & Metrics Engine (Phase 4)</h3>
        <p className="text-xs text-slate-400 max-w-md mx-auto">
          Phase 1 Foundation complete. Time-series metrics analysis and resource utilization reporting will be active in later phases.
        </p>
      </div>
    </div>
  );
};
