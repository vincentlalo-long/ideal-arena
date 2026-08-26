"""Core matchmaking, tournament, and seeding abstractions."""

from ideal_arena.core.match import MatchResult, RoundRecord, play_match
from ideal_arena.core.seeding import derive_match_seed, seed_context
from ideal_arena.core.tournament import (
    PlayerTournamentStats,
    TournamentResult,
    run_round_robin,
)

__all__ = [
    "derive_match_seed",
    "seed_context",
    "RoundRecord",
    "MatchResult",
    "play_match",
    "PlayerTournamentStats",
    "TournamentResult",
    "run_round_robin",
]
