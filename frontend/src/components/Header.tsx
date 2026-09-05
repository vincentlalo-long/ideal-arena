import React from 'react';

interface HeaderProps {
  activeTab: 'visualizer' | 'tournament';
  onTabChange: (tab: 'visualizer' | 'tournament') => void;
  isOnline: boolean;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, onTabChange, isOnline }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50 px-6 py-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <span className="text-2xl font-black tracking-wider text-blue-500">IDEAL ARENA</span>
          <span className="text-xs bg-blue-950 text-blue-400 border border-blue-800/80 px-2 py-0.5 rounded font-mono font-medium">v0.1.0</span>
        </div>
        <span className="hidden md:inline text-slate-600">|</span>
        <span className="hidden md:inline text-xs text-slate-400">Competitive Multi-Agent Judger Platform</span>
      </div>

      <div className="flex items-center space-x-3 w-full md:w-auto justify-between md:justify-end">
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => onTabChange('visualizer')}
            className={`px-4 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'visualizer'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Match Visualizer
          </button>
          <button
            onClick={() => onTabChange('tournament')}
            className={`px-4 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'tournament'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Tournament Leaderboard
          </button>
        </div>

        <div className="flex items-center space-x-2 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-full text-xs">
          <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
          <span className="text-slate-300 font-mono text-[11px]">{isOnline ? 'Judger API Online' : 'Local Fallback'}</span>
        </div>
      </div>
    </header>
  );
};
