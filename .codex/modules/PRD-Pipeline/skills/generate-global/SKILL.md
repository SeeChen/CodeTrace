---
name: generate-global
description: Generate the global specification layer from the PRD, workflow, planning outputs, and Phase 0 ref documents. Use this before planning domain specifications.
---

# Generate Global

This skill creates or refreshes the `specs/global/` layer for the current project.

Use this skill when the user wants to:

- turn PRD and Phase 0 findings into system-wide specifications
- define business flow, architecture, modules, constraints, and API contracts
- prepare the project for domain planning

Do not use this skill for:

- detailed domain specs
- testing plans
- implementation code

## Required Inputs

Read these files first:

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-to-Coding-Orchestration.md`
4. `specs/ref/*`
5. planning output from `/plan-docs`, if present
6. `.codex/modules/PRD-Pipeline/rules/doc-scope.md`
7. `.codex/modules/PRD-Pipeline/rules/summary-sync.md`

Also read [references/global-output-contract.md](references/global-output-contract.md) before drafting.

## Output Contract

Write or update the project's global specification set, typically under `specs/global/`.

Expected files:

1. `app-business.md`
2. `SA.md`
3. `project-structure.md`
4. `modules.md`
5. `constraint.md`
6. `API.md`

Adapt the file list when the project boundary justifies a different structure.

## Workflow

### Step 1: Reconstruct the system view

Use the PRD and Phase 0 documents to identify:

- primary product flow
- main modules
- extension points
- high-level contracts

### Step 2: Define the global layer

Document:

- business flow across the system
- architecture topology
- structure and module ownership
- non-negotiable constraints
- public API or contract expectations
- frozen decisions versus deferred decisions
- cross-domain lifecycle expectations
- major failure-boundary expectations
- implementation-facing notes that downstream domain specs should not need to rediscover

### Step 3: Prepare downstream domain work

Make sure the global files tell later agents:

- what to expand
- what not to change casually
- which boundaries are already frozen

## Writing Rules

- Keep the global layer stable, but not thin.
- Planning sections may stay concise, but global design documents should be detailed enough to guide domain work without forcing re-derivation of architecture.
- Use diagrams only if plain text structure is insufficient.
- Separate required constraints from implementation suggestions.
- Mark uncertain areas as open questions instead of pretending they are resolved.
- Prefer concrete contracts, lifecycle descriptions, dependency notes, and failure-boundary explanations over abstract summaries.
- Each global file should clearly state what is frozen here and what remains deferred to domain specs.

## Handoff Rules

Before finishing, verify:

1. the file set matches the current project shape
2. each file serves a distinct purpose
3. domain planning can proceed from the output
4. progress tracking will be updated after generation


