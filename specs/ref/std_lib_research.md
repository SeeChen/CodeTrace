# CodeTrace Standard Library Research

## Purpose

This document narrows the Python standard-library search space for CodeTrace's MVP and near-term extension points. It is a candidate map, not a final implementation proof.

## Source Documents

- `docs/PRD.md`
- `docs/Workflow.md`

## Research Scope

The PRD requires a zero-external-dependency, local-first tracing framework with decorator, class, and context-manager triggers; deterministic artifact persistence; structured summaries; compare hooks; and future metrics-readiness.

## Standard Library Candidates

| Capability Area | Candidate Module or Mechanism | Expected Role | Benefits | Risks or Limits | Source |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Decorator instrumentation | `functools.wraps`, plain call wrappers | Preserve metadata while wrapping user callables. | Lightweight and idiomatic for function and method tracing. | Does not help with arbitrary line-level tracing by itself. | PRD 3 / FR-01 |
| Callable inspection | `inspect`, `types`, `inspect.signature` | Capture callable identity, arguments, and class-method eligibility. | Helps normalize method/class tracing and public API documentation. | Bound-method and inherited-method behavior must be handled carefully. | PRD 3 / FR-01, FR-09 |
| Timing | `time.perf_counter`, `time.perf_counter_ns`, `datetime` | Measure execution duration and capture wall-clock metadata. | Standard, accurate enough for local benchmarking and summary output. | Wall-clock timestamps and duration clocks should not be conflated. | PRD 3 / FR-01, PRD 6 |
| Filesystem paths | `pathlib`, `os`, `tempfile` | Build deterministic run and trace directories. | Clear path composition and cross-platform local-first support. | Windows path and filename constraints still need normalization. | PRD 3 / FR-02, PRD 4 |
| Serialization | `json`, `pickle`, `dataclasses.asdict`, custom safe fallback | Persist inputs, outputs, and comparison artifacts through a stable contract. | Supports structured text-first storage with optional richer fallbacks. | Arbitrary objects may not be JSON-serializable; `pickle` adds reviewability tradeoffs. | PRD 3 / FR-02, FR-12 |
| Hashing and identity | `hashlib`, `uuid`, deterministic string normalization | Generate run and trace identities and optional content hashes. | Predictable IDs can support replay-ready organization. | Hash input canonicalization must be explicit to stay deterministic. | PRD 4, PRD 6 |
| Logging | `logging` | Report infrastructure failures without breaking user execution. | Matches robustness requirements and configurable behavior. | Logging configuration can become invasive if global handlers are modified carelessly. | PRD 3 / FR-07, PRD 4 |
| Context manager support | `contextlib` | Build block tracing and lifecycle wrappers. | Native support for `with`-based tracing. | API shape still needs a project-specific contract. | PRD 3 / FR-08 |
| Exception propagation | `traceback`, `contextlib`, standard `try/finally` flow | Preserve user exceptions while still capturing trace metadata and reporting failures. | Supports the PRD rule that tracing failures must not corrupt main execution flow. | Exception-path persistence must avoid masking original failures. | PRD 4 |
| Exit-time summary | `atexit` | Flush run summary at process exit. | Aligns well with PRD summary expectations. | Ordering with interpreter shutdown and abrupt termination needs graceful fallback. | PRD 3 / FR-03 |
| Thread-local context | `threading.local`, `contextvars` | Isolate per-execution state for nested calls or future concurrency support. | Provides a path to avoid shared mutable global runtime state. | The PRD is local-first, but concurrency behavior is still unspecified and needs validation. | PRD 4, PRD 7 |
| In-memory buffering | `queue`, `collections.deque` | Future buffering of records before summary or persistence flush. | Useful if persistence needs isolation from hot paths later. | Could add complexity before it is justified by MVP behavior. | PRD 4, PRD 5 |

## Risks and Boundary Notes

- `sys.settrace` exists in the standard library but is likely too invasive for the MVP's decorator-first contract. It should stay a research note rather than a default architectural choice.
- JSON should be the preferred human-reviewable artifact format, but the system needs a clear fallback strategy for non-serializable values.
- `atexit` supports summary generation, but explicit flush hooks may still be needed for testability and abnormal shutdown cases.
- If class tracing includes inherited methods, `inspect`-based discovery rules must avoid wrapping dunder methods or unrelated descriptors unintentionally.
- Thread-aware runtime state should remain optional unless domain specs confirm concurrent tracing requirements.

## Recommended Validation Tasks

1. Validate argument capture behavior for positional-only, keyword-only, varargs, and bound methods.
2. Decide the default artifact serialization ladder for non-JSON-friendly values.
3. Validate deterministic trace directory naming on Windows and POSIX paths.
4. Measure wrapper overhead using `perf_counter_ns` for very fast functions and nested traces.
5. Confirm whether `threading.local` or `contextvars` better fits nested trace-session state.
6. Validate that `atexit` summary flushes remain reliable in normal process termination and test harness execution.

## Open Questions

- Should the MVP ever use `pickle` as an opt-in adapter, or should all default persistence remain text-oriented for reviewability?
- Is concurrency support limited to safe isolation, or should the MVP also document behavior under multi-threaded traced calls?
