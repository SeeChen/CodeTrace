# CodeTrace Performance Baseline Plan

## Purpose

This document defines the initial performance-budget frame for CodeTrace. It describes how overhead should be measured and reviewed; it does not claim benchmark results.

## Source Documents

- `docs/PRD.md`
- `docs/Workflow.md`

## Budget Framing

- The workflow references a `15%` performance budget as a milestone-level quality gate.
- The PRD states that tracing overhead must remain low relative to underlying execution and that optional future metrics must be opt-in rather than unconditional cost.
- Engineering inference: the immediate MVP should treat `15%` as the default acceptable median overhead target for representative scenarios, with extra scrutiny for very fast functions where fixed wrapper cost can dominate.

## Baseline Definition

Baseline behavior is the same user code executed without CodeTrace instrumentation, persistence, or comparison logic enabled.

## Overhead Definition

Tracing overhead is the additional time and resource cost introduced by:

- wrapper entry and exit logic
- argument and result normalization
- identity generation
- persistence preparation and writes
- comparison execution when compare mode is enabled
- summary recording and shutdown flush work

## Benchmark Scenario Matrix

| Scenario | Goal | Baseline Setup | Traced Setup | Key Metrics | Notes |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Very fast pure function | Measure fixed wrapper cost sensitivity. | Small arithmetic/string function in a tight loop. | Decorator tracing with persistence off. | per-call duration, p50, p95, overhead ratio | Fixed overhead can dominate here; interpret carefully. |
| Medium-cost business logic | Measure realistic refactor-validation overhead. | Function doing moderate branching and object shaping. | Decorator tracing with persistence on. | total duration, overhead ratio, artifact size | Closest to expected daily use. |
| Nested traced calls | Measure compounding cost and context handling. | Call graph with parent and child functions. | All nodes traced. | per-call duration, total run cost, trace count | Important for recursion and stack behavior. |
| Compare mode | Measure baseline-plus-candidate execution cost. | Same input executed once without tracing. | Baseline plus candidate under compare flow. | total duration, comparison payload size | Must separate duplicated business execution cost from framework overhead. |
| Exception path | Validate robustness on failing user code. | Function raises a controlled exception. | Traced execution with failure-path recording. | exception propagation time, logging side effects | Tracing must not mask or materially distort failures. |
| Persistence off vs on | Isolate filesystem write impact. | Same traced function with persistence disabled. | Same function with persistence enabled. | overhead delta, bytes written, file count | Needed for tuning adapter boundaries. |
| Summary flush | Measure end-of-process report cost. | No tracing summary write. | Summary aggregation and flush. | shutdown latency, output size | Review separately from hot-path call overhead. |

## Metrics to Record

- wall-clock duration per scenario
- per-call duration where applicable
- median and tail latency (`p50`, `p95`)
- overhead ratio compared with baseline
- trace count
- bytes written and file count
- comparison payload size when compare mode is used
- error/log events triggered by infrastructure failures

## Measurement Risks

- Very fast functions exaggerate fixed wrapper cost and can make percentage-based thresholds noisy.
- Filesystem caching and antivirus activity can distort persistence timings.
- Debug logging can materially change overhead and should be measured separately.
- Warm-up effects and interpreter startup noise should be excluded from repeated-loop measurements.
- Compare mode combines framework cost with doubled business execution cost, so results need split interpretation.

## Validation TODOs

1. Add a benchmark harness after the tracing runtime and persistence domains are implemented.
2. Define the exact statistical aggregation method for acceptance reporting.
3. Decide whether summary flush time counts inside or outside the main `15%` gate.
4. Validate persistence-off fast-path behavior before optimizing compare mode.
