/**
 * web-performance-field-readiness evidence.
 *
 * Measures the production build on an emulated mid-range mobile device with
 * throttled CPU and network, and measures the transfer budget of every
 * critical route from the bytes actually sent over the wire.
 */
import { chromium } from "@playwright/test";
import { writeFileSync, mkdirSync } from "node:fs";

const BASE = process.env.ASTERIA_BASE_URL ?? "http://localhost:3100";
const OUT = "../evidence/performance";
mkdirSync(OUT, { recursive: true });

// Budgets, declared before measurement.
const BUDGET = {
  totalTransferKb: 320,
  scriptTransferKb: 190,
  fontTransferKb: 130,
  imageTransferKb: 40,
  requests: 40,
  lcpMs: 2500,
  clsScore: 0.1,
  domContentLoadedMs: 3000,
};

const ROUTES = ["/", "/residences", "/residences/ridge-house-04", "/location", "/journal", "/enquire"];

const browser = await chromium.launch({
  executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
});

const results = [];
const problems = [];

for (const route of ROUTES) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent:
      "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36",
  });
  const page = await context.newPage();
  const client = await context.newCDPSession(page);

  // Mid-range mobile profile: 4x CPU slowdown, "Slow 4G"-class network.
  await client.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await client.send("Network.enable");
  await client.send("Network.emulateNetworkConditions", {
    offline: false,
    latency: 150,
    downloadThroughput: (1.6 * 1024 * 1024) / 8,
    uploadThroughput: (750 * 1024) / 8,
  });

  /*
   * Transfer sizes are taken from CDP `encodedDataLength`, i.e. the bytes that
   * actually crossed the wire after compression — not the decompressed body.
   */
  const transfers = [];
  const meta = new Map();
  client.on("Network.responseReceived", (event) => {
    meta.set(event.requestId, {
      url: event.response.url.replace(BASE, ""),
      status: event.response.status,
      type: (event.response.headers["content-type"] ?? event.response.mimeType ?? "").split(";")[0],
    });
  });
  client.on("Network.loadingFinished", (event) => {
    const info = meta.get(event.requestId);
    if (!info) return;
    transfers.push({ ...info, bytes: event.encodedDataLength });
  });

  const started = Date.now();
  await page.goto(`${BASE}${route}`, { waitUntil: "load" });
  await page.waitForTimeout(2500);

  const vitals = await page.evaluate(
    () =>
      new Promise((resolve) => {
        const out = { lcp: 0, cls: 0, fcp: 0, dcl: 0, load: 0, longTasks: 0 };
        const nav = performance.getEntriesByType("navigation")[0];
        if (nav) {
          out.dcl = Math.round(nav.domContentLoadedEventEnd);
          out.load = Math.round(nav.loadEventEnd);
        }
        const fcp = performance.getEntriesByName("first-contentful-paint")[0];
        if (fcp) out.fcp = Math.round(fcp.startTime);
        try {
          new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) out.lcp = Math.round(entry.startTime);
          }).observe({ type: "largest-contentful-paint", buffered: true });
          new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
              if (!entry.hadRecentInput) out.cls += entry.value;
            }
          }).observe({ type: "layout-shift", buffered: true });
          new PerformanceObserver((list) => {
            out.longTasks += list.getEntries().length;
          }).observe({ type: "longtask", buffered: true });
        } catch {
          /* observer unsupported */
        }
        setTimeout(() => resolve({ ...out, cls: Number(out.cls.toFixed(4)) }), 900);
      }),
  );

  const byType = (predicate) =>
    Math.round(transfers.filter(predicate).reduce((sum, t) => sum + t.bytes, 0) / 1024);

  const measurement = {
    route,
    wallClockMs: Date.now() - started,
    requests: transfers.length,
    totalTransferKb: byType(() => true),
    documentKb: byType((t) => t.type.includes("html")),
    scriptTransferKb: byType((t) => t.type.includes("javascript")),
    styleTransferKb: byType((t) => t.type.includes("css")),
    fontTransferKb: byType((t) => t.type.includes("font")),
    imageTransferKb: byType((t) => t.type.startsWith("image")),
    vitals,
    largest: [...transfers].sort((a, b) => b.bytes - a.bytes).slice(0, 6),
  };
  results.push(measurement);

  if (measurement.totalTransferKb > BUDGET.totalTransferKb) {
    problems.push(`${route}: ${measurement.totalTransferKb} KB total > ${BUDGET.totalTransferKb} KB budget`);
  }
  if (measurement.scriptTransferKb > BUDGET.scriptTransferKb) {
    problems.push(`${route}: ${measurement.scriptTransferKb} KB script > ${BUDGET.scriptTransferKb} KB budget`);
  }
  if (measurement.fontTransferKb > BUDGET.fontTransferKb) {
    problems.push(`${route}: ${measurement.fontTransferKb} KB fonts > ${BUDGET.fontTransferKb} KB budget`);
  }
  if (measurement.imageTransferKb > BUDGET.imageTransferKb) {
    problems.push(`${route}: ${measurement.imageTransferKb} KB images > ${BUDGET.imageTransferKb} KB budget`);
  }
  if (measurement.requests > BUDGET.requests) {
    problems.push(`${route}: ${measurement.requests} requests > ${BUDGET.requests} budget`);
  }
  if (vitals.lcp > BUDGET.lcpMs) problems.push(`${route}: LCP ${vitals.lcp}ms > ${BUDGET.lcpMs}ms`);
  if (vitals.cls > BUDGET.clsScore) problems.push(`${route}: CLS ${vitals.cls} > ${BUDGET.clsScore}`);
  if (vitals.dcl > BUDGET.domContentLoadedMs) {
    problems.push(`${route}: DCL ${vitals.dcl}ms > ${BUDGET.domContentLoadedMs}ms`);
  }

  console.log(
    `${route.padEnd(30)} ${String(measurement.totalTransferKb).padStart(4)} KB  ` +
      `js ${String(measurement.scriptTransferKb).padStart(3)} KB  ` +
      `req ${String(measurement.requests).padStart(2)}  ` +
      `LCP ${String(vitals.lcp).padStart(4)}ms  CLS ${vitals.cls}`,
  );

  await context.close();
}

await browser.close();

writeFileSync(
  `${OUT}/performance.json`,
  JSON.stringify(
    {
      base: BASE,
      generatedAt: new Date().toISOString(),
      deviceProfile: {
        viewport: "390x844 @3x",
        cpuThrottling: "4x",
        network: "1.6 Mbps down / 750 Kbps up / 150 ms RTT",
        note: "Emulated mid-range mobile; measured on the production build over HTTP on the loopback interface, so network latency is emulated rather than real.",
      },
      budget: BUDGET,
      results,
      problems,
    },
    null,
    2,
  ),
);

console.log(problems.length ? `\nPROBLEMS:\n- ${problems.join("\n- ")}` : "\nall routes inside budget");
process.exit(problems.length ? 1 : 0);
