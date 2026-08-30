---
name: complexity-audit
version: 0.1.0
description: 对项目做只读的广度复杂度与治理漂移扫描，只发现候选，不删除代码，输出 Governance Finding 而不是确定结论。
---

# Complexity Audit

这个 Skill 回答：**项目哪些地方值得进一步调查？**

它是广度发现。深度验证交给 `simplify-codebase`。它不删除代码，不做完整 consumer / contract 证明，不计算伪精确的 Entropy Score。

## 范围

对仓库做结构化的 read-only 调查，重点覆盖治理对象：

- `Code`
- `Architecture`
- `Concept / Abstraction`
- `State`
- `Contract`
- `Compatibility`
- `Documentation`
- `Agent Context`

允许做的轻量调查：

- 静态 references；
- 明显 consumers；
- 目录结构与模块边界；
- 当前 active docs；
- 简单历史信息。

不追求完整证明。发现一个“看起来值得查”的对象即可产出 Finding。

## 复杂度类型

使用以下可观察类型：

- `duplicated-concept`
- `duplicated-state`
- `obsolete-contract`
- `obsolete-compatibility`
- `redundant-abstraction`
- `governance-drift`
- `unknown-complexity`

`unknown-complexity` 是合法类型。证据不足时保留它，不要为了分类而强行推断。

## 产出 Governance Finding

每个候选输出一个 `Governance Finding`：

```text
type: <复杂度类型>
scope: <符号、路径、模块或边界>
claim: <可证伪的假设>
evidence: <已观察到的线索>
confidence: low | medium | high
```

可选字段：`impact`、`blast_radius`、`recommended_action`。

`confidence` 表示证据对 claim 的支持强度，不表示问题严重性。

## 交付

报告：

1. 覆盖范围和明确排除的领域；
2. 0..N 个 Finding；
3. 每个 Finding 的下一步验证方向；
4. 本轮未覆盖的盲区。

没有发现高价值 Candidate 也是成功结果。

## 边界

- 不修改文件；
- 不直接删除、合并或重构；
- 不建立 findings registry 或 complexity database；
- 不把静态 smell 写成已确认问题；
- 不冒充 `simplify-codebase` 做深度证明。

