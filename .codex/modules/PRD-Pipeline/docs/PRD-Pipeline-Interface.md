# PRD-Pipeline Interface

This document defines how the active `PRD-Pipeline` workflow should be called directly or composed into other workflows.

## Primary Entry Point

- `/prd-pipeline`

## Preferred Stage Commands

- `/pipeline-init`
- `/generate-sa`
- `/generate-spec`
- `/slice-work`
- `/implement`
- `/verify`
- `/accept`

## Purpose

Generate or refresh the delivery-oriented artifact set from the PRD through acceptance while remaining resumable and repository-backed.

## Required Inputs

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.codex/modules/PRD-Pipeline/memory/pipeline-state.md`
5. `.codex/modules/PRD-Pipeline/memory/frozen-decisions.md`
6. `.codex/modules/PRD-Pipeline/memory/open-questions.md`
7. `.codex/modules/PRD-Pipeline/memory/implementation-log.md`

## Active Outputs

1. `specs/intent/brief.md`
2. `specs/architecture/SA.md`
3. `specs/build/*`
4. `specs/acceptance/criteria.md`
5. `specs/acceptance/report.md`
5. updated memory state

## Stage Contract

The active stage order is:

1. `pipeline-init`
2. `generate-sa`
3. `generate-spec`
4. `slice-work`
5. `implement`
6. `verify`
7. `accept`

Another workflow may compose this pipeline only if it preserves that ordering or records an explicit reason for deviation.

## Resume Contract

The workflow must:

1. read `memory/pipeline-state.md` before starting work
2. update the current stage after each completed stage
3. record blockers instead of silently stopping
4. store frozen contract decisions in `memory/frozen-decisions.md`
5. store unresolved issues in `memory/open-questions.md`
6. store implementation deviations and fix-loop notes in `memory/implementation-log.md`

## Blocking Conditions

The workflow may ask for clarification only when:

1. `docs/PRD.md` is missing
2. the PRD is contradictory in a way that blocks the next stage
3. the repository target is materially ambiguous
4. the user explicitly requests alternate scope

## Non-Blocking Principle

If one area is blocked but the rest of the current stage can proceed safely, finish the non-blocked work first and record the blocker in workflow memory.

## Legacy Compatibility

The pipeline module should not recreate or extend the removed legacy command path.

If old spec outputs need to be preserved for archival reasons in the future, they should be stored outside the active generation path.
