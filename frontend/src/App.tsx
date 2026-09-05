import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { MatchVisualizer } from './components/MatchVisualizer';
import { TournamentDashboard } from './components/TournamentDashboard';
import { checkHealth } from './services/api';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'visualizer' | 'tournament'>('visualizer');
  const [isOnline, setIsOnline] = useState<boolean>(false);

  useEffect(() => {
    checkHealth().then(setIsOnline);
    const interval = setInterval(() => {
      checkHealth().then(setIsOnline);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header activeTab={activeTab} onTabChange={setActiveTab} isOnline={isOnline} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-8">
        {activeTab === 'visualizer' ? <MatchVisualizer /> : <TournamentDashboard />}
      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        Ideal Arena © 2026 - High-Performance Algorithmic Multi-Agent Sandbox Platform
      </footer>
    </div>
  );
};

export default App;
