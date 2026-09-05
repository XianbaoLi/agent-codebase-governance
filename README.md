# Agent Codebase Governance

面向 Codex / AI Agent 长期开发场景的**项目演化治理系统**。

它不负责教 Agent 如何“更好地写代码”，也不把各种软件工程最佳实践组合成一个 Super Skill。它只关心一件事：**当项目发生长期影响的变化时，这次变化是否应该发生、是否遵守既有约束、变化之后项目是否重新收敛。**

一句话边界：

> Governance controls how the project evolves, not how the agent codes.

## 核心闭环

```text
Proposed Change
      |
      v
   SHOULD ?        <- 这次变化是否应该发生，边界是什么
      |
      v
   Agent executes  <- HOW 默认交给 Agent / 专用工具
      |
      v
   DID IT ?        <- 实际变化是否符合约束
      |
      v
    Audit
      |
      +--> aligned --------> Closure
      |
      +--> drifted --------> Remediation / Delete ----> Closure
```

治理系统重点负责 `SHOULD` 和 `DID IT`。中间的 `HOW` 不是本项目的产品边界。

## 治理原则

1. **Justify before structural change**：引入长期结构、状态、契约或抽象前，先证明为什么需要。
2. **One authority for each fact**：会影响 Agent 后续决策的长期事实，同一时间只能有明确权威来源。
3. **Audit for governance drift**：审计的是项目是否偏离已确认的决策和边界，不是泛化代码质量检查。
4. **Prove before remediation**：修正或删除之前必须建立治理证据，不能因为“看起来复杂”就动手。
5. **Closure over ceremony**：代码改完不代表治理结束，必须确认实现、契约、active docs 和必要验证重新一致。

元原则：**Governance must not become another source of entropy。**

## 系统组成

| 组件 | 回答的问题 | 角色 |
| --- | --- | --- |
| `governance-trigger.md` | 这次任务是否需要进入治理系统 | Ambient Admission Gate |
| `project-governance` | 已进入治理后，这是 E1–E5 哪类事件、下一步由谁处理、最终是否收敛 | Router / Orchestrator / Closure |
| `architecture-governance` | 这个长期变化该不该发生，允许到什么边界 | SHOULD |
| `govern-project-docs` | 当前哪些长期知识仍然有效，Agent 应该相信什么 | Context / Authority |
| `complexity-audit` | 项目是否出现治理漂移、失效决策残留或上下文污染 | DID IT / Audit |
| `governance-remediation` | 已确认的治理偏离应修正、退役、删除还是保留 | Remediation |

这些组件都服务于同一个“项目演化闭环”，不是独立最佳实践集合。

## 明确不属于本项目

- 通用 Clean Code / code review；
- 通用 TDD、测试生成或安全扫描；
- 自动选择设计模式；
- 因为“代码很多”就做通用简化；
- 因为“抽象复杂”就做通用重构；
- 最小代码哲学、YAGNI 执行策略等实现层约束。

这些能力可以由 Agent 或独立工具完成，但不作为本项目的组成部分。

## 真实触发入口

`governance-trigger.md` 是应暴露给普通 Agent 的最小常驻 admission gate。它只做二分类：

```text
NO_GOVERNANCE
GOVERNANCE_REQUIRED
```

- 普通 helper、命名、局部算法、一般测试/重构直接走 `NO_GOVERNANCE`，不加载治理 Skills；
- 命中长期架构、state、contract、authority、compatibility、context drift 等信号后输出 `GOVERNANCE_REQUIRED`；
- 只有此时才加载 `project-governance`；
- `project-governance` 不再重复 YES/NO 判断，只负责 E1–E5 分类、路由、跨阶段协调和 Closure。

因此职责是“Trigger 决定进不进，Router 决定进来后去哪”。

## 事件路由

| 事件 | 判断要点 | 默认路由 |
| --- | --- | --- |
| `E1 Structural Change` | 新增子系统、长期 state ownership、持久状态、公共契约、schema/protocol、插件机制、兼容机制或跨模块抽象 | `architecture-governance` |
| `E2 Knowledge Change` | 当前有效事实或长期约束发生变化 | `govern-project-docs` |
| `E3 Governance Audit` | code/docs/ADR drift、失效决策残留、obsolete artifact、上下文污染 | `complexity-audit` |
| `E4 Remediation Candidate` | 已有证据指出某个治理偏离或失效 artifact，需要验证并修正/退役/删除 | `governance-remediation` |
| `E5 Governance Drift` | Code != Documentation、Code != ADR、Active Doc A != Active Doc B | 先确定 authority，再审计/修正 |

普通 helper、局部算法替换、变量重命名、常规测试补充等没有长期治理影响的任务应返回 `NO_GOVERNANCE`。

## 审计与删除的边界

审计保留，但只做**治理审计**：

- 当前实现是否违反已确认架构边界；
- ADR、active docs 与代码是否表达不同版本的系统；
- 已 superseded / abandoned 的决策是否仍留下会误导 Agent 的 artifact；
- 失败实验、旧兼容层、旧状态 owner 是否已经失去当前决策依据。

删除也保留，但只删除**有治理证据证明应退役的 artifact**。删除前必须检查 consumer、contract、运行时使用、历史原因和回滚影响。

## 典型工作流

所有治理工作流先经过 `governance-trigger -> GOVERNANCE_REQUIRED -> project-governance`。

1. **新增变化**：`E1 -> architecture-governance -> Agent execution -> complexity-audit/closure`。
2. **知识变化**：`E2/E5 -> govern-project-docs` 确定 authority，并隔离 superseded context。
3. **发现偏离**：`E3 -> complexity-audit -> Governance Finding`。
4. **修复/退役**：已确认 Finding -> `governance-remediation` -> 必要时产生 `Governance Change` -> `govern-project-docs` -> Closure。

## 与其他工具的关系

Ponytail、simplify-codebase 等可以独立存在，但**不是本项目的组成部分，也不是治理生命周期中的必经阶段**。

- Ponytail 关注实现阶段如何避免 over-engineering；
- simplify-codebase 关注已有代码复杂度如何化简；
- 本项目关注一次长期项目变化从决策、执行、审计到退役是否形成闭环。

## 第一版边界

覆盖治理对象：`Code`、`Architecture`、`Concept / Abstraction`、`State`、`Contract`、`Compatibility`、`Documentation`、`Agent Context`。

`Governance Finding`、`Governance Change` 和 lifecycle `trace` 都是 ephemeral artifact，不建立长期 findings / workflow database。治理系统自身不新建复杂 workflow engine、长期 Registry 或额外事实数据库，除非真实案例证明必要。
