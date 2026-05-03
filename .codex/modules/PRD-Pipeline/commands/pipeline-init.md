# Command: pipeline-init

## Purpose

Normalize the PRD into the active intent pack used by the rest of the workflow.

## Direct Invocation

- `/pipeline-init`
- `/pipeline-init --refresh`

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.codex/modules/PRD-Pipeline/skills/normalize-prd/SKILL.md`
5. `.codex/modules/PRD-Pipeline/rules/agent-skill-design.md`

## Execute

1. Reconstruct the project mission, scope, constraints, and acceptance framing from the PRD.
2. Write the intent pack to `specs/intent/brief.md`.
3. Record unresolved issues in `memory/open-questions.md`.
4. Update `memory/pipeline-state.md`.

## Output

- `specs/intent/brief.md`
