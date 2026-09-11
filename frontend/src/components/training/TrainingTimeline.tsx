import React from 'react';
import { CheckCircleIcon, PlayIcon, SparklesIcon, PowerIcon } from '@heroicons/react/24/solid';

interface TrainingTimelineProps {
  currentStage: string;
  status: string;
  gpuState: string;
}

const STAGES = [
  { id: 'DATASET_LOADED', label: 'Dataset Loaded' },
  { id: 'ENVIRONMENT_READY', label: 'Environment Ready' },
  { id: 'TRAINING_STARTED', label: 'Training Started' },
  { id: 'TRAINING_RUNNING', label: 'Training Running' },
  { id: 'MODEL_SAVING', label: 'Model Saving' },
  { id: 'COMPLETED', label: 'Training Completed' },
  { id: 'GPU_RELEASED', label: 'GPU Released' },
  { id: 'SHUTDOWN', label: 'Auto Shutdown' },
];

export const TrainingTimeline: React.FC<TrainingTimelineProps> = ({ currentStage, status, gpuState }) => {
  const getStageIndex = () => {
    const s = currentStage.toUpperCase();
    const st = status.toUpperCase();

    if (st === 'COMPLETED') {
      if (gpuState === 'Released') return 6;
      return 5;
    }
    if (s.includes('SAVING') || st === 'SAVING_MODEL') return 4;
    if (s.includes('RUNNING') || st === 'RUNNING' || st === 'TRAINING') return 3;
    if (s.includes('STARTED')) return 2;
    if (s.includes('ENV')) return 1;
    if (s.includes('DATASET')) return 0;
    if (st === 'STARTING' || st === 'INITIALIZING') return 1;
    return -1;
  };

  const activeIdx = getStageIndex();

  return (
    <div className="glass-panel p-5 rounded-2xl space-y-4 border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-white text-sm tracking-tight flex items-center gap-2">
          <SparklesIcon className="w-4 h-4 text-indigo-400" /> Training Workflow Pipeline Timeline
        </h3>
        <span className="text-xs font-mono text-slate-400">Automated Stage Progression</span>
      </div>

      <div className="overflow-x-auto pb-2">
        <div className="flex items-center min-w-[750px] justify-between">
          {STAGES.map((stage, idx) => {
            const isCompleted = idx < activeIdx || (status === 'COMPLETED' && idx <= activeIdx);
            const isCurrent = idx === activeIdx && status !== 'COMPLETED';
            const isFuture = idx > activeIdx;

            return (
              <React.Fragment key={stage.id}>
                {/* Node */}
                <div className="flex flex-col items-center gap-2 group relative">
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center border-2 transition-all duration-300 font-bold text-xs ${
                      isCompleted
                        ? 'bg-emerald-600/20 border-emerald-500 text-emerald-400 shadow-lg shadow-emerald-500/20'
                        : isCurrent
                        ? 'bg-blue-600/30 border-blue-400 text-blue-300 animate-pulse shadow-lg shadow-blue-500/30 ring-4 ring-blue-500/20'
                        : 'bg-slate-900 border-slate-800 text-slate-600'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircleIcon className="w-5 h-5" />
                    ) : isCurrent ? (
                      <div className="w-2.5 h-2.5 bg-blue-400 rounded-full animate-ping" />
                    ) : (
                      <span>{idx + 1}</span>
                    )}
                  </div>

                  <span
                    className={`text-[11px] font-mono whitespace-nowrap font-medium ${
                      isCompleted
                        ? 'text-emerald-400'
                        : isCurrent
                        ? 'text-blue-300 font-bold'
                        : 'text-slate-500'
                    }`}
                  >
                    {stage.label}
                  </span>
                </div>

                {/* Connector Line */}
                {idx < STAGES.length - 1 && (
                  <div
                    className={`flex-1 h-0.5 mx-2 rounded-full transition-colors duration-300 ${
                      idx < activeIdx ? 'bg-emerald-500' : 'bg-slate-800'
                    }`}
                  />
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};
