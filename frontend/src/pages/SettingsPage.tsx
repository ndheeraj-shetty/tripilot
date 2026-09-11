import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { CogIcon, ServerIcon, FolderIcon, SwatchIcon } from '@heroicons/react/24/outline';
import { useSettings } from '../hooks/useSettings';
import { useToast } from '../components/common/Toast';

const settingsSchema = z.object({
  theme: z.string(),
  app_env: z.string(),
  default_output_folder: z.string().min(1, 'Default output folder is required'),
  default_checkpoint_folder: z.string().min(1, 'Default checkpoint folder is required'),
  postgres_server: z.string().min(1, 'PostgreSQL server host is required'),
  postgres_port: z.string().min(1, 'PostgreSQL port is required'),
  postgres_db: z.string().min(1, 'PostgreSQL database name is required'),
});

type SettingsFormData = z.infer<typeof settingsSchema>;

export const SettingsPage: React.FC = () => {
  const { settings, isLoading, updateSettings } = useSettings();
  const { showToast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<SettingsFormData>({
    resolver: zodResolver(settingsSchema),
  });

  useEffect(() => {
    if (settings) {
      reset({
        theme: settings.theme || 'dark',
        app_env: settings.app_env || 'development',
        default_output_folder: settings.default_output_folder || './storage/outputs',
        default_checkpoint_folder: settings.default_checkpoint_folder || './storage/checkpoints',
        postgres_server: settings.postgres_server || 'localhost',
        postgres_port: settings.postgres_port || '5432',
        postgres_db: settings.postgres_db || 'trainpilot_db',
      });
    }
  }, [settings, reset]);

  const onSubmit = async (data: SettingsFormData) => {
    try {
      await updateSettings(data);
      showToast('Settings Saved', 'System configurations updated successfully.', 'success');
    } catch (err: any) {
      showToast('Save Failed', err.message, 'error');
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center text-slate-400 font-mono text-xs">Loading application settings...</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">System Settings</h1>
        <p className="text-slate-400 text-xs mt-1">Configure global application defaults, database connection, and theme settings.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Application Defaults */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-blue-400 font-semibold text-sm">
            <FolderIcon className="w-5 h-5" />
            <span>Default Application Folders</span>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Default Output Directory</label>
              <input
                {...register('default_output_folder')}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
              />
              {errors.default_output_folder && (
                <p className="text-rose-400 text-[11px] mt-1">{errors.default_output_folder.message}</p>
              )}
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Default Checkpoint Directory</label>
              <input
                {...register('default_checkpoint_folder')}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
              />
              {errors.default_checkpoint_folder && (
                <p className="text-rose-400 text-[11px] mt-1">{errors.default_checkpoint_folder.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Database Configuration */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-purple-400 font-semibold text-sm">
            <ServerIcon className="w-5 h-5" />
            <span>PostgreSQL Database Connection</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Database Host</label>
              <input
                {...register('postgres_server')}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Database Port</label>
              <input
                {...register('postgres_port')}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Database Name</label>
              <input
                {...register('postgres_db')}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Theme Settings */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
            <SwatchIcon className="w-5 h-5" />
            <span>User Interface & Theme</span>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Theme</label>
              <select
                {...register('theme')}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
              >
                <option value="dark">Dark Mode (Default)</option>
                <option value="system">System Preference</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Application Environment</label>
              <input
                {...register('app_env')}
                readOnly
                className="w-full bg-slate-900/60 border border-slate-800 rounded-xl px-3.5 py-2.5 text-slate-400 font-mono"
              />
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-lg shadow-blue-500/20 transition"
          >
            {isSubmitting ? 'Saving Settings...' : 'Save Settings'}
          </button>
        </div>
      </form>
    </div>
  );
};
