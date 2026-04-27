---
name: normalize-prd
description: Convert the PRD into a compact intent pack that freezes scope, constraints, entities, and acceptance framing for downstream architecture work.
---

# Normalize PRD

Use this skill to create the active intent pack for the repository.

## Use When

- the project is starting from a PRD
- architecture work needs a stable, compact upstream artifact
- the current repository still has broad requirement documents but no active intent pack

## Do Not Use When

- system architecture is already frozen and only implementation work is needed
- the task is only verification or acceptance refresh

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.codex/modules/PRD-Pipeline/rules/agent-skill-design.md`

## Write

- `specs/intent/brief.md`

## Required Content

The intent pack should capture:

- project mission
- MVP scope
- explicit non-goals
- non-negotiable constraints
- core entities and actions
- acceptance framing
- open questions

## Guardrails

- Keep the output compact and implementation-relevant.
- Do not generate architecture decisions here.
- Distinguish explicit PRD facts from inferred clarifications.
- Record unresolved ambiguity as open questions instead of forcing certainty.
