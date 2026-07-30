from __future__ import annotations
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY_ROOT = ROOT / ".claude" / "memory"
DATE_PATTERN = re.compile(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", re.I)

def main() -> None:
    warnings = []
    today = date.today()

    for path in sorted(MEMORY_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = DATE_PATTERN.search(text)
        if not match:
            warnings.append(f"Unknown review date: {path.relative_to(ROOT)}")
            continue

        reviewed = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        age = (today - reviewed).days
        if age > 180:
            warnings.append(
                f"Stale ({age} days): {path.relative_to(ROOT)}"
            )

    if warnings:
        print("Memory freshness warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("Memory freshness check passed.")

if __name__ == "__main__":
    main()
