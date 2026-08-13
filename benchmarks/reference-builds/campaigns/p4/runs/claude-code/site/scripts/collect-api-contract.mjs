/**
 * form-mutation-design + rate-limit-abuse-control + failure-resilience
 * evidence, exercised directly against the running production build.
 *
 * Instances:
 *   3100  normal (rate capacity raised for the suite)
 *   3101  production-default rate capacity of 5
 *   3102  ASTERIA_STORE_MODE=fail
 *   3103  ASTERIA_BROKER_MODE=fail
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { randomUUID } from "node:crypto";

const OUT = "../evidence/browser";
mkdirSync(OUT, { recursive: true });
const ADMIN = { "x-asteria-admin-key": process.env.ASTERIA_ADMIN_KEY ?? "bench-p4-admin-key-3f9c2a71" };

const problems = [];
const cases = [];

const post = (base, body, headers = {}) =>
  fetch(`${base}/api/visit-requests`, {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json", ...headers },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });

const stats = async (base) => (await fetch(`${base}/api/visit-requests/_stats`, { headers: ADMIN })).json();

const valid = (over = {}) => ({
  name: "Contract Case",
  email: `contract.${randomUUID().slice(0, 8)}@example.com`,
  timeframe: "3-6-months",
  context: "primary-home",
  consent: true,
  idempotencyKey: randomUUID(),
  ...over,
});

async function record(id, description, run) {
  const result = await run();
  cases.push({ id, description, ...result });
  if (result.ok === false) problems.push(`${id}: ${result.why}`);
  console.log(`${result.ok === false ? "FAIL" : "ok  "}  ${id}`);
}

const B = "http://localhost:3100";

await record("method-not-allowed", "GET /api/visit-requests", async () => {
  const response = await fetch(`${B}/api/visit-requests`);
  return {
    status: response.status,
    allow: response.headers.get("allow"),
    ok: response.status === 405,
    why: `expected 405, got ${response.status}`,
  };
});

await record("unsupported-media-type", "POST text/plain", async () => {
  const response = await fetch(`${B}/api/visit-requests`, {
    method: "POST",
    headers: { "content-type": "text/plain", accept: "application/json" },
    body: "hello",
  });
  return { status: response.status, ok: response.status === 415, why: `expected 415, got ${response.status}` };
});

await record("malformed-json", "POST broken JSON", async () => {
  const response = await post(B, "{not json");
  const body = await response.json();
  return { status: response.status, body, ok: response.status === 400, why: `expected 400, got ${response.status}` };
});

await record("payload-too-large", "POST 20 KB body", async () => {
  const response = await post(B, valid({ message: "x".repeat(20_000) }));
  return { status: response.status, ok: response.status === 413, why: `expected 413, got ${response.status}` };
});

await record("validation-required-fields", "POST empty object", async () => {
  const response = await post(B, { idempotencyKey: randomUUID() });
  const body = await response.json();
  const fields = Object.keys(body.fields ?? {});
  const expected = ["name", "email", "timeframe", "context", "consent"];
  const missing = expected.filter((f) => !fields.includes(f));
  return {
    status: response.status,
    fields: body.fields,
    ok: response.status === 422 && missing.length === 0,
    why: `status ${response.status}, missing field errors: ${missing.join(", ")}`,
  };
});

await record("validation-unknown-residence", "POST residenceId=A99 vs A11", async () => {
  const bad = await post(B, valid({ residenceId: "A99" }));
  const badBody = await bad.json();
  const good = await post(B, valid({ residenceId: "A11" }));
  return {
    unknownStatus: bad.status,
    unknownFields: badBody.fields,
    knownStatus: good.status,
    ok: bad.status === 422 && good.status === 201,
    why: `unknown ${bad.status} (expect 422), known ${good.status} (expect 201)`,
  };
});

await record("validation-consent-false", "POST consent=false", async () => {
  const response = await post(B, valid({ consent: false }));
  const body = await response.json();
  return {
    status: response.status,
    fields: body.fields,
    ok: response.status === 422 && Boolean(body.fields?.consent),
    why: `status ${response.status}`,
  };
});

await record("honeypot-discarded", "POST with honeypot filled", async () => {
  const before = await stats(B);
  const response = await post(B, valid({ website: "https://spam.example" }));
  const body = await response.json();
  const after = await stats(B);
  return {
    status: response.status,
    body,
    rowsCreated: after.visitRequests - before.visitRequests,
    ok: response.status === 200 && after.visitRequests === before.visitRequests,
    why: `status ${response.status}, rows +${after.visitRequests - before.visitRequests}`,
  };
});

await record("too-fast", "POST rendered <2s ago", async () => {
  const response = await post(B, valid({ renderedAt: Date.now() }));
  return { status: response.status, ok: response.status === 429, why: `expected 429, got ${response.status}` };
});

await record("idempotent-replay", "same idempotencyKey twice", async () => {
  const payload = valid();
  const before = await stats(B);
  const first = await (await post(B, payload)).json();
  const second = await (await post(B, payload)).json();
  const after = await stats(B);
  return {
    firstReference: first.reference,
    secondReference: second.reference,
    secondDuplicate: second.duplicate,
    rowsCreated: after.visitRequests - before.visitRequests,
    eventsCreated: after.conversionEvents - before.conversionEvents,
    ok:
      first.reference === second.reference &&
      second.duplicate === true &&
      after.visitRequests - before.visitRequests === 1 &&
      after.conversionEvents - before.conversionEvents === 1,
    why: `refs ${first.reference}/${second.reference}, rows +${after.visitRequests - before.visitRequests}`,
  };
});

await record("same-day-dedupe", "same email+residence, new key", async () => {
  const email = `sameday.${randomUUID().slice(0, 8)}@example.com`;
  const before = await stats(B);
  const first = await (await post(B, valid({ email, residenceId: "A02" }))).json();
  const second = await (await post(B, valid({ email, residenceId: "A02" }))).json();
  const after = await stats(B);
  return {
    firstReference: first.reference,
    second,
    rowsCreated: after.visitRequests - before.visitRequests,
    ok: second.duplicate === true && after.visitRequests - before.visitRequests === 1,
    why: `duplicate=${second.duplicate}, rows +${after.visitRequests - before.visitRequests}`,
  };
});

await record("parallel-submit", "8 concurrent identical POSTs", async () => {
  const payload = valid();
  const before = await stats(B);
  const responses = await Promise.all(Array.from({ length: 8 }, () => post(B, payload)));
  const bodies = await Promise.all(responses.map((r) => r.json()));
  const after = await stats(B);
  const references = new Set(bodies.map((b) => b.reference));
  return {
    statuses: responses.map((r) => r.status),
    distinctReferences: [...references],
    rowsCreated: after.visitRequests - before.visitRequests,
    eventsCreated: after.conversionEvents - before.conversionEvents,
    ok:
      references.size === 1 &&
      after.visitRequests - before.visitRequests === 1 &&
      after.conversionEvents - before.conversionEvents === 1,
    why: `${references.size} distinct references, rows +${after.visitRequests - before.visitRequests}`,
  };
});

await record("rate-limit", "7 sequential submits at capacity 5", async () => {
  const R = "http://localhost:3101";
  const statuses = [];
  let retryAfter = null;
  for (let i = 0; i < 7; i += 1) {
    const response = await post(R, valid());
    statuses.push(response.status);
    if (response.status === 429) retryAfter = response.headers.get("retry-after");
  }
  const accepted = statuses.filter((s) => s === 201).length;
  const limited = statuses.filter((s) => s === 429).length;
  return {
    statuses,
    accepted,
    limited,
    retryAfter,
    ok: accepted === 5 && limited === 2 && retryAfter !== null,
    why: `accepted ${accepted} (expect 5), limited ${limited} (expect 2), retry-after ${retryAfter}`,
  };
});

await record("store-failure", "instance with ASTERIA_STORE_MODE=fail", async () => {
  const S = "http://localhost:3102";
  const before = await stats(S);
  const response = await post(S, valid());
  const body = await response.json();
  const after = await stats(S);
  return {
    status: response.status,
    body,
    rowsCreated: after.visitRequests - before.visitRequests,
    ok:
      response.status === 503 &&
      body.ok === false &&
      /NOT recorded/i.test(body.message) &&
      after.visitRequests === before.visitRequests,
    why: `status ${response.status}, ok=${body.ok}, rows +${after.visitRequests - before.visitRequests}`,
  };
});

await record("broker-failure", "instance with ASTERIA_BROKER_MODE=fail", async () => {
  const K = "http://localhost:3103";
  const response = await post(K, valid());
  const body = await response.json();
  const readback = await (
    await fetch(`${K}/api/visit-requests/${body.reference}`, { headers: ADMIN })
  ).json();
  return {
    status: response.status,
    notification: body.notification,
    stored: readback.record,
    ok:
      response.status === 201 &&
      body.notification === "failed" &&
      readback.record?.status === "received" &&
      readback.record?.notification_status === "failed" &&
      readback.record?.notification_error === "simulated_broker_failure",
    why: `notification=${body.notification}, stored=${readback.record?.notification_status}`,
  };
});

await record("admin-endpoint-protected", "GET without / with a bad key", async () => {
  const noKey = await fetch(`${B}/api/visit-requests/_stats`);
  const badKey = await fetch(`${B}/api/visit-requests/_stats`, {
    headers: { "x-asteria-admin-key": "not-the-key-at-all-padd" },
  });
  const goodKey = await fetch(`${B}/api/visit-requests/_stats`, { headers: ADMIN });
  return {
    noKeyStatus: noKey.status,
    badKeyStatus: badKey.status,
    goodKeyStatus: goodKey.status,
    ok: noKey.status === 401 && badKey.status === 401 && goodKey.status === 200,
    why: `${noKey.status}/${badKey.status}/${goodKey.status}`,
  };
});

await record("unknown-reference", "GET an invented reference", async () => {
  const response = await fetch(`${B}/api/visit-requests/AST-00000000`, { headers: ADMIN });
  return { status: response.status, ok: response.status === 404, why: `expected 404, got ${response.status}` };
});

await record("events-conversion-rejected", "POST conversion event from client", async () => {
  const rejected = await fetch(`${B}/api/events`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ name: "conversion.visit_request.submitted", sessionId: "fake" }),
  });
  const accepted = await fetch(`${B}/api/events`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ name: "residence_detail_viewed", sessionId: randomUUID(), subject: "A04" }),
  });
  return {
    conversionStatus: rejected.status,
    funnelStatus: accepted.status,
    ok: rejected.status === 422 && accepted.status === 204,
    why: `conversion ${rejected.status} (expect 422), funnel ${accepted.status} (expect 204)`,
  };
});

await record("conversion-parity", "events == leads on the primary instance", async () => {
  const s = await stats(B);
  return {
    ...s,
    ok: s.visitRequests === s.conversionEvents,
    why: `${s.visitRequests} leads vs ${s.conversionEvents} conversion events`,
  };
});

writeFileSync(
  `${OUT}/api-contract.json`,
  JSON.stringify({ generatedAt: new Date().toISOString(), cases, problems }, null, 2),
);

console.log(`\ncases: ${cases.length}`);
console.log(problems.length ? `PROBLEMS:\n- ${problems.join("\n- ")}` : "no problems found");
process.exit(problems.length ? 1 : 0);
