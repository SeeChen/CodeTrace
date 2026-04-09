# CodeTrace-AI

这是一个以 AI 为核心的开发仓库，目标是通过 PRD 驱动的文档体系、可复用的系统约束以及分阶段规格生成来构建软件。项目重点是把单一 PRD 逐步转化为可以驱动 Coding、Testing 与 Acceptance 的文档系统。

## 概述

CodeTrace-AI 探索一种模块化工作流：AI 通过明确的 rules、skills、commands、memory 与 staged specifications 协作完成文档与后续实现。项目强调：

- **PRD 驱动规划**：从单一 PRD 出发，根据真实项目边界决定文档体系
- **规范驱动开发**：先生成 global、domain、testing、acceptance 文档，再进入实现
- **可复用 AI 约束**：将 system prompts、rules、commands、skills、memory 纳入版本管理
- **可恢复工作流**：持续记录进度，使工作可以从上次完成点继续而不是重来

## 文档

- [产品需求文档 (PRD)](docs/PRD.md)
- [AI 开发工作流](docs/Workflow.md)
- [PRD 到 Coding 的文档编排](.codex/docs/PRD-to-Coding-Orchestration.md)
- [文档系统任务计划](.codex/docs/todo-plan.md)

## 开始使用

本仓库面向 AI 辅助开发，当前重点是先建立完整的 document system，再让后续 Coding 建立在清晰、可追溯的规格之上。

### 先决条件

- 能读取仓库文件并遵循结构化约束的 AI 开发工具
- 作为主事实来源的项目 PRD
- 对 staged specification workflow 有基本理解

### 使用方法

1. 先阅读 [PRD](docs/PRD.md) 与 [Workflow](docs/Workflow.md)。
2. 结合 `docs/PRD.md`、`docs/Workflow.md` 与 `.codex/docs/` 中的编排文档理解目标文档链路。
3. 使用 `.codex/` 下的可复用资产：
   - `agents/`：system prompt 角色
   - `skills/`：任务型生成流程
   - `commands/`：可复用任务入口
   - `rules/`：仓库级约束
   - `memory/`：稳定的项目上下文
4. 按阶段生成 `specs/ref/`、`specs/global/`、`specs/domains/`、`specs/testing/` 与 `specs/acceptance/`。

## 项目结构

```
CodeTrace-AI/
├── .codex/
│   ├── agents/                 # 可复用 agent system prompts
│   ├── commands/               # 可复用 command 入口
│   ├── docs/                   # Codex 内部编排与计划文档
│   ├── memory/                 # 稳定 workflow memory
│   ├── modules/                # Pipeline 或模块化 bundle
│   ├── rules/                  # AI 工作流规则
│   └── skills/                 # 任务型生成技能
├── docs/
│   ├── PRD.md                          # 产品需求文档
│   ├── Workflow.md                     # 高层工作流参考
├── LICENSE
├── README.md
└── README-zh.md
```

## 当前范围

当前仓库已经具备以下文档系统基础能力：

- PRD 边界判断
- 文档树规划
- Phase 0 `ref` 生成
- global 规格生成
- domain 规划与单域展开
- testing 文档生成
- acceptance 文档生成

代码实现仍然位于这些文档阶段之后。

## 贡献

欢迎围绕 AI-first workflow 提交改进。请遵循：

1. 遵循 `.codex/rules/` 中的规则。
2. 可复用 system-constraint 文件默认使用英文，除非有明确例外说明。
3. 使用与任务语义匹配的 branch，不要复用无关 branch。
4. 完成文档生成工作后，记得同步更新进度跟踪文件。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- 受模块化 AI 辅助开发实践启发
- 用于展示 PRD 驱动的文档系统如何组织后续 Coding 工作

