# Tracing Runtime Facade Layer

## Scope

The facade layer exposes runtime behavior through user-facing trigger forms while keeping orchestration inside the runtime core.

## Facade Responsibilities

- function and method decorator entry
- class decorator entry for eligible public methods
- context-manager entry for traced blocks
- local override injection without leaking internal state handling

## Boundary Rules

- facade code should stay thin and mostly validate or normalize user-facing parameters
- facade code must not own filesystem or summary logic
- facade behavior should be consistent across trigger types where semantics overlap

## Open Questions

- Whether class tracing should skip `staticmethod` and `classmethod` by default or support both with explicit rules.
