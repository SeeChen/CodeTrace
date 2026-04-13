# CodeTrace MVP Acceptance Criteria

## Purpose

This document defines the review gates for the current CodeTrace MVP milestone derived from the PRD and current specification set.

## Source Documents

- `docs/PRD.md`
- `specs/ref/*`
- `specs/global/*`
- `specs/domains/*`
- `specs/testing/*`

## Milestone Scope

In scope:

- function and method tracing
- deterministic local artifact persistence
- structured run summary generation
- baseline-versus-candidate comparison
- custom compare and record hooks
- configuration defaults with per-call overrides
- design-ready contracts for block tracing, class tracing, and future metrics/replay extensibility

Deferred and non-blocking:

- multi-variant A/B execution
- replay engine implementation
- shipped memory metrics collection
- remote or hosted interfaces

## Mandatory Gates

| Gate | Requirement Link | Acceptance Standard |
| :-- | :-- | :-- |
| Core semantics | FR-01, PRD 4 | Traced execution preserves return values and exception propagation of user code. |
| Artifact persistence | FR-02, FR-12 | Inputs and outputs are stored in predictable run and trace directories with isolated local outputs. |
| Summary output | FR-03 | A structured run summary is emitted with total trace count and per-trace details. |
| Compare mode | FR-04, FR-11 | Baseline and candidate can run under the same inputs and produce a structured comparison result without redefining baseline semantics. |
| Extensibility hooks | FR-05, FR-06, FR-13 | Custom compare and record hooks work through stable contracts, and metrics-readiness remains additive. |
| Configuration usability | FR-07 | Global defaults and per-call overrides are both available and documented. |
| Architecture quality | FR-10 | Persistence, reporting, comparison, and runtime responsibilities remain separated by explicit boundaries. |
| Quality and style | PRD 4, PRD 7 | Public APIs are documented, Google-style expectations are met, and tests cover public contracts and major edge cases. |

## Required Evidence

- implementation aligned with `specs/global/*` and domain specs
- automated test results covering core functionality and edge cases
- performance evidence against the benchmark plan in `specs/testing/engine_perf.md`
- examples or README usage for the main public API
- clear documentation of any deferred decisions or known limitations

## Deferred or Non-Blocking Checks

- block tracing may be accepted as a documented planned contract if the milestone is intentionally scoped to stabilize decorator tracing first
- class tracing may be accepted in the same staged way only if the repository explicitly records the narrowed milestone
- replay and metrics support are reviewed for readiness, not for feature completion

## Open Questions

- Whether the immediate milestone should require block tracing and class tracing as implemented features or only as frozen contracts ready for the next implementation step.
