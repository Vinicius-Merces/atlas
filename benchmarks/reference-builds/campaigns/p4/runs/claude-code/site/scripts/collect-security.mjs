/**
 * secret-environment-audit evidence + response-header verification.
 *
 * Proves that no server secret, lead datum, or private provider configuration
 * is reachable from the browser.
 */
import { writeFileSync, mkdirSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const BASE = process.env.ASTERIA_BASE_URL ?? "http://localhost:3100";
const OUT = "../evidence/security";
mkdirSync(OUT, { recursive: true });

const problems = [];

// --- 1. Client bundle scan -------------------------------------------------
const SECRET_MARKERS = [
  { id: "admin-key", pattern: /bench-p4-admin-key-[a-z0-9]+/i },
  { id: "admin-key-env-name", pattern: /ASTERIA_ADMIN_KEY/ },
  { id: "broker-webhook-env-name", pattern: /ASTERIA_BROKER_WEBHOOK/ },
  { id: "ip-salt", pattern: /ASTERIA_IP_SALT|bench-p4-salt/ },
  { id: "db-path", pattern: /ASTERIA_DB_PATH|asteria\.db|primary\.db/ },
  { id: "sqlite-import", pattern: /node:sqlite/ },
  { id: "lead-email-domain", pattern: /benchmark\.buyer\.|contract\.[a-f0-9]{8}@example\.com/ },
];

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

const clientAssets = walk(".next/static").filter((f) => /\.(js|css|map)$/.test(f));
const bundleFindings = [];
for (const file of clientAssets) {
  const content = readFileSync(file, "utf8");
  for (const marker of SECRET_MARKERS) {
    if (marker.pattern.test(content)) {
      bundleFindings.push({ file, marker: marker.id });
      problems.push(`client asset ${file} contains ${marker.id}`);
    }
  }
}

// --- 2. Served HTML scan ---------------------------------------------------
const htmlFindings = [];
for (const route of ["/", "/residences/ridge-house-04", "/enquire", "/privacy"]) {
  const html = await (await fetch(`${BASE}${route}`)).text();
  for (const marker of SECRET_MARKERS) {
    if (marker.pattern.test(html)) {
      htmlFindings.push({ route, marker: marker.id });
      problems.push(`${route} HTML contains ${marker.id}`);
    }
  }
}

// --- 3. Lead data is not readable without the key --------------------------
const leakProbes = [];
for (const path of [
  "/api/visit-requests/_stats",
  "/api/visit-requests/AST-00000000",
  "/data/asteria.db",
  "/data/primary.db",
  "/.env",
  "/.env.production",
  "/.next/server/app/page.js",
]) {
  const response = await fetch(`${BASE}${path}`);
  const text = (await response.text()).slice(0, 200);
  leakProbes.push({ path, status: response.status, sample: text });
  if (path.startsWith("/api/") && response.status === 200) {
    problems.push(`${path} readable without a key`);
  }
  if (!path.startsWith("/api/") && response.status === 200) {
    problems.push(`${path} is publicly served`);
  }
}

// --- 4. Security headers on a real response --------------------------------
const headResponse = await fetch(`${BASE}/`);
const headers = Object.fromEntries(headResponse.headers.entries());
const REQUIRED_HEADERS = {
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "referrer-policy": "strict-origin-when-cross-origin",
};
for (const [key, value] of Object.entries(REQUIRED_HEADERS)) {
  if (headers[key] !== value) problems.push(`header ${key} is "${headers[key]}", expected "${value}"`);
}
const csp = headers["content-security-policy"] ?? "";
for (const directive of [
  "default-src 'self'",
  "frame-ancestors 'none'",
  "object-src 'none'",
  "form-action 'self'",
  "base-uri 'self'",
]) {
  if (!csp.includes(directive)) problems.push(`CSP missing "${directive}"`);
}
if (headers["x-powered-by"]) problems.push("x-powered-by header is present");

// --- 5. No third-party origins are contacted -------------------------------
const html = await (await fetch(`${BASE}/`)).text();
const externalOrigins = [
  ...new Set(
    (html.match(/https?:\/\/[a-z0-9.-]+/gi) ?? [])
      .map((u) => u.toLowerCase())
      .filter(
        (u) =>
          !u.includes("asteria-residences.example") &&
          !u.includes("schema.org") &&
          !u.includes("localhost") &&
          !u.includes("www.w3.org"),
      ),
  ),
];
if (externalOrigins.length) {
  problems.push(`unexpected external origins referenced: ${externalOrigins.join(", ")}`);
}

const report = {
  base: BASE,
  generatedAt: new Date().toISOString(),
  clientAssetsScanned: clientAssets.length,
  secretMarkersSearched: SECRET_MARKERS.map((m) => m.id),
  bundleFindings,
  htmlFindings,
  leakProbes,
  headers,
  externalOriginsInHtml: externalOrigins,
  problems,
};
writeFileSync(`${OUT}/secret-and-header-audit.json`, JSON.stringify(report, null, 2));

console.log(`client assets scanned: ${clientAssets.length}`);
console.log(`secret markers searched: ${SECRET_MARKERS.length}`);
console.log(problems.length ? `PROBLEMS:\n- ${problems.join("\n- ")}` : "no problems found");
process.exit(problems.length ? 1 : 0);
