from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTINUITY = ROOT / ".atlas" / "continuity"

def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    drift_path = CONTINUITY / "memory-drift-report.json"
    if not drift_path.is_file():
        raise SystemExit("Run scripts/audit_memory_drift.py first")

    drift = json.loads(drift_path.read_text(encoding="utf-8"))
    proposed = []

    for finding in drift["findings"]:
        proposed.append({
            "source": finding["source"],
            "finding_type": finding["type"],
            "severity": finding["severity"],
            "proposed_action": {
                "version-drift": "Update the source to the current framework version.",
                "continuity-version-drift": "Regenerate continuity artifacts.",
                "orphaned-reference": "Repair or remove the invalid reference.",
                "unknown-freshness": "Review the memory source and add review metadata.",
                "missing-source": "Restore the canonical source or update the manifest.",
            }.get(finding["type"], "Review manually."),
            "automatic": False,
        })

    proposal = {
        "framework_version": version,
        "drift_report": str(drift_path.relative_to(ROOT)),
        "proposed_updates": proposed,
        "manual_review": True,
        "status": "proposed",
    }

    output = CONTINUITY / "reconciliation-proposal.json"
    output.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
