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

- `generate-ref` skill
- `ref-docs` rule
- `Research Agent`
- `generate-ref` command

## Intended Expansion Order

1. `generate-global`
2. `Architect Agent`
3. `generate-domain-spec`
4. `Domain Expert Agent`
5. `generate-test-plan`
6. `Coding Agent`
