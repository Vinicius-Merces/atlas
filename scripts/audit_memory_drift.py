from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTINUITY = ROOT / ".atlas" / "continuity"
LAST_REVIEWED = re.compile(r"Last reviewed:\*{0,2}\s*\d{4}-\d{2}-\d{2}", re.I)

def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    findings = []
    sources_checked = []

    version_sources = [
        "VERSION",
        ".claude/registry.json",
        "adapters/shared/runtime-contract.json",
        "adapters/claude/runtime-declaration.json",
        "adapters/codex/runtime-declaration.json",
    ]

    for relative in version_sources:
        path = ROOT / relative
        if not path.is_file():
            findings.append({
                "type": "missing-source",
                "severity": "high",
                "source": relative,
                "message": "Expected version-bearing source is missing."
            })
            continue

        sources_checked.append(relative)
        text = path.read_text(encoding="utf-8")
        if version not in text:
            findings.append({
                "type": "version-drift",
                "severity": "blocking",
                "source": relative,
                "message": f"Source does not declare framework version {version}."
            })

    memory_paths = [
        path
        for path in sorted((ROOT / ".claude" / "memory").glob("*.md"))
        if path.name not in {"README.md", "index.md"}
    ]
    for path in memory_paths:
        relative = path.relative_to(ROOT).as_posix()
        sources_checked.append(relative)
        text = path.read_text(encoding="utf-8")
        if not LAST_REVIEWED.search(text):
            findings.append({
                "type": "unknown-freshness",
                "severity": "warning",
                "source": relative,
                "message": "Memory file has no Last reviewed metadata."
            })

    resume = CONTINUITY / "resume-packet.json"
    if resume.is_file():
        sources_checked.append(resume.relative_to(ROOT).as_posix())
        data = json.loads(resume.read_text(encoding="utf-8"))
        if data.get("framework_version") != version:
            findings.append({
                "type": "continuity-version-drift",
                "severity": "high",
                "source": resume.relative_to(ROOT).as_posix(),
                "message": "Resume packet was generated for another framework version."
            })

        for field in ["project_brief", "latest_session"]:
            relative = data.get(field)
            if relative and not (ROOT / relative).exists():
                findings.append({
                    "type": "orphaned-reference",
                    "severity": "high",
                    "source": resume.relative_to(ROOT).as_posix(),
                    "message": f"Missing referenced artifact: {relative}"
                })

    report = {
        "framework_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources_checked": sorted(set(sources_checked)),
        "findings": findings,
        "summary": {
            "total": len(findings),
            "blocking": sum(1 for x in findings if x["severity"] == "blocking"),
            "high": sum(1 for x in findings if x["severity"] == "high"),
            "warning": sum(1 for x in findings if x["severity"] == "warning"),
        }
    }

    output = CONTINUITY / "memory-drift-report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
