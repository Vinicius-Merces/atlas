from __future__ import annotations

import argparse
from pathlib import Path

from release_utils import (
    source_payload,
    write_deterministic_zip,
    write_external_metadata,
)


ROOT = Path(__file__).resolve().parents[1]


def recovery_instructions(version: str) -> bytes:
    return f"""# ATLAS Recovery Package

This package restores the complete ATLAS {version} framework.

1. Preserve the current repository or create a backup.
2. Extract the archive.
3. Copy the contents of the versioned root into the target repository.
4. Keep the included `.claude/` directory under that exact hidden name.
5. Run the documented validators after restoration.

Recovery is explicit and does not delete unrelated project files.
""".encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", default=str(ROOT))
    parser.add_argument("--output-dir")
    parser.add_argument(
        "--kind", choices=["cumulative", "recovery"], default="cumulative"
    )
    args = parser.parse_args()

    source_root = Path(args.source_root).resolve()
    output_dir = (
        Path(args.output_dir).resolve()
        if args.output_dir
        else source_root / "dist"
    )
    version = (source_root / "VERSION").read_text(encoding="utf-8").strip()
    payload = source_payload(source_root)
    if args.kind == "recovery":
        payload["RECOVERY-INSTRUCTIONS.md"] = recovery_instructions(version)

    root_name = f"atlas-framework-{version}"
    archive_path = output_dir / f"{root_name}-{args.kind}.zip"
    manifest_bytes = write_deterministic_zip(archive_path, root_name, payload)
    manifest_path, checksum_path = write_external_metadata(
        archive_path,
        args.kind,
        version,
        manifest_bytes,
        len(payload),
    )

    print(f"Created {archive_path}")
    print(f"Created {manifest_path}")
    print(f"Created {checksum_path}")


if __name__ == "__main__":
    main()
