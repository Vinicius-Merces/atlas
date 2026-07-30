# Release Workflow

## Trigger

A validated set of changes is ready for deployment or publication.

## Sequence

1. Confirm release scope.
2. Verify version and changelog.
3. Review unresolved findings.
4. Validate tests and quality gates.
5. Confirm migrations and compatibility.
6. Confirm monitoring and rollback.
7. Prepare release notes.
8. Approve or block release.
9. Record post-release validation expectations.

## Blocking conditions

- Critical security findings
- Failed mandatory tests
- Unapproved breaking changes
- Missing rollback for high-risk migration
- Unknown production impact
