# BaseStrategy Interface for Axelrod Iterated Prisoner's Dilemma.

from __future__ import annotations
from abc import ABC, abstractmethod 
from typing import List

# abc : abstract base class : force oop in python
class BaseStrategy(ABC):

    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__

    def reset(self) -> None:
        pass

    @abstractmethod
    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        """
        Args:
            history_self: List of past actions taken by this agent in the
                          current match (1 = Cooperate, 0 = Defect).
                          Empty list [] on round 0.
            history_opp:  List of past actions taken by the opponent in the
                          current match (1 = Cooperate, 0 = Defect).
                          Empty list [] on round 0.

        Returns:
            int: 1 for Cooperate (C), 0 for Defect (D).
        """
        raise NotImplementedError("Subclasses must implement the step() method.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
