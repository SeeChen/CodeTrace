# CodeTrace

> 输入一份 PRD,输出架构、代码、测试与验收证据 —— 然后由一个自收敛循环持续加固,
> 直到跨过可度量的质量门槛。

**CodeTrace** 是一套 AI-first 交付流水线:位于 `.claude/` 下、纳入版本管理的可复用系统,
由 agents、skills、commands、rules 与 memory 组成。为了证明流水线真的能跑,它自己生成了
载荷 —— `src/` 下一个轻量、local-first、零依赖的 Python 函数 tracing 库。

**流水线才是产物,库只是证据。**

## 流程

```
PRD → 意图 → 架构 → 构建契约 → 任务切片 → 编码 → 验证 → 验收 → ⟳ 收敛
```

每个阶段都是三个文件:**命令**(入口)、**技能**(怎么做)、**代理**(谁负责),
外加不可妥协的 rules 与可续跑的 memory。

```bash
/seechen --run      # 从 docs/PRD.md 跑完整条流水线
/converge --run     # 对已变绿的 milestone 做加固直到收敛
```

## 实测运行

流水线端到端生成了这个库,收敛循环再用三轮把它加固:

**77/77 测试 · 99% 行覆盖率 · 77.3% 变异分 · ruff 净 · mypy 0 错 ·
复杂度 ≤ B → 已收敛**

循环揪出了绿灯掩盖的问题 —— 一个类型安全漏洞、一个复杂度热点,以及一场
**覆盖率幻觉**:99% 的行被执行,但只有 **64.5%** 的逻辑真正被断言。加固把变异分提到
77.3%,越过闸门后循环自行停止。

→ [案例报告](docs/Case-Study.md)(英文,完整叙事) · [审计证据](specs/audit/)(逐轮报告)

## 文档

| 文档 | 内容 |
| --- | --- |
| [PRD](docs/PRD.md) | 产品事实来源 |
| [Workflow](docs/Workflow.md) | 逐阶段定义 |
| [Pipeline Components](docs/Pipeline-Components.md) | **每个 agent 与 skill 的详解** —— 输入、输出、边界 |
| [案例报告](docs/Case-Study.md) | 端到端运行的逐轮记录 |
| [收敛循环](.claude/docs/Convergence-Loop.md) | rubric、闸门、停止条件、驱动器 |
| [图示](docs/diagrams/) | PlantUML 流程图与时序图 |

## 结构

```
CodeTrace/
├── .claude/          # 流水线本体:agents、skills、commands、rules、memory、docs
├── docs/             # PRD、工作流、组件详解、案例报告、图示
├── specs/            # 生成产物:intent、architecture、build、acceptance、audit
├── src/ tests/       # 生成的库与测试套件
└── CLAUDE.md         # 仓库入口
```

## 贡献

遵循 [`.claude/rules/`](.claude/rules/) 中的规则:使用与任务匹配的分支、Conventional
Commits、可复用约束文件用英文,并在每个阶段完成后更新
`.claude/memory/pipeline-state.md`。

## 许可证

MIT —— 详见 [LICENSE](LICENSE)。
