import React, { useState } from 'react';
import {
  BookmarkIcon,
  PlayIcon,
  TrashIcon,
  ArrowDownTrayIcon,
  SparklesIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  DocumentDuplicateIcon
} from '@heroicons/react/24/outline';

export const CheckpointManagerPage: React.FC = () => {
  const [checkpoints] = useState([
    {
      id: 'ckpt-1',
      filename: 'resnet50_epoch_10_best.pt',
      epoch: 10,
      step: 1000,
      loss: 0.2450,
      val_loss: 0.2810,
      accuracy: 0.9420,
      model_size_mb: 98.4,
      is_best: true,
      is_latest: false,
      created_at: '2026-07-30 14:45:00',
    },
    {
      id: 'ckpt-2',
      filename: 'resnet50_epoch_12_latest.pt',
      epoch: 12,
      step: 1200,
      loss: 0.2310,
      val_loss: 0.2980,
      accuracy: 0.9480,
      model_size_mb: 98.4,
      is_best: false,
      is_latest: true,
      created_at: '2026-07-30 15:02:12',
    },
  ]);

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <BookmarkIcon className="w-6 h-6 text-amber-400" />
            Checkpoint Manager & Model Weights Registry
          </h1>
          <p className="text-slate-400 text-xs mt-1">Automatic checkpoint discovery, pre-flight weight verification, resume training, and export.</p>
        </div>
      </div>

      {/* Checkpoints Grid / Table */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-white text-base">Discovered Model Checkpoints</h3>
          <span className="text-xs font-mono text-slate-400">{checkpoints.length} Checkpoints Available</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-slate-400 font-mono uppercase text-[10px]">
              <tr>
                <th className="p-3">Checkpoint Name</th>
                <th className="p-3">Epoch / Step</th>
                <th className="p-3">Loss (Train / Val)</th>
                <th className="p-3">Accuracy</th>
                <th className="p-3">Size</th>
                <th className="p-3">Status</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300 font-mono">
              {checkpoints.map((ckpt) => (
                <tr key={ckpt.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-white flex items-center gap-2">
                    <BookmarkIcon className="w-4 h-4 text-amber-400 shrink-0" />
                    {ckpt.filename}
                  </td>
                  <td className="p-3 text-slate-400">Epoch {ckpt.epoch} (Step {ckpt.step})</td>
                  <td className="p-3">
                    <span className="text-emerald-400">{ckpt.loss.toFixed(4)}</span> / <span className="text-amber-400">{ckpt.val_loss.toFixed(4)}</span>
                  </td>
                  <td className="p-3 text-emerald-400 font-bold">{(ckpt.accuracy * 100).toFixed(1)}%</td>
                  <td className="p-3 text-slate-400">{ckpt.model_size_mb} MB</td>
                  <td className="p-3">
                    {ckpt.is_best && (
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[10px] font-bold border border-emerald-500/30">
                        BEST MODEL
                      </span>
                    )}
                    {ckpt.is_latest && (
                      <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 text-[10px] font-bold border border-blue-500/30">
                        LATEST
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-right space-x-2">
                    <button className="px-3 py-1 rounded bg-blue-600 hover:bg-blue-500 text-white font-semibold text-[11px] inline-flex items-center gap-1">
                      <PlayIcon className="w-3.5 h-3.5" /> Resume Training
                    </button>
                    <button className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px]">
                      <ArrowDownTrayIcon className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
