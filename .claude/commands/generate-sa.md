---
description: "Stage 1: generate specs/architecture/SA.md from the intent brief."
argument-hint: "[--refresh]"
---

# Command: generate-sa

## Purpose

Generate the active system architecture layer from the normalized intent pack.

## Direct Invocation

- `/generate-sa`
- `/generate-sa --refresh`

## Read First

1. `specs/intent/brief.md`
2. `docs/Workflow.md`
3. `.claude/agents/architect-agent.md`
4. `.claude/skills/generate-sa/SKILL.md`
5. `.claude/memory/frozen-decisions.md`

## Execute

1. Freeze the system boundaries, lifecycle, interfaces, and extension points.
2. Write `specs/architecture/SA.md`.
3. Update frozen decisions and open questions as needed.
4. Update `memory/pipeline-state.md`.

## Output

- `specs/architecture/SA.md`
