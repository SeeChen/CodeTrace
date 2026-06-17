# Build Spec — Artifact Schema

> Stage 2. Concrete, frozen on-disk contract. Derived from `SA.md` §7 and the PRD output schema. The persistence adapter is the only module that may know this layout.

## Directory Topology

```text
<trace_root>/                  # default ".codetrace"
└── <run_id>/                  # one process execution
    ├── summary.json
    └── <trace_name>/          # one traced target (with __<n> collision suffix)
        ├── input.json
        ├── output.json
        ├── metadata.json
        └── compare.json       # only in compare mode
```

- `<run_id>` — file-name-safe ISO 8601 timestamp, e.g. `2026-05-04T10-30-00`. Generated once per process.
- `<trace_name>` — function qualname, file-safe; repeated names get `__2`, `__3`, … within a run.

## File Schemas

### `input.json`
```json
{ "args": ["<jsonable-or-repr>"], "kwargs": {"<key>": "<jsonable-or-repr>"} }
```

### `output.json`
```json
{ "value": "<jsonable-or-repr>", "is_none": false }
```
On user-code exception, no `output.json` is written for that call (the failure is reflected in `metadata.json`).

### `metadata.json`  (authoritative per-trace record)
```json
{
  "name": "my_function",
  "type": "function",
  "time_start": "2026-05-04T10:30:00",
  "time_end": "2026-05-04T10:30:00",
  "duration": 0.0021,
  "compare_mode": false,
  "compare_result": {},
  "metrics": {},
  "failures": [
    { "subsystem": "persistence", "exception_type": "OSError", "message": "..." }
  ]
}
```
`failures` is present only when an isolated infra failure occurred; otherwise omitted or `[]`.

### `compare.json`  (compare mode only)
```json
{ "equal": true, "baseline": "<...>", "candidate": "<...>" }
```
Candidate-exception variant (frozen decision):
```json
{ "status": "candidate_error", "exception_type": "ValueError", "message": "..." }
```

### `summary.json`  (run aggregate, written at exit)
```json
{
  "run_id": "2026-05-04T10-30-00",
  "total": 1,
  "details": [
    {
      "name": "my_function",
      "type": "function",
      "record": {
        "duration": 0.0021,
        "time_start": "2026-05-04T10:30:00",
        "time_end": "2026-05-04T10:30:00",
        "compare_mode": false,
        "compare_result": {},
        "metrics": {}
      }
    }
  ]
}
```
`details[].record` inlines the per-trace record (matches PRD schema); `metadata.json` remains the per-trace source of truth.

## Serialization Rule

All payloads pass through `util/serialization.safe_to_jsonable`: JSON-native values pass through; anything else falls back to `repr(value)`. Serialization must never raise into user code (see `failure-policy.md`).
