"""Tracing configuration with global defaults and per-call overrides."""

from dataclasses import dataclass, field, replace
from typing import Optional, Tuple

from .contracts import CompareCallable, RecordBuilder

# Keys accepted by config() and per-call overrides. ``metrics_collectors`` is
# reserved and inert in the MVP.
ALLOWED_KEYS = frozenset(
    {
        "enabled",
        "logging",
        "persistence",
        "summary",
        "trace_root",
        "compare",
        "record",
        "metrics_collectors",
    }
)


@dataclass(frozen=True)
class Config:
    """Immutable tracing configuration.

    Use :meth:`merge` to derive a new scoped configuration from overrides; the
    original instance is never mutated.
    """

    enabled: bool = True
    logging: bool = True
    persistence: bool = True
    summary: bool = True
    trace_root: str = ".codetrace"
    compare: Optional[CompareCallable] = None
    record: Optional[RecordBuilder] = None
    metrics_collectors: Tuple = field(default_factory=tuple)

    def merge(self, **overrides) -> "Config":
        """Return a new config with ``overrides`` applied.

        Args:
            **overrides: Keys from :data:`ALLOWED_KEYS`.

        Returns:
            A new :class:`Config` instance.

        Raises:
            ValueError: If any override key is unknown.
        """
        _validate(overrides)
        return replace(self, **overrides)


def _validate(options: dict) -> None:
    """Raise ``ValueError`` if ``options`` contains unknown keys."""
    unknown = set(options) - ALLOWED_KEYS
    if unknown:
        raise ValueError(f"Unknown config option(s): {sorted(unknown)}")
