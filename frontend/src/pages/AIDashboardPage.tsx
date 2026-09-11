import React, { useState } from 'react';
import {
  SparklesIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  ArrowTrendingUpIcon,
  LightBulbIcon,
  ClockIcon,
  CpuChipIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

export const AIDashboardPage: React.FC = () => {
  // Phase 3 AI State Mock / Integration
  const [healthScore] = useState({
    score: 94,
    category: 'EXCELLENT',
    subScores: {
      loss_health: 96,
      hardware_health: 98,
      stability_health: 92,
      fail_prob_pct: 4,
    },
  });

  const [detections] = useState([
    {
      type: 'OVERFITTING_WARNING',
      severity: 'WARNING',
      confidence: 0.78,
      reason: 'Validation loss diverged by +0.024 over last 3 epochs while training loss decreased.',
      timestamp: '2 mins ago',
    },
    {
      type: 'GPU_EFFICIENCY',
      severity: 'INFO',
      confidence: 0.88,
      reason: 'GPU VRAM utilization is at 59% (14.2 GB / 24.0 GB).',
      timestamp: '5 mins ago',
    },
  ]);

  const [predictions] = useState({
    remainingTime: '~ 24 minutes',
    failureProb: '4%',
    expectedCompletion: '15:28:45',
    memoryGrowth: 'STABLE',
    speedTrend: 'STABLE (4.2 steps/sec)',
    accuracyTrend: 'RISING (+0.022/epoch)',
    lossTrend: 'DECREASING (-0.035/epoch)',
  });

  const [recommendations] = useState([
    {
      title: 'Enable Automatic Mixed Precision (AMP FP16)',
      description: 'System detects available Tensor Cores on RTX 4090. Enable `torch.cuda.amp.autocast()` to double throughput.',
      priority: 'MEDIUM',
      category: 'OPTIMIZATION',
      reason: 'GPU memory bandwidth is available.',
      confidence: '92%',
      expectedImpact: '+120% training speedup',
    },
    {
      title: 'Reduce Learning Rate by 50% at Epoch 10',
      description: 'Validation loss divergence indicates slight overfitting. Decay learning rate from 0.001 to 0.0005.',
      priority: 'HIGH',
      category: 'HYPERPARAMETER',
      reason: 'Loss divergence slope is positive.',
      confidence: '85%',
      expectedImpact: 'Stabilizes validation loss decay',
    },
  ]);

  const [decisionHistory] = useState([
    {
      epoch: 5,
      step: 50,
      score: 94,
      summary: 'Epoch 5 Step 50: Health Score 94/100 (EXCELLENT). 2 anomalies detected.',
      timestamp: '15:02:12',
    },
    {
      epoch: 4,
      step: 40,
      score: 96,
      summary: 'Epoch 4 Step 40: Health Score 96/100 (EXCELLENT). 0 critical anomalies.',
      timestamp: '14:58:30',
    },
    {
      epoch: 3,
      step: 30,
      score: 98,
      summary: 'Epoch 3 Step 30: Health Score 98/100 (EXCELLENT). Training appears healthy.',
      timestamp: '14:55:00',
    },
  ]);

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <SparklesIcon className="w-6 h-6 text-amber-400" />
            AI Decision & Diagnostics Hub
          </h1>
          <p className="text-slate-400 text-xs mt-1">Continuous training health scoring, failure prediction, and hyperparameter advice.</p>
        </div>
        <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono font-medium flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
          AI Decision Engine Active
        </span>
      </div>

      {/* Top Overview Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Health Score Gauge */}
        <div className="glass-panel p-6 rounded-2xl space-y-4 border border-emerald-500/30 bg-emerald-950/10">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold uppercase tracking-wider">Training Health Score</span>
            <ShieldCheckIcon className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="flex items-baseline justify-between">
            <span className="text-4xl font-extrabold text-white">{healthScore.score}</span>
            <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 font-semibold text-xs font-mono">
              {healthScore.category}
            </span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${healthScore.score}%` }}></div>
          </div>
          <div className="grid grid-cols-3 gap-2 text-[11px] font-mono text-slate-400 pt-2 border-t border-slate-800">
            <div>Loss: <span className="text-white">{healthScore.subScores.loss_health}%</span></div>
            <div>HW: <span className="text-white">{healthScore.subScores.hardware_health}%</span></div>
            <div>Stability: <span className="text-white">{healthScore.subScores.stability_health}%</span></div>
          </div>
        </div>

        {/* Predictive Analytics */}
        <div className="glass-panel p-6 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold uppercase tracking-wider">Predictive Insights</span>
            <ClockIcon className="w-5 h-5 text-blue-400" />
          </div>
          <div className="space-y-2 text-xs font-mono">
            <div className="flex justify-between border-b border-slate-800 pb-1.5">
              <span className="text-slate-400">Est. Remaining Time:</span>
              <span className="text-white font-semibold">{predictions.remainingTime}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-1.5">
              <span className="text-slate-400">Failure Probability:</span>
              <span className="text-emerald-400 font-semibold">{predictions.failureProb}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-1.5">
              <span className="text-slate-400">VRAM Growth Trend:</span>
              <span className="text-blue-400 font-semibold">{predictions.memoryGrowth}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Accuracy Trend:</span>
              <span className="text-emerald-400 font-semibold">{predictions.accuracyTrend}</span>
            </div>
          </div>
        </div>

        {/* System & Loss Trends */}
        <div className="glass-panel p-6 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold uppercase tracking-wider">Trend Direction</span>
            <ArrowTrendingUpIcon className="w-5 h-5 text-purple-400" />
          </div>
          <div className="space-y-2 text-xs font-mono">
            <div className="flex justify-between border-b border-slate-800 pb-1.5">
              <span className="text-slate-400">Loss Curve Trend:</span>
              <span className="text-emerald-400 font-semibold">{predictions.lossTrend}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-1.5">
              <span className="text-slate-400">Training Speed:</span>
              <span className="text-white font-semibold">{predictions.speedTrend}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Expected Completion:</span>
              <span className="text-slate-300 font-semibold">{predictions.expectedCompletion}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Detections & Recommendations Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Detections */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-amber-400">
            <ExclamationTriangleIcon className="w-5 h-5" />
            <h3 className="font-bold text-white text-sm">Detected Anomalies & Flags</h3>
          </div>
          <div className="space-y-3">
            {detections.map((det, i) => (
              <div
                key={i}
                className={`p-4 rounded-xl text-xs space-y-1 border ${
                  det.severity === 'CRITICAL'
                    ? 'bg-rose-950/30 border-rose-500/30 text-rose-200'
                    : det.severity === 'WARNING'
                    ? 'bg-amber-950/30 border-amber-500/30 text-amber-200'
                    : 'bg-blue-950/30 border-blue-500/30 text-blue-200'
                }`}
              >
                <div className="flex items-center justify-between font-semibold">
                  <span className="font-mono">{det.type}</span>
                  <span className="px-2 py-0.5 rounded bg-slate-900 text-[10px] font-mono">{det.severity}</span>
                </div>
                <p className="text-slate-300">{det.reason}</p>
                <div className="text-[10px] text-slate-500 pt-1 font-mono">Confidence: {(det.confidence * 100).toFixed(0)}% | {det.timestamp}</div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Recommendations */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-2 text-blue-400">
            <LightBulbIcon className="w-5 h-5" />
            <h3 className="font-bold text-white text-sm">Actionable AI Advice</h3>
          </div>
          <div className="space-y-3">
            {recommendations.map((rec, i) => (
              <div key={i} className="p-4 bg-slate-900/60 rounded-xl space-y-2 text-xs border border-slate-800">
                <div className="flex items-center justify-between">
                  <h4 className="font-bold text-white flex items-center gap-2">
                    <CheckCircleIcon className="w-4 h-4 text-emerald-400" />
                    {rec.title}
                  </h4>
                  <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 text-[10px] font-mono font-semibold">
                    {rec.priority}
                  </span>
                </div>
                <p className="text-slate-300">{rec.description}</p>
                <div className="pt-2 border-t border-slate-800 flex justify-between text-[11px] text-slate-400 font-mono">
                  <span>Impact: <strong className="text-emerald-400">{rec.expectedImpact}</strong></span>
                  <span>Confidence: <strong className="text-white">{rec.confidence}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Decision Timeline */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-sm flex items-center gap-2">
          <CpuChipIcon className="w-5 h-5 text-purple-400" />
          AI Evaluation Decision Timeline
        </h3>
        <div className="space-y-3 text-xs font-mono">
          {decisionHistory.map((item, i) => (
            <div key={i} className="p-3 bg-slate-900/60 rounded-xl flex items-center justify-between border border-slate-800">
              <div className="flex items-center gap-3">
                <span className="px-2.5 py-1 rounded bg-slate-800 text-blue-400 font-bold">
                  Epoch {item.epoch} / Step {item.step}
                </span>
                <span className="text-slate-300">{item.summary}</span>
              </div>
              <span className="text-slate-500 text-[11px]">{item.timestamp}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
