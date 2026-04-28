# Frozen Decisions

## Purpose

This file stores architectural and workflow decisions that downstream stages should not silently override.

## Current Decisions

1. The active workflow is `PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`.
2. New workflow assets should prefer the smaller `specs/intent`, `specs/architecture`, `specs/build`, and `specs/acceptance` structure.
3. Agents and skills should remain lightweight and rely on `docs/` for deeper reference material.
4. Legacy pipeline assets inside `.codex/modules/PRD-Pipeline` and legacy generated outputs under `specs/` should be removed once replaced so active runs do not mix structures.
