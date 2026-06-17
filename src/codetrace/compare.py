"""Comparison coordinator and default compare callable."""

from typing import Any, Callable

from .util.serialization import safe_to_jsonable


def default_compare(baseline: Any, candidate: Any, context: dict) -> dict:
    """Compare two outputs for equality.

    Args:
        baseline: The baseline output.
        candidate: The candidate output.
        context: Runtime context (unused by the default implementation).

    Returns:
        A dict with ``equal`` plus serialized ``baseline`` and ``candidate``.
    """
    return {
        "equal": bool(baseline == candidate),
        "baseline": safe_to_jsonable(baseline),
        "candidate": safe_to_jsonable(candidate),
    }


def run_comparison(
    baseline_output: Any,
    candidate_callable: Callable,
    args: tuple,
    kwargs: dict,
    compare_fn: Callable[[Any, Any, dict], dict],
    context: dict,
) -> dict:
    """Run the candidate under the same inputs and compare against the baseline.

    The coordinator does not assume exactly one candidate at the type level, so
    a future multi-variant A/B mode can reuse the same compare contract.

    If the candidate raises, the failure is recorded as a comparison result
    (``status: "candidate_error"``) rather than an infrastructure failure; the
    baseline result is unaffected.

    Args:
        baseline_output: The already-computed baseline output.
        candidate_callable: The candidate implementation to run.
        args: Positional arguments to replay.
        kwargs: Keyword arguments to replay.
        compare_fn: The compare callable to apply on success.
        context: Runtime context passed to ``compare_fn``.

    Returns:
        A structured comparison result.
    """
    try:
        candidate_output = candidate_callable(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - candidate failure is a compare outcome
        return {
            "status": "candidate_error",
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
    return compare_fn(baseline_output, candidate_output, context)
