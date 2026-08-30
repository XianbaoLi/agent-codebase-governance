---
name: project-governance
version: 0.1.0
description: 识别并路由具有长期复杂度影响的治理事件，协调后续治理影响，并检查 Closure；普通工程改动返回 NO_GOVERNANCE，不亲自分析、删除或决定权威。
---

# Project Governance

这是治理系统的路由器和协调器，不是分析器。它分类治理事件、分派专业能力、传递 ephemeral artifact、检查治理影响是否收敛。

它不亲自进行架构分析、代码删除、consumer analysis 或文档权威判断。

## 分类事件

先判断这是不是普通工程任务。如果只是 helper、局部重构、测试补充、变量重命名、内部算法替换，或没有长期治理影响，返回 `NO_GOVERNANCE`。

| 事件 | 判断要点 | 路由 |
| --- | --- | --- |
| `E1 Structural Change` | 新增子系统、长期 state ownership、持久状态、公共契约、schema/protocol、插件机制、兼容机制或跨模块抽象 | `architecture-governance` |
| `E2 Knowledge Change` | 当前有效事实或长期约束发生变化；继续相信旧文档会让 Agent 做错决策 | `govern-project-docs` |
| `E3 Health Check` | 技术债、重复设计、架构腐化、code/docs drift、治理审计 | `complexity-audit` |
| `E4 Simplification Candidate` | 用户已指出明确对象，如某个 Manager、adapter、重复状态 | `simplify-codebase` |
| `E5 Governance Drift` | 本应一致的事实不一致，如 Code != Documentation、Code != ADR、Active Doc A != Active Doc B | `govern-project-docs`，先确定 authority |

`E4` 不再经过 `complexity-audit`，但必须把用户的判断转换为假设，而不是既定结论。

## 路由规则

`E5` 发现漂移时，不能默认“文档旧了”。也可能是代码违反了仍然有效的架构约束。必须先确定 authority；如果无法判断，输出 `UNRESOLVED`，不要自行折中。

## 协调

接收并传递 `Governance Finding` 和 `Governance Change`：

- 收到 `Governance Finding`：如果用户要求验证具体候选，路由到 `simplify-codebase`；否则只在一次协同中保持为假设。
- 收到 `Governance Change`：路由到 `govern-project-docs`，由它同步权威知识与 Agent 当前上下文。

不要把 Finding 或 Change 持久化成 registry。

## 检查 Closure

| 检查项 | 取值 |
| --- | --- |
| implementation consistent? | `yes` / `no` / `na` |
| contract consistent? | `yes` / `no` / `na` |
| active documentation consistent? | `yes` / `no` / `na` |
| required verification passed? | `yes` / `no` / `na` |

只有不存在未处理的治理后果，才输出 `CLOSED`。否则输出仍未收敛的原因和下一条路由。

## 输出

```text
event: E1 | E2 | E3 | E4 | E5 | NO_GOVERNANCE
assigned_to: <skill>
findings: <0..N ephemeral Governance Finding>
changes: <0..N ephemeral Governance Change>
closure: CLOSED | OPEN(...)
```

