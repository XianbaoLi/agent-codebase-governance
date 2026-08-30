# Agent instructions

This repository is the source and acceptance suite for Agent Codebase Governance.

- Treat `GOVERNANCE_MODEL.md` and `integration-contract.md` as the current system contracts.
- For governance work, begin with `project-governance/SKILL.md`, then read only the routed specialist Skill.
- Treat files under `tests/e2e/fixtures/` as synthetic repositories, never as current project facts.
- Run `python tests/e2e/run_e2e.py --check` after changing contracts, Skills, cases, schemas, or the harness.
- Do not weaken an assertion merely to make a model output pass. Change an expectation only when the governance contract changes.

