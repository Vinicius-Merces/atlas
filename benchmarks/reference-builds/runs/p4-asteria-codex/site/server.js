import { createServer } from "node:http";
import { readFile, mkdir, rename, writeFile, appendFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import crypto from "node:crypto";
import { renderPage } from "./src/render.js";
import { absolute, residences, site } from "./src/content.js";

const root = fileURLToPath(new URL(".", import.meta.url));
const publicRoot = join(root, "public");
const assetRoot = resolve(root, "../assets");
const dataRoot = join(root, "data");
const leadsFile = join(dataRoot, "leads.json");
const analyticsFile = join(dataRoot, "analytics.jsonl");
const port = Number(process.env.PORT || 4173);
const limits = new Map();
const idempotency = new Map();

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

function clientIp(req) {
  return String(req.headers["x-forwarded-for"] || req.socket.remoteAddress || "unknown").split(",")[0].trim();
}

function rateAllowed(key) {
  const now = Date.now();
  const windowMs = 10 * 60 * 1000;
  const previous = (limits.get(key) || []).filter((time) => now - time < windowMs);
  previous.push(now);
  limits.set(key, previous);
  return { allowed: previous.length <= 5, retryAfter: Math.ceil((windowMs - (now - previous[0])) / 1000) };
}

async function loadLeads() {
  if (!existsSync(leadsFile)) return [];
  try { return JSON.parse(await readFile(leadsFile, "utf8")); } catch { return []; }
}

async function persistLead(lead) {
  await mkdir(dataRoot, { recursive: true });
  const leads = await loadLeads();
  leads.push(lead);
  const temporary = `${leadsFile}.${process.pid}.tmp`;
  await writeFile(temporary, `${JSON.stringify(leads, null, 2)}\n`, { mode: 0o600 });
  await rename(temporary, leadsFile);
}

async function track(event, properties = {}) {
  await mkdir(dataRoot, { recursive: true });
  await appendFile(analyticsFile, `${JSON.stringify({ event, properties, at: new Date().toISOString() })}\n`, { mode: 0o600 });
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
  if (idempotency.has(key)) return json(res, 200, { ...idempotency.get(key), duplicate: true });
  const limit = rateAllowed(clientIp(req));
  if (!limit.allowed) return json(res, 429, { ok: false, message: "Muitas tentativas. Aguarde alguns minutos antes de tentar novamente." }, { "retry-after": String(limit.retryAfter) });
  let input;
  try { input = await bodyJson(req); } catch (error) { return json(res, error.status || 400, { ok: false, message: error.message }); }
  const validation = validateLead(input);
  if (!validation.valid) return json(res, 422, { ok: false, message: "Revise os campos destacados.", errors: validation.errors });
  if (process.env.NODE_ENV !== "production" && validation.data.email.endsWith("@failure.test")) {
    return json(res, 503, { ok: false, code: "PROVIDER_UNAVAILABLE", message: "A agenda está temporariamente indisponível. Seus dados não foram registrados; tente novamente em instantes." }, { "retry-after": "30" });
  }
  const leads = await loadLeads();
  const recent = leads.find((lead) => lead.email === validation.data.email && lead.phone === validation.data.phone && Date.now() - new Date(lead.createdAt).valueOf() < 86_400_000);
  if (recent) {
    const result = { ok: true, leadId: recent.id, status: "received", duplicate: true, message: "Sua solicitação já foi recebida. Usaremos o primeiro registro para entrar em contato." };
    idempotency.set(key, result);
    return json(res, 200, result);
  }
  const lead = { id: `ast_${crypto.randomUUID()}`, ...validation.data, company: undefined, createdAt: new Date().toISOString(), status: "received", source: "website" };
  try {
    await persistLead(lead);
    await track("lead_authoritative_success", { leadId: lead.id, interest: lead.interest, budget: lead.budget });
  } catch {
    return json(res, 503, { ok: false, code: "PERSISTENCE_FAILURE", message: "Não foi possível confirmar o registro. Seus dados não foram salvos; tente novamente." }, { "retry-after": "30" });
  }
  const result = { ok: true, leadId: lead.id, status: lead.status, message: "Solicitação recebida. Nossa equipe responderá em até um dia útil." };
  idempotency.set(key, result);
  return json(res, 201, result);
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
  if (req.method === "GET" && url.pathname === "/api/health") return json(res, 200, { ok: true, service: "asteria-lead-intake", persistence: "filesystem" });
  if (req.method === "POST" && url.pathname === "/api/leads") return handleLead(req, res);
  if (req.method === "POST" && url.pathname === "/api/analytics") {
    let input; try { input = await bodyJson(req); } catch { return json(res, 400, { ok: false }); }
    const allowed = new Set(["page_view", "lead_form_start", "residence_view"]);
    if (!allowed.has(input.event)) return json(res, 422, { ok: false });
    await track(input.event, { path: String(input.path || "").slice(0, 160) });
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
