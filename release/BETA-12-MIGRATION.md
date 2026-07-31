# Migration from 0.1.0-beta.11 to 0.1.0-beta.12

The incremental package applies only to an exact `0.1.0-beta.11` installation.
Use the cumulative package for any other base or when the local installation
has unknown changes.

## Before applying

1. Back up the target repository or create a recoverable version-control
   checkpoint.
2. Confirm that the installed `VERSION` is `0.1.0-beta.11`.
3. Extract the incremental archive into a temporary staging directory.
4. Run `python scripts/manual_deploy_preflight.py` from the extracted package
   with the beta.11 target as its base.
5. Stop if the preflight reports a mismatched base, undeclared file, checksum
   error, unsafe path, or operation conflict.

## Important structural change

Agent definitions previously stored under the root `agents/` directory are
deleted and reintroduced under the canonical `.claude/agents/` directory.
This is an intentional architecture correction.

In the incremental archive, every file below `CLAUDE-DIRECTORY/` maps to the
target repository's hidden `.claude/` directory. Do not leave a permanent
`CLAUDE-DIRECTORY/` directory in the installed repository.

## Apply the declared operations

- Copy files listed in `FILES-TO-ADD.md`.
- Replace files listed in `FILES-TO-REPLACE.md`.
- Delete only files listed in `FILES-TO-DELETE.md`.
- Never infer a recursive directory deletion from a listed file.

The package simulator performs these operations without mutating the original
base:

```text
python scripts/simulate_incremental_install.py PACKAGE_ROOT BASE_DIRECTORY OUTPUT_DIRECTORY
```

After application, run the validators described in `docs/installation.md` and
confirm that `VERSION` is `0.1.0-beta.12`, `.claude/agents/` is present, and
the root `agents/` directory is absent.

## Rollback

Restore the pre-deployment checkpoint. If that is unavailable, install the
beta.12 recovery archive into a clean directory and reconcile project-specific
files manually. The recovery package does not reconstruct unrecorded local
changes.

