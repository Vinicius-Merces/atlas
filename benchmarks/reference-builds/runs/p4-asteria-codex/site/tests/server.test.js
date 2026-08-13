import test from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { AsteriaStore, validateLead } from "../server.js";
import { renderPage } from "../src/render.js";

test("validates a complete lead", () => {
  const result = validateLead({ name:"Marina Duarte", email:"marina@example.com", phone:"(11) 99999-0000", interest:"casa-patio", budget:"5m-7m", visitDate:"2026-09-01", consent:true }, new Date("2026-08-13T12:00:00Z"));
  assert.equal(result.valid, true);
  assert.equal(result.data.phone, "11999990000");
});

test("rejects invalid and bot-shaped lead", () => {
  const result = validateLead({ name:"A", email:"nope", phone:"1", interest:"unknown", budget:"", consent:false, company:"spam" });
  assert.equal(result.valid, false);
  assert.deepEqual(Object.keys(result.errors).sort(), ["budget", "consent", "email", "form", "interest", "name", "phone"]);
});

test("renders canonical public pages and truthful schema", () => {
  const page = renderPage(new URL("http://localhost:4173/residencias/casa-patio"));
  assert.equal(page.status, 200);
  assert.match(page.html, /rel="canonical"/);
  assert.match(page.html, /SingleFamilyResidence/);
  assert.match(page.html, /384 m²/);
  assert.match(page.html, /numberOfBedrooms/);
  assert.doesNotMatch(page.html, /numberOfRooms/);
});

test("returns a real 404 document", () => {
  const page = renderPage(new URL("http://localhost:4173/nao-existe"));
  assert.equal(page.status, 404);
  assert.match(page.html, /Página não encontrada/);
  assert.match(page.html, /noindex,nofollow/);
  assert.doesNotMatch(page.html, /rel="canonical"/);
});

test("models all twelve residences and distinct editorial bodies", () => {
  const index = renderPage(new URL("http://localhost:4173/residencias"));
  assert.equal((index.html.match(/class="catalog-entry"/g) || []).length, 12);
  assert.match(index.html, /três famílias arquitetônicas/);
  const article = renderPage(new URL("http://localhost:4173/caderno/doze-casas-uma-paisagem"));
  assert.match(article.html, /Vizinhança sem exposição/);
  assert.doesNotMatch(article.html, /Materiais residenciais precisam/);
});

test("persists idempotency and analytics outbox across store restart", () => {
  const testDataRoot = fileURLToPath(new URL("../data/", import.meta.url));
  mkdirSync(testDataRoot, { recursive: true });
  const directory = mkdtempSync(join(testDataRoot, "test-store-"));
  const path = join(directory, "asteria.sqlite");
  const lead = { name:"Rafael Nogueira", email:"rafael@example.test", phone:"11988887777", interest:"casa-horizonte", budget:"acima-7m", visitDate:"2026-09-10", consent:true };
  try {
    const firstStore = new AsteriaStore(path);
    const first = firstStore.acceptLead("persistent_key_0001", lead);
    assert.equal(first.created, true);
    const outbox = firstStore.db.prepare("SELECT COUNT(*) AS count FROM analytics_outbox WHERE event = 'lead_authoritative_success'").get();
    assert.equal(Number(outbox.count), 1);
    firstStore.close();
    const restartedStore = new AsteriaStore(path);
    const retry = restartedStore.acceptLead("persistent_key_0001", lead);
    assert.equal(retry.created, false);
    assert.equal(retry.result.duplicate, true);
    assert.equal(retry.result.leadId, first.result.leadId);
    const secondKey = restartedStore.acceptLead("persistent_key_0002", lead);
    assert.equal(secondKey.result.leadId, first.result.leadId);
    assert.equal(secondKey.result.duplicate, true);
    restartedStore.close();
  } finally {
    rmSync(directory, { recursive:true, force:true });
  }
});
