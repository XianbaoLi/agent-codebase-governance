# Agent Codebase Governance

面向 Codex / AI Agent 长期开发场景的复杂度治理系统。它管理复杂度从“产生、存续、发现到回收”的完整生命周期，不替代普通代码规范检查，也不在每次普通工程改动上增加审批。

## 治理原则

1. **Justify before add：新增前先说明理由**
   新增长期复杂度之前，必须说明为什么现有系统无法承担这项职责。

2. **One authority for each fact：每个事实只有一个权威来源**
   对会影响 Agent 后续决策的事实、架构约束和设计决策，同一时间只能存在一个明确的权威来源。

3. **Audit what remains：持续审计存量**
   曾经合理的复杂度不代表永远合理，需要持续检查存量复杂度和治理漂移。

4. **Prove before delete：先证明，再删除**
   删除已有复杂度之前必须建立证据，不能因为“看起来没用”就删除。

元原则：**Governance must not become another source of entropy。** 治理系统自身必须保持轻量。除非有真实案例证明必要，否则不新增长期状态文件、Registry、数据库式 YAML 或复杂 workflow engine。

## 系统组成

| 组件 | 回答的问题 | 角色 |
| --- | --- | --- |
| `project-governance` | 当前属于哪种治理事件，应路由给谁，后续影响是否收敛 | 路由器与协调器 |
| `architecture-governance` | 这个长期复杂度该不该新增 | 新复杂度入口 |
| `govern-project-docs` | 当前什么知识具有权威性，Agent 应该相信什么 | 知识与上下文权威 |
| `complexity-audit` | 项目哪些地方可能存在不必要复杂度或治理漂移 | 广度发现 |
| `simplify-codebase` | 某个明确复杂度能不能安全删除、合并或必须保留 | 深度验证与回收 |

治理是例外路径，不是默认路径。普通 helper、局部重构、测试补充、变量重命名、内部算法替换等应返回 `NO_GOVERNANCE`。

## 事件路由

| 事件 | 判断要点 | 默认路由 |
| --- | --- | --- |
| `E1 Structural Change` | 新增子系统、长期 state ownership、持久状态、公共契约、schema/protocol、插件机制、兼容机制或跨模块抽象 | `architecture-governance` |
| `E2 Knowledge Change` | 当前有效事实或长期约束发生变化，继续相信旧知识会做出错误决策 | `govern-project-docs` |
| `E3 Health Check` | 技术债、重复设计、架构腐化、code/docs drift、治理审计 | `complexity-audit` |
| `E4 Simplification Candidate` | 用户已指出明确对象，如某个 Manager、adapter、重复状态 | `simplify-codebase` |
| `E5 Governance Drift` | Code != Documentation、Code != ADR、Active Doc A != Active Doc B 等 | `govern-project-docs`，先确定 authority |

`E5` 发现漂移时，不能默认“文档旧了”。也可能是代码违反了仍然有效的架构约束。无法判断权威时输出 `UNRESOLVED`，不要自行折中。

## 典型工作流

1. **防止熵新增**：`E1` -> `architecture-governance` 判断是否新增；若允许且改变长期知识，产出 `Governance Change` -> `govern-project-docs` 同步知识 -> `project-governance` 检查 Closure。
2. **修复知识漂移**：`E2/E5` -> `govern-project-docs` 确定权威并更新 active/superseded 路由；无法确定时报告 `UNRESOLVED`。
3. **回收存量熵**：`E3` -> `complexity-audit` 产出 `Governance Finding` -> `simplify-codebase` 深度验证 -> 若发生真实结构变化，产出 `Governance Change` -> `govern-project-docs` 同步长期权威知识 -> Closure。

## 目录结构

```text
.
├── README.md
├── GOVERNANCE_MODEL.md
├── integration-contract.md
├── project-governance/
│   └── SKILL.md
├── architecture-governance/
│   └── SKILL.md
├── complexity-audit/
│   └── SKILL.md
├── govern-project-docs/
│   ├── SKILL.md
│   └── UPSTREAM.md
├── integrations/
│   └── simplify-codebase.md
└── tests/
    └── validation-cases.md
```

## 第一版边界

- 覆盖治理对象：`Code`、`Architecture`、`Concept / Abstraction`、`State`、`Contract`、`Compatibility`、`Documentation`、`Agent Context`。
- 使用可观察复杂度类型，不引入伪精确的 Entropy Score。
- `unknown-complexity` 是合法类型，不需要为了分类而强行推断。
- `Governance Finding` 和 `Governance Change` 是 ephemeral artifact，不建立长期 findings 数据库。
- 不复制 `govern-project-docs` 与 `simplify-codebase` 的已有实现，只定义协议和边界。

## 验证

最小验证案例见 [tests/validation-cases.md](tests/validation-cases.md)，覆盖防止熵新增、权威漂移修复和存量熵回收三个场景。

