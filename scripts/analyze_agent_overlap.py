#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from capability_metrics import ROOT, build_idf, cosine, parse_markdown, section, vectorize

REGISTRY = ROOT / ".claude" / "registry.json"
TAXONOMY = ROOT / "framework" / "capabilities" / "agent-taxonomy.yaml"


def build_report() -> dict[str, object]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    names = [str(registry["orchestrator"]), *list(registry.get("agents", []))]
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8")) or {}
    domains: dict[str, str] = {}
    for domain, data in (taxonomy.get("categories") or {}).items():
        for agent in data.get("agents", []):
            domains[str(agent)] = str(domain)

    texts: dict[str, str] = {}
    for name in names:
        metadata, _, sections = parse_markdown(ROOT / ".claude" / "agents" / f"{name}.md")
        description = str(metadata.get("description", ""))
        mission = section(sections, "mission")
        ownership = "\n".join([
            section(sections, "owns"),
            section(sections, "responsibilities"),
            section(sections, "scope"),
            section(sections, "required outputs"),
        ])
        texts[name] = f"{description}\n{description}\n{mission}\n{ownership}"
        if name not in domains:
            raise ValueError(f"agent has no taxonomy domain: {name}")

    idf = build_idf(texts.values())
    vectors = {name: vectorize(text, idf) for name, text in texts.items()}
    pairs: list[dict[str, object]] = []
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            similarity = cosine(vectors[left], vectors[right])
            pairs.append({
                "left": left,
                "right": right,
                "similarity": round(similarity, 4),
                "same_domain": domains[left] == domains[right],
                "left_domain": domains[left],
                "right_domain": domains[right],
            })
    pairs.sort(key=lambda item: (-float(item["similarity"]), str(item["left"]), str(item["right"])))
    return {
        "agent_count": len(names),
        "pair_count": len(pairs),
        "pairs_ge_0_55": sum(1 for item in pairs if float(item["similarity"]) >= 0.55),
        "pairs_ge_0_70": sum(1 for item in pairs if float(item["similarity"]) >= 0.70),
        "cross_domain_ge_0_55": sum(1 for item in pairs if not item["same_domain"] and float(item["similarity"]) >= 0.55),
        "top_20": pairs[:20],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()
    report = build_report()
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        "Agent overlap proxy: "
        f"agents={report['agent_count']} pairs={report['pair_count']} "
        f">=0.55={report['pairs_ge_0_55']} >=0.70={report['pairs_ge_0_70']} cross_domain>=0.55={report['cross_domain_ge_0_55']}"
    )
    print("Top overlaps: " + ", ".join(f"{item['left']}~{item['right']}={item['similarity']:.2f}" for item in report["top_20"][:10]))


if __name__ == "__main__":
    main()
