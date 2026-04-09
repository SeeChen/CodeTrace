# Rule 7: Branch Selection Before Work

This rule defines how AI agents should choose a branch before starting a task in the CodeTrace-AI repository.

## Purpose

Every task should run on an appropriate working branch. AI agents must not treat the current branch as the default branch for unrelated work.

## Guidelines

- Check the current branch before making changes
- Decide whether the current task belongs on the current branch
- Reuse the current branch only when the task matches that branch's meaning and scope
- Create or switch to a suitable branch when the task is new or unrelated
- Keep related changes on the same branch and separate meaningfully different changes onto different branches
- Do not use `main` as the default working branch for normal tasks

## Branch Naming

- Use `feature/*` for new functionality
- Use `fix/*` for bug fixes
- Use `docs/*` for documentation or workflow-rule changes
- Use `chore/*` for maintenance work when no better type fits

## Expected Behavior

Before starting implementation, verify:

1. The current branch matches the task scope
2. The branch name reflects the type of work
3. The task will not mix review-in-progress changes with unrelated work

## Anti-Patterns

- Do not keep working on a branch whose purpose does not match the current task
- Do not mix multiple meaningfully different tasks into one branch
- Do not commit routine work directly to `main`
