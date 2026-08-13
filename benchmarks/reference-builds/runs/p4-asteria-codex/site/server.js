import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { chmodSync, mkdirSync } from "node:fs";
import { dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import crypto from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { renderPage } from "./src/render.js";
import { absolute, residences, site } from "./src/content.js";

const root = fileURLToPath(new URL(".", import.meta.url));
const publicRoot = join(root, "public");
const assetRoot = resolve(root, "../assets");
const dataRoot = join(root, "data");
const port = Number(process.env.PORT || 4173);
const databasePath = process.env.ASTERIA_DB_PATH || (process.env.NODE_ENV === "test" ? ":memory:" : join(dataRoot, "asteria.sqlite"));

const mime = {
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".webp": "image/webp",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
};

const securityHeaders = {
  "content-security-policy": "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'",
  "referrer-policy": "strict-origin-when-cross-origin",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "permissions-policy": "camera=(), microphone=(), geolocation=()",
  "cross-origin-opener-policy": "same-origin",
};

function send(res, status, body, type = "application/json; charset=utf-8", extra = {}) {
  res.writeHead(status, { ...securityHeaders, "content-type": type, "cache-control": status === 200 && !type.includes("json") ? "public, max-age=300" : "no-store", ...extra });
  res.end(body);
}

function json(res, status, payload, extra = {}) {
  send(res, status, JSON.stringify(payload), "application/json; charset=utf-8", extra);
}

async function bodyJson(req) {
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > 16_384) throw Object.assign(new Error("Payload muito grande"), { status: 413 });
    chunks.push(chunk);
  }
  try { return JSON.parse(Buffer.concat(chunks).toString("utf8")); }
  catch { throw Object.assign(new Error("JSON inválido"), { status: 400 }); }
}

function normalize(input) {
  return {
    name: String(input.name || "").trim().replace(/\s+/g, " "),
    email: String(input.email || "").trim().toLowerCase(),
    phone: String(input.phone || "").replace(/\D/g, ""),
    interest: String(input.interest || ""),
    budget: String(input.budget || ""),
    visitDate: String(input.visitDate || ""),
    consent: input.consent === true,
    company: String(input.company || "").trim(),
  };
}

export function validateLead(input, now = new Date()) {
  const data = normalize(input);
  const errors = {};
  if (data.name.length < 3 || data.name.length > 90) errors.name = "Informe seu nome completo.";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email) || data.email.length > 160) errors.email = "Informe um e-mail válido.";
  if (data.phone.length < 10 || data.phone.length > 13) errors.phone = "Informe um telefone com DDD.";
  const interests = new Set([...residences.map((r) => r.slug), "a-definir"]);
  if (!interests.has(data.interest)) errors.interest = "Selecione uma opção de interesse.";
  if (!new Set(["ate-5m", "5m-7m", "acima-7m"]).has(data.budget)) errors.budget = "Selecione uma faixa de investimento.";
  if (data.visitDate) {
    const date = new Date(`${data.visitDate}T12:00:00Z`);
    const floor = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
    if (Number.isNaN(date.valueOf()) || date < floor) errors.visitDate = "Escolha uma data futura.";
  }
  if (!data.consent) errors.consent = "Precisamos da sua autorização para responder.";
  if (data.company) errors.form = "Não foi possível enviar esta solicitação.";
  return { data, errors, valid: Object.keys(errors).length === 0 };
}

export class AsteriaStore {
  constructor(path = databasePath) {
    if (path !== ":memory:") mkdirSync(dirname(path), { recursive: true });
    this.db = new DatabaseSync(path);
    this.db.exec("PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON;");
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL,
        interest TEXT NOT NULL, budget TEXT NOT NULL, visit_date TEXT, consent INTEGER NOT NULL,
        created_at TEXT NOT NULL, status TEXT NOT NULL, source TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS leads_identity_time ON leads(email, phone, created_at DESC);
      CREATE TABLE IF NOT EXISTS idempotency (
        key TEXT PRIMARY KEY, result_json TEXT NOT NULL, created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS analytics_outbox (
        id TEXT PRIMARY KEY, event TEXT NOT NULL, properties_json TEXT NOT NULL,
        created_at TEXT NOT NULL, delivered_at TEXT
      );
      CREATE TABLE IF NOT EXISTS rate_events (
        actor_hash TEXT NOT NULL, scope TEXT NOT NULL, occurred_at INTEGER NOT NULL
      );
      CREATE INDEX IF NOT EXISTS rate_window ON rate_events(actor_hash, scope, occurred_at);
    `);
    if (path !== ":memory:") chmodSync(path, 0o600);
  }

  idempotentResult(key) {
    const row = this.db.prepare("SELECT result_json FROM idempotency WHERE key = ?").get(key);
    return row ? JSON.parse(row.result_json) : null;
  }

  rateAllowed(actorHash, scope, maximum, windowMs) {
    const now = Date.now();
    const start = now - windowMs;
    this.db.exec("BEGIN IMMEDIATE");
    try {
      this.db.prepare("DELETE FROM rate_events WHERE occurred_at < ?").run(start);
      const row = this.db.prepare("SELECT COUNT(*) AS count, MIN(occurred_at) AS oldest FROM rate_events WHERE actor_hash = ? AND scope = ? AND occurred_at >= ?").get(actorHash, scope, start);
      if (Number(row.count) >= maximum) {
        this.db.exec("COMMIT");
        return { allowed: false, retryAfter: Math.max(1, Math.ceil((windowMs - (now - Number(row.oldest))) / 1000)) };
      }
      this.db.prepare("INSERT INTO rate_events(actor_hash, scope, occurred_at) VALUES (?, ?, ?)").run(actorHash, scope, now);
      this.db.exec("COMMIT");
      return { allowed: true, retryAfter: 0 };
    } catch (error) {
      this.db.exec("ROLLBACK");
      throw error;
    }
  }

  acceptLead(key, data) {
    const now = new Date();
    const createdAt = now.toISOString();
    const recentBoundary = new Date(now.valueOf() - 86_400_000).toISOString();
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const existingKey = this.db.prepare("SELECT result_json FROM idempotency WHERE key = ?").get(key);
      if (existingKey) {
        this.db.exec("COMMIT");
        return { created: false, result: { ...JSON.parse(existingKey.result_json), duplicate: true } };
      }
      const recent = this.db.prepare("SELECT id FROM leads WHERE email = ? AND phone = ? AND created_at >= ? ORDER BY created_at DESC LIMIT 1").get(data.email, data.phone, recentBoundary);
      if (recent) {
        const result = { ok: true, leadId: recent.id, status: "received", duplicate: true, message: "Sua solicitação já foi recebida. Usaremos o primeiro registro para entrar em contato." };
        this.db.prepare("INSERT INTO idempotency(key, result_json, created_at) VALUES (?, ?, ?)").run(key, JSON.stringify(result), createdAt);
        this.db.exec("COMMIT");
        return { created: false, result };
      }
      const leadId = `ast_${crypto.randomUUID()}`;
      this.db.prepare("INSERT INTO leads(id,name,email,phone,interest,budget,visit_date,consent,created_at,status,source) VALUES (?,?,?,?,?,?,?,?,?,?,?)")
        .run(leadId, data.name, data.email, data.phone, data.interest, data.budget, data.visitDate || null, 1, createdAt, "received", "website");
      const eventId = `evt_${crypto.randomUUID()}`;
      this.db.prepare("INSERT INTO analytics_outbox(id,event,properties_json,created_at) VALUES (?,?,?,?)")
        .run(eventId, "lead_authoritative_success", JSON.stringify({ leadId, interest: data.interest, budget: data.budget }), createdAt);
      const result = { ok: true, leadId, status: "received", message: "Solicitação recebida. Nossa equipe responderá em até um dia útil." };
      this.db.prepare("INSERT INTO idempotency(key, result_json, created_at) VALUES (?, ?, ?)").run(key, JSON.stringify(result), createdAt);
      this.db.exec("COMMIT");
      return { created: true, result };
    } catch (error) {
      this.db.exec("ROLLBACK");
      throw error;
    }
  }

  track(event, properties = {}) {
    this.db.prepare("INSERT INTO analytics_outbox(id,event,properties_json,created_at) VALUES (?,?,?,?)")
      .run(`evt_${crypto.randomUUID()}`, event, JSON.stringify(properties), new Date().toISOString());
  }

  close() { this.db.close(); }
}

export const store = new AsteriaStore();

function actorHash(req) {
  const forwarded = process.env.TRUST_PROXY === "true" ? String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() : "";
  const address = forwarded || req.socket.remoteAddress || "unknown";
  return crypto.createHash("sha256").update(address).digest("hex");
}

function sameOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return true;
  try { return new URL(origin).host === req.headers.host; } catch { return false; }
}

async function handleLead(req, res) {
  if (!sameOrigin(req)) return json(res, 403, { ok: false, message: "Origem não autorizada." });
  const key = String(req.headers["idempotency-key"] || "");
  if (!/^[a-zA-Z0-9_-]{16,80}$/.test(key)) return json(res, 400, { ok: false, message: "Identificador de envio ausente." });
  const existing = store.idempotentResult(key);
  if (existing) return json(res, 200, { ...existing, duplicate: true });
  const limit = store.rateAllowed(actorHash(req), "lead", 5, 10 * 60 * 1000);
  if (!limit.allowed) return json(res, 429, { ok: false, message: "Muitas tentativas. Aguarde alguns minutos antes de tentar novamente." }, { "retry-after": String(limit.retryAfter) });
  let input;
  try { input = await bodyJson(req); } catch (error) { return json(res, error.status || 400, { ok: false, message: error.message }); }
  const validation = validateLead(input);
  if (!validation.valid) return json(res, 422, { ok: false, message: "Revise os campos destacados.", errors: validation.errors });
  if (process.env.NODE_ENV !== "production" && validation.data.email.endsWith("@failure.test")) {
    return json(res, 503, { ok: false, code: "PROVIDER_UNAVAILABLE", message: "A agenda está temporariamente indisponível. Seus dados não foram registrados; tente novamente em instantes." }, { "retry-after": "30" });
  }
  try {
    const accepted = store.acceptLead(key, validation.data);
    return json(res, accepted.created ? 201 : 200, accepted.result);
  } catch {
    return json(res, 503, { ok: false, code: "PERSISTENCE_FAILURE", message: "Não foi possível confirmar o registro. Seus dados não foram salvos; tente novamente." }, { "retry-after": "30" });
  }
}

function robots() {
  return `User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: ${absolute("/sitemap.xml")}\n`;
}

function sitemap() {
  const paths = ["/", "/residencias", ...residences.map((r) => `/residencias/${r.slug}`), "/localizacao", "/caderno", "/caderno/viver-entre-cidade-e-paisagem", "/caderno/arquitetura-que-envelhece-bem", "/caderno/doze-casas-uma-paisagem", "/contato", "/privacidade", "/termos"];
  return `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map((path) => `<url><loc>${absolute(path)}</loc><changefreq>${path.startsWith("/caderno/") ? "monthly" : "weekly"}</changefreq></url>`).join("")}</urlset>`;
}

async function staticFile(reqPath, res) {
  const clean = reqPath.replace(/^\/+/, "");
  const base = clean.startsWith("assets/") ? assetRoot : publicRoot;
  const relative = clean.startsWith("assets/") ? clean.slice(7) : clean;
  const path = resolve(base, relative);
  if (!path.startsWith(resolve(base))) return false;
  try {
    const body = await readFile(path);
    send(res, 200, body, mime[extname(path)] || "application/octet-stream", { "cache-control": clean.startsWith("assets/") ? "public, max-age=31536000, immutable" : "public, max-age=300" });
    return true;
  } catch { return false; }
}

export const server = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || `localhost:${port}`}`);
  if (req.method === "GET" && url.pathname === "/api/health") return json(res, 200, { ok: true, service: "asteria-lead-intake", persistence: "sqlite" });
  if (req.method === "POST" && url.pathname === "/api/leads") return handleLead(req, res);
  if (req.method === "POST" && url.pathname === "/api/analytics") {
    if (!sameOrigin(req)) return json(res, 403, { ok: false });
    const limit = store.rateAllowed(actorHash(req), "analytics", 60, 10 * 60 * 1000);
    if (!limit.allowed) return json(res, 429, { ok: false }, { "retry-after": String(limit.retryAfter) });
    let input; try { input = await bodyJson(req); } catch { return json(res, 400, { ok: false }); }
    const allowed = new Set(["page_view", "lead_form_start", "residence_view"]);
    if (!allowed.has(input.event)) return json(res, 422, { ok: false });
    store.track(input.event, { path: String(input.path || "").slice(0, 160) });
    return json(res, 202, { ok: true });
  }
  if (req.method === "GET" && url.pathname === "/robots.txt") return send(res, 200, robots(), "text/plain; charset=utf-8");
  if (req.method === "GET" && url.pathname === "/sitemap.xml") return send(res, 200, sitemap(), "application/xml; charset=utf-8");
  if (req.method === "GET" && (url.pathname.startsWith("/assets/") || ["/styles.css", "/app.js"].includes(url.pathname))) {
    if (await staticFile(url.pathname, res)) return;
  }
  if (req.method !== "GET" && req.method !== "HEAD") return json(res, 405, { ok: false, message: "Método não permitido." }, { allow: "GET, HEAD, POST" });
  const page = renderPage(url);
  send(res, page.status, req.method === "HEAD" ? "" : page.html, "text/html; charset=utf-8", { "cache-control": "public, max-age=60" });
});

if (process.env.NODE_ENV !== "test") {
  server.listen(port, "0.0.0.0", () => console.log(`Asteria listening on http://0.0.0.0:${port}`));
}
