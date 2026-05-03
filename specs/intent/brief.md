# CodeTrace Intent Brief

## Input Sources

- `docs/PRD.md`
- `docs/Workflow.md`

## Project Mission

CodeTrace is a lightweight, local-first Python tracing framework for developers who need structured, reproducible evidence while debugging, refactoring, and validating behavior changes.

The product should make it easy to instrument functions and methods without changing business logic semantics. It should capture execution metadata, persist runtime artifacts, compare baseline and candidate implementations, and generate reviewable reports.

## MVP Scope

The next milestone should focus on:

1. decorator-based tracing for functions and methods
2. input and output persistence
3. execution timing capture
4. structured summary generation
5. baseline versus candidate comparison
6. custom record and compare hooks
7. deterministic local artifact layout
8. infrastructure failure isolation
9. style and structure cleanup aligned with Google Python Style Guide

## Explicit Non-Goals

The immediate milestone excludes:

1. full A/B multi-variant execution
2. full replay-based self-regression workflow
3. memory usage collection as a shipped feature
4. web UI or remote observability features
5. production observability platform behavior
6. context-manager tracing as a required MVP implementation target

## Non-Negotiable Constraints

1. Python 3.10+ is the target runtime.
2. The MVP must remain local-first and file-system based.
3. The MVP should have zero external runtime dependencies.
4. Python standard library facilities should be preferred for timing, serialization, hashing, logging, and path handling.
5. Tracing must not silently change the return value of user code.
6. User-code exceptions must propagate unless a future explicit policy says otherwise.
7. Persistence, reporting, and comparison failures must be isolated from the main execution flow.
8. File-system outputs must be deterministic and organized by run and trace identity.
9. Public APIs must use stable, explicit signatures and clear naming.
10. Extension points must use small, explicit contracts instead of implicit shared state.
11. Public Python modules, classes, functions, and extension contracts must include Google-style docstrings.
12. Every core action must map to at least one unit or integration test.

## Deterministic File Schema

Runtime artifacts must use this default file-system topology:

```text
.codetrace/
└── <run_id>/
    ├── summary.json
    └── <trace_name>/
        ├── input.json
        ├── output.json
        ├── metadata.json
        └── compare.json
```

Directory and file expectations:

1. `<run_id>` identifies one program execution.
2. `<trace_name>` identifies one traced function, method, class method, or future block trace.
3. `input.json` stores serialized call arguments or deterministic fallback representations.
4. `output.json` stores serialized return data or deterministic fallback representations.
5. `metadata.json` stores timing, trace identity, execution status, and infrastructure error metadata.
6. `compare.json` stores baseline versus candidate comparison data when comparison is enabled.
7. `summary.json` aggregates run-level trace records.

## Failure Isolation Policy

Infrastructure failures must be isolated with explicit try-except encapsulation around persistence, reporting, and comparison work.

Required behavior:

1. User-code execution remains primary.
2. User-code return values must be preserved.
3. User-code exceptions must propagate normally.
4. Persistence, reporting, and comparison exceptions must not interrupt successful user-code execution.
5. Isolated infrastructure failures must be recorded through standard error (`stderr`), internal logging, or `metadata.json`.
6. Isolated failure records must include the failing subsystem, exception type, and message.
7. The MVP must not silently swallow infrastructure failures without recording evidence.

## MVP Decisions

These decisions reduce downstream ambiguity:

1. `run_id` defaults to an ISO 8601 timestamp safe for file names, such as `2026-05-04T10-30-00`.
2. Non-serializable values fall back to `repr(value)` in the MVP.
3. Comparison failures are recorded as artifacts and metadata by default, not raised, unless a future explicit strict mode is introduced.
4. Context-manager tracing remains a reserved extension path until function and method tracing are stable.
5. `pytest` is the preferred test framework unless the repository later standardizes on another runner.

## Core Entities

- Trace trigger: decorator, class decorator, or future context manager that starts tracing.
- Trace session: execution scope that hosts captured runtime data and future extension hooks.
- Trace record: normalized dictionary payload describing one traced execution.
- Persistence adapter: component responsible for saving inputs, outputs, metadata, and replay-ready artifacts.
- Comparison adapter: component responsible for comparing baseline and candidate outputs.
- Record builder: callable that receives runtime metadata and returns a trace record payload.
- Summary recorder: component that aggregates trace records and emits `summary.json`.
- Metrics collector: future optional lifecycle extension for resource metrics such as memory usage.

## Core Actions

1. Configure tracing defaults.
2. Decorate a function or method.
3. Execute traced user code without changing return semantics.
4. Capture timing and runtime metadata.
5. Persist inputs, outputs, metadata, and comparison artifacts.
6. Build a normalized trace record.
7. Aggregate and write a run-level summary report.
8. Compare baseline and candidate implementations when requested.
9. Isolate infrastructure failures from the user execution path.
10. Write runtime artifacts through the deterministic file schema unless explicitly configured otherwise.

## Contextual Awareness

Downstream AI agents should preserve these project-level expectations:

1. Treat this brief as the current single source of truth until architecture is generated.
2. Prefer explicit contracts, deterministic file names, and small adapter boundaries.
3. Keep generated code local-first and zero-dependency unless a later frozen decision changes that.
4. Use Google-style docstrings for public APIs and extension contracts.
5. Use `pytest` as the preferred test framework.
6. Ensure every core action has at least one corresponding unit or integration test.
7. Record unresolved choices explicitly instead of inventing hidden behavior.

## Acceptance Framing

The milestone is acceptable when:

1. traced functions preserve return values and exception behavior
2. inputs and outputs are written into the deterministic `.codetrace/<run_id>/<trace_name>/` schema
3. timing and trace metadata appear in `metadata.json` and the run-level summary
4. baseline/candidate comparison produces a structured `compare.json` result when enabled
5. custom record and compare callables can be injected without changing core tracing logic
6. infrastructure failures are reported without corrupting the main execution path
7. isolated infrastructure failures include subsystem, exception type, and message
8. core modules have direct unit coverage and important workflows have integration coverage
9. every core action has at least one `pytest` unit or integration test
10. public APIs and docstrings follow Google Python Style Guide expectations

## Open Questions

1. Should the first implementation reserve configuration fields for a future strict comparison mode?
2. Should `trace_name` sanitization preserve full dotted paths or normalize them into shorter file-system-safe names?
