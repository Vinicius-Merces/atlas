# Migration from 0.1.0-beta.12 to 0.1.0-rc.1

The RC incremental package applies only to an exact `0.1.0-beta.12`
installation. Use the cumulative package for any other base.

## Upgrade

1. Create a recoverable checkpoint of the target repository.
2. Confirm that `VERSION` is exactly `0.1.0-beta.12`.
3. Extract the RC incremental archive into a temporary directory.
4. Run the manual deployment preflight against the target installation.
5. Apply only the declared additions, replacements, and deletions.
6. Map `CLAUDE-DIRECTORY/` package paths to `.claude/`.
7. Confirm that `VERSION` is `0.1.0-rc.1`.
8. Run the documented validators.

The migration promotes version and stability metadata and adds RC release
records. It does not change canonical paths or contract semantics.

## Upgrading from beta.11 or earlier

Apply the documented beta.11-to-beta.12 upgrade first and then this patch, or
install the RC cumulative package into a clean directory. Do not apply the RC
incremental archive directly over beta.11.

## Rollback

Restore the beta.12 checkpoint. If no checkpoint exists, use the RC recovery
package to obtain a complete known-good framework tree and reconcile
project-specific files manually.

