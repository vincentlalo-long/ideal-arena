from __future__ import annotations

from typing import Dict, List, Optional, Type

from ideal_arena.core.base import BaseProblem, ProblemDomain

_PROBLEM_REGISTRY: Dict[str, BaseProblem] = {}


def register_problem(problem: BaseProblem) -> None:
    """Registers a problem instance in the global registry."""
    _PROBLEM_REGISTRY[problem.problem_id] = problem


def get_problem(problem_id: str) -> BaseProblem:
    """Retrieves a registered problem by its identifier."""
    # Ensure default problems are loaded
    _ensure_defaults_loaded()

    if problem_id not in _PROBLEM_REGISTRY:
        available = ", ".join(_PROBLEM_REGISTRY.keys())
        raise KeyError(f"Problem '{problem_id}' not found. Available problems: {available}")
    return _PROBLEM_REGISTRY[problem_id]


def list_problems(domain: Optional[ProblemDomain | str] = None) -> List[BaseProblem]:
    """Lists all registered problems, optionally filtered by domain."""
    _ensure_defaults_loaded()

    problems = list(_PROBLEM_REGISTRY.values())
    if domain is not None:
        domain_val = domain.value if isinstance(domain, ProblemDomain) else domain
        problems = [p for p in problems if p.domain.value == domain_val]
    return problems


def list_domains() -> List[ProblemDomain]:
    """Lists all active problem domains."""
    return list(ProblemDomain)


def _ensure_defaults_loaded() -> None:
    """Lazily imports problems to populate the registry."""
    if _PROBLEM_REGISTRY:
        return

    try:
        from ideal_arena.problems.game_theory.axelrod.problem import AxelrodProblem
        register_problem(AxelrodProblem())
    except ImportError:
        pass
