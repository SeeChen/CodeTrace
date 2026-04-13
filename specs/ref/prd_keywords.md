# CodeTrace PRD Keywords

## Purpose

This document normalizes the core vocabulary used in the CodeTrace PRD so later architecture, domain, and testing documents use the same language for tracing, persistence, comparison, and extension design.

## Source Documents

- `docs/PRD.md`
- `docs/Workflow.md`

## Core Terms

| Term | Definition | Why It Matters | Source |
| :-- | :-- | :-- | :-- |
| Trace | One observed execution of a function, method, class-instrumented method, or traced block. | The entire artifact model, summary schema, and performance budget are organized around per-trace execution. | PRD 2, PRD 3 / FR-01, FR-08, FR-09 |
| Trace Session | The broader execution lifecycle that can host one or more candidates, collectors, and emitters. | The PRD explicitly wants future evolution beyond one hard-coded wrapper. | PRD 5, PRD 6 |
| Artifact | A persisted runtime output such as serialized inputs, outputs, comparison data, or metrics. | Deterministic artifact organization is required for replay readiness and local review. | PRD 1, PRD 3 / FR-02, FR-12 |
| Record | The normalized dictionary payload describing a trace result. | Custom record builders are a first-class extension point. | PRD 3 / FR-06, PRD 6 |
| Summary | The run-level structured report that aggregates trace records. | The product must emit a structured end-of-process summary. | PRD 3 / FR-03, PRD 6 |
| Baseline | The reference implementation used as the comparison source in compare mode. | Baseline semantics drive A/B readiness and acceptance behavior. | PRD 2, PRD 3 / FR-04 |
| Candidate | The replacement or alternate implementation executed against the same inputs as the baseline. | Candidate handling must not hard-code the product into a one-off comparison dead end. | PRD 2, PRD 3 / FR-04, FR-11 |
| Compare Mode | A tracing mode that executes comparable implementations under one input set and emits comparison output. | This is the bridge from MVP validation into future A/B workflows. | PRD 2, PRD 3 / FR-04, FR-11 |
| Persistence | Local filesystem writing of artifacts through a stable storage contract. | The PRD requires local-first, isolated run directories, and future replay-friendly organization. | PRD 3 / FR-02, FR-10, FR-12 |
| Storage Adapter | The component boundary that owns writing artifacts and hides file-format details from orchestration. | This keeps the engine extensible and zero-dependency-friendly. | PRD 3 / FR-10, PRD 4, PRD 5 |
| Compare Callable | A user-supplied callable that transforms comparable outputs into a comparison result payload. | It is the main comparison extension seam. | PRD 3 / FR-05, PRD 6 |
| Record Builder | A user-supplied callable that builds the final trace record from runtime context. | It is the main record assembly extension seam. | PRD 3 / FR-06, PRD 6 |
| Metrics Collector | A future lifecycle-aware extension that records runtime measurements such as memory. | The MVP must preserve a safe path for later opt-in metrics. | PRD 3 / FR-13, PRD 5, PRD 6 |
| Local-First | Product behavior centered on local execution and local artifact storage rather than remote services. | This excludes hosted-platform assumptions from architecture and acceptance. | PRD 1, PRD 4 |
| Zero External Dependency | MVP runtime should rely on Python standard library facilities only. | This strongly shapes module choices and package structure. | PRD 1, PRD 4 |
| Deterministic Traceability | Artifacts, trace identity, and summary outputs should be predictable and reviewable across runs. | This underpins replay readiness, debugging value, and acceptance review. | PRD 1, PRD 4, PRD 6 |
| Trigger | The user-facing mechanism that starts tracing, such as decorator, class decorator, or context manager. | API and runtime domains need a shared term for all entry styles. | PRD 5, PRD 6 |

## Ambiguous or Easily Confused Terms

| Term | Current Normalization Need | Source |
| :-- | :-- | :-- |
| Trace vs Trace Session | Use `trace` for one observed execution and `trace session` for the broader execution container. | PRD 5 |
| Record vs Summary Detail | Use `record` for the payload attached to a trace and `summary detail` for the run-level wrapper entry. | PRD 3 / FR-03, PRD 6 |
| Comparison vs A/B Framework | The MVP comparison flow is one current capability; full A/B is future scope and should not be assumed in acceptance gates. | PRD 2, Appendix |
| Persistence vs Serialization | Serialization is representation shaping; persistence is the act of writing artifacts through storage boundaries. | PRD 3 / FR-02, FR-10 |
| Class Tracing vs Method Tracing | Class tracing means applying the same tracing contract across eligible methods, not inventing a separate runtime model. | PRD 3 / FR-09 |

## Open Questions

- Should the project reserve the term `run` exclusively for one process execution, or can it include smaller manual session scopes in the future?
- Should `record builder` and `summary recorder` remain separate named concepts in the public docs, or should summary recording be described as a reporting adapter?
