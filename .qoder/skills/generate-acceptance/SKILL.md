---
name: generate-acceptance
description: Generate acceptance criteria from the PRD and specification layers. Use this to define the final document-level delivery gate for the current milestone.
---

# Generate Acceptance

This skill creates or refreshes the acceptance layer for the current project.

Use this skill when the user wants to:

- define milestone completion gates
- translate the PRD and specs into acceptance criteria
- make final review requirements explicit

Do not use this skill for:

- rewriting the product scope
- replacing test planning
- implementing code or tests

## Required Inputs

Read these files first:

1. `docs/PRD.md`
2. `specs/ref/*`
3. `specs/global/*`
4. `specs/domains/*`
5. `specs/testing/*`
6. `.qoder/rules/summary-sync.md`

Also read [references/acceptance-contract.md](references/acceptance-contract.md).

## Output Contract

Write or update the acceptance layer, usually:

- `specs/acceptance/criteria.md`

Add more files only if the project shape justifies them.

## Workflow

### Step 1: Rebuild milestone scope

Identify what is in scope, deferred, and non-negotiable for the current milestone.

### Step 2: Define acceptance gates

Document:

- mandatory functional gates
- mandatory technical gates
- required evidence or review artifacts
- deferred or non-blocking checks

### Step 3: Align with testing

Make sure acceptance criteria can be supported by the testing and spec layers.

## Handoff Rules

Before finishing, verify:

1. the criteria reflect the current milestone rather than future scope
2. the gates are clear enough for human review
3. the output is concise and decision-friendly
4. progress tracking will be updated
