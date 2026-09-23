from typing import Any


class MyStrategy:
    def reset(self, seed: int | None = None) -> None:
        pass

    def act(self, observation: Any) -> Any:
        return None
