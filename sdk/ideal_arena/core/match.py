
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Literal, Tuple

from ideal_arena.core.seeding import seed_context
from ideal_arena.problems.axelrod.environment import (
    MatchConfig,
    evaluate_round,
    validate_action,
)
from ideal_arena.problems.axelrod.strategy import BaseStrategy


@dataclass(frozen=True)
class RoundRecord:
    """Detailed record of a single round in a match."""

    round_idx: int
    action_a: int
    action_b: int
    payoff_a: int
    payoff_b: int


@dataclass
class MatchResult:
    """Complete summary and timeline of a finished pairwise match."""

    player_a_name: str
    player_b_name: str
    rounds: int
    score_a: int
    score_b: int
    history_a: List[int] = field(default_factory=list)
    history_b: List[int] = field(default_factory=list)
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
        """Fraction of rounds Player A chose Cooperate (1)."""
        return sum(self.history_a) / self.rounds if self.rounds > 0 else 0.0

    @property
    def cooperation_rate_b(self) -> float:
        """Fraction of rounds Player B chose Cooperate (1)."""
        return sum(self.history_b) / self.rounds if self.rounds > 0 else 0.0

    @property
    def outcome(self) -> Literal["A_WINS", "B_WINS", "TIE"]:
        """Match outcome from the perspective of Player A."""
        if self.score_a > self.score_b:
            return "A_WINS"
        elif self.score_b > self.score_a:
            return "B_WINS"
        return "TIE"

    def summary(self) -> str:
        """Generates a human-readable match summary table."""
        winner = (
            self.player_a_name
            if self.outcome == "A_WINS"
            else (self.player_b_name if self.outcome == "B_WINS" else "Tie")
        )
        return (
            f"Match: {self.player_a_name} vs {self.player_b_name} ({self.rounds} rounds)\n"
            f"  Score: {self.score_a} - {self.score_b} (Winner: {winner})\n"
            f"  Avg Payoff: {self.average_payoff_a:.3f} - {self.average_payoff_b:.3f}\n"
            f"  Coop Rate: {self.cooperation_rate_a * 100:.1f}% - {self.cooperation_rate_b * 100:.1f}%"
        )


def play_match(
    strategy_a: BaseStrategy,
    strategy_b: BaseStrategy,
    config: MatchConfig | None = None,
    seed: int | None = None,
) -> MatchResult:
    """
    Executes a synchronous lock-step match between two strategies.

    Args:
        strategy_a: Instance of player A strategy.
        strategy_b: Instance of player B strategy.
        config: Match configuration parameters (defaults to 200 rounds).
        seed: Deterministic PRNG seed for randomized strategies.

    Returns:
        MatchResult: Comprehensive match result object.
    """
    cfg = config or MatchConfig()

    with seed_context(seed):
        # 1. Reset both strategies to ensure hermetic isolation between matches
        strategy_a.reset()
        strategy_b.reset()

        hist_a: List[int] = []
        hist_b: List[int] = []
        total_score_a = 0
        total_score_b = 0

        # 2. Synchronous lock-step round execution
        for _ in range(cfg.rounds):
            # Pass shallow copies of histories to prevent strategies from mutating them
            raw_act_a = strategy_a.step(list(hist_a), list(hist_b))
            raw_act_b = strategy_b.step(list(hist_b), list(hist_a))

            # Validate actions (fallback to Defect on invalid values)
            act_a = validate_action(raw_act_a)
            act_b = validate_action(raw_act_b)

            # Evaluate stage payoffs
            pay_a, pay_b = evaluate_round(act_a, act_b)

            # Accumulate scores and update history
            total_score_a += pay_a
            total_score_b += pay_b
            hist_a.append(act_a)
            hist_b.append(act_b)

        return MatchResult(
            player_a_name=strategy_a.name,
            player_b_name=strategy_b.name,
            rounds=cfg.rounds,
            score_a=total_score_a,
            score_b=total_score_b,
            history_a=hist_a,
            history_b=hist_b,
            seed=seed,
        )
