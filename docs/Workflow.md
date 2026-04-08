# AI 驱动开发全流程规范（V1.0）

本规范定义从 PRD 到交付的 AI Agent 驱动开发流程，明确各阶段目标、核心产出、Agent 职责和协作规则。适用于 CodeTrace 等 Python 项目。

## 一、顶层工作流（Full Workflow）
目标：建立从需求到验收的端到端流程框架，确保每个阶段都有明确交付物和责任人。

**PRD** → **Global Blueprint（全局蓝图）** → **Domain Spec（领域规格）** → **Coding** → **Testing** → **验收**

---

## 二、Phase 0: 知识底座（Memory）
目标：建立项目基础知识，收集核心术语、标准库边界与性能基准。

### 1. 核心产出
* **prd_keywords.md**：核心术语提取（Instrumentation, Artifacts）。
* **std_lib_research.md**：sys.settrace/inspect 等标准库边界调研。
* **perf_baseline.md**：15% 性能预算参考基准。

### 2. Agent 职能定义
* **Research Agent（调研员）**
  * 职能：分析 PRD，提取关键概念与技术边界。
  * Skill：标准库调研、性能基准建立、术语定义。

---

## 三、Phase 1: 全局骨架（Skeleton）
目标：消除技术歧义，建立跨域契约，形成可落地的系统全局方案。

### 1. 核心产出
| 文档名称 | 核心内容 |
| :--- | :--- |
| **app-business.md** | 业务全景：装饰器触发 -> 捕获 -> 持久化流转。 |
| **SA.md** | 全局架构：Hook-Processor-Sink 拓扑设计。 |
| **project-structure.md** | 工程规范：Google Style & 零依赖结构定义。 |
| **modules.md** | 模块/域定义：明确各 Domain 边界、职责与依赖关系。 |
| **constraint.md** | 核心红线：故障隔离与 Python 3.10+ 约束。 |
| **API.md** | 全局契约：@trace 装饰器入参与 Hook 签名。 |

### 2. Agent 职能定义
* **Architect Agent（架构师）**
  * 职能：解析 PRD、建模业务领域、确定系统边界与模块划分。
  * Skill：行业方案调研、领域依赖图绘制、分布式方案决策。
* **Security & Logic Agent（合规官）**
  * 职能：制定 `constraint.md`，识别风险与合规点。
  * Skill：安全策略、全局异常处理、事务与幂等设计。
* **Liaison Agent（契约员）**
  * 职能：协调跨域接口定义、保证 API 一致性。
  * Skill：生成 API 签名、接口兼容性校验。

---

## 四、Phase 2: 核心域展开（Domain Expansion）
目标：将全局设计拆解为可实现的领域模块，并形成领域级实施方案。

### 1. 核心产出
* **Domain SA.md**：领域架构，如递归追踪与堆栈管理逻辑。
* **layer-core.md**：核心规格，如 TraceContext 与 FrameInspector 规格。
* **layer-dao.md**：数据访问层，如 CSV 分片存储协议与索引设计。
* **layer-biz.md**：业务逻辑层，如异步写入缓冲区管理规约。
* **layer-facade.md**：接口层，如结构化报告导出接口（Text/JSON/CSV）。

### 2. Agent 职能定义
* **Domain Expert Agent（领域专家）**
  * 职能：深耕业务规则，细化业务状态机和边界逻辑。
  * Skill：编写复杂业务流程、异常处理、业务一致性方案。
* **Framework Agent（框架助手）**
  * 职能：映射 Python 体系结构，定义模块与依赖。
  * Skill：生成包结构模板、管理模块依赖、确保部署可执行。
* **QA Agent（测试分析师）**
  * 职能：设计测试方案，生成测试文档。
  * Skill：制定 Mock 策略、覆盖异常路径、设计性能与稳定性断言。

---

## 五、Phase 2.5: 测试策略（TDD 锚点）
目标：嵌入测试驱动开发，确保质量与性能。

### 1. 核心产出
* **engine_perf.md**：嵌套调用开销压力测试场景。
* **idempotency.md**：追踪 ID 唯一性与多线程验证。

### 2. Agent 职能定义
* **Test Designer Agent（测试设计师）**
  * 职能：制定 TDD 计划与测试用例。
  * Skill：性能测试设计、并发验证、边界条件覆盖。

---

## 六、Phase 3: 编码与验证（Coding & Testing）
目标：实现代码交付并完成验证，形成开发-测试闭环。

### 1. 核心产出
* 代码实现：符合规格的可运行模块。
* 测试报告：单元测试、集成测试、回归测试结果与缺陷清单。
* 修复反馈：自动化测试结果反馈、缺陷修复与验证记录。

### 2. Agent 职能定义
* **Coding Agent（程序员）**
  * 职能：根据 Spec 与 API 实现代码。
  * Skill：熟练使用 Python、严格遵循约束、编写可维护代码。
* **Refactor Agent（代码审查）**
  * 职能：评审代码质量与架构一致性。
  * Skill：静态分析、循环依赖识别、性能与可维护性优化。
* **Test Runner Agent（自动化测试）**
  * 职能：执行测试用例并反馈结果。
  * Skill：运行 Pytest、分析失败原因、推动修复闭环。

---

## 七、Phase 3.5: 验收标准（Final Criteria）
目标：定义最终验收门禁，确保交付质量。

### 1. 核心产出
* **criteria.md**：15% 损耗门禁与零依赖合规验收。

### 2. Agent 职能定义
* **Acceptance Agent（验收官）**
  * 职能：制定验收标准并验证交付物。
  * Skill：性能门禁检查、合规验证、质量评估。

---

## 八、关键协作逻辑（Collaboration Logic）
1. **分权而治**：Global Agent 负责全局契约与规范，Domain Agent 负责领域落地与实现。
2. **契约先行**：未锁定 Global API 前，不得进入 Coding 阶段。
3. **反馈闭环**：Domain Agent 若发现 Global SA 无法落地，必须申请修改全局设计，避免擅自变更。
4. **文档常绿**：各阶段交付物应保持可迭代，变更需同步更新全局与领域文档。 

---

## 九、持续优化建议
* 以 PRD 为核心，保持需求与设计同步。
* 每个阶段产出应量化可验收（文档、契约、测试用例）。
* 定期复盘 Agent 协作过程，发现并补齐流程缺口。

---

## 十、产出结构示例（基于 CodeTrace 项目）
以下为应用本规范后的实际产出目录结构示例（以 CodeTrace 项目为例）。结构可根据项目特性调整，但核心层次保持一致。

```
specs/
├── ref/                                # Phase 0: 知识底座 (Memory)
│   ├── prd_keywords.md                 # 核心术语提取 (Instrumentation, Artifacts)
│   ├── std_lib_research.md             # sys.settrace/inspect 等标准库边界调研
│   └── perf_baseline.md                # 15% 性能预算参考基准
├── global/                             # Phase 1: 全局骨架 (Skeleton)
│   ├── app-business.md                 # 业务全景: 装饰器触发 -> 捕获 -> 持久化流转
│   ├── SA.md                           # 全局架构: Hook-Processor-Sink 拓扑设计
│   ├── project-structure.md            # 工程规范: Google Style & 零依赖结构定义
│   ├── modules.md                      # 模块/域定义: 明确各 Domain 边界、职责与依赖关系
│   ├── constraint.md                   # 核心红线: 故障隔离与 Python 3.10+ 约束
│   └── API.md                          # 全局契约: @trace 装饰器入参与 Hook 签名
├── domains/                            # Phase 2: 核心域展开 (Domain Expansion)
│   ├── tracing_engine/                 # 核心引擎域 (根据 modules.md 定义展开)
│   │   ├── SA.md                       # 递归追踪与堆栈管理逻辑
│   │   └── layer-core.md               # TraceContext 与 FrameInspector 规格
│   ├── persistence/                    # 持久化域 (手搓静态存储)
│   │   ├── layer-dao.md                # CSV 分片存储协议与索引设计
│   │   └── layer-biz.md                # 异步写入缓冲区管理规约
│   └── comparison/                     # 比对与报告域
│       ├── layer-core.md               # Baseline vs Candidate 差异计算算法
│       └── layer-facade.md             # 结构化报告导出接口 (Text/JSON/CSV)
├── testing/                            # Phase 2.5: 测试策略 (TDD 锚点)
│   ├── engine_perf.md                  # 嵌套调用开销压力测试场景
│   └── idempotency.md                  # 追踪 ID 唯一性与多线程验证
├── acceptance/                         # Phase 3.5: 验收标准 (Final Criteria)
│   └── criteria.md                     # 15% 损耗门禁与零依赖合规验收
└── summary.md                          # 汇总索引与文档生成状态跟踪
```

### 结构说明
- **ref/**: Phase 0 的产出，基础知识收集。
- **global/**: Phase 1 的核心产出，全局设计。
- **domains/**: Phase 2 的模块化展开。
- **testing/**: Phase 2.5 的测试策略。
- **acceptance/**: Phase 3.5 的验收标准。
- **summary.md**: 文档索引与状态跟踪。

此结构体现了分层设计：从全局到领域，从设计到测试，确保每个阶段产出可追溯、可验证。

---

### 说明
本规范适用于 AI Agent 协同开发场景，可根据团队实际技术栈与组织形态调整。产出结构应保持层次清晰，文件名与文件夹名可根据项目语境自定义。