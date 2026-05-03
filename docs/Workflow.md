# AI-Driven Development Workflow Specification

This document defines the active PRD-to-delivery workflow for this repository.

The workflow is designed for AI-assisted implementation, but it is intentionally structured so that humans can review each stage without reconstructing the entire reasoning chain.

## 1. Primary Goal

The repository should be able to start from one product requirements document and move through architecture, implementation planning, coding, testing, and acceptance with explicit handoffs and low design drift.

The active target flow is:

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`

## 2. Design Principles

1. `docs/PRD.md` is the only product-level source of truth.
2. Every downstream artifact must declare or clearly imply its upstream inputs.
3. Architecture must be frozen before coding-ready specifications are generated.
4. Coding should follow task slices, not broad reinterpretation of the PRD.
5. Verification and acceptance are first-class stages, not optional cleanup.
6. Reusable orchestration assets should remain lightweight and load deeper references only when needed.

## 3. Active Stages

### Stage 0: Normalize PRD

Purpose:
Create a compact intent artifact that removes ambiguity before architecture work begins.

Main output:
- `specs/intent/brief.md`

The intent pack should capture:
- mission
- MVP scope
- non-goals
- constraints
- core entities and actions
- acceptance framing
- open questions

### Stage 1: Generate SA

Purpose:
Freeze the system architecture and major module boundaries.

Main output:
- `specs/architecture/SA.md`

The system architecture should define:
- module boundaries
- public API shape
- extension points
- runtime lifecycle
- cross-cutting constraints
- frozen decisions

### Stage 2: Generate Build Spec

Purpose:
Convert architecture into implementation-ready planning assets.

Main outputs:
- `specs/build/module-map.md`
- `specs/build/interfaces.md`
- `specs/build/file-plan.md`
- `specs/build/artifact-schema.md`
- `specs/build/failure-policy.md`
- `specs/build/test-matrix.md`

The build-spec layer should answer:
- what to build
- where to build it
- how modules interact
- how artifacts are shaped
- how failures are isolated
- how requirements will be tested

### Stage 3: Slice Work

Purpose:
Break the build spec into small coding tasks that can be implemented safely and reviewed clearly.

Main output:
- `specs/build/tasks.md`

Task slices should define:
- sequence
- file ownership
- prerequisites
- expected outputs
- required tests
- acceptance notes

### Stage 4: Coding

Purpose:
Implement the code and tests from task slices.

Main outputs:
- `src/`
- `tests/`

Coding should not silently redefine:
- architecture boundaries
- public interfaces
- failure policies
- artifact contracts

If a conflict is discovered, it should be written back into workflow memory before continuing.

### Stage 5: Verify

Purpose:
Validate that the implementation matches the build spec and task expectations.

Main outputs:
- test execution evidence
- defect records
- fix-loop notes when needed

Verification should include:
- unit tests
- integration checks where relevant
- failure-path checks
- contract conformance review

### Stage 6: Accept

Purpose:
Define milestone acceptance standards and decide whether the current milestone is complete based on explicit evidence.

Main outputs:
- `specs/acceptance/criteria.md`
- `specs/acceptance/report.md`

Acceptance should state:
- milestone criteria and required evidence
- delivered scope
- evidence used
- deferred or blocked items
- final milestone status

## 4. Artifact Layout

The active target structure is:

```text
specs/
├── intent/
│   └── brief.md
├── architecture/
│   └── SA.md
├── build/
│   ├── module-map.md
│   ├── interfaces.md
│   ├── file-plan.md
│   ├── artifact-schema.md
│   ├── failure-policy.md
│   ├── test-matrix.md
│   └── tasks.md
└── acceptance/
    ├── criteria.md
    └── report.md
```

Older `ref / global / domains / testing` outputs may still exist during migration, but the repository should gradually move toward the smaller active structure.

## 5. Responsibility Model

### Docs

Store durable project truth and detailed references.

### Memory

Store stage progress, frozen decisions, open questions, and implementation deviations.

After every stage transition, update `.codex/modules/PRD-Pipeline/memory/pipeline-state.md` with:

- stage number
- stage name
- stage status
- concrete progress percentage
- current situation
- output or evidence
- next action
- blockers, if any

### Rules

Store non-negotiable workflow and generation constraints.

### Agents

Store role-based ownership and handoff behavior.

### Skills

Store lightweight execution guides for recurring task types.

### Commands

Store the user-facing workflow entry points.

## 6. Recommended Command Path

The public command surface is unified under:

- `/seechen`

Recommended examples:

1. `/seechen --run`
2. `/seechen --init`
3. `/seechen --sa`
4. `/seechen --spec`
5. `/seechen --slice`
6. `/seechen --implement`
7. `/seechen --verify`
8. `/seechen --accept`

Natural-language requests routed through `/seechen` are also valid when the intent is clear enough to infer safely.

## 7. Collaboration Rules

1. Do not skip architecture and go directly from the PRD to code.
2. Do not let coding agents redefine frozen contracts silently.
3. Keep agents and skills compact; deeper material belongs in `docs/`.
4. Preserve open questions rather than hiding uncertainty.
5. Keep stage outputs reviewable and implementation-facing.

## 8. Migration Note

This workflow replaces the older emphasis on:

`PRD -> ref -> global -> domains -> testing -> acceptance`

The older outputs are still useful during migration, but the active model now optimizes for:

`PRD -> intent -> architecture -> build -> implementation -> verification -> acceptance`
