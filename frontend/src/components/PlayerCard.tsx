import React from 'react';

interface PlayerCardProps {
  label: string;
  name: string;
  currentMove: number | null; // 1 = C, 0 = D, null = Pending
  totalScore: number;
  avgPayoff: number;
  coopRate: number;
  colorScheme: 'blue' | 'purple';
}

export const PlayerCard: React.FC<PlayerCardProps> = ({
  label,
  name,
  currentMove,
  totalScore,
  avgPayoff,
  coopRate,
  colorScheme,
}) => {
  const isBlue = colorScheme === 'blue';

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-lg relative overflow-hidden">
      <div className="flex justify-between items-start">
        <div>
          <span className={`text-[11px] font-bold uppercase tracking-wider ${isBlue ? 'text-blue-400' : 'text-purple-400'}`}>
            {label}
          </span>
          <h2 className="text-lg font-bold text-white mt-0.5 truncate max-w-[240px]">{name}</h2>
        </div>

        {currentMove !== null ? (
          <div
            className={`px-3 py-1 rounded text-xs font-bold border tracking-wider ${
              currentMove === 1
                ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                : 'bg-rose-500/20 text-rose-400 border-rose-500/40'
            }`}
          >
            {currentMove === 1 ? 'COOPERATE' : 'DEFECT'}
          </div>
        ) : (
          <div className="px-3 py-1 rounded text-xs font-mono text-slate-500 border border-slate-800 bg-slate-950">
            PENDING
          </div>
        )}
      </div>

      <div className="grid grid-cols-3 gap-2 mt-5 pt-4 border-t border-slate-800/80 text-center">
        <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/50">
          <div className="text-[11px] text-slate-400 font-medium">Total Score</div>
          <div className="text-xl font-black text-white mt-0.5">{totalScore}</div>
        </div>
        <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/50">
          <div className="text-[11px] text-slate-400 font-medium">Avg Payoff</div>
          <div className={`text-xl font-black mt-0.5 ${isBlue ? 'text-blue-400' : 'text-purple-400'}`}>
            {avgPayoff.toFixed(3)}
          </div>
        </div>
        <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/50">
          <div className="text-[11px] text-slate-400 font-medium">Cooperation</div>
          <div className="text-xl font-black text-emerald-400 mt-0.5">{coopRate.toFixed(1)}%</div>
        </div>
      </div>
    </div>
  );
};
