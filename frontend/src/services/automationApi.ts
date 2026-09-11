import api from './api';

export interface AutomationRulePayload {
  project_id?: string;
  name: string;
  trigger_event: string;
  conditions_json?: Record<string, any>;
  actions_sequence: Array<{ action_type: string; params: Record<string, any> }>;
  is_active?: boolean;
}

export const automationApi = {
  getRules: async (projectId?: string) => {
    const url = projectId ? `/automation/rules?project_id=${projectId}` : '/automation/rules';
    const res = await api.get(url);
    return res.data;
  },
  createRule: async (payload: AutomationRulePayload) => {
    const res = await api.post('/automation/rules', payload);
    return res.data;
  },
  updateRule: async (id: string, payload: Partial<AutomationRulePayload>) => {
    const res = await api.put(`/automation/rules/${id}`, payload);
    return res.data;
  },
  deleteRule: async (id: string) => {
    await api.delete(`/automation/rules/${id}`);
  },
  executeWorkflow: async (payload: { session_id: string; trigger_event: string; project_id: string; output_dir: string; checkpoint_dir: string }) => {
    const res = await api.post('/automation/execute', payload);
    return res.data;
  },
  cancelCountdown: async (sessionId: string) => {
    const res = await api.post('/automation/cancel', { session_id: sessionId });
    return res.data;
  },
  getHistory: async (sessionId?: string) => {
    const url = sessionId ? `/automation/history?session_id=${sessionId}` : '/automation/history';
    const res = await api.get(url);
    return res.data;
  },
  getStatus: async () => {
    const res = await api.get('/automation/status');
    return res.data;
  },
};
