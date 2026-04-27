# Command: prd-pipeline

## Purpose

Run the active PRD-Pipeline from PRD normalization through acceptance with minimal interruption.

The active flow is:

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`

## Direct Invocation

- `/prd-pipeline`
- `/prd-pipeline docs/PRD.md`
- `/prd-pipeline docs/PRD.md --from generate-sa`
- `/prd-pipeline docs/PRD.md --only generate-spec`
- `/prd-pipeline docs/PRD.md --refresh build`

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Interface.md`
5. `.codex/modules/PRD-Pipeline/rules/rules.md`
6. `.codex/modules/PRD-Pipeline/memory/pipeline-state.md`
7. `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`
8. `.codex/modules/PRD-Pipeline/memory/open-questions.md`
9. `.codex/modules/PRD-Pipeline/memory/implementation-log.md`

## Execution Model

This command owns the active end-to-end delivery workflow:

1. pipeline init
2. system architecture generation
3. build-spec generation
4. work slicing
5. implementation
6. verification
7. acceptance

## Stage Flow

### Stage 0: Pipeline Init

Run:
- `/pipeline-init`
- `normalize-prd` skill

Output:
- `specs/intent/brief.md`

### Stage 1: Generate SA

Run:
- `/generate-sa`
- `generate-sa` skill

Output:
- `specs/architecture/SA.md`

### Stage 2: Generate Build Spec

Run:
- `/generate-spec`
- `generate-build-spec` skill

Output:
- `specs/build/*`

### Stage 3: Slice Work

Run:
- `/slice-work`
- `slice-build-tasks` skill

Output:
- `specs/build/tasks.md`

### Stage 4: Implement

Run:
- `/implement`

Output:
- `src/`
- `tests/`

### Stage 5: Verify

Run:
- `/verify`

Output:
- verification evidence
- fix-loop updates

### Stage 6: Accept

Run:
- `/accept`

Output:
- `specs/acceptance/report.md`

## Resume Behavior

Before doing any work:

1. read `memory/pipeline-state.md`
2. resume from the first incomplete active stage
3. record blockers instead of stopping silently

## Guardrails

- Do not skip architecture or build-spec generation when they are required.
- Do not let implementation silently override frozen decisions.
- Do not expand agent or skill files with large embedded reference content.
- Do not treat legacy stage outputs as the primary target structure for new work.
