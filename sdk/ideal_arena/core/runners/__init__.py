"""Execution engines and tournament runners."""

from ideal_arena.core.runners.tournament import (
    MatchResult,
    PlayerTournamentStats,
    TournamentResult,
    play_match,
    run_round_robin,
)

__all__ = [
    "MatchResult",
    "PlayerTournamentStats",
    "TournamentResult",
    "play_match",
    "run_round_robin",
]
