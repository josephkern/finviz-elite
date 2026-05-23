import os
import threading
import time


DEFAULT_MIN_INTERVAL_S = 13.0
_ENV_VAR = "FINVIZ_MCP_MIN_INTERVAL_S"


class MinIntervalGate:
    """Block callers so consecutive entries are spaced at least ``min_interval`` seconds apart.

    Finviz Elite returns 429s under burst, and a 429 poisons the rest of a
    batch — so the server gates every outbound call on a single shared
    instance.
    """

    def __init__(self, min_interval: float) -> None:
        self._min_interval = min_interval
        self._lock = threading.Lock()
        self._last = 0.0

    @property
    def min_interval(self) -> float:
        return self._min_interval

    def wait(self) -> None:
        with self._lock:
            elapsed = time.monotonic() - self._last
            remaining = self._min_interval - elapsed
            if remaining > 0:
                time.sleep(remaining)
            self._last = time.monotonic()


def _load_interval() -> float:
    raw = os.getenv(_ENV_VAR)
    if not raw:
        return DEFAULT_MIN_INTERVAL_S
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{_ENV_VAR} must be a number, got {raw!r}") from exc
    if value < 0:
        raise ValueError(f"{_ENV_VAR} must be non-negative, got {value}")
    return value


gate = MinIntervalGate(_load_interval())
