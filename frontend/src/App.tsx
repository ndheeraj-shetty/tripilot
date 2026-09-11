import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastProvider } from './components/common/Toast';
import { Layout } from './components/layout/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { AIDashboardPage } from './pages/AIDashboardPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { TrainingPage } from './pages/TrainingPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';
import { AutomationPage } from './pages/AutomationPage';
import { CheckpointManagerPage } from './pages/CheckpointManagerPage';
import { ModelComparisonPage } from './pages/ModelComparisonPage';
import { ReportsPage } from './pages/ReportsPage';

import { HistoryPage } from './pages/HistoryPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/ai-hub" element={<AIDashboardPage />} />
              <Route path="/projects" element={<ProjectsPage />} />
              <Route path="/training" element={<TrainingPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/checkpoints" element={<CheckpointManagerPage />} />
              <Route path="/compare" element={<ModelComparisonPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/automation" element={<AutomationPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </ToastProvider>
    </QueryClientProvider>
  );
};
