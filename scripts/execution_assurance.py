"""Deterministic admission gates. Never execute supplied commands or skill code."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/execution-assurance.schema.json"
DATA_CLASSES = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}


def validate(data: dict) -> None:
    Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker()).validate(data)


def project_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Evidence/source path must be project relative")
    candidate = root / path
    if any(part.is_symlink() for part in [candidate, *candidate.parents] if part != root.parent):
        raise ValueError("Symlink evidence/source is not accepted")
    if not candidate.resolve().is_relative_to(root.resolve()) or not candidate.is_file():
        raise ValueError("Evidence/source unavailable in project")
    if any(p == '.git' or p == '.env' or p.startswith('.env.') for p in path.parts) or path.suffix in {'.pem', '.key'}:
        raise ValueError("Sensitive evidence/source path is not accepted")
    return candidate


def artifact(root: Path, record: dict) -> None:
    path = project_file(root, record["path"])
    if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
        raise ValueError("Evidence/source hash mismatch")


def security(data: dict, root: Path) -> dict:
    validate(data)
    if data["kind"] != "security":
        raise ValueError("Expected security manifest")
    artifact(root, {"path": data["source"], "sha256": data["source_sha256"]})
    # Source is a reviewed immutable archive/file, not only SKILL.md. Runtime
    # must hash the complete skill bundle, including scripts/dependencies.
    if data["trust"] not in {"internal", "verified-external"} or not data["approved"]:
        raise ValueError("Source lacks reviewed approval")
    if not set(data["permissions"]) <= set(data["approved_permissions"]):
        raise ValueError("Requested permissions exceed approved scope")
    if not data["sandbox"]["enforced"]:
        raise ValueError("Sandbox enforcement evidence is required")
    artifact(root, data["sandbox"]["receipt"])
    checks = data["checks"]
    if {c["type"] for c in checks} != {"secrets", "dependencies"} or len(checks) != 2:
        raise ValueError("Exactly one secrets and dependencies check is required")
    for check in checks:
        if check["status"] != "passed" or check["source_sha256"] != data["source_sha256"]:
            raise ValueError("Security check failed, unavailable, or for another source")
        artifact(root, check["evidence"])
    return {"outcome": "admitted", "kind": "security", "source_sha256": data["source_sha256"]}


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True,
                          text=True, timeout=30).stdout.strip()


def delivery(data: dict, root: Path, task_id: str, verify_remote: bool,
             receipt_paths: set[str] | None = None) -> dict:
    validate(data)
    if data["kind"] != "delivery" or data["task_id"] != task_id:
        raise ValueError("Delivery manifest belongs to another task")
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise ValueError("Explicit project root must be the Git root")
    if git(root, "rev-parse", "HEAD") != data["commit"]:
        raise ValueError("Delivery evidence is for another commit")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Tracked changes have not been checkpointed")
    allowed = set(receipt_paths or ())
    allowed.update(c["evidence"]["path"] for c in data["acceptance"])
    if "deployment_evidence" in data:
        allowed.add(data["deployment_evidence"]["path"])
    untracked = set(filter(None, git(root, "ls-files", "--others", "--exclude-standard", "-z").split('\0')))
    if untracked - allowed:
        raise ValueError("Untracked implementation files have not been checkpointed")
    if data["pending"] or any(c["status"] != "passed" for c in data["acceptance"]):
        raise ValueError("Pending work or acceptance checks prevent completion")
    if not any(c["functional"] for c in data["acceptance"]):
        raise ValueError("Functional evidence is required; structural validation is insufficient")
    for check in data["acceptance"]:
        artifact(root, check["evidence"])
    if data["deployment"] == "not-verified":
        raise ValueError("Requested deployment remains unverified")
    if data["deployment"] == "verified":
        if "deployment_evidence" not in data:
            raise ValueError("Deployment evidence is required")
        artifact(root, data["deployment_evidence"])
    if not verify_remote:
        raise ValueError("Remote checkpoint not verified; use --verify-remote when authorized")
    remote = data["remote"]
    git(root, "remote", "get-url", remote["name"])
    git(root, "check-ref-format", remote["ref"])
    observed = git(root, "ls-remote", "--exit-code", remote["name"], remote["ref"]).split()
    if observed != [data["commit"], remote["ref"]]:
        raise ValueError("Remote checkpoint differs from delivery commit")
    return {"outcome": "admitted", "kind": "delivery", "task_id": task_id, "commit": data["commit"]}


def models(data: dict, *, profile: str, requires: set[str], data_class: str,
           allow_paid: bool, today: date | None = None) -> dict:
    validate(data)
    if data["kind"] != "models" or data_class not in DATA_CLASSES or not profile.strip() or not requires:
        raise ValueError("Model request must declare profile, capabilities and data class")
    today = today or date.today()
    admitted, rejected, seen = [], [], set()
    for model in data["models"]:
        key = (model["provider"], model["model"])
        if key in seen:
            raise ValueError("Duplicate provider/model inventory entry")
        seen.add(key)
        reason = None
        if model["status"] != "active":
            reason = "lifecycle-status"
        elif not date.fromisoformat(model["verified_on"]) <= today <= date.fromisoformat(model["valid_until"]):
            reason = "stale-or-future-verification"
        elif "retirement_on" in model and today >= date.fromisoformat(model["retirement_on"]):
            reason = "retired"
        elif not requires <= set(model["capabilities"]) or profile not in model["profiles"]:
            reason = "capability-or-evaluation"
        elif DATA_CLASSES[data_class] > DATA_CLASSES[model["max_data_class"]]:
            reason = "privacy"
        elif model["financial_class"] == "paid" and not allow_paid:
            reason = "paid-not-authorized"
        entry = {"provider": key[0], "model": key[1]}
        if reason:
            rejected.append({**entry, "reason": reason})
        else:
            admitted.append(entry)
    return {"outcome": "admitted" if admitted else "blocked", "kind": "models",
            "as_of": today.isoformat(), "eligible": admitted, "rejected": rejected}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--task-id")
    parser.add_argument("--verify-remote", action="store_true")
    parser.add_argument("--profile")
    parser.add_argument("--requires", action="append", default=[])
    parser.add_argument("--data-class", choices=list(DATA_CLASSES), default="public")
    parser.add_argument("--allow-paid", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text())
        validate(data)
        root = args.project_root.resolve(strict=True)
        if data["kind"] == "security":
            result = security(data, root)
        elif data["kind"] == "delivery":
            manifest = args.manifest.resolve(strict=True).relative_to(root).as_posix()
            result = delivery(data, root, args.task_id, args.verify_remote, {manifest})
        else:
            result = models(data, profile=args.profile or "", requires=set(args.requires),
                            data_class=args.data_class, allow_paid=args.allow_paid)
        print(json.dumps(result, indent=2))
        if result["outcome"] != "admitted":
            raise SystemExit(1)
    except (ValueError, OSError, ValidationError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"Execution assurance blocked: {type(exc).__name__}") from None


if __name__ == "__main__":
    main()
