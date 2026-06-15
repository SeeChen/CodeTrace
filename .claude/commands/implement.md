---
description: "Stage 4: implement code and tests from task slices."
argument-hint: "[--task <id>]"
---

# Command: implement

## Purpose

Implement the current build tasks into code and tests.

## Direct Invocation

- `/implement`
- `/implement --task <id>`

## Read First

1. `specs/build/tasks.md`
2. `specs/build/*`
3. `.claude/agents/coding-agent.md`
4. `.claude/skills/implement-from-task/SKILL.md`
5. `.claude/memory/frozen-decisions.md`
6. `.claude/memory/implementation-log.md`

## Execute

1. Implement the next approved task slice.
2. Keep code aligned with frozen architecture and build contracts.
3. Record deviations or blockers in `implementation-log.md`.
4. Update `pipeline-state.md`.

## Output

- implementation changes under `src/`
- tests under `tests/`
