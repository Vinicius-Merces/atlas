from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    results = []

    registry = json.loads((ROOT / ".claude/registry.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "adapters/shared/runtime-contract.json").read_text(encoding="utf-8"))
    claude = json.loads((ROOT / "adapters/claude/runtime-declaration.json").read_text(encoding="utf-8"))
    codex = json.loads((ROOT / "adapters/codex/runtime-declaration.json").read_text(encoding="utf-8"))

    versions = {
        "registry": registry.get("version"),
        "runtime_contract": contract.get("version"),
        "claude": claude.get("version"),
        "codex": codex.get("version"),
    }
    mismatches = {k: v for k, v in versions.items() if v != version}
    results.append({
        "policy_id": "atlas.version.consistency",
        "outcome": "blocked" if mismatches else "passed",
        "evidence": versions,
        "findings": mismatches,
    })

    report = {
        "framework_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": {
            "passed": sum(1 for x in results if x["outcome"] == "passed"),
            "blocked": sum(1 for x in results if x["outcome"] == "blocked"),
        },
    }
    output = ROOT / ".atlas" / "policy" / "policy-report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(output)
    if report["summary"]["blocked"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
