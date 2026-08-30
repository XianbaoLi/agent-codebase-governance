# Simplify-codebase 集成

上游来源：

```text
https://github.com/tt-a1i/simplify-codebase
```

本项目不复制 `simplify-codebase`。它作为独立 Skill 安装，通过 `Governance Finding` 和 `Governance Change` 与本系统衔接。

## 职责边界

`complexity-audit` 是广度发现，`simplify-codebase` 是深度验证。

| 阶段 | 输出 |
| --- | --- |
| `complexity-audit` | 0..N 个候选假设 `Governance Finding` |
| `simplify-codebase` | 对候选的 consumer / contract / history / persistence / dynamic usage 等证据证明，输出 `REMOVE` / `MERGE` / `RETAIN` / `UNRESOLVED` |

`RETAIN` 也是成功结果。

## Finding 到 simplify 的映射

`Governance Finding` 只代表“值得进一步验证的假设”，不是已确认问题。

| `Governance Finding` | `simplify-codebase` 使用方式 |
| --- | --- |
| `type` / `scope` | 确定 Focused 或 Broad 范围 |
| `claim` | 作为待证伪的假设，不改写成既定结论 |
| `evidence` | 作为静态 smell / lead，不当作删除权威 |
| `confidence` | 帮助排序，但不代表可安全删除 |
| `recommended_action` | 建议进入 Survey 或明确用户授权后可进入 Change |

## 调用模式

- 用户请求健康检查、技术债审计或发现候选：`simplify-codebase` 使用 `Survey`，保持只读并返回排序证据。
- 用户明确要求删除、合并或化简某个已指出对象：`simplify-codebase` 使用 `Change`，但必须先证明每个 cut，并在授权 scope 内执行。
- `E4` 到达时，务必把“这个 Manager 多余”转换为假设，例如“这个 Manager 可能不再有实际 consumer”，而不是直接删除。

## 结果回传

如果 `simplify-codebase` 发生真实结构变化，且改变了项目长期有效知识，它不直接管理 ADR 生命周期或文档，而是生成一个 `Governance Change`：

```text
type
scope
change
reason
authority_impact
```

由 `project-governance` 路由到 `govern-project-docs` 完成权威知识同步，最后做 Closure。

如果结果只是证据报告，或结论是 `RETAIN` / `UNRESOLVED`，不强行制造文档变化。

