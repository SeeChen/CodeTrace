# PRD-Pipeline Refactor Blueprint

This document defines how to refactor the current PRD-driven workflow into a delivery-oriented pipeline that can move from one PRD to architecture, implementation specs, coding, testing, and acceptance with less drift and lower context cost.

## 1. Refactor Goal

The current pipeline is strong at producing layered documents, but it is still too document-centric. The refactor should make it stronger at producing coding-ready outputs.

The new target flow is:

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Unit Tests -> Acceptance`

This refactor keeps the existing modular structure of `Agents`, `Skills`, `Rules`, `Commands`, `Docs`, and `Memory`, but changes their responsibilities so each part contributes directly to delivery.

## 2. Problems to Solve

The refactor exists to address the following problems:

1. The current workflow can generate many documents before it produces a coding-ready contract.
2. Domain documents are useful, but they can still leave too much implementation freedom for downstream agents.
3. There is no strong intermediate layer that freezes file planning, interface contracts, artifact schema, and test intent before coding begins.
4. The current pipeline emphasizes phase completeness more than implementation traceability.
5. Agent and skill design can become too heavy if background knowledge is embedded directly into the execution files.

## 3. Refactor Principles

1. Treat the PRD as the only product-level source of truth.
2. Generate downstream outputs only from upstream artifacts.
3. Freeze architecture before generating implementation-ready specs.
4. Treat specs as executable planning assets, not as passive documentation.
5. Keep orchestration assets lightweight and composable.
6. Store detailed references in `docs/` and load them only when needed.
7. Keep all reusable orchestration documents in English.

## 4. New Delivery Model

The refactored workflow should use seven stages.

### Stage 0: Normalize PRD

Purpose:
Convert the PRD into a compact project intent pack that is easier for downstream agents to consume consistently.

Inputs:
- `docs/PRD.md`
- `docs/Workflow.md`

Outputs:
- `specs/intent/brief.md`

Required sections:
- project mission
- MVP scope
- out-of-scope items
- non-negotiable constraints
- core entities and actions
- acceptance framing
- open questions

### Stage 1: Generate SA

Purpose:
Freeze the system architecture before any implementation planning starts.

Inputs:
- `specs/intent/brief.md`

Outputs:
- `specs/architecture/SA.md`

Required sections:
- system context
- module boundaries
- public API surface
- extension points
- runtime lifecycle
- cross-cutting constraints
- architecture decisions
- open questions

### Stage 2: Generate Build Spec

Purpose:
Translate architecture into implementation-ready contracts that coding agents can follow with low ambiguity.

Inputs:
- `specs/intent/brief.md`
- `specs/architecture/SA.md`

Outputs:
- `specs/build/module-map.md`
- `specs/build/interfaces.md`
- `specs/build/file-plan.md`
- `specs/build/artifact-schema.md`
- `specs/build/failure-policy.md`
- `specs/build/test-matrix.md`

Required guarantees:
- every implementation area maps to a module
- every public interface has an explicit contract
- every artifact has a predictable schema or directory rule
- every failure type has an isolation policy
- every important requirement maps to at least one test intent

### Stage 3: Slice Work

Purpose:
Split the build spec into small implementation tasks that can be delegated safely to coding agents.

Inputs:
- `specs/build/*`

Outputs:
- `specs/build/tasks.md`

Required sections:
- task sequence
- file ownership
- prerequisites
- expected outputs
- required tests
- acceptance notes

### Stage 4: Implement

Purpose:
Generate production code and tests from frozen task slices instead of from broad conversational interpretation.

Inputs:
- `specs/build/tasks.md`
- `specs/build/*`

Outputs:
- `src/`
- `tests/`
- implementation notes if needed

Required rules:
- coding may not silently redefine architecture
- coding must follow file ownership from the task slices
- unresolved spec conflicts must be written back to memory before continuing

### Stage 5: Verify

Purpose:
Validate the implementation against the build spec and task-level expectations.

Inputs:
- `src/`
- `tests/`
- `specs/build/test-matrix.md`

Outputs:
- test execution evidence
- defect list
- fix loop records when applicable

Required checks:
- unit test pass status
- integration behavior where relevant
- failure-path validation
- contract conformance review

### Stage 6: Accept

Purpose:
Decide whether the current milestone is complete based on explicit evidence instead of broad narrative summaries.

Inputs:
- implementation outputs
- verification outputs
- original acceptance framing

Outputs:
- `specs/acceptance/report.md`

Required sections:
- scope delivered
- evidence summary
- blocked or deferred items
- final acceptance status

## 5. Recommended Artifact Layout

The repository should gradually move toward the following output structure:

```text
specs/
├── intent/
│   └── brief.md
├── architecture/
│   └── SA.md
├── build/
│   ├── module-map.md
│   ├── interfaces.md
│   ├── file-plan.md
│   ├── artifact-schema.md
│   ├── failure-policy.md
│   ├── test-matrix.md
│   └── tasks.md
└── acceptance/
    └── report.md
```

This structure is intentionally smaller than the current pipeline output tree. The reduction is deliberate. The goal is to keep only the artifacts that directly improve implementation accuracy and validation.

## 6. Responsibility Model

The six orchestration building blocks should be redefined as follows.

### Docs

`Docs` store durable project truth and reusable references.

They should contain:
- PRD
- workflow definitions
- detailed guidance documents
- reference contracts
- long-form examples

They should not contain:
- ephemeral status
- implementation progress that belongs in memory

### Memory

`Memory` stores durable execution state and frozen decisions.

It should contain:
- stage progress
- resolved decisions
- open questions
- accepted deviations
- task completion state

It should not contain:
- full design explanations that belong in docs

### Rules

`Rules` define non-negotiable generation and delivery boundaries.

They should cover:
- stage order
- source-of-truth hierarchy
- escalation conditions
- doc size and context economy
- acceptance constraints

### Agents

`Agents` define role perspective and ownership.

Recommended primary agents:
- `prd-analyst-agent`
- `architect-agent`
- `spec-builder-agent`
- `coding-agent`
- `qa-acceptance-agent`

### Skills

`Skills` define reusable execution methods.

Recommended primary skills:
- `normalize-prd`
- `generate-sa`
- `generate-build-spec`
- `slice-build-tasks`
- `implement-from-task`
- `verify-build`
- `accept-milestone`

### Commands

`Commands` define task entry points.

Recommended top-level commands:
- `/pipeline-init`
- `/generate-sa`
- `/generate-spec`
- `/slice-work`
- `/implement`
- `/verify`
- `/accept`

## 7. Recommended Agent Set

The current agent set should be simplified.

### Keep

- `architect-agent`
- `acceptance-agent`

### Replace or Rename

- `research-agent` -> `prd-analyst-agent`
- `domain-planner-agent` + `domain-spec-agent` -> `spec-builder-agent`
- `test-design-agent` -> `qa-acceptance-agent`

### Add

- `coding-agent`

This change reduces role fragmentation and makes the handoff path easier to reason about.

## 8. Recommended Skill Set

The current skill set should also be refocused.

### Keep Conceptually

- planning from the PRD
- architecture generation
- acceptance generation

### Replace

- `generate-ref` with `normalize-prd`
- `generate-global` with `generate-sa`
- `plan-domains` + `generate-domain-spec` with `generate-build-spec`
- `generate-test-design` with `verify-build`

### Add

- `slice-build-tasks`
- `implement-from-task`

The key idea is that domain planning should no longer stop at descriptive domain documents. It should produce implementation-facing build contracts.

## 9. Recommended Command Flow

The current command set should be reorganized into a shorter and more direct flow.

### New Main Flow

1. `/pipeline-init`
2. `/generate-sa`
3. `/generate-spec`
4. `/slice-work`
5. `/implement`
6. `/verify`
7. `/accept`

### Why This Is Better

1. The command names map more directly to delivery work.
2. The transition into coding is explicit.
3. Verification is a first-class stage, not only a document-generation side effect.
4. Acceptance becomes evidence-driven.

## 10. Memory Refactor

The current memory model should be extended from checkpointing into delivery state tracking.

Recommended files:

- `memory/pipeline-state.md`
  Stage status, current task, blockers, and next action.
- `memory/frozen-decisions.md`
  Architecture and contract decisions that downstream stages may not override silently.
- `memory/open-questions.md`
  Unresolved design points and required escalation items.
- `memory/implementation-log.md`
  Task completion, deviations, and fix-loop notes.

## 11. Rules to Add or Strengthen

The refactor should add or strengthen the following rules:

1. Coding may not start before `SA.md` and `specs/build/*` are present.
2. Acceptance may not introduce new product requirements.
3. Agents and skills must stay lightweight and load references on demand.
4. Detailed schemas, examples, and research belong in `docs/`, not in agents or skills.
5. Every generated artifact must declare its input sources.
6. Every implementation task must map back to a build-spec section.

## 12. Mapping from Current Outputs

The current outputs can be migrated instead of discarded.

Recommended mapping:

- `specs/ref/*` -> merge relevant material into `specs/intent/brief.md` or move to supporting `docs/`
- `specs/global/*` -> condense into `specs/architecture/SA.md`
- `specs/domains/*` -> convert into `specs/build/*`
- `specs/testing/*` -> convert into `specs/build/test-matrix.md`
- `specs/acceptance/criteria.md` -> evolve into `specs/acceptance/report.md` and a reusable acceptance contract

## 13. Immediate Refactor Plan

The recommended implementation sequence is:

1. Add the new blueprint and design rules.
2. Introduce the new agent and skill constraints.
3. Define the new stage model in the workflow docs.
4. Create the new command interfaces.
5. Create the new skill contracts.
6. Create the new memory files.
7. Migrate existing spec outputs into the smaller target structure.
8. Run one end-to-end project pass from `PRD -> SA -> Build Spec -> task slices`.
9. Only then enable coding automation by default.

## 14. Success Criteria

The refactor is successful when:

1. one PRD can produce a stable `SA` and `Build Spec` set
2. coding agents can implement from task slices without reinterpreting the PRD broadly
3. verification outputs map cleanly back to the build spec
4. acceptance decisions rely on evidence, not only document presence
5. agent and skill files remain compact, navigational, and context-efficient

## 15. Final Recommendation

Do not treat this refactor as a document rewrite only. Treat it as a contract redesign for AI-assisted delivery.

The best next practical milestone is:

`PRD -> specs/intent/brief.md -> specs/architecture/SA.md -> specs/build/* -> specs/build/tasks.md`

Once that milestone is stable, coding and validation can become much more reliable.
