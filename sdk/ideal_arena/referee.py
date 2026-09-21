from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, Mapping, Sequence, TypeVar

S = TypeVar("S")


class AgentStatus:
    OK = "OK"
    INVALID = "INVALID"
    CRASH = "CRASH"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True)
class EpisodeContext:
    episode_id: str
    seed: int
    config: Mapping[str, Any]
    num_agents: int
    rng: random.Random


@dataclass(frozen=True)
class AgentOutcome:
    seat: int
    status: str
    action: Any | None


@dataclass
class Transition(Generic[S]):
    state: S
    rewards: Sequence[float]
    to_act: Sequence[int]
    observations: Mapping[int, Any]
    done: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)


class Referee(ABC, Generic[S]):
    default_action: Any = None

    @abstractmethod
    def reset(self, ctx: EpisodeContext) -> Transition[S]: ...

    @abstractmethod
    def validate_action(self, seat: int, raw: Any, state: S) -> Any | None: ...

    @abstractmethod
    def step(self, state: S, outcomes: Sequence[AgentOutcome]) -> Transition[S]: ...

    @abstractmethod
    def finalize(self, state: S) -> Mapping[str, Any]: ...
