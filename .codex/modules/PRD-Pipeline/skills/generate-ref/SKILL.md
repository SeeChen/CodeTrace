---
name: generate-ref
description: Generate Phase 0 ref documents for specs/ref from a project PRD and workflow. Use this when the task is to create or refresh prd_keywords.md, std_lib_research.md, and perf_baseline.md as the knowledge base before global architecture or coding begins.
---

# Generate Ref

This skill creates or updates the `specs/ref/` knowledge base for Phase 0 in the workflow.

Use this skill when the user wants to:

- generate the first version of `ref/` documents from a PRD
- refresh `specs/ref/` after PRD changes
- prepare memory documents before writing `global/` or `domains/` specs

Do not use this skill for:

- writing `global/`, `domains/`, `testing/`, or `acceptance/` documents
- implementing product code
- inventing requirements that are not grounded in the PRD

## Required Inputs

Read these files first:

1. `docs/Workflow.md`
2. `docs/PRD.md`

If the repository uses a different PRD path, use the user-provided path instead. Treat `Workflow.md` as the process contract and `PRD.md` as the product truth source.

## Output Contract

Write or update these files under `specs/ref/`:

1. `prd_keywords.md`
2. `std_lib_research.md`
3. `perf_baseline.md`

Also read [references/ref-output-contract.md](references/ref-output-contract.md) before drafting so the section structure stays stable.

## Workflow

### Step 1: Extract grounded facts

From the PRD, extract only:

- product goals
- user scenarios
- functional requirements
- technical constraints
- extensibility expectations
- performance constraints

Keep a strict line between:

- explicit PRD facts
- reasonable engineering inference
- open questions or undecided areas

Label inferences clearly. Do not present them as settled facts.

### Step 2: Generate `prd_keywords.md`

This file is the shared vocabulary for later phases.

It must include:

- a short purpose statement
- a glossary table of core terms from the PRD
- each term's project-specific meaning
- why the term matters to implementation or design
- ambiguous terms that need normalization later

Prioritize terms like:

- tracing
- artifact
- trace session
- baseline
- candidate
- comparison
- persistence
- summary
- adapter
- collector
- contract
- deterministic traceability
- local-first
- zero external dependency

Do not turn this into an architecture document. Keep it focused on language, semantics, and shared definitions.

### Step 3: Generate `std_lib_research.md`

This file translates PRD constraints into standard-library research directions for implementation.

It must include:

- the research goal
- a table of required capability areas
- likely standard-library modules or mechanisms
- what each candidate is good at
- known limitations, edge cases, or compatibility concerns
- a decision note for what should be validated during implementation

For this project, cover at least:

- instrumentation and call interception
- timing
- filesystem and path handling
- serialization
- hashing and identity
- logging
- context management
- exception handling
- thread or concurrency considerations when relevant

The goal is not to prove the final implementation. The goal is to narrow the search space for later architecture and coding work.

When a library choice is not fully proven by the PRD alone, phrase it as a candidate recommendation, not a final decision.

### Step 4: Generate `perf_baseline.md`

This file defines the initial performance budget frame, not benchmark results.

It must include:

- the source of the 15% budget from the workflow and PRD
- what should count as baseline behavior
- what should count as tracing overhead
- a first-pass measurement scope
- proposed benchmark scenarios grounded in the PRD
- metrics to record
- risks that can distort measurement

Include concrete benchmark scenario ideas such as:

- very fast pure functions
- medium-cost business logic functions
- nested traced calls
- compare mode with baseline and candidate
- persistence on versus persistence off
- exceptional execution paths

If the repository has no measurement code yet, write this as a planning document with explicit TODO validation points.

## Writing Rules

- Prefer concise, reviewable markdown over long essays.
- Use tables where they improve scanability.
- Keep each document self-contained.
- Cite the source section in the PRD or workflow when a claim matters.
- Never fabricate benchmark numbers, API signatures, or confirmed implementation details.
- If information is missing, create an `Open Questions` section instead of guessing.

## Handoff Rules

The generated `ref/` documents should help later phases by:

- giving `global/` documents a stable vocabulary
- reducing uncertainty around standard-library boundaries
- making the performance budget testable later

Before finishing, verify:

1. `prd_keywords.md` does not drift into architecture design
2. `std_lib_research.md` stays focused on standard-library boundaries and candidate choices
3. `perf_baseline.md` defines measurement strategy and budget framing, not fake results
4. all three files are traceable back to `docs/PRD.md` and `docs/Workflow.md`


