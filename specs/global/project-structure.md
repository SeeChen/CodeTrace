# CodeTrace Project Structure Plan

## Purpose

This document proposes the implementation-facing repository structure that matches the current specification set and the PRD's zero-dependency, Google-style Python goals.

## Decisions Frozen Here

- The codebase should separate public API, runtime orchestration, adapters, and shared contracts.
- Tests should mirror major domains and include both unit and integration layers.
- Documentation should remain under `specs/` until implementation catches up.

## Deferred to Domain Specs

- Exact file count inside each package
- Helper-module breakdown within a domain

## Proposed Structure

```text
src/
└── codetrace/
    ├── __init__.py
    ├── api/
    ├── runtime/
    ├── adapters/
    ├── contracts/
    └── utils/

tests/
├── unit/
├── integration/
└── performance/
```

## Package Guidance

| Package Area | Responsibility |
| :-- | :-- |
| `api/` | Public tracing entry points and stable user-facing contracts. |
| `runtime/` | Session orchestration, trigger execution, timing, and lifecycle coordination. |
| `adapters/` | Persistence, reporting, and future optional output adapters. |
| `contracts/` | Typed protocols, schemas, defaults, and extension contracts. |
| `utils/` | Small deterministic helpers such as path, hash, serialization, and logging setup. |

## Review Notes

- A single flat module would make extension boundaries and test ownership unclear.
- A deeper package tree is not justified yet because the repository is still pre-implementation.
- The code package name should remain lowercase and snake_case-friendly to align with the PRD style rules.

## Open Questions

- Whether the public API should center on `TraceFunc` only at first or expose a broader `trace` convenience surface immediately.
