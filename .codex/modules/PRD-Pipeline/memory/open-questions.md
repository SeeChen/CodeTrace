# Open Questions

## Purpose

This file records unresolved design or implementation questions that should remain visible across workflow runs.

## Current Open Questions

1. Should comparison failures be represented only in artifacts, or should there also be an optional strict mode that raises?
2. What exact serialization fallback should be used for non-serializable inputs and outputs in the MVP?
3. Should run identity be timestamp-only, hash-assisted, or configurable from the beginning?
4. Should context-manager tracing be part of the first implementation milestone or reserved for the next milestone after function tracing stabilizes?
