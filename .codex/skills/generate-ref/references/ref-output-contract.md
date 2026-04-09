# Ref Output Contract

Use this file as the stable shape for `specs/ref/` outputs.

## 1. `prd_keywords.md`

Recommended sections:

1. Title
2. Purpose
3. Source Documents
4. Core Terms
5. Ambiguous or Easily Confused Terms
6. Open Questions

Recommended table columns:

- Term
- Definition
- Why It Matters
- Source

## 2. `std_lib_research.md`

Recommended sections:

1. Title
2. Purpose
3. Source Documents
4. Research Scope
5. Standard Library Candidates
6. Risks and Boundary Notes
7. Recommended Validation Tasks
8. Open Questions

Recommended table columns:

- Capability Area
- Candidate Module or Mechanism
- Expected Role
- Benefits
- Risks or Limits
- Source

## 3. `perf_baseline.md`

Recommended sections:

1. Title
2. Purpose
3. Source Documents
4. Budget Framing
5. Baseline Definition
6. Overhead Definition
7. Benchmark Scenario Matrix
8. Metrics to Record
9. Measurement Risks
10. Validation TODOs

Recommended table columns for scenario matrix:

- Scenario
- Goal
- Baseline Setup
- Traced Setup
- Key Metrics
- Notes

## General Rules

- Each file should start with a one-paragraph purpose statement.
- Each file should end with `Open Questions` or `Validation TODOs` if uncertainty remains.
- Prefer explicit `Source` references like `PRD 3 / FR-01` or `Workflow Phase 0`.
- Do not copy large PRD passages verbatim. Summarize and normalize.

