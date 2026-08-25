"""
Unit tests for Axelrod Match Execution Engine and Payoff Mechanics.
"""

import pytest

from ideal_arena.core.match import MatchResult, play_match
from ideal_arena.core.seeding import derive_match_seed
from ideal_arena.problems.axelrod.baselines import (
    AlwaysCooperate,
    AlwaysDefect,
    GrimTrigger,
    Pavlov,
    Prober,
    RandomStrategy,
    TitForTat,
)
from ideal_arena.problems.axelrod.environment import MatchConfig
from ideal_arena.problems.axelrod.strategy import BaseStrategy


def test_mutual_cooperation() -> None:
    """AlwaysCooperate vs AlwaysCooperate: 200 rounds of (C, C) -> (600, 600)."""
    res = play_match(AlwaysCooperate(), AlwaysCooperate())
    assert res.score_a == 600
    assert res.score_b == 600
    assert res.outcome == "TIE"
    assert res.cooperation_rate_a == 1.0
    assert res.cooperation_rate_b == 1.0


def test_mutual_defection() -> None:
    """AlwaysDefect vs AlwaysDefect: 200 rounds of (D, D) -> (200, 200)."""
    res = play_match(AlwaysDefect(), AlwaysDefect())
    assert res.score_a == 200
    assert res.score_b == 200
    assert res.outcome == "TIE"
    assert res.cooperation_rate_a == 0.0
    assert res.cooperation_rate_b == 0.0


def test_tit_for_tat_vs_always_defect() -> None:
    """
    TFT vs ALLD:
    - Round 0: (C, D) -> (0, 5)
    - Rounds 1..199: (D, D) -> (199 * 1, 199 * 1)
    - Total: (199, 204), Winner: ALLD
    """
    res = play_match(TitForTat(), AlwaysDefect())
    assert res.score_a == 199
    assert res.score_b == 204
    assert res.outcome == "B_WINS"


def test_tit_for_tat_vs_always_cooperate() -> None:
    """TFT vs ALLC: 200 rounds of mutual cooperation -> (600, 600)."""
    res = play_match(TitForTat(), AlwaysCooperate())
    assert res.score_a == 600
    assert res.score_b == 600
    assert res.outcome == "TIE"


def test_prober_exploits_unretaliating_cooperator() -> None:
    """
    Prober vs ALLC:
    - Rounds 0..3 (Probing): [C, D, C, C] vs [C, C, C, C]
      - Round 0: (C, C) -> (3, 3)
      - Round 1: (D, C) -> (5, 0)
      - Round 2: (C, C) -> (3, 3)
      - Round 3: (C, C) -> (3, 3)
      - Subtotal: (14, 9)
    - Rounds 4..199 (196 rounds): Prober defects permanently against non-retaliator:
      - 196 * (D, C) -> 196 * (5, 0) = (980, 0)
    - Total: (994, 9), Winner: Prober
    """
    res = play_match(Prober(), AlwaysCooperate())
    assert res.score_a == 994
    assert res.score_b == 9
    assert res.outcome == "A_WINS"


def test_seed_reproducibility() -> None:
    """Ensures identical match seeds yield bitwise identical outcomes for stochastic strategies."""
    seed = derive_match_seed(999, "Random", "TitForTat", match_index=1)
    res_1 = play_match(RandomStrategy(), TitForTat(), seed=seed)
    res_2 = play_match(RandomStrategy(), TitForTat(), seed=seed)

    assert res_1.score_a == res_2.score_a
    assert res_1.score_b == res_2.score_b
    assert res_1.history_a == res_2.history_a
    assert res_1.history_b == res_2.history_b


def test_history_immutability() -> None:
    """Verifies that malicious strategy mutating input lists does not corrupt engine state."""

    class MutatingStrategy(BaseStrategy):
        def step(self, history_self: list[int], history_opp: list[int]) -> int:
            history_self.append(999)  # Malicious mutation
            history_opp.clear()        # Malicious mutation
            return 1

    res = play_match(MutatingStrategy(), AlwaysCooperate(), config=MatchConfig(rounds=10))
    assert res.rounds == 10
    assert len(res.history_a) == 10
    assert len(res.history_b) == 10
    assert 999 not in res.history_a
