---
name: project-governance
version: 0.2.0
description: 识别并路由具有长期项目演化影响的治理事件，协调 SHOULD、DID IT、Remediation 与 Closure；普通工程改动返回 NO_GOVERNANCE。
---

# Project Governance

这是项目演化治理系统的 Trigger、Router 和 Closure 协调器。

它不教 Agent 如何实现代码，也不把 Ponytail、simplify-codebase、TDD、通用 code review 等工具变成治理流程的一部分。

## Trigger

`governance-trigger.md` 是面向普通 Agent 的轻量常驻触发面。本 Skill 不应对每个普通编码请求无条件加载；只有触发面命中长期项目演化信号后才进入这里。

进入后，先判断任务是否会改变长期项目状态。普通 helper、局部算法替换、变量重命名、常规测试补充、无长期影响的局部重构等返回 `NO_GOVERNANCE`。

需要治理的典型信号：

- 新增或改变长期架构边界；
- 新增 state ownership、持久状态、公共 contract、schema/protocol、compatibility；
- 改变 Agent 后续必须相信的长期事实；
- 发现 Code / ADR / docs / contract 不一致；
- 已 superseded / abandoned 的决策可能仍留下 artifact 或 context；
- 一次治理变化执行后需要确认是否闭合。

## 事件

| 事件 | 判断要点 | 路由 |
| --- | --- | --- |
| `E1 Structural Change` | 长期结构、状态、契约或边界发生变化 | `architecture-governance` |
| `E2 Knowledge Change` | active/canonical knowledge 发生变化 | `govern-project-docs` |
| `E3 Governance Audit` | 需要检查项目是否偏离当前有效决策 | `complexity-audit` |
| `E4 Remediation Candidate` | 已有治理 Finding / authority conflict，需要修正、退役或删除 | `governance-remediation` |
| `E5 Governance Drift` | Code != Documentation、Code != ADR、Active Doc A != Active Doc B | 先确认 authority，再进入 Audit / Remediation |

## SHOULD

对于 `E1`，由 `architecture-governance` 给出是否允许变化以及 constraints。

Governance 只把 constraints 交给执行 Agent，不规定 `HOW`。例如可以约束“不改变公共 API”“不得新增长期 state owner”，但不应进一步指定设计模式或代码组织，除非那本身就是已有 authority。

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
event: E1 | E2 | E3 | E4 | E5 | NO_GOVERNANCE
phase: TRIGGER | SHOULD | DID_IT | REMEDIATION | CLOSURE
assigned_to: <skill | agent | none>
constraints: <0..N>
findings: <0..N ephemeral Governance Finding>
changes: <0..N ephemeral Governance Change>
trace: <0..N ephemeral lifecycle phase records>
closure: CLOSED | OPEN(...)
```
