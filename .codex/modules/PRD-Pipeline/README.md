# PRD-Pipeline

`PRD-Pipeline` is a self-contained document-generation workflow that turns a project PRD into a full specification set through staged AI execution.

## Purpose

This pipeline exists to let a user trigger one command and drive the repository from:

- project-boundary planning
- Phase 0 reference generation
- global specification generation
- domain planning
- domain-by-domain expansion
- testing-document generation
- acceptance-document generation

The intended entry point is:

- `/prd-pipeline`

Unless a real clarification blocker exists, the workflow should continue automatically to the end and leave behind resumable artifacts.

## What It Produces

The pipeline is designed to generate or refresh:

- planning outputs
- `specs/ref/*`
- `specs/global/*`
- `specs/domains/*`
- `specs/testing/*`
- `specs/acceptance/*`
- checkpoint and status-tracking artifacts

## Directory Layout

```text
.codex/modules/PRD-Pipeline/
├── README.md
├── agents/
├── commands/
├── docs/
├── memory/
├── rules/
└── skills/
```

## How It Works

The pipeline is organized by responsibility:

- `agents/`
  Role prompts. They define who owns each stage of work.
- `commands/`
  Task entry points. They define what to run and in what order.
- `docs/`
  Internal orchestration and interface documents. They explain how the pipeline is structured and how other workflows may call it.
- `memory/`
  Durable shared context. This includes workflow memory and the checkpoint file used for resume behavior.
- `rules/`
  Constraints and operating rules. These define branch policy, document scope, checkpoint behavior, language rules, and progress-sync requirements.
- `skills/`
  Task-specific execution guides. These define how to generate planning, global, domain, testing, and acceptance outputs.

## Execution Flow

```mermaid
flowchart TD
    A[User or External Workflow] --> B[/prd-pipeline]
    B --> C[Read PRD and Workflow]
    C --> D[Read Pipeline Rules]
    D --> E[Read Checkpoint]
    E --> F{Resume or Start}
    F --> G[Stage 1 Plan Documents]
    G --> H[Stage 2 Generate ref]
    H --> I[Stage 3 Generate global]
    I --> J[Stage 4 Plan domains]
    J --> K[Stage 5 Generate domain specs]
    K --> L[Stage 6 Generate testing docs]
    L --> M[Stage 7 Generate acceptance docs]
    M --> N[Stage 8 Finalize and Sync]
    G --> CP1[Update checkpoint]
    H --> CP2[Update checkpoint]
    I --> CP3[Update checkpoint]
    J --> CP4[Update checkpoint]
    K --> CP5[Update checkpoint after each domain]
    L --> CP6[Update checkpoint]
    M --> CP7[Update checkpoint]
    N --> O[Complete specs and status artifacts]
```

## From External Input to Final Artifacts

```mermaid
flowchart LR
    PRD[docs/PRD.md] --> CMD[/prd-pipeline]
    WF[docs/Workflow.md] --> CMD
    CMD --> PIPE[.codex/modules/PRD-Pipeline]
    PIPE --> AG[agents]
    PIPE --> CM[commands]
    PIPE --> DC[docs]
    PIPE --> ME[memory]
    PIPE --> RL[rules]
    PIPE --> SK[skills]
    AG --> OUT[specs/ref global domains testing acceptance]
    CM --> OUT
    DC --> OUT
    ME --> OUT
    RL --> OUT
    SK --> OUT
```

## Agents

These agents own the major stages of the workflow:

- `orchestrator-agent.md`
  Determines project boundary, document scope, and first-pass structure.
- `research-agent.md`
  Generates Phase 0 reference documents.
- `architect-agent.md`
  Generates the global specification layer.
- `domain-planner-agent.md`
  Turns the global layer into a domain map and domain expansion order.
- `domain-spec-agent.md`
  Generates one domain's detailed spec set at a time.
- `test-design-agent.md`
  Converts specs into testing-document coverage and validation plans.
- `acceptance-agent.md`
  Converts the current spec set into milestone acceptance criteria.

## Skills

These skills define how work is performed:

- `generate-ref`
  Generate `specs/ref/*`.
- `plan-doc-structure`
  Decide the document tree and phase structure from the PRD.
- `generate-global`
  Generate `specs/global/*`.
- `plan-domains`
  Plan domain boundaries and domain order.
- `generate-domain-spec`
  Generate one domain's document set.
- `generate-test-design`
  Generate `specs/testing/*`.
- `generate-acceptance`
  Generate `specs/acceptance/*`.

## Commands

These commands are the runnable entry points:

- `prd-pipeline.md`
  Full end-to-end command. This is the main command for direct use.
- `plan-docs.md`
  Run only planning.
- `generate-ref.md`
  Run only Phase 0 reference generation.
- `generate-global.md`
  Run only global-spec generation.
- `plan-domains.md`
  Run only domain planning.
- `generate-domain.md`
  Run one domain-spec pass.
- `generate-tests.md`
  Run testing-document generation.
- `generate-acceptance.md`
  Run acceptance-document generation.

## Rules

These rules keep execution predictable:

- `doc-scope.md`
  Prevents blind copying of example document trees.
- `summary-sync.md`
  Requires durable progress tracking after each meaningful step.
- `pipeline-checkpoint.md`
  Requires checkpoint-based resume behavior for `/prd-pipeline`.
- `agent-doc-size.md`
  Keeps agent prompts lightweight.
- `system-constraint-language.md`
  Keeps reusable system files in English.
- `branch-selection.md`, `branch.md`, `commit.md`
  Control branch and commit behavior.

## Memory

These files preserve durable pipeline state:

- `workflow-memory.md`
  Stable pipeline assumptions and reusable workflow facts.
- `prd-pipeline-checkpoint.md`
  Stage-by-stage resume state for `/prd-pipeline`.

## Relationship Model

The internal dependency order is:

1. `rules` constrain execution
2. `memory` provides durable context and checkpoint state
3. `commands` define the invoked task
4. `agents` define stage ownership
5. `skills` define task execution details
6. outputs are written to `specs/`
7. checkpoint and status are updated for resume

This means the pipeline does not depend on hidden conversational memory. It depends on repository artifacts.

## Checkpoint and Resume

`/prd-pipeline` must read:

- `memory/prd-pipeline-checkpoint.md`

before work begins.

It must update that file:

- after every completed stage
- after every completed domain during domain expansion
- whenever a blocker is discovered before stopping

This lets the pipeline resume from the first incomplete stage instead of restarting.

## Composition by Other Workflows

Other workflows may call this pipeline if they:

1. use `/prd-pipeline` as the authoritative entry point
2. preserve the checkpoint contract
3. treat the pipeline outputs as authoritative for downstream work
4. respect the interface defined in `docs/PRD-Pipeline-Interface.md`

This makes `PRD-Pipeline` usable both directly and as a nested workflow.

## Recommended Usage

For end-to-end document generation:

1. ensure `docs/PRD.md` exists
2. ensure `docs/Workflow.md` exists
3. run `/prd-pipeline`
4. inspect the generated `specs/` outputs
5. inspect `memory/prd-pipeline-checkpoint.md` if the workflow was interrupted

For partial execution, call the narrower commands instead.
