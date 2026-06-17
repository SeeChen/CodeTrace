# Open Questions

## Purpose

This file records unresolved design or implementation questions that should remain visible across workflow runs.

## Current Open Questions

All four Stage 1 architecture open questions were resolved in Stage 2 and frozen in `frozen-decisions.md` (#13–#16): session sharing = module-level singleton; `<trace_name>` collisions = `__<n>` suffix; summary inlines records; candidate exceptions = `candidate_error` compare result.

Remaining (non-blocking, deferred to their owning stages):

1. Trace root default — assumed `.codetrace/` and now configurable via `trace_root` config option; revisit only if a future requirement changes the default.
2. Future class-tracing "public method" scope (dunder/inherited handling) — deferred; class tracing is a reserved extension path, not MVP.

No open questions block Stage 3 (slice) or Stage 4 (implement).
