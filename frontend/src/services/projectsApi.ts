import api from './api';
import { Project, ProjectFormData } from '../types/project';

export const projectsApi = {
  getProjects: async (): Promise<Project[]> => {
    const res = await api.get<Project[]>('/projects');
    return res.data;
  },
  getProject: async (id: string): Promise<Project> => {
    const res = await api.get<Project>(`/projects/${id}`);
    return res.data;
  },
  createProject: async (data: ProjectFormData): Promise<Project> => {
    const res = await api.post<Project>('/projects', data);
    return res.data;
  },
  updateProject: async (id: string, data: Partial<ProjectFormData>): Promise<Project> => {
    const res = await api.put<Project>(`/projects/${id}`, data);
    return res.data;
  },
  deleteProject: async (id: string): Promise<void> => {
    await api.delete(`/projects/${id}`);
  },
};
