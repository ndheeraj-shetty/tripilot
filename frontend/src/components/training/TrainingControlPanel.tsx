import React from 'react';
import {
  PlayIcon,
  PauseIcon,
  StopIcon,
  ArrowPathIcon,
  CpuChipIcon,
  XMarkIcon,
  BoltIcon,
  ArrowDownTrayIcon,
  CubeIcon
} from '@heroicons/react/24/outline';

interface TrainingControlPanelProps {
  status: string;
  pid: number | null;
  gpuState?: string;
  isStarting?: boolean;
  onStart: () => void;
  onPause: () => void;
  onResume: () => void;
  onStop: () => void;
  onKill: () => void;
  onReleaseGpu: () => void;
  onDownloadLogs: () => void;
  onDownloadModel: () => void;
  onRestart: () => void;
}

export const TrainingControlPanel: React.FC<TrainingControlPanelProps> = ({
  status,
  pid,
  gpuState = 'Idle',
  isStarting = false,
  onStart,
  onPause,
  onResume,
  onStop,
  onKill,
  onReleaseGpu,
  onDownloadLogs,
  onDownloadModel,
  onRestart,
}) => {
  const isRunning = status === 'RUNNING';
  const isPaused = status === 'PAUSED';
  const isActive = isRunning || isPaused;

  return (
    <div className="glass-panel p-6 rounded-2xl flex flex-col xl:flex-row items-center justify-between gap-4 border border-slate-800 shadow-xl">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
          <CpuChipIcon className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h2 className="font-bold text-lg text-white">Action Control Center</h2>
            <span
              className={`px-2.5 py-0.5 rounded-full text-xs font-semibold font-mono ${
                isRunning
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : isPaused
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  : 'bg-slate-800 text-slate-400 border border-slate-700'
              }`}
            >
              {status}
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            {pid ? `Sub-Process PID: ${pid} | GPU State: ${gpuState}` : 'No active process currently running.'}
          </p>
        </div>
      </div>

      {/* 9 Action Controls */}
      <div className="flex items-center gap-2 flex-wrap">
        {!isRunning && !isPaused && (
          <button
            onClick={onStart}
            disabled={isStarting}
            className={`px-3.5 py-2 rounded-xl text-white text-xs font-semibold flex items-center gap-1.5 shadow-lg transition ${
              isStarting
                ? 'bg-blue-800 cursor-not-allowed opacity-75'
                : 'bg-blue-600 hover:bg-blue-500 shadow-blue-500/20'
            }`}
          >
            {isStarting ? (
              <>
                <ArrowPathIcon className="w-4 h-4 animate-spin" /> Starting...
              </>
            ) : (
              <>
                <PlayIcon className="w-4 h-4" /> Start Training
              </>
            )}
          </button>
        )}

        {isRunning && (
          <button
            onClick={onPause}
            className="px-3.5 py-2 rounded-xl bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <PauseIcon className="w-4 h-4" /> Pause
          </button>
        )}

        {isPaused && (
          <button
            onClick={onResume}
            className="px-3.5 py-2 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <PlayIcon className="w-4 h-4" /> Resume
          </button>
        )}

        {isActive && (
          <button
            onClick={onStop}
            className="px-3.5 py-2 rounded-xl bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <StopIcon className="w-4 h-4" /> Graceful Stop
          </button>
        )}

        {isActive && (
          <button
            onClick={onKill}
            className="px-3.5 py-2 rounded-xl bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <XMarkIcon className="w-4 h-4" /> Kill Process
          </button>
        )}

        <button
          onClick={onReleaseGpu}
          className="px-3.5 py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
        >
          <BoltIcon className="w-4 h-4" /> Release GPU
        </button>

        <button
          onClick={onDownloadLogs}
          className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition"
        >
          <ArrowDownTrayIcon className="w-4 h-4" /> Logs
        </button>

        <button
          onClick={onDownloadModel}
          className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition"
        >
          <CubeIcon className="w-4 h-4" /> Download Model
        </button>

        <button
          onClick={onRestart}
          className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition"
        >
          <ArrowPathIcon className="w-4 h-4" /> Restart
        </button>
      </div>
    </div>
  );
};
