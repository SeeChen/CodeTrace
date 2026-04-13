---
name: plan-doc-structure
description: Plan the first-pass specification directory structure and document set from a PRD, workflow, and current project boundaries. Use this before generating global or domain documents.
---

# Plan Doc Structure

This skill creates a first-pass document plan for the current project.

Use this skill when the user wants to:

- determine which spec documents are actually needed
- generate the initial `specs/` directory structure
- classify documents as required, optional, deferred, or unnecessary
- avoid copying the example workflow structure blindly

Do not use this skill for:

- writing detailed architecture specifications
- writing domain implementation specs
- generating code

## Required Inputs

Read these files first:

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-to-Coding-Orchestration.md`
4. `.codex/modules/PRD-Pipeline/rules/doc-scope.md`
5. `.codex/modules/PRD-Pipeline/memory/workflow-memory.md`

Also read [references/doc-structure-contract.md](references/doc-structure-contract.md) before drafting.

## Output Contract

Write or update a planning document that includes:

1. project boundary assessment
2. document phase plan
3. first-pass target directory structure
4. document classification by phase
5. entry gates between phases
6. recommended next commands or agents

Default output path:

- `specs/summary.md` if a summary file already exists
- otherwise a planning section in the current orchestration or planning document

## Workflow

### Step 1: Assess the project boundary

Determine:

- project shape
- project size
- core complexity drivers
- likely documentation granularity

### Step 2: Map the workflow example to the real project

Decide:

- which example documents are required
- which can be merged
- which should be deferred
- which extra documents are needed for this project shape

### Step 3: Produce the first-pass structure

Include:

- directory tree
- required files
- optional files
- files intentionally omitted for now

### Step 4: Explain every major scoping decision

For each important inclusion, omission, merge, or split, explain the reason briefly and trace it back to the PRD or workflow.

## Writing Rules

- Keep the plan concise and decision-oriented.
- Separate facts, inferences, and open questions.
- Avoid detailed architecture design in this planning output.
- Prefer tables for document classification.
- Keep planning intentionally lean; this skill should freeze scope and structure, not substitute for detailed design work.

## Handoff Rules

Before finishing, verify:

1. the output can guide downstream document generation
2. the plan is specific to the current project rather than generic
3. omitted or merged documents are justified
4. the next command or agent to run is obvious


