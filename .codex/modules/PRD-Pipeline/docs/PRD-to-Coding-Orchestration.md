# PRD 到 Coding 文档编排工作流

本文档定义一个适合纯 AI Coding 场景的文档编排流程。目标是在只有 `PRD` 的前提下，通过一组稳定的 `Agent / Skill / Rule / Command / Memory`，逐步生成可执行的规格文档，最终驱动 Coding。

## 1. 设计目标

这套工作流解决三个问题：

1. AI 不能直接从 PRD 跳到 Coding，否则容易遗漏约束或在中途漂移。
2. 不同 Agent 如果没有统一输入输出边界，很容易重复生成、互相覆盖，或者写出冲突文档。
3. 文档必须既能让 AI 读，也能让人复核，因此需要结构稳定、职责清晰。

## 2. 从 PRD 到 Coding 的推荐链路

推荐采用以下顺序推进：

`PRD -> Memory -> Global -> Domain -> Test Design -> Coding`

对应目录如下：

1. `specs/ref/`
2. `specs/global/`
3. `specs/domains/`
4. `specs/testing/`
5. `src/` 与 `tests/`

## 3. 五类构件的职责

### Agent

Agent 是角色。它负责“站在什么视角做事”。

例如：

- `Research Agent` 负责 Phase 0 的 `ref/`
- `Architect Agent` 负责 `global/`
- `Domain Expert Agent` 负责 `domains/`
- `Test Designer Agent` 负责 `testing/`
- `Coding Agent` 负责实现代码

### Skill

Skill 是能力包。它负责“如何稳定完成一类任务”。

例如：

- `generate-ref` 负责从 PRD 生成 `specs/ref/`
- 后续可以有 `generate-global`
- 后续可以有 `generate-domain-spec`
- 后续可以有 `generate-test-plan`

### Rule

Rule 是约束。它负责“什么可以做，什么不可以做”。

例如：

- 只能基于 `PRD` 和上游规格生成
- 必须区分事实、推断、待确认项
- 未锁定 API 前不得进入 Coding
- 不能伪造 benchmark 结果

### Command

Command 是入口。它负责“用户说一句话后，AI 应该触发哪条工作流”。

它可以是脚本，也可以是 markdown prompt 模板。

例如：

- `generate-ref`
- `generate-global`
- `generate-domain tracing_engine`
- `generate-tests persistence`

### Memory

Memory 是长期上下文。它负责“跨多轮保留哪些项目共识”。

例如：

- 项目术语表
- 已确认架构约束
- 文档生成顺序
- 已冻结 API 决策
- 当前阶段状态

## 4. 推荐的最小闭环

如果你要先把这套系统跑起来，建议先做下面这一条闭环：

1. `PRD`
2. `Research Agent`
3. `generate-ref` skill
4. `generate-ref` command
5. 输出 `specs/ref/*`
6. 进入 `generate-global`

原因很简单：`ref/` 是最适合作为第一步自动化的部分，输入单一，输出稳定，而且能为后续所有文档降噪。

## 5. 每一阶段的进入条件

### Phase 0: Memory

输入：

- `docs/PRD.md`
- `docs/Workflow.md`

输出：

- `specs/ref/prd_keywords.md`
- `specs/ref/std_lib_research.md`
- `specs/ref/perf_baseline.md`

进入下一阶段前必须满足：

- 术语已归一
- 标准库候选边界清晰
- 性能预算已写成可验证计划

### Phase 1: Global

输入：

- `PRD`
- `specs/ref/*`

输出：

- `app-business.md`
- `SA.md`
- `project-structure.md`
- `modules.md`
- `constraint.md`
- `API.md`

进入下一阶段前必须满足：

- 模块边界明确
- API 契约冻结
- 关键约束可以指导 Domain 拆解

### Phase 2: Domain

输入：

- `specs/global/*`
- `specs/ref/*`

输出：

- 各领域 `SA.md`
- `layer-core.md`
- `layer-dao.md`
- `layer-biz.md`
- `layer-facade.md`

进入下一阶段前必须满足：

- 每个模块都有实现边界
- 层级职责明确
- 关键异常路径已描述

### Phase 2.5: Test Design

输入：

- `specs/global/*`
- `specs/domains/*`

输出：

- 性能测试设计
- 并发/幂等测试设计
- 边界条件测试设计

进入 Coding 前必须满足：

- 每个关键模块都有对应测试意图
- 核心红线可映射为测试用例

### Phase 3: Coding

输入：

- `specs/global/*`
- `specs/domains/*`
- `specs/testing/*`

输出：

- `src/`
- `tests/`
- 测试结果

## 6. 推荐目录

建议补充以下目录作为 AI 编排入口：

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

职责建议：

- `modules/`: 可继续扩展的 pipeline 或模块化 bundle
- `modules/PRD-Pipeline/agents/`: 角色 prompt
- `modules/PRD-Pipeline/commands/`: 用户可直接触发的任务入口
- `modules/PRD-Pipeline/docs/`: Codex 内部编排与计划文档
- `modules/PRD-Pipeline/memory/`: 跨轮共享的项目记忆
- `modules/PRD-Pipeline/rules/`: 仓库级约束
- `modules/PRD-Pipeline/skills/`: 具体任务能力包

## 7. 编排原则

1. 永远从上游文档生成下游文档，不要跳阶段。
2. 每个 Agent 只负责自己的输出，不直接改别人的领域文档。
3. 每个文档都必须写明输入来源。
4. 每个阶段结束都要留下 `Open Questions`。
5. Coding 只消费已冻结规格，不替代规格设计。

## 8. 为什么有些 command 是 `.md`

因为在 AI 工作流里，`command` 不一定是“执行 shell 脚本”。

它经常是一个“可复用的任务入口模板”，本质上是：

- 触发词
- 输入要求
- 输出要求
- 执行步骤
- 禁止事项

这类内容用 markdown 很合适，因为：

1. AI 更容易直接读取自然语言规范。
2. 这类 command 主要是“约束生成行为”，不是做系统调用。
3. markdown 比脚本更容易审阅、版本控制、协作修改。
4. 同一条 command 以后既可以被人手动调用，也可以被 Agent 当提示词模板读取。

你可以把它理解成：

- 脚本型 command：让机器执行动作
- markdown 型 command：让 AI 按固定流程思考和产出

在你的项目里，两种都可以存在，但在“文档生成工作流”里，markdown command 往往更实用。

## 9. Current Status

The repository now has the first-pass document-system foundation in place:

1. core planning and orchestration assets
2. reusable rules for scope, branching, language, and progress sync
3. agent prompts for `ref`, `global`, `domain`, `testing`, and `acceptance`
4. commands and skills for staged document generation
5. a resumable progress tracker in `.codex/modules/PRD-Pipeline/docs/todo-plan.md`

The next practical step is no longer to define the system itself. The next practical step is to use the system to generate real project documents under `specs/`.

Recommended execution order:

1. `/plan-docs`
2. `/generate-ref`
3. `/generate-global`
4. `/plan-domains`
5. `/generate-domain`
6. `/generate-tests`
7. `/generate-acceptance`


