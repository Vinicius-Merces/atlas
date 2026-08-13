# Web Production Assurance Review Gate

## Scope

Independently evaluate a significant public web release across critical browser behavior, technical crawl/index health, structured-data truth, and changed dependency/build-input supply-chain risk.

This review complements frontend craft and SaaS trust. A page can be visually excellent and secure yet still fail critical browser journeys or be accidentally non-indexable.

## Required evidence

- Request, acceptance criteria, risk, and affected paths
- Critical-journey browser results and diagnostics
- Representative deployed HTTP responses and redirect evidence when public discovery matters
- Robots/noindex, sitemap, canonical, rendered metadata/content evidence when applicable
- Structured-data parser/validator and truth-source evidence when applicable
- Dependency/lockfile/build-input diff and advisory/script/provenance evidence when applicable
- Adjacent frontend craft, SaaS trust, accessibility, performance, privacy, or release evidence required by scope

Missing mandatory release-critical evidence prevents an unconditional Approved outcome.

## Review questions

### Browser journeys

- Are the release-critical journeys identified rather than inferred from implementation?
- Were they exercised in a real rendered browser from controlled state?
- Do assertions prove meaningful outcomes rather than only successful clicks?
- Are runtime exceptions, console errors, failed requests, unexpected redirects, loading/error states, and direct URL entry covered where material?
- Are failures reproducible from retained diagnostics?

### Crawl and index intent

- Which URLs are intended indexable, noindex, redirects, duplicates, errors, or private?
- Do status codes and redirects match that intent without loops or unnecessary chains?
- Do canonical, redirects, sitemap, robots meta/X-Robots-Tag, and `robots.txt` behavior conflict?
- Can important public pages and resources be fetched/rendered through the intended crawler path?
- Are important routes internally discoverable through crawlable links?

### Metadata and structured data

- Are public domain/canonical/title/description/locale values current and route-appropriate?
- Does every structured-data block describe the actual visible/authoritative page/entity facts?
- Are ratings, reviews, offers, prices, availability, authors, locations, and dates genuine?
- Are duplicate plugins/templates emitting conflicting canonical entities?
- Were generic schema validity and target search-feature validation both considered where applicable?

### Supply chain

- What direct/transitive dependency or build-input delta was introduced?
- Are registry/source/package identities intentional?
- Are known vulnerability/malware findings addressed proportionally to reach and severity?
- Did new lifecycle/install/build scripts or opaque binary/network behavior appear?
- Are CI actions/plugins/container bases and other executable build inputs governed with appropriate provenance/integrity/update controls?
- Is broad lockfile churn understood and reproducible?

## Findings

Record each finding with severity, evidence, affected journey/URL/entity/dependency, user/search/security impact, required remediation, and verification method. State `No findings` only after every applicable evidence source has been inspected.

## Severity

Use `.claude/contracts/review-contract.md`: Critical, High, Medium, Low, or Note.

Examples normally blocking until resolved or governed include a release-critical journey that cannot complete, accidental site/route-wide noindex or canonicalization away from intended content, materially deceptive structured data, malware evidence, or a critical reachable dependency vulnerability without an accepted exception.

## Required actions

For every finding, identify the correction, explicit product/security decision, or missing evidence required and how it will be verified. Critical or High findings must be resolved or explicitly governed before approval. Missing mandatory browser, deployed HTTP, structured-data truth, or supply-chain evidence is a required action rather than an assumption of safety.

## Outcome

Record exactly one outcome after required evidence and mandatory validation are complete:

- Approved
- Approved with conditions
- Changes required
- Blocked

The sole implementing agent may provide evidence and remediation but must not be the only approver of its own significant public-web assurance work.
