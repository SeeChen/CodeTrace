# PRD-Pipeline

`PRD-Pipeline` is the repository's modular PRD-to-delivery orchestration system.

Its purpose is no longer only to generate layered specifications. Its active purpose is to turn one PRD into architecture, build contracts, task slices, implementation work, verification evidence, and acceptance outputs with explicit stage ownership.

## Active Flow

The active flow is:

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`

This flow is delivery-oriented. It keeps documentation where it improves implementation accuracy, but avoids generating extra document layers that do not materially improve coding or validation.

## What It Produces

The active target outputs are:

- `specs/intent/brief.md`
- `specs/architecture/SA.md`
- `specs/build/*`
- `specs/acceptance/criteria.md`
- `specs/acceptance/report.md`
- implementation and verification state tracked through workflow memory

## Core Idea

The system is built from six orchestration building blocks:

- `agents/`
  Role ownership and handoff boundaries.
- `skills/`
  Lightweight task maps for repeatable work.
- `commands/`
  User-facing or workflow-facing entry points.
- `docs/`
  Detailed reference material, contracts, and blueprint guidance.
- `memory/`
  Durable workflow state, frozen decisions, and unresolved questions.
- `rules/`
  Non-negotiable operating constraints.

## Active Command Surface

The active user-facing entry point is:

- `/seechen`

Recommended examples:

1. `/seechen --run`
2. `/seechen --init`
3. `/seechen --sa`
4. `/seechen --spec`
5. `/seechen --slice`
6. `/seechen --implement`
7. `/seechen --verify`
8. `/seechen --accept`

Natural-language requests routed through `/seechen` are also supported.

Internal stage command files may still exist as execution references, but the intended public command surface is the single `/seechen` command.

## Legacy Migration Status

The legacy `ref -> global -> domains -> testing -> acceptance` orchestration path has been removed from the active module assets.

The old generated spec set has also been cleared so the next workflow run can produce the active structure without mixing legacy outputs into the review surface.

## Design Rules

1. `docs/PRD.md` is the primary source of truth.
2. Downstream outputs must be generated from upstream artifacts.
3. Architecture must be frozen before build-spec generation.
4. Coding should follow task slices, not broad PRD reinterpretation.
5. Agents and skills should stay compact and load deeper references only when needed.

## Recommended Next Step

The next practical milestone for this pipeline is:

`PRD -> specs/intent/brief.md -> specs/architecture/SA.md -> specs/build/* -> specs/build/tasks.md`

Once that is stable, coding and verification can be automated much more reliably.
