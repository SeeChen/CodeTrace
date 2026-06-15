---
name: slice-build-tasks
description: Split the build spec into small ordered implementation tasks with file ownership and test expectations.
---

# Slice Build Tasks

Use this skill to convert the build-spec layer into coding-ready task slices.

## Use When

- the build-spec layer is already written
- implementation needs an explicit task plan
- file ownership and prerequisites need to be made reviewable

## Do Not Use When

- the build-spec layer is incomplete
- the task is direct coding without planning approval

## Read First

1. `specs/build/*`
2. `.claude/docs/PRD-Pipeline-Refactor-Blueprint.md`
3. `.claude/memory/frozen-decisions.md`
4. `.claude/memory/open-questions.md`

## Write

- `specs/build/tasks.md`

## Required Content

Each task slice should state:

- task identifier
- purpose
- file ownership
- prerequisites
- expected code outputs
- required tests
- acceptance notes

## Guardrails

- Keep tasks small enough that coding agents can own them safely.
- Avoid overlapping write scopes where possible.
- Make each task traceable back to the build-spec layer.
