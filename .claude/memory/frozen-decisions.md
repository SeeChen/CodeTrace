# Frozen Decisions

## Purpose

This file stores architectural and workflow decisions that downstream stages should not silently override.

## Current Decisions

1. The active workflow is `PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`.
2. New workflow assets should prefer the smaller `specs/intent`, `specs/architecture`, `specs/build`, and `specs/acceptance` structure.
3. Agents and skills should remain lightweight and rely on `docs/` for deeper reference material.
4. The orchestration module lives under `.claude/` (`agents`, `commands`, `skills`, `rules`, `memory`, `docs`) as the single source of truth; the legacy `.codex/` tree and stale generated `specs/` outputs are removed so active runs do not mix structures.
5. The public command surface should be unified under `/seechen`, with defined flags for known stages and intent routing for natural-language requests.
6. Runtime artifacts default to `.codetrace/<run_id>/<trace_name>/` with `input.json`, `output.json`, `metadata.json`, and optional `compare.json`.
7. `run_id` defaults to an ISO 8601 timestamp safe for file names.
8. Non-serializable values fall back to `repr(value)` in the MVP.
9. Persistence, reporting, and comparison failures must be isolated with try-except encapsulation and recorded through `stderr`, internal logging, or metadata.
10. Comparison failures are recorded as artifacts and metadata by default, not raised, unless a future explicit strict mode is introduced.
11. Context-manager tracing remains a reserved extension path until function and method tracing are stable.
12. Public Python APIs and extension contracts must use Google-style docstrings.
13. Every core action must map to at least one unit or integration test.
