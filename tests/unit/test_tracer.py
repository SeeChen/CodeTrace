"""Unit tests for the tracer executor and TraceFunc."""

import json

import pytest

from codetrace import session
from codetrace.tracer import TraceFunc


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _trace_dir(root, suffix):
    """Return the single run's trace dir whose (sanitized) name ends with suffix."""
    run_id = session.current_session().run_id
    base = root / run_id
    matches = [p for p in base.iterdir() if p.is_dir() and p.name.endswith(suffix)]
    assert matches, f"no trace dir ending with {suffix!r} in {list(base.iterdir())}"
    return matches[0]


def test_return_value_unchanged(trace_root):
    trace = TraceFunc()

    @trace()
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    meta = _read(_trace_dir(trace_root, "add") / "metadata.json")
    assert meta["duration"] is not None
    assert meta["time_start"] and meta["time_end"]


def test_none_return_persisted(trace_root):
    trace = TraceFunc()

    @trace()
    def nothing():
        return None

    assert nothing() is None
    out = _read(_trace_dir(trace_root, "nothing") / "output.json")
    assert out["is_none"] is True


def test_user_exception_propagates_without_output(trace_root):
    trace = TraceFunc()

    @trace()
    def boom():
        raise KeyError("k")

    with pytest.raises(KeyError):
        boom()

    tdir = _trace_dir(trace_root, "boom")
    assert not (tdir / "output.json").exists()
    assert (tdir / "metadata.json").exists()  # metadata still attempted


def test_per_call_override_disables_persistence(trace_root):
    trace = TraceFunc()

    @trace(persistence=False)
    def quiet(x):
        return x

    assert quiet(1) == 1
    # No artifacts written: the run dir has no trace subdirectories.
    run_id = session.current_session().run_id
    run_dir = trace_root / run_id
    subdirs = [p for p in run_dir.iterdir() if p.is_dir()] if run_dir.exists() else []
    assert subdirs == []


def test_singleton_session_shared_across_instances(trace_root):
    trace_a = TraceFunc()
    trace_b = TraceFunc()

    @trace_a()
    def fa():
        return 1

    @trace_b()
    def fb():
        return 2

    fa()
    run_id_after_first = session.current_session().run_id
    fb()
    assert session.current_session().run_id == run_id_after_first


def test_trace_name_collision_creates_suffixed_dirs(trace_root):
    trace = TraceFunc()

    def make():
        @trace()
        def dup():
            return 1
        return dup

    make()()
    make()()
    run_id = session.current_session().run_id
    base = trace_root / run_id
    names = {p.name for p in base.iterdir() if p.is_dir()}
    assert any(n.endswith("dup") for n in names)
    assert any("dup__2" in n for n in names)


def test_persistence_failure_is_isolated(trace_root, monkeypatch):
    trace = TraceFunc()

    @trace()
    def f(x):
        return x

    # Force the output write to fail; user code must still return.
    from codetrace.adapters.persistence import JsonPersistenceAdapter

    def boom(self, *args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(JsonPersistenceAdapter, "save_output", boom)
    assert f(7) == 7

    meta = _read(_trace_dir(trace_root, "f") / "metadata.json")
    assert any(fl["subsystem"] == "persistence" for fl in meta.get("failures", []))


def test_custom_record_builder_used(trace_root):
    trace = TraceFunc()

    def builder(context):
        return {"name": context["name"], "custom": True}

    @trace(record=builder)
    def f():
        return 1

    f()
    meta = _read(_trace_dir(trace_root, "f") / "metadata.json")
    assert meta["custom"] is True
