---
description: "Stage 5: verify the implementation against the build spec."
argument-hint: "[--task <id>]"
---

# Command: verify

## Purpose

Verify the implementation against the build spec and task expectations.

## Direct Invocation

- `/verify`
- `/verify --task <id>`

## Read First

1. `specs/build/test-matrix.md`
2. `specs/build/tasks.md`
3. `.claude/agents/qa-acceptance-agent.md`
4. `.claude/skills/verify-build/SKILL.md`
5. `.claude/memory/implementation-log.md`

## Execute

1. Run the relevant tests and validation checks.
2. Record failures, risks, and fix-loop notes.
3. Update `implementation-log.md` and `pipeline-state.md`.

## Output

- verification evidence
- defect notes
- updated fix-loop records
