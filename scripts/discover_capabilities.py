#!/usr/bin/env python3
"""Return a bounded, deterministic capability set for a natural-language query."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "atlas-registry" / "ard-index.json"
TOKEN = re.compile(r"[a-z0-9]+")


def tokens(value: str) -> set[str]:
    return set(TOKEN.findall(value.lower()))


def score(query: str, item: dict[str, object]) -> int:
    query_tokens = tokens(query)
    name = str(item["id"]).split(":", 1)[1]
    name_tokens = tokens(name)
    description_tokens = tokens(str(item["description"]))
    keyword_tokens = {str(value) for value in item.get("keywords", [])}
    exact = 100 if query.strip().lower() == name else 0
    phrase = 40 if name.replace("-", " ") in query.lower() else 0
    return exact + phrase + 12 * len(query_tokens & name_tokens) + 4 * len(query_tokens & keyword_tokens) + len(query_tokens & description_tokens)


def discover(query: str, *, limit: int, kinds: set[str]) -> list[dict[str, object]]:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    candidates = [
        item for item in index["capabilities"]
        if (not kinds or item["kind"] in kinds) and item["trust"] != "blocked"
    ]
    ranked = sorted(
        ((score(query, item), item) for item in candidates),
        key=lambda pair: (-pair[0], str(pair[1]["id"])),
    )
    return [dict(item, score=value) for value, item in ranked if value > 0][:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--kind", action="append", choices=["agent", "skill", "workflow", "review", "command"], default=[])
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 10:
        parser.error("--limit must be between 1 and 10")
    print(json.dumps(discover(args.query, limit=args.limit, kinds=set(args.kind)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
