import { BotSpec, MatchResult, TournamentResult } from '../types/arena';

const API_BASE = '/api/v1';

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}

export async function simulateMatch(
  playerA: BotSpec,
  playerB: BotSpec,
  rounds: number = 200
): Promise<MatchResult> {
  const res = await fetch(`${API_BASE}/matches/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_a: playerA, player_b: playerB, rounds }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }
  return res.json();
}

export async function simulateTournament(
  bots: BotSpec[],
  rounds: number = 50,
  concurrency: number = 4
): Promise<TournamentResult> {
  const res = await fetch(`${API_BASE}/tournaments/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bots, rounds, concurrency }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.statusText}`);
  }
  return res.json();
}

export function generateDemoMatch(rounds: number = 200): MatchResult {
  const histA: number[] = [];
  const histB: number[] = [];
  let scoreA = 0;
  let scoreB = 0;

  for (let t = 0; t < rounds; t++) {
    // Player A: Tit-for-Tat
    const actA = t === 0 ? 1 : histB[t - 1];

    // Player B: Prober (Detective)
    let actB = 1;
    if (t === 0) actB = 1;
    else if (t === 1) actB = 0;
    else if (t === 2 || t === 3) actB = 1;
    else {
      const retaliated = histA[2] === 0 || histA[3] === 0;
      actB = retaliated ? histA[t - 1] : 0;
    }

    let pa = 1, pb = 1;
    if (actA === 1 && actB === 1) { pa = 3; pb = 3; }
    else if (actA === 1 && actB === 0) { pa = 0; pb = 5; }
    else if (actA === 0 && actB === 1) { pa = 5; pb = 0; }

    scoreA += pa;
    scoreB += pb;
    histA.push(actA);
    histB.push(actB);
  }

  return {
    player_a_name: 'Tit-for-Tat (Python)',
    player_b_name: 'Prober (Detective)',
    rounds,
    score_a: scoreA,
    score_b: scoreB,
    history_a: histA,
    history_b: histB,
    duration_ns: 25000000,
  };
}
