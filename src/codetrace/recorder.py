"""Default record builder and summary aggregation."""

from typing import List


def default_record_builder(context: dict) -> dict:
    """Build a normalized trace record from a runtime context.

    Args:
        context: Runtime metadata with keys ``name``, ``type``, ``time_start``,
            ``time_end``, ``duration``, ``compare_mode``, ``compare_result``,
            and ``metrics``.

    Returns:
        The record payload persisted to ``metadata.json`` and inlined into the
        run summary.
    """
    return {
        "name": context.get("name"),
        "type": context.get("type"),
        "time_start": context.get("time_start"),
        "time_end": context.get("time_end"),
        "duration": context.get("duration"),
        "compare_mode": context.get("compare_mode", False),
        "compare_result": context.get("compare_result", {}),
        "metrics": context.get("metrics", {}),
    }


def build_summary(run_id: str, records: List[dict]) -> dict:
    """Aggregate trace records into the run-level summary payload.

    Each record is inlined under ``details[].record`` (matching the PRD output
    schema); ``metadata.json`` remains the authoritative per-trace artifact.

    Args:
        run_id: The run identifier.
        records: The trace records registered during the run.

    Returns:
        The summary payload written to ``summary.json``.
    """
    details = []
    for record in records:
        details.append(
            {
                "name": record.get("name"),
                "type": record.get("type"),
                "record": {
                    "duration": record.get("duration"),
                    "time_start": record.get("time_start"),
                    "time_end": record.get("time_end"),
                    "compare_mode": record.get("compare_mode", False),
                    "compare_result": record.get("compare_result", {}),
                    "metrics": record.get("metrics", {}),
                },
            }
        )
    return {"run_id": run_id, "total": len(records), "details": details}
