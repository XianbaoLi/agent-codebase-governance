#!/usr/bin/env python3
"""Deterministic stand-in used only to self-test the acceptance harness."""

from __future__ import annotations

import json
from pathlib import Path
import sys


def argument(name: str) -> str:
    return sys.argv[sys.argv.index(name) + 1]


def trace(*phases: tuple[str, str, str]) -> list[dict[str, str]]:
    return [
        {"phase": phase, "assigned_to": assigned_to, "outcome": outcome}
        for phase, assigned_to, outcome in phases
    ]


workspace = Path(argument("--cd"))
output = Path(argument("--output-last-message"))
fixture_files = {
    path.relative_to(workspace).as_posix()
    for path in workspace.rglob("*")
    if path.is_file()
}

if "docs/decisions/ADR-010.md" in fixture_files:
    (workspace / "src/session_store.py").write_text(
        "class SessionStore:\n"
        "    def load_session(self, session_id):\n"
        "        return {\\\"id\\\": session_id}\n",
        encoding="utf-8",
    )
    service = workspace / "src/service.py"
    service.write_text(
        service.read_text(encoding="utf-8")
        .replace("legacy_session_store", "session_store")
        .replace("LegacySessionStore", "SessionStore"),
        encoding="utf-8",
    )
    legacy = workspace / "src/legacy_session_store.py"
    legacy.unlink()
    state = workspace / "docs/current/state.md"
    state.write_text(
        "---\nstatus: active\nauthority: canonical\n---\n"
        "SessionStore is the current and only owner of session state.\n",
        encoding="utf-8",
    )
    findings = [{
        "type": "obsolete-artifact",
        "scope": "src/legacy_session_store.py::LegacySessionStore",
        "expected": "SessionStore is the sole active session-state owner after consumer migration",
        "observed": "LegacySessionStore still existed after the consumer was migrated",
        "claim": "LegacySessionStore may be obsolete residue after the staged migration",
        "evidence": "ADR-010 requires sole ownership and the consumer no longer imports the legacy owner",
        "confidence": "high",
        "next_validation": "Verify no remaining consumer, contract, state, or dynamic loading responsibility",
    }]
    changes = [
        {
            "type": "architecture",
            "scope": "session state ownership",
            "change": "Migrated the consumer to SessionStore and removed LegacySessionStore",
            "reason": "ADR-010 approved a sole-owner migration",
            "authority_impact": "SessionStore is now the sole runtime owner",
            "verification": "Consumer points to SessionStore and legacy file is absent",
        },
        {
            "type": "authority",
            "scope": "docs/current/state.md",
            "change": "Updated active state authority to SessionStore",
            "reason": "Runtime migration and remediation completed",
            "authority_impact": "Future agents now read the new owner as canonical",
            "verification": "Active doc names SessionStore",
        },
    ]
    result = {
        "event": "E1",
        "assigned_to": "project-governance",
        "decision": "ALLOW_WITH_CONDITIONS; staged migration completed and CLOSED",
        "findings": findings,
        "changes": changes,
        "trace": trace(
            ("TRIGGER", "project-governance", "E1 structural change detected"),
            ("SHOULD", "architecture-governance", "ALLOW_WITH_CONDITIONS under ADR-010"),
            ("EXECUTION", "agent", "Created SessionStore and migrated the consumer"),
            ("DID_IT", "complexity-audit", "Found the legacy owner as possible obsolete residue"),
            ("REMEDIATION", "governance-remediation", "REMOVE after consumer/contract/state checks"),
            ("KNOWLEDGE_SYNC", "govern-project-docs", "Updated active owner authority"),
            ("CLOSURE", "project-governance", "CLOSED"),
        ),
        "mutation_attempted": True,
        "closure": "CLOSED",
        "evidence": ["ADR-010", "consumer migration", "legacy removal", "active doc sync"],
    }
elif "config/runtime.toml" in fixture_files:
    runtime = workspace / "docs/current/runtime.md"
    runtime.write_text(
        runtime.read_text(encoding="utf-8").replace("permissive", "strict"),
        encoding="utf-8",
    )
    result = {
        "event": "E2",
        "assigned_to": "govern-project-docs",
        "decision": "UPDATED authority to strict",
        "findings": [],
        "changes": [{
            "type": "authority",
            "scope": "docs/current/runtime.md",
            "change": "Synced runtime default to strict",
            "reason": "config/runtime.toml is the declared machine authority",
            "authority_impact": "Active runtime documentation now matches machine authority",
            "verification": "Document contains strict",
        }],
        "trace": trace(
            ("TRIGGER", "project-governance", "Knowledge change detected"),
            ("KNOWLEDGE_SYNC", "govern-project-docs", "Synced known authority"),
            ("CLOSURE", "project-governance", "CLOSED"),
        ),
        "mutation_attempted": True,
        "closure": "CLOSED",
        "evidence": ["config/runtime.toml"],
    }
elif "config/plugins.txt" in fixture_files:
    result = {
        "event": "E4",
        "assigned_to": "governance-remediation",
        "decision": "RETAIN: dynamic consumer exists",
        "findings": [],
        "changes": [],
        "trace": trace(
            ("TRIGGER", "project-governance", "Remediation candidate detected"),
            ("REMEDIATION", "governance-remediation", "RETAIN because a dynamic consumer exists"),
            ("CLOSURE", "project-governance", "CLOSED"),
        ),
        "mutation_attempted": False,
        "closure": "CLOSED",
        "evidence": ["config/plugins.txt references OrderLegacyAdapter"],
    }
elif "docs/decisions/ADR-014.md" in fixture_files:
    result = {
        "event": "E5",
        "assigned_to": "govern-project-docs",
        "decision": "UNRESOLVED authority conflict",
        "findings": [],
        "changes": [],
        "trace": trace(
            ("TRIGGER", "project-governance", "Conflicting active authorities detected"),
            ("KNOWLEDGE_SYNC", "govern-project-docs", "Authority cannot be resolved safely"),
        ),
        "mutation_attempted": False,
        "closure": "OPEN(authority conflict)",
        "evidence": ["ADR-001 and ADR-014 are both active canonical"],
    }
elif "docs/current/state.md" in fixture_files:
    result = {
        "event": "E1",
        "assigned_to": "architecture-governance",
        "decision": "RECONSIDER duplicate state owner",
        "findings": [],
        "changes": [],
        "trace": trace(
            ("TRIGGER", "project-governance", "Persistent duplicate owner proposal detected"),
            ("SHOULD", "architecture-governance", "RECONSIDER duplicate state owner"),
        ),
        "mutation_attempted": False,
        "closure": "OPEN(reconsider)",
        "evidence": ["docs/current/state.md declares a sole owner"],
    }
elif "src/legacy_adapter.py" in fixture_files:
    findings = [{
        "type": "obsolete-artifact",
        "scope": "OrderLegacyAdapter",
        "expected": "Artifacts from superseded compatibility decisions should not remain active without a current basis",
        "observed": "OrderLegacyAdapter remains in src while ADR-003 is superseded",
        "claim": "OrderLegacyAdapter may be residue from a superseded decision",
        "evidence": "Current service documentation omits the adapter and ADR-003 is superseded",
        "confidence": "medium",
        "next_validation": "Check static/dynamic consumers, contracts, state, and compatibility obligations",
    }]
    result = {
        "event": "E3",
        "assigned_to": "complexity-audit",
        "decision": "AUDIT produced a governance-residue FINDING",
        "findings": findings,
        "changes": [],
        "trace": trace(
            ("TRIGGER", "project-governance", "Governance audit requested"),
            ("DID_IT", "complexity-audit", "Produced one falsifiable finding"),
            ("CLOSURE", "project-governance", "Audit request completed"),
        ),
        "mutation_attempted": False,
        "closure": "CLOSED",
        "evidence": ["ADR-003"],
    }
else:
    result = {
        "event": "NO_GOVERNANCE",
        "assigned_to": "none",
        "decision": "NO_GOVERNANCE",
        "findings": [],
        "changes": [],
        "trace": trace(
            ("TRIGGER", "none", "No long-term project-evolution signal"),
            ("CLOSURE", "none", "CLOSED without governance"),
        ),
        "mutation_attempted": False,
        "closure": "CLOSED",
        "evidence": ["ambient trigger fast path"],
    }

output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
