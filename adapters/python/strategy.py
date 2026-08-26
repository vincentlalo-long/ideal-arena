class MyStrategy:
    def __init__(self) -> None:
        self.name = "MyBot"

    def reset(self) -> None:
        pass

    def step(self, history_self: list[int], history_opp: list[int]) -> int:
        if not history_opp:
            return 1
        return history_opp[-1]
