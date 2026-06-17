# CodeTrace System Architecture (SA)

> Stage 1 architecture. Derived from `specs/intent/brief.md`. Once frozen, downstream build-spec generation implements against these boundaries and must not casually redefine them. Architecture-level frozen decisions are mirrored in `.claude/memory/frozen-decisions.md`.

## 1. System Context

CodeTrace is an in-process Python library. It instruments user-selected functions/methods, captures runtime evidence, optionally compares a candidate against a baseline, persists artifacts to the local file system, and emits a run summary at process exit.

```text
        ┌─────────────────────────────────────────────┐
        │                User Process                  │
        │                                              │
  call  │   user code ──► [TraceFunc decorator] ──►    │  return (unchanged)
 ─────► │                      │                       │ ─────►
        │                      ▼                       │
        │             Core (trace session)            │
        │           │        │        │        │       │
        │        timing   persist   compare   record   │
        │                      │                       │
        │                      ▼                       │
        │             Summary recorder (atexit)        │
        └──────────────────────┬───────────────────────┘
                               ▼
                       .codetrace/<run_id>/...
```

- **Boundary:** everything runs inside the user's process; no network, no daemon, no external service.
- **Primary invariant:** the traced call's return value and exception behavior are identical to the un-traced call.

## 2. Module Boundaries

Four layers, matching the intent pack. Each layer depends only on layers below it (Contract is depended on by all).

| Layer | Responsibility | Must NOT do |
| --- | --- | --- |
| **Core** | Trace orchestration, session/run identity, execution timing, lifecycle coordination, compare coordination, summary aggregation. | Know concrete file formats or serialization details. |
| **Adapter** | Persistence (write artifacts), report/summary emission, and reserved seams for metrics collectors / alternate storage. | Contain tracing/orchestration logic. |
| **Utility** | Timing, file-name-safe `run_id` generation, safe JSON serialization (with `repr` fallback), path preparation, logger setup. | Hold trace state or business decisions. |
| **Contract** | Callable protocols and shared schemas: record-builder, compare callable, persistence interface, (reserved) metrics collector. | Import Core/Adapter (contracts are dependency-free). |

**Dependency rule (frozen):** `Core → Adapter → Utility`, and all may depend on `Contract`. No upward or cyclic imports. This is the seam that keeps comparison, persistence, reporting, and future metrics independently replaceable.

### Core responsibilities decomposed

- **Trace session** — owns one `run_id`, the active config, and the live collection of trace records for the process.
- **Trace executor** — wraps a single call: start timer → run user code → stop timer → hand off to persistence/compare/record → register the record. User-code exceptions bypass infra steps and propagate (see §6).
- **Compare coordinator** — when a candidate is supplied, runs it under the same inputs and invokes the compare callable; never blocks the baseline result.
- **Summary recorder** — aggregates registered records and writes `summary.json` at process exit.

## 3. Public API Surface (stable contract)

The following surface is frozen for the MVP; downstream stages may add behind it but must not change these shapes.

1. **`TraceFunc`** — primary entry object.
   - `TraceFunc.config(**options)` — set global defaults: logging on/off, persistence on/off, summary on/off, trace root, default compare callable, default record builder. Reserved keys for future collectors are accepted but inert.
   - `TraceFunc.__call__(*, new_function=None, compare=None, record=None, **overrides)` — returns a decorator. Per-call overrides shadow global config for that target only.
2. **Decorated callable** — same signature, same return value, same exception behavior as the original.
3. **Hook contracts** (from the Contract layer):
   - **Record builder** — `(context: dict) -> dict`. Receives runtime metadata (name, type, timing, identity, compare flag/result), returns the record payload persisted into `metadata.json` / summarized.
   - **Compare callable** — `(baseline_output, candidate_output, context: dict) -> dict`. Returns a structured comparison result for `compare.json`.
   - **Persistence interface** — stable `save`-style methods for inputs, outputs, metadata, compare artifacts; the default adapter writes JSON to the deterministic schema.

**Reserved (defined, not shipped):** `TraceBlock` / context-manager contract, class-decorator contract, and metrics-collector lifecycle (`start`/`stop`/`emit`). These have named seams but no MVP implementation.

## 4. Extension Points

| Extension point | Mechanism | MVP status |
| --- | --- | --- |
| Custom comparison | inject `compare` callable (global or per-call) | shipped |
| Custom record assembly | inject `record` builder (global or per-call) | shipped |
| Alternate storage / format | new persistence adapter behind the persistence interface | seam only |
| Runtime metrics (memory, etc.) | metrics-collector lifecycle attached to the trace executor | seam only |
| Multi-variant A/B | compare coordinator generalized from 1 baseline + 1 candidate to N candidates | seam only (do not hard-code "exactly one candidate" in a way that blocks this) |
| Replay / self-regression | deterministic, predictably named artifacts re-loaded as inputs | seam only (guaranteed by the file schema) |
| Block / class tracing | additional trigger surfaces feeding the same trace session | seam only |

The architectural rule that keeps all of these additive: **the trace executor talks to compare/persist/record/metrics only through Contract-layer interfaces**, never via concrete classes.

## 5. Runtime Lifecycle

```text
config (optional, once)
   │
   ▼
first trace use ──► acquire/create trace session (assign run_id, prepare .codetrace/<run_id>/)
   │
   ▼  (per traced call)
start timer
   │
   ├─ run baseline (user code)            ◄── return value captured, exceptions propagate
   ├─ [if new_function] run candidate
stop timer
   │
   ├─ persist input.json / output.json          (isolated, §6)
   ├─ [if compare] run compare callable ─► compare.json   (isolated)
   ├─ build record ─► metadata.json             (isolated)
   └─ register record in session
   │
   ▼
return user result to caller (always)
   ...
process exit (atexit) ──► summary recorder writes summary.json
```

- **Session creation is lazy:** the run directory is created on first trace, not at import.
- **Summary emission is at process exit** via an `atexit`-style hook; if disabled by config, no summary is written.

## 6. Cross-Cutting Constraints (frozen)

These bind every downstream stage:

1. **Return transparency** — the traced call returns exactly what the original returns; CodeTrace never substitutes or mutates it.
2. **Exception transparency** — user-code exceptions propagate unchanged; infra steps are skipped for a failed call but the exception still surfaces (and the failure may still be recorded in metadata before re-raising).
3. **Failure isolation** — persistence, compare, and report steps are each wrapped in try-except. An infra failure is recorded (subsystem, exception type, message) via logger/`stderr`/`metadata.json` and never interrupts a successful user call, never silently swallowed.
4. **Zero dependency / local-first** — standard library only for the MVP; all artifacts are local files.
5. **Determinism** — `run_id` is a file-name-safe ISO 8601 timestamp; artifact paths follow the frozen schema; non-serializable values fall back to `repr(value)`.
6. **Layer isolation** — Core never imports concrete adapters; everything crosses layers through Contract interfaces.
7. **Style** — Google Python Style Guide, `snake_case` modules, Google-style docstrings on public APIs/contracts.

## 7. Persistence Schema (frozen topology)

Carried forward from the intent brief as the architectural data contract:

```text
.codetrace/
└── <run_id>/                  # one process execution (ISO-8601 file-safe timestamp)
    ├── summary.json           # run aggregate: run_id, total, details[]
    └── <trace_name>/          # one traced target
        ├── input.json         # serialized args/kwargs
        ├── output.json        # serialized return value
        ├── metadata.json      # timing, identity, compare flag, isolated-failure records
        └── compare.json       # structured compare result (compare mode only)
```

`summary.json` shape follows the PRD output schema (`run_id`, `total`, `details[].record{duration, time_start, time_end, compare_mode, compare_result, metrics}`).

## 8. Frozen Decisions (this stage)

1. Four-layer architecture (Core / Adapter / Utility / Contract) with one-directional dependency `Core → Adapter → Utility`, all over `Contract`.
2. Public API surface = `TraceFunc.config` + `TraceFunc.__call__` decorator + three Contract hooks (record / compare / persistence); shapes frozen for MVP.
3. Cross-layer communication only through Contract interfaces (enables additive A/B, replay, metrics, block/class tracing).
4. Lazy session creation; summary written at process exit via atexit hook.
5. Compare coordinator must not hard-code "exactly one candidate" in a way that blocks future multi-variant A/B.
6. Default serialization = JSON; non-serializable → `repr`; `run_id` = file-safe ISO 8601 timestamp; persistence topology per §7.
7. The four cross-cutting transparency/isolation rules (§6.1–§6.3) are inviolable by any later stage.

## 9. Open Questions (carried to build spec)

1. **Session sharing model** — is the trace session a module-level singleton, or explicitly attached to each `TraceFunc` instance? (Affects how multiple `TraceFunc` objects in one process share a `run_id`.) → resolve in `generate-spec`.
2. **`<trace_name>` collisions** — when the same function name is traced multiple times in one run, how are trace directories disambiguated (call index suffix vs. overwrite)? → resolve in `generate-spec`.
3. **Summary detail granularity** — does `summary.json` inline full per-trace records or reference `metadata.json`? (Brief Open Question #2.) → freeze the summary schema in `generate-spec`.
4. **Candidate exception policy** — if the candidate (`new_function`) raises but the baseline succeeds, is that recorded as a compare result or an isolated infra failure? → resolve in `generate-spec`.
