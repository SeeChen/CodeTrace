---
name: generate-sa
description: Generate the active system architecture document from the normalized intent pack and freeze the main design boundaries for downstream build-spec generation.
---

# Generate SA

Use this skill to produce the active architecture layer.

## Use When

- the repository has a stable intent pack
- system boundaries, lifecycle, and extension points need to be frozen
- build-spec generation is the next intended step

## Do Not Use When

- the task is only PRD normalization
- the task is already implementation detail generation

## Read First

1. `specs/intent/brief.md`
2. `docs/Workflow.md`
3. `.claude/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.claude/memory/frozen-decisions.md`

## Write

- `specs/architecture/SA.md`

## Required Content

The architecture should define:

- system context
- module boundaries
- public API surface
- extension points
- runtime lifecycle
- cross-cutting constraints
- frozen decisions
- open questions

## Guardrails

- Keep the architecture stable, explicit, and downstream-friendly.
- Do not expand into file-by-file planning here.
- Freeze what later stages should not casually redefine.
- Push unresolved detail into open questions rather than hiding uncertainty.
