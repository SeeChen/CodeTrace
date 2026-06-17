"""Shared contracts for CodeTrace.

This module is the Contract layer. It must not import from the Core, Adapter,
or Utility layers so that any component can depend on it safely.
"""

from typing import Any, Callable, Protocol, runtime_checkable

# A record builder receives a runtime context dict and returns a record payload.
RecordBuilder = Callable[[dict], dict]

# A compare callable receives baseline output, candidate output, and a context
# dict, and returns a structured comparison result.
CompareCallable = Callable[[Any, Any, dict], dict]


@runtime_checkable
class PersistenceAdapter(Protocol):
    """Stable save interface for trace artifacts.

    Implementations own the concrete on-disk layout. Every method must be safe
    to call from within the failure-isolation wrapper used by the tracer.
    """

    def save_input(self, run_id: str, trace_name: str, payload: Any) -> None:
        """Persist the call inputs for one traced target."""

    def save_output(self, run_id: str, trace_name: str, payload: Any) -> None:
        """Persist the return value for one traced target."""

    def save_metadata(self, run_id: str, trace_name: str, record: dict) -> None:
        """Persist the per-trace record (timing, identity, failures)."""

    def save_compare(self, run_id: str, trace_name: str, result: dict) -> None:
        """Persist the comparison result for compare-mode traces."""

    def save_summary(self, run_id: str, summary: dict) -> None:
        """Persist the run-level summary aggregate."""


@runtime_checkable
class MetricsCollector(Protocol):
    """Reserved metrics-collector lifecycle.

    Defined so the tracer can attach collectors in a future release without an
    API change. No MVP code path invokes this protocol.
    """

    def start(self, context: dict) -> None:
        """Begin collecting metrics for a traced call."""

    def stop(self, context: dict) -> None:
        """Stop collecting metrics for a traced call."""

    def emit(self) -> dict:
        """Return the collected metrics payload."""
