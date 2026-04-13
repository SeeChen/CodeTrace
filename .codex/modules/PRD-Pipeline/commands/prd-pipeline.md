# Command: prd-pipeline

## Purpose

Run the full PRD-Pipeline from planning to acceptance-document generation with minimal interruption. Unless a true clarification blocker exists, continue automatically until all required documents for the current project have been generated.

## Direct Invocation

Trigger this workflow with:

- `/prd-pipeline`
- `/prd-pipeline docs/PRD.md`
- `/prd-pipeline docs/PRD.md --force`
- `/prd-pipeline docs/PRD.md --from global`
- `/prd-pipeline docs/PRD.md --only acceptance`
- `/prd-pipeline docs/PRD.md --refresh global,domains`
- `/prd-pipeline docs/PRD.md --domain comparison_reporting`
- `/prd-pipeline docs/PRD.md --depth balanced`
- `/prd-pipeline docs/PRD.md --depth deep`

This command may be run by a user directly or invoked by another workflow.

## Invocation Modes

Use these modes when full resume behavior is not enough:

- `--force`
  Ignore completed-stage status and regenerate the whole pipeline from planning through finalize.
- `--from <stage>`
  Re-run from a named stage onward. Supported stage names: `plan-docs`, `ref`, `global`, `plan-domains`, `domains`, `testing`, `acceptance`, `finalize`.
- `--only <stage>`
  Run only one stage and update checkpoint state accordingly.
- `--refresh <scope>`
  Regenerate a comma-separated scope such as `ref`, `global`, `domains`, `testing`, `acceptance`, or a mixed scope like `global,domains`.
- `--domain <name>`
  Limit Stage 5 to one named domain. This is valid with `--from domains`, `--only domains`, or `--refresh domains`.
- `--depth balanced|deep`
  Control document density. `balanced` keeps planning documents concise while producing implementation-ready detail in design documents. `deep` expands design, failure-path, contract, and validation detail further.

When multiple options are provided, interpret them in this order:

1. `--force`
2. `--only`
3. `--from`
4. `--refresh`
5. `--domain`
6. `--depth`

## Read First

1. `docs/PRD.md`
2. `docs/Workflow.md`
3. `.codex/modules/PRD-Pipeline/docs/PRD-to-Coding-Orchestration.md`
4. `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Interface.md`
5. `.codex/modules/PRD-Pipeline/rules/rules.md`
6. `.codex/modules/PRD-Pipeline/rules/pipeline-checkpoint.md`
7. `.codex/modules/PRD-Pipeline/memory/workflow-memory.md`
8. `.codex/modules/PRD-Pipeline/memory/prd-pipeline-checkpoint.md`

## Execution Model

This is a complete pipeline command. It owns the end-to-end document workflow:

1. project-boundary planning
2. Phase 0 reference generation
3. global specification generation
4. domain planning
5. domain-by-domain specification expansion
6. testing-document generation
7. acceptance-document generation
8. final status sync

## Resume Behavior

Before doing any work:

1. read `.codex/modules/PRD-Pipeline/memory/prd-pipeline-checkpoint.md`
2. detect the last completed stage
3. resume from the first incomplete stage
4. do not restart completed stages unless the inputs changed materially

If the checkpoint says the pipeline is complete, verify outputs briefly and stop unless the user requested regeneration.

If the user requested `--force`, `--from`, `--only`, or `--refresh`, that explicit invocation overrides the default resume behavior.

## Clarification Policy

Do not stop for routine confirmation.

Ask the user only when:

1. the PRD is missing
2. the PRD is unreadable or contradictory in a way that blocks the next stage
3. the target output location is ambiguous and risky
4. the user explicitly requests an alternative scope

If a blocker affects only one area, continue all non-blocked work first.

## Stage Flow

### Stage 1: Plan Documents

Run:

- `Orchestrator Agent`
- `plan-doc-structure` skill
- `/plan-docs`

Output:

- project-specific document plan
- target document tree
- required, optional, deferred, and unnecessary document decisions

Checkpoint after completion.

Depth behavior:

- keep planning concise and decision-oriented
- do not over-expand planning into domain internals

### Stage 2: Generate `ref`

Run:

- `Research Agent`
- `generate-ref` skill
- `/generate-ref`

Output:

- `specs/ref/*`

Checkpoint after completion.

### Stage 3: Generate `global`

Run:

- `Architect Agent`
- `generate-global` skill
- `/generate-global`

Output:

- `specs/global/*`

Checkpoint after completion.

Depth behavior:

- keep the global layer architectural rather than domain-specific
- include enough detail that downstream domain work does not need to re-derive contracts, lifecycle expectations, failure boundaries, or implementation-relevant frozen decisions

### Stage 4: Plan Domains

Run:

- `Domain Planner Agent`
- `plan-domains` skill
- `/plan-domains`

Output:

- domain map
- domain expansion order

Checkpoint after completion.

### Stage 5: Generate Domain Specs

Run repeatedly for each required domain:

- `Domain Spec Agent`
- `generate-domain-spec` skill
- `/generate-domain`

Output:

- `specs/domains/<domain-name>/*`

Checkpoint after each domain.

Depth behavior:

- domain specs should be implementation-ready, not merely skeletal
- include lifecycle, responsibilities, data/control flow, failure paths, extension points, dependency notes, and testing implications for each required layer

### Stage 6: Generate Testing Documents

Run:

- `Test Design Agent`
- `generate-test-design` skill
- `/generate-tests`

Output:

- `specs/testing/*`

Checkpoint after completion.

Depth behavior:

- testing outputs should include scenario matrices, requirement coverage, major fixtures or dependencies, pass/fail intent, and remaining validation risk

### Stage 7: Generate Acceptance Documents

Run:

- `Acceptance Agent`
- `generate-acceptance` skill
- `/generate-acceptance`

Output:

- `specs/acceptance/*`

Checkpoint after completion.

Depth behavior:

- acceptance outputs should stay concise in shape but concrete in gates, evidence, and non-blocking scope decisions

### Stage 8: Finalize

Verify:

1. required document phases are complete
2. deferred items are documented explicitly
3. open questions are preserved
4. `.codex/modules/PRD-Pipeline/memory/prd-pipeline-checkpoint.md` is marked complete
5. `specs/summary.md` or equivalent status output reflects the final state

## Self-Closure Requirements

The pipeline must remain self-contained:

- each stage consumes only upstream artifacts and stable pipeline rules
- each stage writes outputs for the next stage
- each stage records progress before exiting
- each stage can resume from checkpoint without hidden memory

## Composition Rules

Other workflows may call this workflow by:

1. loading this command
2. honoring its checkpoint file
3. providing the same core inputs
4. reading `.codex/modules/PRD-Pipeline/docs/PRD-Pipeline-Interface.md`

When called by another workflow, this command remains authoritative for its internal stage order and checkpoint semantics.

## Output

This command should leave the repository with:

- planning outputs
- `specs/ref/*`
- `specs/global/*`
- `specs/domains/*`
- `specs/testing/*`
- `specs/acceptance/*`
- updated checkpoint and status tracking

## Guardrails

- Do not skip stages when required upstream artifacts are missing.
- Do not regenerate already-complete stages without reason.
- Do not overwrite open questions with unsupported assumptions.
- Do not stop after intermediate document generation unless a real blocker exists.
- Do not keep every stage at the same level of detail; planning may stay lean, while design and validation stages should expand to implementation-supporting depth.
