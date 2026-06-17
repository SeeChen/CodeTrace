# Build Spec — Failure Policy

> Stage 2. Implementation rules for the inviolable failure-isolation constraint (`SA.md` §6, brief Failure Isolation Policy). Coding must follow this exactly.

## Principle

User-code execution is primary. CodeTrace infrastructure (persistence, compare, record, summary) must never break a successful user call and must never silently swallow its own errors.

## Classification

| Failure source | Policy |
| --- | --- |
| **User code raises** | Propagate unchanged. Skip output persistence for that call. Still attempt to record the call's metadata (timing + a `failures`-style note if applicable) before/while re-raising, but never suppress the original exception. |
| **Persistence error** | Isolate: catch, record, continue. Never re-raise into user code. |
| **Compare error (default/custom hook)** | Isolate: catch, record as a failure; the baseline result is still returned. |
| **Record builder error** | Isolate: fall back to the default record; record the failure. |
| **Summary write error (atexit)** | Isolate: log to stderr; never raise during interpreter shutdown. |
| **Candidate raises (compare mode)** | Not an infra failure — recorded as `compare.json` `status: "candidate_error"`. Baseline result returned normally. |

## Isolation Wrapper

Every infra step runs inside a single helper, e.g.:

```python
def _isolated(subsystem: str, fn, *args, failures: list, logger, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - intentional isolation boundary
        record = {
            "subsystem": subsystem,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
        failures.append(record)
        logger.warning("codetrace %s failure: %s", subsystem, record)
        return None
```

- `subsystem` ∈ {`persistence`, `compare`, `record`, `summary`, `serialization`}.
- Each captured failure is appended to the trace's `failures` list → surfaced in `metadata.json`.
- A broad `except Exception` is **intentional and required** at these boundaries; document it inline.

## Hard Rules

1. The traced call's return value is whatever the user function returned — never replaced by `None` due to an infra failure.
2. User exceptions are re-raised with original type and traceback.
3. No infra failure is silent: it lands in `metadata.json` `failures` and/or the logger.
4. Each failure record carries `subsystem`, `exception_type`, `message`.
5. `safe_to_jsonable` itself must not raise (worst case returns `repr` or a placeholder string).
6. Disabling persistence/summary via config is not a failure — it is a clean no-op path.
