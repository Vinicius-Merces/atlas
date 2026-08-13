# Asteria Residences

Production-equivalent implementation for the ATLAS P4 Codex target.

```bash
npm start
```

The default origin is `http://localhost:4173`. Set `PUBLIC_ORIGIN` to the final HTTPS origin before production deployment so canonical, sitemap and structured-data URLs match the deployed domain.

Lead state is stored atomically in `data/leads.json`; analytics events are appended to `data/analytics.jsonl`. Both are excluded from Git. For multi-instance production, replace the filesystem adapter with a transactional database while preserving the validation/idempotency contract.

In non-production only, an address ending in `@failure.test` triggers the recoverable provider-failure path for browser evidence.
