# Governance Trigger Contract

This is the lightweight ambient trigger surface for Agent Codebase Governance. It is meant to be visible from a target repository's `AGENTS.md` (or equivalent agent instructions) without loading every governance Skill.

## Fast path: stay out

Return `NO_GOVERNANCE` and do not load specialist governance Skills when the task is limited to local implementation detail, such as:

- a private helper or variable rename;
- a local algorithm replacement;
- ordinary test additions;
- formatting, lint, naming, or generic Clean Code review;
- a local refactor that does not change long-lived architecture, state ownership, contract, compatibility, authority, or Agent context.

## Trigger governance

Load `project-governance/SKILL.md` before making project mutations when the request or repository evidence plausibly involves any of these:

- a new or changed long-lived architecture/module boundary;
- new state ownership, persistence, migration responsibility, or durable state;
- a public API, contract, schema, protocol, plugin boundary, or compatibility obligation;
- a change to facts future Agents must treat as active/canonical authority;
- Code / ADR / active docs / contract disagreement;
- superseded or abandoned decisions that may still leave executable artifacts or active context;
- a governance change that still needs DID_IT verification, remediation, knowledge sync, or Closure.

If one of these signals is plausible but facts are incomplete, load `project-governance` and let it classify the event. Do not guess a specialist directly.

## Loading rule

1. Keep this trigger surface lightweight and ambient.
2. Only after it triggers, read `project-governance/SKILL.md`.
3. Then read only the routed specialist Skill.
4. Governance controls project evolution, not ordinary coding HOW.
