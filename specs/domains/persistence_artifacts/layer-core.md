# Persistence Artifacts Core Layer

## Scope

This layer defines the payload and path rules for deterministic artifact persistence.

## Owns

- run identifier to directory mapping
- trace identifier to subdirectory mapping
- artifact naming conventions for inputs, outputs, comparison, and metadata
- serialization outcome metadata returned to the runtime

## Core Rules

- run-level directory groups one process execution
- trace-level directory groups one traced target execution
- artifact names remain predictable across reruns given the same policy
- serialization failures are represented explicitly in metadata

## Open Questions

- Whether artifact names should prefer semantic labels only or include ordered numeric prefixes for easier manual browsing.
