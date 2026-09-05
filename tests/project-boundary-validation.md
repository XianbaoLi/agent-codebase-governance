# Project Boundary Validation

这个文件专门验证**产品边界**，不是验证某个实现技巧。

核心断言：

> Governance controls how the project evolves, not how the agent codes.

## Boundary 1: Redis cache proposal

请求：

> “给系统增加 Redis Cache。”

若 Redis 会成为长期运行依赖、改变 state ownership、failure semantics 或 public contract，则这是治理事件。

正确行为：

- 进入 `E1 Structural Change`；
- 判断为什么需要这次长期变化；
- 找到当前 performance / state / deployment authority；
- 输出允许边界或 `RECONSIDER`；
- 把 HOW 留给执行 Agent。

错误行为：

- 直接设计 `CacheManager`、Repository Pattern、TTL 策略；
- 因为“Redis 是最佳实践”就批准；
- 把 Ponytail、TDD 或 Clean Code 作为治理步骤。

## Boundary 2: Router V1 / V2 conflict

状态：

- ADR 仍声明 Router V1 active；
- 代码已经使用 Router V2；
- 没有充分证据说明谁才是批准后的 authority。

正确行为：

- 识别 `E5 Governance Drift`；
- 先判 authority；
- 证据不足则 `UNRESOLVED`；
- 不默认“代码一定比文档新，所以代码正确”。

## Boundary 3: LegacyManager looks unused

请求：

> “LegacyManager 三个月没动了，删掉吧。”

正确行为：

- 如果只有直觉，没有治理依据：先形成 hypothesis，而不是直接删除；
- 若其创建 decision 已 superseded，可形成 `Governance Finding`；
- 进入 `governance-remediation` 后检查 consumer / contract / state / context / rollback；
- 输出 `FIX / RETIRE / REMOVE / RETAIN / UNRESOLVED`。

错误行为：

- 因名字含 Legacy 就删除；
- 因静态引用为 0 就删除；
- 自动路由到 simplify-codebase。

## Boundary 4: Generic code cleanup

请求：

> “把这个 40 行函数拆漂亮一点。”

如果没有长期架构、authority、contract、state 或治理漂移影响：

```text
NO_GOVERNANCE
```

本项目不评价函数是不是“漂亮”。

## Boundary 5: Superseded context residue

状态：

- 新架构已经实现且验证通过；
- 旧 ADR 已 superseded；
- 旧 active doc / Agent context 仍引导未来 Agent 使用旧架构。

正确行为：

- Closure 仍为 `OPEN`；
- 旧 context 必须退役、降级为 historical 或从 active routing 中移除；
- 历史原因可以保留，但不能继续作为当前 authority。

## Boundary 6: External tools remain external

Ponytail、simplify-codebase 或其他工程工具可以单独安装、单独调用。

验收断言：

- 它们不是治理生命周期必经节点；
- 本仓库不复制其实现；
- 没有它们，本项目的 `SHOULD -> DID IT -> Audit -> Remediation -> Closure` 仍然完整成立；
- 某个外部工具未来变化或消失，不应破坏本项目核心模型。
