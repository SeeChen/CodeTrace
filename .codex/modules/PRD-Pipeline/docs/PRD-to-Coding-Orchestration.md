# PRD-to-Coding Document Orchestration Workflow

This document defines a document-orchestration workflow for AI-first coding environments. The goal is to start from a `PRD` and, through a stable set of `Agent / Skill / Rule / Command / Memory` assets, generate executable specifications step by step until the repository is ready for coding.

## 1. Design Goals

This workflow addresses three problems:

1. AI should not jump directly from `PRD` to coding, because that often causes missing constraints or mid-stream design drift.
2. Without explicit input/output boundaries, different agents tend to duplicate work, overwrite each other, or generate conflicting documents.
3. Documents must be readable by both AI and humans, so the structure has to remain stable, reviewable, and responsibility-driven.

## 2. Recommended Path from PRD to Coding

The recommended progression is:

`PRD -> Memory -> Global -> Domain -> Test Design -> Coding`

The corresponding directories are:

1. `specs/ref/`
2. `specs/global/`
3. `specs/domains/`
4. `specs/testing/`
5. `src/` and `tests/`

## 3. Responsibilities of the Five Building Blocks

### Agent

An Agent is a role. It defines the perspective from which work is performed.

Examples:

- `Research Agent` owns Phase 0 `ref/`
- `Architect Agent` owns `global/`
- `Domain Expert Agent` owns `domains/`
- `Test Designer Agent` owns `testing/`
- `Coding Agent` owns code implementation

### Skill

A Skill is a capability package. It defines how one class of task is completed reliably.

Examples:

- `generate-ref` creates `specs/ref/` from the PRD
- `generate-global` creates the global specification layer
- `generate-domain-spec` expands one implementation domain
- `generate-test-plan` or equivalent creates the testing layer

### Rule

A Rule is a constraint. It defines what is allowed and what is not allowed.

Examples:

- generate only from the `PRD` and upstream specs
- distinguish facts, inferences, and open questions
- do not enter coding before the API is stable
- do not fabricate benchmark results

### Command

A Command is the entry point. It defines which workflow should run when a user triggers a task.

It may be a script, or it may be a markdown prompt template.

Examples:

- `generate-ref`
- `generate-global`
- `generate-domain tracing_engine`
- `generate-tests persistence`

### Memory

Memory is long-lived project context. It defines which shared project agreements survive across runs.

Examples:

- project glossary
- confirmed architectural constraints
- document generation order
- frozen API decisions
- current stage status

## 4. Recommended Minimal Closed Loop

If you want to bring the system to life quickly, start with this minimum loop:

1. `PRD`
2. `Research Agent`
3. `generate-ref` skill
4. `generate-ref` command
5. output `specs/ref/*`
6. continue to `generate-global`

This works well because `ref/` is the most automation-friendly first step: the inputs are narrow, the outputs are stable, and the result reduces ambiguity for every downstream document.

## 5. Entry Conditions for Each Stage

### Phase 0: Memory

Inputs:

- `docs/PRD.md`
- `docs/Workflow.md`

Outputs:

- `specs/ref/prd_keywords.md`
- `specs/ref/std_lib_research.md`
- `specs/ref/perf_baseline.md`

Before moving to the next stage:

- terminology must be normalized
- standard-library candidate boundaries must be clear
- the performance budget must be written as a reviewable validation plan

### Phase 1: Global

Inputs:

- `PRD`
- `specs/ref/*`

Outputs:

- `app-business.md`
- `SA.md`
- `project-structure.md`
- `modules.md`
- `constraint.md`
- `API.md`

Before moving to the next stage:

- module boundaries must be clear
- API contracts must be stable enough to guide domain work
- key constraints must be explicit enough to support domain decomposition

### Phase 2: Domain

Inputs:

- `specs/global/*`
- `specs/ref/*`

Outputs:

- domain `SA.md`
- `layer-core.md`
- `layer-dao.md`
- `layer-biz.md`
- `layer-facade.md`

Before moving to the next stage:

- every module must have a clear implementation boundary
- layer responsibilities must be explicit
- major failure paths must be described

### Phase 2.5: Test Design

Inputs:

- `specs/global/*`
- `specs/domains/*`

Outputs:

- performance test design
- concurrency or idempotency test design when relevant
- boundary-case and failure-path validation design

Before moving to coding:

- every critical module must have clear test intent
- core constraints must map to reviewable test cases

### Phase 3: Coding

Inputs:

- `specs/global/*`
- `specs/domains/*`
- `specs/testing/*`

Outputs:

- `src/`
- `tests/`
- test results

## 6. Recommended Directory for AI Orchestration Assets

Use the following structure as the orchestration entry point:

```text
.codex/
└── modules/
    └── PRD-Pipeline/
        ├── agents/
        ├── commands/
        ├── docs/
        ├── memory/
        ├── rules/
        └── skills/
```

Suggested responsibilities:

- `modules/`: reusable pipelines or modular orchestration bundles
- `modules/PRD-Pipeline/agents/`: role prompts
- `modules/PRD-Pipeline/commands/`: direct task entry points
- `modules/PRD-Pipeline/docs/`: internal orchestration and planning documents
- `modules/PRD-Pipeline/memory/`: durable shared project context
- `modules/PRD-Pipeline/rules/`: repository-level constraints
- `modules/PRD-Pipeline/skills/`: reusable task capability packages

## 7. Orchestration Principles

1. Always generate downstream documents from upstream documents; do not skip stages.
2. Each agent should own its own outputs rather than directly rewriting another domain's document set.
3. Every document should state its input sources.
4. Every stage should preserve `Open Questions`.
5. Coding consumes frozen specs; it does not replace specification design.

## 8. Why Some Commands Are Markdown Files

In AI workflows, a `command` does not have to be an executable shell script.

It is often a reusable task-entry template that defines:

- trigger phrase
- required inputs
- expected outputs
- execution steps
- prohibitions and guardrails

Markdown works well for this because:

1. AI can read and follow natural-language constraints directly.
2. These commands constrain generation behavior more than they perform system calls.
3. Markdown is easier to review, version, and evolve collaboratively than one-off scripts.
4. The same command can later be used manually by a person or loaded by another agent as a workflow template.

You can think of the distinction like this:

- script command: makes the machine perform actions
- markdown command: makes the AI reason and produce outputs in a fixed workflow

Both can exist in the same repository, but markdown commands are often the better fit for document-generation workflows.

## 9. Current Status

The repository now has the first-pass document-system foundation in place:

1. core planning and orchestration assets
2. reusable rules for scope, branching, language, and progress sync
3. agent prompts for `ref`, `global`, `domain`, `testing`, and `acceptance`
4. commands and skills for staged document generation
5. a resumable progress tracker in `.codex/modules/PRD-Pipeline/docs/todo-plan.md`

The pipeline also now includes:

6. a complete `/prd-pipeline` command
7. a dedicated checkpoint file for resume behavior
8. an interface contract so other workflows can call the pipeline
9. partial-regeneration and scoped rerun modes such as `--force`, `--from`, `--only`, `--refresh`, `--domain`, and `--depth`

The next practical step is no longer to define the system itself. The next practical step is to use the system to generate real project documents under `specs/` and then implement from those outputs.

Recommended execution order:

1. `/prd-pipeline`

If a workflow needs finer-grained control, the internal sequence remains:

1. `/plan-docs`
2. `/generate-ref`
3. `/generate-global`
4. `/plan-domains`
5. `/generate-domain`
6. `/generate-tests`
7. `/generate-acceptance`
