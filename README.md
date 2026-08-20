# Ideal Arena (Algorithm Arena)

**Ideal Arena** is a competitive algorithmic arena and multi-agent benchmark platform where developers, researchers, and AI agents design and submit autonomous strategies to compete, optimize, and solve complex decision-making problems.

---

## 📚 Specification Architecture

Ideal Arena enforces a strict **Three-Tier Specification Architecture** to separate mathematical game definitions from tournament matchmaking and platform execution infrastructure:

```
docs/
├── axelrod/                                # Problem: Iterated Prisoner's Dilemma
│   ├── problem_spec.tex / .pdf             # [Document A] Formal Problem Specification
│   └── evaluation_spec.tex / .pdf          # [Document B] Arena & Evaluation Specification
├── platform/                               # Platform-Wide Infrastructure Standard
│   └── execution_sandbox_spec.tex / .pdf   # [Document C] Execution & Sandboxing Specification
└── template/                               # Reusable Templates for Future Problems
    ├── problem_spec_template.tex / .pdf    # Template for Document A
    └── evaluation_spec_template.tex / .pdf # Template for Document B
```

### 1. Document A — Problem Specification
Defines the pure mathematical and domain-level specification of the problem (State space, Observation space, Action space, Transition dynamics, Payoff matrix, and Theoretical optimality bounds), independent of programming languages and platform runtimes.

* **Inaugural Problem:** [Axelrod IPD Problem Specification (PDF)](docs/axelrod/problem_spec.pdf)

### 2. Document B — Arena & Evaluation Specification
Defines how participant submissions are structured, matched, and scored:
* **Language-Neutral Controller Interface:** Standardized lifecycle (`initialize`, `reset`, `step`) with native adapters for:
  * 🐍 **Python 3**
  * ⚡ **C++ (C++17 / C++20)**
  * 🦀 **Rust**
  * ☕ **Java (Java 17 / 21 LTS)**
  * 🐹 **Go (Go 1.22+)**
* **Deterministic Reproducibility:** Hierarchical PRNG seeding (`Seed_match` $\to$ `Seed_controller`) guaranteeing 100% bitwise reproducible replays.
* **Match & Tournament Rules:** Fixed $T = 200$ rounds, full Round-Robin brackets, and Average Payoff Per Round ranking.

* **Inaugural Problem:** [Axelrod IPD Evaluation Specification (PDF)](docs/axelrod/evaluation_spec.pdf)

### 3. Document C — Execution & Sandbox Specification
Defines platform-wide zero-trust security and resource limits:
* **Linux Namespaces & Seccomp-BPF:** Hermetic containerization blocking forbidden syscalls (`fork`, `socket`, `ptrace`, `execve`).
* **Resource Quotas:** 1 vCPU (core pinned), $\le 256$ MB RAM, $\le 10$ ms/step, $\le 2.0$ s/match.
* **Driver-Worker IPC:** Low-latency Unix pipe / shared-memory communication with hardware monotonic watchdog.

* **Global Standard:** [Execution & Sandboxing Specification (PDF)](docs/platform/execution_sandbox_spec.pdf)

---

## 🛠️ Building Documentation from Source

To compile the LaTeX specifications locally:

```bash
# Compile Axelrod specifications
pdflatex -output-directory=docs/axelrod docs/axelrod/problem_spec.tex
pdflatex -output-directory=docs/axelrod docs/axelrod/evaluation_spec.tex

# Compile Platform specification
pdflatex -output-directory=docs/platform docs/platform/execution_sandbox_spec.tex

# Compile templates
pdflatex -output-directory=docs/template docs/template/problem_spec_template.tex
pdflatex -output-directory=docs/template docs/template/evaluation_spec_template.tex
```

---

## 📄 License
MIT License. Copyright (c) 2026 Arena Core Team.
