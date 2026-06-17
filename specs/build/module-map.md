# Build Spec — Module Map

> Stage 2. Derived from `specs/architecture/SA.md` and `specs/intent/brief.md`. Implementation-facing module decomposition for the CodeTrace MVP.

## Artifact Scope Decision (doc-scope rule)

CodeTrace is a single in-process Python library, moderate complexity, but contract-heavy (3 hooks), schema-driven (deterministic file topology), and failure-isolation-critical. All six baseline build-spec artifacts are therefore **required**:

| Artifact | Status | Why |
| --- | --- | --- |
| `module-map.md` | required | multiple modules across 4 layers need explicit ownership |
| `interfaces.md` | required | 3 frozen hook contracts + public API must be unambiguous |
| `file-plan.md` | required | maps modules to concrete files before coding |
| `artifact-schema.md` | required | deterministic JSON topology is a hard product contract |
| `failure-policy.md` | required | failure isolation is an inviolable cross-cutting rule |
| `test-matrix.md` | required | >90% coverage + 8 mandatory edge cases must be traceable |

No artifacts merged or deferred — each maps to a distinct, non-trivial concern in this project.

## Module Inventory

Layer ownership follows the frozen dependency rule: `Core → Adapter → Utility`, all over `Contract`.

| Module | Layer | Responsibility | Key collaborators |
| --- | --- | --- | --- |
| `contracts` | Contract | Type aliases / Protocols for record-builder, compare callable, persistence interface, (reserved) metrics collector; shared record/summary dataclasses or TypedDicts. | imported by all |
| `config` | Core | Holds global defaults; merges per-call overrides; validates option keys. | `TraceFunc` |
| `session` | Core | Module-level run session: owns `run_id`, registers trace records, triggers summary at exit. | `recorder`, `persistence` |
| `tracer` | Core | `TraceFunc` entry: `config(...)` + `__call__(...)` decorator; the trace executor (timing, baseline/candidate run, orchestration, failure isolation). | `session`, `compare`, `persistence`, `contracts`, `timing` |
| `compare` | Core | Compare coordinator + default compare callable; runs candidate under same inputs, produces compare result. | `contracts` |
| `recorder` | Core | Default record builder; aggregates registered records into the summary payload. | `contracts` |
| `persistence` | Adapter | Default JSON persistence adapter implementing the persistence interface; writes input/output/metadata/compare/summary. | `serialization`, `paths`, `contracts` |
| `serialization` | Utility | Safe JSON encoding with `repr(value)` fallback for non-serializable values. | — |
| `paths` | Utility | Build/prepare deterministic `.codetrace/<run_id>/<trace_name>/` paths; `run_id` generation; collision suffixing. | — |
| `timing` | Utility | Monotonic timing + ISO 8601 start/end timestamps. | — |
| `logging_setup` | Utility | Logger configuration for isolated-failure reporting. | — |

## Resolved Open Questions (carried from SA §9)

These were owned by Stage 2 and are now frozen:

1. **Session sharing model** → **module-level singleton run session.** One `run_id` per process; all `TraceFunc` instances share it. Lazily created on first traced call.
2. **`<trace_name>` collisions** → trace directory name = function qualified name (file-safe). On repeat within a run, append `__<n>` starting at `__2` (`my_func`, `my_func__2`, …).
3. **Summary detail granularity** → `summary.json` **inlines** the per-trace record (matches the PRD output schema) and `metadata.json` is also written per trace as the authoritative per-trace artifact.
4. **Candidate exception policy** → if `new_function` raises while the baseline succeeds, it is recorded as a **compare result** (`status: "candidate_error"` with exception type/message) in `compare.json`, **not** as an infra failure. The baseline result is returned to the caller unchanged.

## Build Order (informs Stage 3 slicing)

1. `contracts`, then Utility (`serialization`, `paths`, `timing`, `logging_setup`)
2. `persistence` adapter
3. `config`, `session`, `recorder`
4. `tracer` (executor) + `compare`
5. Wire-up, summary-at-exit, end-to-end
