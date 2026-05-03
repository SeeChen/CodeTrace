---
name: generate-build-spec
description: Generate the implementation-facing build-spec layer from the intent pack and system architecture.
---

# Generate Build Spec

Use this skill to turn architecture into implementation-ready contracts.

## Use When

- the system architecture is already present
- coding-ready planning needs to be generated
- module contracts and file planning need to be frozen before implementation

## Do Not Use When

- the architecture is still unstable
- the task is only work slicing or coding

## Read First

1. `specs/intent/brief.md`
2. `specs/architecture/SA.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`

## Write

- `specs/build/module-map.md`
- `specs/build/interfaces.md`
- `specs/build/file-plan.md`
- `specs/build/artifact-schema.md`
- `specs/build/failure-policy.md`
- `specs/build/test-matrix.md`

## Required Guarantees

- every implementation area maps to a module
- every important interface has an explicit contract
- every artifact has a predictable schema or directory rule
- every important failure mode has an isolation policy
- every important requirement maps to at least one test intent

## Guardrails

- Write implementation-facing contracts, not broad narrative summaries.
- Keep the output smaller than the legacy domain-heavy document tree.
- Do not re-open architecture decisions without recording the change explicitly.
