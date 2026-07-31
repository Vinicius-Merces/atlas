from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


def run(
    script: str, *args: str, expected: int = 0
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    return result


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate(instance: Path, schema_name: str) -> None:
    schema = load(ROOT / "schemas" / schema_name)
    Draft202012Validator(schema).validate(load(instance))


def test_complete_runtime_and_evidence_lifecycle(tmp_path: Path) -> None:
    workspace = tmp_path / "atlas-e2e"
    continuity = workspace / ".atlas" / "continuity"
    evidence_dir = workspace / ".atlas" / "evidence"
    deployments = workspace / ".atlas" / "deployments"
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    workspace.mkdir()
    (workspace / "VERSION").write_text(version + "\n", encoding="utf-8")

    task = workspace / "task.json"
    run(
        "atlas_route.py",
        "--task-type",
        "feature",
        "--summary",
        "Exercise the complete portable runtime lifecycle",
        "--output",
        str(task),
    )
    task_data = load(task)
    task_data["supporting_roles"] = ["qa-engineer"]
    write(task, task_data)
    run("validate_task_envelope.py", str(task))
    validate(task, "task-envelope.schema.json")

    context = workspace / "context.md"
    run(
        "build_context_pack.py",
        "--task-envelope",
        str(task),
        "--output",
        str(context),
    )
    context_manifest = context.with_suffix(".manifest.json")
    validate(context_manifest, "context-pack-manifest.schema.json")
    task_data["context_pack"] = str(context)
    write(task, task_data)

    execution_plan = workspace / "execution-plan.json"
    run(
        "build_execution_plan.py",
        "--task-envelope",
        str(task),
        "--runtime",
        "codex",
        "--output",
        str(execution_plan),
    )
    validate(execution_plan, "runtime-execution-plan.schema.json")

    checkpoint = continuity / "checkpoint.json"
    run(
        "create_checkpoint.py",
        "--task-envelope",
        str(task),
        "--runtime",
        "codex",
        "--output",
        str(checkpoint),
    )
    validate(checkpoint, "checkpoint.schema.json")

    handoff = continuity / "handoff.json"
    run(
        "create_handoff.py",
        "--checkpoint",
        str(checkpoint),
        "--to-runtime",
        "claude-code",
        "--output",
        str(handoff),
    )
    run("validate_handoff.py", str(handoff))
    validate(handoff, "handoff-manifest.schema.json")

    continuation = continuity / "continuation.json"
    run(
        "build_continuation_plan.py",
        "--handoff",
        str(handoff),
        "--output",
        str(continuation),
    )
    validate(continuation, "continuation-plan.schema.json")

    parallel = workspace / "parallel.json"
    run(
        "create_workstreams.py",
        "--task-envelope",
        str(task),
        "--output",
        str(parallel),
    )
    parallel_data = load(parallel)
    assert len(parallel_data["workstreams"]) == 2

    workstream_paths = []
    claim_paths = []
    resources = ["src/shared", "src/shared/component.py"]
    for index, workstream in enumerate(parallel_data["workstreams"]):
        workstream_path = workspace / f"workstream-{index}.json"
        write(workstream_path, workstream)
        workstream_paths.append(workstream_path)
        claim_path = workspace / f"claim-{index}.json"
        run(
            "claim_resources.py",
            "--workstream",
            str(workstream_path),
            "--mode",
            "exclusive",
            "--resource",
            resources[index],
            "--output",
            str(claim_path),
        )
        claim_paths.append(claim_path)
        validate(claim_path, "resource-claim.schema.json")

    parallel_data["claims"] = [load(path) for path in claim_paths]
    write(parallel, parallel_data)
    conflict = run(
        "detect_workstream_conflicts.py",
        "--manifest",
        str(parallel),
        expected=1,
    )
    assert '"severity": "blocking"' in conflict.stdout

    parallel_data["claims"][1]["resources"] = ["tests/runtime"]
    for index, workstream in enumerate(parallel_data["workstreams"]):
        workstream["status"] = "completed"
        workstream["changed_files"] = [f"artifact-{index}.txt"]
        workstream["remaining_risks"] = []
    parallel_data["conflicts"] = []
    parallel_data["status"] = "completed"
    write(parallel, parallel_data)
    run("detect_workstream_conflicts.py", "--manifest", str(parallel))
    run("validate_merge_readiness.py", "--manifest", str(parallel))
    validate(parallel, "parallel-execution-manifest.schema.json")
    for workstream in parallel_data["workstreams"]:
        workstream_path = workspace / f"{workstream['workstream_id']}.json"
        write(workstream_path, workstream)
        validate(workstream_path, "workstream.schema.json")

    reconciliation = workspace / "reconciliation.json"
    run(
        "build_reconciliation_report.py",
        "--manifest",
        str(parallel),
        "--output",
        str(reconciliation),
    )
    assert load(reconciliation)["outcome"] == "ready"
    validate(reconciliation, "reconciliation-report.schema.json")

    reconciliation_data = load(reconciliation)
    execution_result = workspace / "execution-result.json"
    write(
        execution_result,
        {
            "task_id": task_data["id"],
            "runtime": "codex",
            "status": "completed",
            "summary": "Portable runtime lifecycle completed",
            "changed_files": reconciliation_data["changed_files"],
            "validation": reconciliation_data["combined_validation"],
            "reviews": reconciliation_data["combined_reviews"],
            "assumptions": [],
            "remaining_risks": [],
        },
    )
    run("validate_execution_result.py", str(execution_result))
    validate(execution_result, "execution-result.schema.json")

    evidence = evidence_dir / "evidence.json"
    run(
        "create_evidence_record.py",
        "--task-id",
        task_data["id"],
        "--runtime",
        "codex",
        "--status",
        "completed",
        "--output",
        str(evidence),
    )
    validate(evidence, "evidence-record.schema.json")

    patch = workspace / "patch"
    patch.mkdir()
    (patch / "FILES-TO-ADD.md").write_text(
        "# Files to add\n\n- `new-file.txt`\n", encoding="utf-8"
    )
    (patch / "FILES-TO-REPLACE.md").write_text(
        "# Files to replace\n\n- `VERSION`\n", encoding="utf-8"
    )
    (patch / "FILES-TO-DELETE.md").write_text(
        "# Files to delete\n\n", encoding="utf-8"
    )
    receipt = deployments / "receipt.json"
    run(
        "record_manual_deploy.py",
        "--from-version",
        "0.1.0-beta.10",
        "--to-version",
        version,
        "--patch",
        "atlas-e2e-incremental.zip",
        "--patch-root",
        str(patch),
        "--output",
        str(receipt),
    )
    validate(receipt, "manual-deployment-receipt.schema.json")

    bundle = workspace / ".atlas" / "audit" / "audit-bundle.json"
    run("build_audit_bundle.py", "--root", str(workspace))
    validate(bundle, "audit-bundle-manifest.schema.json")
    run("verify_evidence_integrity.py", "--root", str(workspace))
    assert load(bundle)["integrity"]["record_count"] >= 5

    evidence.write_text("{}\n", encoding="utf-8")
    tampered = run(
        "verify_evidence_integrity.py",
        "--root",
        str(workspace),
        expected=1,
    )
    assert "Hash mismatch" in tampered.stdout
