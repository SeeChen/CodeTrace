"""Unit tests for path and identifier helpers."""

import re

from codetrace.util import paths


def test_run_id_is_file_safe_iso8601():
    run_id = paths.generate_run_id()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}", run_id)
    assert ":" not in run_id


def test_trace_name_collision_suffix():
    existing = set()
    first = paths.resolve_trace_name(existing, "mod.func")
    existing.add(first)
    second = paths.resolve_trace_name(existing, "mod.func")
    existing.add(second)
    third = paths.resolve_trace_name(existing, "mod.func")
    assert first == "mod.func"
    assert second == "mod.func__2"
    assert third == "mod.func__3"


def test_prepare_trace_dir_creates_tree(tmp_path):
    trace_dir = paths.prepare_trace_dir(str(tmp_path), "RUN", "trace")
    assert trace_dir.is_dir()
    assert trace_dir.name == "trace"
    assert trace_dir.parent.name == "RUN"
