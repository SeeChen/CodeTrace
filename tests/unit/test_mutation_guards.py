"""Assertion-hardening tests targeting surviving mutants (convergence round 3).

Round 2 measured 99% line coverage but only 64.5% mutation score: code was
executed but not actually asserted. These tests pin exact defaults, structures,
and failure shapes so that mutating the corresponding source logic makes at
least one test fail. See specs/audit/round-2.md and round-3.md.
"""

import json
import logging
import re

import pytest

from codetrace import tracer as tracer_mod
from codetrace.adapters.persistence import JsonPersistenceAdapter
from codetrace.compare import default_compare, run_comparison
from codetrace.config import ALLOWED_KEYS, Config
from codetrace.contracts import MetricsCollector, PersistenceAdapter
from codetrace.recorder import build_summary, default_record_builder
from codetrace.util import paths
from codetrace.util.logging_setup import get_logger
from codetrace.util.timing import Timer


class _RecLogger:
    """Logger stub that records warning calls."""

    def __init__(self):
        self.warnings = []

    def warning(self, *args, **kwargs):
        self.warnings.append((args, kwargs))


# ---- config.py --------------------------------------------------------------

def test_config_defaults_are_exact():
    cfg = Config()
    assert cfg.enabled is True
    assert cfg.logging is True
    assert cfg.persistence is True
    assert cfg.summary is True
    assert cfg.trace_root == ".codetrace"
    assert cfg.compare is None
    assert cfg.record is None
    assert cfg.metrics_collectors == ()


def test_allowed_keys_exact_membership():
    assert ALLOWED_KEYS == frozenset(
        {
            "enabled", "logging", "persistence", "summary",
            "trace_root", "compare", "record", "metrics_collectors",
        }
    )


def test_merge_rejects_unknown_key():
    with pytest.raises(ValueError):
        Config().merge(nope=1)


def test_merge_changes_only_target_key():
    cfg = Config().merge(enabled=False)
    assert cfg.enabled is False
    assert cfg.persistence is True
    assert cfg.trace_root == ".codetrace"


# ---- timing.py --------------------------------------------------------------

def test_timer_fresh_fields_are_none():
    t = Timer()
    assert t.time_start is None
    assert t.time_end is None
    assert t.duration is None


def test_timer_start_stop_return_self_and_set_fields():
    t = Timer()
    assert t.start() is t
    assert t.stop() is t
    assert isinstance(t.time_start, str)
    assert isinstance(t.time_end, str)
    assert isinstance(t.duration, float)
    assert t.duration >= 0.0


def test_timer_timestamps_are_iso_microseconds():
    t = Timer().start().stop()
    assert "T" in t.time_start
    assert re.search(r"\.\d{6}$", t.time_start)
    assert re.search(r"\.\d{6}$", t.time_end)


# ---- recorder.py ------------------------------------------------------------

def test_default_record_builder_full_context_is_verbatim():
    ctx = {
        "name": "f", "type": "function",
        "time_start": "s", "time_end": "e", "duration": 1.5,
        "compare_mode": True, "compare_result": {"equal": True},
        "metrics": {"m": 1},
    }
    assert default_record_builder(ctx) == ctx


def test_default_record_builder_defaults_for_missing_keys():
    rec = default_record_builder({})
    assert rec["name"] is None
    assert rec["type"] is None
    assert rec["duration"] is None
    assert rec["compare_mode"] is False
    assert rec["compare_result"] == {}
    assert rec["metrics"] == {}


def test_build_summary_structure_and_total():
    records = [
        {"name": "a", "type": "function", "duration": 0.1,
         "time_start": "s1", "time_end": "e1",
         "compare_mode": False, "compare_result": {}, "metrics": {}},
        {"name": "b", "type": "function", "duration": 0.2,
         "time_start": "s2", "time_end": "e2",
         "compare_mode": True, "compare_result": {"equal": False}, "metrics": {}},
    ]
    summary = build_summary("run-x", records)
    assert summary["run_id"] == "run-x"
    assert summary["total"] == 2
    assert len(summary["details"]) == 2
    d0 = summary["details"][0]
    assert d0["name"] == "a"
    assert d0["type"] == "function"
    assert d0["record"]["duration"] == 0.1
    assert d0["record"]["compare_mode"] is False
    assert summary["details"][1]["record"]["compare_result"] == {"equal": False}


def test_build_summary_empty_is_exact():
    assert build_summary("r", []) == {"run_id": "r", "total": 0, "details": []}


# ---- compare.py -------------------------------------------------------------

def test_default_compare_equal_true_is_exact():
    assert default_compare(3, 3, {}) == {"equal": True, "baseline": 3, "candidate": 3}


def test_default_compare_unequal():
    res = default_compare(1, 2, {})
    assert res["equal"] is False
    assert res["baseline"] == 1
    assert res["candidate"] == 2


def test_run_comparison_success_uses_compare_fn():
    res = run_comparison(10, lambda x: x, (10,), {}, default_compare, {})
    assert res == {"equal": True, "baseline": 10, "candidate": 10}


def test_run_comparison_candidate_error_shape():
    def boom(*a, **k):
        raise ValueError("bad")

    res = run_comparison(1, boom, (), {}, default_compare, {})
    assert res["status"] == "candidate_error"
    assert res["exception_type"] == "ValueError"
    assert res["message"] == "bad"


# ---- paths.py ---------------------------------------------------------------

def test_generate_run_id_format_has_no_colons():
    rid = paths.generate_run_id()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}", rid)
    assert ":" not in rid


def test_sanitize_replaces_only_illegal_chars():
    assert paths.sanitize("a<b>c:d") == "a_b_c_d"
    assert paths.sanitize("keep.OK-1_2") == "keep.OK-1_2"


def test_resolve_trace_name_collision_suffixes_increment():
    assert paths.resolve_trace_name(set(), "f") == "f"
    assert paths.resolve_trace_name({"f"}, "f") == "f__2"
    assert paths.resolve_trace_name({"f", "f__2"}, "f") == "f__3"
    assert paths.resolve_trace_name({"f", "f__2", "f__3"}, "f") == "f__4"


# ---- persistence.py ---------------------------------------------------------

def test_save_output_is_none_true(tmp_path):
    JsonPersistenceAdapter(str(tmp_path)).save_output("run", "trace", None)
    data = json.loads((tmp_path / "run" / "trace" / "output.json").read_text("utf-8"))
    assert data["is_none"] is True
    assert data["value"] is None


def test_save_output_is_none_false(tmp_path):
    JsonPersistenceAdapter(str(tmp_path)).save_output("run", "trace", 42)
    data = json.loads((tmp_path / "run" / "trace" / "output.json").read_text("utf-8"))
    assert data["is_none"] is False
    assert data["value"] == 42


# ---- logging_setup.py -------------------------------------------------------

def test_get_logger_name_level_and_handler():
    logger = get_logger()
    assert logger.name == "codetrace"
    assert logger.level == logging.WARNING
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)


def test_get_logger_is_idempotent_without_duplicate_handlers():
    a = get_logger()
    n = len(a.handlers)
    b = get_logger()
    assert a is b
    assert len(b.handlers) == n


# ---- contracts.py -----------------------------------------------------------

def test_runtime_checkable_persistence_adapter():
    assert isinstance(JsonPersistenceAdapter(), PersistenceAdapter)


def test_runtime_checkable_metrics_collector():
    class _M:
        def start(self, context):
            ...

        def stop(self, context):
            ...

        def emit(self):
            return {}

    assert isinstance(_M(), MetricsCollector)
    assert not isinstance(object(), MetricsCollector)


# ---- tracer.py --------------------------------------------------------------

def test_isolated_returns_value_on_success():
    failures = []
    out = tracer_mod._isolated("sub", lambda a, b: a + b, failures, _RecLogger(), 2, 3)
    assert out == 5
    assert failures == []


def test_isolated_records_exact_failure_dict_and_warns():
    failures = []
    logger = _RecLogger()

    def boom():
        raise ValueError("nope")

    out = tracer_mod._isolated("persistence", boom, failures, logger)
    assert out is None
    assert failures == [
        {"subsystem": "persistence", "exception_type": "ValueError", "message": "nope"}
    ]
    assert logger.warnings


def test_run_user_call_success_returns_result_and_no_exc():
    result, exc, timer = tracer_mod._run_user_call(lambda x: x * 2, (5,), {})
    assert result == 10
    assert exc is None
    assert isinstance(timer.duration, float)


def test_run_user_call_captures_exception_without_raising():
    def boom():
        raise KeyError("k")

    result, exc, timer = tracer_mod._run_user_call(boom, (), {})
    assert result is None
    assert isinstance(exc, KeyError)
    assert timer.time_end is not None


def test_maybe_compare_off_without_candidate():
    mode, res = tracer_mod._maybe_compare(
        Config(), None, None, 1, (), {}, "f", None, [], _RecLogger()
    )
    assert mode is False
    assert res == {}


def test_maybe_compare_off_when_user_raised():
    mode, res = tracer_mod._maybe_compare(
        Config(), lambda: 1, None, 1, (), {}, "f", ValueError("x"), [], _RecLogger()
    )
    assert mode is False
    assert res == {}


def test_maybe_compare_on_with_candidate_and_success():
    mode, res = tracer_mod._maybe_compare(
        Config(), lambda x: x, None, 5, (5,), {}, "f", None, [], _RecLogger()
    )
    assert mode is True
    assert res["equal"] is True
