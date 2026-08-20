"""Axelrod Iterated Prisoner's Dilemma (IPD) Problem Module."""

from ideal_arena.problems.axelrod.baselines import (
    BASELINE_CLASSES,
    AlwaysCooperate,
    AlwaysDefect,
    GenerousTitForTat,
    GrimTrigger,
    Pavlov,
    Prober,
    RandomStrategy,
    TitFor2Tat,
    TitForTat,
    get_all_baselines,
)
from ideal_arena.problems.axelrod.environment import (
    ACTION_COOPERATE,
    ACTION_DEFECT,
    PAYOFF_MATRIX,
    PAYOFF_PUNISHMENT,
    PAYOFF_REWARD,
    PAYOFF_SUCKER,
    PAYOFF_TEMPTATION,
    VALID_ACTIONS,
    MatchConfig,
    evaluate_round,
    validate_action,
)
from ideal_arena.problems.axelrod.strategy import BaseStrategy

__all__ = [
    # Environment & Payoffs
    "ACTION_COOPERATE",
    "ACTION_DEFECT",
    "PAYOFF_MATRIX",
    "PAYOFF_PUNISHMENT",
    "PAYOFF_REWARD",
    "PAYOFF_SUCKER",
    "PAYOFF_TEMPTATION",
    "VALID_ACTIONS",
    "MatchConfig",
    "evaluate_round",
    "validate_action",
    # Abstract Base
    "BaseStrategy",
    # 9 Canonical Baselines
    "AlwaysCooperate",
    "AlwaysDefect",
    "TitForTat",
    "TitFor2Tat",
    "GrimTrigger",
    "Pavlov",
    "GenerousTitForTat",
    "RandomStrategy",
    "Prober",
    "BASELINE_CLASSES",
    "get_all_baselines",
]
