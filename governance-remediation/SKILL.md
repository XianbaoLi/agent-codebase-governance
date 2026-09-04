---
name: governance-remediation
version: 0.1.0
description: 对已有治理证据确认的偏离或失效 artifact 做深度验证，并决定 FIX、RETIRE、REMOVE、RETAIN 或 UNRESOLVED；不做通用代码简化。
---

# Governance Remediation

这个 Skill 回答：**一个已经进入治理范围的偏离或失效 artifact，应该怎样让项目重新与当前 authority 一致？**

它不是 simplify-codebase，也不是通用重构器。没有 `Governance Finding`、明确 authority conflict 或用户指定的治理假设时，不应自行寻找“可删代码”。

## 输入

至少需要：

```text
scope: <对象>
claim: <待验证治理假设>
evidence: <已有证据>
authority: <当前有效决策/契约/文档；未知则标记 unknown>
```

用户说“这个 Manager 应该没用了”只能作为 hypothesis，不能直接作为删除依据。

## 深度验证

在产生破坏性修改前检查：

1. `decision`：对象对应的长期决策是否仍有效？是否已 superseded / abandoned？
2. `consumer`：是否仍有静态、动态或外部 consumer？
3. `contract`：是否承担 API、schema、protocol、compatibility 等职责？
4. `state`：是否拥有 persistence、migration 或 runtime state？
5. `context`：删除/退役后是否还有文档或 Agent context 会继续引用旧事实？
6. `blast radius`：误判会影响什么，是否可回滚？

证据不足时输出 `UNRESOLVED`，不能为了完成任务强行删除。

## 决策

- `FIX`：artifact 仍应存在，但当前实现违反有效约束。
- `RETIRE`：artifact 不再属于 active system，但需要历史保留或迁移期。
- `REMOVE`：artifact 已失去有效决策依据且安全删除条件成立。
- `RETAIN`：证据证明它仍承担当前有效职责。
- `UNRESOLVED`：authority 或使用证据不足。

## 删除规则

只有 `REMOVE` 才允许删除。删除前必须明确记录：

```text
why_obsolete:
consumer_check:
contract_check:
state_check:
context_cleanup:
verification:
rollback:
```

不要因为“代码重复”“实现不漂亮”“可以更短”而进入 REMOVE。

## 输出 Governance Change

如果发生 `FIX` / `RETIRE` / `REMOVE` 且改变长期有效知识，输出：

```text
type:
scope:
change:
reason:
authority_impact:
verification:
```

交给 `govern-project-docs` 同步 active authority，再由 `project-governance` 做 Closure。

## 边界

- 不主动做 broad complexity survey；
- 不提供通用重构建议；
- 不复制 Ponytail、simplify-codebase 或 Clean Code 工具；
- 不建立 remediation registry；
- `RETAIN` / `UNRESOLVED` 都是合法完成状态。
