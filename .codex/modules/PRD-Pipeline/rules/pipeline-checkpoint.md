# Rule 11: PRD-Pipeline Checkpoint and Resume

This rule defines how the `PRD-Pipeline` workflow must track progress and recover from interruption.

## Purpose

`PRD-Pipeline` is a long-running document workflow. It must be resumable without depending on hidden conversational memory.

## Required Checkpoint File

Use:

- `.codex/modules/PRD-Pipeline/memory/prd-pipeline-checkpoint.md`

## Required Behavior

- Read the checkpoint before starting work
- Update the checkpoint after every completed stage
- Update the checkpoint after every completed domain during domain expansion
- Record blockers before stopping
- Resume from the first incomplete stage on the next run

## Minimum Checkpoint Data

The checkpoint must record:

1. overall pipeline status
2. last completed stage
3. next stage
4. completed and remaining domains
5. current blockers
6. output status by phase

## Anti-Patterns

- Do not restart from Stage 1 when a valid checkpoint exists
- Do not rely on chat memory instead of checkpoint state
- Do not mark a stage complete before its outputs exist
- Do not stop without recording the current blocker or next step
