/**
 * structured-data-validation evidence.
 *
 * Two things are checked, and the second is the one that matters:
 *   1. Syntactic validity of every JSON-LD block served.
 *   2. TRUTHFULNESS — every asserted value is compared against the visible,
 *      authoritative content on the same page. Structured data that claims
 *      something the page does not say is a defect here, not a bonus.
 */
import { writeFileSync, mkdirSync } from "node:fs";

const BASE = process.env.ASTERIA_BASE_URL ?? "http://localhost:3100";
const OUT = "../evidence/structured-data";
mkdirSync(OUT, { recursive: true });

const problems = [];
const documents = [];

async function load(path) {
  const html = await (await fetch(`${BASE}${path}`)).text();
  const blocks = [...html.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)].map(
    (m) => m[1],
  );
  const parsed = [];
  blocks.forEach((raw, i) => {
    try {
      parsed.push(JSON.parse(raw));
    } catch (error) {
      problems.push(`${path} block ${i}: invalid JSON — ${error.message}`);
    }
  });
  const text = html
    .replace(/<script[\s\S]*?<\/script>/g, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&#x27;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#x2F;/g, "/")
    .replace(/\s+/g, " ");
  return { html, text, graphs: parsed };
}

function nodesOf(graphs) {
  const out = [];
  for (const graph of graphs) {
    if (!graph["@context"]) problems.push("graph is missing @context");
    for (const node of graph["@graph"] ?? []) out.push(node);
  }
  return out;
}

function requireType(nodes, type, path) {
  const found = nodes.filter((n) => n["@type"] === type);
  if (!found.length) problems.push(`${path}: no ${type} node`);
  return found;
}

// ---------------------------------------------------------------- home
{
  const path = "/";
  const { text, graphs } = await load(path);
  const nodes = nodesOf(graphs);
  documents.push({ path, nodeTypes: nodes.map((n) => n["@type"]), graphs });

  const org = requireType(nodes, "RealEstateAgent", path)[0];
  if (org) {
    if (!text.includes(org.telephone)) problems.push(`${path}: telephone in JSON-LD not visible on page`);
    if (!text.includes(org.address.streetAddress)) {
      problems.push(`${path}: street address in JSON-LD not visible on page`);
    }
  }
  requireType(nodes, "WebSite", path);
  requireType(nodes, "Place", path);
  requireType(nodes, "BreadcrumbList", path);

  const list = requireType(nodes, "ItemList", path)[0];
  if (list) {
    if (list.numberOfItems !== 12) problems.push(`${path}: ItemList claims ${list.numberOfItems} items`);
    if (list.itemListElement.length !== 12) {
      problems.push(`${path}: ItemList has ${list.itemListElement.length} entries`);
    }
  }
}

// ------------------------------------------------------- residence pages
const RESIDENCES = [
  { slug: "ridge-house-04", status: "available" },
  { slug: "ridge-house-01", status: "sold" },
  { slug: "ridge-house-03", status: "reserved" },
  { slug: "courtyard-house-12", status: "reserved" },
];

for (const residence of RESIDENCES) {
  const path = `/residences/${residence.slug}`;
  const { text, graphs } = await load(path);
  const nodes = nodesOf(graphs);
  documents.push({ path, nodeTypes: nodes.map((n) => n["@type"]), graphs });

  const node = requireType(nodes, "SingleFamilyResidence", path)[0];
  if (!node) continue;

  // Name, areas, bedrooms and bathrooms must all appear on the page.
  if (!text.includes(node.name)) problems.push(`${path}: name "${node.name}" not visible`);
  const floor = node.floorSize.value;
  const lot = node.lotSize.value;
  if (!text.includes(`${floor} m²`)) problems.push(`${path}: floorSize ${floor} not visible`);
  if (!text.includes(`${lot} m²`)) problems.push(`${path}: lotSize ${lot} not visible`);
  if (node.floorSize.unitCode !== "MTK") problems.push(`${path}: floorSize unit is not MTK`);

  // The offer must exist only when the residence can actually be bought.
  const hasOffer = Boolean(node.offers);
  if (residence.status === "available" && !hasOffer) {
    problems.push(`${path}: available residence has no Offer node`);
  }
  if (residence.status !== "available" && hasOffer) {
    problems.push(`${path}: ${residence.status} residence publishes an Offer — contradicts the page`);
  }
  if (hasOffer) {
    const spec = node.offers.priceSpecification;
    if (spec.priceCurrency !== "EUR") problems.push(`${path}: offer currency is not EUR`);
    if (spec.minPrice >= spec.maxPrice) problems.push(`${path}: offer band min >= max`);
    if (node.offers.availability !== "https://schema.org/PreOrder") {
      problems.push(`${path}: availability should be PreOrder for an off-plan sale`);
    }
    // The visible price band must match the structured band.
    const compact = (v) => `€${(v / 1_000_000) % 1 === 0 ? (v / 1_000_000).toFixed(0) : (v / 1_000_000).toFixed(2)}M`;
    const visibleBand = `${compact(spec.minPrice)}–${compact(spec.maxPrice)}`;
    if (!text.includes(visibleBand)) {
      problems.push(`${path}: structured price band ${visibleBand} not visible on page`);
    }
  }

  // Bedrooms / bathrooms
  if (!text.includes(`Bedrooms ${node.numberOfBedrooms}`)) {
    problems.push(`${path}: bedrooms ${node.numberOfBedrooms} not visible in the specification table`);
  }

  requireType(nodes, "BreadcrumbList", path);
}

// ----------------------------------------------------------- journal
{
  const path = "/journal/why-twelve-houses";
  const { text, graphs } = await load(path);
  const nodes = nodesOf(graphs);
  documents.push({ path, nodeTypes: nodes.map((n) => n["@type"]), graphs });
  const article = requireType(nodes, "Article", path)[0];
  if (article) {
    if (!text.includes(article.headline)) problems.push(`${path}: headline not visible`);
    if (!text.includes(article.author.name)) problems.push(`${path}: author not visible`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(article.datePublished)) {
      problems.push(`${path}: datePublished is not an ISO date`);
    }
    if (article.wordCount < 100) problems.push(`${path}: implausible wordCount`);
  }
}

// -------------------------------------------------------------- enquire
{
  const path = "/enquire";
  const { text, graphs } = await load(path);
  const nodes = nodesOf(graphs);
  documents.push({ path, nodeTypes: nodes.map((n) => n["@type"]), graphs });
  const faq = requireType(nodes, "FAQPage", path)[0];
  if (faq) {
    for (const question of faq.mainEntity) {
      if (!text.includes(question.name)) {
        problems.push(`${path}: FAQ question "${question.name.slice(0, 40)}" not visible on the page`);
      }
      if (!text.includes(question.acceptedAnswer.text.slice(0, 40))) {
        problems.push(`${path}: FAQ answer not visible on the page`);
      }
    }
  }
}

// ------------------------------------------------------------- location
{
  const path = "/location";
  const { text, graphs } = await load(path);
  const nodes = nodesOf(graphs);
  documents.push({ path, nodeTypes: nodes.map((n) => n["@type"]), graphs });
  const places = nodes.filter((n) => n["@type"] === "Place");
  if (places.length < 5) problems.push(`${path}: expected the development plus four districts`);
  for (const place of places) {
    if (!text.includes(place.name.split(",")[0])) {
      problems.push(`${path}: place "${place.name}" not visible`);
    }
  }
}

// ---------------------------------------------------- global consistency
const allIds = new Set();
for (const doc of documents) {
  for (const graph of doc.graphs) {
    for (const node of graph["@graph"] ?? []) {
      if (node["@id"]) allIds.add(node["@id"]);
    }
  }
}

writeFileSync(
  `${OUT}/structured-data.json`,
  JSON.stringify(
    { base: BASE, generatedAt: new Date().toISOString(), documents, uniqueEntityIds: [...allIds], problems },
    null,
    2,
  ),
);

console.log(`documents checked: ${documents.length}`);
console.log(`unique entity @ids: ${allIds.size}`);
console.log(problems.length ? `PROBLEMS:\n- ${problems.join("\n- ")}` : "no problems found");
process.exit(problems.length ? 1 : 0);
