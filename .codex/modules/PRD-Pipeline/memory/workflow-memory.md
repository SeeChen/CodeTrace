# Workflow Memory

## Core Principle

The repository follows a document-first AI workflow:

`PRD -> ref -> global -> domains -> testing -> coding`

## Stable Rules

1. PRD is the primary source of truth.
2. Each downstream phase consumes the documents from the previous phase.
3. Coding should not begin before global API and constraints are stable.
4. Open questions must be written down instead of silently guessed.

## Current Reusable Assets

- `Orchestrator Agent`
- `/prd-pipeline` command
- `generate-ref` skill
- `plan-doc-structure` skill
- `generate-global` skill
- `plan-domains` skill
- `generate-domain-spec` skill
- `generate-test-design` skill
- `generate-acceptance` skill
- `plan-docs` command
- `PRD-Pipeline` checkpoint
- `ref-docs` rule
- `Research Agent`
- `generate-ref` command

## Intended Expansion Order

1. generate `specs/ref/`
2. plan the document tree
3. generate `specs/global/`
4. plan domains
5. generate one domain at a time
6. generate testing documents
7. generate acceptance criteria

## Resume Principle

Long-running workflow execution must resume from repository artifacts, especially:

- `.codex/modules/PRD-Pipeline/memory/prd-pipeline-checkpoint.md`
- `specs/summary.md`
- generated specification documents


