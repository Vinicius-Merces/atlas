from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path

from execution_assurance import delivery, git


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Record a portable ATLAS execution result for a routed task. "
            "Repeat list options to preserve concrete execution evidence."
        )
    )
    result.add_argument("--task-envelope", required=True)
    result.add_argument(
        "--runtime",
        choices=("claude-code", "codex"),
        required=True,
    )
    result.add_argument(
        "--status",
        choices=("completed", "partial", "blocked", "failed"),
        default="partial",
    )
    result.add_argument("--summary", required=True)
    result.add_argument("--changed-file", action="append", default=[])
    result.add_argument("--validation", action="append", default=[])
    result.add_argument("--review", action="append", default=[])
    result.add_argument("--finding", action="append", default=[])
    result.add_argument("--assumption", action="append", default=[])
    result.add_argument("--remaining-risk", action="append", default=[])
    result.add_argument("--knowledge-update", action="append", default=[])
    result.add_argument("--output")
    result.add_argument("--delivery-evidence", type=Path)
    result.add_argument("--project-root", type=Path)
    result.add_argument("--verify-remote", action="store_true")
    return result


def main() -> None:
    args = parser().parse_args()
    envelope_path = Path(args.task_envelope).resolve()
    output = Path(args.output).resolve() if args.output else envelope_path.with_suffix(".execution-result.json")
    if args.project_root:
        root = args.project_root.resolve(strict=True)
        if not envelope_path.is_relative_to(root) or not output.is_relative_to(root):
            raise SystemExit("Task envelope and result must remain in the explicit project root")
    try:
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        task_id = envelope["id"]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        raise SystemExit(f"Invalid task envelope: {exc}") from None

    record = {
        "task_id": task_id,
        "runtime": args.runtime,
        "status": args.status,
        "summary": args.summary,
        "changed_files": list(dict.fromkeys(args.changed_file)),
        "validation": list(dict.fromkeys(args.validation)),
        "reviews": list(dict.fromkeys(args.review)),
        "findings": list(dict.fromkeys(args.finding)),
        "assumptions": list(dict.fromkeys(args.assumption)),
        "remaining_risks": list(dict.fromkeys(args.remaining_risk)),
        "knowledge_updates": list(dict.fromkeys(args.knowledge_update)),
    }
    if args.status == "completed":
        if not args.delivery_evidence or not args.project_root:
            raise SystemExit("Completed requires --delivery-evidence and explicit --project-root; otherwise record partial")
        from jsonschema.exceptions import ValidationError
        import subprocess
        try:
            root = args.project_root.resolve(strict=True)
            evidence_path = args.delivery_evidence.resolve(strict=True)
            evidence_path.relative_to(root)
            raw = evidence_path.read_bytes()
            evidence = json.loads(raw)
            protected = {envelope_path, evidence_path}
            for check in evidence.get("acceptance", []):
                protected.add((root / check["evidence"]["path"]).resolve())
            if "deployment_evidence" in evidence:
                protected.add((root / evidence["deployment_evidence"]["path"]).resolve())
            if output in protected or output.suffix != ".json":
                raise ValueError("Completion output must be a separate JSON result")
            if git(root, "ls-files", "--", output.relative_to(root).as_posix()):
                raise ValueError("Completion output must not modify an already tracked file")
            expected = set(envelope.get("acceptance_criteria", []))
            observed = {c["criterion"] for c in evidence.get("acceptance", [])}
            if not expected or expected != observed:
                raise ValueError("Acceptance evidence must exactly match task criteria")
            receipts = {path.relative_to(root).as_posix() for path in (evidence_path, envelope_path, output)}
            delivery(evidence, root, task_id, args.verify_remote, receipts)
            record["delivery_evidence"] = evidence_path.relative_to(root).as_posix()
            record["delivery_sha256"] = hashlib.sha256(raw).hexdigest()
        except (ValueError, OSError, KeyError, TypeError, ValidationError, subprocess.SubprocessError) as exc:
            raise SystemExit(f"Completion blocked: {type(exc).__name__}") from None
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
