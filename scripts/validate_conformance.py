from __future__ import annotations

import argparse
from pathlib import Path

from validate_runtime_contract import collect_failures


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Claude Code and Codex conformance to the universal "
            "runtime contract."
        )
    )
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    failures = collect_failures(Path(args.root).resolve())
    if failures:
        print("Runtime conformance validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Claude Code and Codex conform to the universal runtime contract.")


if __name__ == "__main__":
    main()
