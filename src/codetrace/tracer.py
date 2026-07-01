"""TraceFunc entry point and the trace executor.

The executor wires timing, persistence, comparison, and record building around
a user call while guaranteeing return transparency, exception transparency, and
failure isolation (see ``specs/build/failure-policy.md``).
"""

import functools
from typing import Any, Callable, List, Optional

from . import compare as compare_mod
from . import recorder as recorder_mod
from . import session as session_mod
from .adapters.persistence import JsonPersistenceAdapter
from .config import Config
from .contracts import CompareCallable, RecordBuilder
from .util.logging_setup import get_logger
from .util.timing import Timer


class _NullLogger:
    """No-op logger used when isolated-failure logging is disabled."""

    def warning(self, *args, **kwargs) -> None:  # noqa: D401 - trivial no-op
        """Discard the warning."""


class TraceFunc:
    """Primary tracing entry point.

    Configure global defaults with :meth:`config`, then use an instance as a
    decorator factory::

        trace = TraceFunc()

        @trace()
        def my_function(...):
            ...
    """

    _global_config = Config()

    @classmethod
    def config(cls, **options) -> None:
        """Update the global tracing configuration.

        Args:
            **options: Keys from :data:`codetrace.config.ALLOWED_KEYS`.

        Raises:
            ValueError: If any option key is unknown.
        """
        cls._global_config = cls._global_config.merge(**options)

    def __call__(
        self,
        *,
        new_function: Optional[Callable] = None,
        compare: Optional[CompareCallable] = None,
        record: Optional[RecordBuilder] = None,
        **overrides,
    ) -> Callable:
        """Return a decorator that traces the wrapped callable.

        Args:
            new_function: A candidate implementation; enables compare mode.
            compare: A compare callable overriding the configured/default one.
            record: A record builder overriding the configured/default one.
            **overrides: Per-call config overrides scoped to this target only.

        Returns:
            A decorator preserving the wrapped callable's signature and
            return/exception behavior.
        """
        effective = self._global_config.merge(**overrides)

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not effective.enabled:
                    return func(*args, **kwargs)
                return _execute(
                    func, args, kwargs, effective, new_function, compare, record
                )

            return wrapper

        return decorator


def _isolated(subsystem: str, fn: Callable, failures: List[dict], logger, *args, **kwargs) -> Any:
    """Run an infrastructure step, isolating and recording any failure.

    A broad ``except`` is intentional here: this is the failure-isolation
    boundary that keeps infrastructure errors from breaking user code.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - intentional isolation boundary
        failure = {
            "subsystem": subsystem,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
        failures.append(failure)
        logger.warning("codetrace %s failure: %s", subsystem, failure)
        return None


def _execute(
    func: Callable,
    args: tuple,
    kwargs: dict,
    cfg: Config,
    new_function: Optional[Callable],
    compare_override: Optional[CompareCallable],
    record_override: Optional[RecordBuilder],
) -> Any:
    """Execute and trace a single call. See module docstring for guarantees."""
    logger = get_logger() if cfg.logging else _NullLogger()
    session = session_mod.get_or_create_session(
        cfg, JsonPersistenceAdapter(cfg.trace_root), logger
    )
    adapter = session.adapter
    qualname: str = str(
        getattr(func, "__qualname__", None) or getattr(func, "__name__", "trace")
    )
    trace_name = session.resolve_trace_name(qualname)
    failures: List[dict] = []

    if cfg.persistence:
        input_payload = {"args": list(args), "kwargs": dict(kwargs)}
        _isolated(
            "persistence", adapter.save_input, failures, logger,
            session.run_id, trace_name, input_payload,
        )

    timer = Timer().start()
    user_exc: Optional[BaseException] = None
    result: Any = None
    try:
        result = func(*args, **kwargs)
    except Exception as exc:  # user code: captured to record, then re-raised intact
        user_exc = exc
    timer.stop()

    compare_mode = new_function is not None and user_exc is None
    compare_result: dict = {}
    if compare_mode:
        compare_fn = compare_override or cfg.compare or compare_mod.default_compare
        ctx = {"name": qualname, "type": "function"}
        compare_result = _isolated(
            "compare", compare_mod.run_comparison, failures, logger,
            result, new_function, args, kwargs, compare_fn, ctx,
        ) or {}

    if cfg.persistence and user_exc is None:
        _isolated(
            "persistence", adapter.save_output, failures, logger,
            session.run_id, trace_name, result,
        )
    if cfg.persistence and compare_mode and compare_result:
        _isolated(
            "persistence", adapter.save_compare, failures, logger,
            session.run_id, trace_name, compare_result,
        )

    context = {
        "name": qualname,
        "type": "function",
        "time_start": timer.time_start,
        "time_end": timer.time_end,
        "duration": timer.duration,
        "compare_mode": compare_mode,
        "compare_result": compare_result,
        "metrics": {},
    }
    builder = record_override or cfg.record or recorder_mod.default_record_builder
    record = _isolated("record", builder, failures, logger, context)
    if not isinstance(record, dict):
        record = recorder_mod.default_record_builder(context)
    if failures:
        record["failures"] = failures

    if cfg.persistence:
        _isolated(
            "persistence", adapter.save_metadata, failures, logger,
            session.run_id, trace_name, record,
        )
    session.register(record)

    if user_exc is not None:
        raise user_exc
    return result
