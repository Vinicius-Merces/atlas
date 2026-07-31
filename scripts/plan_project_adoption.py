from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from release_utils import canonical_release_bytes, source_payload


ROOT = Path(__file__).resolve().parents[1]
MERGE_REQUIRED_FILES = {
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
    "VERSION",
}
MERGE_REQUIRED_PREFIXES = {
    ".claude/memory/",
    ".github/",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def requires_merge(relative: str) -> bool:
    return relative in MERGE_REQUIRED_FILES or any(
        relative.startswith(prefix) for prefix in MERGE_REQUIRED_PREFIXES
    )


def classify(
    framework_root: Path, target_root: Path
) -> tuple[list[dict[str, object]], dict[str, int]]:
    operations: list[dict[str, object]] = []
    counts = {
        "copy": 0,
        "identical": 0,
        "merge-required": 0,
        "review-required": 0,
    }
    for relative, content in sorted(source_payload(framework_root).items()):
        target = target_root / Path(relative)
        if not target.exists():
            action = "copy"
            target_hash = None
        elif not target.is_file():
            action = "review-required"
            target_hash = None
        else:
            target_content = canonical_release_bytes(target.read_bytes())
            target_hash = digest(target_content)
            if target_content == content:
                action = "identical"
            elif requires_merge(relative):
                action = "merge-required"
            else:
                action = "review-required"

        counts[action] += 1
        operations.append(
            {
                "path": relative,
                "action": action,
                "framework_sha256": digest(content),
                "target_sha256": target_hash,
            }
        )
    return operations, counts


def render_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    if not isinstance(summary, dict):
        raise ValueError("Adoption report summary must be an object")
    lines = [
        "# ATLAS Project Adoption Plan",
        "",
        f"- Framework root: `{report['framework_root']}`",
        f"- Target root: `{report['target_root']}`",
        f"- Copy: {summary['copy']}",
        f"- Identical: {summary['identical']}",
        f"- Merge required: {summary['merge-required']}",
        f"- Review required: {summary['review-required']}",
        "",
        "No target file was changed. Merge or review every collision before "
        "copying ATLAS into an existing project.",
        "",
    ]
    operations = report["operations"]
    if not isinstance(operations, list):
        raise ValueError("Adoption report operations must be an array")
    for action in ("merge-required", "review-required", "copy", "identical"):
        selected = [item for item in operations if item["action"] == action]
        lines.extend([f"## {action}", ""])
        if selected:
            lines.extend(f"- `{item['path']}`" for item in selected)
        else:
            lines.append("_None._")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only ATLAS adoption plan for an existing project. "
            "The command never copies or overwrites target files."
        )
    )
    parser.add_argument("--framework-root", default=str(ROOT))
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--output", help="Optional JSON report path.")
    parser.add_argument("--markdown-output", help="Optional Markdown report path.")
    args = parser.parse_args()

    framework_root = Path(args.framework_root).resolve()
    target_root = Path(args.target_root).resolve()
    if not (framework_root / "VERSION").is_file():
        raise SystemExit("Framework root has no VERSION file")
    if not target_root.is_dir():
        raise SystemExit("Target root must be an existing directory")

    operations, summary = classify(framework_root, target_root)
    report: dict[str, object] = {
        "framework_version": (
            framework_root / "VERSION"
        ).read_text(encoding="utf-8").strip(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "framework_root": framework_root.as_posix(),
        "target_root": target_root.as_posix(),
        "mode": "read-only",
        "summary": summary,
        "operations": operations,
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

    if args.markdown_output:
        markdown_output = Path(args.markdown_output).resolve()
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(render_markdown(report), encoding="utf-8")
        print(markdown_output)

    if summary["merge-required"] or summary["review-required"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
