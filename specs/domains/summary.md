# CodeTrace Domain Plan

## Purpose

This document maps the global architecture into the implementation domains that should be expanded before coding.

## Source Documents

- `docs/PRD.md`
- `specs/ref/*`
- `specs/global/*`

## Domain Map

| Domain | Purpose | Owns | Depends On | Required Docs | Priority |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `tracing_runtime` | Coordinate decorator, class, and block-trigger execution lifecycles. | session state, timing, exception-safe wrapper flow | `configuration_contracts`, `persistence_artifacts`, `comparison_reporting` | `SA.md`, `layer-core.md`, `layer-biz.md`, `layer-facade.md` | 1 |
| `configuration_contracts` | Freeze config state, per-call overrides, and extension protocols. | config schema, defaults, hook contracts | none | `SA.md`, `layer-core.md`, `layer-facade.md` | 2 |
| `persistence_artifacts` | Serialize and store run and trace artifacts deterministically. | path model, save policies, artifact payload handling | `configuration_contracts` | `SA.md`, `layer-core.md`, `layer-dao.md` | 3 |
| `comparison_reporting` | Produce comparison results, records, and run summaries. | compare payload shaping, record builder orchestration, summary aggregation | `configuration_contracts`, `tracing_runtime`, `persistence_artifacts` | `SA.md`, `layer-core.md`, `layer-biz.md`, `layer-facade.md` | 4 |

## Domain Boundaries

- `tracing_runtime` owns hot-path execution and must preserve user semantics.
- `configuration_contracts` owns reusable contracts and default-resolution rules so the rest of the system does not invent policy ad hoc.
- `persistence_artifacts` owns directory layout and serialization behavior, but not business-level compare decisions.
- `comparison_reporting` owns derived outputs from execution results, but not trigger wrappers or path construction.

## Dependencies

- `configuration_contracts` is foundational.
- `tracing_runtime` consumes config and calls persistence/reporting boundaries.
- `persistence_artifacts` consumes config-derived policy and runtime-provided payloads.
- `comparison_reporting` depends on runtime metadata and may reference persisted artifact locations in its records and summaries.

## Expansion Order

1. `tracing_runtime`
2. `configuration_contracts`
3. `persistence_artifacts`
4. `comparison_reporting`

Rationale: tracing semantics are the highest-risk core behavior, configuration contracts stabilize cross-domain interfaces, persistence follows once payload boundaries are clear, and reporting should finalize after the other domains define what evidence exists.

## Open Questions

- Whether block tracing should share the same runtime engine instance as decorator tracing or only the same lifecycle contract.
