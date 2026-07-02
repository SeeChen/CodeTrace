# CodeTrace-AI

一个以 AI 为核心的仓库，用于演示一套**可复用的交付流水线**：由 agents、skills、commands、rules 与 memory 组成的系统，把一份 PRD 逐步转化为架构、构建契约、代码、测试与验收证据——并在验收之后继续用一个**自收敛的审计/加固循环**打磨，直到结果跨过可度量的质量门槛。

用来演示这套流水线的产品是 **CodeTrace**——一个轻量、local-first、零依赖的 Python 函数 tracing 框架（见 [docs/PRD.md](docs/PRD.md)）。本仓库真正的产物是流水线本身（位于 `.claude/`）；`src/` 与 `tests/` 由运行流水线自动生成。

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

### 收敛循环（验收后的加固）

milestone 变绿之后，**`/converge`** 会继续迭代——`audit -> score -> 停止判断 -> re-plan -> implement -> verify`——直到复合质量分达标才停下。它按业界 loop-engineering 原语来设计：

- **驱动器**：重复交给原生调度器（`/loop` 或 `ScheduleWakeup`）；`/converge --resume` 只跑一轮（幂等），跑完输出"是否再来一轮"的信号。
- **目标 / 评分**：70% 机器可判定闸门（测试、覆盖率、变异、lint、类型、复杂度）+ 30% 引证据的主观评审；循环不能仅凭自评收敛。
- **安全护栏**：回归护栏会回退任何让闸门变差的轮次；停止条件（收敛 / plateau / 预算）保证终止；真正模糊时升级给人类 checkpoint，而不是瞎猜。

详见 [.claude/docs/Convergence-Loop.md](.claude/docs/Convergence-Loop.md)。

## 实测结果

针对 `docs/PRD.md` 端到端跑通流水线，生成了 CodeTrace MVP，再由收敛循环加固至收敛：

| 轮次 | 复合分 | 变异分 | 复杂度 | 测试 | 这轮动作 |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.82 | 未测 | `_execute` D(21) | 43 | 修类型安全漏洞 |
| 2 | 0.97 | 64.5% | `_execute` A(5) | 46 | 重构 `_execute`；补 session 路径 |
| 3 | 0.97 | **77.3%** ✅ | A | 77 | +31 断言硬化测试 |

**最终闸门（全部实测）：** 测试 77/77 · 行覆盖率 99% · **变异 77.3%（≥70%）** · ruff 净 · mypy 0 错 · 复杂度无低于 B 的块。

循环揪出了绿灯掩盖的东西——一个类型漏洞、一个复杂度热点，以及一场**覆盖率幻觉**（99% 的行被执行，但只有 64.5% 的逻辑真正被断言）。变异测试在原生 Windows 上跑不了时它选择升级问人（改用 WSL 测量），并且在达标处（77.3%）就停手，而不是无限打磨。完整证据：[specs/audit/](specs/audit/) 与 [convergence-summary.md](specs/audit/convergence-summary.md)。

## 概述

仓库强调：

- **PRD 驱动**：`docs/PRD.md` 是唯一的产品级事实来源；所有下游产物都从上游派生
- **规范驱动**：在编码前先冻结架构与构建契约，使实现遵循 task slices 而非宽泛的重新解读
- **自收敛**：验收后的审计/加固循环用机器可判定闸门驱动质量,带回归护栏与保证终止
- **可复用 AI 约束**：agents、skills、commands、rules、memory 都纳入版本管理，统一放在 `.claude/`
- **可恢复工作流**：阶段状态与循环状态保存在 `.claude/memory/`，使一次运行可以从上次完成的步骤继续

## 文档

- [产品需求文档 (PRD)](docs/PRD.md)
- [AI 开发工作流](docs/Workflow.md)
- [PRD-Pipeline 调用接口](.claude/docs/PRD-Pipeline-Interface.md)
- [收敛循环](.claude/docs/Convergence-Loop.md) —— rubric、闸门、停止条件、驱动器
- [收敛总结](specs/audit/convergence-summary.md) —— 逐轮的实测过程
- [CLAUDE.md](CLAUDE.md) —— 仓库入口与流水线总览

## 开始使用

本仓库面向在 Claude Code 中进行的 AI 辅助开发：先建立文档体系，再从冻结的规格生成代码。

### 先决条件

- Claude Code（或能读取仓库文件并遵循结构化约束的 AI 工具）
- 作为主事实来源的项目 PRD

### 使用方法

1. 先阅读 [PRD](docs/PRD.md)、[Workflow](docs/Workflow.md) 与 [CLAUDE.md](CLAUDE.md)。
2. 运行 `/seechen --run` 跑完整流程，或运行单个阶段如 `/seechen --sa`。
3. 运行 `/converge --run` 用收敛循环加固一个已变绿的 milestone。
4. 查看 `.claude/` 下的可复用资产：
   - `agents/`：各阶段角色归属（含 audit-agent）
   - `skills/`：各阶段执行指南（含 audit-quality）
   - `commands/`：斜杠命令入口（`/seechen`、`/converge` 及各阶段）
   - `rules/`：仓库级约束
   - `memory/`：持久的流水线与循环状态
   - `docs/`：流水线调用接口与收敛循环参考
5. 随每个阶段完成，查看 `specs/` 下生成的产物（含 `specs/audit/` 的循环证据）。

## 项目结构

```
CodeTrace-AI/
├── CLAUDE.md                  # 仓库入口与流水线总览
├── .claude/
│   ├── agents/                # 各阶段角色归属（含 audit-agent）
│   ├── commands/              # 斜杠命令入口（/seechen、/converge、各阶段）
│   ├── skills/                # 各阶段执行指南（含 audit-quality）
│   ├── rules/                 # 仓库约束
│   ├── memory/                # 持久的流水线与循环状态
│   └── docs/                  # 流水线调用接口 + 收敛循环参考
├── docs/
│   ├── PRD.md                 # 产品需求文档
│   └── Workflow.md            # 逐阶段工作流定义
├── src/、tests/                # 生成的实现与测试
├── specs/                     # 流水线生成的产物
│   ├── intent/ architecture/ build/ acceptance/
│   └── audit/                 # 收敛循环的逐轮报告与总结
├── LICENSE
├── README.md
└── README-zh.md
```

## 当前范围

仓库提供了覆盖完整交付流程（intent、architecture、build spec、task slices、coding、verification、acceptance）的编排系统，外加验收后的收敛循环。它已被端到端演示：针对 `docs/PRD.md` 运行流水线生成了 `src/`/`tests/` 下的 CodeTrace MVP，收敛循环再把它加固到一个实测、已收敛的状态（见[实测结果](#实测结果)）。针对变更后的 PRD 重新运行，会从冻结的规格重新生成产物。

## 贡献

欢迎围绕 AI-first workflow 提交改进。请遵循：

1. 遵循 `.claude/rules/` 中的规则。
2. 可复用 system-constraint 文件默认使用英文，除非有明确例外说明。
3. 使用与任务语义匹配的 branch，不要复用无关 branch。
4. 每个步骤完成后，同步更新 `.claude/memory/pipeline-state.md`（循环运行时同步 `convergence-state.md`）。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- 受模块化 AI 辅助开发实践与 loop-engineering 模式启发
- 用于展示 PRD 驱动的流水线如何把项目从需求带到经过验证、加固的代码
