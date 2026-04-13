# Comparison and Reporting Facade Layer

## Scope

The facade layer exposes summary and comparison-related outputs to the rest of the system through narrow contracts.

## Responsibilities

- provide runtime-callable compare and record-builder interfaces
- expose summary flush entry points for explicit or exit-time usage
- normalize outward-facing summary schema

## Boundary Rules

- facade contracts should accept explicit payloads rather than shared mutable globals
- the facade should not own trace execution or path creation
- custom hooks should receive stable, documented input shapes

## Open Questions

- Whether a public `flush_summary()` hook is needed in the MVP for test harness control.
