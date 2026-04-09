# Rule 5: Phase 0 Ref Document Generation

This rule defines how AI agents should create or update Phase 0 knowledge-base documents under `specs/ref/`.

## Purpose

Phase 0 exists to establish shared terminology, standard-library research boundaries, and initial performance-budget framing before architecture design or coding begins.

These documents must stay grounded in:

- `docs/Workflow.md`
- `docs/PRD.md`

## Required Outputs

When a task requests initial specification generation for the knowledge base, AI agents should create or refresh:

1. `specs/ref/prd_keywords.md`
2. `specs/ref/std_lib_research.md`
3. `specs/ref/perf_baseline.md`

## Generation Rules

1. **PRD-grounded only**
   - Extract facts, constraints, and terminology from the PRD
   - Do not invent requirements, APIs, or implementation details

2. **Separate fact from inference**
   - Explicit product requirements should be presented as facts
   - Engineering interpretation should be labeled clearly
   - Missing information should be captured as open questions

3. **Keep document boundaries clear**
   - `prd_keywords.md` defines vocabulary and semantic normalization
   - `std_lib_research.md` captures standard-library candidates, limits, and validation targets
   - `perf_baseline.md` defines budget framing and benchmark strategy, not fabricated results

4. **Support downstream phases**
   - Outputs should reduce ambiguity for `global/` and `domains/`
   - Outputs should not preempt architecture decisions that belong to later phases

## Document Expectations

### `prd_keywords.md`

- Summarize core terms from the PRD
- Define each term in project context
- Explain why each term matters
- Record ambiguous or overloaded terms that need later normalization

### `std_lib_research.md`

- Focus on standard-library candidate modules and mechanisms
- Cover tracing, timing, filesystem, serialization, hashing, logging, context management, and error-handling concerns where relevant
- Record risks, limits, and validation points
- Present candidates as recommendations unless a decision is explicitly fixed elsewhere

### `perf_baseline.md`

- Reference the Phase 0 performance budget expectation
- Define baseline behavior versus tracing overhead
- Propose benchmark scenarios relevant to the PRD
- Record metrics to collect and factors that may distort measurement

## Review Checklist

Before merging AI-generated changes involving `specs/ref/`, verify:

1. All statements are traceable to `docs/PRD.md` or `docs/Workflow.md`
2. No benchmark values or technical decisions were fabricated
3. The three documents remain scoped to Phase 0 and do not drift into architecture or implementation
4. The outputs improve readiness for later `global/`, `domains/`, and testing documents
