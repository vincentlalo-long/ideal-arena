"""
Unit tests for Round-Robin Tournament Orchestrator and Leaderboard Rankings.
"""

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


def test_tournament_match_count() -> None:
    """Verifies total pairwise match count equals M*(M+1)/2 including self-play."""
    baselines = get_all_baselines()
    m = len(baselines)
    expected_matches = (m * (m + 1)) // 2

    res = run_round_robin(baselines, config=MatchConfig(rounds=10), tournament_seed=42)
    assert len(res.matches) == expected_matches
    assert len(res.standings) == m


def test_tournament_standings_order() -> None:
    """Verifies leaderboard standings are monotonically descending by average payoff."""
    baselines = get_all_baselines()
    res = run_round_robin(baselines, config=MatchConfig(rounds=50), tournament_seed=42)

    for i in range(len(res.standings) - 1):
        curr_p = res.standings[i].average_payoff_per_round
        next_p = res.standings[i + 1].average_payoff_per_round
        assert curr_p >= next_p, f"Standings not sorted at rank {i+1}: {curr_p} < {next_p}"


def test_tournament_tit_for_tat_dominance() -> None:
    """Confirms TitForTat outperforms pure AlwaysDefect and AlwaysCooperate in overall tournament."""
    strats = [TitForTat(), AlwaysDefect(), AlwaysCooperate(), Pavlov(), GrimTrigger()]
    res = run_round_robin(strats, config=MatchConfig(rounds=50), tournament_seed=42)

    tft_stat = res.get_player_stat("Tit-for-Tat")
    alld_stat = res.get_player_stat("Always Defect")
    allc_stat = res.get_player_stat("Always Cooperate")

    assert tft_stat is not None
    assert alld_stat is not None
    assert allc_stat is not None

    assert tft_stat.average_payoff_per_round > alld_stat.average_payoff_per_round
    assert tft_stat.average_payoff_per_round > allc_stat.average_payoff_per_round


def test_tournament_reproducibility() -> None:
    """Ensures running tournament with identical seed produces bitwise identical standings."""
    baselines = get_all_baselines()
    res_1 = run_round_robin(baselines, config=MatchConfig(rounds=50), tournament_seed=12345)
    res_2 = run_round_robin(baselines, config=MatchConfig(rounds=50), tournament_seed=12345)

    for s1, s2 in zip(res_1.standings, res_2.standings):
        assert s1.name == s2.name
        assert s1.total_score == s2.total_score
        assert s1.wins == s2.wins
        assert s1.losses == s2.losses
        assert s1.ties == s2.ties


def test_tournament_empty_pool() -> None:
    """Verifies tournament engine handles empty strategy list gracefully."""
    res = run_round_robin([], tournament_seed=42)
    assert len(res.standings) == 0
    assert len(res.matches) == 0


def test_tournament_display_leaderboard() -> None:
    """Verifies display_leaderboard renders valid formatted table string."""
    baselines = get_all_baselines()
    res = run_round_robin(baselines, config=MatchConfig(rounds=10), tournament_seed=42)
    output = res.display_leaderboard()
    assert "Leaderboard" in output
    assert "Tit-for-Tat" in output
    assert "Avg Payoff" in output
