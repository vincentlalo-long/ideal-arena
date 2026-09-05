import React, { useState, useEffect, useRef } from 'react';
import { MatchResult } from '../types/arena';
import { PlayerCard } from './PlayerCard';
import { PayoffChart } from './PayoffChart';
import { TimelineTape } from './TimelineTape';
import { Controls } from './Controls';
import { simulateMatch, generateDemoMatch } from '../services/api';

export const MatchVisualizer: React.FC = () => {
  const [matchData, setMatchData] = useState<MatchResult>(() => generateDemoMatch(200));
  const [currentRound, setCurrentRound] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [speed, setSpeed] = useState<number>(100);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const playTimerRef = useRef<number | null>(null);

  // Auto-play interval logic
  useEffect(() => {
    if (isPlaying) {
      playTimerRef.current = setInterval(() => {
        setCurrentRound((prev) => {
          if (prev >= matchData.rounds) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, speed);
    } else if (playTimerRef.current) {
      clearInterval(playTimerRef.current);
    }
    return () => {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    };
  }, [isPlaying, speed, matchData.rounds]);

  // Compute metrics up to current round
  let scoreA = 0, scoreB = 0;
  let coopA = 0, coopB = 0;
  const cumA: number[] = [];
  const cumB: number[] = [];

  for (let i = 0; i < currentRound; i++) {
    const actA = matchData.history_a[i];
    const actB = matchData.history_b[i];

    let pa = 1, pb = 1;
    if (actA === 1 && actB === 1) { pa = 3; pb = 3; }
    else if (actA === 1 && actB === 0) { pa = 0; pb = 5; }
    else if (actA === 0 && actB === 1) { pa = 5; pb = 0; }

    scoreA += pa;
    scoreB += pb;
    if (actA === 1) coopA++;
    if (actB === 1) coopB++;

    cumA.push(scoreA);
    cumB.push(scoreB);
  }

  const avgA = currentRound > 0 ? scoreA / currentRound : 0;
  const avgB = currentRound > 0 ? scoreB / currentRound : 0;
  const cRateA = currentRound > 0 ? (coopA / currentRound) * 100 : 100;
  const cRateB = currentRound > 0 ? (coopB / currentRound) * 100 : 100;

  const curMoveA = currentRound > 0 ? matchData.history_a[currentRound - 1] : null;
  const curMoveB = currentRound > 0 ? matchData.history_b[currentRound - 1] : null;

  const handleSimulate = async () => {
    setIsLoading(true);
    try {
      const res = await simulateMatch(
        { name: 'Tit-for-Tat (Python)', command: 'python', args: ['../../adapters/python/runner.py'] },
        { name: 'Always-Defect (Python)', command: 'python', args: ['../../adapters/python/runner.py'] },
        200
      );
      setMatchData(res);
      setCurrentRound(0);
      setIsPlaying(true);
    } catch {
      // Fallback demo
      setMatchData(generateDemoMatch(200));
      setCurrentRound(0);
      setIsPlaying(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Player Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PlayerCard
          label="Player A"
          name={matchData.player_a_name}
          currentMove={curMoveA}
          totalScore={scoreA}
          avgPayoff={avgA}
          coopRate={cRateA}
          colorScheme="blue"
        />
        <PlayerCard
          label="Player B"
          name={matchData.player_b_name}
          currentMove={curMoveB}
          totalScore={scoreB}
          avgPayoff={avgB}
          coopRate={cRateB}
          colorScheme="purple"
        />
      </div>

      {/* Controls */}
      <Controls
        currentRound={currentRound}
        totalRounds={matchData.rounds}
        isPlaying={isPlaying}
        speed={speed}
        onPlayToggle={() => setIsPlaying(!isPlaying)}
        onNext={() => setCurrentRound((r) => Math.min(matchData.rounds, r + 1))}
        onPrev={() => setCurrentRound((r) => Math.max(0, r - 1))}
        onSeek={(r) => setCurrentRound(r)}
        onSpeedChange={(s) => setSpeed(s)}
        onSimulate={handleSimulate}
        isLoading={isLoading}
      />

      {/* Timeline Tape */}
      <TimelineTape
        historyA={matchData.history_a}
        historyB={matchData.history_b}
        currentRound={currentRound}
        totalRounds={matchData.rounds}
        onSeek={(r) => setCurrentRound(r)}
      />

      {/* Payoff Chart */}
      <PayoffChart
        nameA={matchData.player_a_name}
        nameB={matchData.player_b_name}
        dataA={cumA}
        dataB={cumB}
        currentRound={currentRound}
        totalRounds={matchData.rounds}
      />
    </div>
  );
};
