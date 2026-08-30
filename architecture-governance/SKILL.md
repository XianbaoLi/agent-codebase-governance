---
name: architecture-governance
version: 0.1.0
description: 判断拟新增的长期复杂度是否真的必要，遵循 Justify before add。只用于新增长期 state ownership、持久状态、公共契约、兼容义务或跨模块抽象等承诺。
---

# Architecture Governance

这个 Skill 只回答一个问题：**这个长期复杂度该不该新增？**

它不是架构评审委员会，不评审所有代码修改，也不亲自编辑文档或代码。它只在拟新增“长期复杂度承诺”时介入。

## 触发条件

考虑治理时，至少满足以下一种情况：

- 新增第二份事实来源；
- 新增长期 state ownership 或持久状态；
- 新增 public contract、schema 或 protocol；
- 新增 compatibility obligation；
- 新增跨模块 abstraction；
- 新增插件或机制边界，未来需要长期维护；
- 需要复用或解释一个已有概念。

以下情况通常不触发治理：

- 普通 helper；
- 局部重构；
- 测试补充；
- 变量重命名；
- 内部算法替换；
- 一次性脚本或数据修复。

## 调查

开始判断前，先掌握已有事实来源。使用 `$govern-project-docs` 读取当前权威知识、ADR 当前所有者和 Agent Context 路由；也要检查代码中已存在的同类状态、契约、抽象和 compatibility 机制。

回答这些问题：

- 现有系统为什么无法承担这个职责？
- 这个新概念是否已经存在，只是未被复用或未被命名？
- 是否新增了第二份事实来源，而不是引用已有权威？
- 是否新增了长期 state ownership 或持久状态？
- 是否新增了 public contract 或 schema/protocol？
- 是否新增了 compatibility obligation？
- 是否新增了跨模块 abstraction？
- 如果新增，它的存在理由是什么，未来谁负责维持一致？

如果新旧概念只是名字不同但语义相同，优先复用而不是新增。

## 输出

只输出以下结论之一：

| 结论 | 含义 |
| --- | --- |
| `ALLOW` | 现有系统无法承担该职责，新增复杂度有明确且无法替代的理由 |
| `ALLOW_WITH_CONDITIONS` | 可以新增，但必须满足明确条件，如先迁移消费者、删除旧事实来源、补齐契约测试或记录所有权 |
| `RECONSIDER` | 当前理由不足，应优先复用现有机制，或改为不增加长期义务的实现 |
| `UNRESOLVED` | 关键事实无法判断，不应自行批准或拒绝 |

`ALLOW_WITH_CONDITIONS` 必须写明条件。`RECONSIDER` 不是拒绝，而是要提供可替代方案。

## 知识变化

如果决定新增或改变长期知识，生成一个 `Governance Change`，字段至少包含：

```text
type
scope
change
reason
authority_impact
```

把它交给 `project-governance` 路由到 `govern-project-docs`。这个 Skill 不决定修改哪个 Markdown，也不负责自己更新文档。

