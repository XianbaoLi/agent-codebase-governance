# Integration Contract

第一版只用两个轻量跨 Skill 对象。它们都是 ephemeral artifact，不代表已确认的问题，也不进入长期 findings 数据库。

## Governance Finding

用途：把值得进一步验证的“假设”从广度发现传给深度验证。

| 字段 | 必需 | 含义 |
| --- | --- | --- |
| `type` | 是 | 复杂度类型之一，如 `duplicated-state`、`obsolete-contract` |
| `scope` | 是 | 涉及的符号、路径、模块或边界 |
| `claim` | 是 | 一句可证伪的假设，不能写成既定结论 |
| `evidence` | 是 | 已观察到的静态、目录、文档或历史线索 |
| `confidence` | 是 | `low` / `medium` / `high`，表示证据对 claim 的支持强度 |
| `impact` | 否 | 可能释放的责任、认知负担或维护成本 |
| `blast_radius` | 否 | 误判可能影响的范围 |
| `recommended_action` | 否 | 建议下一步的 Survey 或验证动作 |

规则：

- `confidence` 表示证据强度，不表示问题严重性。
- `claim` 永远是假设，例如“LegacyManager may no longer have a meaningful consumer”，而不是“LegacyManager is dead code”。
- Finding 默认临时存在，可以在一次协同中传递，不需要持久化。

## Governance Change

用途：把已经改变或准备改变的项目长期有效知识交给文档治理。

| 字段 | 必需 | 含义 |
| --- | --- | --- |
| `type` | 是 | 变化类型，例如 authority 变更、contract 变更、compatibility policy 变更 |
| `scope` | 是 | 受影响的事实、模块或架构边界 |
| `change` | 是 | 具体发生了什么变化 |
| `reason` | 是 | 为什么发生这个变化 |
| `authority_impact` | 是 | 哪些长期权威知识受到影响，而不是“应该修改哪个 Markdown” |
| `verification` | 否 | 已完成的验证证据 |

规则：

- `architecture-governance` 不负责决定修改哪个 Markdown。
- `simplify-codebase` 也不负责自己管理 ADR 生命周期。
- 长期知识同步一律交给 `govern-project-docs`。

## Closure

`project-governance` 负责最终检查治理影响是否收敛。

| 检查项 | 取值 |
| --- | --- |
| implementation consistent? | `yes` / `no` / `na` |
| contract consistent? | `yes` / `no` / `na` |
| active documentation consistent? | `yes` / `no` / `na` |
| required verification passed? | `yes` / `no` / `na` |

只有不存在未处理的治理后果，才返回 `CLOSED`。否则必须说明仍然开着的原因和下一个需要执行的路由。

## 协同流

```text
complexity-audit
  -> Governance Finding（hypothesis）
  -> simplify-codebase（Survey / Change）
  -> 若发生真实结构变化
  -> Governance Change
  -> govern-project-docs
  -> project-governance Closure
```

`architecture-governance` 在产生长期知识变化时也通过同一个 `Governance Change` 流向 `govern-project-docs`。

