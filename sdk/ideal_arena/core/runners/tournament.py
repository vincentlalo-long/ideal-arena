from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Literal, Sequence, Tuple, Union

from ideal_arena.core.base import GameTheoryStrategy
from ideal_arena.core.seeding import derive_match_seed, seed_context

# Type for evaluation function: (action_a, action_b) -> (score_a, score_b)
RoundEvaluator = Callable[[Any, Any], Tuple[float, float]]


@dataclass(frozen=True)
class RoundRecord:
    """Detailed record of a single round in a match."""

    round_idx: int
    action_a: Any
    action_b: Any
    payoff_a: float
    payoff_b: float


@dataclass
class MatchResult:
    """Complete summary and timeline of a finished pairwise match."""

    player_a_name: str
    player_b_name: str
    rounds: int
    score_a: float
    score_b: float
    history_a: List[Any] = field(default_factory=list)
    history_b: List[Any] = field(default_factory=list)
    seed: int | None = None

    @property
    def average_payoff_a(self) -> float:
        """Average payoff per round for Player A."""
        return self.score_a / self.rounds if self.rounds > 0 else 0.0

    @property
    def average_payoff_b(self) -> float:
        """Average payoff per round for Player B."""
        return self.score_b / self.rounds if self.rounds > 0 else 0.0

    @property
    def cooperation_rate_a(self) -> float:
        """Fraction of rounds Player A chose Cooperate (1) if applicable."""
        c = sum(1 for a in self.history_a if a == 1)
        return c / self.rounds if self.rounds > 0 else 0.0

    @property
    def cooperation_rate_b(self) -> float:
        """Fraction of rounds Player B chose Cooperate (1) if applicable."""
        c = sum(1 for b in self.history_b if b == 1)
        return c / self.rounds if self.rounds > 0 else 0.0

    @property
    def outcome(self) -> Literal["A_WINS", "B_WINS", "TIE"]:
        """Match outcome from the perspective of Player A."""
        if self.score_a > self.score_b:
            return "A_WINS"
        elif self.score_b > self.score_a:
            return "B_WINS"
        return "TIE"

    def summary(self) -> str:
        """Generates a human-readable match summary."""
        winner = (
            self.player_a_name
            if self.outcome == "A_WINS"
            else (self.player_b_name if self.outcome == "B_WINS" else "Tie")
        )
        return (
            f"Match: {self.player_a_name} vs {self.player_b_name} ({self.rounds} rounds)\n"
            f"  Score: {self.score_a:.1f} - {self.score_b:.1f} (Winner: {winner})\n"
            f"  Avg Payoff: {self.average_payoff_a:.3f} - {self.average_payoff_b:.3f}"
        )


def play_match(
    strategy_a: GameTheoryStrategy,
    strategy_b: GameTheoryStrategy,
    evaluator: RoundEvaluator,
    rounds: int = 200,
    seed: int | None = None,
    validator: Callable[[Any], Any] | None = None,
) -> MatchResult:
    """
    Executes a synchronous lock-step match between two game-theoretic strategies.

    Args:
        strategy_a: Instance of player A strategy.
        strategy_b: Instance of player B strategy.
        evaluator: Round evaluation callable (act_a, act_b) -> (score_a, score_b).
        rounds: Total rounds to simulate.
        seed: Deterministic PRNG seed for randomized strategies.
        validator: Optional action sanitizer/validator.
    """
    with seed_context(seed):
        strategy_a.reset()
        strategy_b.reset()

        hist_a: List[Any] = []
        hist_b: List[Any] = []
        total_score_a = 0.0
        total_score_b = 0.0

        for _ in range(rounds):
            raw_act_a = strategy_a.step(list(hist_a), list(hist_b))
            raw_act_b = strategy_b.step(list(hist_b), list(hist_a))

            act_a = validator(raw_act_a) if validator else raw_act_a
            act_b = validator(raw_act_b) if validator else raw_act_b

            pay_a, pay_b = evaluator(act_a, act_b)

            total_score_a += pay_a
            total_score_b += pay_b
            hist_a.append(act_a)
            hist_b.append(act_b)

        return MatchResult(
            player_a_name=strategy_a.name,
            player_b_name=strategy_b.name,
            rounds=rounds,
            score_a=total_score_a,
            score_b=total_score_b,
            history_a=hist_a,
            history_b=hist_b,
            seed=seed,
        )


@dataclass
class PlayerTournamentStats:
    """Aggregated tournament statistics for a single strategy."""

    name: str
    rank: int = 0
    total_score: float = 0.0
    matches_played: int = 0
    rounds_played: int = 0
    wins: int = 0
    losses: int = 0
    ties: int = 0
    cooperations: int = 0

    @property
    def average_payoff_per_round(self) -> float:
        return self.total_score / self.rounds_played if self.rounds_played > 0 else 0.0

    @property
    def win_rate(self) -> float:
        return self.wins / self.matches_played if self.matches_played > 0 else 0.0

    @property
    def cooperation_rate(self) -> float:
        return self.cooperations / self.rounds_played if self.rounds_played > 0 else 0.0


@dataclass
class TournamentResult:
    """Complete tournament outcome, standings, and match records."""

    standings: List[PlayerTournamentStats]
    matches: List[MatchResult]
    pairwise_scores: Dict[Tuple[str, str], Tuple[float, float]] = field(default_factory=dict)
    tournament_seed: int = 42
    rounds_per_match: int = 200

    def get_player_stat(self, player_name: str) -> PlayerTournamentStats | None:
        for stat in self.standings:
            if stat.name == player_name:
                return stat
        return None

    def display_leaderboard(self) -> str:
        headers = ["Rank", "Strategy", "Avg Payoff", "Total Score", "W - L - T", "Win %", "Coop %"]
        rows = []
        for s in self.standings:
            wlt = f"{s.wins:2d} - {s.losses:2d} - {s.ties:2d}"
            rows.append([
                f"#{s.rank:<2d}",
                s.name,
                f"{s.average_payoff_per_round:.4f}",
                f"{s.total_score:.1f}",
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
            f"=== Tournament Leaderboard (Seed: {self.tournament_seed}) ===",
            format_row(headers),
            separator,
        ]
        for row in rows:
            lines.append(format_row(row))
        lines.append(separator)
        return "\n".join(lines)


StrategyInput = Union[GameTheoryStrategy, Callable[[], GameTheoryStrategy]]


def _instantiate_strategy(strat: Any) -> Any:
    if callable(strat) and not hasattr(strat, "step"):
        return strat()
    return copy.deepcopy(strat)


def run_round_robin(
    strategies: Sequence[StrategyInput],
    evaluator: RoundEvaluator,
    rounds: int = 200,
    tournament_seed: int = 42,
    validator: Callable[[Any], Any] | None = None,
) -> TournamentResult:
    """
    Executes a complete Round-Robin tournament among all provided strategies.
    Includes pairwise matches (i < j) and self-play (i == j).
    """
    m = len(strategies)
    if m == 0:
        return TournamentResult(standings=[], matches=[], tournament_seed=tournament_seed, rounds_per_match=rounds)

    instances = [_instantiate_strategy(s) for s in strategies]
    player_names = [s.name for s in instances]

    stats_dict: Dict[str, PlayerTournamentStats] = {
        name: PlayerTournamentStats(name=name) for name in player_names
    }

    all_matches: List[MatchResult] = []
    pairwise_scores: Dict[Tuple[str, str], Tuple[float, float]] = {}

    # Pairwise matches
    for i in range(m):
        for j in range(i + 1, m):
            name_i = player_names[i]
            name_j = player_names[j]

            match_seed = derive_match_seed(tournament_seed, name_i, name_j)
            strat_i = copy.deepcopy(instances[i])
            strat_j = copy.deepcopy(instances[j])

            res = play_match(strat_i, strat_j, evaluator=evaluator, rounds=rounds, seed=match_seed, validator=validator)
            all_matches.append(res)
            pairwise_scores[(name_i, name_j)] = (res.score_a, res.score_b)
            pairwise_scores[(name_j, name_i)] = (res.score_b, res.score_a)

            st_i = stats_dict[name_i]
            st_i.total_score += res.score_a
            st_i.matches_played += 1
            st_i.rounds_played += rounds
            st_i.cooperations += sum(1 for a in res.history_a if a == 1)

            st_j = stats_dict[name_j]
            st_j.total_score += res.score_b
            st_j.matches_played += 1
            st_j.rounds_played += rounds
            st_j.cooperations += sum(1 for b in res.history_b if b == 1)

            if res.outcome == "A_WINS":
                st_i.wins += 1
                st_j.losses += 1
            elif res.outcome == "B_WINS":
                st_j.wins += 1
                st_i.losses += 1
            else:
                st_i.ties += 1
                st_j.ties += 1

    # Self-play matches
    for i in range(m):
        name_i = player_names[i]
        match_seed = derive_match_seed(tournament_seed, name_i, name_i, match_index=1)
        inst_1 = copy.deepcopy(instances[i])
        inst_2 = copy.deepcopy(instances[i])

        res_self = play_match(inst_1, inst_2, evaluator=evaluator, rounds=rounds, seed=match_seed, validator=validator)
        all_matches.append(res_self)
        pairwise_scores[(name_i, name_i)] = (res_self.score_a, res_self.score_b)

        st_i = stats_dict[name_i]
        st_i.total_score += res_self.score_a
        st_i.matches_played += 1
        st_i.rounds_played += rounds
        st_i.cooperations += sum(1 for a in res_self.history_a if a == 1)

        if res_self.outcome == "A_WINS":
            st_i.wins += 1
        elif res_self.outcome == "B_WINS":
            st_i.losses += 1
        else:
            st_i.ties += 1

    # Standings ranking
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
        rounds_per_match=rounds,
    )
