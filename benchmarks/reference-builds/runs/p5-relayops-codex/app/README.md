# RelayOps

Operational multi-tenant field-service SaaS used by the ATLAS P5 Codex target.

```bash
node scripts/build.mjs
NODE_ENV=test node --test tests/*.test.js
RELAYOPS_DEMO_MODE=1 PORT=4173 node dist/server.js
```

Demo users:

- `manager@northstar.test`
- `dispatcher@northstar.test`
- `tech@northstar.test`
- `billing@northstar.test`
- password: `RelayOps!2026`
- support: `support@relayops.test` / `Support!2026`

Runtime configuration is server-only: `RELAYOPS_DB_PATH`, `RELAYOPS_WEBHOOK_SECRET`, `RELAYOPS_DEMO_MODE`, `PORT`, `PUBLIC_ORIGIN`, and optional `TRUST_PROXY`. No privileged value is serialized into public JavaScript or HTML.

The provider behavior is a deterministic sandbox-equivalent for distributed-state verification. It proves checkout authority, signed duplicate/out-of-order events, reconciliation and revocation, but is not claimed as live payment production configuration.
