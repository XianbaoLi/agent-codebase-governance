# Codex end-to-end acceptance

This suite tests governance behavior as a black box. It creates isolated synthetic repositories, exposes the lightweight ambient admission gate through `AGENTS.md`, gives each request to `codex exec`, constrains the final response with a JSON Schema, and checks both the response and the actual filesystem diff. `NO_GOVERNANCE` fixtures intentionally omit the router and specialist Skills, so the fast path cannot depend on a second governance classification pass.

Run deterministic contract checks:

```bash
python tests/e2e/run_e2e.py --check
```

Self-test the harness without model calls:

```bash
python tests/e2e/run_e2e.py --agent-command "python tests/e2e/fake_codex.py"
```

Run the real acceptance suite with an authenticated Codex CLI:

```bash
python tests/e2e/run_e2e.py
```

Run one case and preserve a failed fixture for inspection:

```bash
python tests/e2e/run_e2e.py --case e5-conflicting-active-authorities --keep-failed
```

The suite covers both admission decisions plus events E1 through E5, plus `lifecycle-e1-to-closure`, which must show the ordered trace `TRIGGER -> ROUTING -> SHOULD -> EXECUTION -> DID_IT -> REMEDIATION -> KNOWLEDGE_SYNC -> CLOSURE` and the expected final filesystem state. Read-only cases must leave no project-file diff. Model-dependent runs are acceptance evidence, not deterministic unit tests; do not place them on every commit until their variance and cost are understood.
