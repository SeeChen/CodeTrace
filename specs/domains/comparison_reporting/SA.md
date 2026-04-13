# Comparison and Reporting Domain Architecture

## Scope

This domain owns compare-mode result shaping, record assembly, and run-level summary aggregation.

## Responsibilities

- normalize baseline and candidate outputs for comparison
- apply default or custom compare callables
- build final trace records
- aggregate records into a structured run summary

## Internal Structure

- compare coordinator
- record builder adapter
- summary recorder
- output schema normalizer

## Dependencies

- runtime metadata and execution results
- configuration contracts for custom hooks and summary policy
- persistence metadata when artifact paths should be referenced in records

## Failure Paths

- custom compare callable fails
- custom record builder fails
- summary flush fails at exit

These failures should be captured as infrastructure outcomes without invalidating the main baseline result.

## Open Questions

- Whether compare outputs should always include a normalized status field even when users provide custom compare payloads.
