#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function arg(name, fallback = null) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : fallback;
}
function safeName(value) { return value.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') || 'home'; }

(async () => {
  const baseUrl = arg('--base-url');
  const outputDir = arg('--output-dir');
  const routes = (arg('--routes', '/') || '/').split(',').map(v => v.trim()).filter(Boolean);
  const notFoundRoute = arg('--not-found-route', '/__atlas_reference_build_missing__');
  if (!baseUrl || !outputDir) throw new Error('--base-url and --output-dir are required');
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(outputDir, 'screenshots'), { recursive: true });

  const viewports = [
    { name: 'phone-360', width: 360, height: 800 },
    { name: 'tablet-768', width: 768, height: 1024 },
    { name: 'laptop-1280', width: 1280, height: 800 },
    { name: 'wide-1920', width: 1920, height: 1080 },
  ];
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, reducedMotion: 'reduce' });
    for (const route of routes) {
      const page = await context.newPage();
      const consoleErrors = [];
      const pageErrors = [];
      const failedRequests = [];
      page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
      page.on('pageerror', e => pageErrors.push(String(e)));
      page.on('requestfailed', r => failedRequests.push({ url: r.url(), error: r.failure()?.errorText || 'unknown' }));
      const response = await page.goto(new URL(route, baseUrl).toString(), { waitUntil: 'networkidle' });
      const metrics = await page.evaluate(() => ({
        title: document.title,
        h1: document.querySelector('h1')?.textContent?.trim() || null,
        horizontalOverflow: Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth),
        canonical: document.querySelector('link[rel="canonical"]')?.href || null,
        robots: [...document.querySelectorAll('meta[name="robots"]')].map(n => n.content),
        lang: document.documentElement.lang || null,
        formControls: [...document.querySelectorAll('input:not([type="hidden"]),select,textarea,button')].map(el => ({
          tag: el.tagName.toLowerCase(),
          id: el.id || null,
          ariaLabel: el.getAttribute('aria-label'),
          label: el.id ? document.querySelector(`label[for="${CSS.escape(el.id)}"]`)?.textContent?.trim() || null : null,
          rect: { width: Math.round(el.getBoundingClientRect().width), height: Math.round(el.getBoundingClientRect().height) },
          borderColor: getComputedStyle(el).borderTopColor,
          backgroundColor: getComputedStyle(el).backgroundColor,
        }))
      }));
      const screenshot = path.join(outputDir, 'screenshots', `${safeName(route)}--${viewport.name}.png`);
      await page.screenshot({ path: screenshot, fullPage: true, animations: 'disabled' });
      results.push({ route, viewport, status: response?.status() || null, ...metrics, consoleErrors, pageErrors, failedRequests, screenshot: path.relative(outputDir, screenshot) });
      await page.close();
    }
    await context.close();
  }

  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();
  const missingResponse = await page.goto(new URL(notFoundRoute, baseUrl).toString(), { waitUntil: 'networkidle' });
  const notFound = await page.evaluate(() => ({
    robots: [...document.querySelectorAll('meta[name="robots"]')].map(n => n.content),
    canonical: document.querySelector('link[rel="canonical"]')?.href || null,
    title: document.title,
  }));
  notFound.route = notFoundRoute;
  notFound.status = missingResponse?.status() || null;
  await context.close();
  await browser.close();

  const summary = {
    version: 1,
    evidence_source: 'campaign-portable',
    generated_at: new Date().toISOString(),
    base_url: baseUrl,
    results,
    seo_not_found: notFound,
  };
  fs.writeFileSync(path.join(outputDir, 'browser-summary.json'), JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify({ outputDir, routes: routes.length, viewports: viewports.length, notFound }, null, 2));
})().catch(error => { console.error(error); process.exit(1); });
