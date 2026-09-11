import { create } from 'zustand';
import { Project, TrainingSession, SystemTelemetry, Metric } from '../types';

interface AppState {
  projects: Project[];
  activeSession: TrainingSession | null;
  latestTelemetry: SystemTelemetry | null;
  metricsHistory: Metric[];
  setProjects: (projects: Project[]) => void;
  setActiveSession: (session: TrainingSession | null) => void;
  setLatestTelemetry: (telemetry: SystemTelemetry) => void;
  addMetric: (metric: Metric) => void;
}

export const useStore = create<AppState>((set) => ({
  projects: [],
  activeSession: null,
  latestTelemetry: null,
  metricsHistory: [
    { epoch: 1, step: 10, loss: 0.85, val_loss: 0.91, accuracy: 0.65, timestamp: new Date().toISOString() },
    { epoch: 2, step: 20, loss: 0.62, val_loss: 0.70, accuracy: 0.74, timestamp: new Date().toISOString() },
    { epoch: 3, step: 30, loss: 0.48, val_loss: 0.55, accuracy: 0.81, timestamp: new Date().toISOString() },
    { epoch: 4, step: 40, loss: 0.35, val_loss: 0.49, accuracy: 0.86, timestamp: new Date().toISOString() },
    { epoch: 5, step: 50, loss: 0.28, val_loss: 0.52, accuracy: 0.88, timestamp: new Date().toISOString() },
  ],
  setProjects: (projects) => set({ projects }),
  setActiveSession: (session) => set({ activeSession: session }),
  setLatestTelemetry: (telemetry) => set({ latestTelemetry: telemetry }),
  addMetric: (metric) => set((state) => ({ metricsHistory: [...state.metricsHistory, metric] })),
}));
