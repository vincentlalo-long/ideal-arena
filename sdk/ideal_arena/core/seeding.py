
from __future__ import annotations

import hashlib
import random
from contextlib import contextmanager
from typing import Generator

try:
    import numpy as np
except ImportError:
    np = None  


def derive_match_seed(
    tournament_seed: int,
    player_a: str,
    player_b: str,
    match_index: int = 0,
) -> int:
    payload = f"{tournament_seed}:{player_a}:{player_b}:{match_index}"
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], byteorder="big")


@contextmanager
def seed_context(seed: int | None) -> Generator[None, None, None]:
    if seed is None:
        yield
        return

    py_state = random.getstate()
    np_state = np.random.get_state() if np is not None else None

    try:
        random.seed(seed)
        if np is not None:
            np.random.seed(seed % (2**32 - 1))
        yield
    finally:
        random.setstate(py_state)
        if np is not None and np_state is not None:
            np.random.set_state(np_state)
