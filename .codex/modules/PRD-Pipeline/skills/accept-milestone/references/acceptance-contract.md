# Acceptance Contract

This reference defines the minimum contract for the active acceptance stage.

## Purpose

The acceptance stage must produce:

1. a milestone acceptance standards document
2. an evidence-based acceptance outcome document

The standards document defines what must be true.

The outcome document states whether those standards were met.

## Required Outputs

### `specs/acceptance/criteria.md`

This file should define:

- milestone scope
- blocking acceptance gates
- required evidence
- non-blocking deferred items
- known exclusions

### `specs/acceptance/report.md`

This file should define:

- evidence reviewed
- pass or conditional status per major gate
- blocked items
- deferred items
- final milestone status

## Rules

1. Acceptance criteria must be derived from the PRD, intent pack, build spec, and test matrix.
2. Acceptance may not invent new product requirements.
3. Future-scope items may be mentioned, but they must not become current blocking gates unless they are already in scope.
4. The report must evaluate the delivered state against the criteria instead of replacing the criteria.
