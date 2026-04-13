# Configuration and Contracts Core Layer

## Scope

Core configuration schema, default values, and protocol definitions.

## Owns

- trace root policy
- persistence enablement policy
- compare-mode configuration
- summary policy
- callable protocol definitions for compare, record, persistence, and future collectors

## Core Rules

- defaults should be safe for local development
- per-call overrides should be mergeable without ambiguity
- protocols should document required inputs and expected outputs clearly

## Open Questions

- Whether a single config object or a small set of immutable config sections best balances clarity and ergonomics.
