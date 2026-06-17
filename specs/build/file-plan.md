# Build Spec — File Plan

> Stage 2. Maps modules (`module-map.md`) to concrete files. This is the file ownership coding must follow.

## Package Layout

```text
src/
└── codetrace/
    ├── __init__.py            # public exports: TraceFunc (+ default hooks for advanced use)
    ├── contracts.py           # Protocols + type aliases (RecordBuilder, CompareCallable,
    │                          #   PersistenceAdapter, MetricsCollector) + record/summary shapes
    ├── config.py              # Config dataclass, defaults, key validation, override merge
    ├── session.py             # module-level run session: run_id, record registry, atexit summary
    ├── tracer.py              # TraceFunc: config() + __call__() decorator + trace executor
    ├── compare.py             # compare coordinator + default_compare
    ├── recorder.py            # default_record_builder + summary aggregation
    └── adapters/
        ├── __init__.py
        └── persistence.py     # JsonPersistenceAdapter (default PersistenceAdapter impl)
    └── util/
        ├── __init__.py
        ├── serialization.py   # safe_to_jsonable(value) with repr() fallback
        ├── paths.py           # run_id gen, path prep, resolve_trace_name (collision suffix)
        ├── timing.py          # Timer / monotonic duration + ISO 8601 timestamps
        └── logging_setup.py   # get_logger() for isolated-failure reporting

tests/
├── conftest.py               # tmp trace_root fixture, reset session fixture
├── unit/
│   ├── test_serialization.py
│   ├── test_paths.py
│   ├── test_timing.py
│   ├── test_config.py
│   ├── test_persistence.py
│   ├── test_compare.py
│   ├── test_recorder.py
│   └── test_tracer.py
└── integration/
    ├── test_decorator_end_to_end.py
    └── test_compare_end_to_end.py
```

## File Ownership Notes

- `__init__.py` exposes `TraceFunc` as the single primary import; default hooks are importable for users who want to wrap them.
- `contracts.py` imports nothing from Core/Adapter/Utility (keeps the Contract layer dependency-free).
- `tracer.py` imports adapters/compare/recorder **only through contract types** at call time (constructor injection or config), preserving the frozen layer rule.
- `adapters/persistence.py` is the only file allowed to know the on-disk JSON layout.
- `util/*` files hold no trace state.

## Out of Scope Files (reserved seams, not created in MVP)

- `tracer.py` block/class trigger surfaces, `adapters/` alternate stores, and any metrics collector module — defined as seams in `interfaces.md`, not implemented now.
