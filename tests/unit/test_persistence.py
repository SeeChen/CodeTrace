"""Unit tests for the JSON persistence adapter."""

import json

from codetrace.adapters.persistence import JsonPersistenceAdapter


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def test_save_input_output_under_run_trace_dir(tmp_path):
    adapter = JsonPersistenceAdapter(str(tmp_path))
    adapter.save_input("RUN", "tr", {"args": [1], "kwargs": {"k": 2}})
    adapter.save_output("RUN", "tr", "value")

    base = tmp_path / "RUN" / "tr"
    assert _read(base / "input.json") == {"args": [1], "kwargs": {"k": 2}}
    assert _read(base / "output.json") == {"value": "value", "is_none": False}


def test_save_output_none_flags_is_none(tmp_path):
    adapter = JsonPersistenceAdapter(str(tmp_path))
    adapter.save_output("RUN", "tr", None)
    out = _read(tmp_path / "RUN" / "tr" / "output.json")
    assert out["is_none"] is True


def test_save_summary_at_run_level(tmp_path):
    adapter = JsonPersistenceAdapter(str(tmp_path))
    adapter.save_summary("RUN", {"run_id": "RUN", "total": 0, "details": []})
    assert _read(tmp_path / "RUN" / "summary.json")["total"] == 0


def test_non_serializable_payload_uses_repr(tmp_path):
    class Widget:
        def __repr__(self):
            return "<Widget>"

    adapter = JsonPersistenceAdapter(str(tmp_path))
    adapter.save_output("RUN", "tr", Widget())
    out = _read(tmp_path / "RUN" / "tr" / "output.json")
    assert out["value"] == "<Widget>"
