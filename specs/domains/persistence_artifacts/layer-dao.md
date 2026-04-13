# Persistence Artifacts DAO Layer

## Scope

This layer performs filesystem writes and read-ready artifact layout operations.

## Responsibilities

- create directories safely
- write structured text artifacts
- optionally support alternate persisted payload forms behind the same adapter contract
- return saved path metadata and write-failure details

## DAO Rules

- prefer human-reviewable formats by default
- never let a failed write silently look successful
- keep adapter methods narrow and explicit
- avoid leaking raw filesystem exceptions as the only observable signal

## Open Questions

- Whether a manifest file per trace should be written immediately in MVP or deferred until replay work becomes active.
