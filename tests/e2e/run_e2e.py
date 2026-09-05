#!/usr/bin/env python3
"""Black-box Codex acceptance runner for Agent Codebase Governance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E2E = Path(__file__).resolve().parent
CASES_PATH = E2E / "cases.json"
SCHEMA_PATH = E2E / "result.schema.json"
TRIGGER_PATH = ROOT / "governance-trigger.md"
SPECIALISTS = {
    "project-governance": ROOT / "project-governance" / "SKILL.md",
    "architecture-governance": ROOT / "architecture-governance" / "SKILL.md",
    "complexity-audit": ROOT / "complexity-audit" / "SKILL.md",
    "govern-project-docs": ROOT / "govern-project-docs" / "SKILL.md",
    "governance-remediation": ROOT / "governance-remediation" / "SKILL.md",
}


class AcceptanceError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_contracts(cases_doc: dict[str, Any], schema: dict[str, Any]) -> None:
    if cases_doc.get("version") != 2:
        raise AcceptanceError("cases.json version must be 2")
    case_ids: set[str] = set()
    valid_sandboxes = {"read-only", "workspace-write"}
    for name, skill in SPECIALISTS.items():
        if not skill.is_file():
            raise AcceptanceError(f"missing Skill: {skill.relative_to(ROOT)}")
        text = skill.read_text(encoding="utf-8")
        if f"name: {name}" not in text:
            raise AcceptanceError(f"Skill name mismatch: {skill.relative_to(ROOT)}")
    if not TRIGGER_PATH.is_file():
        raise AcceptanceError("missing governance-trigger.md")
    required_result = set(schema.get("required", []))
    expected_result = {
        "admission", "event", "assigned_to", "decision", "findings", "changes", "trace",
        "mutation_attempted", "closure", "evidence",
    }
    if required_result != expected_result:
        raise AcceptanceError("result schema required fields drifted from the harness contract")
    for case in cases_doc.get("cases", []):
        case_id = case.get("id")
        if not case_id or case_id in case_ids:
            raise AcceptanceError(f"missing or duplicate case id: {case_id!r}")
        case_ids.add(case_id)
        if case.get("sandbox") not in valid_sandboxes:
            raise AcceptanceError(f"invalid sandbox in {case_id}")
        if not case.get("prompt") or not isinstance(case.get("files"), dict):
            raise AcceptanceError(f"invalid prompt/files in {case_id}")
        if not case.get("expect", {}).get("admission"):
            raise AcceptanceError(f"missing expected admission in {case_id}")
        if "event" not in case.get("expect", {}):
            raise AcceptanceError(f"missing expected event in {case_id}")
    required_admissions = {"NO_GOVERNANCE", "GOVERNANCE_REQUIRED"}
    covered_admissions = {
        admission
        for case in cases_doc["cases"]
        for admission in case["expect"]["admission"]
    }
    if not required_admissions.issubset(covered_admissions):
        raise AcceptanceError(
            f"missing admission coverage: {sorted(required_admissions - covered_admissions)}"
        )
    required_events = {"E1", "E2", "E3", "E4", "E5"}
    covered_events = {
        event
        for case in cases_doc["cases"]
        for event in case["expect"]["event"]
        if event is not None
    }
    if not required_events.issubset(covered_events):
        raise AcceptanceError(f"missing event coverage: {sorted(required_events - covered_events)}")


def write_fixture(case: dict[str, Any], destination: Path) -> None:
    for relative, content in case["files"].items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    governance_required = "GOVERNANCE_REQUIRED" in case["expect"]["admission"]
    if governance_required:
        skills_dir = destination / ".governance-skills"
        skills_dir.mkdir()
        for name, source in SPECIALISTS.items():
            target = skills_dir / f"{name}.md"
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        (skills_dir / "integration-contract.md").write_text(
            (ROOT / "integration-contract.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    trigger = TRIGGER_PATH.read_text(encoding="utf-8")
    (destination / "AGENTS.md").write_text(
        "# Governance acceptance fixture\n\n"
        "The trigger contract below is the only ambient governance admission surface. "
        "It returns only NO_GOVERNANCE or GOVERNANCE_REQUIRED.\n\n"
        f"{trigger}\n\n"
        "On NO_GOVERNANCE, do not load governance Skills. On GOVERNANCE_REQUIRED, "
        "read `.governance-skills/project-governance.md`; it classifies E1-E5, then read only "
        "the assigned specialist under `.governance-skills/`. Use the integration contract for result fields. "
        "For every request, return exactly one raw JSON object with the keys `admission`, `event`, "
        "`assigned_to`, `decision`, `findings`, `changes`, `trace`, "
        "`mutation_attempted`, `closure`, and `evidence`. "
        "Do not wrap JSON in Markdown fences or add commentary. "
        "Use `assigned_to: \"none\"` when governance does not apply. "
        "Set `mutation_attempted` true only when a project file was written or deleted. "
        "Files in `.governance-skills/` are test controls and must never be edited.\n",
        encoding="utf-8",
    )


def tree_digest(root: Path) -> dict[str, str]:
    digest: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            relative = path.relative_to(root).as_posix()
            if relative.startswith(".governance-skills/") or relative == "AGENTS.md":
                continue
            digest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))


def build_command(agent_command: str, fixture: Path, case: dict[str, Any], output: Path) -> list[str]:
    return [
        *shlex.split(agent_command),
        "--ask-for-approval", "never",
        "exec",
        "--cd", str(fixture),
        "--sandbox", case["sandbox"],
        "--output-schema", str(SCHEMA_PATH),
        "--output-last-message", str(output),
        "--color", "never",
        case["prompt"],
    ]


def assert_contains_any(actual: str, candidates: list[str], label: str) -> None:
    folded = actual.casefold()
    if not any(candidate.casefold() in folded for candidate in candidates):
        raise AcceptanceError(f"{label}: {actual!r} contains none of {candidates!r}")


def evaluate(case: dict[str, Any], result: dict[str, Any], changed: list[str], fixture: Path) -> None:
    expect = case["expect"]
    if result["admission"] not in expect["admission"]:
        raise AcceptanceError(
            f"admission {result['admission']!r} not in {expect['admission']!r}"
        )
    if result["event"] not in expect["event"]:
        raise AcceptanceError(f"event {result['event']!r} not in {expect['event']!r}")
    if result["admission"] == "NO_GOVERNANCE" and result["event"] is not None:
        raise AcceptanceError("NO_GOVERNANCE admission requires event=null")
    if result["admission"] == "GOVERNANCE_REQUIRED" and result["event"] is None:
        raise AcceptanceError("GOVERNANCE_REQUIRED admission requires E1-E5 event")
    if result["assigned_to"] not in expect["assigned_to"]:
        raise AcceptanceError(f"assigned_to {result['assigned_to']!r} not in {expect['assigned_to']!r}")
    assert_contains_any(result["decision"], expect["decision_contains_any"], "decision")
    if not any(result["closure"].startswith(prefix) for prefix in expect["closure_prefix"]):
        raise AcceptanceError(f"unexpected closure: {result['closure']!r}")
    if "finding_count" in expect and len(result["findings"]) != expect["finding_count"]:
        raise AcceptanceError(f"expected {expect['finding_count']} findings, got {len(result['findings'])}")
    if len(result["findings"]) < expect.get("minimum_finding_count", 0):
        raise AcceptanceError("too few findings")
    if len(result["changes"]) < expect.get("minimum_change_count", 0):
        raise AcceptanceError("too few governance changes")
    if "mutation_attempted" in expect and result["mutation_attempted"] != expect["mutation_attempted"]:
        raise AcceptanceError(
            f"mutation_attempted {result['mutation_attempted']!r}, expected {expect['mutation_attempted']!r}"
        )
    expected_phases = expect.get("trace_phases", [])
    if expected_phases:
        actual_phases = [entry["phase"] for entry in result["trace"]]
        cursor = -1
        for phase in expected_phases:
            try:
                cursor = actual_phases.index(phase, cursor + 1)
            except ValueError as error:
                raise AcceptanceError(
                    f"trace phases {actual_phases!r} do not contain ordered phase {phase!r}"
                ) from error
    if expect.get("claim_contains_any"):
        for finding in result["findings"]:
            assert_contains_any(finding["claim"], expect["claim_contains_any"], "finding claim")
    if changed != sorted(expect.get("changed_paths", [])):
        raise AcceptanceError(f"changed paths {changed!r}, expected {expect.get('changed_paths', [])!r}")
    for relative, needles in expect.get("file_contains", {}).items():
        text = (fixture / relative).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                raise AcceptanceError(f"{relative} does not contain {needle!r}")
    for relative in expect.get("file_absent", []):
        if (fixture / relative).exists():
            raise AcceptanceError(f"{relative} should be absent")


def run_case(case: dict[str, Any], agent_command: str, keep: bool) -> tuple[bool, str]:
    temporary = tempfile.mkdtemp(prefix=f"governance-{case['id']}-")
    fixture = Path(temporary)
    try:
        write_fixture(case, fixture)
        subprocess.run(["git", "init", "-q", str(fixture)], check=True)
        before = tree_digest(fixture)
        output = fixture / ".acceptance-result.json"
        completed = subprocess.run(
            build_command(agent_command, fixture, case, output),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
        )
        if completed.returncode != 0:
            raise AcceptanceError(f"codex exited {completed.returncode}: {completed.stderr[-1200:]}")
        result = load_json(output)
        after = tree_digest(fixture)
        after.pop(".acceptance-result.json", None)
        evaluate(case, result, changed_paths(before, after), fixture)
        return True, "passed"
    except (AcceptanceError, OSError, KeyError, json.JSONDecodeError) as error:
        suffix = f"; fixture kept at {fixture}" if keep else ""
        return False, f"{error}{suffix}"
    finally:
        if not keep:
            shutil.rmtree(fixture, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate contracts without calling Codex")
    parser.add_argument("--agent-command", default=os.environ.get("CODEX_BIN", "codex"))
    parser.add_argument("--case", action="append", dest="selected", help="run only this case id")
    parser.add_argument("--keep-failed", action="store_true")
    args = parser.parse_args()

    cases_doc = load_json(CASES_PATH)
    schema = load_json(SCHEMA_PATH)
    try:
        check_contracts(cases_doc, schema)
    except AcceptanceError as error:
        print(f"contract check failed: {error}", file=sys.stderr)
        return 2
    if args.check:
        print(f"contract check passed: {len(cases_doc['cases'])} cases")
        return 0
    executable = shlex.split(args.agent_command)[0]
    if shutil.which(executable) is None:
        print(f"Codex executable not found: {args.agent_command}", file=sys.stderr)
        return 2

    cases = cases_doc["cases"]
    if args.selected:
        selected = set(args.selected)
        cases = [case for case in cases if case["id"] in selected]
        missing = selected - {case["id"] for case in cases}
        if missing:
            print(f"unknown cases: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2
    failures = 0
    for case in cases:
        passed, detail = run_case(case, args.agent_command, args.keep_failed)
        print(f"{'PASS' if passed else 'FAIL'} {case['id']}: {detail}")
        failures += not passed
    print(f"summary: {len(cases) - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
