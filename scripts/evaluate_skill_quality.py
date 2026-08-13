#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from capability_metrics import ROOT, has_any, jaccard, markdown_words, parse_markdown, section

REGISTRY = ROOT / ".claude" / "registry.json"
REQUIRED_SECTIONS = ["purpose", "trigger conditions", "inputs", "outputs", "dependencies", "limitations", "validation"]
TRIGGER_CUES = ("when", "use", "if", "before", "after", "change", "changes", "added", "adding", "review", "audit")
EVIDENCE_CUES = ("verify", "validate", "test", "check", "inspect", "evidence", "run", "confirm", "compare", "exercise")
FAILURE_CUES = ("failure", "negative", "error", "edge", "risk", "blocked", "missing", "invalid", "drift", "regression")


def evaluate(name: str, path: Path, peer_descriptions: dict[str, str]) -> dict[str, object]:
    metadata, body, sections = parse_markdown(path)
    description = str(metadata.get("description", "")).strip()
    purpose = section(sections, "purpose")
    trigger = section(sections, "trigger conditions")
    inputs = section(sections, "inputs")
    outputs = section(sections, "outputs")
    dependencies = section(sections, "dependencies")
    limitations = section(sections, "limitations")
    validation = section(sections, "validation")
    procedure = section(sections, "procedure")
    reasons: list[str] = []

    metadata_score = 0
    if metadata.get("name") == name:
        metadata_score += 4
    else:
        reasons.append("canonical name mismatch")
    if description:
        metadata_score += 4
    else:
        reasons.append("missing discovery description")
    desc_words = markdown_words(description)
    if 6 <= desc_words <= 55:
        metadata_score += 3
    else:
        reasons.append(f"description word count={desc_words}")
    if has_any(description, TRIGGER_CUES):
        metadata_score += 2
    else:
        reasons.append("description lacks an explicit activation cue")
    if description and "\n" not in description and len(description) <= 320:
        metadata_score += 2

    structure_score = 0
    for required in REQUIRED_SECTIONS:
        if section(sections, required):
            structure_score += 3
        else:
            reasons.append(f"missing or empty section: {required}")
    if markdown_words(purpose) >= 8:
        structure_score += 2
    else:
        reasons.append("purpose is too thin")
    if "- " in inputs and "- " in outputs:
        structure_score += 2
    else:
        reasons.append("inputs/outputs are not clearly enumerated")

    trigger_score = 0
    trigger_words = markdown_words(trigger)
    if trigger_words >= 8:
        trigger_score += 5
    else:
        reasons.append("trigger conditions are too thin")
    if has_any(trigger, TRIGGER_CUES):
        trigger_score += 3
    else:
        reasons.append("trigger section lacks condition language")
    purpose_overlap = jaccard(trigger, purpose)
    if purpose_overlap < 0.75:
        trigger_score += 4
    else:
        reasons.append(f"trigger largely restates purpose ({purpose_overlap:.2f})")
    desc_overlap = jaccard(trigger, description)
    if desc_overlap >= 0.05:
        trigger_score += 4
    else:
        reasons.append(f"trigger/discovery alignment is weak ({desc_overlap:.2f})")
    if desc_overlap < 0.85:
        trigger_score += 2
    else:
        reasons.append("trigger nearly duplicates discovery description")
    nearest = 0.0
    nearest_name = None
    for other_name, other_description in peer_descriptions.items():
        if other_name == name:
            continue
        score = jaccard(description, other_description)
        if score > nearest:
            nearest = score
            nearest_name = other_name
    if nearest < 0.80:
        trigger_score += 2
    else:
        reasons.append(f"discovery description collides with {nearest_name} ({nearest:.2f})")

    evidence_score = 0
    if markdown_words(validation) >= 8:
        evidence_score += 5
    else:
        reasons.append("validation guidance is too thin")
    if has_any(validation, EVIDENCE_CUES):
        evidence_score += 5
    else:
        reasons.append("validation lacks executable/inspectable evidence cues")
    if markdown_words(outputs) >= 5:
        evidence_score += 3
    else:
        reasons.append("outputs are too thin")
    if markdown_words(limitations) >= 6:
        evidence_score += 3
    else:
        reasons.append("limitations are too thin")
    if has_any(procedure + "\n" + validation + "\n" + limitations, FAILURE_CUES):
        evidence_score += 4
    else:
        reasons.append("failure/negative-path handling is not explicit")

    boundary_score = 0
    if dependencies:
        boundary_score += 4
    if limitations:
        boundary_score += 3
    if not has_any(body, ("todo", "tbd", "placeholder", "fixme")):
        boundary_score += 3
    else:
        reasons.append("contains TODO/TBD/placeholder debt")

    context_score = 0
    body_words = markdown_words(body)
    if 100 <= body_words <= 1800:
        context_score += 5
    elif 60 <= body_words <= 2200:
        context_score += 3
        reasons.append(f"body size is outside preferred range ({body_words} words)")
    else:
        reasons.append(f"body size is outside bounded range ({body_words} words)")
    line_count = len(body.splitlines())
    if line_count <= 350:
        context_score += 3
    else:
        reasons.append(f"body is long ({line_count} lines)")
    if desc_words <= 55:
        context_score += 2

    scores = {
        "metadata_discovery": metadata_score,
        "structure": structure_score,
        "trigger": trigger_score,
        "evidence": evidence_score,
        "boundaries": boundary_score,
        "context": context_score,
    }
    total = sum(scores.values())
    grade = "A" if total >= 90 else "B" if total >= 80 else "C" if total >= 70 else "D"
    return {
        "name": name,
        "score": total,
        "grade": grade,
        "scores": scores,
        "nearest_description_skill": nearest_name,
        "nearest_description_jaccard": round(nearest, 4),
        "reasons": reasons,
    }


def build_report() -> dict[str, object]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    names = list(registry.get("skills", []))
    descriptions: dict[str, str] = {}
    for name in names:
        metadata, _, _ = parse_markdown(ROOT / ".claude" / "skills" / name / "SKILL.md")
        descriptions[name] = str(metadata.get("description", "")).strip()
    results = [evaluate(name, ROOT / ".claude" / "skills" / name / "SKILL.md", descriptions) for name in names]
    results.sort(key=lambda item: (int(item["score"]), str(item["name"])))
    scores = [int(item["score"]) for item in results]
    grades = {grade: sum(1 for item in results if item["grade"] == grade) for grade in ("A", "B", "C", "D")}
    quantiles = statistics.quantiles(scores, n=4, method="inclusive") if len(scores) > 1 else [scores[0]] * 3
    return {
        "skill_count": len(results),
        "mean": round(statistics.mean(scores), 2),
        "median": round(statistics.median(scores), 2),
        "minimum": min(scores),
        "maximum": max(scores),
        "p25": round(quantiles[0], 2),
        "p75": round(quantiles[2], 2),
        "grades": grades,
        "bottom_10": results[:10],
        "skills": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--fail-below", type=int)
    args = parser.parse_args()
    report = build_report()
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        "Skill quality: "
        f"count={report['skill_count']} mean={report['mean']} median={report['median']} "
        f"min={report['minimum']} p25={report['p25']} p75={report['p75']} grades={report['grades']}"
    )
    print("Bottom 10: " + ", ".join(f"{item['name']}={item['score']}" for item in report["bottom_10"]))
    if args.fail_below is not None:
        failures = [item for item in report["skills"] if int(item["score"]) < args.fail_below]
        if failures:
            print(f"ERROR: {len(failures)} skills scored below {args.fail_below}")
            raise SystemExit(1)


if __name__ == "__main__":
    main()
