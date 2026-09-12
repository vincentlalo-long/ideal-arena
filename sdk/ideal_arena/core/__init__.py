"""Ideal Arena Core: Problem Domain Abstractions, Seeding, and Runners."""

from ideal_arena.core.base import (
    BaseAgent,
    BaseEnvironment,
    BaseProblem,
    GameTheoryStrategy,
    OptimizationSolver,
    ProblemDomain,
    ProblemMetadata,
    SimulationAgent,
)
from ideal_arena.core.registry import (
    get_problem,
    list_domains,
    list_problems,
    register_problem,
)
from ideal_arena.core.runners.tournament import (
    MatchResult,
    PlayerTournamentStats,
    TournamentResult,
    play_match,
    run_round_robin,
)
from ideal_arena.core.seeding import derive_match_seed, seed_context

__all__ = [
    "BaseAgent",
    "BaseEnvironment",
    "BaseProblem",
    "GameTheoryStrategy",
    "OptimizationSolver",
    "SimulationAgent",
    "ProblemDomain",
    "ProblemMetadata",
    "register_problem",
    "get_problem",
    "list_problems",
    "list_domains",
    "play_match",
    "run_round_robin",
    "MatchResult",
    "TournamentResult",
    "PlayerTournamentStats",
    "seed_context",
    "derive_match_seed",
]
