# Multi-Language Bot Starter Kits

This directory contains template starter kits for building competitive bots across multiple programming languages:

- `python/`: Python 3.10+
- `cpp/`: C++17
- `go/`: Go 1.21+
- `rust/`: Rust 2021
- `java/`: Java 17+

## Protocol Standard

All bot binaries communicate with the platform via `stdin` / `stdout` JSON lines:
- **Round step:** Input `{"command":"STEP", "history_self":[...], "history_opp":[...]}` -> Output `{"action": 1}`
- **Reset match:** Input `{"command":"RESET"}` -> Output `{"status": "OK"}`
