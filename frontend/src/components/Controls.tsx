import React from 'react';

interface ControlsProps {
  currentRound: number;
  totalRounds: number;
  isPlaying: boolean;
  speed: number;
  onPlayToggle: () => void;
  onNext: () => void;
  onPrev: () => void;
  onSeek: (round: number) => void;
  onSpeedChange: (speed: number) => void;
  onSimulate: () => void;
  isLoading: boolean;
}

export const Controls: React.FC<ControlsProps> = ({
  currentRound,
  totalRounds,
  isPlaying,
  speed,
  onPlayToggle,
  onNext,
  onPrev,
  onSeek,
  onSpeedChange,
  onSimulate,
  isLoading,
}) => {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Round:</span>
          <span className="text-lg font-mono font-bold text-white bg-slate-950 px-3 py-1 rounded border border-slate-800">
            {currentRound} / {totalRounds}
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => onSeek(0)}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition"
            title="Start"
          >
            ⏮
          </button>
          <button
            onClick={onPrev}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition"
            title="Previous"
          >
            ◀
          </button>
          <button
            onClick={onPlayToggle}
            className={`px-4 py-2 font-bold rounded shadow transition min-w-[80px] text-xs uppercase tracking-wider ${
              isPlaying
                ? 'bg-amber-600 hover:bg-amber-500 text-white'
                : 'bg-blue-600 hover:bg-blue-500 text-white'
            }`}
          >
            {isPlaying ? 'Pause ❚❚' : 'Play ▶'}
          </button>
          <button
            onClick={onNext}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition"
            title="Next"
          >
            ▶
          </button>
          <button
            onClick={() => onSeek(totalRounds)}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition"
            title="End"
          >
            ⏭
          </button>
        </div>

        <div className="flex items-center space-x-3 text-xs">
          <div className="flex items-center space-x-1.5">
            <span className="text-slate-400 font-medium">Speed:</span>
            <select
              value={speed}
              onChange={(e) => onSpeedChange(Number(e.target.value))}
              className="bg-slate-950 text-slate-200 border border-slate-800 rounded px-2 py-1.5 focus:outline-none focus:border-blue-500 font-mono"
            >
              <option value={400}>0.5x</option>
              <option value={200}>1x</option>
              <option value={100}>2x</option>
              <option value={40}>5x</option>
            </select>
          </div>

          <button
            onClick={onSimulate}
            disabled={isLoading}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 text-white px-3.5 py-1.5 rounded font-bold transition shadow"
          >
            {isLoading ? 'Running...' : 'Simulate Match'}
          </button>
        </div>
      </div>

      {/* Progress Slider */}
      <input
        type="range"
        min={0}
        max={totalRounds}
        value={currentRound}
        onChange={(e) => onSeek(Number(e.target.value))}
        className="w-full h-2 bg-slate-950 rounded-lg appearance-none cursor-pointer accent-blue-500 border border-slate-800/80"
      />
    </div>
  );
};
