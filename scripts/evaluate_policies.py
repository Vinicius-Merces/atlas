from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]


def command_check(root: Path, script: str, *args: str) -> tuple[bool, Any, list[str]]:
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / script), *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, {"command": script, "output": output}, (
        [] if result.returncode == 0 else [output or f"{script} failed"]
    )


def version_consistency(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "manage_version.py", "--root", str(root))


def codex_integrity(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "validate_codex_adapter.py")


def runtime_drift(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "detect_runtime_drift.py")


def source_of_truth(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "validate_source_of_truth.py")


def schema_integrity(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "validate_schemas.py")


def package_structure(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "validate_package.py")


def policy_exceptions(root: Path) -> tuple[bool, Any, list[str]]:
    return command_check(root, "validate_policy_exceptions.py", "--root", str(root))


def ci_integrity(root: Path) -> tuple[bool, Any, list[str]]:
    try:
        import yaml
    except ImportError:
        return False, {}, ["PyYAML is required; install requirements-test.txt"]

    path = root / ".github" / "workflows" / "validate.yml"
    if not path.is_file():
        return False, {"path": path.as_posix()}, ["Validation workflow is missing"]
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        return False, {"path": path.as_posix()}, [f"Invalid CI YAML: {exc}"]

    findings: list[str] = []
    jobs = data.get("jobs", {}) if isinstance(data, dict) else {}
    validate = jobs.get("validate", {}) if isinstance(jobs, dict) else {}
    steps = validate.get("steps", []) if isinstance(validate, dict) else []
    if not isinstance(steps, list):
        findings.append("jobs.validate.steps must be an array")
        steps = []
    rendered = json.dumps(steps)
    for required in [
        "actions/checkout@",
        "actions/setup-python@",
        "validate_registry.py",
        "validate_codex_adapter.py",
        "evaluate_policies.py",
        "pytest tests -q",
    ]:
        if required not in rendered:
            findings.append(f"CI is missing required step content: {required}")
    return not findings, {"path": path.relative_to(root).as_posix()}, findings


def hidden_directory_mapping(root: Path) -> tuple[bool, Any, list[str]]:
    path = root / "PATCH-MANIFEST.json"
    if not path.is_file():
        return True, {"applicable": False}, []
    manifest = json.loads(path.read_text(encoding="utf-8"))
    findings: list[str] = []
    mappings = manifest.get("directory_mappings", {})
    if mappings.get("CLAUDE-DIRECTORY") != ".claude":
        findings.append("PATCH-MANIFEST has no CLAUDE-DIRECTORY -> .claude mapping")
    for item in manifest.get("files", []):
        target = item.get("target_path", item.get("path", ""))
        package = item.get("package_path", item.get("path", ""))
        operation = item.get("operation")
        if operation not in {"add", "replace", "delete"}:
            findings.append(f"Invalid patch operation: {operation}")
        if (
            target.startswith(".claude/")
            and operation != "delete"
            and not package.startswith("CLAUDE-DIRECTORY/")
        ):
            findings.append(f"Invalid .claude package mapping: {package} -> {target}")
    return not findings, {"manifest": "PATCH-MANIFEST.json"}, findings


def markdown_paths(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return set(re.findall(r"- `([^`]+)`", path.read_text(encoding="utf-8")))


def deletion_safety(root: Path) -> tuple[bool, Any, list[str]]:
    manifest_path = root / "PATCH-MANIFEST.json"
    list_path = root / "FILES-TO-DELETE.md"
    if not manifest_path.is_file():
        return True, {"applicable": False}, []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_deletions = {
        item.get("target_path", item.get("path", ""))
        for item in manifest.get("files", [])
        if item.get("operation") == "delete"
    }
    listed_deletions = markdown_paths(list_path)
    findings: list[str] = []
    if manifest_deletions != listed_deletions:
        findings.append(
            "Manifest deletions do not exactly match FILES-TO-DELETE.md"
        )
    for item in manifest.get("files", []):
        if item.get("operation") == "delete" and item.get("sha256"):
            findings.append(
                f"Delete operation must not carry a payload hash: {item.get('path')}"
            )
    evidence = {
        "manifest_deletions": sorted(manifest_deletions),
        "listed_deletions": sorted(listed_deletions),
    }
    return not findings, evidence, findings


def manual_patch_base(root: Path) -> tuple[bool, Any, list[str]]:
    path = root / "PATCH-MANIFEST.json"
    if not path.is_file():
        return True, {"applicable": False}, []
    manifest = json.loads(path.read_text(encoding="utf-8"))
    source = manifest.get("from_version")
    target = manifest.get("to_version")
    findings = [] if source and target and source != target else [
        "Patch must declare distinct from_version and to_version"
    ]
    return not findings, {
        "evaluation_scope": "repository",
        "from_version": source,
        "to_version": target,
        "deployment_check": "deferred to manual_deploy_preflight.py",
    }, findings


def repository_cleanliness(root: Path) -> tuple[bool, Any, list[str]]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        capture_output=True,
    )
    if result.returncode:
        return False, {}, ["git ls-files failed"]
    paths = [
        item.decode("utf-8").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    ]
    forbidden_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist"}
    forbidden_roots = {
        ".atlas/audit",
        ".atlas/evidence",
        ".atlas/deployments",
        ".atlas/policy/policy-report.json",
    }
    secret_names = {".env", "id_rsa", "id_ed25519"}
    findings = []
    for path in paths:
        parts = set(Path(path).parts)
        if parts & forbidden_parts:
            findings.append(path)
        if any(path == root_name or path.startswith(root_name + "/") for root_name in forbidden_roots):
            findings.append(path)
        if Path(path).name in secret_names or Path(path).suffix.lower() in {".pem", ".key"}:
            findings.append(path)
    return not findings, {"candidate_files": len(paths)}, sorted(set(findings))


def support_policy(root: Path) -> tuple[bool, Any, list[str]]:
    claude = json.loads(
        (root / "adapters/claude/runtime-declaration.json").read_text(encoding="utf-8")
    )
    codex = json.loads(
        (root / "adapters/codex/runtime-declaration.json").read_text(encoding="utf-8")
    )
    policy = (root / "compatibility/support-policy.md").read_text(encoding="utf-8")
    matrix = (root / "compatibility/runtime-matrix.md").read_text(encoding="utf-8")
    findings = []
    if not (
        claude.get("canonical") is True
        and claude.get("support") == "beta-supported"
    ):
        findings.append("Claude Code declaration is not canonical beta-supported")
    if not (
        codex.get("canonical") is False
        and codex.get("support") == "beta-supported"
    ):
        findings.append("Codex declaration is not beta-supported compatibility")
    for phrase in [
        "canonical beta-supported runtime",
        "Codex",
        "Gemini",
        "Cursor",
    ]:
        if phrase not in policy:
            findings.append(f"Support policy is missing: {phrase}")
    for runtime in ["Claude Code", "Codex", "Gemini", "Cursor"]:
        if runtime not in matrix:
            findings.append(f"Runtime matrix is missing: {runtime}")
    return not findings, {
        "claude": claude.get("support"),
        "codex": codex.get("support"),
    }, findings


def stable_release_gate(root: Path) -> tuple[bool, Any, list[str]]:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        return True, {"applicable": False, "version": version}, []
    findings = []
    checklist = root / "release" / "STABLE-RELEASE-CHECKLIST.md"
    if not checklist.is_file():
        findings.append("Stable release checklist is missing")
    elif "- [ ]" in checklist.read_text(encoding="utf-8"):
        findings.append("Stable release checklist is incomplete")
    manifest = json.loads(
        (root / "release" / "manifest.json").read_text(encoding="utf-8")
    )
    if manifest.get("version") != version:
        findings.append("Stable release manifest version is stale")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## {version}" not in changelog:
        findings.append("Stable version is missing from CHANGELOG.md")
    return not findings, {"applicable": True, "version": version}, findings


EVALUATORS: dict[str, Callable[[Path], tuple[bool, Any, list[str]]]] = {
    "version_consistency": version_consistency,
    "codex_integrity": codex_integrity,
    "runtime_drift": runtime_drift,
    "source_of_truth": source_of_truth,
    "schema_integrity": schema_integrity,
    "package_structure": package_structure,
    "policy_exceptions": policy_exceptions,
    "ci_integrity": ci_integrity,
    "hidden_directory_mapping": hidden_directory_mapping,
    "deletion_safety": deletion_safety,
    "manual_patch_base": manual_patch_base,
    "repository_cleanliness": repository_cleanliness,
    "support_policy": support_policy,
    "stable_release_gate": stable_release_gate,
}


def approved_exceptions(root: Path) -> dict[str, dict[str, Any]]:
    exception_root = root / ".atlas" / "policy" / "exceptions"
    approved: dict[str, dict[str, Any]] = {}
    if not exception_root.exists():
        return approved
    now = datetime.now(timezone.utc)
    for path in sorted(exception_root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") != "approved":
            continue
        expires = datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires > now:
            approved[data["policy_id"]] = data
    return approved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    policies = []
    for path in sorted((root / "policies").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        required = {
            "policy_id",
            "evaluator",
            "description",
            "severity",
            "condition",
            "evidence",
            "remediation",
        }
        missing = required - data.keys()
        if missing:
            raise SystemExit(
                f"{path}: missing policy fields {', '.join(sorted(missing))}"
            )
        policies.append(data)

    exceptions = approved_exceptions(root)
    results = []
    for policy in policies:
        evaluator = EVALUATORS.get(policy["evaluator"])
        if evaluator is None:
            passed, evidence, findings = False, {}, [
                f"Unknown evaluator: {policy['evaluator']}"
            ]
        else:
            passed, evidence, findings = evaluator(root)

        outcome = "passed"
        exception = None
        if not passed:
            exception = exceptions.get(policy["policy_id"])
            if exception and policy["policy_id"] != "atlas.policy.exception-validity":
                outcome = "approval"
            elif policy["severity"] == "blocking":
                outcome = "blocked"
            elif policy["severity"] == "approval":
                outcome = "approval"
            else:
                outcome = "warning"

        results.append(
            {
                "policy_id": policy["policy_id"],
                "outcome": outcome,
                "evidence": evidence,
                "findings": findings,
                "remediation": policy["remediation"],
                "exception_id": exception.get("exception_id") if exception else None,
            }
        )

    summary = {
        outcome: sum(1 for result in results if result["outcome"] == outcome)
        for outcome in ["passed", "warning", "approval", "blocked"]
    }
    report = {
        "framework_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": summary,
    }
    output = (
        Path(args.output)
        if args.output
        else root / ".atlas" / "policy" / "policy-report.json"
    )
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(output)
    print(
        "Policy summary: "
        + ", ".join(f"{key}={value}" for key, value in summary.items())
    )
    if summary["blocked"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
