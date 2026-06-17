# Build Spec — Test Matrix

> Stage 2. Maps every important requirement, frozen decision, and mandatory edge case to test intent. Target: >90% line coverage on core modules; every public API and contract has direct coverage (brief Acceptance Framing).

## Requirement → Test Intent

| Source | Requirement | Test intent | Where |
| --- | --- | --- | --- |
| FR-01 | Function tracing preserves return semantics; records timing | decorate fn; assert identical return + metadata has duration/timestamps | `test_tracer`, `test_decorator_end_to_end` |
| FR-02 | Persist inputs/outputs to isolated per-run/per-trace dir | assert `input.json`/`output.json` exist under `<run_id>/<trace_name>/` | `test_persistence`, integration |
| FR-03 | Summary at process exit with total + per-trace details | trigger summary flush; assert `summary.json` shape (`run_id`,`total`,`details[]`) | `test_recorder`, integration |
| FR-04 | Baseline vs candidate comparison emits structured result | trace with `new_function`; assert `compare.json` with `equal` | `test_compare`, `test_compare_end_to_end` |
| FR-05 | Custom compare callable replaces default w/o core change | inject custom compare; assert it is invoked, core flow unchanged | `test_compare` |
| FR-06 | Custom record builder receives context, returns dict | inject record builder; assert context keys + payload used | `test_recorder`, `test_tracer` |
| FR-07 | Global config + per-call override | set global then override per-call (e.g. `persistence=False`); assert scoping | `test_config`, `test_tracer` |
| FR-10 | Storage isolated from engine | assert `tracer` has no direct on-disk knowledge; swap adapter in test | `test_tracer`, `test_persistence` |

## Frozen Decision → Test Intent

| Decision | Test intent | Where |
| --- | --- | --- |
| `run_id` = file-safe ISO 8601 | assert generated id matches pattern, no illegal path chars | `test_paths` |
| Non-serializable → `repr` | pass unserializable object; assert `repr` string stored, no raise | `test_serialization` |
| `<trace_name>` collision → `__<n>` | trace same fn twice; assert `name` and `name__2` dirs | `test_paths`, `test_tracer` |
| Summary inlines record | assert `details[].record` matches `metadata.json` record | `test_recorder` |
| Module-level singleton session | two `TraceFunc` instances share one `run_id` in a process | `test_tracer` |
| Candidate exception → `candidate_error` | candidate raises, baseline ok; assert `compare.json` status + baseline returned | `test_compare` |

## Mandatory Edge Cases (PRD §7)

| # | Edge case | Expected |
| --- | --- | --- |
| 1 | Function raises | exception propagates unchanged; no `output.json`; metadata still attempted |
| 2 | Function returns `None` | `output.json` `is_none: true`; no error |
| 3 | Non-serializable input/output | `repr` fallback; no raise into user code |
| 4 | Missing/invalid output dir | persistence failure isolated + recorded; user call still returns |
| 5 | Compare candidate differs from baseline | `compare.json` `equal: false` with both values |
| 6 | Multiple traced fns in one process | all appear in `summary.json` `details`; `total` correct |
| 7 | (reserved) metrics collector fails | seam only — not tested in MVP |
| 8 | (reserved) partial/corrupt replay artifacts | seam only — not tested in MVP |

## Failure-Isolation Tests

- Force each subsystem (persistence/compare/record) to raise via monkeypatch; assert user return is intact and a `failures` entry with `subsystem`/`exception_type`/`message` is recorded.
- Force summary write error at exit; assert no exception escapes.

## Framework & Gates

- `pytest`; `tmp_path` for trace roots; a fixture resets the module-level session between tests.
- Gate: core modules (`tracer`, `compare`, `recorder`, `persistence`, `paths`, `serialization`) > 90% line coverage; every public API / contract directly exercised.
