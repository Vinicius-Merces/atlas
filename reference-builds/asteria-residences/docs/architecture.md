# Architecture

Asteria uses static public pages plus a small Python HTTP service so the benchmark behavior stays inspectable.

- Public assets live in `site/`.
- `server.py` serves the site and owns `POST /api/leads`.
- Lead validation is repeated on the server.
- An idempotency key prevents repeated effects for one request intent.
- A per-IP sliding window limits mutation frequency.
- Accepted leads are persisted as private JSONL data in this controlled reference environment before success is returned.
- A test-only failure mode is disabled unless explicitly enabled by environment variable.
- Client assets contain no credentials or stored lead records.

JSONL is a benchmark storage boundary, not a recommendation for a production CRM. A deployed project would replace the persistence adapter without changing the public form contract.
