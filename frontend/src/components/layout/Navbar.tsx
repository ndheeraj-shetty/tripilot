import React from 'react';
import { CpuChipIcon, SignalIcon, CircleStackIcon } from '@heroicons/react/24/outline';

export const Navbar: React.FC = () => {
  return (
    <header className="h-16 border-b border-slate-800 bg-[#090d16]/80 backdrop-blur-md px-6 flex items-center justify-between select-none sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
          <span className="px-2 py-1 rounded bg-slate-800 border border-slate-700 text-blue-400 font-semibold">V1 Local</span>
          <span>Single Computer Engine</span>
        </div>
      </div>

      <div className="flex items-center gap-4 text-xs font-mono">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
          <SignalIcon className="w-3.5 h-3.5 animate-pulse" />
          <span>Backend Connected (Port 8000)</span>
        </div>
        <div className="flex items-center gap-2 text-slate-400">
          <CircleStackIcon className="w-4 h-4 text-blue-400" />
          <span>PostgreSQL Active</span>
        </div>
      </div>
    </header>
  );
};
