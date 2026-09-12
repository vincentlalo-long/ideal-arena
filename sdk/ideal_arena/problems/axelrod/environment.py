"""Backward compatibility wrapper for axelrod environment."""

from ideal_arena.problems.game_theory.axelrod.environment import (
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

__all__ = [
    "ACTION_COOPERATE",
    "ACTION_DEFECT",
    "VALID_ACTIONS",
    "PAYOFF_TEMPTATION",
    "PAYOFF_REWARD",
    "PAYOFF_PUNISHMENT",
    "PAYOFF_SUCKER",
    "PAYOFF_MATRIX",
    "MatchConfig",
    "validate_action",
    "evaluate_round",
]
