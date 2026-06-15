---
description: Unified entry point for the PRD-to-delivery pipeline; routes flags and natural language to the right stage.
argument-hint: "[--run | --init | --sa | --spec | --slice | --implement | --verify | --accept | <request>]"
---

# Command: seechen

## Purpose

`/seechen` is the unified command entry point for the active delivery workflow.

It routes structured flags, defined stage actions, and natural-language requests through one command surface.

The active flow is:

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`

## Direct Invocation

Structured examples:

- `/seechen --run`
- `/seechen --init`
- `/seechen --sa`
- `/seechen --spec`
- `/seechen --slice`
- `/seechen --implement`
- `/seechen --verify`
- `/seechen --accept`
- `/seechen --from verify`
- `/seechen --only spec`
- `/seechen --refresh accept`

Natural-language examples:

- `/seechen generate the architecture from the current PRD`
- `/seechen create the build spec for me`
- `/seechen continue from where we stopped`
- `/seechen I want acceptance criteria for the current milestone`

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.claude/docs/PRD-Pipeline-Interface.md`
4. `.claude/docs/PRD-Pipeline-Refactor-Blueprint.md`
5. `.claude/rules/rules.md`
6. `.claude/memory/pipeline-state.md`
7. `.claude/memory/frozen-decisions.md`
8. `.claude/memory/open-questions.md`
9. `.claude/memory/implementation-log.md`

## Routing Model

### Mode 1: Defined Workflow Action

If the user provides a defined action or flag, run it directly.

Supported actions:

- `--run`
  Run the end-to-end active flow.
- `--init`
  Generate `specs/intent/brief.md`.
- `--sa`
  Generate `specs/architecture/SA.md`.
- `--spec`
  Generate `specs/build/*`.
- `--slice`
  Generate `specs/build/tasks.md`.
- `--implement`
  Execute the implementation stage.
- `--verify`
  Execute the verification stage.
- `--accept`
  Generate `specs/acceptance/criteria.md` and `specs/acceptance/report.md`.

### Mode 2: Directed Control Flags

These flags modify how `/seechen` executes:

- `--from <stage>`
- `--only <stage>`
- `--refresh <stage-or-scope>`

Supported stage names:

- `init`
- `sa`
- `spec`
- `slice`
- `implement`
- `verify`
- `accept`

### Mode 3: Natural-Language Intent

If the user input is natural language or uses an undefined instruction:

1. infer the most likely requested stage or workflow goal
2. use existing repository state to reduce ambiguity
3. run the matching stage if the inferred action is safe and clear
4. ask for clarification only when the intent is materially ambiguous or risky

Examples:

- "generate the architecture" -> route to `--sa`
- "continue from current state" -> route to `--run` with resume behavior
- "make acceptance criteria" -> route to `--accept`

## Execution Model

`/seechen` is the only user-facing command surface for the active workflow.

Stage-specific command files may still exist as internal execution references, but users should not need to call them directly.

## Resume Behavior

Before doing any work:

1. read `memory/pipeline-state.md`
2. detect the current stage and next stage
3. resume from the first incomplete stage when the request implies continuation
4. record blockers instead of silently stopping

After each stage transition:

1. update `memory/pipeline-state.md`
2. record the active stage number, stage name, status, progress, current situation, output evidence, and next action
3. mark completed stages as `completed` with `100%` progress
4. mark blocked stages as `blocked` and write the blocker plus recovery action
5. keep `Overall Progress`, `Current Stage`, `Last Completed Stage`, and `Next Stage` aligned

## Guardrails

- Do not invent a workflow stage that is not defined.
- Do not skip required upstream stages unless the existing outputs already justify it.
- Do not ignore natural-language requests only because they are not written as formal flags.
- Do not ask for clarification when repository state makes the user's likely intent clear enough to proceed safely.
