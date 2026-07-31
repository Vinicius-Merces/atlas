from __future__ import annotations

import argparse
import json
from pathlib import Path


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
        default="completed",
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
    return result


def main() -> None:
    args = parser().parse_args()
    envelope_path = Path(args.task_envelope).resolve()
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
    output = (
        Path(args.output).resolve()
        if args.output
        else envelope_path.with_suffix(".execution-result.json")
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
