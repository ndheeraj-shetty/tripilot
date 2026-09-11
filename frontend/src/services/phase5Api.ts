import api from './api';

export const phase5Api = {
  // Checkpoints
  getCheckpoints: async (sessionId?: string, checkpointDir?: string) => {
    let url = '/checkpoints';
    if (sessionId && checkpointDir) {
      url += `?session_id=${sessionId}&checkpoint_dir=${encodeURIComponent(checkpointDir)}`;
    } else if (sessionId) {
      url += `?session_id=${sessionId}`;
    }
    const res = await api.get(url);
    return res.data;
  },
  resumeCheckpoint: async (sessionId: string, checkpointPath: string) => {
    const res = await api.post('/checkpoints/resume', { session_id: sessionId, checkpoint_path: checkpointPath });
    return res.data;
  },
  deleteCheckpoint: async (checkpointId: string) => {
    await api.delete(`/checkpoints/${checkpointId}`);
  },

  // Experiments
  getExperiments: async (projectId?: string) => {
    const url = projectId ? `/experiments?project_id=${projectId}` : '/experiments';
    const res = await api.get(url);
    return res.data;
  },
  createExperiment: async (payload: any) => {
    const res = await api.post('/experiments', payload);
    return res.data;
  },

  // Analytics & Comparison
  getAnalytics: async (sessionId: string) => {
    const res = await api.get(`/analytics?session_id=${sessionId}`);
    return res.data;
  },
  compareSessions: async (sessionAId: string, sessionBId: string) => {
    const res = await api.post('/compare', { session_a_id: sessionAId, session_b_id: sessionBId });
    return res.data;
  },

  // Reports
  generateReport: async (sessionId: string, reportType = 'PDF') => {
    const res = await api.post('/reports/generate', { session_id: sessionId, report_type: reportType });
    return res.data;
  },

  // Exports
  createExportBundle: async (sessionId: string) => {
    const res = await api.post('/exports', { session_id: sessionId });
    return res.data;
  },
};
