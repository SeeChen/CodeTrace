# Command: verify

## Purpose

Verify the implementation against the build spec and task expectations.

## Direct Invocation

- `/verify`
- `/verify --task <id>`

## Read First

1. `specs/build/test-matrix.md`
2. `specs/build/tasks.md`
3. `.codex/modules/PRD-Pipeline/agents/qa-acceptance-agent.md`
4. `.codex/modules/PRD-Pipeline/skills/verify-build/SKILL.md`
5. `.codex/modules/PRD-Pipeline/memory/implementation-log.md`

## Execute

1. Run the relevant tests and validation checks.
2. Record failures, risks, and fix-loop notes.
3. Update `implementation-log.md` and `pipeline-state.md`.

## Output

- verification evidence
- defect notes
- updated fix-loop records
