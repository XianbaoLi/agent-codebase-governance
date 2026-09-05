# Governance Model

## 定位

本系统治理的对象不是“代码质量”，而是**项目演化（project evolution）**。

它回答两个核心问题：

1. `SHOULD`：一个具有长期影响的变化是否应该发生？如果允许，它必须满足哪些项目边界？
2. `DID IT`：变化执行后，项目是否仍与有效决策、契约和权威上下文一致？

实现阶段的 `HOW` 默认不属于本系统。Governance 不负责告诉 Agent 应使用哪种设计模式、如何写最少代码、如何做通用重构或如何组织测试。

## 核心闭环

```text
Ambient Trigger (admission only)
  -> Project Governance (routing/orchestration)
  -> Context / Authority
  -> SHOULD (decision + constraints)
  -> Agent executes HOW
  -> DID IT (audit against decision)
  -> aligned: Closure
  -> drifted: Remediation / Retirement / Delete
  -> Closure
```

治理是例外路径。`governance-trigger.md` 先输出 `NO_GOVERNANCE` 或 `GOVERNANCE_REQUIRED`；只有后者进入 `project-governance` 做 E1–E5 分类。没有长期项目影响的普通工程任务不会加载治理 Router 或 specialist Skills。

## 入口与五个治理能力

`governance-trigger.md` 是平台适配/上下文层面的轻量入口，只回答“进不进入治理系统”，不属于五个 specialist/orchestration 能力之一。

| 能力 | 只回答 |
| --- | --- |
| `project-governance` | 已确认需要治理后，这是哪类事件、应该路由到哪里、跨阶段如何协调、最终是否闭合？ |
| `architecture-governance` | 这个长期项目变化该不该发生，边界是什么？ |
| `govern-project-docs` | 当前哪些项目知识仍具有 authority，Agent 应该相信什么？ |
| `complexity-audit` | 当前项目是否存在与有效决策不一致的治理偏离或失效残留？ |
| `governance-remediation` | 一个有治理依据的偏离/失效 artifact 应修正、退役、删除还是保留？ |

禁止把这些能力扩展成通用软件工程 Super Skill。

## 治理对象

第一版重点覆盖：

- `Code`
- `Architecture`
- `Concept / Abstraction`
- `State`
- `Contract`
- `Compatibility`
- `Documentation`
- `Agent Context`

对象本身不是问题。只有当它与当前有效项目决策之间出现需要治理的关系时，才进入本系统。

## Governance Finding

审计输出的是可证伪假设，不是代码 smell 清单。推荐类型：

- `decision-drift`
- `authority-conflict`
- `obsolete-artifact`
- `superseded-context-leak`
- `orphaned-responsibility`
- `contract-drift`
- `unknown-governance-risk`

证据不足时必须保留 `unknown`，不能为了分类强行推断。

## Authority 与 Context

发现 `Code != Documentation`、`Code != ADR`、`Active Doc A != Active Doc B` 时，不能默认任何一方自动正确。

先确认当前 authority：

- active + canonical 表示当前权威；
- superseded / historical 内容可以保留，但默认不能污染当前 Agent context；
- ADR 有生命周期；
- `AGENTS.md` 更偏向 context router，而不是百科全书；
- 一个长期事实尽量只有一个 canonical source；
- 确定性检查交给脚本，语义冲突交给 Agent；
- 无法确定 authority 时输出 `UNRESOLVED`。

## Audit

Audit 的对象是**治理一致性**，而不是泛化代码质量。

属于本系统：

- 实现是否违反有效架构决策；
- Code / ADR / active docs 是否发生语义漂移；
- 已失效决策是否仍留下可执行或可检索 artifact；
- 旧 context 是否仍可能影响 Agent 当前决策；
- 某个长期 responsibility 是否已经没有有效 owner 或决策依据。

不属于本系统：

- 函数是否写得优雅；
- 是否可以少写几十行代码；
- 通用 duplication / style / lint；
- 没有治理依据的“这个模块看起来复杂”。

## Remediation / Delete

删除是治理闭环的一部分，但删除理由必须来自治理证据，而不是复杂度偏好。

候选 artifact 只有在完成以下检查后才能删除：

1. 对应的长期决策是否已失效、被 supersede，或该 artifact 已被证明违反当前 authority；
2. 是否仍有真实 consumer；
3. 是否承担 contract、persistence、compatibility 或动态运行职责；
4. 删除是否会破坏当前有效架构边界；
5. 是否需要同步 active docs / ADR / Agent context。

合法结果：`FIX` / `RETIRE` / `REMOVE` / `RETAIN` / `UNRESOLVED`。

`RETAIN` 和 `UNRESOLVED` 都是成功的治理结果，不为了“完成清理”强行删除。

## Closure

治理流程不是“代码改完”就结束。Closure 检查：

1. implementation consistent?
2. contract consistent?
3. active documentation consistent?
4. superseded context isolated?
5. required verification passed?

不适用项允许 `N/A`。只有不存在未处理的治理后果，才可判定为 `CLOSED`。

## 与实现层工具的边界

Ponytail、simplify-codebase、TDD 工具、通用 refactoring / code review 工具都可以与 Agent 同时使用，但它们不是 Governance 的内部阶段。

Governance 可以输出 constraints，外部实现工具可以选择如何满足；Governance 最后只验证结果是否与项目有效决策一致。

## 设计约束

- Governance controls project evolution, not coding style.
- 治理是例外路径。
- 不复制外部最佳实践工具。
- 不为治理建立第二套项目事实数据库。
- Finding / Change 默认 ephemeral。
- 不建立复杂 workflow 状态机。
- 每新增一个治理机制，都要证明它解决的是“项目演化失控”，而不是一般软件工程问题。
