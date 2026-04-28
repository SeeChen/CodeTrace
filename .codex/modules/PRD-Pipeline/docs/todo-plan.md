# PRD-Pipeline Refactor Todo Plan

This file records the staged migration from the legacy document-generation pipeline to the active delivery-oriented pipeline.

## Usage

1. Update the status after each completed task.
2. Resume from the first `todo` or `in_progress` item after interruption.
3. Keep this plan aligned with `memory/pipeline-state.md`.
4. Record completed work in the progress log instead of relying on hidden conversation history.

## Migration Principles

- `docs/PRD.md` remains the primary source of truth.
- New workflow assets should target the active `intent -> architecture -> build -> tasks -> coding -> verify -> accept` model.
- Legacy assets may remain during migration, but should not attract new structural dependency unless needed temporarily.
- Agents and skills should stay compact and docs-backed.

## Todo List

| ID | Status | Item | Output |
| :-- | :-- | :-- | :-- |
| REF-001 | done | Add the refactor blueprint for the new delivery-oriented pipeline. | `docs/PRD-Pipeline-Refactor-Blueprint.md` |
| REF-002 | done | Add the agent and skill design rule for compact, docs-backed orchestration assets. | `rules/agent-skill-design.md` |
| REF-003 | done | Rewrite the repository workflow to the active stage model. | `docs/Workflow.md` |
| REF-004 | done | Rewrite the pipeline README and interface around the active stage model. | `README.md`, `docs/PRD-Pipeline-Interface.md` |
| REF-005 | done | Replace legacy-first workflow memory with the active memory set. | `memory/*` |
| REF-006 | done | Add the new top-level command set. | `commands/pipeline-init.md`, `generate-sa.md`, `generate-spec.md`, `slice-work.md`, `implement.md`, `verify.md`, `accept.md` |
| REF-007 | done | Add the new core skill set for intent, architecture, build spec, and task slicing. | `skills/normalize-prd/`, `generate-sa/`, `generate-build-spec/`, `slice-build-tasks/` |
| REF-008 | done | Add or migrate the active agent set for PRD analysis, build-spec generation, coding, and QA acceptance. | `agents/*` |
| REF-009 | done | Remove legacy pipeline assets from `.codex/modules/PRD-Pipeline` while preserving external reviewable documents. | cleaned command, skill, agent, docs, and rule set |
| REF-010 | done | Clear the legacy generated spec set and legacy checkpoint so the active workflow has a clean output surface. | cleaned `specs/` legacy files and removed legacy checkpoint |
| REF-011 | todo | Run the new workflow on the current `docs/PRD.md` and generate the first active outputs. | `specs/intent/*`, `specs/architecture/*`, `specs/build/*`, `specs/acceptance/criteria.md` |

## Current Focus

- The workflow scaffolding is being migrated first.
- Output generation under the new structure remains the next milestone.

## Progress Log

- `done` `REF-001` Added the refactor blueprint that redefines the active workflow as `PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`.
- `done` `REF-002` Added the new rule that keeps agents and skills compact, navigational, and docs-backed.
- `done` `REF-003` Rewrote `docs/Workflow.md` to the active stage model and smaller target artifact layout.
- `done` `REF-004` Rewrote the pipeline README and interface to match the new delivery-oriented flow.
- `done` `REF-005` Added active memory files for pipeline state, frozen decisions, open questions, and implementation logging while keeping a legacy checkpoint note.
- `done` `REF-006` Added the new top-level command set for init, architecture, build spec, work slicing, implementation, verification, and acceptance.
- `done` `REF-007` Added the new core skill set for intent normalization, system architecture generation, build-spec generation, and task slicing.
- `done` `REF-008` Added the active agent set for PRD analysis, build-spec generation, implementation ownership, and QA acceptance.
- `done` `REF-009` Removed legacy pipeline assets from `.codex/modules/PRD-Pipeline` and kept only the active delivery-oriented command path.
- `done` `REF-010` Cleared the old generated spec tree and removed the legacy checkpoint so the next run can write only active outputs.
