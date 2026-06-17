"""End-to-end integration tests for compare-mode tracing."""

import json

from codetrace import session
from codetrace.tracer import TraceFunc


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _compare_file(trace_root):
    run_id = session.current_session().run_id
    base = trace_root / run_id
    tdir = next(p for p in base.iterdir() if p.is_dir())
    return tdir / "compare.json"


def test_compare_equal(trace_root):
    trace = TraceFunc()

    def candidate(x):
        return x * 2

    @trace(new_function=candidate)
    def baseline(x):
        return x + x

    assert baseline(5) == 10
    result = _read(_compare_file(trace_root))
    assert result["equal"] is True


def test_compare_differs(trace_root):
    trace = TraceFunc()

    def candidate(x):
        return x + 1

    @trace(new_function=candidate)
    def baseline(x):
        return x

    assert baseline(5) == 5
    result = _read(_compare_file(trace_root))
    assert result["equal"] is False


def test_candidate_error_recorded(trace_root):
    trace = TraceFunc()

    def candidate(x):
        raise RuntimeError("candidate failed")

    @trace(new_function=candidate)
    def baseline(x):
        return x

    # Baseline result is returned normally despite candidate failure.
    assert baseline(3) == 3
    result = _read(_compare_file(trace_root))
    assert result["status"] == "candidate_error"
    assert result["exception_type"] == "RuntimeError"
