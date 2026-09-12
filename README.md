# Ideal Arena

[![CI Pipeline](https://github.com/vincentlalo-long/ideal-arena/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentlalo-long/ideal-arena/actions)

Ideal Arena is an extensible, high-performance competitive platform for algorithmic strategy development, multi-agent game theory simulations, optimization benchmarks, and tournament evaluation.

## Architecture

The platform is designed around domain paradigms with clean separation between core runners and concrete problem implementations:

- **sdk/**: Python SDK with core abstractions (`BaseProblem`, `GameTheoryStrategy`, `OptimizationSolver`, `SimulationAgent`), deterministic PRNG seeding, tournament engines, and CLI.
  - `core/`: Generic problem registry, execution runners, and seeding context (fully decoupled from specific problems).
  - `problems/`: Categorized by domain paradigm:
    - `game_theory/`: Multi-agent games (including `axelrod` - Iterated Prisoner's Dilemma).
    - `optimization/`: Combinatorial and continuous optimization benchmarks (extensible).
    - `simulation/`: Sequential decision-making and agent-environment simulations (extensible).
- **server/**: Go backend platform featuring a sandboxed subprocess judger with a watchdog timer, REST API endpoints, and an interactive Terminal UI (TUI).
- **adapters/**: Multi-language bot starter kits (Python, C++, Go, Rust, Java) communicating via standard JSON lines over stdio.
- **docs/**: Formal specifications (Problem Math, Evaluation Protocol, Sandbox Security).

## Quickstart

### 1. Python Simulation SDK

```bash
pip install -e sdk

# List supported domains and registered problems
ideal-arena list

# Run official 9-baseline Axelrod tournament
ideal-arena baselines

# Benchmark a custom strategy against baselines
ideal-arena benchmark my_strategy.py
```

### 2. Terminal UI (TUI) Visualizer

Run the interactive keyboard-driven replay visualizer in your terminal:

```bash
cd server
go run cmd/tui/main.go
```

Controls:
- `Right / l`: Step forward
- `Left / h`: Step backward
- `Space`: Play / Pause auto-play
- `r`: Reset to round 0
- `1, 2, 3`: Change playback speed
- `q`: Quit

### 3. REST API & Judger Daemon

Start the Go judger backend:

```bash
cd server
go run cmd/server/main.go --port 8080
```

Available endpoints:
- `GET /api/v1/health` - Service health status
- `GET /api/v1/domains` - Active problem domains (`game_theory`, `optimization`, `simulation`)
- `GET /api/v1/problems` - Registered problem specifications
- `GET /api/v1/presets` - Bot presets
- `POST /api/v1/matches/simulate` - Execute pairwise match between bots
- `POST /api/v1/tournaments/simulate` - Run concurrent tournament

## Documentation Specifications

- **docs/axelrod/problem_spec.pdf**: Problem Specification (Document A) - Formal mathematical definition of Iterated Prisoner's Dilemma.
- **docs/axelrod/evaluation_spec.pdf**: Arena & Evaluation Specification (Document B) - Controller interfaces, match protocol, and tournament rules.
- **docs/platform/execution_sandbox_spec.pdf**: Platform Specification (Document C) - Sandbox isolation, resource limits, and security standards.
