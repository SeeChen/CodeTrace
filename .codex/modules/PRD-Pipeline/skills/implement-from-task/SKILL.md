---
name: implement-from-task
description: Implement code and tests from a frozen build-spec task slice without silently redesigning the architecture or contracts.
---

# Implement From Task

Use this skill to turn a single build-spec task slice into production code and tests.

## Use When

- the build-spec layer and `specs/build/tasks.md` already exist
- a specific task slice is ready to be implemented
- implementation should follow frozen contracts instead of broad PRD reinterpretation

## Do Not Use When

- the build spec or task slices do not exist yet
- the architecture is still unstable
- the task is only verification or acceptance synthesis

## Read First

1. `specs/build/tasks.md`
2. `specs/build/*`
3. `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`
4. `.codex/modules/PRD-Pipeline/memory/implementation-log.md`

## Write

- code under `src/`
- tests under `tests/`
- deviation notes in `.codex/modules/PRD-Pipeline/memory/implementation-log.md`

## Execution Steps

1. Select the next approved task slice and confirm its prerequisites are met.
2. Implement only the files owned by that task slice.
3. Add or update the tests the task slice requires.
4. Keep code aligned with frozen architecture, interfaces, and failure policy.
5. Record any unavoidable deviation in the implementation log before continuing.

## Required Guarantees

- traced behavior matches the contracts in `specs/build/*`
- the task's required tests exist and target the task's expected outputs
- write scope stays inside the task's file ownership
- frozen decisions are not overridden silently

## Guardrails

- Implement one task slice at a time whenever possible.
- Surface blockers instead of making hidden structural changes.
- Write deviations back to memory rather than reinterpreting the spec.
- Prefer maintainable code over clever shortcuts.
