import React, { useState } from 'react';
import {
  AdjustmentsHorizontalIcon,
  PlusIcon,
  PlayIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  PowerIcon,
  DocumentTextIcon,
  ArchiveBoxIcon,
  BellIcon,
  TrashIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';
import { automationApi } from '../services/automationApi';
import { useToast } from '../components/common/Toast';
import { SafetyCountdownModal } from '../components/automation/SafetyCountdownModal';

export const AutomationPage: React.FC = () => {
  const { showToast } = useToast();
  const [activeCountdown, setActiveCountdown] = useState<{ actionName: string; remainingSec: number } | null>(null);

  const [rules, setRules] = useState([
    {
      id: 'rule-1',
      name: 'Post-Training Success Auto-Shutdown Pipeline',
      trigger_event: 'ON_SUCCESS',
      actions_sequence: [
        { action_type: 'SAVE_BEST_MODEL', label: 'Save Best Model to ./output/best_models/' },
        { action_type: 'GENERATE_REPORT', label: 'Generate PDF Training Performance Report' },
        { action_type: 'COMPRESS_LOGS', label: 'Compress Session Logs to ZIP archive' },
        { action_type: 'NOTIFY_USER', label: 'Dispatch Desktop Toast Alert' },
        { action_type: 'SYSTEM_SHUTDOWN', label: 'Shutdown Computer (30s Safety Grace Period)' },
      ],
      is_active: true,
    },
    {
      id: 'rule-2',
      name: 'Training Failure Error Log & Summary Pipeline',
      trigger_event: 'ON_FAILED',
      actions_sequence: [
        { action_type: 'GENERATE_FAILURE_REPORT', label: 'Generate Failure Summary PDF' },
        { action_type: 'COMPRESS_LOGS', label: 'Compress Error Logs' },
        { action_type: 'NOTIFY_USER', label: 'Send Windows Toast Alert Notification' },
      ],
      is_active: true,
    },
    {
      id: 'rule-3',
      name: 'GPU Thermal Safeguard Pipeline',
      trigger_event: 'ON_OVERHEATING',
      actions_sequence: [
        { action_type: 'NOTIFY_USER', label: 'Alert GPU Temperature Limit Exceeded' },
      ],
      is_active: true,
    }
  ]);

  const [history] = useState([
    {
      id: 'hist-1',
      trigger_event: 'ON_SUCCESS',
      status: 'SUCCESS',
      duration_ms: 1420.5,
      timestamp: '15:02:15',
      executed_actions: [
        { action_type: 'SAVE_BEST_MODEL', message: 'Best model saved to ./output/best_models/best_model_run123.pt' },
        { action_type: 'GENERATE_REPORT', message: 'PDF report generated' },
        { action_type: 'COMPRESS_LOGS', message: 'Logs compressed to ZIP' },
        { action_type: 'NOTIFY_USER', message: 'Desktop notification sent' },
      ],
    },
  ]);

  const handleTestShutdown = () => {
    setActiveCountdown({ actionName: 'Shutdown', remainingSec: 30 });
  };

  const handleCancelCountdown = async () => {
    try {
      await automationApi.cancelCountdown('active');
      setActiveCountdown(null);
      showToast('Action Cancelled', 'Safety Manager cancelled computer shutdown.', 'info');
    } catch (err: any) {
      setActiveCountdown(null);
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <AdjustmentsHorizontalIcon className="w-6 h-6 text-blue-400" />
            Automation Engine & Workflow Pipelines
          </h1>
          <p className="text-slate-400 text-xs mt-1">Configurable post-training workflows, file actions, and safe Win32 power management.</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleTestShutdown}
            className="px-4 py-2 rounded-xl bg-amber-600/20 text-amber-300 border border-amber-500/30 text-xs font-semibold flex items-center gap-2 hover:bg-amber-600/30 transition"
          >
            <PowerIcon className="w-4 h-4" /> Test Safety Shutdown
          </button>
          <button className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-blue-500/20 transition">
            <PlusIcon className="w-4 h-4" /> Add Automation Rule
          </button>
        </div>
      </div>

      {/* Safety Manager Banner */}
      <div className="glass-panel p-5 rounded-2xl border-l-4 border-l-emerald-500 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <ShieldCheckIcon className="w-6 h-6 text-emerald-400 shrink-0" />
          <div>
            <h3 className="font-bold text-white text-sm">Safety Manager Active</h3>
            <p className="text-xs text-slate-400">
              All destructive system power actions (Shutdown, Sleep, Hibernate) enforce a 30s/60s grace period with manual cancellation.
            </p>
          </div>
        </div>
        <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-mono font-medium">
          Grace Period: 30s
        </span>
      </div>

      {/* Configured Automation Rules */}
      <div className="space-y-6">
        <h2 className="text-lg font-bold text-white tracking-tight">Active Automation Pipelines</h2>
        {rules.map((rule) => (
          <div key={rule.id} className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
                  <AdjustmentsHorizontalIcon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-base">{rule.name}</h3>
                  <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                    <span>Trigger Event:</span>
                    <span className="px-2.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono font-semibold">
                      {rule.trigger_event}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-slate-400 font-mono">Active Rule</span>
                <div className="w-10 h-5 rounded-full bg-blue-600 p-0.5 flex items-center justify-end cursor-pointer">
                  <div className="w-4 h-4 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

            {/* Action Steps Visual Pipeline */}
            <div className="p-4 bg-slate-900/60 rounded-xl space-y-3">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Configured Action Sequence (Chained)</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                {rule.actions_sequence.map((act, i) => (
                  <div key={i} className="p-3 bg-slate-800/60 border border-slate-700/60 rounded-xl space-y-1.5 text-xs">
                    <div className="flex items-center justify-between text-slate-400 font-mono text-[10px]">
                      <span>STEP {i + 1}</span>
                      {act.action_type === 'SAVE_BEST_MODEL' && <DocumentTextIcon className="w-3.5 h-3.5 text-blue-400" />}
                      {act.action_type === 'GENERATE_REPORT' && <DocumentTextIcon className="w-3.5 h-3.5 text-purple-400" />}
                      {act.action_type === 'COMPRESS_LOGS' && <ArchiveBoxIcon className="w-3.5 h-3.5 text-amber-400" />}
                      {act.action_type === 'NOTIFY_USER' && <BellIcon className="w-3.5 h-3.5 text-emerald-400" />}
                      {act.action_type === 'SYSTEM_SHUTDOWN' && <PowerIcon className="w-3.5 h-3.5 text-rose-400" />}
                    </div>
                    <p className="font-semibold text-slate-200">{act.label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Action Execution History Table */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base">Automation Execution History Log</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-slate-400 font-mono uppercase text-[10px]">
              <tr>
                <th className="p-3">Trigger Event</th>
                <th className="p-3">Execution Status</th>
                <th className="p-3">Executed Steps</th>
                <th className="p-3">Duration</th>
                <th className="p-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300 font-mono">
              {history.map((h) => (
                <tr key={h.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-blue-400">{h.trigger_event}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px]">
                      {h.status}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{h.executed_actions.length} Actions Completed</td>
                  <td className="p-3">{h.duration_ms.toFixed(1)} ms</td>
                  <td className="p-3 text-slate-500">{h.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Safety Countdown Modal */}
      {activeCountdown && (
        <SafetyCountdownModal
          actionName={activeCountdown.actionName}
          remainingSec={activeCountdown.remainingSec}
          onCancel={handleCancelCountdown}
        />
      )}
    </div>
  );
};
