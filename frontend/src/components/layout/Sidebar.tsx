import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Squares2X2Icon,
  FolderIcon,
  PlayIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  BeakerIcon,
  DocumentChartBarIcon,
  AdjustmentsHorizontalIcon,
  InformationCircleIcon,
  CpuChipIcon,
  SparklesIcon,
  BookmarkIcon,
  ScaleIcon,
  DocumentTextIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: Squares2X2Icon },
    { to: '/ai-hub', label: 'AI Co-Pilot Hub', icon: SparklesIcon },
    { to: '/projects', label: 'Projects', icon: FolderIcon },
    { to: '/training', label: 'Live Training', icon: PlayIcon },
    { to: '/history', label: 'Training History', icon: ClockIcon },
    { to: '/checkpoints', label: 'Checkpoints', icon: BookmarkIcon },
    { to: '/compare', label: 'Model Comparison', icon: ScaleIcon },
    { to: '/analytics', label: 'Analytics', icon: ChartBarIcon },
    { to: '/reports', label: 'Reports & Export', icon: DocumentTextIcon },
    { to: '/automation', label: 'Automation Rules', icon: AdjustmentsHorizontalIcon },
    { to: '/settings', label: 'Settings', icon: Cog6ToothIcon },
  ];

  return (
    <aside className="w-64 bg-slate-900/95 border-r border-slate-800 flex flex-col justify-between shrink-0 select-none">
      <div>
        {/* Brand Header */}
        <div className="p-6 flex items-center gap-3 border-b border-slate-800/80">
          <div className="p-2 bg-gradient-to-tr from-blue-600 to-indigo-500 rounded-xl shadow-lg shadow-blue-500/20 text-white">
            <CpuChipIcon className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-extrabold text-white text-base tracking-tight flex items-center gap-1.5">
              Zombie Run <span className="text-blue-400 text-xs px-1.5 py-0.5 rounded bg-blue-500/10 border border-blue-500/20 font-mono">CK</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-medium">Cost Optimization & Automation</p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30 shadow-md shadow-blue-500/10'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`
              }
            >
              <item.icon className="w-4 h-4 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800/80">
        <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-400 text-[11px] font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Single PC (v1.0)</span>
          </div>
          <InformationCircleIcon className="w-4 h-4 text-slate-500" />
        </div>
      </div>
    </aside>
  );
};
