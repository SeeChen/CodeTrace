# Tracing Runtime Domain Architecture

## Scope

This domain owns the execution lifecycle for traced functions, methods, class-decorated methods, and traced blocks.

## Responsibilities

- enter and exit trace sessions
- capture timestamps and execution metadata
- preserve user return values and exception flow
- invoke compare, persistence, and reporting boundaries without transferring ownership

## Internal Structure

- Trigger adapters: function, class, and block entry surfaces
- Session coordinator: builds lifecycle state for one trace execution
- Execution wrapper: runs baseline and optional candidate flows safely
- Failure isolator: routes infrastructure errors to logging/reporting without masking user errors

## Dependencies

- configuration defaults and per-call override resolution
- persistence adapter interface
- comparison and record-building interfaces

## Failure Paths

- user code raises: original exception propagates after runtime captures available metadata
- persistence fails: runtime records infrastructure failure and continues user semantics
- compare hook fails: runtime marks comparison failure in metadata and continues baseline result semantics

## Open Questions

- Should nested traced calls share one run recorder automatically or allow opt-out boundaries?
