import api from './api';
import { AppSettings } from '../types/project';

export const settingsApi = {
  getSettings: async (): Promise<AppSettings> => {
    const res = await api.get<AppSettings>('/settings');
    return res.data;
  },
  updateSettings: async (data: Partial<AppSettings>): Promise<AppSettings> => {
    const res = await api.put<AppSettings>('/settings', data);
    return res.data;
  },
};
