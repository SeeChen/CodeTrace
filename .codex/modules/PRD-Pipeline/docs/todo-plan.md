# Document System Todo Plan

本文件记录“从 PRD 到文档体系”的落地任务清单。目标是把文档系统所需的 `agent / skill / rule / command / memory` 分阶段落库，并持续更新状态，保证中断后可以继续。

## 使用方式

1. 每完成一个任务，就更新一次状态。
2. 如中断，下一次从最后一个 `todo` 或 `in_progress` 项继续。
3. 如果过程中发现边界变化，先更新本计划，再继续执行。
4. `Progress Log` 必须记录已完成项，避免重新开始。

## 当前原则

- `PRD` 是唯一主源。
- `Workflow.md` 是流程参考，不是固定模板。
- 示例目录结构可以调整，必须先判断项目边界再生成真实目录结构。
- 下游文档必须依赖上游文档，不能跳级生成。

## Todo List

| ID | Status | Item | Output |
| :-- | :-- | :-- | :-- |
| DOC-001 | done | Create the `Orchestrator Agent` system prompt for project-boundary analysis, document scoping, and target directory planning. | `.codex/modules/PRD-Pipeline/agents/orchestrator-agent.md` |
| DOC-002 | done | Create `doc-scope-rule` so agents must determine project boundary before choosing the document set. | `.codex/modules/PRD-Pipeline/rules/doc-scope.md` |
| DOC-003 | done | Create the `plan-doc-structure` skill for first-pass document tree and document-list planning from the PRD. | `.codex/modules/PRD-Pipeline/skills/plan-doc-structure/` |
| DOC-004 | done | Create the `/plan-docs` command as the document-planning entry point. | `.codex/modules/PRD-Pipeline/commands/plan-docs.md` |
| DOC-005 | done | Create the summary-sync rule so every document-generation step updates durable progress tracking. | `.codex/modules/PRD-Pipeline/rules/summary-sync.md` |
| DOC-006 | done | Create the `Architect Agent` system prompt. | `.codex/modules/PRD-Pipeline/agents/architect-agent.md` |
| DOC-007 | done | Create the `generate-global` skill. | `.codex/modules/PRD-Pipeline/skills/generate-global/` |
| DOC-008 | done | Create the `/generate-global` command. | `.codex/modules/PRD-Pipeline/commands/generate-global.md` |
| DOC-009 | done | Create the `Domain Planner Agent` system prompt. | `.codex/modules/PRD-Pipeline/agents/domain-planner-agent.md` |
| DOC-010 | done | Create the `plan-domains` skill. | `.codex/modules/PRD-Pipeline/skills/plan-domains/` |
| DOC-011 | done | Create the `/plan-domains` command. | `.codex/modules/PRD-Pipeline/commands/plan-domains.md` |
| DOC-012 | done | Create the `Domain Spec Agent` system prompt. | `.codex/modules/PRD-Pipeline/agents/domain-spec-agent.md` |
| DOC-013 | done | Create the `generate-domain-spec` skill. | `.codex/modules/PRD-Pipeline/skills/generate-domain-spec/` |
| DOC-014 | done | Create the `/generate-domain <name>` command. | `.codex/modules/PRD-Pipeline/commands/generate-domain.md` |
| DOC-015 | done | Create the `Test Design Agent` system prompt. | `.codex/modules/PRD-Pipeline/agents/test-design-agent.md` |
| DOC-016 | done | Create the `generate-test-design` skill. | `.codex/modules/PRD-Pipeline/skills/generate-test-design/` |
| DOC-017 | done | Create the `/generate-tests` command. | `.codex/modules/PRD-Pipeline/commands/generate-tests.md` |
| DOC-018 | done | Create the `Acceptance Agent` system prompt. | `.codex/modules/PRD-Pipeline/agents/acceptance-agent.md` |
| DOC-019 | done | Create the `generate-acceptance` skill. | `.codex/modules/PRD-Pipeline/skills/generate-acceptance/` |
| DOC-020 | done | Create the `/generate-acceptance` command. | `.codex/modules/PRD-Pipeline/commands/generate-acceptance.md` |

## Current Focus

- All tasks in the current todo list are complete.
- `DOC-001` is complete and already reflected in the repository state.

## Progress Log

- `done` `DOC-001` Created the English `Orchestrator Agent` prompt and aligned it with current system-constraint language rules.
- `done` `DOC-002` Added the document-scope rule to both rule trees and indexed it for discovery.
- `done` `DOC-003` Added the `plan-doc-structure` skill and its lightweight output contract reference.
- `done` `DOC-004` Added the `/plan-docs` command as the planning entry point.
- `done` `DOC-005` Added the summary-sync rule so progress tracking stays resumable.
- `done` `DOC-006` Added the `Architect Agent` system prompt for the global specification layer.
- `done` `DOC-007` Added the `generate-global` skill and output contract reference.
- `done` `DOC-008` Added the `/generate-global` command for the global-spec generation step.
- `done` `DOC-009` Added the `Domain Planner Agent` system prompt for domain-level decomposition.
- `done` `DOC-010` Added the `plan-domains` skill and its planning contract reference.
- `done` `DOC-011` Added the `/plan-domains` command for domain mapping.
- `done` `DOC-012` Added the `Domain Spec Agent` system prompt for one-domain-at-a-time expansion.
- `done` `DOC-013` Added the `generate-domain-spec` skill and its domain output contract reference.
- `done` `DOC-014` Added the `/generate-domain` command for single-domain spec generation.
- `done` `DOC-015` Added the `Test Design Agent` system prompt for test-planning ownership.
- `done` `DOC-016` Added the `generate-test-design` skill and its testing contract reference.
- `done` `DOC-017` Added the `/generate-tests` command for testing-layer generation.
- `done` `DOC-018` Added the `Acceptance Agent` system prompt for milestone-level acceptance gates.
- `done` `DOC-019` Added the `generate-acceptance` skill and its acceptance contract reference.
- `done` `DOC-020` Added the `/generate-acceptance` command for final acceptance-document generation.


