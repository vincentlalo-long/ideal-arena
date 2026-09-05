import React from 'react';

interface PayoffChartProps {
  nameA: string;
  nameB: string;
  dataA: number[];
  dataB: number[];
  currentRound: number;
  totalRounds: number;
}

export const PayoffChart: React.FC<PayoffChartProps> = ({
  nameA,
  nameB,
  dataA,
  dataB,
  currentRound,
  totalRounds,
}) => {
  const width = 800;
  const height = 240;
  const padding = { top: 20, right: 30, bottom: 30, left: 50 };

  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  // Find max score
  const maxScore = Math.max(
    10,
    ...dataA,
    ...dataB,
    totalRounds * 3
  );

  const getX = (roundIndex: number) => {
    if (totalRounds <= 1) return padding.left;
    return padding.left + (roundIndex / (totalRounds - 1)) * chartWidth;
  };

  const getY = (score: number) => {
    return padding.top + chartHeight - (score / maxScore) * chartHeight;
  };

  // Build SVG path
  const buildPath = (data: number[]) => {
    if (data.length === 0) return '';
    return data
      .map((val, idx) => `${idx === 0 ? 'M' : 'L'} ${getX(idx)} ${getY(val)}`)
      .join(' ');
  };

  const pathA = buildPath(dataA);
  const pathB = buildPath(dataB);

  // Current scrubber cursor X
  const cursorX = currentRound > 0 ? getX(currentRound - 1) : padding.left;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
          Cumulative Payoff Trajectory
        </h3>
        <div className="flex items-center space-x-4 text-xs">
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-0.5 bg-blue-500 inline-block" />
            <span className="text-slate-300 font-medium truncate max-w-[150px]">{nameA}</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-0.5 bg-purple-400 inline-block" />
            <span className="text-slate-300 font-medium truncate max-w-[150px]">{nameB}</span>
          </div>
        </div>
      </div>

      <div className="w-full overflow-hidden">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
          {/* Horizontal Grid Lines */}
          {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => {
            const y = padding.top + chartHeight * (1 - pct);
            const scoreLabel = Math.round(maxScore * pct);
            return (
              <g key={i}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="#1e293b"
                  strokeDasharray="4 4"
                />
                <text
                  x={padding.left - 10}
                  y={y + 4}
                  textAnchor="end"
                  fontSize="10"
                  fill="#64748b"
                  fontFamily="monospace"
                >
                  {scoreLabel}
                </text>
              </g>
            );
          })}

          {/* Paths */}
          {pathA && (
            <path
              d={pathA}
              fill="none"
              stroke="#3b82f6"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          )}
          {pathB && (
            <path
              d={pathB}
              fill="none"
              stroke="#c084fc"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          )}

          {/* Current Scrubber Cursor Line */}
          {currentRound > 0 && (
            <line
              x1={cursorX}
              y1={padding.top}
              x2={cursorX}
              y2={padding.top + chartHeight}
              stroke="#f8fafc"
              strokeWidth="1.5"
              strokeDasharray="2 2"
              opacity="0.75"
            />
          )}
        </svg>
      </div>
    </div>
  );
};
