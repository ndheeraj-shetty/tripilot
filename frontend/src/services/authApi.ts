import api from './api';

export const authApi = {
  login: async (email: string, password: string) => {
    const res = await api.post('/auth/login', { email, password });
    if (res.data.access_token) {
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user_email', res.data.user_email);
      localStorage.setItem('role', res.data.role);
    }
    return res.data;
  },
  logout: async () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('role');
    await api.post('/auth/logout');
  },
  getSystemStatus: async () => {
    const res = await api.get('/admin/system');
    return res.data;
  },
  createBackup: async () => {
    const res = await api.post('/backup');
    return res.data;
  },
  getUsers: async () => {
    const res = await api.get('/users');
    return res.data;
  },
};
