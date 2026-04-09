# Command: generate-global

## Purpose

Generate or refresh the global specification layer for the current project.

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `specs/ref/*`
4. `.codex/modules/PRD-Pipeline/skills/generate-global/SKILL.md`
5. `.codex/modules/PRD-Pipeline/rules/doc-scope.md`
6. `.codex/modules/PRD-Pipeline/rules/summary-sync.md`

## Execute

1. Reconstruct the system-level view from the PRD and Phase 0 outputs.
2. Generate the appropriate `specs/global/` file set for the current project shape.
3. Keep each file scoped to global architecture rather than domain implementation.
4. Record any open questions and update progress tracking.

## Output

- `specs/global/` documents appropriate to the current project

## Guardrails

- Do not write detailed domain specs in this step.
- Do not copy the example file list blindly.
- Keep decisions traceable to the PRD and upstream planning outputs.


