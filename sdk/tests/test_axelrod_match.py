"""Unit tests for Axelrod Match Execution Engine and Payoff Mechanics."""

import unittest

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


class TestAxelrodMatch(unittest.TestCase):
    def test_mutual_cooperation(self) -> None:
        """AlwaysCooperate vs AlwaysCooperate: 200 rounds of (C, C) -> (600, 600)."""
        res = play_match(AlwaysCooperate(), AlwaysCooperate())
        self.assertEqual(res.score_a, 600)
        self.assertEqual(res.score_b, 600)
        self.assertEqual(res.outcome, "TIE")
        self.assertEqual(res.cooperation_rate_a, 1.0)
        self.assertEqual(res.cooperation_rate_b, 1.0)

    def test_mutual_defection(self) -> None:
        """AlwaysDefect vs AlwaysDefect: 200 rounds of (D, D) -> (200, 200)."""
        res = play_match(AlwaysDefect(), AlwaysDefect())
        self.assertEqual(res.score_a, 200)
        self.assertEqual(res.score_b, 200)
        self.assertEqual(res.outcome, "TIE")
        self.assertEqual(res.cooperation_rate_a, 0.0)
        self.assertEqual(res.cooperation_rate_b, 0.0)

    def test_tit_for_tat_vs_always_defect(self) -> None:
        res = play_match(TitForTat(), AlwaysDefect())
        self.assertEqual(res.score_a, 199)
        self.assertEqual(res.score_b, 204)
        self.assertEqual(res.outcome, "B_WINS")

    def test_tit_for_tat_vs_always_cooperate(self) -> None:
        res = play_match(TitForTat(), AlwaysCooperate())
        self.assertEqual(res.score_a, 600)
        self.assertEqual(res.score_b, 600)
        self.assertEqual(res.outcome, "TIE")

    def test_prober_exploits_unretaliating_cooperator(self) -> None:
        res = play_match(Prober(), AlwaysCooperate())
        self.assertEqual(res.score_a, 994)
        self.assertEqual(res.score_b, 9)
        self.assertEqual(res.outcome, "A_WINS")

    def test_seed_reproducibility(self) -> None:
        seed = derive_match_seed(999, "Random", "TitForTat", match_index=1)
        res_1 = play_match(RandomStrategy(), TitForTat(), seed=seed)
        res_2 = play_match(RandomStrategy(), TitForTat(), seed=seed)

        self.assertEqual(res_1.score_a, res_2.score_a)
        self.assertEqual(res_1.score_b, res_2.score_b)
        self.assertEqual(res_1.history_a, res_2.history_a)
        self.assertEqual(res_1.history_b, res_2.history_b)

    def test_history_immutability(self) -> None:
        class MutatingStrategy(BaseStrategy):
            def step(self, history_self: list[int], history_opp: list[int]) -> int:
                history_self.append(999)
                history_opp.clear()
                return 1

        res = play_match(MutatingStrategy(), AlwaysCooperate(), config=MatchConfig(rounds=10))
        self.assertEqual(res.rounds, 10)
        self.assertEqual(len(res.history_a), 10)
        self.assertEqual(len(res.history_b), 10)
        self.assertNotIn(999, res.history_a)


if __name__ == "__main__":
    unittest.main()
