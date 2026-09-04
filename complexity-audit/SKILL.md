---
name: complexity-audit
version: 0.2.0
description: 对项目做只读治理审计，发现项目实现、有效决策、契约、文档和 Agent Context 之间的漂移与失效残留；不做通用代码质量或复杂度审计。
---

# Governance Audit

这个 Skill 回答：**项目当前状态是否已经偏离有效的项目决策与治理边界？**

它是 read-only 的 `DID IT` 检查。它不负责判断代码是否优雅、是否足够简洁，也不因为一个模块“看起来复杂”就提出删除建议。

## 进入条件

至少满足一个条件才进入治理审计：

- 存在一个可识别的有效架构决策或约束，可与实现对照；
- Code / ADR / active docs / contract 之间出现不一致迹象；
- 某个历史决策已 superseded / abandoned，但可能仍留下 artifact；
- 某段 historical context 可能继续影响 Agent 当前决策；
- 一次治理变化执行后需要做 Closure 前验证。

否则返回 `NO_GOVERNANCE_FINDING`，不要退化成普通 code review。

## 调查范围

允许只读检查：

- 代码与模块边界；
- references 与明显 consumers；
- contracts / schemas / compatibility 层；
- active / canonical docs；
- ADR 生命周期；
- superseded / historical docs；
- 与当前变化有关的 git history；
- Agent context routing（如 `AGENTS.md`）。

## Finding 类型

- `decision-drift`
- `authority-conflict`
- `obsolete-artifact`
- `superseded-context-leak`
- `orphaned-responsibility`
- `contract-drift`
- `unknown-governance-risk`

## Governance Finding

```text
type: <finding type>
scope: <符号、路径、模块、文档或边界>
expected: <根据当前有效 authority 应该是什么状态>
observed: <实际观察到什么>
claim: <可证伪的治理假设>
evidence: <证据>
confidence: low | medium | high
next_validation: <下一步如何验证>
```

`confidence` 表示证据对 claim 的支持强度，不表示严重性。

## 不属于本 Skill

- lint / formatting / naming；
- 通用 duplicated code；
- 通用 Clean Code review；
- “代码太多所以应该删”；
- “抽象太复杂所以应该重构”；
- 没有当前项目 authority 依据的架构偏好；
- 直接修改、删除或合并代码。

## 交付

报告：

1. 本轮使用了哪些 authority / constraints；
2. 覆盖范围与明确盲区；
3. 0..N 个 `Governance Finding`；
4. 每个 Finding 的下一步验证方向；
5. 是否足以进入 `governance-remediation`。

没有 Finding 是成功结果。
