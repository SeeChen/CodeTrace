# Command: slice-work

## Purpose

Convert the build-spec layer into implementation task slices.

## Direct Invocation

- `/slice-work`
- `/slice-work --refresh`

## Read First

1. `specs/build/*`
2. `.codex/modules/PRD-Pipeline/skills/slice-build-tasks/SKILL.md`
3. `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`
4. `.codex/modules/PRD-Pipeline/memory/open-questions.md`

## Execute

1. Split the build spec into small ordered tasks.
2. Assign file ownership and test expectations per task.
3. Write `specs/build/tasks.md`.
4. Update `memory/pipeline-state.md`.

## Output

- `specs/build/tasks.md`
