from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable

PROTOCOL_VERSION = "orcust-agent/1"


@runtime_checkable
class Agent(Protocol):
    name: str

    def reset(self, seed: int | None = None) -> None: ...

    def act(self, observation: Any) -> Any: ...


class BaseAgent(ABC):
    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or self.__class__.__name__

    def reset(self, seed: int | None = None) -> None:
        pass

    @abstractmethod
    def act(self, observation: Any) -> Any:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
