# Command: generate-acceptance

## Purpose

Generate the acceptance criteria layer for the current milestone.

## Direct Invocation

- `/generate-acceptance`
- `/generate-acceptance --refresh`
- `/generate-acceptance --depth balanced`
- `/generate-acceptance --depth deep`

## Read First

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/*`
5. `specs/testing/*`
6. `.codex/modules/PRD-Pipeline/skills/generate-acceptance/SKILL.md`
7. `.codex/modules/PRD-Pipeline/rules/summary-sync.md`

## Execute

1. Rebuild the current milestone scope from the PRD and specs.
2. Define mandatory gates and required evidence.
3. Distinguish blocking acceptance items from deferred future work.
4. Update progress tracking after writing the output.

## Output

- `specs/acceptance/criteria.md` or the project-equivalent acceptance file

## Guardrails

- Do not invent new requirements at this stage.
- Do not make acceptance depend on future-scope features.
- Keep the criteria concrete and reviewable.
- Keep the document concise in form, but not vague in gates or evidence requirements.


