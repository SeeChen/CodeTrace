# Comparison and Reporting Core Layer

## Scope

Core schemas and invariants for compare results, trace records, and run summaries.

## Owns

- default compare result structure
- record field expectations
- summary top-level schema
- status fields for infrastructure-side failures

## Core Rules

- schemas should remain dictionary-like and serializable
- custom builders may extend payloads but should not remove required structural anchors
- summary entries must stay traceable to one trace identity

## Open Questions

- Which fields are mandatory enough to be frozen for public compatibility in MVP.
