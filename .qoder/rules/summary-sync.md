# Rule 10: Summary Sync After Document Changes

This rule defines how status tracking should be updated after document-generation work.

## Purpose

The document system must be resumable. After each meaningful document-generation task, the repository should record progress so future runs continue from the current state instead of starting over.

## Guidelines

- Update the relevant tracking document after each completed todo or generation step
- Record completed, in-progress, and pending work clearly
- Make the next recommended step obvious
- Keep progress notes concise and factual
- Prefer a single durable status document over scattered ad hoc notes

## Preferred Tracking Targets

- `docs/todo-plan.md`
- `specs/summary.md`

## Required Behavior

After completing a task, record:

1. what was completed
2. where the output was written
3. what remains next
4. any open questions or blockers

## Anti-Patterns

- Do not leave progress only in commit messages
- Do not mark work as done before outputs exist
- Do not restart planning from scratch when a current status file already exists
