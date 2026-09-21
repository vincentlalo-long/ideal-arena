from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Generic, Mapping, Sequence, TypeVar
from ideal_arena.agent import Agent
from ideal_arena.referee import AgentOutcome, AgentStatus, EpisodeContext, Referee, Transition


S = TypeVar("S")

@dataclass(frozen=True)
class EpisodeSpec:
    episode_id: str = ""
    seed: int = 0
    max_steps: int = 200
    config: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class Frame:
    step: int
    actions: Mapping[int, Any]
    statuses: Mapping[int, str]
    rewards: Sequence[float]


@dataclass
class EpisodeRecord:
    spec: EpisodeSpec
    frames: list[Frame]
    result: Mapping[str, Any]


class EpisodeRunner(Generic[S]):
    def __init__(self, referee: Referee[S]) -> None:
        self._referee = referee

    def run(self, agents: Sequence[Agent], spec: EpisodeSpec) -> EpisodeRecord:
        contex = EpisodeContext(
            episode_id=spec.episode_id,
            seed=spec.seed,
            config=spec.config,
            num_agents=len(agents),
            rng=random.Random(spec.seed),
        )
        transition = self._referee.reset(contex)
        self._reset_agents(agents, spec.seed)
        frames: list[Frame] = []
        state = transition.state

        for step in range(spec.max_steps):
            if transition.done:
                break
            outcomes = self._collect(agents, transition)
            frames.append(
                Frame(
                    step=step,
                    actions={o.seat: o.action for o in outcomes},
                    statuses={o.seat: o.status for o in outcomes},
                    rewards=list(transition.rewards),
                )
            )
            transition = self._referee.step(state, outcomes)
            state = transition.state

        return EpisodeRecord(spec=spec, frames=frames, result=self._referee.finalize(state))

    def _reset_agents(self, agents: Sequence[Agent], seed: int) -> None:
        rng = random.Random(seed)
        for agent in agents:
            agent.reset(rng.randint(0, 2**31 - 1))

    def _collect(self, agents: Sequence[Agent], transition: Transition[S]) -> list[AgentOutcome]:
        outcomes: list[AgentOutcome] = []
        for seat in transition.to_act:
            observation = transition.observations[seat]
            try:
                raw = agents[seat].act(observation)
            except Exception:
                outcomes.append(AgentOutcome(seat, AgentStatus.CRASH, self._referee.default_action))
                continue
            valid = self._referee.validate_action(seat, raw, transition.state)
            if valid is None:
                outcomes.append(AgentOutcome(seat, AgentStatus.INVALID, self._referee.default_action))
            else:
                outcomes.append(AgentOutcome(seat, AgentStatus.OK, valid))
        return outcomes
