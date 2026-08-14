# RelayOps local execution summary

- Runtime/model: `codex` / `GPT-5`
- Source tenant: `org_northstar`
- Target tenant: `org_harbor`
- Test command: `NODE_ENV=test node --test tests/*.test.js`
- Result: 13 passed, 0 failed
- Build command: `node scripts/build.mjs`
- Build result: passed
- HTTP smoke: health 200, login 200, demo session 303, authenticated dashboard 200

The machine-readable evidence is `assurance-results.json`. It records direct denied attempts for database/object read and mutation, attachment read and write, search sentinel leakage, cache/job context, notification scope, export scope, support without context, vertical escalation, stale authorization and revoked entitlement. It also records duplicate delivery, bounded retry/recovery, duplicate and out-of-order billing events, import partial failure/safe replay, session lifecycle and secret scans.

No PostgreSQL RLS, live payment provider, live email delivery, public HTTPS, responsive browser evidence or production deployment is inferred from these local results. Those claims require their corresponding campaign evidence.
