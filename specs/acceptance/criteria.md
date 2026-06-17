# Milestone Acceptance Criteria — CodeTrace MVP

> Stage 6 standards document. Derived from `docs/PRD.md`, `specs/intent/brief.md`, `specs/build/*`, and `specs/build/test-matrix.md`. Defines what must be true for the MVP milestone to be accepted. The pass/fail evaluation lives in `report.md`.

## Milestone Scope

The function-tracing MVP of CodeTrace: decorator-based function/method tracing with input/output persistence, timing, run summary, baseline-vs-candidate comparison, custom record/compare hooks, global + per-call configuration, and a storage layer isolated from the tracing engine — all local-first and zero-dependency.

In scope: PRD Appendix "In scope for the next milestone" items 1–7 (function/method tracing, I/O persistence, timing, summary, comparison, custom hooks, style/structure compliance).

## Blocking Acceptance Gates

A gate must hold for acceptance. Each cites its required evidence.

| Gate | Requirement | Required evidence |
| --- | --- | --- |
| **G1 — Functional** | FR-01–FR-07 and FR-10 are implemented and behave per their PRD acceptance criteria. | Passing tests mapped to each FR in the verification report. |
| **G2 — Return/exception transparency** | Traced calls return exactly the original value; user exceptions propagate unchanged. | Tests for unchanged return and exception propagation. |
| **G3 — Failure isolation** | Persistence/compare/record failures are caught, recorded (`subsystem`/`type`/`message`), and never break a successful user call or get silently swallowed. | Forced-failure test showing user return intact + recorded `failures`. |
| **G4 — Deterministic artifacts** | On-disk topology matches `artifact-schema.md`; `run_id` is a file-safe ISO 8601 timestamp; non-serializable values fall back to `repr`. | Persistence/paths/serialization tests + integration artifact-tree assertions. |
| **G5 — Summary** | A run summary with `run_id`, `total`, and per-trace `details` is produced. | Recorder test + integration summary assertion. |
| **G6 — Comparison** | Baseline vs candidate emits a structured compare result; candidate exceptions are recorded as `candidate_error` without affecting the baseline. | Compare unit + integration tests. |
| **G7 — Mandatory edge cases** | PRD §7 edge cases 1–6 are covered. | Tests enumerated in the test matrix. |
| **G8 — Coverage** | Core modules (`tracer`, `compare`, `recorder`, `persistence`, `paths`, `serialization`) exceed 90% line coverage; public APIs and contracts are directly tested. | Coverage report. |
| **G9 — Zero dependency / Python 3.10+** | No external runtime dependency; runs on Python 3.10+. | `pyproject.toml` (`dependencies = []`, `requires-python = ">=3.10"`); test run on 3.11. |
| **G10 — Test suite green** | The full unit + integration suite passes. | `pytest` run summary. |

## Required Evidence

- A verification report mapping each FR, frozen decision, and edge case to a concrete test result (`specs/verification/report.md`).
- A reproducible test command and its pass count.
- A coverage report for the core modules.

## Non-Blocking Deferred Items

These are acknowledged future scope and must NOT block this milestone:

1. Multi-variant A/B execution engine (FR-11 keeps the seam open only).
2. Replay-based self-regression workflow (FR-12 keeps artifacts replay-friendly only).
3. Runtime metrics (memory) collectors (FR-13 reserves the seam only).
4. Context-manager (`with`) tracing and class-decorator tracing.
5. Edge cases 7–8 (metrics-collector failure, partial/corrupt replay artifacts).

## Known Exclusions

- Web UI / remote observability.
- Production observability-platform behavior.

## Residual-Risk Tolerance

Acceptance may pass with documented low residual risks (e.g. an exit-only code path exercised only indirectly), provided they are recorded and non-blocking.
