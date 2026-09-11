import React, { useState } from 'react';
import { ScaleIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

export const ModelComparisonPage: React.FC = () => {
  const [comparison] = useState({
    session_a: {
      name: 'ResNet50 Baseline (LR 0.001)',
      final_loss: 0.2850,
      best_val_loss: 0.3120,
      best_accuracy: '92.4%',
      avg_gpu_pct: '84.5%',
      avg_vram_mb: '14,200 MB',
      training_duration: '24m 30s',
      speed: '4.2 steps/sec'
    },
    session_b: {
      name: 'ResNet50 + AMP FP16 + Cosine Decay (LR 0.0005)',
      final_loss: 0.2140,
      best_val_loss: 0.2410,
      best_accuracy: '95.8%',
      avg_gpu_pct: '94.2%',
      avg_vram_mb: '8,400 MB',
      training_duration: '11m 15s',
      speed: '9.1 steps/sec'
    },
    deltas: {
      loss_improvement: '-0.0710 (24.9% better)',
      val_loss_improvement: '-0.0710 (22.7% better)',
      accuracy_gain: '+3.4%',
      speedup: '2.16x faster training throughput',
      vram_saving: '-5,800 MB (40.8% VRAM reduction)'
    }
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <ScaleIcon className="w-6 h-6 text-purple-400" />
          Model & Experiment Comparison Engine
        </h1>
        <p className="text-slate-400 text-xs mt-1">Side-by-side metric deltas, hardware utilization efficiency, and speedup comparison.</p>
      </div>

      {/* Comparison Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Session A Card */}
        <div className="glass-panel p-6 rounded-2xl space-y-4 border border-slate-800">
          <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 text-[10px] font-mono font-bold uppercase">Training Run A</span>
          <h3 className="text-base font-bold text-white">{comparison.session_a.name}</h3>
          <div className="space-y-2 text-xs font-mono pt-2 border-t border-slate-800">
            <div className="flex justify-between"><span className="text-slate-400">Final Train Loss:</span><span className="text-white">{comparison.session_a.final_loss}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Best Validation Loss:</span><span className="text-white">{comparison.session_a.best_val_loss}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Best Accuracy:</span><span className="text-emerald-400 font-bold">{comparison.session_a.best_accuracy}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">GPU Utilization:</span><span className="text-white">{comparison.session_a.avg_gpu_pct}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">VRAM Usage:</span><span className="text-white">{comparison.session_a.avg_vram_mb}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Training Speed:</span><span className="text-white">{comparison.session_a.speed}</span></div>
          </div>
        </div>

        {/* Session B Card */}
        <div className="glass-panel p-6 rounded-2xl space-y-4 border-2 border-emerald-500/40 bg-emerald-950/10">
          <div className="flex justify-between items-center">
            <span className="px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 text-[10px] font-mono font-bold uppercase">Training Run B (Winner)</span>
            <CheckCircleIcon className="w-5 h-5 text-emerald-400" />
          </div>
          <h3 className="text-base font-bold text-white">{comparison.session_b.name}</h3>
          <div className="space-y-2 text-xs font-mono pt-2 border-t border-slate-800">
            <div className="flex justify-between"><span className="text-slate-400">Final Train Loss:</span><span className="text-emerald-400 font-bold">{comparison.session_b.final_loss}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Best Validation Loss:</span><span className="text-emerald-400 font-bold">{comparison.session_b.best_val_loss}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Best Accuracy:</span><span className="text-emerald-400 font-bold">{comparison.session_b.best_accuracy}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">GPU Utilization:</span><span className="text-white">{comparison.session_b.avg_gpu_pct}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">VRAM Usage:</span><span className="text-emerald-400 font-bold">{comparison.session_b.avg_vram_mb}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Training Speed:</span><span className="text-emerald-400 font-bold">{comparison.session_b.speed}</span></div>
          </div>
        </div>
      </div>

      {/* Metric Deltas Box */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base">Delta Analysis Summary</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-4 bg-slate-900/60 rounded-xl space-y-1 border border-slate-800">
            <span className="text-slate-400">Accuracy Gain</span>
            <div className="text-lg font-bold text-emerald-400">{comparison.deltas.accuracy_gain}</div>
          </div>
          <div className="p-4 bg-slate-900/60 rounded-xl space-y-1 border border-slate-800">
            <span className="text-slate-400">Validation Loss Improvement</span>
            <div className="text-lg font-bold text-emerald-400">{comparison.deltas.val_loss_improvement}</div>
          </div>
          <div className="p-4 bg-slate-900/60 rounded-xl space-y-1 border border-slate-800">
            <span className="text-slate-400">Training Speedup</span>
            <div className="text-lg font-bold text-blue-400">{comparison.deltas.speedup}</div>
          </div>
          <div className="p-4 bg-slate-900/60 rounded-xl space-y-1 border border-slate-800">
            <span className="text-slate-400">VRAM Footprint</span>
            <div className="text-lg font-bold text-emerald-400">{comparison.deltas.vram_saving}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
