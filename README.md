# Ideal Arena

Ideal Arena is a competitive platform for algorithmic strategy development, optimization, and multi-agent tournament benchmarking.

## Documentation Architecture

The repository separates problem specifications from evaluation protocols and platform execution:

- **docs/axelrod/problem_spec.pdf**: Problem Specification (Document A) - Formal mathematical definition of Iterated Prisoner's Dilemma.
- **docs/axelrod/evaluation_spec.pdf**: Arena & Evaluation Specification (Document B) - Controller interfaces (Python, C++, Rust, Java, Go), match protocol, and tournament rules.
- **docs/platform/execution_sandbox_spec.pdf**: Platform Specification (Document C) - Sandbox isolation, resource limits, and security standards.
- **docs/template/**: Reusable templates for future problems.

## Building Documentation

To compile the LaTeX specifications locally:

```bash
# Axelrod IPD
pdflatex -output-directory=docs/axelrod docs/axelrod/problem_spec.tex
pdflatex -output-directory=docs/axelrod docs/axelrod/evaluation_spec.tex

# Platform
pdflatex -output-directory=docs/platform docs/platform/execution_sandbox_spec.tex

# Templates
pdflatex -output-directory=docs/template docs/template/problem_spec_template.tex
pdflatex -output-directory=docs/template docs/template/evaluation_spec_template.tex
```
