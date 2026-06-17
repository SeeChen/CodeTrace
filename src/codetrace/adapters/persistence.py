"""Default JSON persistence adapter.

This is the only module that knows the concrete on-disk artifact layout
described in ``specs/build/artifact-schema.md``.
"""

import json
from pathlib import Path
from typing import Any

from ..util import paths
from ..util.serialization import safe_to_jsonable


class JsonPersistenceAdapter:
    """Write trace artifacts as JSON files under a run/trace directory tree.

    Implements the :class:`codetrace.contracts.PersistenceAdapter` protocol.
    """

    def __init__(self, root: str = ".codetrace") -> None:
        """Create an adapter rooted at ``root`` (default ``.codetrace``)."""
        self.root = root

    def save_input(self, run_id: str, trace_name: str, payload: Any) -> None:
        """Write ``input.json`` for one traced target."""
        trace_dir = paths.prepare_trace_dir(self.root, run_id, trace_name)
        self._write(trace_dir / "input.json", safe_to_jsonable(payload))

    def save_output(self, run_id: str, trace_name: str, payload: Any) -> None:
        """Write ``output.json`` (value plus ``is_none`` flag)."""
        trace_dir = paths.prepare_trace_dir(self.root, run_id, trace_name)
        self._write(
            trace_dir / "output.json",
            {"value": safe_to_jsonable(payload), "is_none": payload is None},
        )

    def save_metadata(self, run_id: str, trace_name: str, record: dict) -> None:
        """Write ``metadata.json``, the authoritative per-trace record."""
        trace_dir = paths.prepare_trace_dir(self.root, run_id, trace_name)
        self._write(trace_dir / "metadata.json", safe_to_jsonable(record))

    def save_compare(self, run_id: str, trace_name: str, result: dict) -> None:
        """Write ``compare.json`` for a compare-mode trace."""
        trace_dir = paths.prepare_trace_dir(self.root, run_id, trace_name)
        self._write(trace_dir / "compare.json", safe_to_jsonable(result))

    def save_summary(self, run_id: str, summary: dict) -> None:
        """Write the run-level ``summary.json``."""
        run_dir = paths.prepare_run_dir(self.root, run_id)
        self._write(run_dir / "summary.json", safe_to_jsonable(summary))

    @staticmethod
    def _write(path: Path, data: Any) -> None:
        """Serialize ``data`` to ``path`` as indented UTF-8 JSON."""
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
