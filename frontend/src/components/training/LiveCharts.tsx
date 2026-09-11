import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';
import { MetricState, TelemetryState } from '../../hooks/useLiveTraining';

interface LiveChartsProps {
  metrics: MetricState[];
  telemetry: TelemetryState | null;
}

export const LiveCharts: React.FC<LiveChartsProps> = ({ metrics, telemetry }) => {
  // Mock data fallback if no live session metrics yet
  const chartMetrics = metrics.length > 0 ? metrics : [
    { epoch: 1, step: 10, loss: 1.15, val_loss: 1.22, accuracy: 0.52 },
    { epoch: 2, step: 20, loss: 0.92, val_loss: 0.98, accuracy: 0.65 },
    { epoch: 3, step: 30, loss: 0.74, val_loss: 0.81, accuracy: 0.74 },
    { epoch: 4, step: 40, loss: 0.58, val_loss: 0.65, accuracy: 0.82 },
    { epoch: 5, step: 50, loss: 0.42, val_loss: 0.51, accuracy: 0.88 },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Loss Convergence Chart */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-white text-sm">Training & Validation Loss Curve</h3>
          <span className="text-xs text-slate-400 font-mono">Live Loss Metrics</span>
        </div>
        <div className="h-60 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartMetrics} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="trainLossGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="valLossGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="step" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }} />
              <Area type="monotone" dataKey="loss" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#trainLossGrad)" name="Train Loss" />
              <Area type="monotone" dataKey="val_loss" stroke="#f43f5e" strokeWidth={2} fillOpacity={1} fill="url(#valLossGrad)" name="Val Loss" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Accuracy Curve Chart */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-white text-sm">Validation Accuracy Curve</h3>
          <span className="text-xs text-slate-400 font-mono">Live Accuracy Metrics</span>
        </div>
        <div className="h-60 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartMetrics} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="step" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} domain={[0, 1]} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }} />
              <Line type="monotone" dataKey="accuracy" stroke="#10b981" strokeWidth={2.5} dot={{ r: 3 }} name="Accuracy" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
