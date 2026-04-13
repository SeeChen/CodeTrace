# CodeTrace Module Boundaries

## Purpose

This document defines the system-level module and domain boundaries that later domain specs must elaborate without contradicting.

## Decisions Frozen Here

- The MVP is decomposed into four implementation domains.
- Persistence and reporting stay separate from the tracing runtime even when invoked in the same lifecycle.
- Configuration and extension contracts deserve their own ownership boundary to keep public API stability manageable.

## Deferred to Domain Specs

- Internal classes and helper functions
- Exact data structures and file payload schemas

## Global Module Map

| Module / Domain | Owns | Depends On | Does Not Own |
| :-- | :-- | :-- | :-- |
| `tracing_runtime` | Trigger entry, session lifecycle, timing, exception-safe orchestration | configuration contracts, persistence adapters, comparison/reporting hooks | Filesystem layout details |
| `persistence_artifacts` | Path preparation, serialization policy, run/trace directory writes | configuration contracts, runtime metadata | Trigger behavior and compare decisions |
| `comparison_reporting` | Compare execution result shaping, record assembly, summary aggregation | runtime metadata, persistence outputs, configuration hooks | Trace trigger wrappers |
| `configuration_contracts` | Global config state, per-call overrides, protocol contracts, defaults | none | Hot-path execution and storage I/O |

## Dependency Rules

- `configuration_contracts` should be foundational and reusable by every other domain.
- `tracing_runtime` can call persistence and reporting boundaries, but those domains should not orchestrate runtime entry.
- `comparison_reporting` can consume runtime context and extension hooks, but should not redefine trigger semantics.
- Cycles between runtime and persistence should be avoided by exchanging explicit payloads rather than shared mutable state.

## Open Questions

- Whether summary recording should live entirely inside `comparison_reporting` or be split into a thinner dedicated reporting adapter package later.
