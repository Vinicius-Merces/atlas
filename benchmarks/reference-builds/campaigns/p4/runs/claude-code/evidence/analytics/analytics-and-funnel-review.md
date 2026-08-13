# Analytics implementation audit and conversion funnel review

Capabilities: `analytics-implementation-audit`, `conversion-funnel-review`
Checks: `marketing-analytics`, and the funnel half of `marketing-audience-outcome`

## 1. The measurement architecture, and why it is shaped this way

There is **no third-party analytics script on this site** — no tag manager, no
pixel, no session recorder. Two reasons, in order of weight:

1. The fixture's decisive constraint is that *a client-side success toast is not
   proof that a lead reached authoritative downstream state*. A client-emitted
   `conversion` event has exactly the same defect: it is a claim made by the
   browser about something only the server can know. So the conversion event is
   written **by the server, inside the same SQLite transaction as the lead row**.
2. A privacy notice that promises no third-party tracking has to be true. It is
   (verified: `evidence/security/secret-and-header-audit.json` → no external
   origins referenced in the served HTML; the CSP restricts `connect-src` to
   `'self'`).

## 2. Event taxonomy

| Event | Emitted by | Keyed / deduplicated by | Meaning |
| --- | --- | --- | --- |
| `residence_detail_viewed` | client `sendBeacon` → `POST /api/events` | `name:sessionId:residenceId`, `UNIQUE` index | a specific residence was actually opened |
| `enquire_opened` | client `sendBeacon` → `POST /api/events` | `name:sessionId:-`, `UNIQUE` index | the conversion surface was reached |
| `conversion.visit_request.submitted` | **server**, inside the lead transaction | `conversion.visit_request.submitted:<reference>`, `UNIQUE` index | a lead exists in authoritative state |

`POST /api/events` accepts only the two funnel steps. A client that posts
`conversion.visit_request.submitted` is answered **422** — verified as case
`events-conversion-rejected` in `evidence/browser/api-contract.json`. A false
conversion cannot be manufactured from the browser.

## 3. The properties that make the funnel decision-useful

Every lead row carries `residence_id`, `timeframe` and `context`. Those are the
three axes the sales team actually segments on: *which house*, *how soon*, and
*owner-occupier / second home / investor / broker*. They are on the form because
they change what the broker does next, not to lengthen the form — which is why
the other four fields are optional and labelled as such.

## 4. No duplicate and no false-success events

| Property | How it is guaranteed | Evidence |
| --- | --- | --- |
| One conversion event per lead | same transaction, `UNIQUE` dedupe key on the reference | `api-contract.json` → `idempotent-replay`, `parallel-submit`, `conversion-parity` |
| No event when the store fails | the event insert is inside the transaction that rolled back | `api-contract.json` → `store-failure` (rows +0) |
| No event for a honeypot submission | nothing is written at all | `api-contract.json` → `honeypot-discarded` (rows +0) |
| No double-count under concurrency | 8 parallel identical POSTs → 1 row, 1 event | `api-contract.json` → `parallel-submit` |
| Broker failure does not suppress the conversion | the lead happened; only the hand-off is degraded | `api-contract.json` → `broker-failure` |

The `conversion-parity` case asserts the invariant directly:
`COUNT(visit_request) === COUNT(funnel_event WHERE name='conversion...')` on the
primary instance after the whole suite has run. It held.

## 5. Funnel review — friction, and what was removed

The journey is: **home → index → residence detail → request a visit → reference**.

| Step | Friction removed | Friction deliberately kept |
| --- | --- | --- |
| Home → index | The twelve are listed *on the home page* with real areas and prices, so the first click is already qualified | — |
| Index → detail | Filters are a plain GET form: linkable, shareable, works without JS | — |
| Detail → form | The CTA carries the residence (`/enquire?residence=A04`) and the field arrives pre-selected | — |
| Form | 5 required fields; the rest optional and labelled `optional` | Explicit consent checkbox — an unticked box is a real barrier and it stays, because pre-ticked consent is a dark pattern |
| Submission | Server reference issued immediately; no email round-trip needed to have a handle | 2-second minimum time-to-submit (invisible to a human) |
| After | Reference is selectable text, and quoted in the follow-up path | — |

### Dark patterns explicitly not used

No fake scarcity ("2 left!"), no countdown, no invented "34 people viewed this",
no pre-ticked marketing consent, no interstitial that blocks content behind an
email, no exit-intent modal, no cookie wall. Sold and reserved houses stay
listed and keep their pages — the opposite of the usual pattern, and the reason
the index can be trusted.

### Honest asymmetry

Requesting a visit consents to *answering that request only*. Marketing contact
would need a separate opt-in, and this form does not ask for one, so the site
cannot harvest a mailing list from its conversion. That costs list growth; it is
the correct trade for an audience whose main anxiety about a property form is
what happens to their details afterwards.

## 6. Residual measurement limitations

- Funnel steps depend on `sessionStorage` for a session id; where storage is
  blocked the event is still sent with `no-storage` and simply cannot be
  stitched into a session. Degrades measurement, never the page.
- `sendBeacon` is fire-and-forget: a beacon lost on a flaky network is an
  under-count of funnel steps. The conversion count is unaffected, because it
  never travels over that path.
- There is no attribution model (no campaign parameters are captured) because
  the brief has no acquisition channels defined. Adding UTM capture would be
  measurement theatre against requirements that do not exist yet.
