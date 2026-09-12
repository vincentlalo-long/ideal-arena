from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ProblemDomain(str, Enum):
    """Supported problem paradigms in Ideal Arena."""

    GAME_THEORY = "game_theory"
    OPTIMIZATION = "optimization"
    SIMULATION = "simulation"


@dataclass
class ProblemMetadata:
    """Metadata describing a problem specification."""

    problem_id: str
    name: str
    domain: ProblemDomain
    version: str = "1.0.0"
    description: str = ""
    author: str = "Ideal Arena"
    tags: List[str] = field(default_factory=list)


class BaseAgent(ABC):
    """Abstract base class for all autonomous agents, strategies, and solvers."""

    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__

    def reset(self) -> None:
        """Resets any internal agent state between episodes, instances, or matches."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class GameTheoryStrategy(BaseAgent):
    """Base class for multi-agent game-theoretic strategies (e.g. Axelrod IPD)."""

    @abstractmethod
    def step(self, history_self: List[Any], history_opp: List[Any]) -> Any:
        """
        Determines the next move given action histories.

        Args:
            history_self: List of past actions chosen by this strategy.
            history_opp: List of past actions chosen by the opponent.

        Returns:
            The selected action for the current step.
        """
        raise NotImplementedError


class OptimizationSolver(BaseAgent):
    """Base class for solvers addressing combinatorial or continuous optimization problems."""

    @abstractmethod
    def solve(self, instance: Any) -> Any:
        """
        Solves an optimization instance.

        Args:
            instance: Problem instance data (e.g., coordinates, weights, constraints).

        Returns:
            Candidate solution (e.g. tour, subset of items, assignment).
        """
        raise NotImplementedError


class SimulationAgent(BaseAgent):
    """Base class for agents interacting sequentially with an environment."""

    @abstractmethod
    def act(self, observation: Any) -> Any:
        """
        Selects an action given the current observation from the environment.

        Args:
            observation: State or observation representation from the environment.

        Returns:
            Action to execute in the environment.
        """
        raise NotImplementedError


class BaseProblem(ABC):
    """Abstract base class for all problems in Ideal Arena."""

    metadata: ProblemMetadata

    @property
    def problem_id(self) -> str:
        return self.metadata.problem_id

    @property
    def domain(self) -> ProblemDomain:
        return self.metadata.domain

    @property
    def name(self) -> str:
        return self.metadata.name

    @abstractmethod
    def get_baselines(self) -> List[BaseAgent]:
        """Returns the canonical baseline implementations for this problem."""
        raise NotImplementedError


class BaseEnvironment(ABC):
    """Abstract base class for stateful simulation environments."""

    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> Any:
        """Resets the environment to an initial state and returns the initial observation."""
        raise NotImplementedError

    @abstractmethod
    def step(self, action: Any) -> Tuple[Any, float, bool, Dict[str, Any]]:
        """
        Transitions the environment forward by one step.

        Returns:
            Tuple of (observation, reward, terminated, info).
        """
        raise NotImplementedError
