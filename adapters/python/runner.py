import json
import sys
from strategy import MyStrategy


def main() -> None:
    bot = MyStrategy()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        cmd = req.get("command", "STEP")
        if cmd == "RESET":
            bot.reset()
            sys.stdout.write(json.dumps({"status": "OK"}) + "\n")
            sys.stdout.flush()
        elif cmd == "STEP":
            hist_self = req.get("history_self", [])
            hist_opp = req.get("history_opp", [])
            action = bot.step(hist_self, hist_opp)
            sys.stdout.write(json.dumps({"action": int(action)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
