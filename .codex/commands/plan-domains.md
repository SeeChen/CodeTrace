# Command: plan-domains

## Purpose

Plan the domain breakdown of the project from the global specification layer.

## Read First

1. `specs/global/*`
2. `specs/ref/*`
3. `.codex/skills/plan-domains/SKILL.md`
4. `.codex/rules/doc-scope.md`
5. `.codex/rules/summary-sync.md`

## Execute

1. Identify the domain map from the global layer.
2. Define ownership boundaries and dependencies.
3. Recommend the document set for each domain.
4. Prioritize the order of detailed domain expansion.
5. Update progress tracking after writing the result.

## Output

- `specs/domains/summary.md` or an equivalent domain planning document

## Guardrails

- Do not write detailed domain internals in this step.
- Do not create domains only because the example workflow has them.
- Keep the domain map traceable to the global layer and PRD.

