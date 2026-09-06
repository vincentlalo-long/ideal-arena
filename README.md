# Ideal Arena

[![CI Pipeline](https://github.com/vincentlalo-long/ideal-arena/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentlalo-long/ideal-arena/actions)

Ideal Arena is a high-performance competitive platform for algorithmic strategy development, multi-agent game theory simulations, and tournament benchmarking.

## Repository Architecture

- **docs/**: 3-tier formal specifications (Problem Math, Evaluation Protocol, Sandbox Security).
- **sdk/**: Python SDK, deterministic PRNG match runner, round-robin tournament engine, and CLI.
- **adapters/**: Multi-language bot starter kits (Python, C++, Go, Rust, Java) communicating via standard JSON lines over stdio.
- **server/**: Go backend platform featuring a sandboxed subprocess judger with a 10ms watchdog timer, REST API, and an interactive Terminal UI (TUI).
- **frontend/**: Modern React, TypeScript, and Tailwind CSS web application for match replay visualization and tournament leaderboards.

## Quickstart

### 1. Python Simulation SDK

```bash
pip install -e sdk

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

### 3. Web Visualizer & REST API

Start the Go judger backend:

```bash
cd server
go run cmd/server/main.go --port 8080
```

Start the React web visualizer:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 to interact with the visualizer.

## Documentation Specifications

- **docs/axelrod/problem_spec.pdf**: Problem Specification (Document A) - Formal mathematical definition of Iterated Prisoner's Dilemma.
- **docs/axelrod/evaluation_spec.pdf**: Arena & Evaluation Specification (Document B) - Controller interfaces, match protocol, and tournament rules.
- **docs/platform/execution_sandbox_spec.pdf**: Platform Specification (Document C) - Sandbox isolation, resource limits, and security standards.
