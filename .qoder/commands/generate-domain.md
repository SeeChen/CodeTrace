# Command: generate-domain

## Purpose

Generate the specification set for one planned domain.

## Read First

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/summary.md`
5. `.qoder/skills/generate-domain-spec/SKILL.md`
6. `.qoder/rules/summary-sync.md`

## Execute

1. Select the target domain from the current domain plan.
2. Rebuild its boundary and responsibilities.
3. Generate the required layer documents for that domain.
4. Record open questions and update progress tracking.

## Output

- `specs/domains/<domain-name>/` document set

## Guardrails

- Work on one domain per run unless the task explicitly requests more.
- Do not override global decisions in the domain documents.
- Generate only the layer files that the domain actually needs.
