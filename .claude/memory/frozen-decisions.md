# Frozen Decisions

## Purpose

This file stores architectural and workflow decisions that downstream stages should not silently override.

## Current Decisions

1. The active workflow is `PRD -> intent -> architecture -> build -> tasks -> coding -> verify -> accept`.
2. Generated outputs use the `specs/intent`, `specs/architecture`, `specs/build`, and `specs/acceptance` structure.
3. Agents and skills should remain lightweight and rely on `docs/` for deeper reference material.
4. The orchestration module lives under `.claude/` (`agents`, `commands`, `skills`, `rules`, `memory`, `docs`) as the single source of truth.
5. The public command surface is unified under `/seechen`, with defined flags for known stages and intent routing for natural-language requests.

## Notes

- Product- and implementation-level decisions (for example artifact schema, identifiers, or serialization fallbacks) are derived during the pipeline run and recorded here as each stage freezes them.
