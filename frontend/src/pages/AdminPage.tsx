import React, { useState } from 'react';
import { UserIcon, ShieldCheckIcon, CpuChipIcon, KeyIcon } from '@heroicons/react/24/outline';

export const AdminPage: React.FC = () => {
  const [users] = useState([
    { id: '1', email: 'admin@zombierun.ai', name: 'Lead Architect', role: 'ADMIN', status: 'ACTIVE' },
    { id: '2', email: 'mle@zombierun.ai', name: 'ML Engineer', role: 'ML_ENGINEER', status: 'ACTIVE' },
  ]);

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <ShieldCheckIcon className="w-6 h-6 text-blue-400" />
          Admin & User Management Hub (RBAC)
        </h1>
        <p className="text-slate-400 text-xs mt-1">Role-based access controls, user provisioning, and enterprise audit logs.</p>
      </div>

      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base">User Accounts & Roles</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-slate-400 font-mono uppercase text-[10px]">
              <tr>
                <th className="p-3">User Email</th>
                <th className="p-3">Full Name</th>
                <th className="p-3">Role</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300 font-mono">
              {users.map((u) => (
                <tr key={u.id}>
                  <td className="p-3 font-semibold text-white">{u.email}</td>
                  <td className="p-3 text-slate-400">{u.name}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 text-[10px] font-bold">
                      {u.role}
                    </span>
                  </td>
                  <td className="p-3 text-emerald-400">{u.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
