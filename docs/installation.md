# Installation

## Choose a delivery mode

- Use a **cumulative package** for a clean installation, recovery, or when the
  installed base is uncertain.
- Use an **incremental package** only when the installed `VERSION` exactly
  matches the package's `from_version`.
- Use a **project-local installation** when ATLAS should govern one repository.
- Use a **dedicated framework repository** when maintaining ATLAS centrally and
  distributing validated packages to projects.

## Clean installation from a cumulative package

1. Verify the external `.sha256` file against the final ZIP.
2. Extract the archive.
3. Open its single versioned root, such as
   `atlas-framework-0.1.0-rc.1/`.
4. Copy the contents into the target repository root.
5. Confirm `.claude/registry.json`, `VERSION`, `README.md`, and `LICENSE` exist.
6. Optionally run the validators documented in the README.

The cumulative archive contains the canonical hidden `.claude/` directory. It
does not use `CLAUDE-DIRECTORY/`.

## Project-local installation

Keep the full framework at the project root:

```text
project/
├── .claude/
├── adapters/
├── compatibility/
├── docs/
├── framework/
├── policies/
├── schemas/
├── scripts/
├── templates/
├── tests/
├── AGENTS.md
└── VERSION
```

Add validated project knowledge under `.claude/memory/`. Never store secrets,
temporary logs, or unconfirmed assumptions in durable memory.

## Dedicated repository

Maintain ATLAS as its own repository, run all release gates there, then
distribute cumulative or incremental packages. Do not copy runtime-specific
memory into separate forks: Claude Code and Codex must continue to share the
same canonical contracts and knowledge.

## Incremental manual installation

1. Read `APPLY-PATCH.md`.
2. Confirm installed `VERSION` equals `from_version` in
   `PATCH-MANIFEST.json`.
3. Copy files from `FILES-TO-ADD.md`.
4. Copy and overwrite files from `FILES-TO-REPLACE.md`.
5. Translate every package path under `CLAUDE-DIRECTORY/` to `.claude/`.
6. Remove only target paths listed in `FILES-TO-DELETE.md`.
7. Confirm the resulting `VERSION` equals `to_version`.

Absence from the package is never a deletion instruction. Applying the patch
does not require a script.

## Windows and hidden directories

Windows Explorer and upload dialogs may hide `.claude/`. Incremental packages
therefore use the visible package-only name `CLAUDE-DIRECTORY/`. After copying,
the installed directory must still be named `.claude`.

Enable **View hidden items** when verifying the installed repository. Do not
leave a permanent `CLAUDE-DIRECTORY/` beside `.claude/`.

## GitHub manual upload

When uploading through GitHub's web interface:

1. Apply non-hidden directories normally.
2. Open `CLAUDE-DIRECTORY/` from the patch and upload its contents into the
   repository's existing `.claude/` directory.
3. Review `FILES-TO-DELETE.md` and delete only those paths explicitly.
4. Confirm the diff before committing.

Package instructions and manifests remain at the patch root. A
`CLAUDE-DIRECTORY/` payload must contain only files whose target is `.claude/`.

## Optional validation

```bash
python scripts/manual_deploy_preflight.py \
  --installed-root <installed-repository> \
  --patch-root <extracted-patch>

python scripts/simulate_incremental_install.py \
  --installed-root <installed-repository> \
  --patch-root <extracted-patch> \
  --output-root <new-empty-path>
```

For cumulative archives:

```bash
python scripts/validate_release_artifacts.py --archive <archive.zip>
python scripts/simulate_cumulative_install.py \
  --archive <archive.zip> \
  --output-root <new-empty-path>
```
