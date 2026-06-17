# Frozen Decisions

## Purpose

This file stores architectural and workflow decisions that downstream stages should not silently override.

## Current Decisions

1. The active workflow is `PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`.
2. Generated outputs use the `specs/intent`, `specs/architecture`, `specs/build`, and `specs/acceptance` structure.
3. Agents and skills should remain lightweight and rely on `docs/` for deeper reference material.
4. The orchestration module lives under `.claude/` (`agents`, `commands`, `skills`, `rules`, `memory`, `docs`) as the single source of truth.
5. The public command surface is unified under `/seechen`, with defined flags for known stages and intent routing for natural-language requests.

## Architecture Decisions (Stage 1, from `specs/architecture/SA.md`)

6. Four-layer architecture — Core / Adapter / Utility / Contract — with one-directional dependency `Core → Adapter → Utility`, all over `Contract`; no upward or cyclic imports.
7. Public API surface = `TraceFunc.config(...)` + `TraceFunc.__call__(...)` decorator + three Contract hooks (record builder, compare callable, persistence interface); these shapes are frozen for the MVP.
8. Cross-layer communication happens only through Contract interfaces, so A/B, replay, metrics, and block/class tracing stay additive.
9. Trace session creation is lazy; the run summary is written at process exit via an atexit hook.
10. The compare coordinator must not hard-code "exactly one candidate" in a way that blocks future multi-variant A/B.
11. Default serialization is JSON; non-serializable values fall back to `repr(value)`; `run_id` is a file-name-safe ISO 8601 timestamp; persistence topology is `.codetrace/<run_id>/{summary.json, <trace_name>/{input,output,metadata,compare}.json}`.
12. Return transparency, exception transparency, and failure isolation (SA §6.1–§6.3) are inviolable by any later stage.

## Build-Spec Decisions (Stage 2, from `specs/build/*`)

13. Run session is a module-level singleton: one `run_id` per process, shared by all `TraceFunc` instances, created lazily on first traced call.
14. `<trace_name>` = function qualname (file-safe); repeated names within a run get a `__<n>` suffix starting at `__2`.
15. `summary.json` inlines each per-trace record (PRD schema); `metadata.json` remains the authoritative per-trace artifact.
16. Candidate (`new_function`) exceptions are recorded in `compare.json` as `status: "candidate_error"` (type + message), not as infra failures; the baseline result is still returned.
17. Package layout is `src/codetrace/` with Core modules at top level, `adapters/` (persistence) and `util/` subpackages; only `adapters/persistence.py` knows the on-disk JSON layout.
18. All infra steps run inside one `_isolated(subsystem, ...)` wrapper; captured failures carry `subsystem`/`exception_type`/`message` and surface in `metadata.json` `failures`.

## Notes

- Product- and implementation-level decisions (for example artifact schema, identifiers, or serialization fallbacks) are derived during the pipeline run and recorded here as each stage freezes them.
