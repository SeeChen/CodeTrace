# PRD-Pipeline Interface

This document defines how the `PRD-Pipeline` workflow may be called directly or composed into another workflow.

## Entry Command

- `/prd-pipeline`

## Purpose

Generate the complete project document set from the PRD through acceptance-document generation while remaining resumable and self-contained.

## Required Inputs

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. existing upstream artifacts, if any, under `specs/`
4. `.codex/modules/PRD-Pipeline/memory/prd-pipeline-checkpoint.md`

## Required Outputs

1. planning outputs
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/*`
5. `specs/testing/*`
6. `specs/acceptance/*`
7. updated checkpoint and status tracking

## Checkpoint Contract

The workflow must:

1. update the checkpoint after each completed stage
2. update the checkpoint after each completed domain during domain expansion
3. record blockers instead of silently failing
4. resume from the first incomplete stage on the next run

## Composition Contract

Another workflow may call `PRD-Pipeline` only if it:

1. does not alter the internal stage order without explicit reason
2. preserves the checkpoint file
3. treats the pipeline's outputs as authoritative for downstream document work
4. does not rely on hidden conversational memory instead of repository artifacts

## Blocking Conditions

The pipeline may ask for clarification only when:

1. the PRD is missing
2. the PRD is contradictory in a way that blocks the next stage
3. the output target is materially ambiguous
4. the user explicitly requests alternate scope

## Non-Blocking Principle

If one area is blocked but others are not, complete all non-blocked work first and record the blocker in the checkpoint.
