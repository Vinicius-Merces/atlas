from __future__ import annotations
import argparse
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY_ROOT = ROOT / ".claude" / "memory"
DATE_PATTERN = re.compile(
    r"Last reviewed:\*{0,2}\s*(\d{4}-\d{2}-\d{2})", re.I
)
METADATA_PATTERNS = {
    "Purpose": re.compile(r"Purpose:\*{0,2}\s*(.+)", re.I),
    "Scope": re.compile(r"Scope:\*{0,2}\s*(.+)", re.I),
    "Owner": re.compile(r"Owner:\*{0,2}\s*(.+)", re.I),
    "Source of truth": re.compile(r"Source of truth:\*{0,2}\s*(.+)", re.I),
    "Related contracts or ADRs": re.compile(
        r"Related contracts or ADRs:\*{0,2}\s*(.+)", re.I
    ),
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    errors = []
    warnings = []
    today = date.today()

    memory_paths = [
        path
        for path in sorted(MEMORY_ROOT.glob("*.md"))
        if path.name not in {"README.md", "index.md"}
    ]
    if not memory_paths:
        errors.append("No canonical project memory documents are present")

    for path in memory_paths:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for label, pattern in METADATA_PATTERNS.items():
            match = pattern.search(text)
            if not match or not match.group(1).strip():
                errors.append(f"Missing {label}: {relative}")

        match = DATE_PATTERN.search(text)
        if not match:
            errors.append(f"Unknown review date: {relative}")
            continue

        reviewed = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        if reviewed > today:
            errors.append(f"Future review date: {relative}")
            continue
        age = (today - reviewed).days
        if age > args.max_age_days:
            warnings.append(
                f"Stale ({age} days): {relative}"
            )

        source_match = METADATA_PATTERNS["Source of truth"].search(text)
        source_paths = re.findall(r"`([^`]+)`", source_match.group(1))
        if not source_paths:
            errors.append(f"Source of truth has no repository path: {relative}")
        for source in source_paths:
            if not (ROOT / source).exists():
                errors.append(f"Missing source {source}: {relative}")

    if errors:
        print("Memory freshness validation failed:")
        for error in errors:
            print(f"- {error}")
    if warnings:
        print("Memory freshness warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors or (args.strict and warnings):
        raise SystemExit(1)
    if not warnings:
        print(f"Memory freshness check passed: {len(memory_paths)} documents")

if __name__ == "__main__":
    main()
