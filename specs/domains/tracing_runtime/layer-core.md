# Tracing Runtime Core Layer

## Scope

Core runtime types and lifecycle data for a single trace execution.

## Owns

- trace-session context
- trace identity and timing values
- callable metadata normalization
- lifecycle state transitions for start, execute, compare, persist, finalize

## Key Rules

- start-state capture happens before user execution
- duration is measured with a monotonic clock
- return values are passed through unchanged
- exception metadata may be recorded, but exception propagation remains intact

## Outputs to Other Domains

- normalized runtime metadata
- comparable baseline and candidate payloads
- persistence input payloads
- record-building input payloads

## Open Questions

- Whether argument capture should preserve both raw values and serialization-ready projections at the runtime boundary.
