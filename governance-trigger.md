# Governance Trigger Contract

This is the lightweight ambient admission gate for Agent Codebase Governance. It is meant to be visible from a target repository's `AGENTS.md` (or equivalent agent instructions) without loading the governance router or specialist Skills.

It answers exactly one question:

> Does this request plausibly affect long-lived project evolution?

## Output

Return exactly one admission decision:

- `NO_GOVERNANCE`: the task is ordinary local implementation work. Continue normally and do not load `project-governance`.
- `GOVERNANCE_REQUIRED`: the task plausibly affects long-lived project evolution. Hand off to `project-governance/SKILL.md`.

This trigger does **not** classify E1–E5, choose a specialist, decide SHOULD, audit the project, remediate artifacts, or perform Closure.

## NO_GOVERNANCE fast path

Use `NO_GOVERNANCE` when the task is limited to local implementation detail, such as:

- a private helper or variable rename;
- a local algorithm replacement;
- ordinary test additions;
- formatting, lint, naming, or generic Clean Code review;
- a local refactor that does not change long-lived architecture, state ownership, contract, compatibility, authority, or Agent context.

## GOVERNANCE_REQUIRED signals

Use `GOVERNANCE_REQUIRED` when the request or repository evidence plausibly involves any of these:

- a new or changed long-lived architecture/module boundary;
- new state ownership, persistence, migration responsibility, or durable state;
- a public API, contract, schema, protocol, plugin boundary, or compatibility obligation;
- a change to facts future Agents must treat as active/canonical authority;
- Code / ADR / active docs / contract disagreement;
- superseded or abandoned decisions that may still leave executable artifacts or active context;
- a governance change that still needs DID_IT verification, remediation, knowledge sync, or Closure.

If a long-lived governance signal is plausible but facts are incomplete, prefer `GOVERNANCE_REQUIRED`; classification uncertainty belongs to the router, not the admission gate.

## Handoff rule

1. Keep this admission gate lightweight and ambient.
2. On `NO_GOVERNANCE`, do not load governance Skills.
3. On `GOVERNANCE_REQUIRED`, load `project-governance/SKILL.md`.
4. Let `project-governance` classify E1–E5 and route the required specialist.
5. Governance controls project evolution, not ordinary coding HOW.
