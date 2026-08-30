# Codex end-to-end acceptance

This suite tests governance behavior as a black box. It creates isolated synthetic repositories, gives each request to `codex exec`, constrains the final response with a JSON Schema, and checks both the response and the actual filesystem diff.

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

The suite covers `NO_GOVERNANCE` and events E1 through E5. Read-only cases must leave no project-file diff. The E2 case is the only expected mutation and may modify only its declared canonical document. Model-dependent runs are acceptance evidence, not deterministic unit tests; do not place them on every commit until their variance and cost are understood.
