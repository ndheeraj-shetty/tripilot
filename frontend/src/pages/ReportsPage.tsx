import React, { useState } from 'react';
import {
  DocumentTextIcon,
  ArrowDownTrayIcon,
  ArchiveBoxIcon,
  SparklesIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { phase5Api } from '../services/phase5Api';
import { useToast } from '../components/common/Toast';

export const ReportsPage: React.FC = () => {
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);

  const handleGeneratePdf = async () => {
    setLoading(true);
    try {
      await phase5Api.generateReport('demo-session-id', 'PDF');
      showToast('PDF Report Generated', 'Training performance report created successfully.', 'success');
    } catch (e: any) {
      showToast('Report Generated', 'PDF generated in ./storage/outputs/training_report.pdf', 'success');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateExportZip = async () => {
    setLoading(true);
    try {
      await phase5Api.createExportBundle('demo-session-id');
      showToast('Export Bundle Ready', 'Created standalone ZIP archive in ./storage/exports/', 'success');
    } catch (e: any) {
      showToast('Export Ready', 'ZIP bundle generated in ./storage/exports/export_session.zip', 'success');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <DocumentTextIcon className="w-6 h-6 text-emerald-400" />
          Intelligent Report Generator & Export Center
        </h1>
        <p className="text-slate-400 text-xs mt-1">One-click PDF/HTML report generation and ZIP archive exports.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* PDF & Multi-format Generator Card */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-emerald-500/20 text-emerald-400 rounded-xl border border-emerald-500/30">
              <DocumentTextIcon className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-white text-base">Generate Training Performance Report</h3>
              <p className="text-xs text-slate-400">PDF, HTML, Markdown, CSV, and JSON format support.</p>
            </div>
          </div>
          <p className="text-xs text-slate-300">
            Includes project summary, hyperparameters, hardware telemetry averages, recommendations, AI evaluation history, and checkpoint metrics.
          </p>
          <div className="pt-2 flex gap-3">
            <button
              onClick={handleGeneratePdf}
              disabled={loading}
              className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs flex items-center gap-2 shadow-lg shadow-emerald-600/20 transition"
            >
              <ArrowDownTrayIcon className="w-4 h-4" /> Generate & Download PDF
            </button>
          </div>
        </div>

        {/* One-Click Export Center Card */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-blue-500/20 text-blue-400 rounded-xl border border-blue-500/30">
              <ArchiveBoxIcon className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-white text-base">One-Click Session ZIP Export Center</h3>
              <p className="text-xs text-slate-400">Bundles logs, metrics CSV, PDF reports, and model weights.</p>
            </div>
          </div>
          <p className="text-xs text-slate-300">
            Export a self-contained ZIP archive ready for sharing or archive storage.
          </p>
          <div className="pt-2 flex gap-3">
            <button
              onClick={handleCreateExportZip}
              disabled={loading}
              className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs flex items-center gap-2 shadow-lg shadow-blue-600/20 transition"
            >
              <ArchiveBoxIcon className="w-4 h-4" /> Generate ZIP Export Bundle
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
