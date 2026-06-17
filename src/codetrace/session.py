"""Module-level run session.

A single run session exists per process. It owns the ``run_id``, registers
trace records, resolves trace-name collisions, and flushes the run summary at
interpreter exit. All ``TraceFunc`` instances share this session.
"""

import atexit
from typing import List, Optional

from .contracts import PersistenceAdapter
from .recorder import build_summary
from .util import paths


class Session:
    """Holds run-wide tracing state for one process execution."""

    def __init__(self, config, adapter: PersistenceAdapter, logger) -> None:
        """Create a session, generating a fresh ``run_id``.

        Args:
            config: The effective configuration captured at session creation.
            adapter: The persistence adapter used for per-trace and summary writes.
            logger: Logger for isolated-failure reporting.
        """
        self.config = config
        self.adapter = adapter
        self.logger = logger
        self.run_id = paths.generate_run_id()
        self.records: List[dict] = []
        self.trace_names: set = set()
        self._summary_done = False

    def resolve_trace_name(self, qualname: str) -> str:
        """Assign and reserve a unique trace name for ``qualname``."""
        name = paths.resolve_trace_name(self.trace_names, qualname)
        self.trace_names.add(name)
        return name

    def register(self, record: dict) -> None:
        """Register a completed trace record."""
        self.records.append(record)

    def flush_summary(self) -> None:
        """Write the run summary once. Isolated; never raises."""
        if self._summary_done:
            return
        self._summary_done = True
        if not getattr(self.config, "summary", True):
            return
        try:
            summary = build_summary(self.run_id, self.records)
            self.adapter.save_summary(self.run_id, summary)
        except Exception as exc:  # noqa: BLE001 - summary failure must not escape at exit
            self.logger.warning("codetrace summary failure: %s", exc)


_SESSION: Optional[Session] = None


def get_or_create_session(config, adapter: PersistenceAdapter, logger) -> Session:
    """Return the process session, creating it on first use.

    The first caller fixes the run identity and adapter for the process;
    subsequent callers receive the same session.
    """
    global _SESSION
    if _SESSION is None:
        _SESSION = Session(config, adapter, logger)
    return _SESSION


def current_session() -> Optional[Session]:
    """Return the current session, or ``None`` if none exists yet."""
    return _SESSION


def flush() -> None:
    """Flush the current session summary, if any."""
    if _SESSION is not None:
        _SESSION.flush_summary()


def reset_session() -> None:
    """Drop the current session (primarily for tests)."""
    global _SESSION
    _SESSION = None


@atexit.register
def _atexit_flush() -> None:
    """Flush the summary at interpreter shutdown."""
    if _SESSION is not None:
        _SESSION.flush_summary()
