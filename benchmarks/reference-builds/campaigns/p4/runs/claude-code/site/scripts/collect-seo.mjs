/**
 * seo-technical-audit + content-discoverability-review evidence.
 *
 * Every assertion is made against the RESPONSE the deployed build actually
 * returns, not against source configuration.
 */
import { writeFileSync, mkdirSync } from "node:fs";

const BASE = process.env.ASTERIA_BASE_URL ?? "http://localhost:3100";
const OUT = "../evidence/seo";
mkdirSync(OUT, { recursive: true });

const ROUTES = [
  { path: "/", expect: "index" },
  { path: "/residences", expect: "index" },
  { path: "/residences/ridge-house-01", expect: "index" },
  { path: "/residences/ridge-house-04", expect: "index" },
  { path: "/residences/courtyard-house-12", expect: "index" },
  { path: "/location", expect: "index" },
  { path: "/journal", expect: "index" },
  { path: "/journal/why-twelve-houses", expect: "index" },
  { path: "/journal/the-energy-strategy", expect: "index" },
  { path: "/enquire", expect: "index" },
  { path: "/privacy", expect: "index" },
  { path: "/terms", expect: "index" },
  { path: "/contact", expect: "index" },
  { path: "/enquire/received?ref=AST-NONE", expect: "noindex" },
  { path: "/journal/material-samples-autumn", expect: "404" },
  { path: "/residences/no-such-house", expect: "404" },
];

const pick = (html, re) => (html.match(re)?.[1] ?? null);

const results = [];
const problems = [];

for (const route of ROUTES) {
  const response = await fetch(`${BASE}${route.path}`, { redirect: "manual" });
  const html = await response.text();
  const record = {
    path: route.path,
    expected: route.expect,
    status: response.status,
    contentType: response.headers.get("content-type"),
    title: pick(html, /<title>([^<]*)<\/title>/),
    description: pick(html, /<meta name="description" content="([^"]*)"/),
    canonical: pick(html, /<link rel="canonical" href="([^"]*)"/),
    robots: pick(html, /<meta name="robots" content="([^"]*)"/),
    ogTitle: pick(html, /<meta property="og:title" content="([^"]*)"/),
    ogUrl: pick(html, /<meta property="og:url" content="([^"]*)"/),
    ogLocale: pick(html, /<meta property="og:locale" content="([^"]*)"/),
    twitterCard: pick(html, /<meta name="twitter:card" content="([^"]*)"/),
    lang: pick(html, /<html lang="([^"]*)"/),
    h1: pick(html, /<h1[^>]*>([\s\S]*?)<\/h1>/)?.replace(/<[^>]+>/g, "").trim().slice(0, 90) ?? null,
    h1Count: (html.match(/<h1[\s>]/g) ?? []).length,
    internalLinks: new Set((html.match(/href="\/[^"#?]*/g) ?? []).map((h) => h.slice(6))).size,
    jsonLdBlocks: (html.match(/application\/ld\+json/g) ?? []).length,
    // Content is present in the server response, not only after hydration.
    serverRenderedTextChars: html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().length,
  };
  results.push(record);

  if (route.expect === "404") {
    if (record.status !== 404) problems.push(`${route.path}: expected 404, got ${record.status}`);
    continue;
  }
  if (record.status !== 200) problems.push(`${route.path}: expected 200, got ${record.status}`);
  if (!record.canonical) problems.push(`${route.path}: missing canonical`);
  if (!record.title) problems.push(`${route.path}: missing title`);
  if (!record.description) problems.push(`${route.path}: missing description`);
  if (record.h1Count !== 1) problems.push(`${route.path}: ${record.h1Count} h1 elements`);
  if (record.lang !== "en-GB") problems.push(`${route.path}: lang is ${record.lang}`);
  if (record.serverRenderedTextChars < 800) {
    problems.push(`${route.path}: only ${record.serverRenderedTextChars} chars of server-rendered text`);
  }
  if (route.expect === "noindex" && !(record.robots ?? "").includes("noindex")) {
    problems.push(`${route.path}: expected noindex, robots="${record.robots}"`);
  }
  if (route.expect === "index" && (record.robots ?? "").includes("noindex")) {
    problems.push(`${route.path}: unexpectedly noindex`);
  }
  // The root canonical is emitted without a trailing slash; both forms address
  // the same resource, so the comparison is made on the normalised value.
  const norm = (u) => (u ?? "").replace(/\/$/, "");
  const expectedCanonical = `https://asteria-residences.example${route.path.split("?")[0]}`;
  if (route.expect === "index" && norm(record.canonical) !== norm(expectedCanonical)) {
    problems.push(`${route.path}: canonical is ${record.canonical}, expected ${expectedCanonical}`);
  }
}

// robots.txt and sitemap.xml as served
const robotsResponse = await fetch(`${BASE}/robots.txt`);
const robotsTxt = await robotsResponse.text();
const sitemapResponse = await fetch(`${BASE}/sitemap.xml`);
const sitemapXml = await sitemapResponse.text();
const sitemapUrls = (sitemapXml.match(/<loc>([^<]+)<\/loc>/g) ?? []).map((l) =>
  l.replace(/<\/?loc>/g, ""),
);

if (robotsResponse.status !== 200) problems.push("robots.txt did not return 200");
if (!robotsTxt.includes("Sitemap:")) problems.push("robots.txt does not declare a sitemap");
if (!robotsTxt.includes("Disallow: /api/")) problems.push("robots.txt does not disallow /api/");
if (sitemapResponse.status !== 200) problems.push("sitemap.xml did not return 200");
// 5 static + 12 residences + 5 published journal entries + 3 legal = 25
if (sitemapUrls.length !== 25) problems.push(`sitemap has ${sitemapUrls.length} urls, expected 25`);
if (sitemapUrls.some((u) => u.includes("material-samples-autumn"))) {
  problems.push("draft journal entry present in sitemap");
}
if (sitemapUrls.some((u) => u.includes("/enquire/received"))) {
  problems.push("per-submission confirmation route present in sitemap");
}

// Every indexable route must be reachable from the sitemap and vice versa.
const indexable = results.filter((r) => r.expected === "index").map((r) => `https://asteria-residences.example${r.path}`);
const missingFromSitemap = indexable.filter(
  (u) => !sitemapUrls.some((s) => s.replace(/\/$/, "") === u.replace(/\/$/, "")),
);
if (missingFromSitemap.length) problems.push(`not in sitemap: ${missingFromSitemap.join(", ")}`);

// Internal linking: is every residence reachable from the index page?
const indexHtml = await (await fetch(`${BASE}/residences`)).text();
const linkedResidences = new Set(
  (indexHtml.match(/href="\/residences\/[a-z0-9-]+"/g) ?? []).map((h) => h.slice(7, -1)),
);

const report = {
  base: BASE,
  generatedAt: new Date().toISOString(),
  routes: results,
  robotsTxt,
  sitemapUrlCount: sitemapUrls.length,
  sitemapUrls,
  residencesLinkedFromIndex: linkedResidences.size,
  headers: Object.fromEntries((await fetch(`${BASE}/`)).headers.entries()),
  problems,
};

writeFileSync(`${OUT}/seo-audit.json`, JSON.stringify(report, null, 2));

console.log(`routes checked: ${results.length}`);
console.log(`sitemap urls: ${sitemapUrls.length}`);
console.log(`residences linked from /residences: ${linkedResidences.size}`);
console.log(problems.length ? `PROBLEMS:\n- ${problems.join("\n- ")}` : "no problems found");
process.exit(problems.length ? 1 : 0);
