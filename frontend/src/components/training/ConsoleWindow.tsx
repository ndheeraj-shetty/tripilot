import React, { useState, useRef, useEffect } from 'react';
import {
  CommandLineIcon,
  ArrowDownIcon,
  MagnifyingGlassIcon,
  TrashIcon,
  ArrowDownTrayIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface ConsoleWindowProps {
  logs: string[];
  onClear: () => void;
}

export const ConsoleWindow: React.FC<ConsoleWindowProps> = ({ logs, onClear }) => {
  const [autoScroll, setAutoScroll] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterErrors, setFilterErrors] = useState(false);
  const logContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (autoScroll && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, autoScroll]);

  const filteredLogs = logs.filter((line) => {
    const matchesSearch = searchQuery ? line.toLowerCase().includes(searchQuery.toLowerCase()) : true;
    const matchesError = filterErrors ? line.toLowerCase().includes('error') || line.toLowerCase().includes('failed') || line.toLowerCase().includes('stderr') : true;
    return matchesSearch && matchesError;
  });

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([logs.join('\n')], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `zombie_run_training_logs_${Date.now()}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="glass-panel rounded-2xl overflow-hidden border border-slate-800 flex flex-col">
      {/* Console Top Toolbar */}
      <div className="bg-slate-900 px-4 py-3 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs select-none">
        <div className="flex items-center gap-2 font-mono text-slate-300">
          <CommandLineIcon className="w-4 h-4 text-blue-400" />
          <span className="font-semibold">Stdout / Stderr Stream Console</span>
          <span className="text-slate-500">({filteredLogs.length} lines)</span>
        </div>

        <div className="flex items-center gap-3">
          {/* Search Filter */}
          <div className="relative">
            <MagnifyingGlassIcon className="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-2" />
            <input
              type="text"
              placeholder="Search logs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg pl-8 pr-3 py-1 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 w-40"
            />
          </div>

          {/* Filter Errors Button */}
          <button
            onClick={() => setFilterErrors(!filterErrors)}
            className={`px-2.5 py-1 rounded-lg border text-xs flex items-center gap-1.5 transition ${
              filterErrors
                ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 font-medium'
                : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
            }`}
          >
            <ExclamationTriangleIcon className="w-3.5 h-3.5" /> Errors Only
          </button>

          {/* Auto Scroll Toggle */}
          <button
            onClick={() => setAutoScroll(!autoScroll)}
            className={`px-2.5 py-1 rounded-lg border text-xs flex items-center gap-1.5 transition ${
              autoScroll
                ? 'bg-blue-600/20 text-blue-300 border-blue-500/40 font-medium'
                : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
            }`}
          >
            <ArrowDownIcon className="w-3.5 h-3.5" /> Auto-scroll
          </button>

          {/* Download Logs */}
          <button
            onClick={handleDownload}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            title="Download Logs as TXT"
          >
            <ArrowDownTrayIcon className="w-4 h-4" />
          </button>

          {/* Clear Console */}
          <button
            onClick={onClear}
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition"
            title="Clear Console"
          >
            <TrashIcon className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Terminal Text Buffer */}
      <div
        ref={logContainerRef}
        className="p-4 bg-[#070a12] font-mono text-xs text-slate-300 h-80 overflow-y-auto space-y-1 selection:bg-blue-600 selection:text-white"
      >
        {filteredLogs.length === 0 ? (
          <div className="text-slate-600 italic text-center pt-16">No log stream output recorded yet. Launch a session to stream logs.</div>
        ) : (
          filteredLogs.map((line, idx) => (
            <div key={idx} className="flex items-start gap-3">
              <span className="text-slate-600 select-none w-8 text-right shrink-0">{idx + 1}</span>
              <span
                className={
                  line.toLowerCase().includes('error') || line.toLowerCase().includes('failed')
                    ? 'text-rose-400 font-semibold'
                    : line.includes('Epoch:')
                    ? 'text-blue-300'
                    : 'text-slate-300'
                }
              >
                {line}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
