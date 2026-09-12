"""Unit tests for Round-Robin Tournament Orchestrator and Leaderboard Rankings."""

import unittest

from ideal_arena.core.tournament import run_round_robin
from ideal_arena.problems.axelrod.baselines import (
    AlwaysCooperate,
    AlwaysDefect,
    GrimTrigger,
    Pavlov,
    TitForTat,
    get_all_baselines,
)
from ideal_arena.problems.axelrod.environment import MatchConfig


class TestAxelrodTournament(unittest.TestCase):
    def test_tournament_match_count(self) -> None:
        baselines = get_all_baselines()
        m = len(baselines)
        expected_matches = (m * (m + 1)) // 2

        res = run_round_robin(baselines, config=MatchConfig(rounds=10), tournament_seed=42)
        self.assertEqual(len(res.matches), expected_matches)
        self.assertEqual(len(res.standings), m)

    def test_tournament_standings_order(self) -> None:
        baselines = get_all_baselines()
        res = run_round_robin(baselines, config=MatchConfig(rounds=50), tournament_seed=42)

        for i in range(len(res.standings) - 1):
            curr_p = res.standings[i].average_payoff_per_round
            next_p = res.standings[i + 1].average_payoff_per_round
            self.assertGreaterEqual(curr_p, next_p)

    def test_tournament_tit_for_tat_dominance(self) -> None:
        strats = [TitForTat(), AlwaysDefect(), AlwaysCooperate(), Pavlov(), GrimTrigger()]
        res = run_round_robin(strats, config=MatchConfig(rounds=50), tournament_seed=42)

        tft_stat = res.get_player_stat("Tit-for-Tat")
        alld_stat = res.get_player_stat("Always Defect")
        allc_stat = res.get_player_stat("Always Cooperate")

        self.assertIsNotNone(tft_stat)
        self.assertIsNotNone(alld_stat)
        self.assertIsNotNone(allc_stat)

        self.assertGreater(tft_stat.average_payoff_per_round, alld_stat.average_payoff_per_round)
        self.assertGreater(tft_stat.average_payoff_per_round, allc_stat.average_payoff_per_round)

    def test_tournament_reproducibility(self) -> None:
        baselines = get_all_baselines()
        res_1 = run_round_robin(baselines, config=MatchConfig(rounds=50), tournament_seed=12345)
        res_2 = run_round_robin(baselines, config=MatchConfig(rounds=50), tournament_seed=12345)

        for s1, s2 in zip(res_1.standings, res_2.standings):
            self.assertEqual(s1.name, s2.name)
            self.assertEqual(s1.total_score, s2.total_score)
            self.assertEqual(s1.wins, s2.wins)
            self.assertEqual(s1.losses, s2.losses)
            self.assertEqual(s1.ties, s2.ties)

    def test_tournament_empty_pool(self) -> None:
        res = run_round_robin([], tournament_seed=42)
        self.assertEqual(len(res.standings), 0)
        self.assertEqual(len(res.matches), 0)

    def test_tournament_display_leaderboard(self) -> None:
        baselines = get_all_baselines()
        res = run_round_robin(baselines, config=MatchConfig(rounds=10), tournament_seed=42)
        output = res.display_leaderboard()
        self.assertIn("Leaderboard", output)
        self.assertIn("Tit-for-Tat", output)
        self.assertIn("Avg Payoff", output)


if __name__ == "__main__":
    unittest.main()
