import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FolderKanban,
  PlaySquare,
  BarChart3,
  Workflow,
  FileCheck,
  FileSpreadsheet,
  Settings,
  Cpu
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/projects', label: 'Projects', icon: FolderKanban },
    { to: '/training', label: 'Live Training', icon: PlaySquare },
    { to: '/analytics', label: 'Analytics', icon: BarChart3 },
    { to: '/automation', label: 'Automation Rules', icon: Workflow },
    { to: '/checkpoints', label: 'Checkpoints', icon: FileCheck },
    { to: '/reports', label: 'Reports', icon: FileSpreadsheet },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 glass-panel h-screen flex flex-col border-r border-slate-800/80 select-none">
      {/* Brand Header */}
      <div className="p-6 flex items-center gap-3 border-b border-slate-800/60">
        <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30 shadow-lg shadow-blue-500/10">
          <Cpu className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h1 className="font-bold text-lg tracking-wide text-white flex items-center gap-1.5">
            Zombie Run <span className="text-blue-500 text-xs px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 font-mono">CK</span>
          </h1>
          <p className="text-xs text-slate-400 font-medium">Cost Killer Platform v1.0</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Status Footer */}
      <div className="p-4 border-t border-slate-800/60 bg-slate-900/40">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            Engine Active
          </span>
          <span className="text-slate-500 font-mono">Local Win32</span>
        </div>
      </div>
    </aside>
  );
};
