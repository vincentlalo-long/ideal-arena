"""Backward compatibility wrapper for match runner."""

from ideal_arena.core.runners.tournament import (
    MatchResult,
    RoundRecord,
    play_match as _generic_play_match,
)


def play_match(strategy_a, strategy_b, config=None, seed=None, evaluator=None, rounds=None):
    """Executes a match between two strategies."""
    if evaluator is None:
        from ideal_arena.problems.game_theory.axelrod.environment import (
            evaluate_round,
            validate_action,
        )
        eval_fn = evaluate_round
        val_fn = validate_action
    else:
        eval_fn = evaluator
        val_fn = None

    total_rounds = rounds or (config.rounds if config else 200)
    return _generic_play_match(
        strategy_a,
        strategy_b,
        evaluator=eval_fn,
        rounds=total_rounds,
        seed=seed,
        validator=val_fn,
    )


__all__ = ["RoundRecord", "MatchResult", "play_match"]
