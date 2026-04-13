# CodeTrace Business Flow

## Purpose

This document freezes the product-level flow for how CodeTrace is used and what outcomes it produces, without dropping into domain implementation details.

## Decisions Frozen Here

- CodeTrace is a local development aid for behavioral validation, not a remote observability product.
- The primary user journey is instrumentation -> execution -> artifact review -> refactor confidence.
- Comparison and extension hooks are first-class product capabilities in the MVP boundary, while replay and advanced metrics remain future-facing.

## Deferred to Domain Specs

- Exact trace identity format
- Serialization fallback mechanics
- Lifecycle details for compare-mode error handling

## Primary User Flow

1. The user configures global defaults, especially trace root, persistence behavior, summary behavior, and optional compare/record hooks.
2. The user starts tracing through one of three triggers: function decorator, class decorator, or context manager.
3. The tracing runtime captures call context, timing, and optional comparison execution.
4. Persistence writes per-run and per-trace artifacts through storage boundaries.
5. Record assembly normalizes the trace result into a structured payload.
6. Reporting aggregates all trace records into a run-level summary for later inspection.

## Key Product Scenarios

| Scenario | Product Need | Global Implication |
| :-- | :-- | :-- |
| Basic function tracing | Observe inputs, outputs, timing, and result metadata. | Decorator path must be the most direct and stable trigger. |
| Refactor verification | Compare baseline and candidate using identical inputs. | Compare flow must sit inside the same session lifecycle as tracing. |
| Class tracing | Instrument multiple public methods under one contract. | Trigger logic must support method discovery rules consistently. |
| Block tracing | Instrument code without a function boundary. | Lifecycle contracts must not depend only on callable wrapping. |
| Future replay and metrics | Preserve deterministic artifacts and extension seams. | Global design must favor session-centric composition over hard-coded wrappers. |

## Business Rules

- Tracing must not change user-code return semantics.
- User-code exceptions still propagate unless a future explicit policy says otherwise.
- Infrastructure failures are reported and isolated instead of corrupting the primary execution path.
- Artifacts must stay deterministic and locally reviewable.

## Open Questions

- Should compare mode be treated as a specialized trigger option or as a runtime option shared across all trigger types?
