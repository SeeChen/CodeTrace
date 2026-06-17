# Build Spec — Task Slices

> Stage 3. Ordered, file-scoped implementation tasks derived from `module-map.md`, `file-plan.md`, `interfaces.md`, `artifact-schema.md`, `failure-policy.md`, and `test-matrix.md`. Each task is small enough for a coding agent to own with non-overlapping write scope. Implement top-to-bottom.

## Conventions

- **Write scope** is exclusive per task where possible; shared touch-points are called out.
- Every code task names its **required tests** (from `test-matrix.md`).
- Style: Google Python Style Guide, Google-style docstrings on public APIs, `snake_case`, no manual alignment.

---

## T0 — Project scaffolding

- **Purpose:** create the package skeleton and test layout so later tasks have stable import paths.
- **Files:** `src/codetrace/__init__.py` (empty export stub), `src/codetrace/adapters/__init__.py`, `src/codetrace/util/__init__.py`, `tests/conftest.py`, `pyproject.toml` (or `setup.cfg`) for an installable, dependency-free package + `pytest` config.
- **Prerequisites:** none.
- **Outputs:** importable `codetrace` package; `pytest` runs (zero tests pass).
- **Tests:** smoke import test optional.
- **Acceptance:** `pip install -e .` works; `pytest` exits 0; no external runtime deps declared.

## T1 — Contracts

- **Purpose:** define the Contract layer (dependency-free).
- **Files:** `src/codetrace/contracts.py`.
- **Prerequisites:** T0.
- **Outputs:** `RecordBuilder`, `CompareCallable` type aliases; `PersistenceAdapter` Protocol; reserved `MetricsCollector` Protocol; shared record/summary TypedDicts or dataclasses (per `interfaces.md`).
- **Tests:** `tests/unit/test_contracts.py` — import + Protocol structural checks (a dummy adapter satisfies `PersistenceAdapter`).
- **Acceptance:** imports nothing from Core/Adapter/Utility.

## T2 — Utility: serialization

- **Purpose:** safe JSON encoding with `repr` fallback that never raises.
- **Files:** `src/codetrace/util/serialization.py`.
- **Prerequisites:** T0.
- **Outputs:** `safe_to_jsonable(value) -> Any`.
- **Tests:** `test_serialization.py` — native passthrough; non-serializable → `repr`; never raises (edge case 3).
- **Acceptance:** frozen decision (non-serializable → `repr`) + failure rule 5 hold.

## T3 — Utility: paths & run_id

- **Purpose:** deterministic paths, `run_id` generation, trace-name collision suffixing.
- **Files:** `src/codetrace/util/paths.py`.
- **Prerequisites:** T0.
- **Outputs:** `generate_run_id() -> str`; `prepare_trace_dir(root, run_id, trace_name) -> Path`; `resolve_trace_name(existing: set[str], qualname) -> str` (applies `__<n>`).
- **Tests:** `test_paths.py` — `run_id` matches file-safe ISO 8601, no illegal chars; collision → `name`, `name__2`, `name__3`.
- **Acceptance:** frozen decisions (run_id format, `__<n>` suffix) hold.

## T4 — Utility: timing & logging

- **Purpose:** monotonic timing + ISO timestamps; logger for isolated failures.
- **Files:** `src/codetrace/util/timing.py`, `src/codetrace/util/logging_setup.py`.
- **Prerequisites:** T0.
- **Outputs:** `Timer` (or `start()/stop()` returning duration + ISO `time_start`/`time_end`); `get_logger() -> logging.Logger`.
- **Tests:** `test_timing.py` — duration ≥ 0, timestamps well-formed.
- **Acceptance:** timing fields match `metadata.json` schema.

## T5 — Persistence adapter

- **Purpose:** default JSON adapter — the only module that knows the on-disk layout.
- **Files:** `src/codetrace/adapters/persistence.py`.
- **Prerequisites:** T1, T2, T3.
- **Outputs:** `JsonPersistenceAdapter` implementing all `save_*` methods, writing the `artifact-schema.md` topology via `safe_to_jsonable` + `paths`.
- **Tests:** `test_persistence.py` — files land under `<run_id>/<trace_name>/`; `output.json` `is_none` for None; summary shape; missing/invalid dir handled (edge cases 2, 4, 6).
- **Acceptance:** satisfies `PersistenceAdapter` Protocol; no tracing logic present.

## T6 — Config

- **Purpose:** global defaults + per-call override merge + key validation.
- **Files:** `src/codetrace/config.py`.
- **Prerequisites:** T1.
- **Outputs:** `Config` dataclass with defaults from `interfaces.md`; `merge(overrides)`; unknown-key → `ValueError`; accepts reserved `metrics_collectors` inertly.
- **Tests:** `test_config.py` — defaults, override scoping, unknown key raises (FR-07).
- **Acceptance:** override produces a new scoped config without mutating global.

## T7 — Recorder

- **Purpose:** default record builder + summary aggregation.
- **Files:** `src/codetrace/recorder.py`.
- **Prerequisites:** T1, T4.
- **Outputs:** `default_record_builder(context) -> dict`; `build_summary(run_id, records) -> dict` inlining each record (PRD schema).
- **Tests:** `test_recorder.py` — context keys consumed; summary `total`/`details[].record` correct; custom builder honored (FR-03, FR-06).
- **Acceptance:** summary inlines record (frozen #15).

## T8 — Compare

- **Purpose:** compare coordinator + default compare callable; candidate-exception handling.
- **Files:** `src/codetrace/compare.py`.
- **Prerequisites:** T1, T2.
- **Outputs:** `default_compare(baseline, candidate, context) -> dict` (`equal` + serialized values); coordinator that runs the candidate under the same inputs and returns a result; candidate raise → `{"status": "candidate_error", ...}`.
- **Tests:** `test_compare.py` — equal/diff (edge case 5); custom compare injected (FR-05); candidate raises while baseline ok → `candidate_error`, baseline returned (frozen #16).
- **Acceptance:** coordinator does not hard-code exactly one candidate in a blocking way (SA extension rule).

## T9 — Session

- **Purpose:** module-level singleton run session.
- **Files:** `src/codetrace/session.py`.
- **Prerequisites:** T3, T4.
- **Outputs:** `get_or_create_session(config) -> Session`; `Session.run_id`, `Session.register(record)`, lazy run-dir creation, `atexit`-registered summary flush; a `reset_session()` test hook.
- **Tests:** covered via `test_tracer.py` (singleton sharing) + summary-at-exit integration.
- **Acceptance:** one `run_id` per process shared across `TraceFunc` instances (frozen #13); summary write isolated at exit.

## T10 — Tracer (executor + TraceFunc)

- **Purpose:** the public entry and trace executor wiring everything together with failure isolation.
- **Files:** `src/codetrace/tracer.py`; update `src/codetrace/__init__.py` to export `TraceFunc`.
- **Prerequisites:** T5, T6, T7, T8, T9.
- **Outputs:** `TraceFunc.config(...)`, `TraceFunc.__call__(...)` decorator; executor: timer → baseline (+candidate) → isolated persist/compare/record → register; return transparency + exception propagation; `_isolated(subsystem, ...)` wrapper (failure-policy).
- **Tests:** `test_tracer.py` — return semantics unchanged (FR-01); exception propagates, no `output.json`, metadata attempted (edge case 1); per-call override (FR-07); collision dirs (frozen #14); singleton session (frozen #13); each infra subsystem failure isolated + recorded (failure-policy tests); storage swappable (FR-10).
- **Acceptance:** all cross-cutting rules (SA §6) hold; talks to adapters only via contracts.

## T11 — Integration & summary end-to-end

- **Purpose:** prove the end-to-end flow and summary emission.
- **Files:** `tests/integration/test_decorator_end_to_end.py`, `tests/integration/test_compare_end_to_end.py`.
- **Prerequisites:** T10.
- **Outputs:** decorate → run → assert full artifact tree + `summary.json`; compare run → `compare.json`; multiple traced functions in one run (edge case 6).
- **Tests:** the integration suite itself.
- **Acceptance:** `summary.json` total/details correct; artifact topology matches `artifact-schema.md`.

## T12 — Coverage & style gate

- **Purpose:** meet the quality gates.
- **Files:** test additions as needed; no new source modules.
- **Prerequisites:** T11.
- **Outputs:** core modules > 90% line coverage; every public API/contract directly tested; docstrings present.
- **Tests:** `pytest --cov` report; fill coverage gaps.
- **Acceptance:** gates in `test-matrix.md` satisfied; Google style respected.

---

## Dependency Graph (summary)

```text
T0
├─ T1 contracts ─────────────┐
├─ T2 serialization ──┐      │
├─ T3 paths ──────────┤      │
└─ T4 timing/logging ─┤      │
                      ▼      ▼
                 T5 persistence   T6 config   T7 recorder   T8 compare
                          └──────────┴───────────┴──────────┴──► T9 session ──► T10 tracer ──► T11 integration ──► T12 gate
```

## Traceability

Every task cites its build-spec source; every FR, frozen decision (#13–#18), and mandatory edge case in `test-matrix.md` is covered by at least one task's required tests. Edge cases 7–8 (metrics, replay) are reserved seams and intentionally untested in the MVP.
