# CodeTrace Global API Contracts

## Purpose

This document defines the stable public-facing API expectations and extension contracts for the MVP global layer.

## Decisions Frozen Here

- The public API centers on global configuration plus trigger-specific tracing entry points.
- Compare and record customization are supported through explicit callable contracts.
- Per-call overrides are part of the MVP contract.

## Deferred to Domain Specs

- Exact parameter names for every optional policy field
- Concrete typing syntax and schema modules

## Primary Interfaces

| Interface | Responsibility | Notes |
| :-- | :-- | :-- |
| `TraceFunc.config(...)` | Set global defaults for trace root, persistence, summary, compare hook, record builder, and future collectors. | Global mutable configuration must be explicit and reviewable. |
| `TraceFunc.__call__(...)` | Return a decorator that applies tracing with optional local overrides. | Core function and method trigger. |
| `TraceBlock(...)` | Provide block-level tracing via context manager semantics. | MVP-ready contract, even if implemented after decorator stability. |
| `trace_class(...)` or equivalent class contract | Apply tracing rules across eligible public methods. | Must align with the same session lifecycle as function tracing. |

## Extension Contracts

| Contract | Minimum Expectation |
| :-- | :-- |
| Record Builder | Accepts runtime metadata and returns a dictionary-like record payload. |
| Compare Callable | Accepts comparable execution outputs or artifacts and returns a dictionary-like comparison result. |
| Persistence Adapter | Exposes a stable save interface for inputs, outputs, comparison artifacts, and future replay assets. |
| Metrics Collector | Future lifecycle hook contract with start, stop, and emit responsibilities. |

## Contract Rules

- Public contracts should prefer explicit keyword arguments over ambiguous shared state.
- Per-call overrides should merge cleanly with global defaults.
- Compare mode should not require users to rewrite their original function body.
- Trigger interfaces should remain small enough that README examples stay easy to understand.

## Open Questions

- Whether block tracing should be exposed through the same namespace object as function tracing or through a separate public helper.
