# Axelrod Iterated Prisoner's Dilemma (IPD) Environment.

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Final, Tuple

# Action Constants
ACTION_DEFECT: Final[int] = 0
ACTION_COOPERATE: Final[int] = 1
VALID_ACTIONS: Final[frozenset[int]] = frozenset({ACTION_DEFECT, ACTION_COOPERATE})

# Canonical Axelrod Payoffs: T > R > P > S and 2R > T + S
PAYOFF_TEMPTATION: Final[int] = 5  # T: Defect against Cooperate
PAYOFF_REWARD: Final[int] = 3      # R: Mutual Cooperation
PAYOFF_PUNISHMENT: Final[int] = 1  # P: Mutual Defection
PAYOFF_SUCKER: Final[int] = 0      # S: Cooperate against Defect

# Mapping: (action_agent1, action_agent2) -> (payoff_agent1, payoff_agent2)
PAYOFF_MATRIX: Final[dict[Tuple[int, int], Tuple[int, int]]] = {
    (ACTION_COOPERATE, ACTION_COOPERATE): (PAYOFF_REWARD, PAYOFF_REWARD),          # (1, 1) -> (3, 3)
    (ACTION_COOPERATE, ACTION_DEFECT):    (PAYOFF_SUCKER, PAYOFF_TEMPTATION),      # (1, 0) -> (0, 5)
    (ACTION_DEFECT,    ACTION_COOPERATE): (PAYOFF_TEMPTATION, PAYOFF_SUCKER),      # (0, 1) -> (5, 0)
    (ACTION_DEFECT,    ACTION_DEFECT):    (PAYOFF_PUNISHMENT, PAYOFF_PUNISHMENT),  # (0, 0) -> (1, 1)
}


@dataclass(frozen=True)
class MatchConfig:
    # Configuration parameters for an Axelrod IPD match.
    rounds: int = 200
    step_timeout_ms: float = 10.0
    match_timeout_s: float = 2.0


def validate_action(action: Any) -> int:
    # Validates that an action token is a valid discrete action (0 or 1).
    if action is True or action == 1:
        return ACTION_COOPERATE
    return ACTION_DEFECT


def evaluate_round(action_1: int, action_2: int) -> Tuple[int, int]:
    a1 = validate_action(action_1)
    a2 = validate_action(action_2)
    return PAYOFF_MATRIX[(a1, a2)]
