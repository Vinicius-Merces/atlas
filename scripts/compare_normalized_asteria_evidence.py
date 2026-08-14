#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Compare P4.3 normalized evidence summaries.")
    p.add_argument("--codex", required=True)
    p.add_argument("--claude", required=True)
    p.add_argument("--output", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    codex = json.loads(Path(args.codex).read_text(encoding="utf-8"))
    claude = json.loads(Path(args.claude).read_text(encoding="utf-8"))
    rows = {"codex": codex, "claude-code": claude}

    for key, row in rows.items():
        if row.get("target") != key:
            raise SystemExit(f"target mismatch for {key}: {row.get('target')!r}")
        if row.get("evidence_source") != "campaign-portable":
            raise SystemExit(f"{key} is not campaign-portable evidence")
        if row.get("deployment_class") != "controlled-preview":
            raise SystemExit(f"{key} did not use controlled-preview")

    common_checks = sorted(set(codex.get("checks", {})) & set(claude.get("checks", {})))
    comparison = {
        "version": 1,
        "campaign": "p4-3-normalized-asteria-reevaluation",
        "comparison_type": "frozen-implementation-environment-normalized-evidence",
        "historical_scores_immutable": {
            "codex": codex.get("historical_score"),
            "claude-code": claude.get("historical_score"),
        },
        "source_commits": {
            "codex": codex.get("source_commit"),
            "claude-code": claude.get("source_commit"),
        },
        "campaign_commits": sorted({codex.get("campaign_commit"), claude.get("campaign_commit")}),
        "normalized_floor_pass": {
            "codex": codex.get("normalized_floor_pass"),
            "claude-code": claude.get("normalized_floor_pass"),
        },
        "check_matrix": {
            check: {
                "codex": bool(codex.get("checks", {}).get(check)),
                "claude-code": bool(claude.get("checks", {}).get(check)),
            }
            for check in common_checks
        },
        "observations": {
            "codex": codex.get("observations", {}),
            "claude-code": claude.get("observations", {}),
        },
        "interpretation": (
            "This comparison measures evidence recovered when the exact frozen target implementations receive the same campaign-owned public HTTPS and Chromium path. "
            "It does not replace the historical benchmark scores and does not claim a new model ranking."
        ),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(comparison, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
