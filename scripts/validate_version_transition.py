from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-version", required=True)
    parser.add_argument("--to-version", required=True)
    parser.add_argument("--installed-root", default=str(ROOT))
    args = parser.parse_args()

    installed = Path(args.installed_root)
    current = (installed / "VERSION").read_text(encoding="utf-8").strip()
    if current != args.from_version:
        raise SystemExit(
            f"Invalid transition: expected {args.from_version}, found {current}"
        )
    if args.from_version == args.to_version:
        raise SystemExit("Source and target versions must differ")
    print(f"Valid transition: {args.from_version} -> {args.to_version}")

if __name__ == "__main__":
    main()
