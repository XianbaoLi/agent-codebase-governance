# Upstream goern-project-docs

上游来源：

```text
https://github.com/CH-ZHOU-0512/govern-project-docs
```

许可证：MIT。

本项目只保留轻量适配壳，不 vendor 上游运行时、审计脚本、索引工具和模板，避免把治理能力复制成第二份事实来源。完整工作流以上游 `SKILL.md`、`README.md`、`references/migration-and-authority.md` 和 `references/automation-integration.md` 为准。

安装上游 Skill：

```powershell
git clone https://github.com/CH-ZHOU-0512/govern-project-docs.git (Join-Path $env:USERPROFILE ".codex\skills\govern-project-docs")
```

使用方式：

```text
使用 $govern-project-docs ...
```

当上游已安装时，具体审计、整理、索引和自动化流程优先委托给 `$govern-project-docs`；本目录的 `SKILL.md` 只保证治理模型的边界、接口和 authority 判定不发生漂移。

