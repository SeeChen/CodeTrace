# CodeTrace System Architecture

## Purpose

This document defines the high-level topology for CodeTrace's MVP architecture and the boundaries that downstream domain specs must preserve.

## Decisions Frozen Here

- The architecture is session-oriented rather than wrapper-only.
- Core orchestration is separated from persistence, comparison, reporting, and extension contracts.
- Local filesystem outputs are the default artifact boundary for the MVP.

## Deferred to Domain Specs

- Exact object model and package names
- Concrete file naming scheme for trace artifacts
- Detailed error classes and adapter method signatures

## Topology

```text
Trigger Layer
  -> Session Runtime
  -> Capture and Timing
  -> Optional Comparison Flow
  -> Record Assembly
  -> Persistence Adapter
  -> Summary Recorder
  -> Output Artifacts
```

## Component Responsibilities

| Component | Responsibility | Notes |
| :-- | :-- | :-- |
| Trigger Layer | Enter tracing from decorator, class decorator, or context manager contracts. | User-facing API surface. |
| Session Runtime | Build trace-session state, coordinate lifecycle steps, and preserve user semantics. | Core orchestration center. |
| Capture and Timing | Collect start/end timestamps, duration, trace identity, and callable metadata. | Must stay lightweight. |
| Comparison Flow | Execute baseline and candidate under a shared input set and produce comparable payloads. | Must remain extensible toward multi-variant future work. |
| Record Assembly | Produce normalized dictionary-like records from runtime context. | Supports custom record builders. |
| Persistence Adapter | Save inputs, outputs, comparison artifacts, and future replay assets. | Must isolate filesystem and format concerns. |
| Summary Recorder | Aggregate per-trace records into a run-level summary. | May flush at exit and via explicit hooks. |
| Extension Contracts | Provide compare, record, and future metrics collector seams. | Should use small explicit contracts. |

## Architectural Constraints

- The runtime cannot assume only one tracing trigger style.
- The persistence adapter cannot own core orchestration decisions.
- Comparison logic cannot be hard-wired in a way that blocks multi-variant evolution.
- Summary generation must tolerate infrastructure failures and preserve main execution correctness.

## Open Questions

- Whether summary recording should be synchronous on each trace, deferred until exit, or support both modes by policy.
