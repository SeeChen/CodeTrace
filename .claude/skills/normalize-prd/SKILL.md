---
name: normalize-prd
description: Convert the PRD into a compact intent pack that freezes scope, constraints, entities, and acceptance framing for downstream architecture work.
---

# Normalize PRD

Use this skill to create the active intent pack for the repository.

## Use When

- the project is starting from a PRD
- architecture work needs a stable, compact upstream artifact
- the current repository still has broad requirement documents but no active intent pack

## Do Not Use When

- system architecture is already frozen and only implementation work is needed
- the task is only verification or acceptance refresh

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.claude/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.claude/rules/agent-skill-design.md`

## Write

- `specs/intent/brief.md`

## Required Content

The intent pack should capture:

- project mission
- MVP scope
- explicit non-goals
- non-negotiable constraints
- deterministic file schema
- failure isolation policy
- MVP decisions
- core entities and actions
- contextual awareness for downstream AI agents
- acceptance framing
- open questions

## Output Contract

`specs/intent/brief.md` must be generated as a deterministic, AI-consumable single source of truth. It should use these sections, in this order:

1. `Input Sources`
2. `Project Mission`
3. `MVP Scope`
4. `Explicit Non-Goals`
5. `Non-Negotiable Constraints`
6. `Deterministic File Schema`
7. `Failure Isolation Policy`
8. `MVP Decisions`
9. `Core Entities`
10. `Core Actions`
11. `Contextual Awareness`
12. `Acceptance Framing`
13. `Open Questions`

### Deterministic File Schema Requirements

When the PRD requires local runtime artifacts, the brief must define the concrete default artifact topology instead of using broad wording such as "organized by run and trace identity".

Use this default schema unless the PRD explicitly requires another structure:

```text
.codetrace/
└── <run_id>/
    ├── summary.json
    └── <trace_name>/
        ├── input.json
        ├── output.json
        ├── metadata.json
        └── compare.json
```

The section must define the purpose of `<run_id>`, `<trace_name>`, `input.json`, `output.json`, `metadata.json`, `compare.json`, and `summary.json`.

### Failure Isolation Policy Requirements

When the PRD requires tracing infrastructure not to break user code, the brief must define isolation behavior concretely:

1. user-code execution remains primary
2. user-code exceptions propagate normally
3. persistence, reporting, and comparison exceptions are wrapped with try-except encapsulation
4. isolated infrastructure failures must not interrupt successful user-code execution
5. isolated failures must be recorded through `stderr`, internal logging, or metadata
6. failure records must include subsystem, exception type, and message
7. infrastructure failures must not be silently swallowed

### MVP Decision Requirements

Convert resolvable open questions into explicit MVP decisions when the PRD gives enough direction or when a conservative default reduces downstream ambiguity.

For CodeTrace, the default MVP decisions are:

1. `run_id` defaults to an ISO 8601 timestamp safe for file names, such as `2026-05-04T10-30-00`.
2. non-serializable values fall back to `repr(value)`.
3. comparison failures are recorded as artifacts and metadata by default, not raised, unless a future explicit strict mode is introduced.
4. context-manager tracing remains a reserved extension path until function and method tracing are stable.

### Contextual Awareness Requirements

The brief must include AI execution guidance that reduces hallucination in later stages:

1. treat the brief as the current single source of truth until architecture is generated
2. prefer explicit contracts, deterministic file names, and small adapter boundaries
3. keep generated code local-first and zero-dependency unless a later frozen decision changes that
4. require Google-style docstrings for public Python APIs and extension contracts
5. prefer `pytest` unless the repository standardizes on another test runner
6. require every core action to map to at least one unit or integration test

## Guardrails

- Keep the output compact and implementation-relevant.
- Do not generate architecture decisions here.
- Convert resolvable open questions into explicit MVP decisions when the PRD gives enough direction.
- Use open questions only for unresolved choices that would materially affect architecture or implementation.
- Include deterministic artifact paths when the PRD depends on file-system behavior.
- Define concrete failure-isolation behavior when the PRD requires infrastructure failures not to break user code.
- Distinguish explicit PRD facts from inferred clarifications.
- Record unresolved ambiguity as open questions instead of forcing certainty.
