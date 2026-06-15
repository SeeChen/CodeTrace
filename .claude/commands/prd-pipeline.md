---
description: Deprecated alias for /seechen.
---

# Command: prd-pipeline

Deprecated public alias. Prefer `/seechen`.

## Purpose

`/prd-pipeline` remains only as a compatibility alias for the unified entry point. All routing, stage flow, resume behavior, and guardrails are defined in `/seechen`.

The active flow is:

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`

## Behavior

1. Treat any `/prd-pipeline` invocation as a `/seechen` invocation with the same arguments.
2. Read and follow `.claude/commands/seechen.md`.
3. Do not maintain a separate stage flow or routing model here.

## Migration Note

New work should call `/seechen`. This alias may be removed once external references are updated.
