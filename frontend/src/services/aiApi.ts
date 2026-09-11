import api from './api';

export const aiApi = {
  getHealth: async (sessionId: string) => {
    const res = await api.get(`/ai/health?session_id=${sessionId}`);
    return res.data;
  },
  getPredictions: async (sessionId: string) => {
    const res = await api.get(`/ai/predictions?session_id=${sessionId}`);
    return res.data;
  },
  getRecommendations: async (sessionId: string) => {
    const res = await api.get(`/ai/recommendations?session_id=${sessionId}`);
    return res.data;
  },
  getDetections: async (sessionId: string) => {
    const res = await api.get(`/ai/detections?session_id=${sessionId}`);
    return res.data;
  },
  getHistory: async (sessionId: string, limit = 50) => {
    const res = await api.get(`/ai/history?session_id=${sessionId}&limit=${limit}`);
    return res.data;
  },
  getTrends: async (sessionId: string) => {
    const res = await api.get(`/ai/trends?session_id=${sessionId}`);
    return res.data;
  },
};
