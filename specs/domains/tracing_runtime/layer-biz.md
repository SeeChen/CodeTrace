# Tracing Runtime Business Layer

## Scope

This layer coordinates the trace lifecycle and policy decisions once trigger entry reaches the runtime domain.

## Responsibilities

- resolve effective configuration for a trace
- decide whether compare mode is active
- execute baseline first and optional candidate second under the same input set
- send persistence and reporting work to downstream boundaries
- isolate infrastructure failures from main execution semantics

## Lifecycle Outline

1. Resolve effective trace policy.
2. Build session context and capture start time.
3. Execute baseline target.
4. Optionally execute candidate target and compare outputs.
5. Persist artifacts according to policy.
6. Build record payload and submit to summary recorder.
7. Return baseline result or propagate baseline exception.

## Policy Notes

- Compare mode should enrich evidence, not redefine the user-visible return contract.
- Persistence should be allowed to fail independently.
- Runtime should expose enough metadata for future metrics collectors without requiring them now.

## Open Questions

- Whether candidate execution should be skipped automatically if baseline raises, or whether future policies may allow alternate behavior.
