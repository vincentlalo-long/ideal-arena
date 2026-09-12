from __future__ import annotations

from typing import Any, List, Tuple

from ideal_arena.core.base import BaseProblem, ProblemDomain, ProblemMetadata
from ideal_arena.problems.game_theory.axelrod.baselines import get_all_baselines
from ideal_arena.problems.game_theory.axelrod.environment import (
    MatchConfig,
    evaluate_round,
    validate_action,
)
from ideal_arena.problems.game_theory.axelrod.strategy import AxelrodStrategy


class AxelrodProblem(BaseProblem):
    """Formal problem definition for Iterated Prisoner's Dilemma."""

    metadata = ProblemMetadata(
        problem_id="axelrod",
        name="Iterated Prisoner's Dilemma",
        domain=ProblemDomain.GAME_THEORY,
        version="1.0.0",
        description="Axelrod's classic 2-player iterated game theory tournament.",
        tags=["game-theory", "ipd", "cooperation", "axelrod"],
    )

    def get_baselines(self) -> List[AxelrodStrategy]:
        return get_all_baselines()

    def evaluate_round(self, action_a: int, action_b: int) -> Tuple[int, int]:
        return evaluate_round(action_a, action_b)

    def validate_action(self, action: Any) -> int:
        return validate_action(action)

    def default_config(self) -> MatchConfig:
        return MatchConfig()
