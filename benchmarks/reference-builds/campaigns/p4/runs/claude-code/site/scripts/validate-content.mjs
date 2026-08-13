/**
 * Content integrity checks beyond the Zod schemas: uniqueness, arithmetic
 * consistency between the numbers and the drawings, and the fixture's explicit
 * prohibition on placeholder copy.
 */
import { writeFileSync, mkdirSync, readFileSync } from "node:fs";

const OUT = "../evidence/content";
mkdirSync(OUT, { recursive: true });

// The content modules are TypeScript; the checks below run against what the
// server actually renders, plus a direct read of the source files.
const BASE = process.env.ASTERIA_BASE_URL ?? "http://localhost:3100";
const problems = [];

/**
 * React splits interpolated values into separate text nodes and inserts HTML
 * comments between them, so assertions about rendered copy are made against the
 * flattened text rather than the raw markup.
 */
const flatten = (html) =>
  html
    .replace(/<script[\s\S]*?<\/script>/g, " ")
    .replace(/<style[\s\S]*?<\/style>/g, " ")
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&#x27;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/\s+/g, " ");

const sources = {
  residences: readFileSync("content/residences.ts", "utf8"),
  districts: readFileSync("content/districts.ts", "utf8"),
  journal: readFileSync("content/journal.ts", "utf8"),
  legal: readFileSync("content/legal.ts", "utf8"),
  settings: readFileSync("content/settings.ts", "utf8"),
};

// 1. No placeholder copy anywhere. The fixture prohibits it explicitly.
const PLACEHOLDERS = [
  /lorem ipsum/i,
  /dolor sit amet/i,
  /\bTODO\b/,
  /\bTBD\b/,
  /placeholder/i,
  /coming soon/i,
  /\bXXX\b/,
  /\bfoo\b|\bbar\b|\bbaz\b/i,
];
for (const [name, source] of Object.entries(sources)) {
  for (const pattern of PLACEHOLDERS) {
    if (pattern.test(source)) problems.push(`content/${name}.ts matches placeholder pattern ${pattern}`);
  }
}

// 2. Structural facts read back from the running site.
const residenceSlugs = [
  "ridge-house-01", "ridge-house-02", "ridge-house-03", "ridge-house-04",
  "terrace-house-05", "terrace-house-06", "terrace-house-07", "terrace-house-08",
  "terrace-house-09", "courtyard-house-10", "courtyard-house-11", "courtyard-house-12",
];

const seenIds = new Set();
const seenSlugs = new Set();
const facts = [];

for (const slug of residenceSlugs) {
  const response = await fetch(`${BASE}/residences/${slug}`);
  if (response.status !== 200) {
    problems.push(`/residences/${slug} returned ${response.status}`);
    continue;
  }
  const html = await response.text();
  const ld = [...html.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => JSON.parse(m[1]))
    .flatMap((g) => g["@graph"] ?? []);
  const node = ld.find((n) => n["@type"] === "SingleFamilyResidence");
  if (!node) {
    problems.push(`${slug}: no residence node`);
    continue;
  }
  if (seenSlugs.has(slug)) problems.push(`duplicate slug ${slug}`);
  seenSlugs.add(slug);
  if (seenIds.has(node.name)) problems.push(`duplicate residence name ${node.name}`);
  seenIds.add(node.name);

  // The schedule of areas must be arithmetically consistent with the stated
  // gross interior area (walls and structure account for the difference).
  const text = flatten(html);
  const scheduled = Number(
    text.match(/Scheduled total ([\d,]+) m² against/)?.[1]?.replace(/,/g, "") ?? 0,
  );
  const gross = node.floorSize.value;
  const ratio = scheduled / gross;
  if (ratio < 0.85 || ratio > 1.0) {
    problems.push(`${slug}: scheduled ${scheduled} m² vs gross ${gross} m² (ratio ${ratio.toFixed(3)})`);
  }

  // The drawing's own accessible description must state the same elevation the
  // specification states — the drawing is generated from the data, and this
  // check proves the two cannot drift.
  const elevationInText = text.match(/\+(\d+) m\b/)?.[1];
  const elevationInDrawing = text.match(/set at (\d+) metres above the valley datum/)?.[1];
  if (elevationInText && elevationInDrawing && elevationInText !== elevationInDrawing) {
    problems.push(`${slug}: elevation ${elevationInText} in text vs ${elevationInDrawing} in the drawing`);
  }

  facts.push({
    slug,
    name: node.name,
    grossInteriorSqm: gross,
    scheduledSqm: scheduled,
    scheduledRatio: Number(ratio.toFixed(3)),
    plotSqm: node.lotSize.value,
    bedrooms: node.numberOfBedrooms,
    hasOffer: Boolean(node.offers),
    elevationM: Number(elevationInDrawing ?? 0),
  });
}

if (facts.length !== 12) problems.push(`expected 12 residences, resolved ${facts.length}`);

// 3. The development-level figures on the home page must agree with the twelve.
const homeText = flatten(await (await fetch(`${BASE}/`)).text());
const availableCount = facts.filter((f) => f.hasOffer).length;
if (!homeText.includes(`12 · ${availableCount} available`)) {
  problems.push(`home page availability count disagrees with the residence records (${availableCount} available)`);
}
const minSqm = Math.min(...facts.map((f) => f.grossInteriorSqm));
const maxSqm = Math.max(...facts.map((f) => f.grossInteriorSqm));
if (!homeText.includes(`${minSqm}–${maxSqm} m²`)) {
  problems.push(`home page area range disagrees with the residence records (${minSqm}–${maxSqm})`);
}
const minElev = Math.min(...facts.map((f) => f.elevationM));
const maxElev = Math.max(...facts.map((f) => f.elevationM));
if (!homeText.includes(`${minElev}–${maxElev} m`)) {
  problems.push(`home page elevation range disagrees with the drawings (${minElev}–${maxElev})`);
}

// 4. Editorial state: the draft entry must be invisible everywhere.
const draft = await fetch(`${BASE}/journal/material-samples-autumn`);
if (draft.status !== 404) problems.push(`draft entry is reachable (status ${draft.status})`);
const journalHtml = flatten(await (await fetch(`${BASE}/journal`)).text());
if (journalHtml.includes("Autumn material samples")) problems.push("draft entry listed in the journal index");

// 5. Every district and legal document renders.
for (const path of ["/location", "/privacy", "/terms", "/contact"]) {
  const response = await fetch(`${BASE}${path}`);
  if (response.status !== 200) problems.push(`${path} returned ${response.status}`);
}

const report = { generatedAt: new Date().toISOString(), residences: facts, availableCount, problems };
writeFileSync(`${OUT}/content-integrity.json`, JSON.stringify(report, null, 2));

console.log(`residences validated: ${facts.length}`);
console.log(`available (with a published Offer): ${availableCount}`);
console.log(problems.length ? `PROBLEMS:\n- ${problems.join("\n- ")}` : "no problems found");
process.exit(problems.length ? 1 : 0);
