"""Backward compatibility wrapper for axelrod baselines."""

from ideal_arena.problems.game_theory.axelrod.baselines import (
    BASELINE_CLASSES,
    AlwaysCooperate,
    AlwaysDefect,
    GrimTrigger,
    Pavlov,
    Prober,
    RandomStrategy,
    TitFor2Tat,
    TitForTat,
    get_all_baselines,
)

__all__ = [
    "BASELINE_CLASSES",
    "AlwaysCooperate",
    "AlwaysDefect",
    "GrimTrigger",
    "Pavlov",
    "Prober",
    "RandomStrategy",
    "TitFor2Tat",
    "TitForTat",
    "get_all_baselines",
]
