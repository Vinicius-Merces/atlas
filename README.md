# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.11`  
**Status:** Beta / Policy Enforcement and Manual Deployment Safety

ATLAS coordinates software engineering through shared memory, specialized
agents, workflows, review gates, runtime contracts, portable continuity,
parallel execution, auditability, and policy enforcement.

## Beta.11 milestone

Policies can now be evaluated before execution, review, release, and manual
deployment.

### New capabilities

- Machine-readable policy rules
- Policy evaluation
- Manual deployment preflight
- Required-file checks
- Forbidden-path checks
- Version transition validation
- Policy exceptions
- Deployment safety reports
- Visible `CLAUDE-DIRECTORY` packaging

## Manual package convention

Updates intended for `.claude` are delivered inside:

```text
CLAUDE-DIRECTORY/
```

During manual deployment, copy its contents into `.claude/` in the repository.

## Commands

```bash
python scripts/evaluate_policies.py
python scripts/manual_deploy_preflight.py --patch-root .
python scripts/validate_version_transition.py --from-version 0.1.0-beta.10 --to-version 0.1.0-beta.11
python scripts/build_policy_report.py
```

Validation scripts remain optional. The package can still be applied manually.
