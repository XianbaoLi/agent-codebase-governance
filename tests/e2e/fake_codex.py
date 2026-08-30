#!/usr/bin/env python3
"""Deterministic stand-in used only to self-test the acceptance harness."""

from __future__ import annotations

import json
from pathlib import Path
import sys


def argument(name: str) -> str:
    return sys.argv[sys.argv.index(name) + 1]


workspace = Path(argument("--cd"))
output = Path(argument("--output-last-message"))
fixture_files = {path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file()}

if "config/runtime.toml" in fixture_files:
    runtime = workspace / "docs/current/runtime.md"
    runtime.write_text(runtime.read_text(encoding="utf-8").replace("permissive", "strict"), encoding="utf-8")
    result = ("E2", "govern-project-docs", "UPDATED authority to strict", [], ["runtime authority synced"], True, "CLOSED")
elif "config/plugins.txt" in fixture_files:
    result = ("E4", "simplify-codebase", "RETAIN: dynamic consumer exists", [], [], False, "CLOSED")
elif "docs/decisions/ADR-014.md" in fixture_files:
    result = ("E5", "govern-project-docs", "UNRESOLVED authority conflict", [], [], False, "OPEN(authority conflict)")
elif "docs/current/state.md" in fixture_files:
    result = ("E1", "architecture-governance", "RECONSIDER duplicate state owner", [], [], False, "OPEN(reconsider)")
elif "src/legacy_adapter.py" in fixture_files:
    findings = [{
        "type": "obsolete-compatibility", "scope": "OrderLegacyAdapter",
        "claim": "OrderLegacyAdapter may have no current consumer",
        "evidence": "No static reference was observed", "confidence": "medium"
    }]
    result = ("E3", "complexity-audit", "AUDIT produced a candidate FINDING", findings, [], False, "CLOSED")
else:
    result = ("NO_GOVERNANCE", "none", "NO_GOVERNANCE", [], [], False, "CLOSED")

event, assigned, decision, findings, changes, mutation, closure = result
output.write_text(json.dumps({
    "event": event,
    "assigned_to": assigned,
    "decision": decision,
    "findings": findings,
    "changes": changes,
    "mutation_attempted": mutation,
    "closure": closure,
    "evidence": ["fake adapter"],
}, ensure_ascii=False), encoding="utf-8")

