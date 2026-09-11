import React, { useState } from 'react';
import { CpuChipIcon, LockClosedIcon, EnvelopeIcon } from '@heroicons/react/24/outline';
import { authApi } from '../services/authApi';
import { useToast } from '../components/common/Toast';

export const LoginPage: React.FC<{ onLoginSuccess: () => void }> = ({ onLoginSuccess }) => {
  const { showToast } = useToast();
  const [email, setEmail] = useState('admin@zombierun.ai');
  const [password, setPassword] = useState('admin123');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authApi.login(email, password);
      showToast('Authentication Successful', `Welcome back to Zombie Run Cost Killer!`, 'success');
      onLoginSuccess();
    } catch (err: any) {
      showToast('Login Failed', err.response?.data?.detail || 'Invalid email or password.', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="glass-panel w-full max-w-md p-8 rounded-3xl space-y-6 border border-slate-800 shadow-2xl">
        <div className="text-center space-y-2">
          <div className="p-3 bg-gradient-to-tr from-blue-600 to-indigo-500 rounded-2xl w-14 h-14 mx-auto flex items-center justify-center shadow-lg shadow-blue-500/20 text-white">
            <CpuChipIcon className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Zombie Run Cost Killer</h1>
          <p className="text-xs text-slate-400">AI-Powered ML Training Cost Optimization & Automation Platform</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div className="space-y-1">
            <label className="text-slate-300 font-semibold">Email Address</label>
            <div className="relative">
              <EnvelopeIcon className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-slate-300 font-semibold">Password</label>
            <div className="relative">
              <LockClosedIcon className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-3 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-2"
          >
            {loading ? 'Authenticating...' : 'Sign In to Zombie Run Cost Killer'}
          </button>
        </form>
      </div>
    </div>
  );
};
