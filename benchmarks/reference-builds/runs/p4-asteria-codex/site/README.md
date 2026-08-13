# Asteria Residences

Production-equivalent implementation for the ATLAS P4 Codex target.

```bash
npm start
```

The default origin is `http://localhost:4173`. Set `PUBLIC_ORIGIN` to the final HTTPS origin before production deployment so canonical, sitemap and structured-data URLs match the deployed domain.

Lead state, persistent idempotency keys, durable rate events and the analytics outbox use transactional SQLite in `data/asteria.sqlite`, excluded from Git. The lead and its authoritative conversion event commit in the same transaction. For horizontally scaled production, place the same schema/constraints in a managed transactional database shared by all instances.

In non-production only, an address ending in `@failure.test` triggers the recoverable provider-failure path for browser evidence.
