from __future__ import annotations

from abc import abstractmethod
from typing import List

from ideal_arena.core.base import GameTheoryStrategy


class AxelrodStrategy(GameTheoryStrategy):
    """Base class for strategies participating in the Iterated Prisoner's Dilemma."""

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name)

    @abstractmethod
    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        """
        Chooses an action for the current round.

        Args:
            history_self: List of past actions chosen by this strategy (0: Defect, 1: Cooperate).
            history_opp: List of past actions chosen by the opponent (0: Defect, 1: Cooperate).

        Returns:
            0 (Defect) or 1 (Cooperate).
        """
        raise NotImplementedError


# Alias for backward-compatibility
BaseStrategy = AxelrodStrategy
