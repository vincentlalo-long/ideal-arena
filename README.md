# Ideal Arena

[![CI Pipeline](https://github.com/vincentlalo-long/ideal-arena/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentlalo-long/ideal-arena/actions)

Generic multi-agent episode framework. Early draft, core API still evolving.

## Core

`sdk/ideal_arena/` holds three files:

- `agent.py` — `Agent` protocol and `BaseAgent` (`reset(seed)`, `act(observation)`).
- `referee.py` — `Referee` ABC (`reset`, `validate_action`, `step`, `finalize`) plus `Transition` types.
- `engine.py` — `EpisodeRunner`, runs any referee with any agents.

## Install

```bash
pip install -e sdk
```

## Usage

```python
from ideal_arena import BaseAgent, EpisodeRunner, EpisodeSpec


class MyReferee(...): ...


class MyAgent(BaseAgent):
    def act(self, observation):
        ...


record = EpisodeRunner(MyReferee()).run([MyAgent()], EpisodeSpec(seed=0, max_steps=100))
print(record.result)
```
