# PRD-Pipeline Interface

This document defines how the active `PRD-Pipeline` workflow should be called directly or composed into other workflows.

## Primary Entry Point

- `/seechen`

## Public Invocation Model

Structured invocation examples:

- `/seechen --run`
- `/seechen --init`
- `/seechen --sa`
- `/seechen --spec`
- `/seechen --slice`
- `/seechen --implement`
- `/seechen --verify`
- `/seechen --accept`
- `/seechen --converge`
- `/seechen --from verify`
- `/seechen --only spec`

Natural-language invocation is also valid when the request does not match a predefined flag exactly.

## Purpose

Generate or refresh the delivery-oriented artifact set from the PRD through acceptance while remaining resumable and repository-backed.

## Required Inputs

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.claude/memory/pipeline-state.md`
4. `.claude/memory/frozen-decisions.md`
5. `.claude/memory/open-questions.md`
6. `.claude/memory/implementation-log.md`

## Active Outputs

1. `specs/intent/brief.md`
2. `specs/architecture/SA.md`
3. `specs/build/*`
4. `specs/acceptance/criteria.md`
5. `specs/acceptance/report.md`
6. updated memory state

## Stage Contract

The active stage order is:

1. `pipeline-init`
2. `generate-sa`
3. `generate-spec`
4. `slice-work`
5. `implement`
6. `verify`
7. `accept`

Another workflow may compose this pipeline only if it preserves that ordering or records an explicit reason for deviation.

### Optional Post-Acceptance Extension

After `accept`, the optional **convergence loop** (`/converge`) hardens the
milestone against machine-checkable gates until it converges. It is not part of
the linear stage order; it runs only on an already-accepted, green milestone.
Outputs go to `specs/audit/*`; state is tracked in
`.claude/memory/convergence-state.md`; the contract is defined in
`.claude/docs/Convergence-Loop.md`.

## Intent Routing Contract

When the user calls `/seechen`:

1. if the request matches a defined action, execute that action directly
2. if the request uses control flags, apply them to the matching stage flow
3. if the request is natural language or undefined shorthand, infer intent from the request and repository state
4. ask for clarification only when the inferred action is too ambiguous or risky

## Resume Contract

The workflow must:

1. read `memory/pipeline-state.md` before starting work
2. update the current stage after each completed stage
3. record blockers instead of silently stopping
4. store frozen contract decisions in `memory/frozen-decisions.md`
5. store unresolved issues in `memory/open-questions.md`
6. store implementation deviations and fix-loop notes in `memory/implementation-log.md`

## State Update Contract

After every stage transition, the workflow must update `memory/pipeline-state.md` with a concrete status snapshot.

Each update must record:

1. stage number
2. stage name
3. stage status: `pending`, `in_progress`, `completed`, or `blocked`
4. stage progress as a concrete percentage
5. current situation in one short factual sentence
6. output or evidence produced by the stage
7. next action
8. blockers, if any

When a stage completes:

1. mark that stage as `completed` with `100%` progress
2. move `Last Completed Stage` to the completed stage
3. move `Current Stage` and `Next Stage` to the next incomplete stage
4. update `Overall Progress`
5. update `Current Stage Detail`

When a stage is blocked:

1. mark that stage as `blocked`
2. keep `Current Stage` on the blocked stage
3. record the blocker under `Blockers`
4. write the next recovery action clearly

## Blocking Conditions

The workflow may ask for clarification only when:

1. `docs/PRD.md` is missing
2. the PRD is contradictory in a way that blocks the next stage
3. the repository target is materially ambiguous
4. the user explicitly requests alternate scope

## Non-Blocking Principle

If one area is blocked but the rest of the current stage can proceed safely, finish the non-blocked work first and record the blocker in workflow memory.

## Legacy Compatibility

The pipeline module should not recreate or extend the removed legacy command path.

If old spec outputs need to be preserved for archival reasons in the future, they should be stored outside the active generation path.
