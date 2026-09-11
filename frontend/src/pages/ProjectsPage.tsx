import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  PlusIcon,
  FolderIcon,
  PencilSquareIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { useProjects } from '../hooks/useProjects';
import { projectSchema, ProjectFormData, Project } from '../types/project';
import { useToast } from '../components/common/Toast';

export const ProjectsPage: React.FC = () => {
  const { projects, isLoading, isError, createProject, updateProject, deleteProject } = useProjects();
  const { showToast } = useToast();

  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      framework: 'PyTorch',
      automation_enabled: true,
      output_dir: './storage/outputs',
      checkpoint_dir: './storage/checkpoints',
    },
  });

  const openCreateModal = () => {
    setEditingProject(null);
    reset({
      name: '',
      description: '',
      framework: 'PyTorch',
      model_name: '',
      dataset_path: '',
      training_script_path: '',
      output_dir: './storage/outputs',
      checkpoint_dir: './storage/checkpoints',
      automation_enabled: true,
    });
    setIsModalOpen(true);
  };

  const openEditModal = (proj: Project) => {
    setEditingProject(proj);
    reset({
      name: proj.name,
      description: proj.description || '',
      framework: proj.framework,
      model_name: proj.model_name,
      dataset_path: proj.dataset_path,
      training_script_path: proj.training_script_path,
      output_dir: proj.output_dir,
      checkpoint_dir: proj.checkpoint_dir,
      automation_enabled: proj.automation_enabled,
    });
    setIsModalOpen(true);
  };

  const onSubmit = async (data: ProjectFormData) => {
    try {
      if (editingProject) {
        await updateProject({ id: editingProject.id, data });
        showToast('Project Updated', `Project "${data.name}" updated successfully.`, 'success');
      } else {
        await createProject(data);
        showToast('Project Created', `Project "${data.name}" created successfully.`, 'success');
      }
      setIsModalOpen(false);
    } catch (err: any) {
      showToast('Action Failed', err.message, 'error');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteProject(id);
      showToast('Project Deleted', 'Project has been removed from database.', 'info');
      setDeletingId(null);
    } catch (err: any) {
      showToast('Delete Failed', err.message, 'error');
    }
  };

  const filteredProjects = projects.filter(
    (p) =>
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.framework.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.model_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header & Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Project Registry</h1>
          <p className="text-slate-400 text-xs mt-1">Configure ML models, scripts, dataset locations, and output targets.</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <MagnifyingGlassIcon className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 w-64"
            />
          </div>
          <button
            onClick={openCreateModal}
            className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center gap-2 transition shadow-lg shadow-blue-500/20"
          >
            <PlusIcon className="w-4 h-4" /> Add Project
          </button>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="p-12 text-center text-slate-400 font-mono text-xs">
          Loading projects from database...
        </div>
      )}

      {/* Error State */}
      {isError && (
        <div className="p-6 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-3">
          <ExclamationTriangleIcon className="w-5 h-5 shrink-0" />
          <span>Failed to load projects from PostgreSQL backend. Ensure FastAPI server is running.</span>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !isError && filteredProjects.length === 0 && (
        <div className="glass-panel p-12 text-center rounded-2xl space-y-3">
          <FolderIcon className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-300">No Projects Found</h3>
          <p className="text-xs text-slate-500">Create your first ML training project to get started.</p>
          <button
            onClick={openCreateModal}
            className="px-4 py-2 rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30 text-xs font-semibold"
          >
            Create Project
          </button>
        </div>
      )}

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredProjects.map((proj) => (
          <div key={proj.id} className="glass-panel p-6 rounded-2xl space-y-4 hover:border-slate-700 transition">
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <FolderIcon className="w-5 h-5 text-blue-400" />
                  <h3 className="text-lg font-bold text-white">{proj.name}</h3>
                </div>
                <p className="text-xs text-slate-400">{proj.description || 'No description provided.'}</p>
              </div>
              <span className="px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-blue-400 text-xs font-mono font-medium">
                {proj.framework}
              </span>
            </div>

            <div className="p-3.5 bg-slate-900/60 rounded-xl space-y-1.5 text-xs font-mono text-slate-300">
              <div><span className="text-slate-500">Model:</span> {proj.model_name}</div>
              <div><span className="text-slate-500">Script:</span> {proj.training_script_path}</div>
              <div><span className="text-slate-500">Dataset:</span> {proj.dataset_path}</div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-800/60">
              <span className="text-[11px] text-slate-500 font-mono">
                Automation: {proj.automation_enabled ? 'Enabled' : 'Disabled'}
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => openEditModal(proj)}
                  className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                  title="Edit Project"
                >
                  <PencilSquareIcon className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setDeletingId(proj.id)}
                  className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition"
                  title="Delete Project"
                >
                  <TrashIcon className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add / Edit Project Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel w-full max-w-xl p-6 rounded-2xl space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-white">
                {editingProject ? 'Edit Project' : 'Create New ML Project'}
              </h2>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-white">
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Project Name</label>
                <input
                  {...register('name')}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
                  placeholder="e.g. ResNet50 Classifier"
                />
                {errors.name && <p className="text-rose-400 text-[11px] mt-1">{errors.name.message}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-slate-400 mb-1">Framework</label>
                  <select
                    {...register('framework')}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="PyTorch">PyTorch</option>
                    <option value="TensorFlow">TensorFlow</option>
                    <option value="Ultralytics YOLO">Ultralytics YOLO</option>
                  </select>
                  {errors.framework && <p className="text-rose-400 text-[11px] mt-1">{errors.framework.message}</p>}
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Model Name</label>
                  <input
                    {...register('model_name')}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
                    placeholder="e.g. resnet50"
                  />
                  {errors.model_name && <p className="text-rose-400 text-[11px] mt-1">{errors.model_name.message}</p>}
                </div>
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Description (Optional)</label>
                <textarea
                  {...register('description')}
                  rows={2}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
                  placeholder="Describe your model training objective..."
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-slate-400">Python Training Script Path</label>
                  <span className="text-[10px] text-blue-400">Accepts any local Windows path on your laptop</span>
                </div>
                <input
                  {...register('training_script_path')}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
                  placeholder="C:/Users/ndhee/my_project/train.py or ./scripts/sample_training.py"
                />
                {errors.training_script_path && (
                  <p className="text-rose-400 text-[11px] mt-1">{errors.training_script_path.message}</p>
                )}
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-slate-400">Dataset Location Path</label>
                  <span className="text-[10px] text-slate-500">Folder or file on laptop storage</span>
                </div>
                <input
                  {...register('dataset_path')}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
                  placeholder="C:/Users/ndhee/datasets/imagenet or ./storage/datasets"
                />
                {errors.dataset_path && <p className="text-rose-400 text-[11px] mt-1">{errors.dataset_path.message}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-slate-400 mb-1">Output Folder</label>
                  <input
                    {...register('output_dir')}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
                    placeholder="C:/Users/ndhee/outputs or ./storage/outputs"
                  />
                  {errors.output_dir && <p className="text-rose-400 text-[11px] mt-1">{errors.output_dir.message}</p>}
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Checkpoint Folder</label>
                  <input
                    {...register('checkpoint_dir')}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
                    placeholder="C:/Users/ndhee/checkpoints or ./storage/checkpoints"
                  />
                  {errors.checkpoint_dir && (
                    <p className="text-rose-400 text-[11px] mt-1">{errors.checkpoint_dir.message}</p>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold shadow-lg shadow-blue-500/20"
                >
                  {isSubmitting ? 'Saving...' : editingProject ? 'Update Project' : 'Create Project'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deletingId && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel w-full max-w-md p-6 rounded-2xl space-y-4">
            <h3 className="text-lg font-bold text-white">Delete Project Confirmation</h3>
            <p className="text-xs text-slate-400">
              Are you sure you want to delete this project? This will remove its project record from the database.
            </p>
            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setDeletingId(null)}
                className="px-4 py-2 rounded-xl text-slate-400 hover:text-white text-xs"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDelete(deletingId)}
                className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold"
              >
                Confirm Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
