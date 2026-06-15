---
name: accept-milestone
description: Generate milestone acceptance criteria and an evidence-based acceptance report from the PRD, build spec, and verification context.
---

# Accept Milestone

Use this skill to define milestone acceptance gates and write the acceptance-stage outputs.

## Use When

- the project needs a reviewable acceptance criteria document
- implementation or verification work needs to be judged against explicit gates
- the repository is ready for acceptance-stage synthesis

## Do Not Use When

- the build-spec layer does not exist yet
- the task is only PRD normalization, architecture work, or coding

## Read First

1. `docs/PRD.md`
2. `specs/intent/brief.md`
3. `specs/build/*`
4. `.claude/skills/accept-milestone/references/acceptance-contract.md`
5. `.claude/memory/implementation-log.md`
6. `.claude/memory/open-questions.md`

## Write

- `specs/acceptance/criteria.md`
- `specs/acceptance/report.md`

## Required Content

The acceptance outputs should define:

- milestone scope
- blocking acceptance gates
- required evidence
- deferred but non-blocking items
- final delivered status
- residual risks and open issues

## Guardrails

- Do not invent new product requirements.
- Keep criteria concrete, reviewable, and evidence-based.
- Separate acceptance standards from the final acceptance decision.
- Keep future-scope items out of the blocking milestone gates.
