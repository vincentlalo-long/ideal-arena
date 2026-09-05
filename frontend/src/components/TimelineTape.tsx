import React from 'react';

interface TimelineTapeProps {
  historyA: number[];
  historyB: number[];
  currentRound: number;
  totalRounds: number;
  onSeek: (round: number) => void;
}

export const TimelineTape: React.FC<TimelineTapeProps> = ({
  historyA,
  historyB,
  currentRound,
  totalRounds,
  onSeek,
}) => {
  return (
    <div className="space-y-1.5 pt-2">
      <div className="flex justify-between items-center text-[11px] text-slate-400 font-medium">
        <span>Timeline Matrix (Green = Cooperate, Red = Defect)</span>
        <span className="text-slate-500 font-mono">Click any slot to seek</span>
      </div>

      <div className="space-y-1 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 overflow-x-auto">
        <div className="flex gap-1 min-w-max">
          <span className="w-5 text-[10px] text-blue-400 font-bold self-center">A:</span>
          {Array.from({ length: totalRounds }).map((_, i) => {
            const isPlayed = i < historyA.length;
            const isCurrent = i === currentRound - 1;
            const act = isPlayed ? historyA[i] : null;

            return (
              <div
                key={i}
                onClick={() => onSeek(i + 1)}
                title={`Round ${i + 1}: Player A = ${act === 1 ? 'Cooperate' : 'Defect'}`}
                className={`w-2.5 h-4 rounded-[2px] cursor-pointer transition-transform hover:scale-125 ${
                  act === 1
                    ? 'bg-emerald-500'
                    : act === 0
                    ? 'bg-rose-500'
                    : 'bg-slate-800'
                } ${isCurrent ? 'ring-2 ring-white z-10' : 'opacity-80'}`}
              />
            );
          })}
        </div>

        <div className="flex gap-1 min-w-max">
          <span className="w-5 text-[10px] text-purple-400 font-bold self-center">B:</span>
          {Array.from({ length: totalRounds }).map((_, i) => {
            const isPlayed = i < historyB.length;
            const isCurrent = i === currentRound - 1;
            const act = isPlayed ? historyB[i] : null;

            return (
              <div
                key={i}
                onClick={() => onSeek(i + 1)}
                title={`Round ${i + 1}: Player B = ${act === 1 ? 'Cooperate' : 'Defect'}`}
                className={`w-2.5 h-4 rounded-[2px] cursor-pointer transition-transform hover:scale-125 ${
                  act === 1
                    ? 'bg-emerald-500'
                    : act === 0
                    ? 'bg-rose-500'
                    : 'bg-slate-800'
                } ${isCurrent ? 'ring-2 ring-white z-10' : 'opacity-80'}`}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};
