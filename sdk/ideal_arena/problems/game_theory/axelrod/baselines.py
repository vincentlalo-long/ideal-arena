from __future__ import annotations

import random
from typing import Final, List, Sequence

from ideal_arena.problems.game_theory.axelrod.environment import evaluate_round
from ideal_arena.problems.game_theory.axelrod.strategy import AxelrodStrategy, BaseStrategy


class AlwaysCooperate(AxelrodStrategy):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Always Cooperate")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        return 1


class AlwaysDefect(AxelrodStrategy):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Always Defect")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        return 0


class TitForTat(AxelrodStrategy):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Tit-for-Tat")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        if not history_opp:
            return 1
        return history_opp[-1]


class TitFor2Tat(AxelrodStrategy):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Tit-for-Two-Tats")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        if len(history_opp) < 2:
            return 1
        if history_opp[-1] == 0 and history_opp[-2] == 0:
            return 0
        return 1


class GrimTrigger(AxelrodStrategy):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Grim Trigger")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        if 0 in history_opp:
            return 0
        return 1


class Pavlov(AxelrodStrategy):
    """Win-Stay, Lose-Shift (WSLS / Pavlov)."""

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Pavlov")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        if not history_opp:
            return 1
        score_self, _ = evaluate_round(history_self[-1], history_opp[-1])
        if score_self in (3, 5):
            return history_self[-1]
        return 1 - history_self[-1]


class GenerousTitForTat(AxelrodStrategy):
    def __init__(self, name: str | None = None, forgiveness_prob: float = 1.0 / 3.0) -> None:
        super().__init__(name=name or "Generous Tit-for-Tat")
        self.forgiveness_prob = forgiveness_prob

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        if not history_opp:
            return 1
        if history_opp[-1] == 1:
            return 1
        return 1 if random.random() < self.forgiveness_prob else 0


class RandomStrategy(AxelrodStrategy):
    def __init__(self, name: str | None = None, coop_prob: float = 0.5) -> None:
        super().__init__(name=name or "Random")
        self.coop_prob = coop_prob

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        return 1 if random.random() < self.coop_prob else 0


class Prober(AxelrodStrategy):
    PROBING_SEQUENCE: Final[Sequence[int]] = (1, 0, 1, 1)

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name or "Prober")

    def step(self, history_self: List[int], history_opp: List[int]) -> int:
        round_index = len(history_self)
        if round_index < len(self.PROBING_SEQUENCE):
            return self.PROBING_SEQUENCE[round_index]

        opp_retaliated = (history_opp[2] == 0 or history_opp[3] == 0)
        if not opp_retaliated:
            return 0
        return history_opp[-1]


BASELINE_CLASSES: Final[list[type[AxelrodStrategy]]] = [
    AlwaysCooperate,
    AlwaysDefect,
    TitForTat,
    TitFor2Tat,
    GrimTrigger,
    Pavlov,
    GenerousTitForTat,
    RandomStrategy,
    Prober,
]


def get_all_baselines() -> list[AxelrodStrategy]:
    return [cls() for cls in BASELINE_CLASSES]
