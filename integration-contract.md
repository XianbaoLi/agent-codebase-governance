# Integration Contract

跨 Skill 对象保持轻量，并且默认都是 ephemeral artifact。它们服务于一次项目演化治理闭环，不建立长期 findings database。

## Governance Finding

用途：描述“项目可能已经偏离当前有效决策”的可证伪假设。

| 字段 | 必需 | 含义 |
| --- | --- | --- |
| `type` | 是 | `decision-drift`、`obsolete-artifact`、`contract-drift` 等治理类型 |
| `scope` | 是 | 符号、路径、模块、文档或边界 |
| `expected` | 是 | 根据当前 authority 应该是什么状态 |
| `observed` | 是 | 实际观察到的状态 |
| `claim` | 是 | 可证伪假设，不能写成既定结论 |
| `evidence` | 是 | 支持 claim 的证据 |
| `confidence` | 是 | `low` / `medium` / `high` |
| `next_validation` | 否 | 下一步需要补什么证据 |

Finding 不能因为“复杂”“重复”“不优雅”而产生；必须与项目有效 authority / decision / contract 有关系。

## Governance Change

用途：描述已经发生并会改变长期项目知识的治理变化。

| 字段 | 必需 | 含义 |
| --- | --- | --- |
| `type` | 是 | authority、contract、architecture、retirement 等变化类型 |
| `scope` | 是 | 受影响的事实、模块或边界 |
| `change` | 是 | 实际发生了什么 |
| `reason` | 是 | 治理依据 |
| `authority_impact` | 是 | 哪些长期权威知识受到影响 |
| `verification` | 否 | 已完成验证证据 |

长期知识同步统一交给 `govern-project-docs`。

## Remediation Decision

`governance-remediation` 对一个明确治理候选输出：

```text
decision: FIX | RETIRE | REMOVE | RETAIN | UNRESOLVED
scope:
reason:
evidence:
consumer_check:
contract_check:
state_check:
context_impact:
verification:
```

只有 `REMOVE` 允许执行删除；证据不足必须 `UNRESOLVED`。

## Closure

`project-governance` 最终检查：

| 检查项 | 取值 |
| --- | --- |
| implementation consistent? | `yes` / `no` / `na` |
| contract consistent? | `yes` / `no` / `na` |
| active documentation consistent? | `yes` / `no` / `na` |
| superseded context isolated? | `yes` / `no` / `na` |
| required verification passed? | `yes` / `no` / `na` |

只有不存在未处理治理后果才返回 `CLOSED`。

## 协同流

```text
project-governance (Trigger)
  -> Context / Authority
  -> architecture-governance (SHOULD, when needed)
  -> Agent executes HOW
  -> complexity-audit (DID IT / governance audit)
  -> Governance Finding (if drift exists)
  -> governance-remediation
  -> FIX / RETIRE / REMOVE / RETAIN / UNRESOLVED
  -> Governance Change (when long-term knowledge changed)
  -> govern-project-docs
  -> project-governance Closure
```

外部实现或简化工具不属于这份协议的必经阶段。
