# CodeTrace-AI

一个以 AI 为核心的仓库，用于演示一套**可复用的交付流水线**：由 agents、skills、commands、rules 与 memory 组成的系统，把一份 PRD 逐步转化为架构、构建契约、代码、测试与验收证据。

用来演示这套流水线的产品是 **CodeTrace**——一个轻量、local-first、零依赖的 Python 函数 tracing 框架（见 [docs/PRD.md](docs/PRD.md)）。本仓库真正的产物是流水线本身（位于 `.claude/`）；`src/` 与 `tests/` 应当由运行流水线自动生成。

## 活跃流程

`PRD -> Intent Pack -> SA -> Build Spec -> Task Slices -> Coding -> Verify -> Accept`

| 阶段 | 命令 | 产物 |
| --- | --- | --- |
| 0 Init | `/pipeline-init` | `specs/intent/brief.md` |
| 1 SA | `/generate-sa` | `specs/architecture/SA.md` |
| 2 Build Spec | `/generate-spec` | `specs/build/*` |
| 3 Slice | `/slice-work` | `specs/build/tasks.md` |
| 4 Implement | `/implement` | `src/`、`tests/` |
| 5 Verify | `/verify` | 验证证据 |
| 6 Accept | `/accept` | `specs/acceptance/*` |

统一入口是 **`/seechen`**（例如 `/seechen --run`、`/seechen --sa`，或一句自然语言请求）。

## 概述

仓库强调：

- **PRD 驱动**：`docs/PRD.md` 是唯一的产品级事实来源；所有下游产物都从上游派生
- **规范驱动**：在编码前先冻结架构与构建契约，使实现遵循 task slices 而非宽泛的重新解读
- **可复用 AI 约束**：agents、skills、commands、rules、memory 都纳入版本管理，统一放在 `.claude/`
- **可恢复工作流**：阶段状态保存在 `.claude/memory/`，使一次运行可以从上次完成的阶段继续

## 文档

- [产品需求文档 (PRD)](docs/PRD.md)
- [AI 开发工作流](docs/Workflow.md)
- [PRD-Pipeline 调用接口](.claude/docs/PRD-Pipeline-Interface.md)
- [CLAUDE.md](CLAUDE.md) —— 仓库入口与流水线总览

## 开始使用

本仓库面向在 Claude Code 中进行的 AI 辅助开发：先建立文档体系，再从冻结的规格生成代码。

### 先决条件

- Claude Code（或能读取仓库文件并遵循结构化约束的 AI 工具）
- 作为主事实来源的项目 PRD

### 使用方法

1. 先阅读 [PRD](docs/PRD.md)、[Workflow](docs/Workflow.md) 与 [CLAUDE.md](CLAUDE.md)。
2. 运行 `/seechen --run` 跑完整流程，或运行单个阶段如 `/seechen --sa`。
3. 查看 `.claude/` 下的可复用资产：
   - `agents/`：各阶段角色归属
   - `skills/`：各阶段执行指南
   - `commands/`：斜杠命令入口（`/seechen` 及各阶段）
   - `rules/`：仓库级约束
   - `memory/`：持久的流水线状态
   - `docs/`：流水线调用接口
4. 随每个阶段完成，查看 `specs/` 下生成的产物。

## 项目结构

```
CodeTrace-AI/
├── CLAUDE.md                  # 仓库入口与流水线总览
├── .claude/
│   ├── agents/                # 各阶段角色归属
│   ├── commands/              # 斜杠命令入口（/seechen、各阶段）
│   ├── skills/                # 各阶段执行指南
│   ├── rules/                 # 仓库约束
│   ├── memory/                # 持久的流水线状态
│   └── docs/                  # 流水线调用接口
├── docs/
│   ├── PRD.md                 # 产品需求文档
│   └── Workflow.md            # 逐阶段工作流定义
├── specs/                     # 流水线生成的产物（运行时创建）
├── LICENSE
├── README.md
└── README-zh.md
```

## 当前范围

仓库当前提供了覆盖完整交付流程（intent、architecture、build spec、task slices、coding、verification、acceptance）的编排系统。流水线从干净基线开始：`specs/` 下的生成产物，以及 `src/` 与 `tests/`，都由针对 `docs/PRD.md` 运行流水线产生。

## 贡献

欢迎围绕 AI-first workflow 提交改进。请遵循：

1. 遵循 `.claude/rules/` 中的规则。
2. 可复用 system-constraint 文件默认使用英文，除非有明确例外说明。
3. 使用与任务语义匹配的 branch，不要复用无关 branch。
4. 每个阶段完成后，同步更新 `.claude/memory/pipeline-state.md`。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- 受模块化 AI 辅助开发实践启发
- 用于展示 PRD 驱动的流水线如何把项目从需求带到经过验证的代码
