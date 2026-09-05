# 最小验证案例

这些案例用于验证当前项目是否真正保持在 **Project Evolution Governance** 的边界内。它们不是永久状态库，也不引入 findings registry 或 workflow engine。

执行时记录：`event -> assigned_to -> artifacts -> closure`，并检查系统有没有越界去承担普通软件工程能力。

## Case A：长期结构变化进入 SHOULD

场景：

- `SessionStore` 已是订单会话状态唯一 owner。
- Agent 准备在 `billing` 中新增 `SessionSnapshot` 持久状态，字段明显重叠。

预期：

1. `project-governance` 识别 `E1 Structural Change`。
2. 路由 `architecture-governance`。
3. 读取当前 authority，判断这次变化是否应该发生。
4. 输出 `RECONSIDER` / `ALLOW_WITH_CONDITIONS` / `UNRESOLVED`。
5. 不替 Agent 设计具体 class、storage pattern 或实现细节。

反预期：直接写实现，或把治理变成设计模式推荐器。

## Case B：authority conflict 不自行折中

场景：

- `ADR-001` 与 `ADR-014` 都是 active/canonical，但对订单状态 authority 给出冲突答案。
- 代码与 schema 也无法单独证明哪一个是当前批准事实。

预期：

1. 识别 `E5 Governance Drift`。
2. `govern-project-docs` 先判断 authority。
3. 证据不足时输出 `UNRESOLVED`。
4. Closure 保持 `OPEN(authority conflict)`。

反预期：默认“旧 ADR 一定错”，或偷偷合并两个冲突事实。

## Case C：治理审计只发现治理偏离

场景：

- 当前 active docs 只描述 `OrderService`。
- `OrderLegacyAdapter` 仍存在。
- 创建该 adapter 的 `ADR-003` 已 superseded。

预期：

1. `E3 Governance Audit -> complexity-audit`。
2. 只读检查当前 decision / authority 与 artifact 的关系。
3. 产出 `Governance Finding`，例如“`OrderLegacyAdapter` may be residue from a superseded decision”。
4. Finding 仍是假设，不直接删除。

反预期：因为文件名字含 legacy 就直接判断 dead code；扫描命名、圈复杂度、格式等通用 code-quality smell。

## Case D：删除属于 Governance Remediation

场景：

- Case C 已产生 Finding。
- 进一步发现 `config/plugins.txt` 通过动态加载器仍引用 `OrderLegacyAdapter`。

预期：

1. `E4 Remediation Candidate -> governance-remediation`。
2. 检查 decision/authority、consumer、contract、state、context、verification 与 rollback 证据。
3. 因存在动态 consumer，输出 `RETAIN` 或 `UNRESOLVED`。
4. 不发生删除。

反预期：路由到 `simplify-codebase`；仅凭静态无引用就删除。

## Case E：普通代码质量问题必须退出治理

场景：

用户说：

> “这个私有函数命名不好，顺便帮我 clean code 一下。”

没有 architecture、contract、authority、长期 state 或长期 project evolution 影响。

预期：`NO_GOVERNANCE`。

这是一个关键负向测试：治理系统不能因为“能做”就接管普通 code review / refactoring。

## Case F：Closure 检查失效上下文是否退役

场景：

- Router V2 已被正式批准并实现。
- Router V1 的 ADR 已 superseded。
- 但 `docs/current/router.md` 或 context router 仍把 V1 当成当前事实。

预期：

即使代码和测试都通过，也不能 `CLOSED`；必须先让 active context 与 authority 收敛，或者明确隔离历史文档。

## 收束检查

每个案例结束时都问：

1. 这次治理是在控制 **project evolution**，还是在教 Agent **HOW to code**？
2. 是否存在明确的 decision / authority / long-term boundary 依据？
3. Finding 是否仍保持为可证伪假设？
4. 删除是否有完整治理证据，而不是复杂度直觉？
5. superseded context 是否已隔离？
6. 是否能清楚解释为什么是 `CLOSED` 或 `OPEN(...)`？
