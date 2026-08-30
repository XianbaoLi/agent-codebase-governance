# 最小验证案例

这些案例用于验证 v0.1 的治理边界是否成立。它们不是永久的自动化状态库；第一版先做人工可复现的验收，不引入新的 findings registry 或测试 engine。

执行方式：按案例给定一个仓库状态或请求，走一遍对应 SKILL，记录 `event -> assigned_to -> artifacts -> closure`，再和预期比较。

## Case A：防止熵新增

场景：

- 仓库已经有一个 canonical state，`docs/architecture/state.md` 和代码显示 `SessionStore` 是订单会话状态的唯一 owner。
- Agent 准备在 `billing` 模块新增一套 `SessionSnapshot` 持久状态，字段与 `SessionStore` 重叠，但没有说明为什么现有 owner 无法承担。

预期发生：

1. `project-governance` 将请求识别为 `E1 Structural Change`。
2. 路由到 `architecture-governance`。
3. `architecture-governance` 使用 `$govern-project-docs` 找到已有 `state ownership` 权威来源。
4. 输出 `RECONSIDER` 或 `ALLOW_WITH_CONDITIONS`，并要求：复用现有 owner、解释不可替代性，或证明这是真正不同的权威边界。
5. 不修改代码或文档，不新增长期 finding 文件。

反预期：

- 直接创建第二份重叠状态；
- 因为没有 linter 报错就放行；
- 架构审核被用于普通局部代码修改。

## Case B：权威漂移与 ADR 生命周期

场景：

- `ADR-001` 仍标记为 `active`，声称 `orders.status` 是订单状态的事实来源。
- 后来代码与 schema 已改用 `order_state` 表作为当前 owner，并有一条新的 `ADR-014` 没有正确声明 supersession。
- 一个任务继续按旧 ADR 读取 `orders.status`。

预期发生：

1. `project-governance` 识别为 `E5 Governance Drift`，不默认“旧文档错了”。
2. 路由到 `govern-project-docs`。
3. `govern-project-docs` 先确定当前 authority：代码、schema 和 `ADR-014` 是否已经一致地拥有该事实。
4. 若当前 owner 明确，则把 `ADR-001` 标记为 `superseded`，在 `ADR-014` 声明 `supersedes`，并更新 `AGENTS.md` 或等价 context router 指向 `order_state`。
5. 如果两套权威无法判断，输出 `UNRESOLVED`，不自行折中。

反预期：

- 直接删除旧 ADR 或改写历史理由；
- 默认文档永远过时；
- 让两个 active document 继续同时声称同一 authority。

## Case C：发现并回收存量熵

场景：

- 项目里有一个疑似 obsolete 的 `OrderLegacyAdapter`，以及一套可能与新 canonical service 重复的事件状态。
- 用户说“帮我检查项目是不是越来越乱”，随后又指出“这个 adapter 是不是多余”。

预期发生：

1. 健康检查阶段：`project-governance` 识别 `E3 Health Check`，路由到 `complexity-audit`。
2. `complexity-audit` 只做只读调查，产出 `Governance Finding`，`claim` 保持假设，例如“`OrderLegacyAdapter` 可能不再有实际生产消费者”。
3. 用户明确追问具体对象后，`project-governance` 识别 `E4`，路由到 `simplify-codebase`。
4. `simplify-codebase` 进行 Survey 或授权后的 Change，输出 `REMOVE` / `MERGE` / `RETAIN` / `UNRESOLVED`。
5. 如果真实结构变化改变了长期权威知识，生成 `Governance Change`，由 `govern-project-docs` 同步；`project-governance` 最终做 Closure。

反预期：

- `complexity-audit` 直接删除文件；
- `simplify-codebase` 因为用户说“多余”就不做 consumer / contract / persistence 证据直接删除；
- 删除后不更新 active documentation 或 ADR；
- 建立长期 findings database 记录每个候选。

## 收束检查

每个案例结束时检查：

1. 是否出现了错误的所有权转移？
2. 是否新增了本不必要的长期状态或 registry？
3. 是否保留了证据和 authority 判定过程？
4. 是否能清楚解释最终为 `CLOSED` 或仍为 `OPEN(...)`？

