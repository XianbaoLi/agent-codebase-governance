---
name: project-governance
version: 0.3.0
description: 在 governance-trigger 已确认 GOVERNANCE_REQUIRED 后，将治理事件分类为 E1–E5，路由 specialist，协调跨阶段治理并完成 Closure。
---

# Project Governance

这是项目演化治理系统的 **Router、Orchestrator 和 Closure coordinator**。

它不是 ambient Trigger，也不负责重新判断普通工程任务是否应该进入治理。入口契约是：

```text
governance-trigger -> GOVERNANCE_REQUIRED -> project-governance
```

如果 admission 仍未完成，应先回到 `governance-trigger.md`，而不是在本 Skill 内做第二次 YES/NO 判定。

它不教 Agent 如何实现代码，也不把 Ponytail、simplify-codebase、TDD、通用 code review 等工具变成治理流程的一部分。

## Routing

进入本 Skill 后，只做治理事件分类与阶段路由：

| 事件 | 判断要点 | 默认路由 |
| --- | --- | --- |
| `E1 Structural Change` | 长期结构、state ownership、持久状态、公共契约或边界发生变化 | `architecture-governance` |
| `E2 Knowledge Change` | active/canonical knowledge 或长期约束发生变化 | `govern-project-docs` |
| `E3 Governance Audit` | 需要检查项目是否偏离当前有效决策 | `complexity-audit` |
| `E4 Remediation Candidate` | 已有 Governance Finding / authority conflict，需要修正、退役或删除 | `governance-remediation` |
| `E5 Governance Drift` | Code != Documentation、Code != ADR、Active Doc A != Active Doc B | 先路由 authority resolution，再进入 Audit / Remediation |

Router 不直接替代 specialist 的语义判断。例如，E1 只负责送到 `architecture-governance`，不在这里重复做 SHOULD。

## SHOULD

对于 `E1`，由 `architecture-governance` 给出是否允许变化以及 constraints。

Governance 只把 constraints 交给执行 Agent，不规定 `HOW`。例如可以约束“不改变公共 API”“不得新增长期 state owner”，但不应进一步指定设计模式或代码组织，除非那本身就是已有 authority。

## Orchestration

单阶段请求通常只路由一个 specialist；完整治理变化则由本 Skill 协调阶段顺序：

```text
ROUTING
  -> SHOULD (when required)
  -> Agent executes HOW
  -> DID_IT
  -> REMEDIATION (when findings require it)
  -> KNOWLEDGE_SYNC (when long-term knowledge changed)
  -> CLOSURE
```

阶段不是固定 ceremony。不适用的阶段应跳过，不为了形成漂亮 trace 强制经过所有节点。

## DID IT

变化执行后，需要判断实际结果是否满足：

- 原决策与 constraints；
- 当前 contract；
- active/canonical documentation；
- Agent context authority。

语义审计路由给 `complexity-audit`；确定性测试/CI 可作为 verification evidence。

## Remediation

`Governance Finding` 默认只是 hypothesis。只有在需要让项目重新一致时才路由 `governance-remediation`。

Remediation 的合法结果：`FIX` / `RETIRE` / `REMOVE` / `RETAIN` / `UNRESOLVED`。

不允许因为一般代码复杂度问题自动进入删除流程。

## Closure

| 检查项 | 取值 |
| --- | --- |
| implementation consistent? | `yes` / `no` / `na` |
| contract consistent? | `yes` / `no` / `na` |
| active documentation consistent? | `yes` / `no` / `na` |
| superseded context isolated? | `yes` / `no` / `na` |
| required verification passed? | `yes` / `no` / `na` |

只有不存在未处理治理后果，才输出 `CLOSED`。

## 输出

```text
event: E1 | E2 | E3 | E4 | E5
phase: ROUTING | SHOULD | DID_IT | REMEDIATION | CLOSURE
assigned_to: <skill | agent | project-governance>
constraints: <0..N>
findings: <0..N ephemeral Governance Finding>
changes: <0..N ephemeral Governance Change>
trace: <0..N ephemeral lifecycle phase records>
closure: CLOSED | OPEN(...)
```

`NO_GOVERNANCE` 属于 ambient admission gate 的输出，不属于本 Skill 的 event。
