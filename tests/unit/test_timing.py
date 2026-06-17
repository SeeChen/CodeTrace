"""Unit tests for the Timer utility."""

import re

from codetrace.util.timing import Timer


def test_timer_records_duration_and_timestamps():
    timer = Timer().start()
    timer.stop()
    assert timer.duration is not None and timer.duration >= 0
    iso = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    assert re.match(iso, timer.time_start)
    assert re.match(iso, timer.time_end)
