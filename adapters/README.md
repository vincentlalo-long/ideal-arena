# Multi-Language Bot Starter Kits

This directory contains template starter kits for building competitive bots across multiple programming languages:

- `python/`: Python 3.10+
- `cpp/`: C++17
- `go/`: Go 1.21+
- `rust/`: Rust 2021
- `java/`: Java 17+

## Protocol Standard: `arena-agent/1`

All bot binaries speak **`arena-agent/1`** with the platform via `stdin` / `stdout`
JSON lines. `stdout` is reserved for protocol messages; logs must go to `stderr`.
Unknown message `type` values (including `end`) are ignored for forward compatibility.
Malformed JSON lines are ignored (and may be reported on `stderr`).

### Handshake

```
platform -> bot: {"type":"hello","protocol":"arena-agent/1","problem":"demo@1.0.0","seat":0,"limits":{"stepMs":10,"timeBankMs":200}}
bot -> platform: {"type":"ready","sdk":"python/0.2.0"}
```

### Reset (once per episode)

```
platform -> bot: {"type":"reset","episode":"ep_01J...","seed":8841236,"config":{"rounds":200}}
bot -> platform: {"type":"ack","episode":"ep_01J..."}
```

The starter calls `reset(seed)` — seed your RNG here and drop any per-episode state.

### Act (once per round)

```
platform -> bot: {"type":"act","t":0,"obs":{...}}
bot -> platform: {"type":"action","t":0,"action":<any JSON>}
```

- `obs` and `action` are **problem-defined JSON values**; their schemas live in each
  problem's specification, not in the adapter.
- The response must echo the request's `t`.

### End (no response expected)

```
platform -> bot: {"type":"end","episode":"ep_01J...","result":{...}}
```

## Strategy Contract

Each kit exposes the same problem-agnostic interface (aligned with the SDK `Agent`
protocol in `sdk/ideal_arena/agent.py`):

| Language | Interface |
|---|---|
| Python | `reset(seed)` / `act(observation) -> action` in `strategy.py` |
| C++ | `IStrategy::reset(seed)` / `IStrategy::act(observation)` in `strategy.hpp` |
| Go | `Strategy.Reset(seed)` / `Strategy.Act(observation)` in `strategy.go` |
| Rust | `Strategy::reset(seed)` / `Strategy::act(observation)` in `src/strategy.rs` |
| Java | `Strategy.reset(seed)` / `Strategy.act(observation)` in `Strategy.java` |
