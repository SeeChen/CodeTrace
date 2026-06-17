# CodeTrace Intent Brief

> Stage 0 intent pack. Normalized from `docs/PRD.md`. This is the active single source of truth for downstream architecture work until `specs/architecture/SA.md` is frozen.

## Input Sources

1. `docs/PRD.md` (CodeTrace PRD v1.0, the product-level source of truth)
2. `docs/Workflow.md` (stage definitions)
3. `.claude/memory/open-questions.md` (requirement-layer open questions)

## Project Mission

Provide a lightweight, local-first, zero-dependency Python tracing framework that lets developers observe function execution, persist runtime artifacts, and validate behavioral consistency during refactoring — without changing the semantics of traced user code.

The architecture must preserve a clean path toward future A/B comparison, replay-based self-regression, and runtime metrics, even though those are out of MVP scope.

## MVP Scope

1. Function and method tracing via decorator-based instrumentation (FR-01).
2. Input and output persistence under a stable serialization contract (FR-02).
3. Timing capture for each traced call (FR-01).
4. Structured summary generation at process exit (FR-03).
5. Baseline vs candidate comparison under the same input set (FR-04).
6. Custom record-builder and compare hooks (FR-05, FR-06).
7. Global configuration plus per-call overrides (FR-07).
8. Storage/serialization isolated from the tracing engine (FR-10).
9. Google Python Style Guide compliance for all shipped code.

## Explicit Non-Goals

1. Full multi-variant A/B execution engine (FR-11 keeps the path open only).
2. Full replay-based self-regression workflow (FR-12 keeps artifacts replay-friendly only).
3. Memory / resource metrics as a shipped feature (FR-13 reserves extension points only).
4. Web UI or remote observability.
5. Production observability platform behavior.
6. Block-level (`with`) tracing and class-decorator tracing as shipped MVP features — reserved extension paths (see MVP Decisions).

## Non-Negotiable Constraints

1. Python 3.10+ target runtime.
2. MVP is local-first and file-system based.
3. Zero external runtime dependencies for the MVP; prefer the standard library for timing, serialization, hashing, and logging.
4. Any future dependency must be justified and isolated behind an adapter boundary.
5. Traced user code must never have its return value silently changed.
6. User-code exceptions must propagate unless a future explicit policy handles them.
7. Core tracing orchestration must stay separate from serialization, comparison, reporting, and metrics.
8. Hook/adapter interfaces must be small, explicit contracts — not implicit shared state.
9. Google-style docstrings on all public APIs and extension contracts; `snake_case` modules; no manual alignment of parameters/assignments.

## Deterministic File Schema

Default artifact topology (used unless a frozen decision changes it):

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

- `<run_id>` — one program execution; ISO 8601 timestamp safe for file names (e.g. `2026-05-04T10-30-00`).
- `<trace_name>` — one traced target (function/method) within the run.
- `input.json` — serialized call inputs (args/kwargs) for that trace.
- `output.json` — serialized return value for that trace.
- `metadata.json` — timing, run identity, compare mode flag, and any isolated-failure records.
- `compare.json` — structured comparison result when compare mode is active.
- `summary.json` — run-level aggregate: `run_id`, total trace count, and per-trace details (matches the PRD output schema).

## Failure Isolation Policy

1. User-code execution is primary and must complete on its own merits.
2. User-code exceptions propagate normally.
3. Persistence, reporting, and comparison exceptions are wrapped in try-except encapsulation.
4. An isolated infrastructure failure must not interrupt successful user-code execution.
5. Isolated failures are recorded via `stderr`, internal logging, or `metadata.json`.
6. Each failure record includes subsystem, exception type, and message.
7. Infrastructure failures must never be silently swallowed.

## MVP Decisions

Resolved from the PRD with conservative defaults to reduce downstream ambiguity:

1. `run_id` defaults to a file-name-safe ISO 8601 timestamp (e.g. `2026-05-04T10-30-00`).
2. Non-serializable values fall back to `repr(value)`.
3. Comparison failures are recorded as artifacts/metadata by default, not raised, unless a future explicit strict mode is introduced.
4. Context-manager (`with`) tracing and class-decorator tracing remain reserved extension paths until function and method tracing are stable.
5. Serialization format is JSON for all artifacts (`*.json`), consistent with the file schema and the PRD output schema.

## Core Entities

1. `TraceFunc` — primary tracing entry; holds global config and produces the decorator.
2. Trace session / run — the unit of one program execution, owning a `run_id`.
3. Trace record — normalized per-call payload (timing, identity, compare result, metrics slot).
4. Record builder (hook) — accepts runtime metadata, returns a dict record payload.
5. Compare callable (hook) — accepts comparable outputs, returns a dict comparison result.
6. Persistence adapter — stable save interface for inputs/outputs/future replay assets.
7. Summary recorder — aggregates trace records and writes `summary.json` at exit.
8. Metrics collector (reserved) — future lifecycle hooks: start, stop, emit.

## Core Actions

1. Configure tracing defaults — `TraceFunc.config(...)`.
2. Decorate and trace a function/method — capture inputs, outputs, timing, summary.
3. Persist inputs and outputs to the run/trace directory.
4. Run baseline vs candidate and emit a structured comparison result.
5. Inject a custom compare callable without touching core flow.
6. Inject a custom record builder without touching core flow.
7. Aggregate all records and write the run summary at process exit.

Every core action must map to at least one unit or integration test downstream.

## Contextual Awareness

Guidance for downstream AI stages (reduce hallucination):

1. Treat this brief as the single source of truth until `SA.md` is generated.
2. Prefer explicit contracts, deterministic file names, and small adapter boundaries.
3. Keep generated code local-first and zero-dependency unless a later frozen decision changes that.
4. Require Google-style docstrings for public Python APIs and extension contracts.
5. Prefer `pytest` unless the repository standardizes on another runner.
6. Require every core action to map to at least one unit or integration test.
7. Do not implement reserved extension paths (A/B engine, replay, metrics, `with`/class tracing) as shipped MVP features; only preserve clean seams for them.

## Acceptance Framing

The MVP is acceptable when:

1. A decorated function runs with unchanged return semantics while timing and trace metadata are recorded (FR-01).
2. Inputs and outputs are written to an isolated per-run/per-trace directory using the deterministic schema (FR-02, FR-10).
3. A `summary.json` is produced at process exit with total count and per-trace details (FR-03).
4. Baseline vs candidate comparison emits a structured `compare.json` result for the same inputs (FR-04).
5. Custom compare and record-builder hooks can replace defaults without core changes (FR-05, FR-06).
6. Global config and per-call overrides work without modifying business code (FR-07).
7. Mandatory edge cases are covered: raising functions, `None` returns, non-serializable I/O, missing/invalid output dirs, differing compare outputs, multiple traced functions in one process.
8. Core-module line coverage is above 90% and all public APIs/contracts have direct tests.
9. Infrastructure failures (persistence/report/compare) are isolated and recorded, never breaking user code.

## Open Questions

1. Default value of the trace root directory name — assumed `.codetrace/` per the file schema; confirm during architecture if a configurable root changes the default.
2. Whether `metadata.json` and the per-call timing also need to be inlined into `summary.json` details, or referenced only — to be decided when the summary schema is frozen in `SA.md`.
3. Scope of "public methods" for future class tracing (dunder handling, inherited methods) — deferred until class tracing leaves the reserved state.
