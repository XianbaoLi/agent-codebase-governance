# Governance Model

## 目标

这个系统管理复杂度从“产生、存续、发现到回收”的完整生命周期，目标是降低 Agent 长期开发时因重复事实、失效约束、无人负责的抽象和无法移除的兼容负担而产生的认知成本。

它不是：

- 普通代码规范检查器；
- 架构评审委员会；
- 包办一切的 Super Skill；
- 长期状态机或 findings database。

## 生命周期

| 阶段 | 治理能力 | 核心原则 | 输出 |
| --- | --- | --- | --- |
| 产生 | `architecture-governance` | Justify before add | `ALLOW` / `ALLOW_WITH_CONDITIONS` / `RECONSIDER` / `UNRESOLVED` |
| 存续 | `govern-project-docs` | One authority for each fact | active/canonical 路由、ADR 生命周期、上下文隔离 |
| 发现 | `complexity-audit` | Audit what remains | 0..N 个 `Governance Finding` |
| 回收 | `simplify-codebase` | Prove before delete | `REMOVE` / `MERGE` / `RETAIN` / `UNRESOLVED` |
| 收敛 | `project-governance` | Closure over ceremony | `CLOSED` 或未收敛原因 |

## 治理对象

第一版只重点覆盖：

- `Code`
- `Architecture`
- `Concept / Abstraction`
- `State`
- `Contract`
- `Compatibility`
- `Documentation`
- `Agent Context`

不要为这些对象设计伪精确的复杂度分数。用可观察的复杂度类型描述现象。

## 复杂度类型

- `duplicated-concept`
- `duplicated-state`
- `obsolete-contract`
- `obsolete-compatibility`
- `redundant-abstraction`
- `governance-drift`
- `unknown-complexity`

`unknown-complexity` 是合法类型。证据不足时保留它为 `unknown`，不允许为分类而强行推断。

## 事件与能力边界

`project-governance` 只负责识别事件、路由、协调后续影响和检查 Closure。它不亲自进行架构分析、代码删除、consumer analysis 或文档权威判断。

四个专业能力各自回答一个独立问题：

| 能力 | 只回答 |
| --- | --- |
| `architecture-governance` | 这个复杂度该不该新增？ |
| `govern-project-docs` | 当前什么知识具有权威性，Agent 应该相信什么？ |
| `complexity-audit` | 项目哪里可能存在不必要复杂度或治理漂移？ |
| `simplify-codebase` | 某个明确已有复杂度能不能被安全删除、合并或必须保留？ |

禁止构建一个包办一切的 Super Skill。

## 权威与漂移

发现 `Code != Documentation`、`Code != ADR`、`Active Doc A != Active Doc B` 等漂移时，首先确定 authority，而不是默认文档过时。

如果无法判断权威，输出 `UNRESOLVED`。

`govern-project-docs` 应保留以下上游思想：

- active + canonical 表示当前权威；
- historical docs 可以保留，但默认不能污染 Agent 当前 context；
- ADR 有生命周期；
- `AGENTS.md` 更偏向 context router，而不是百科全书；
- 一个事实尽量只有一个 canonical source；
- 确定性检查交给脚本，语义冲突交给 Agent；
- 发现 authority conflict 时不能自行折中。

## Closure

治理流程不是“代码改完”就结束。第一版 Closure 只检查：

1. implementation consistent?
2. contract consistent?
3. active documentation consistent?
4. required verification passed?

不适用项允许 `N/A`。只有不存在未处理的治理后果，才可判定为 `CLOSED`。

不建立单独的 closure Skill，也不建立 workflow 状态数据库。

## 设计约束

- 治理是例外路径。
- 优先复用现有事实来源，不重复建立新事实来源。
- 优先使用协议和路由连接现有能力。
- 不复制已有 Skill 能力。
- 每增加一个治理机制，都要反问：它本身是不是新的 accidental complexity？

