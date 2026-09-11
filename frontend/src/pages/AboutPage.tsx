import React from 'react';
import { InformationCircleIcon, CpuChipIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">About Zombie Run Cost Killer</h1>
        <p className="text-slate-400 text-xs mt-1">AI-Powered ML Training Cost Optimization & Automation Platform.</p>
      </div>

      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <CpuChipIcon className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Zombie Run Cost Killer v1.0 (Local Edition)</h3>
            <p className="text-xs text-slate-400">AI-Powered ML Training Cost Optimization & Automation Platform</p>
          </div>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed">
          Zombie Run Cost Killer is an active, autonomous co-pilot designed to automate model training lifecycles, eliminate manual monitoring, kill runaway or stalled zombie runs, detect training anomalies, and trigger automatic post-training actions (such as saving best models, rendering reports, compressing log files, and shutting down local workstations).
        </p>

        <div className="pt-4 border-t border-slate-800 space-y-2">
          <h4 className="text-xs font-semibold text-white uppercase tracking-wider">Phase 1 Foundation Core Capabilities</h4>
          <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
            <li>Clean Architecture + Repository Pattern + Service Layer</li>
            <li>Normalized PostgreSQL database schema & Alembic migration pipeline</li>
            <li>FastAPI backend REST endpoints for Project & System Settings CRUD</li>
            <li>React 18 + Vite + TypeScript frontend with Tailwind CSS dark theme</li>
            <li>React Query (TanStack Query) data fetching & React Hook Form + Zod validation</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
