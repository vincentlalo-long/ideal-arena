export interface MatchResult {
  player_a_name: string;
  player_b_name: string;
  rounds: number;
  score_a: number;
  score_b: number;
  history_a: number[];
  history_b: number[];
  duration_ns: number;
}

export interface PlayerStats {
  name: string;
  rank: number;
  total_score: number;
  matches_played: number;
  rounds_played: number;
  wins: number;
  losses: number;
  ties: number;
  avg_payoff: number;
  coop_rate: number;
}

export interface TournamentResult {
  standings: PlayerStats[];
  matches: MatchResult[];
}

export interface BotSpec {
  name: string;
  command: string;
  args: string[];
}
