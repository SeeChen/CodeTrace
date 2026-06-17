"""Monotonic timing with ISO 8601 wall-clock timestamps."""

import time
from datetime import datetime


class Timer:
    """Measure the duration of a traced call.

    ``duration`` is computed from a monotonic clock; ``time_start`` and
    ``time_end`` are ISO 8601 wall-clock timestamps for human inspection.
    """

    def __init__(self) -> None:
        self.time_start: str | None = None
        self.time_end: str | None = None
        self.duration: float | None = None
        self._start_perf: float | None = None

    def start(self) -> "Timer":
        """Record the start time and return self."""
        self.time_start = datetime.now().isoformat(timespec="microseconds")
        self._start_perf = time.perf_counter()
        return self

    def stop(self) -> "Timer":
        """Record the end time and compute the duration; return self."""
        if self._start_perf is not None:
            self.duration = time.perf_counter() - self._start_perf
        self.time_end = datetime.now().isoformat(timespec="microseconds")
        return self
