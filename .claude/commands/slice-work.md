---
description: "Stage 3: slice the build spec into specs/build/tasks.md."
argument-hint: "[--refresh]"
---

# Command: slice-work

## Purpose

Convert the build-spec layer into implementation task slices.

## Direct Invocation

- `/slice-work`
- `/slice-work --refresh`

## Read First

1. `specs/build/*`
2. `.claude/agents/spec-builder-agent.md`
3. `.claude/skills/slice-build-tasks/SKILL.md`
4. `.claude/memory/frozen-decisions.md`
5. `.claude/memory/open-questions.md`

## Execute

1. Split the build spec into small ordered tasks.
2. Assign file ownership and test expectations per task.
3. Write `specs/build/tasks.md`.
4. Update `memory/pipeline-state.md`.

## Output

- `specs/build/tasks.md`
