import test from "node:test";
import assert from "node:assert/strict";
import { validateLead } from "../server.js";
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
});

test("returns a real 404 document", () => {
  const page = renderPage(new URL("http://localhost:4173/nao-existe"));
  assert.equal(page.status, 404);
  assert.match(page.html, /Página não encontrada/);
});
