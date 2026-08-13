#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from capability_metrics import ROOT, build_idf, cosine, parse_markdown, section, vectorize

REGISTRY = ROOT / ".claude" / "registry.json"
FIXTURES = ROOT / "tests" / "fixtures" / "capability-routing-cases.yaml"


def rank(query: str, descriptions: dict[str, str], idf: dict[str, float]) -> list[tuple[str, float]]:
    query_vector = vectorize(query, idf)
    scored = [(name, cosine(query_vector, vectorize(text, idf))) for name, text in descriptions.items()]
    return sorted(scored, key=lambda item: (-item[1], item[0]))


def build_report() -> dict[str, object]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    names = list(registry.get("skills", []))
    descriptions: dict[str, str] = {}
    triggers: dict[str, str] = {}
    for name in names:
        metadata, _, sections = parse_markdown(ROOT / ".claude" / "skills" / name / "SKILL.md")
        descriptions[name] = str(metadata.get("description", "")).strip()
        triggers[name] = section(sections, "trigger conditions")
    idf = build_idf(list(descriptions.values()) + list(triggers.values()))

    ranks: dict[str, int] = {}
    misses: list[dict[str, object]] = []
    for name in names:
        ordered = rank(triggers[name], descriptions, idf)
        position = next((index + 1 for index, item in enumerate(ordered) if item[0] == name), len(ordered) + 1)
        ranks[name] = position
        if position > 5:
            misses.append({"skill": name, "rank": position, "top": ordered[:5]})

    fixture_data = yaml.safe_load(FIXTURES.read_text(encoding="utf-8")) or {}
    fixture_results: list[dict[str, object]] = []
    for case in fixture_data.get("cases", []):
        expected = case["expected"]
        if expected not in descriptions:
            raise ValueError(f"fixture target is not registered: {expected}")
        ordered = rank(str(case["query"]), descriptions, idf)
        position = next((index + 1 for index, item in enumerate(ordered) if item[0] == expected), len(ordered) + 1)
        fixture_results.append({"id": case["id"], "expected": expected, "rank": position, "top": ordered[:5]})

    vectors = {name: vectorize(text, idf) for name, text in descriptions.items()}
    pairs: list[dict[str, object]] = []
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            score = cosine(vectors[left], vectors[right])
            pairs.append({"left": left, "right": right, "similarity": round(score, 4)})
    pairs.sort(key=lambda item: (-float(item["similarity"]), str(item["left"]), str(item["right"])))

    count = len(names)
    top1 = sum(1 for value in ranks.values() if value <= 1)
    top3 = sum(1 for value in ranks.values() if value <= 3)
    top5 = sum(1 for value in ranks.values() if value <= 5)
    fixture_count = len(fixture_results)
    fixture_top1 = sum(1 for item in fixture_results if int(item["rank"]) <= 1)
    fixture_top3 = sum(1 for item in fixture_results if int(item["rank"]) <= 3)
    fixture_top5 = sum(1 for item in fixture_results if int(item["rank"]) <= 5)
    return {
        "skill_count": count,
        "self_retrieval": {
            "top1": round(top1 / count, 4) if count else 0.0,
            "top3": round(top3 / count, 4) if count else 0.0,
            "top5": round(top5 / count, 4) if count else 0.0,
            "misses_over_5": misses,
        },
        "fixtures": {
            "count": fixture_count,
            "top1": round(fixture_top1 / fixture_count, 4) if fixture_count else 0.0,
            "top3": round(fixture_top3 / fixture_count, 4) if fixture_count else 0.0,
            "top5": round(fixture_top5 / fixture_count, 4) if fixture_count else 0.0,
            "results": fixture_results,
        },
        "description_collisions": {
            "pairs_ge_0_55": sum(1 for item in pairs if float(item["similarity"]) >= 0.55),
            "pairs_ge_0_70": sum(1 for item in pairs if float(item["similarity"]) >= 0.70),
            "top_15": pairs[:15],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()
    report = build_report()
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    own = report["self_retrieval"]
    fixtures = report["fixtures"]
    collisions = report["description_collisions"]
    print(
        "Skill routing proxy: "
        f"count={report['skill_count']} self_top1={own['top1']:.1%} self_top3={own['top3']:.1%} self_top5={own['top5']:.1%}; "
        f"fixtures={fixtures['count']} fixture_top1={fixtures['top1']:.1%} fixture_top3={fixtures['top3']:.1%} fixture_top5={fixtures['top5']:.1%}; "
        f"collisions>=0.55={collisions['pairs_ge_0_55']} >=0.70={collisions['pairs_ge_0_70']}"
    )
    if collisions["top_15"]:
        print("Top collisions: " + ", ".join(f"{item['left']}~{item['right']}={item['similarity']:.2f}" for item in collisions["top_15"][:8]))


if __name__ == "__main__":
    main()
