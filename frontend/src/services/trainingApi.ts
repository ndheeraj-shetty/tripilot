import api from './api';

export interface StartTrainingPayload {
  project_id: string;
  session_name?: string;
  hyperparameters?: Record<string, any>;
  extra_args?: string[];
}

export const trainingApi = {
  start: async (payload: StartTrainingPayload) => {
    const res = await api.post('/training/start', payload);
    return res.data;
  },
  pause: async (sessionId: string) => {
    const res = await api.post('/training/pause', { session_id: sessionId });
    return res.data;
  },
  resume: async (sessionId: string) => {
    const res = await api.post('/training/resume', { session_id: sessionId });
    return res.data;
  },
  stop: async (sessionId: string) => {
    const res = await api.post('/training/stop', { session_id: sessionId });
    return res.data;
  },
  kill: async (sessionId: string) => {
    const res = await api.post('/training/kill', { session_id: sessionId });
    return res.data;
  },
  releaseGpu: async (sessionId: string) => {
    const res = await api.post('/training/release-gpu', { session_id: sessionId });
    return res.data;
  },
  cancelShutdown: async (sessionId: string) => {
    const res = await api.post('/training/cancel-shutdown', { session_id: sessionId });
    return res.data;
  },
  shutdownNow: async (sessionId: string) => {
    const res = await api.post('/training/shutdown-now', { session_id: sessionId });
    return res.data;
  },
  getShutdownStatus: async (sessionId?: string) => {
    const url = sessionId ? `/training/shutdown-status?session_id=${sessionId}` : '/training/shutdown-status';
    const res = await api.get(url);
    return res.data;
  },
  restart: async (sessionId: string) => {
    const res = await api.post('/training/restart', { session_id: sessionId });
    return res.data;
  },
  getStatus: async (sessionId: string) => {
    const res = await api.get(`/training/status?session_id=${sessionId}`);
    return res.data;
  },
  getLogs: async (sessionId: string, limit = 500) => {
    const res = await api.get(`/training/logs?session_id=${sessionId}&limit=${limit}`);
    return res.data;
  },
  getMetrics: async (sessionId: string, limit = 500) => {
    const res = await api.get(`/training/metrics?session_id=${sessionId}&limit=${limit}`);
    return res.data;
  },
  getSystemMetrics: async () => {
    const res = await api.get('/system/metrics');
    return res.data;
  },
};
