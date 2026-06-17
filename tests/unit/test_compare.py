"""Unit tests for the comparison coordinator and default compare."""

from codetrace.compare import default_compare, run_comparison


def test_default_compare_equal():
    result = default_compare(5, 5, {})
    assert result["equal"] is True


def test_default_compare_differs():
    result = default_compare(1, 2, {})
    assert result["equal"] is False
    assert result["baseline"] == 1
    assert result["candidate"] == 2


def test_run_comparison_uses_custom_compare():
    seen = {}

    def custom(baseline, candidate, context):
        seen["called"] = True
        return {"custom": True}

    result = run_comparison(10, lambda x: x, (10,), {}, custom, {})
    assert seen.get("called") is True
    assert result == {"custom": True}


def test_candidate_exception_is_compare_outcome():
    def boom(*args, **kwargs):
        raise ValueError("nope")

    result = run_comparison(1, boom, (1,), {}, default_compare, {})
    assert result["status"] == "candidate_error"
    assert result["exception_type"] == "ValueError"
    assert result["message"] == "nope"
