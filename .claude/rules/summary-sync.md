# Rule: Summary Sync After Each Stage

This rule defines how workflow state must be updated after each completed stage.

## Purpose

The pipeline must be resumable. After each completed stage, the repository should record progress so future runs continue from the current state instead of starting over.

## Guidelines

- Update workflow state after each completed stage, not only at the end of a run
- Record completed, in-progress, and pending stages clearly
- Make the next recommended stage obvious
- Keep progress notes concise and factual
- Prefer durable workflow-state files over scattered ad hoc notes

## Tracking Targets

- `.claude/memory/pipeline-state.md` (primary stage state)
- `.claude/memory/frozen-decisions.md` (frozen contracts)
- `.claude/memory/open-questions.md` (unresolved choices)
- `.claude/memory/implementation-log.md` (deviations and fix-loop notes)

## Required Behavior

After completing a stage, record:

1. what was completed
2. where the output or evidence was written
3. what stage comes next
4. any open questions or blockers

## Anti-Patterns

- Do not leave progress only in commit messages
- Do not mark a stage as done before its outputs exist
- Do not restart planning from scratch when `pipeline-state.md` already records the current state
