# Frozen Decisions

## Purpose

This file stores architectural and workflow decisions that downstream stages should not silently override.

## Current Decisions

1. The active workflow is `PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`.
2. New workflow assets should prefer the smaller `specs/intent`, `specs/architecture`, `specs/build`, and `specs/acceptance` structure.
3. Agents and skills should remain lightweight and rely on `docs/` for deeper reference material.
4. Legacy `ref / global / domains / testing` assets remain available during migration, but new orchestration design should not deepen dependency on them.
