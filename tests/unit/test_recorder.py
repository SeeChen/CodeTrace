"""Unit tests for the record builder and summary aggregation."""

from codetrace.recorder import build_summary, default_record_builder


def test_default_record_builder_consumes_context():
    context = {
        "name": "f",
        "type": "function",
        "time_start": "t0",
        "time_end": "t1",
        "duration": 0.5,
        "compare_mode": True,
        "compare_result": {"equal": True},
        "metrics": {},
    }
    record = default_record_builder(context)
    assert record["name"] == "f"
    assert record["duration"] == 0.5
    assert record["compare_mode"] is True
    assert record["compare_result"] == {"equal": True}


def test_build_summary_inlines_records():
    records = [
        {"name": "f", "type": "function", "duration": 0.1, "time_start": "t0",
         "time_end": "t1", "compare_mode": False, "compare_result": {}, "metrics": {}},
    ]
    summary = build_summary("RUN", records)
    assert summary["run_id"] == "RUN"
    assert summary["total"] == 1
    assert summary["details"][0]["name"] == "f"
    assert summary["details"][0]["record"]["duration"] == 0.1
