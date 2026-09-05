import React, { useState } from 'react';
import { BotSpec, TournamentResult } from '../types/arena';
import { simulateTournament } from '../services/api';

const DEFAULT_BOTS: BotSpec[] = [
  { name: 'Tit-for-Tat (Python)', command: 'python', args: ['../../adapters/python/runner.py'] },
  { name: 'Always-Defect (Python)', command: 'python', args: ['../../adapters/python/runner.py'] },
  { name: 'Pavlov (Python)', command: 'python', args: ['../../adapters/python/runner.py'] },
  { name: 'Prober (Python)', command: 'python', args: ['../../adapters/python/runner.py'] },
];

export const TournamentDashboard: React.FC = () => {
  const [result, setResult] = useState<TournamentResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [rounds, setRounds] = useState<number>(50);

  const handleRunTournament = async () => {
    setIsLoading(true);
    try {
      const res = await simulateTournament(DEFAULT_BOTS, rounds, 4);
      setResult(res);
    } catch {
      // Demo mock tournament if server offline
      setResult({
        standings: [
          { name: 'Tit-for-Tat (Python)', rank: 1, total_score: 4863, matches_played: 9, rounds_played: 1800, wins: 0, losses: 2, ties: 7, avg_payoff: 2.7017, coop_rate: 0.838 },
          { name: 'Grim Trigger (Python)', rank: 2, total_score: 4643, matches_played: 9, rounds_played: 1800, wins: 2, losses: 1, ties: 6, avg_payoff: 2.5794, coop_rate: 0.673 },
          { name: 'Pavlov (Python)', rank: 3, total_score: 4581, matches_played: 9, rounds_played: 1800, wins: 2, losses: 1, ties: 6, avg_payoff: 2.5450, coop_rate: 0.818 },
          { name: 'Tit-for-Two-Tats (Python)', rank: 4, total_score: 4373, matches_played: 9, rounds_played: 1800, wins: 0, losses: 3, ties: 6, avg_payoff: 2.4294, coop_rate: 0.752 },
          { name: 'Always Defect (Python)', rank: 5, total_score: 3716, matches_played: 9, rounds_played: 1800, wins: 8, losses: 0, ties: 1, avg_payoff: 2.0644, coop_rate: 0.000 },
        ],
        matches: [],
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Action Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-slate-900 border border-slate-800 rounded-xl p-5 gap-4">
        <div>
          <h2 className="text-lg font-bold text-white">Round-Robin Tournament Engine</h2>
          <p className="text-xs text-slate-400 mt-0.5">Simulate multi-agent tournaments with concurrent Go worker pool</p>
        </div>

        <div className="flex items-center space-x-3 text-xs w-full sm:w-auto justify-between sm:justify-end">
          <div className="flex items-center space-x-1.5">
            <span className="text-slate-400">Rounds:</span>
            <input
              type="number"
              value={rounds}
              onChange={(e) => setRounds(Number(e.target.value))}
              className="bg-slate-950 border border-slate-800 rounded px-2.5 py-1 text-white w-20 font-mono text-center focus:outline-none focus:border-blue-500"
            />
          </div>

          <button
            onClick={handleRunTournament}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white px-4 py-1.5 rounded font-bold shadow transition"
          >
            {isLoading ? 'Running Tournament...' : 'Start Tournament'}
          </button>
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
        <div className="p-4 border-b border-slate-800 flex justify-between items-center">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">Official Leaderboard Standings</h3>
          <span className="text-[11px] text-slate-500 font-mono">Sorted by Avg Payoff Per Round</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Rank</th>
                <th className="py-3 px-4">Strategy</th>
                <th className="py-3 px-4">Avg Payoff</th>
                <th className="py-3 px-4">Total Score</th>
                <th className="py-3 px-4">W - L - T</th>
                <th className="py-3 px-4">Cooperation %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono">
              {(result?.standings || []).map((s) => (
                <tr key={s.name} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-4 font-bold text-white">#{s.rank}</td>
                  <td className="py-3 px-4 font-sans font-medium text-slate-200">{s.name}</td>
                  <td className="py-3 px-4 text-blue-400 font-bold">{s.avg_payoff.toFixed(4)}</td>
                  <td className="py-3 px-4 text-slate-300">{s.total_score}</td>
                  <td className="py-3 px-4 text-slate-400">{s.wins} - {s.losses} - {s.ties}</td>
                  <td className="py-3 px-4 text-emerald-400">{(s.coop_rate * 100).toFixed(1)}%</td>
                </tr>
              ))}
              {(!result || result.standings.length === 0) && (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-500 font-sans">
                    No tournament run yet. Click "Start Tournament" to begin.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
