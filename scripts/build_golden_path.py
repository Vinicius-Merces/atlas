from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_NAMES = (
    "task-envelope.json",
    "context-pack.md",
    "context-pack.manifest.json",
    "execution-plan.json",
    "checkpoint.json",
    "handoff.json",
    "continuation-plan.json",
    "execution-result.json",
    "evidence.json",
    "golden-path-manifest.json",
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Generate a complete, non-destructive ATLAS runtime golden path. "
            "The generated execution plan still requires an AI agent or human "
            "to perform real implementation work."
        )
    )
    result.add_argument("--output-dir", required=True)
    result.add_argument(
        "--runtime",
        choices=("claude-code", "codex"),
        default="codex",
    )
    result.add_argument("--task-type", default="feature")
    result.add_argument(
        "--summary",
        default="Exercise the complete governed ATLAS runtime lifecycle",
    )
    result.add_argument(
        "--force",
        action="store_true",
        help="Overwrite only the known golden-path files in the output directory.",
    )
    return result


def run_script(name: str, *arguments: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        details = (result.stdout + result.stderr).strip()
        raise SystemExit(f"{name} failed: {details}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    args = parser().parse_args()
    output_dir = Path(args.output_dir).resolve()
    existing = [
        output_dir / name
        for name in OUTPUT_NAMES
        if (output_dir / name).exists()
    ]
    if existing and not args.force:
        rendered = ", ".join(path.name for path in existing)
        raise SystemExit(
            f"Refusing to overwrite existing golden-path files: {rendered}. "
            "Use --force to replace only these known outputs."
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    task = output_dir / "task-envelope.json"
    context = output_dir / "context-pack.md"
    plan = output_dir / "execution-plan.json"
    checkpoint = output_dir / "checkpoint.json"
    handoff = output_dir / "handoff.json"
    continuation = output_dir / "continuation-plan.json"
    execution_result = output_dir / "execution-result.json"
    evidence = output_dir / "evidence.json"

    run_script(
        "atlas_route.py",
        "--task-type",
        args.task_type,
        "--summary",
        args.summary,
        "--runtime",
        args.runtime,
        "--acceptance",
        "All generated lifecycle artifacts validate against their schemas",
        "--output",
        str(task),
    )
    run_script(
        "build_context_pack.py",
        "--task-envelope",
        str(task),
        "--output",
        str(context),
    )
    run_script(
        "build_execution_plan.py",
        "--task-envelope",
        str(task),
        "--runtime",
        args.runtime,
        "--output",
        str(plan),
    )
    run_script(
        "create_checkpoint.py",
        "--task-envelope",
        str(task),
        "--runtime",
        args.runtime,
        "--output",
        str(checkpoint),
    )
    to_runtime = "claude-code" if args.runtime == "codex" else "codex"
    run_script(
        "create_handoff.py",
        "--checkpoint",
        str(checkpoint),
        "--to-runtime",
        to_runtime,
        "--output",
        str(handoff),
    )
    run_script(
        "build_continuation_plan.py",
        "--handoff",
        str(handoff),
        "--output",
        str(continuation),
    )
    run_script(
        "record_execution_result.py",
        "--task-envelope",
        str(task),
        "--runtime",
        args.runtime,
        "--status",
        "completed",
        "--summary",
        "Golden-path artifact generation completed",
        "--validation",
        "schema-validation",
        "--review",
        "runtime-conformance-review",
        "--output",
        str(execution_result),
    )
    task_id = json.loads(task.read_text(encoding="utf-8"))["id"]
    run_script(
        "create_evidence_record.py",
        "--task-id",
        task_id,
        "--runtime",
        args.runtime,
        "--status",
        "completed",
        "--output",
        str(evidence),
    )

    for validator, artifact in (
        ("validate_task_envelope.py", task),
        ("validate_handoff.py", handoff),
        ("validate_execution_result.py", execution_result),
    ):
        run_script(validator, str(artifact))

    artifacts = [
        output_dir / name
        for name in OUTPUT_NAMES
        if name != "golden-path-manifest.json"
    ]
    manifest = {
        "framework_version": (ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip(),
        "task_id": task_id,
        "runtime": args.runtime,
        "execution_mode": "artifact-generation-only",
        "requires_external_execution": True,
        "artifacts": [
            {
                "path": path.name,
                "sha256": sha256(path),
            }
            for path in artifacts
        ],
    }
    manifest_path = output_dir / "golden-path-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(manifest_path)


if __name__ == "__main__":
    main()
