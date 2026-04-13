# AI-Driven Development Workflow Specification (V1.0)

This document defines an AI-agent-driven delivery workflow from PRD to final acceptance. It clarifies stage goals, core outputs, agent responsibilities, and collaboration rules for Python projects such as CodeTrace.

## 1. Top-Level Workflow

Goal: establish an end-to-end path from requirements to acceptance so that every stage has a clear owner and a reviewable output.

**PRD** -> **Global Blueprint** -> **Domain Spec** -> **Coding** -> **Testing** -> **Acceptance**

---

## 2. Phase 0: Knowledge Base (`ref`)

Goal: create the shared knowledge foundation for the project, including terminology, standard-library boundaries, and performance-budget framing.

### Core Outputs

- `prd_keywords.md`: normalized project terminology such as instrumentation, trace artifacts, and comparison concepts.
- `std_lib_research.md`: standard-library boundary research for tracing, inspection, persistence, and reporting.
- `perf_baseline.md`: performance-budget framing and benchmark-planning guidance, including the `15%` review target.

### Agent Responsibilities

- `Research Agent`
  Role: analyze the PRD and extract key concepts, technical boundaries, and standard-library candidates.
  Skills: terminology definition, standard-library research, performance-budget framing.

---

## 3. Phase 1: Global Skeleton

Goal: remove architectural ambiguity, establish cross-domain contracts, and produce a system-level design that can guide domain expansion.

### Core Outputs

| Document | Focus |
| :--- | :--- |
| `app-business.md` | Product-level flow from trigger to capture to persistence and review. |
| `SA.md` | High-level system architecture and major topology decisions. |
| `project-structure.md` | Repository and package organization aligned with Google style and zero-dependency goals. |
| `modules.md` | Global module and domain boundaries, responsibilities, and dependencies. |
| `constraint.md` | Non-negotiable technical constraints such as failure isolation and Python `3.10+`. |
| `API.md` | Global public contracts such as tracing entry points and hook boundaries. |

### Agent Responsibilities

- `Architect Agent`
  Role: interpret the PRD, model the business flow, and define system boundaries and module structure.
  Skills: architecture design, dependency mapping, extensibility planning.
- `Security & Logic Agent`
  Role: define global constraints and identify risk boundaries.
  Skills: failure handling, policy constraints, cross-cutting robustness rules.
- `Liaison Agent`
  Role: coordinate cross-domain contracts and keep API expectations consistent.
  Skills: interface shaping, compatibility review, contract normalization.

---

## 4. Phase 2: Domain Expansion

Goal: decompose the global design into implementation-ready domains and produce domain-level design artifacts that can guide coding.

### Core Outputs

- `SA.md`: domain-level architecture and scope.
- `layer-core.md`: core data structures, lifecycle state, and invariants.
- `layer-dao.md`: persistence or storage-facing layer details where needed.
- `layer-biz.md`: business-level coordination, policies, and workflow decisions where needed.
- `layer-facade.md`: user-facing or cross-domain interface boundaries where needed.

### Agent Responsibilities

- `Domain Expert Agent`
  Role: refine business rules, edge conditions, state handling, and domain boundaries.
  Skills: detailed lifecycle design, exception paths, extension-point planning.
- `Framework Agent`
  Role: map the design into Python package and module structure.
  Skills: package shaping, dependency control, implementation-oriented structure planning.
- `QA Agent`
  Role: identify testable risks and validation implications while the domain is being designed.
  Skills: edge-case planning, failure-path coverage, performance-sensitive review.

---

## 5. Phase 2.5: Test Strategy

Goal: embed test-driven planning so that the specification set is directly mappable to implementation validation.

### Core Outputs

- `engine_perf.md`: performance-sensitive scenarios such as nested tracing and compare-mode cost.
- `coverage-plan.md` or equivalent: requirement-to-test intent mapping.
- `failure_paths.md` or equivalent: error propagation, serialization failure, and summary-failure validation.

### Agent Responsibilities

- `Test Designer Agent`
  Role: define validation intent, scenario coverage, and acceptance-relevant test plans.
  Skills: performance test design, boundary-case planning, concurrency and robustness analysis when relevant.

---

## 6. Phase 3: Coding and Verification

Goal: implement the code and validate it against the specification set, forming a closed loop between design and execution.

### Core Outputs

- implementation code aligned with the approved specifications
- test results from unit, integration, and regression-oriented execution
- fix and verification records for discovered defects

### Agent Responsibilities

- `Coding Agent`
  Role: implement the code according to the specification and API layers.
  Skills: Python implementation, constraint-aware coding, maintainable structure.
- `Refactor Agent`
  Role: review architecture alignment, maintainability, and quality risks.
  Skills: static review, dependency analysis, performance and readability review.
- `Test Runner Agent`
  Role: execute tests, report failures, and support the fix loop.
  Skills: Pytest execution, failure analysis, regression confirmation.

---

## 7. Phase 3.5: Acceptance Criteria

Goal: define the final delivery gates for the current milestone so review is concrete and consistent.

### Core Outputs

- `criteria.md`: milestone acceptance gates covering functionality, constraints, performance, and evidence requirements.

### Agent Responsibilities

- `Acceptance Agent`
  Role: define acceptance gates and verify that the delivered outputs satisfy the milestone.
  Skills: gate definition, performance review, compliance and quality assessment.

---

## 8. Collaboration Logic

1. `Global` ownership and `Domain` ownership are intentionally separated. The global layer freezes cross-domain contracts; domain layers elaborate them.
2. Contracts come before coding. Coding should not begin until the global API and constraints are stable enough to guide implementation.
3. If a domain cannot be implemented from the current global architecture, the global layer must be revised explicitly instead of being bypassed silently.
4. Documents are living artifacts. When the design changes, the affected global and domain documents must be updated together.

---

## 9. Continuous Improvement Guidance

- Keep the PRD as the primary truth source and update downstream documents when the PRD changes materially.
- Make every stage output reviewable and acceptance-oriented rather than purely descriptive.
- Periodically review the agent workflow itself and strengthen weak handoff points.

---

## 10. Example Output Structure

The following tree shows a representative output structure for a project like CodeTrace. It is a pattern, not a mandatory checklist.

```text
specs/
├── ref/                                # Phase 0 knowledge base
│   ├── prd_keywords.md                 # shared terminology
│   ├── std_lib_research.md             # standard-library boundary research
│   └── perf_baseline.md                # performance-budget framing
├── global/                             # Phase 1 global skeleton
│   ├── app-business.md                 # product-level flow
│   ├── SA.md                           # high-level architecture
│   ├── project-structure.md            # repository and package guidance
│   ├── modules.md                      # module and domain boundaries
│   ├── constraint.md                   # non-negotiable constraints
│   └── API.md                          # public contracts
├── domains/                            # Phase 2 domain expansion
│   ├── tracing_runtime/
│   │   ├── SA.md
│   │   ├── layer-core.md
│   │   ├── layer-biz.md
│   │   └── layer-facade.md
│   ├── persistence_artifacts/
│   │   ├── SA.md
│   │   ├── layer-core.md
│   │   └── layer-dao.md
│   └── comparison_reporting/
│       ├── SA.md
│       ├── layer-core.md
│       ├── layer-biz.md
│       └── layer-facade.md
├── testing/                            # Phase 2.5 test strategy
│   ├── coverage-plan.md
│   ├── engine_perf.md
│   └── failure_paths.md
├── acceptance/                         # Phase 3.5 acceptance criteria
│   └── criteria.md
└── summary.md                          # durable document index and status
```

### Structure Notes

- `ref/`: knowledge base outputs that reduce ambiguity before architecture design.
- `global/`: global design decisions that freeze contracts and boundaries.
- `domains/`: implementation-facing design documents for each planned domain.
- `testing/`: validation intent mapped from requirements and design risks.
- `acceptance/`: milestone completion gates and evidence requirements.
- `summary.md`: durable status tracking and document navigation.

This structure preserves layered traceability from requirements to design to testing and acceptance.

---

## Note

This workflow is intended for AI-assisted development and can be adapted to different project sizes and team setups. File names and exact document counts may change with project scope, but the stage intent and handoff clarity should remain stable.
