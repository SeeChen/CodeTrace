# Command: accept

## Purpose

Generate the milestone acceptance report from the delivered scope and verification evidence.

## Direct Invocation

- `/accept`
- `/accept --refresh`

## Read First

1. `docs/PRD.md`
2. `specs/intent/brief.md`
3. `specs/build/*`
4. `.codex/modules/PRD-Pipeline/memory/implementation-log.md`
5. `.codex/modules/PRD-Pipeline/memory/open-questions.md`

## Execute

1. Reconstruct the delivered scope and evidence.
2. Distinguish delivered, deferred, and blocked work.
3. Write `specs/acceptance/report.md`.
4. Update `pipeline-state.md`.

## Output

- `specs/acceptance/report.md`
