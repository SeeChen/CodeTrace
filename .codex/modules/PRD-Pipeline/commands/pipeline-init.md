# Command: pipeline-init

## Purpose

Normalize the PRD into the active intent pack used by the rest of the workflow.

## Direct Invocation

- `/pipeline-init`
- `/pipeline-init --refresh`

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Refactor-Blueprint.md`
4. `.codex/modules/PRD-Pipeline/agents/prd-analyst-agent.md`
5. `.codex/modules/PRD-Pipeline/skills/normalize-prd/SKILL.md`
6. `.codex/modules/PRD-Pipeline/rules/agent-skill-design.md`

## Execute

1. Reconstruct the project mission, scope, constraints, and acceptance framing from the PRD.
2. Define deterministic file-schema expectations when runtime artifacts are part of the PRD.
3. Define concrete failure-isolation behavior for persistence, reporting, comparison, and other infrastructure paths.
4. Convert resolvable uncertainty into explicit MVP decisions before recording remaining open questions.
5. Write the intent pack to `specs/intent/brief.md`.
6. Record unresolved issues in `memory/open-questions.md`.
7. Update `memory/pipeline-state.md`.

## Brief Generation Contract

The generated `specs/intent/brief.md` must be structured enough for downstream AI agents to use as a single source of truth.

Required sections:

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

For CodeTrace-like local artifact workflows, the generated brief must include:

1. a concrete `.codetrace/<run_id>/<trace_name>/` artifact topology
2. explicit failure-isolation behavior using try-except encapsulation
3. default MVP decisions for `run_id`, non-serializable fallback, comparison failure behavior, and deferred context-manager tracing
4. AI execution guidance for Google-style docstrings, `pytest`, deterministic paths, and test mapping for every core action

## Output

- `specs/intent/brief.md`
