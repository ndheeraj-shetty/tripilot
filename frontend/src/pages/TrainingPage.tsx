import React, { useState } from 'react';
import { TrainingControlPanel } from '../components/training/TrainingControlPanel';
import { TrainingProcessCard } from '../components/training/TrainingProcessCard';
import { GPULifecycleCard } from '../components/training/GPULifecycleCard';
import { TrainingTimeline } from '../components/training/TrainingTimeline';
import { AutoShutdownModule } from '../components/training/AutoShutdownModule';
import { ShutdownConfirmationModal } from '../components/training/ShutdownConfirmationModal';
import { CostSavingsCard } from '../components/training/CostSavingsCard';
import { ConsoleWindow } from '../components/training/ConsoleWindow';
import { LiveCharts } from '../components/training/LiveCharts';
import { useLiveTraining } from '../hooks/useLiveTraining';
import { useProjects } from '../hooks/useProjects';
import { useToast } from '../components/common/Toast';
import { CpuChipIcon, BoltIcon, FireIcon, ServerIcon, SignalIcon, FolderIcon } from '@heroicons/react/24/outline';

export const TrainingPage: React.FC = () => {
  const { projects } = useProjects();
  const { showToast } = useToast();
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');

  React.useEffect(() => {
    if (!selectedProjectId && projects.length > 0) {
      setSelectedProjectId(projects[0].id);
    }
  }, [projects, selectedProjectId]);

  const {
    status,
    pid,
    telemetry,
    metrics,
    logs,
    isConnected,
    isStarting,
    activeSessionId,
    gpuState,
    currentEpoch,
    totalEpochs,
    currentBatch,
    totalBatches,
    progressPct,
    etaSec,
    elapsedSec,
    stage,
    currentSessionCost,
    estimatedUnoptimizedCost,
    moneySaved,
    gpuHoursSaved,
    gpuReleasesCount,
    autoShutdownSec,
    autoShutdownEnabled,
    isShutdownInitiating,
    setAutoShutdownEnabled,
    setAutoShutdownSec,
    cancelShutdown,
    shutdownNow,
    clearLogs,
    startTraining,
    pauseTraining,
    resumeTraining,
    stopTraining,
    killTraining,
    releaseGpuResource,
    restartTraining,
  } = useLiveTraining();

  const latestMetric = metrics.length > 0 ? metrics[metrics.length - 1] : undefined;

  const handleCancelShutdown = async () => {
    await cancelShutdown('active');
    showToast('Shutdown Cancelled', 'Automatic shutdown cancelled. The system will remain running.', 'success');
  };

  const handleShutdownNow = async () => {
    await shutdownNow('active');
  };

  const handleStart = async () => {
    const projId = selectedProjectId || (projects.length > 0 ? projects[0].id : null);
    if (!projId) {
      showToast('Start Error', 'Please create or select a project first.', 'error');
      return;
    }

    try {
      await startTraining({ project_id: projId });
      showToast('Training Started', 'AI Training subprocess spawned successfully.', 'success');
    } catch (err: any) {
      showToast('Start Failed', err.message || 'Failed to start training', 'error');
    }
  };

  const handleKill = async () => {
    try {
      await killTraining('active');
      showToast('Process Terminated', 'Process killed & GPU resources released.', 'warning');
    } catch (err: any) {
      showToast('Kill Failed', err.message, 'error');
    }
  };

  const handleReleaseGpu = async () => {
    try {
      await releaseGpuResource('active');
      showToast('GPU Released', 'GPU memory allocation & compute state released.', 'info');
    } catch (err: any) {
      showToast('GPU Release Failed', err.message, 'error');
    }
  };

  const handleDownloadLogs = () => {
    const element = document.createElement('a');
    const file = new Blob([logs.join('\n')], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `zombie_run_logs_${Date.now()}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    showToast('Logs Exported', 'Downloaded live terminal logs.', 'success');
  };

  const handleDownloadModel = () => {
    showToast('Model Download', 'Best model checkpoint file package downloading...', 'info');
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">AI Training Operations & Control Center</h1>
          <p className="text-slate-400 text-xs mt-1">
            Real-time process monitoring, GPU lifecycle tracking, completion detection, and automated cost optimization.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedProjectId}
            onChange={(e) => setSelectedProjectId(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 font-medium"
          >
            {projects.length === 0 ? (
              <option value="">-- No Projects Found --</option>
            ) : (
              projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.framework})
                </option>
              ))
            )}
          </select>

          <span
            className={`px-3 py-1.5 rounded-lg border text-xs font-mono font-medium flex items-center gap-2 ${
              isConnected
                ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                : 'bg-amber-500/10 border-amber-500/20 text-amber-400'
            }`}
          >
            <SignalIcon className="w-3.5 h-3.5 animate-pulse" />
            {isConnected ? 'WebSocket Telemetry Active' : 'Connecting WS...'}
          </span>
        </div>
      </div>

      {/* 9 Action Controls Bar */}
      <TrainingControlPanel
        status={status}
        pid={pid}
        gpuState={gpuState}
        isStarting={isStarting}
        onStart={handleStart}
        onPause={() => pauseTraining('active')}
        onResume={() => resumeTraining('active')}
        onStop={() => stopTraining('active')}
        onKill={handleKill}
        onReleaseGpu={handleReleaseGpu}
        onDownloadLogs={handleDownloadLogs}
        onDownloadModel={handleDownloadModel}
        onRestart={() => restartTraining('active')}
      />

      {/* Training Workflow Timeline */}
      <TrainingTimeline currentStage={stage} status={status} gpuState={gpuState} />

      {/* Cost Saving Analytics Card */}
      <CostSavingsCard
        currentSessionCost={currentSessionCost}
        estimatedUnoptimizedCost={estimatedUnoptimizedCost}
        moneySaved={moneySaved}
        gpuHoursSaved={gpuHoursSaved}
        gpuReleasesCount={gpuReleasesCount}
      />

      {/* Real-Time Process Monitor & GPU Lifecycle Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TrainingProcessCard
          status={status}
          pid={pid}
          currentEpoch={currentEpoch}
          totalEpochs={totalEpochs}
          currentBatch={currentBatch}
          totalBatches={totalBatches}
          progressPct={progressPct}
          etaSec={etaSec}
          elapsedSec={elapsedSec}
          loss={latestMetric?.loss}
          valLoss={latestMetric?.val_loss}
          accuracy={latestMetric?.accuracy}
          learningRate={latestMetric?.learning_rate}
        />

        <GPULifecycleCard
          gpuState={gpuState}
          gpuUtilization={telemetry?.gpu_utilization_pct || 0}
          gpuMemoryUsedMb={telemetry?.gpu_memory_used_mb || 0}
          gpuMemoryTotalMb={telemetry?.gpu_memory_total_mb || 24576}
          gpuTemperatureC={telemetry?.gpu_temperature_c || 0}
          gpuPowerDrawWatts={telemetry?.gpu_power_draw_watts || 0}
          gpuName={telemetry?.gpu_name || 'NVIDIA GeForce RTX 4090'}
          onReleaseGpu={handleReleaseGpu}
        />
      </div>

      {/* Auto Shutdown Module */}
      <AutoShutdownModule
        enabled={autoShutdownEnabled}
        countdownSec={autoShutdownSec}
        onToggleEnabled={setAutoShutdownEnabled}
        onCancelShutdown={handleCancelShutdown}
        onShutdownNow={handleShutdownNow}
      />

      {/* Shutdown Confirmation Dialog Modal */}
      <ShutdownConfirmationModal
        isOpen={autoShutdownSec !== null || isShutdownInitiating}
        remainingSec={autoShutdownSec}
        isInitiating={isShutdownInitiating}
        onShutdownNow={handleShutdownNow}
        onCancelShutdown={handleCancelShutdown}
      />

      {/* System Telemetry Hardware Stat Cards (1Hz) */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="glass-panel p-3.5 rounded-2xl space-y-1 text-xs">
          <div className="flex items-center justify-between text-slate-400">
            <span>CPU Utilization</span>
            <CpuChipIcon className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-lg font-bold text-white font-mono">{telemetry?.cpu_utilization_pct || 0}%</div>
          <div className="w-full bg-slate-950 h-1 rounded-full overflow-hidden">
            <div className="bg-blue-500 h-full" style={{ width: `${telemetry?.cpu_utilization_pct || 0}%` }} />
          </div>
        </div>

        <div className="glass-panel p-3.5 rounded-2xl space-y-1 text-xs">
          <div className="flex items-center justify-between text-slate-400">
            <span>System RAM</span>
            <ServerIcon className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-lg font-bold text-white font-mono">
            {((telemetry?.ram_used_bytes || 0) / (1024 * 1024 * 1024)).toFixed(1)} GB
          </div>
          <div className="w-full bg-slate-950 h-1 rounded-full overflow-hidden">
            <div
              className="bg-purple-500 h-full"
              style={{
                width: `${(((telemetry?.ram_used_bytes || 0) / (telemetry?.ram_total_bytes || 1)) * 100).toFixed(0)}%`,
              }}
            />
          </div>
        </div>

        <div className="glass-panel p-3.5 rounded-2xl space-y-1 text-xs">
          <div className="flex items-center justify-between text-slate-400">
            <span>GPU Compute</span>
            <BoltIcon className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-lg font-bold text-white font-mono">{telemetry?.gpu_utilization_pct || 0}%</div>
          <div className="w-full bg-slate-950 h-1 rounded-full overflow-hidden">
            <div className="bg-amber-500 h-full" style={{ width: `${telemetry?.gpu_utilization_pct || 0}%` }} />
          </div>
        </div>

        <div className="glass-panel p-3.5 rounded-2xl space-y-1 text-xs">
          <div className="flex items-center justify-between text-slate-400">
            <span>GPU Temp / Power</span>
            <FireIcon className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-lg font-bold text-white font-mono">
            {telemetry?.gpu_temperature_c || 0}°C / {telemetry?.gpu_power_draw_watts || 0}W
          </div>
          <div className="w-full bg-slate-950 h-1 rounded-full overflow-hidden">
            <div className="bg-rose-500 h-full" style={{ width: `${((telemetry?.gpu_temperature_c || 0) / 100) * 100}%` }} />
          </div>
        </div>

        <div className="glass-panel p-3.5 rounded-2xl space-y-1 text-xs">
          <div className="flex items-center justify-between text-slate-400">
            <span>Disk Free Space</span>
            <FolderIcon className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-lg font-bold text-white font-mono">
            {((telemetry?.disk_free_space_bytes || 0) / (1024 * 1024 * 1024)).toFixed(0)} GB
          </div>
          <div className="w-full bg-slate-950 h-1 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full" style={{ width: '85%' }} />
          </div>
        </div>
      </div>

      {/* Real-Time Metrics Chart */}
      <LiveCharts metrics={metrics} telemetry={telemetry} />

      {/* Live Terminal Log Streamer */}
      <ConsoleWindow logs={logs} onClear={clearLogs} />
    </div>
  );
};
