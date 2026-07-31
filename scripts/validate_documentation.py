from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "docs/INDEX.md",
    "docs/installation.md",
    "docs/adoption-guide.md",
    "docs/claude-code-bootstrap-guide.md",
    "docs/codex-adoption-guide.md",
    "docs/runtime-guide.md",
    "docs/manual-deployment-guide.md",
    "docs/release-guide.md",
    "docs/framework-upgrade-guide.md",
    "docs/troubleshooting.md",
    "compatibility/support-policy.md",
    "compatibility/runtime-matrix.md",
    "release/RC-RELEASE-CHECKLIST.md",
    "release/STABLE-RELEASE-CHECKLIST.md",
]


def main() -> None:
    failures: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            failures.append(f"Missing required documentation: {relative}")

    files = [
        ROOT / "README.md",
        *sorted((ROOT / "docs").glob("*.md")),
        ROOT / "compatibility" / "support-policy.md",
        ROOT / "compatibility" / "runtime-matrix.md",
    ]
    links_checked = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            relative_target = target.split("#", 1)[0].strip()
            if (
                not relative_target
                or "://" in relative_target
                or relative_target.startswith("mailto:")
            ):
                continue
            links_checked += 1
            if not (path.parent / relative_target).resolve().exists():
                failures.append(
                    f"Broken link: {path.relative_to(ROOT)} -> {target}"
                )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in [
        "## Who it is for",
        "## What it solves",
        "## Install",
        "## Use with Claude Code",
        "## Use with Codex",
        "## Update manually",
        "## Validate",
        "## Contribute",
        "## Support and limitations",
    ]:
        if heading not in readme:
            failures.append(f"README is missing section: {heading}")

    index = (ROOT / "docs" / "INDEX.md").read_text(encoding="utf-8")
    for capability in [
        "Dual Runtime",
        "Runtime Synchronization",
        "Task Routing",
        "Context Packs",
        "Runtime Handoff",
        "Task Recovery",
        "Parallel Execution",
        "Workstream Merge",
        "Cross-Session Continuity",
        "Memory Governance",
        "Evidence Ledger",
        "Deployment Receipts",
        "Audit Bundles",
        "Policy Enforcement",
        "Deployment Preflight",
    ]:
        if capability not in index:
            failures.append(f"Documentation index is missing: {capability}")

    if failures:
        print("Documentation validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(
        f"Documentation validation passed: {len(REQUIRED)} required files, "
        f"{links_checked} links"
    )


if __name__ == "__main__":
    main()
