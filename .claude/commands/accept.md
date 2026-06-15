---
description: "Stage 6: generate acceptance criteria and report."
argument-hint: "[--refresh]"
---

# Command: accept

## Purpose

Generate the milestone acceptance criteria and acceptance report from the delivered scope and verification evidence.

## Direct Invocation

- `/accept`
- `/accept --refresh`

## Read First

1. `docs/PRD.md`
2. `specs/intent/brief.md`
3. `specs/build/*`
4. `.claude/agents/qa-acceptance-agent.md`
5. `.claude/skills/accept-milestone/SKILL.md`
6. `.claude/memory/implementation-log.md`
7. `.claude/memory/open-questions.md`

## Execute

1. Reconstruct the milestone scope, gates, and evidence needs.
2. Write `specs/acceptance/criteria.md`.
3. Distinguish delivered, deferred, and blocked work.
4. Write `specs/acceptance/report.md`.
5. Update `pipeline-state.md`.

## Output

- `specs/acceptance/criteria.md`
- `specs/acceptance/report.md`
