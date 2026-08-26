"""
Ideal Arena Command-Line Interface (CLI).

Provides local developer commands to simulate matches, benchmark submissions
against standard baselines, and inspect tournament leaderboards.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from typing import Type

from ideal_arena.core.match import play_match
from ideal_arena.core.tournament import run_round_robin
from ideal_arena.problems.axelrod.baselines import (
    AlwaysCooperate,
    AlwaysDefect,
    GrimTrigger,
    Pavlov,
    TitForTat,
    get_all_baselines,
)
from ideal_arena.problems.axelrod.environment import MatchConfig
from ideal_arena.problems.axelrod.strategy import BaseStrategy

OPPONENT_PRESETS: dict[str, Type[BaseStrategy]] = {
    "tft": TitForTat,
    "titfortat": TitForTat,
    "allc": AlwaysCooperate,
    "alld": AlwaysDefect,
    "pavlov": Pavlov,
    "grim": GrimTrigger,
}


def load_strategy_from_file(file_path: str) -> BaseStrategy:
    """Dynamically loads a custom BaseStrategy subclass from a Python source file."""
    if not os.path.exists(file_path):
        print(f"Error: Strategy file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        print(f"Error: Failed to load module from {file_path}", file=sys.stderr)
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Find the first BaseStrategy subclass defined in the module
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (
            isinstance(attr, type)
            and issubclass(attr, BaseStrategy)
            and attr is not BaseStrategy
        ):
            return attr()

    print(
        f"Error: No subclass of BaseStrategy found in {file_path}.",
        file=sys.stderr,
    )
    sys.exit(1)


def cmd_baselines(args: argparse.Namespace) -> None:
    """Executes the standard 9-baseline tournament."""
    strats = get_all_baselines()
    config = MatchConfig(rounds=args.rounds)
    print(f"Running 9-baseline round-robin tournament ({args.rounds} rounds/match, Seed: {args.seed})...")
    res = run_round_robin(strats, config=config, tournament_seed=args.seed)
    print("\n" + res.display_leaderboard())


def cmd_match(args: argparse.Namespace) -> None:
    """Executes a single match between two strategies."""
    # Load player A
    strat_a = load_strategy_from_file(args.player_a)

    # Load player B (either file or preset)
    player_b_lower = args.player_b.lower()
    if player_b_lower in OPPONENT_PRESETS:
        strat_b = OPPONENT_PRESETS[player_b_lower]()
    else:
        strat_b = load_strategy_from_file(args.player_b)

    config = MatchConfig(rounds=args.rounds)
    res = play_match(strat_a, strat_b, config=config, seed=args.seed)
    print("\n" + res.summary())


def cmd_benchmark(args: argparse.Namespace) -> None:
    """Benchmarks a custom strategy against the 9 canonical baselines."""
    custom_strat = load_strategy_from_file(args.strategy_file)
    baselines = get_all_baselines()
    roster = [custom_strat] + baselines

    config = MatchConfig(rounds=args.rounds)
    print(f"Benchmarking '{custom_strat.name}' against 9 canonical baselines (Seed: {args.seed})...")
    res = run_round_robin(roster, config=config, tournament_seed=args.seed)
    print("\n" + res.display_leaderboard())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ideal-arena",
        description="Ideal Arena CLI: Multi-Agent Benchmark and Tournament Simulator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: baselines
    p_base = subparsers.add_parser("baselines", help="Run the canonical 9-baseline tournament")
    p_base.add_argument("--rounds", type=int, default=200, help="Rounds per match (default: 200)")
    p_base.add_argument("--seed", type=int, default=42, help="Tournament master seed (default: 42)")
    p_base.set_defaults(func=cmd_baselines)

    # Command: match
    p_match = subparsers.add_parser("match", help="Simulate a match between two strategies")
    p_match.add_argument("player_a", help="Path to Python file for Player A")
    p_match.add_argument("player_b", help="Path to Python file for Player B (or preset: tft, alld, allc, pavlov)")
    p_match.add_argument("--rounds", type=int, default=200, help="Rounds per match (default: 200)")
    p_match.add_argument("--seed", type=int, default=42, help="Match PRNG seed (default: 42)")
    p_match.set_defaults(func=cmd_match)

    # Command: benchmark
    p_bench = subparsers.add_parser("benchmark", help="Benchmark a strategy against all 9 baselines")
    p_bench.add_argument("strategy_file", help="Path to Python file containing your custom strategy")
    p_bench.add_argument("--rounds", type=int, default=200, help="Rounds per match (default: 200)")
    p_bench.add_argument("--seed", type=int, default=42, help="Tournament master seed (default: 42)")
    p_bench.set_defaults(func=cmd_benchmark)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
