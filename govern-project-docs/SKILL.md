---
name: govern-project-docs
version: 0.1.0
description: 保持项目文档与 Agent Context 的权威性，处理知识变化、ADR 生命周期、active/superseded/archive 路由和 authority drift；在无法判定权威时输出 UNRESOLVED。
---

# Govern Project Docs

这个 Skill 回答：**当前什么知识具有权威性，Agent 应该相信什么？**

它基于已有的 [上游 `govern-project-docs`](UPSTREAM.md)。上游已经定义了完整审计、权威引擎、索引和自动化工作流，本目录只做最小适配，不复制上游运行时实现。

## 角色

在治理系统中负责：

- 处理 `E2 Knowledge Change`；
- 处理已经确定 authority 的 `E5 Governance Drift`；
- 接收 `Governance Change` 并同步长期权威知识；
- 管理 canonical source、ADR 生命周期、`AGENTS.md` 路由、上下文隔离和代码与文档映射。

## 核心规则

保留并优先执行这些上游思想：

- active + canonical 表示当前权威；
- historical docs 可以保留，但默认不能污染 Agent 当前 context；
- ADR 有生命周期，历史决策可被 superseded 或 archive，但不应静默改写；
- `AGENTS.md` 更偏向 context router，而不是百科全书；
- 一个事实尽量只有一个 canonical source；
- 确定性检查交给脚本，语义冲突交给 Agent；
- API、event、database、dependency 等机器事实应留在 machine contract 中；
- 发现 authority conflict 时不能自行折中。

## 接收 Governance Change

当收到 `Governance Change` 时：

1. 确定受影响的长期事实和当前 authority；
2. 检查是否已经存在另一个 active source 声称同一 authority；
3. 更新 active / superseded / archive 关系；
4. 更新 `AGENTS.md` 或等价 context router，而不是让它变成重复知识百科；
5. 更新必要索引和跨文档链接；
6. 返回更新后的 authority map 和当前 Agent 应读取的入口。

不要仅根据文件名、时间戳或“看起来更旧”来选择 winner。语义冲突必须由权威来源、当前契约或用户决策来解决；无法判断时输出 `UNRESOLVED`。

## 处理 Governance Drift

面对 `Code != Documentation`、`Code != ADR`、`Active Doc A != Active Doc B` 等漂移：

1. 先判断哪个事实是当前 authority；
2. 不要把“文档旧了”当作默认结论；
3. 如果代码违反了仍然有效的架构约束，治理目标是修复代码，而不是改文档迁就错误实现；
4. 无法判断 authority 时输出 `UNRESOLVED`。

## 最小改动

- 修改只覆盖被本次治理事件影响的权威事实；
- 保留历史记录和原始理由；
- 不创建 per-session 日志；
- 仅在有真实重复、漂移或长期约束变化时才增加 governance metadata；
- 不复制上游 Node.js 工具链到本项目。

