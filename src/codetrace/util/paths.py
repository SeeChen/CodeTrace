"""Deterministic path and identifier helpers."""

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

_ILLEGAL = re.compile(r"[^A-Za-z0-9._-]")


def generate_run_id() -> str:
    """Return a file-name-safe ISO 8601 timestamp, e.g. ``2026-05-04T10-30-00``."""
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")


def sanitize(name: str) -> str:
    """Replace characters that are unsafe in path components with ``_``."""
    return _ILLEGAL.sub("_", name)


def resolve_trace_name(existing: Iterable[str], qualname: str) -> str:
    """Return a unique trace name within a run.

    The first occurrence of a name is used as-is (after sanitizing). Repeated
    names get a ``__<n>`` suffix starting at ``__2``.

    Args:
        existing: Trace names already assigned in the current run.
        qualname: The function qualified name to derive the trace name from.

    Returns:
        A trace name not present in ``existing``.
    """
    existing = set(existing)
    base = sanitize(qualname)
    if base not in existing:
        return base
    index = 2
    while f"{base}__{index}" in existing:
        index += 1
    return f"{base}__{index}"


def prepare_run_dir(root: str, run_id: str) -> Path:
    """Create and return the run-level directory ``<root>/<run_id>``."""
    path = Path(root) / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def prepare_trace_dir(root: str, run_id: str, trace_name: str) -> Path:
    """Create and return the trace-level directory ``<root>/<run_id>/<trace_name>``."""
    path = Path(root) / run_id / trace_name
    path.mkdir(parents=True, exist_ok=True)
    return path
