from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Sequence, Tuple, Union

from ideal_arena.core.match import MatchResult, play_match
from ideal_arena.core.seeding import derive_match_seed
from ideal_arena.problems.axelrod.environment import MatchConfig
from ideal_arena.problems.axelrod.strategy import BaseStrategy


@dataclass
class PlayerTournamentStats:
    """Aggregated tournament statistics for a single strategy."""

    name: str
    rank: int = 0
    total_score: int = 0
    matches_played: int = 0
    rounds_played: int = 0
    wins: int = 0
    losses: int = 0
    ties: int = 0
    total_cooperations: int = 0

    @property
    def average_payoff_per_round(self) -> float:
        """Primary tournament ranking metric: u_bar_i = total_score / (M * T)."""
        return self.total_score / self.rounds_played if self.rounds_played > 0 else 0.0

    @property
    def cooperation_rate(self) -> float:
        """Overall tournament cooperation rate: rho_C = total_cooperations / total_rounds."""
        return self.total_cooperations / self.rounds_played if self.rounds_played > 0 else 0.0

    @property
    def win_rate(self) -> float:
        """Fraction of matches won."""
        return self.wins / self.matches_played if self.matches_played > 0 else 0.0


@dataclass
class TournamentResult:
    """Complete tournament outcome, standings, and match records."""

    standings: List[PlayerTournamentStats]
    matches: List[MatchResult]
    pairwise_scores: Dict[Tuple[str, str], Tuple[int, int]] = field(default_factory=dict)
    tournament_seed: int = 42
    rounds_per_match: int = 200

    def get_player_stat(self, player_name: str) -> PlayerTournamentStats | None:
        """Returns the stats for a specific player name if present."""
        for stat in self.standings:
            if stat.name == player_name:
                return stat
        return None

    def display_leaderboard(self) -> str:
        """
        Renders an aligned, human-readable terminal leaderboard table.
        """
        headers = ["Rank", "Strategy", "Avg Payoff", "Total Score", "W - L - T", "Win %", "Coop %"]
        rows = []
        for s in self.standings:
            wlt = f"{s.wins:2d} - {s.losses:2d} - {s.ties:2d}"
            rows.append([
                f"#{s.rank:<2d}",
                s.name,
                f"{s.average_payoff_per_round:.4f}",
                str(s.total_score),
                wlt,
                f"{s.win_rate * 100:5.1f}%",
                f"{s.cooperation_rate * 100:5.1f}%",
            ])

        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(val))

        def format_row(values: list[str]) -> str:
            return " | ".join(f"{v:<{col_widths[i]}}" for i, v in enumerate(values))

        separator = "-+-".join("-" * w for w in col_widths)

        lines = [
            f"=== Algorithm Arena Tournament Leaderboard (Seed: {self.tournament_seed}) ===",
            format_row(headers),
            separator,
        ]
        for row in rows:
            lines.append(format_row(row))
        lines.append(separator)
        return "\n".join(lines)


StrategyInput = Union[BaseStrategy, Callable[[], BaseStrategy]]


def _instantiate_strategy(strat: StrategyInput) -> BaseStrategy:
    """Instantiates a strategy whether passed as instance or factory callable."""
    if isinstance(strat, BaseStrategy):
        return copy.deepcopy(strat)
    return strat()


def run_round_robin(
    strategies: Sequence[StrategyInput],
    config: MatchConfig | None = None,
    tournament_seed: int = 42,
) -> TournamentResult:
    """
    Executes a complete Round-Robin tournament among all provided strategies.

    Args:
        strategies: List of strategy instances or factory functions.
        config: Match configuration parameters (default: 200 rounds).
        tournament_seed: Master integer seed for deterministic match derivation.

    Returns:
        TournamentResult: Complete tournament results and sorted leaderboard.
    """
    cfg = config or MatchConfig()
    m = len(strategies)
    if m == 0:
        return TournamentResult(standings=[], matches=[], tournament_seed=tournament_seed)

    # 1. Instantiate strategies and build player roster
    instances = [_instantiate_strategy(s) for s in strategies]
    player_names = [s.name for s in instances]

    # Initialize per-player statistics
    stats_dict: Dict[str, PlayerTournamentStats] = {
        name: PlayerTournamentStats(name=name) for name in player_names
    }

    all_matches: List[MatchResult] = []
    pairwise_scores: Dict[Tuple[str, str], Tuple[int, int]] = {}

    # 2. Pairwise Matches (i < j)
    for i in range(m):
        for j in range(i + 1, m):
            name_i = player_names[i]
            name_j = player_names[j]

            # Derive deterministic seed for pair (i, j)
            match_seed = derive_match_seed(tournament_seed, name_i, name_j)
            strat_i = copy.deepcopy(instances[i])
            strat_j = copy.deepcopy(instances[j])

            # Play match
            res = play_match(strat_i, strat_j, config=cfg, seed=match_seed)
            all_matches.append(res)
            pairwise_scores[(name_i, name_j)] = (res.score_a, res.score_b)
            pairwise_scores[(name_j, name_i)] = (res.score_b, res.score_a)

            # Update stats for player i
            st_i = stats_dict[name_i]
            st_i.total_score += res.score_a
            st_i.matches_played += 1
            st_i.rounds_played += cfg.rounds
            st_i.total_cooperations += sum(res.history_a)
            if res.outcome == "A_WINS":
                st_i.wins += 1
            elif res.outcome == "B_WINS":
                st_i.losses += 1
            else:
                st_i.ties += 1

            # Update stats for player j
            st_j = stats_dict[name_j]
            st_j.total_score += res.score_b
            st_j.matches_played += 1
            st_j.rounds_played += cfg.rounds
            st_j.total_cooperations += sum(res.history_b)
            if res.outcome == "B_WINS":
                st_j.wins += 1
            elif res.outcome == "A_WINS":
                st_j.losses += 1
            else:
                st_j.ties += 1

    # 3. Self-Play Matches (i == j)
    for i in range(m):
        name_i = player_names[i]
        match_seed = derive_match_seed(tournament_seed, name_i, name_i, match_index=1)
        inst_1 = copy.deepcopy(instances[i])
        inst_2 = copy.deepcopy(instances[i])

        res_self = play_match(inst_1, inst_2, config=cfg, seed=match_seed)
        all_matches.append(res_self)
        pairwise_scores[(name_i, name_i)] = (res_self.score_a, res_self.score_b)

        st_i = stats_dict[name_i]
        st_i.total_score += res_self.score_a
        st_i.matches_played += 1
        st_i.rounds_played += cfg.rounds
        st_i.total_cooperations += sum(res_self.history_a)
        if res_self.outcome == "A_WINS":
            st_i.wins += 1
        elif res_self.outcome == "B_WINS":
            st_i.losses += 1
        else:
            st_i.ties += 1

    # 4. Tie-Breaking & Standings Ranking
    # Sort criteria according to Document B:
    # 1. Higher average payoff per round (total score / total rounds)
    # 2. Higher match wins
    # 3. Higher overall cooperation rate
    sorted_stats = sorted(
        stats_dict.values(),
        key=lambda s: (
            -s.average_payoff_per_round,
            -s.wins,
            -s.cooperation_rate,
        ),
    )

    for rank_idx, stat in enumerate(sorted_stats, start=1):
        stat.rank = rank_idx

    return TournamentResult(
        standings=sorted_stats,
        matches=all_matches,
        pairwise_scores=pairwise_scores,
        tournament_seed=tournament_seed,
        rounds_per_match=cfg.rounds,
    )
