# Command: generate-domain

## Purpose

Generate the specification set for one planned domain.

## Direct Invocation

- `/generate-domain <name>`
- `/generate-domain <name> --refresh`
- `/generate-domain <name> --depth balanced`
- `/generate-domain <name> --depth deep`

## Read First

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/summary.md`
5. `.codex/modules/PRD-Pipeline/skills/generate-domain-spec/SKILL.md`
6. `.codex/modules/PRD-Pipeline/rules/summary-sync.md`

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
- Do not stop at skeletal descriptions for critical domains; the output should be detailed enough to guide implementation and testing.


