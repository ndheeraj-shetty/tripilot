import React, { useState } from 'react';
import {
  ClockIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  CurrencyDollarIcon,
  CheckCircleIcon,
  XCircleIcon,
  SparklesIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';

interface RunHistoryItem {
  id: string;
  projectName: string;
  modelName: string;
  dataset: string;
  startTime: string;
  endTime: string;
  duration: string;
  accuracy: string;
  finalLoss: string;
  gpuTime: string;
  estimatedCost: string;
  moneySaved: string;
  status: 'COMPLETED' | 'FAILED' | 'CANCELLED';
}

const SAMPLE_HISTORY: RunHistoryItem[] = [
  {
    id: 'run-001',
    projectName: 'ResNet50 Fine-Tuning',
    modelName: 'resnet50_v2',
    dataset: 'ImageNet-Sub50k',
    startTime: '2026-07-31 14:10:00',
    endTime: '2026-07-31 14:45:20',
    duration: '35m 20s',
    accuracy: '94.2%',
    finalLoss: '0.1824',
    gpuTime: '0.59 hrs',
    estimatedCost: '$3.75',
    moneySaved: '$2.28',
    status: 'COMPLETED',
  },
  {
    id: 'run-002',
    projectName: 'YOLOv8 Object Detection',
    modelName: 'yolov8x',
    dataset: 'COCO-Val2017',
    startTime: '2026-07-31 11:00:00',
    endTime: '2026-07-31 12:15:00',
    duration: '1h 15m',
    accuracy: '88.6%',
    finalLoss: '0.2450',
    gpuTime: '1.25 hrs',
    estimatedCost: '$6.50',
    moneySaved: '$3.38',
    status: 'COMPLETED',
  },
  {
    id: 'run-003',
    projectName: 'BERT Transformer Classifier',
    modelName: 'bert-base-uncased',
    dataset: 'SQuAD-v2.0',
    startTime: '2026-07-30 18:00:00',
    endTime: '2026-07-30 18:22:10',
    duration: '22m 10s',
    accuracy: '91.4%',
    finalLoss: '0.2105',
    gpuTime: '0.37 hrs',
    estimatedCost: '$2.10',
    moneySaved: '$1.18',
    status: 'COMPLETED',
  },
  {
    id: 'run-004',
    projectName: 'Diffusion Model Generator',
    modelName: 'stable-diffusion-xl',
    dataset: 'LAION-5B-Subset',
    startTime: '2026-07-30 15:30:00',
    endTime: '2026-07-30 15:42:00',
    duration: '12m 00s',
    accuracy: 'N/A',
    finalLoss: '0.4120',
    gpuTime: '0.20 hrs',
    estimatedCost: '$1.25',
    moneySaved: '$0.00',
    status: 'CANCELLED',
  },
];

export const HistoryPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const filteredHistory = SAMPLE_HISTORY.filter((item) => {
    const matchesSearch =
      item.projectName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.modelName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.dataset.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'ALL' || item.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <ClockIcon className="w-6 h-6 text-blue-400" /> Training History & Cost Archive
        </h1>
        <p className="text-slate-400 text-xs mt-1">
          Historical record of completed AI model training runs, hardware metrics, and cloud cost savings.
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-panel p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-slate-800">
        <div className="relative w-full md:w-80">
          <MagnifyingGlassIcon className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search by project, model, or dataset..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono"
          />
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <FunnelIcon className="w-4 h-4 text-slate-500" /> Filter Status:
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
          >
            <option value="ALL">All Statuses</option>
            <option value="COMPLETED">Completed Only</option>
            <option value="CANCELLED">Cancelled Only</option>
            <option value="FAILED">Failed Only</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 shadow-xl overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead className="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider">
            <tr>
              <th className="p-3">Project / Model</th>
              <th className="p-3">Dataset</th>
              <th className="p-3">Start / End Time</th>
              <th className="p-3">Duration</th>
              <th className="p-3">Accuracy / Loss</th>
              <th className="p-3">GPU Time</th>
              <th className="p-3">Cost Saved</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {filteredHistory.length === 0 ? (
              <tr>
                <td colSpan={8} className="p-8 text-center text-slate-500 italic">
                  No training history records match your search criteria.
                </td>
              </tr>
            ) : (
              filteredHistory.map((run) => (
                <tr key={run.id} className="hover:bg-slate-900/40 transition">
                  <td className="p-3">
                    <div className="font-bold text-white text-xs">{run.projectName}</div>
                    <div className="text-[11px] text-blue-400">{run.modelName}</div>
                  </td>
                  <td className="p-3 text-slate-400">{run.dataset}</td>
                  <td className="p-3 text-[11px]">
                    <div>{run.startTime}</div>
                    <div className="text-slate-500">{run.endTime}</div>
                  </td>
                  <td className="p-3 font-semibold text-slate-200">{run.duration}</td>
                  <td className="p-3">
                    <div className="text-emerald-400 font-bold">{run.accuracy}</div>
                    <div className="text-slate-500 text-[10px]">Loss: {run.finalLoss}</div>
                  </td>
                  <td className="p-3 text-purple-300">{run.gpuTime}</td>
                  <td className="p-3">
                    <div className="text-emerald-400 font-bold">{run.moneySaved}</div>
                    <div className="text-slate-500 text-[10px]">Cost: {run.estimatedCost}</div>
                  </td>
                  <td className="p-3">
                    <span
                      className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                        run.status === 'COMPLETED'
                          ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                          : run.status === 'CANCELLED'
                          ? 'bg-amber-500/20 text-amber-300 border-amber-500/30'
                          : 'bg-rose-500/20 text-rose-400 border-rose-500/30'
                      }`}
                    >
                      {run.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
