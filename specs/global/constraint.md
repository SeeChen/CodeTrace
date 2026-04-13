# CodeTrace Global Constraints

## Purpose

This document records the non-negotiable technical and delivery constraints that all domain specs and future implementation work must honor.

## Decisions Frozen Here

- Python `3.10+` is the target runtime floor.
- MVP runtime dependencies must remain in the standard library unless explicitly justified later.
- Tracing infrastructure must never silently alter primary user-code semantics.

## Hard Constraints

| Constraint | Meaning | Source |
| :-- | :-- | :-- |
| Local-first | Outputs are written locally and reviewed locally. | PRD 1, PRD 4 |
| Zero external runtime dependencies | The default shipped MVP must use the standard library only. | PRD 4 |
| Google Python Style | Naming, docstrings, and maintainability must follow the stated style guide. | PRD 4 |
| Deterministic artifact organization | Runs and traces must be stored predictably and replay-friendly. | PRD 4, PRD 6 |
| Semantics preservation | Return values and exception propagation of user code must stay intact. | PRD 4 |
| Failure isolation | Persistence, reporting, and comparison failures must not corrupt the main execution path. | PRD 4 |
| Extensible-by-design | Comparison, record, storage, and future metrics boundaries must remain additive. | PRD 1, PRD 4, PRD 5 |

## Design Constraints

- Global configuration must support per-call override without forcing business-code edits.
- Comparison support must preserve a path to multi-variant future execution models.
- Artifact naming must support future replay lookup without requiring invasive redesign.
- Optional future metrics must attach through lifecycle hooks rather than hot-path rewrites.

## Non-Goals for the Current Milestone

- Hosted observability
- Remote storage
- Full replay execution engine
- Full A/B orchestration across multiple variants
- Mandatory memory metrics

## Open Questions

- Should log emission be enabled by default for infrastructure failures, or should it be opt-in with a safe minimal fallback?
