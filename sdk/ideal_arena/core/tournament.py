"""Backward compatibility wrapper for tournament runner."""

from ideal_arena.core.runners.tournament import (
    PlayerTournamentStats,
    TournamentResult,
    run_round_robin as _generic_run_round_robin,
)


def run_round_robin(
    strategies,
    config=None,
    tournament_seed=42,
    evaluator=None,
    rounds=None,
    validator=None,
):
    """Executes a round-robin tournament."""
    if evaluator is None:
        from ideal_arena.problems.game_theory.axelrod.environment import (
            evaluate_round,
            validate_action,
        )
        eval_fn = evaluate_round
        val_fn = validate_action
    else:
        eval_fn = evaluator
        val_fn = validator

    total_rounds = rounds or (config.rounds if config else 200)
    return _generic_run_round_robin(
        strategies=strategies,
        evaluator=eval_fn,
        rounds=total_rounds,
        tournament_seed=tournament_seed,
        validator=val_fn,
    )


__all__ = ["PlayerTournamentStats", "TournamentResult", "run_round_robin"]
