import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strategy import MyStrategy

SDK = "python/0.2.0"


def send(message: dict) -> None:
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def main() -> None:
    bot = MyStrategy()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            print("arena-agent: ignoring malformed line", file=sys.stderr)
            continue
        if not isinstance(msg, dict):
            continue

        msg_type = msg.get("type")
        if msg_type == "hello":
            send({"type": "ready", "sdk": SDK})
        elif msg_type == "reset":
            bot.reset(msg.get("seed"))
            send({"type": "ack", "episode": msg.get("episode") or ""})
        elif msg_type == "act":
            action = bot.act(msg.get("obs"))
            send({"type": "action", "t": msg.get("t", 0), "action": action})


if __name__ == "__main__":
    main()
