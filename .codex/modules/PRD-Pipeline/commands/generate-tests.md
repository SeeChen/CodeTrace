# Command: generate-tests

## Purpose

Generate the testing specification layer from the current PRD and spec set.

## Read First

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/*`
5. `.codex/modules/PRD-Pipeline/skills/generate-test-design/SKILL.md`
6. `.codex/modules/PRD-Pipeline/rules/summary-sync.md`

## Execute

1. Map requirements and constraints to explicit test intent.
2. Generate the testing documents the current project actually needs.
3. Cover functional, edge-case, and non-functional validation where justified.
4. Update progress tracking after writing the output.

## Output

- `specs/testing/` document set

## Guardrails

- Do not write executable tests in this step.
- Do not ignore acceptance-relevant constraints.
- Do not create test documents that the current project does not justify.


