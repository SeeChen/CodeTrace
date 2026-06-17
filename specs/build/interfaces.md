# Build Spec — Interfaces

> Stage 2. Frozen public API surface and hook contracts from `SA.md` §3. Coding must implement these shapes; do not redesign them.

## Public API

### `TraceFunc`

```python
class TraceFunc:
    @classmethod
    def config(cls, **options) -> None:
        """Set global tracing defaults. Unknown keys raise ValueError.

        Recognized options:
            enabled: bool = True
            logging: bool = True            # isolated-failure logging
            persistence: bool = True        # write artifacts
            summary: bool = True            # write summary.json at exit
            trace_root: str = ".codetrace"  # output root directory
            compare: CompareCallable | None = None   # default compare hook
            record: RecordBuilder | None = None      # default record builder
        Reserved (accepted, inert in MVP): metrics_collectors.
        """

    def __call__(
        self,
        *,
        new_function: Callable | None = None,
        compare: "CompareCallable | None" = None,
        record: "RecordBuilder | None" = None,
        **overrides,
    ) -> Callable:
        """Return a decorator. Per-call args shadow global config for this target only.

        new_function: when provided, enables compare mode (baseline vs candidate).
        overrides: same keys as config() (e.g. persistence=False) scoped to this target.
        """
```

**Decorated callable invariant:** identical signature, identical return value, identical exception propagation as the original. CodeTrace adds behavior around the call only.

## Hook Contracts (Contract layer)

### Record builder

```python
RecordBuilder = Callable[[dict], dict]
# context keys: name, type, time_start, time_end, duration,
#               compare_mode, compare_result, metrics
# returns: the record payload persisted to metadata.json and inlined into summary details.
```

### Compare callable

```python
CompareCallable = Callable[[Any, Any, dict], dict]
# (baseline_output, candidate_output, context) -> compare result dict
# Default impl returns: {"equal": bool, "baseline": <repr/serialized>, "candidate": <...>}
# Candidate-exception case (frozen): {"status": "candidate_error",
#                                     "exception_type": str, "message": str}
```

### Persistence interface

```python
class PersistenceAdapter(Protocol):
    def save_input(self, run_id: str, trace_name: str, payload: Any) -> None: ...
    def save_output(self, run_id: str, trace_name: str, payload: Any) -> None: ...
    def save_metadata(self, run_id: str, trace_name: str, record: dict) -> None: ...
    def save_compare(self, run_id: str, trace_name: str, result: dict) -> None: ...
    def save_summary(self, run_id: str, summary: dict) -> None: ...
```

The default adapter writes JSON under the schema in `artifact-schema.md`. All `save_*` calls are invoked inside the failure-isolation wrapper (see `failure-policy.md`).

### Metrics collector (reserved — not implemented in MVP)

```python
class MetricsCollector(Protocol):
    def start(self, context: dict) -> None: ...
    def stop(self, context: dict) -> None: ...
    def emit(self) -> dict: ...
```

Defined so the trace executor can later attach collectors without API change. No MVP code path invokes it.

## Internal Collaboration Contracts

- **Session:** `get_or_create_session(config) -> Session`; `Session.register(record: dict)`; `Session.run_id: str`; summary flush registered via `atexit`.
- **Trace executor → adapters:** only through `PersistenceAdapter` / `CompareCallable` / `RecordBuilder`. No concrete adapter import inside the executor.
- **Trace name resolution:** `paths.resolve_trace_name(run_id, qualname) -> str` applies the `__<n>` collision suffix.
