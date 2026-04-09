# Rule 7: Branch Selection Before Work

This rule defines how AI agents should choose a branch before starting a task in the CodeTrace-AI repository.

## Purpose

Every task should run on an appropriate working branch. AI agents must not treat the current branch as the default branch for unrelated work.

## Guidelines

- Check the current branch before making changes
- Decide whether the current task belongs on the current branch
- Create or switch to a suitable branch when the task is new or unrelated
- Keep related changes on the same branch and separate unrelated changes onto different branches
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

- Do not keep working on a previous task branch by default
- Do not mix multiple unrelated tasks into one branch
- Do not commit routine work directly to `main`
