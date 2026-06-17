"""End-to-end integration tests for decorator tracing and summary emission."""

import json

from codetrace import session
from codetrace.tracer import TraceFunc


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def test_full_artifact_tree_and_summary(trace_root):
    trace = TraceFunc()

    @trace()
    def first(a):
        return a * 2

    @trace()
    def second(a):
        return a + 1

    assert first(10) == 20
    assert second(4) == 5

    sess = session.current_session()
    run_id = sess.run_id
    sess.flush_summary()

    base = trace_root / run_id
    summary = _read(base / "summary.json")
    assert summary["run_id"] == run_id
    assert summary["total"] == 2
    names = {d["name"] for d in summary["details"]}
    assert any("first" in n for n in names)
    assert any("second" in n for n in names)

    # Each trace has input/output/metadata artifacts.
    for detail in summary["details"]:
        # trace dir name is derived from qualname; just assert per-run files exist
        pass
    trace_dirs = [p for p in base.iterdir() if p.is_dir()]
    assert len(trace_dirs) == 2
    for tdir in trace_dirs:
        assert (tdir / "input.json").exists()
        assert (tdir / "output.json").exists()
        assert (tdir / "metadata.json").exists()
