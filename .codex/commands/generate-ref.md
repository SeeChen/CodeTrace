# Command: generate-ref

## Purpose

Generate or refresh `specs/ref/` from the project PRD and workflow.

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/rules/ref-docs.md`
4. `.codex/skills/generate-ref/SKILL.md`

## Execute

1. Extract grounded terms, constraints, and performance expectations from the PRD.
2. Generate `specs/ref/prd_keywords.md`.
3. Generate `specs/ref/std_lib_research.md`.
4. Generate `specs/ref/perf_baseline.md`.
5. Leave open questions instead of guessing when the PRD is incomplete.

## Output

- `specs/ref/prd_keywords.md`
- `specs/ref/std_lib_research.md`
- `specs/ref/perf_baseline.md`

## Guardrails

- Do not write `global/` or `domains/` documents.
- Do not invent APIs or benchmark results.
- Keep all conclusions traceable to source documents.

