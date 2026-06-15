---
name: verify-build
description: Validate implemented code and tests against the build spec and task expectations, and record evidence, defects, and fix-loop notes.
---

# Verify Build

Use this skill to validate implementation outputs against the frozen build spec.

## Use When

- implementation has produced code and tests for one or more task slices
- the build spec and test matrix exist
- evidence is needed before acceptance synthesis

## Do Not Use When

- there is no implementation to validate yet
- the task is only PRD normalization, architecture, or build-spec generation

## Read First

1. `specs/build/test-matrix.md`
2. `specs/build/tasks.md`
3. `specs/build/*`
4. `src/`
5. `tests/`
6. `.claude/memory/implementation-log.md`

## Write

- verification evidence
- defect notes
- fix-loop records in `.claude/memory/implementation-log.md`

## Execution Steps

1. Run the unit and integration tests relevant to the delivered task slices.
2. Check failure-path behavior described in the build spec's failure policy.
3. Confirm delivered code conforms to the interface and artifact contracts.
4. Record passes, failures, and risks as concrete evidence.
5. Capture fix-loop notes when defects require rework.

## Required Guarantees

- every delivered task slice maps back to its test-matrix expectations
- failures and risks are recorded as evidence, not summarized away
- contract conformance is checked, not assumed
- unresolved defects are visible to the acceptance stage

## Guardrails

- Favor concrete findings and evidence over reassurance.
- Do not mark verification complete while required tests fail.
- Keep defect records separate from deferred scope.
- Write fix-loop progress back to memory instead of relying on conversation history.
