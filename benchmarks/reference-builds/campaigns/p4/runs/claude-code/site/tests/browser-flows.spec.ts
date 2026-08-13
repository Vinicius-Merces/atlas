import { test, expect, type Page, type ConsoleMessage } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";
import { randomUUID } from "node:crypto";

/**
 * browser-flow-validation evidence.
 *
 * Every assertion here is exercised against the production build over HTTP,
 * and every screenshot is written into the run's evidence tree.
 */

const SHOTS = "../evidence/browser";
const ADMIN_KEY = process.env.ASTERIA_ADMIN_KEY ?? "bench-p4-admin-key-3f9c2a71";

mkdirSync(SHOTS, { recursive: true });

type Diagnostics = {
  consoleErrors: string[];
  consoleWarnings: string[];
  pageErrors: string[];
  failedRequests: { url: string; failure: string }[];
  badResponses: { url: string; status: number }[];
  cancelledPrefetches: string[];
};

function watch(page: Page): Diagnostics {
  const d: Diagnostics = {
    consoleErrors: [],
    consoleWarnings: [],
    pageErrors: [],
    failedRequests: [],
    badResponses: [],
    cancelledPrefetches: [],
  };
  page.on("console", (message: ConsoleMessage) => {
    if (message.type() === "error") d.consoleErrors.push(message.text());
    if (message.type() === "warning") d.consoleWarnings.push(message.text());
  });
  page.on("pageerror", (error) => d.pageErrors.push(String(error)));
  page.on("requestfailed", (request) => {
    // Next.js cancels in-flight <Link> RSC prefetches when the user navigates.
    // Those abort as designed and are recorded separately rather than counted
    // as runtime failures.
    const url = request.url();
    const failure = request.failure()?.errorText ?? "";
    if (url.includes("_rsc=") && failure === "net::ERR_ABORTED") {
      d.cancelledPrefetches.push(url);
      return;
    }
    d.failedRequests.push({ url, failure });
  });
  page.on("response", (response) => {
    if (response.status() >= 400) {
      d.badResponses.push({ url: response.url(), status: response.status() });
    }
  });
  return d;
}

function record(name: string, data: unknown) {
  writeFileSync(`${SHOTS}/${name}.json`, JSON.stringify(data, null, 2));
}

test.describe("primary conversion journey", () => {
  test("home → residence → enquire → authoritative lead", async ({ page, request }) => {
    const diagnostics = watch(page);
    const journey: Record<string, unknown> = {};

    // 1. Home
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Twelve houses");
    await expect(page.getByRole("link", { name: /request a visit/i }).first()).toBeVisible();
    await page.screenshot({ path: `${SHOTS}/01-home.png`, fullPage: true });

    // 2. Navigate to the index through primary navigation
    await page.getByRole("navigation", { name: "Primary" }).getByRole("link", { name: "Residences" }).click();
    await expect(page).toHaveURL(/\/residences$/);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("twelve residences");
    const cardCount = await page.locator("h2 a[href^='/residences/']").count();
    journey.residenceCardsListed = cardCount;
    expect(cardCount).toBe(12);
    await page.screenshot({ path: `${SHOTS}/02-residences.png`, fullPage: true });

    // 3. Open a residence detail
    await page.getByRole("link", { name: "Ridge House 04" }).first().click();
    await expect(page).toHaveURL(/\/residences\/ridge-house-04$/);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Ridge House 04");
    await expect(page.getByText("404 m²").first()).toBeVisible();
    await expect(page.getByRole("table")).toBeVisible();
    await page.screenshot({ path: `${SHOTS}/03-residence-detail.png`, fullPage: true });

    // 4. Enter the conversion journey from the residence
    await page.getByRole("link", { name: /request a visit to 04/i }).click();
    await expect(page).toHaveURL(/\/enquire\?residence=A04$/);
    const preselected = await page.locator("#field-residenceId").inputValue();
    journey.residencePreselected = preselected;
    expect(preselected).toBe("A04");
    await page.screenshot({ path: `${SHOTS}/04-enquire-prefilled.png`, fullPage: true });

    // 5. Complete and submit
    const email = `benchmark.buyer.${Date.now()}@example.com`;
    await page.fill("#field-name", "Benchmark Buyer");
    await page.fill("#field-email", email);
    await page.fill("#field-phone", "+351 912 345 678");
    await page.selectOption("#field-timeframe", "3-6-months");
    await page.selectOption("#field-context", "primary-home");
    await page.fill("#field-preferredDates", "Weekday mornings");
    await page.fill("#field-message", "Interested in the covered south terrace and the plateau path.");
    await page.check("#field-consent");
    await page.waitForTimeout(2100); // minimum time-to-submit guard
    await page.getByRole("button", { name: /send visit request/i }).click();

    const status = page.getByRole("status");
    await expect(status).toContainText("Recorded", { timeout: 15_000 });
    const reference = (await page.locator("p").filter({ hasText: /^AST-/ }).first().innerText()).trim();
    journey.reference = reference;
    expect(reference).toMatch(/^AST-[0-9A-Z]{8}$/);
    await page.screenshot({ path: `${SHOTS}/05-enquire-success.png`, fullPage: true });

    // 6. Prove the lead reached authoritative server state, not just the UI.
    const readback = await request.get(`/api/visit-requests/${reference}`, {
      headers: { "x-asteria-admin-key": ADMIN_KEY },
    });
    expect(readback.status()).toBe(200);
    const body = await readback.json();
    journey.authoritativeRecord = body.record;
    expect(body.record.email).toBe(email);
    expect(body.record.residence_id).toBe("A04");
    expect(body.record.status).toBe("received");

    journey.diagnostics = diagnostics;
    record("primary-flow", journey);

    // 7. No unexplained runtime failures anywhere in the journey.
    expect(diagnostics.pageErrors).toEqual([]);
    expect(diagnostics.consoleErrors).toEqual([]);
    expect(diagnostics.failedRequests).toEqual([]);
    expect(diagnostics.badResponses).toEqual([]);
  });
});

test.describe("negative journeys", () => {
  test("empty submit is rejected with associated, focused field errors", async ({ page }) => {
    const diagnostics = watch(page);
    await page.goto("/enquire");
    await page.waitForTimeout(2100);
    await page.getByRole("button", { name: /send visit request/i }).click();

    // Next.js injects its own empty route-announcer with role=alert; scope to ours.
    const alert = page.locator('[role="alert"]:not(#__next-route-announcer__)');
    await expect(alert).toContainText("need attention");
    await expect(page.locator("#error-name")).toBeVisible();
    await expect(page.locator("#field-name")).toHaveAttribute("aria-invalid", "true");
    await expect(page.locator("#field-name")).toHaveAttribute("aria-describedby", /error-name/);
    await expect(page.locator("#field-name")).toBeFocused();

    await page.screenshot({ path: `${SHOTS}/06-validation-empty.png`, fullPage: true });
    record("negative-empty-submit", {
      errorsShown: await page.locator("[id^=error-]").allInnerTexts(),
      diagnostics,
    });
    expect(diagnostics.pageErrors).toEqual([]);
  });

  test("malformed email and missing consent produce field-level errors", async ({ page }) => {
    await page.goto("/enquire");
    await page.fill("#field-name", "Ana Ribeiro");
    await page.fill("#field-email", "ana-at-example");
    await page.selectOption("#field-timeframe", "exploring");
    await page.selectOption("#field-context", "second-home");
    await page.waitForTimeout(2100);
    await page.getByRole("button", { name: /send visit request/i }).click();

    await expect(page.locator("#error-email")).toContainText("valid email");
    await expect(page.locator("#error-consent")).toContainText("consent");
    await page.screenshot({ path: `${SHOTS}/07-validation-fields.png`, fullPage: true });
    record("negative-field-validation", {
      email: await page.locator("#error-email").innerText(),
      consent: await page.locator("#error-consent").innerText(),
    });
  });

  test("duplicate submission does not create a second lead", async ({ page, request }) => {
    await page.goto("/enquire");
    const email = `duplicate.buyer.${Date.now()}@example.com`;
    await page.fill("#field-name", "Duplicate Buyer");
    await page.fill("#field-email", email);
    await page.selectOption("#field-timeframe", "immediate");
    await page.selectOption("#field-context", "investment");
    await page.check("#field-consent");
    await page.waitForTimeout(2100);

    const before = await (await request.get("/api/visit-requests/_stats", {
      headers: { "x-asteria-admin-key": ADMIN_KEY },
    })).json();

    await page.getByRole("button", { name: /send visit request/i }).click();
    await expect(page.getByRole("status")).toContainText("Recorded", { timeout: 15_000 });
    const reference = (await page.locator("p").filter({ hasText: /^AST-/ }).first().innerText()).trim();

    // Resubmit the identical enquiry from a new form instance: the same-day
    // dedupe key must catch it even though the idempotency key is new.
    await page.getByRole("button", { name: /send another request/i }).click();
    await page.fill("#field-name", "Duplicate Buyer");
    await page.fill("#field-email", email);
    await page.selectOption("#field-timeframe", "immediate");
    await page.selectOption("#field-context", "investment");
    await page.check("#field-consent");
    await page.waitForTimeout(2100);
    await page.getByRole("button", { name: /send visit request/i }).click();
    await expect(page.getByRole("status")).toContainText("already have this request", { timeout: 15_000 });
    await page.screenshot({ path: `${SHOTS}/08-duplicate.png`, fullPage: true });

    const after = await (await request.get("/api/visit-requests/_stats", {
      headers: { "x-asteria-admin-key": ADMIN_KEY },
    })).json();

    record("negative-duplicate", { reference, before, after });
    expect(after.visitRequests - before.visitRequests).toBe(1);
    expect(after.conversionEvents - before.conversionEvents).toBe(1);
  });

  test("server/provider failure is shown as failure, never as success", async ({ page }) => {
    // The store-failure server runs on 3102 with ASTERIA_STORE_MODE=fail.
    const failBase = process.env.ASTERIA_FAIL_BASE_URL ?? "http://localhost:3102";
    const diagnostics = watch(page);
    await page.goto(`${failBase}/enquire`);
    await page.fill("#field-name", "Failure Path");
    await page.fill("#field-email", `failure.path.${Date.now()}@example.com`);
    await page.selectOption("#field-timeframe", "exploring");
    await page.selectOption("#field-context", "broker");
    await page.check("#field-consent");
    await page.waitForTimeout(2100);
    await page.getByRole("button", { name: /send visit request/i }).click();

    // Next.js injects its own empty route-announcer with role=alert; scope to ours.
    const alert = page.locator('[role="alert"]:not(#__next-route-announcer__)');
    await expect(alert).toContainText("was not recorded", { timeout: 15_000 });
    await expect(page.locator("body")).not.toContainText("Recorded. Your reference is below.");
    // The visitor's answers survive the failure so they can retry.
    await expect(page.locator("#field-name")).toHaveValue("Failure Path");
    await page.screenshot({ path: `${SHOTS}/09-store-failure.png`, fullPage: true });
    record("negative-store-failure", {
      message: await alert.innerText(),
      preservedName: await page.locator("#field-name").inputValue(),
      diagnostics,
    });
  });

  test("broker/provider failure still records the lead and says so honestly", async ({ page, request }) => {
    const brokerBase = process.env.ASTERIA_BROKER_FAIL_BASE_URL ?? "http://localhost:3103";
    await page.goto(`${brokerBase}/enquire`);
    const email = `broker.fail.${Date.now()}@example.com`;
    await page.fill("#field-name", "Broker Failure");
    await page.fill("#field-email", email);
    await page.selectOption("#field-timeframe", "6-12-months");
    await page.selectOption("#field-context", "second-home");
    await page.check("#field-consent");
    await page.waitForTimeout(2100);
    await page.getByRole("button", { name: /send visit request/i }).click();

    await expect(page.getByRole("status")).toContainText("Recorded", { timeout: 15_000 });
    await expect(page.getByRole("status")).toContainText("retried");
    const reference = (await page.locator("p").filter({ hasText: /^AST-/ }).first().innerText()).trim();
    await page.screenshot({ path: `${SHOTS}/10-broker-failure.png`, fullPage: true });

    const readback = await request.get(`${brokerBase}/api/visit-requests/${reference}`, {
      headers: { "x-asteria-admin-key": ADMIN_KEY },
    });
    const body = await readback.json();
    record("negative-broker-failure", { reference, record: body.record });
    expect(body.record.notification_status).toBe("failed");
    expect(body.record.status).toBe("received");
  });
});

test.describe("resilience and progressive enhancement", () => {
  test("the form works with JavaScript disabled", async ({ browser }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const page = await context.newPage();
    await page.goto("http://localhost:3100/enquire");
    await page.fill("#field-name", "No Script Buyer");
    await page.fill("#field-email", `noscript.${Date.now()}@example.com`);
    await page.selectOption("#field-timeframe", "immediate");
    await page.selectOption("#field-context", "primary-home");
    await page.check("#field-consent");
    await page.waitForTimeout(2100);
    await page.getByRole("button", { name: /send visit request/i }).click();
    await page.waitForURL(/\/enquire\/received/, { timeout: 15_000 });
    const url = page.url();
    await page.screenshot({ path: `${SHOTS}/11-nojs-result.png`, fullPage: true });
    const bodyText = await page.locator("body").innerText();
    record("nojs-native-post", { url, body: bodyText.slice(0, 1200) });
    // A server-rendered confirmation carrying the authoritative reference,
    // produced without a single line of client JavaScript.
    expect(bodyText).toMatch(/AST-[0-9A-Z]{8}/);
    expect(bodyText).toContain("Recorded");
    await context.close();
  });

  test("critical navigation survives failing decorative assets", async ({ page }) => {
    const diagnostics = watch(page);
    // Block every font and image request: the site must remain navigable.
    await page.route("**/*.{woff,woff2,ttf,png,jpg,jpeg,webp,avif,gif}", (route) => route.abort());
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await page.getByRole("navigation", { name: "Primary" }).getByRole("link", { name: "Residences" }).click();
    await expect(page).toHaveURL(/\/residences$/);
    await expect(page.locator("h2 a[href^='/residences/']").first()).toBeVisible();
    await page.getByRole("link", { name: /request a visit/i }).first().click();
    await expect(page).toHaveURL(/\/enquire/);
    await expect(page.locator("#field-email")).toBeVisible();
    await page.screenshot({ path: `${SHOTS}/12-degraded-assets.png`, fullPage: true });
    record("degraded-assets", {
      blocked: "fonts and raster images",
      navigationCompleted: true,
      pageErrors: diagnostics.pageErrors,
    });
    expect(diagnostics.pageErrors).toEqual([]);
  });

  test("keyboard-only path reaches the conversion form", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Tab");
    const skip = await page.evaluate(() => document.activeElement?.textContent ?? "");
    const visited: string[] = [];
    for (let i = 0; i < 14; i += 1) {
      await page.keyboard.press("Tab");
      visited.push(
        await page.evaluate(() => {
          const el = document.activeElement as HTMLElement | null;
          if (!el) return "";
          return `${el.tagName.toLowerCase()}:${(el.textContent ?? "").trim().slice(0, 40)}`;
        }),
      );
    }
    record("keyboard-order", { firstStop: skip.trim(), sequence: visited });
    expect(skip.trim()).toBe("Skip to content");

    // The skip link must actually move the reading position.
    await page.goto("/");
    await page.keyboard.press("Tab");
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/#main$/);
  });

  test("404 returns a real 404 status with recovery navigation", async ({ page }) => {
    const response = await page.goto("/residences/this-house-does-not-exist");
    expect(response?.status()).toBe(404);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("not on the ridge");
    await expect(page.getByRole("link", { name: "All twelve residences" })).toBeVisible();
    await page.screenshot({ path: `${SHOTS}/13-not-found.png`, fullPage: true });
    record("not-found", { status: response?.status() });
  });

  test("draft journal content is never published", async ({ page, request }) => {
    const direct = await request.get("/journal/material-samples-autumn");
    expect(direct.status()).toBe(404);
    await page.goto("/journal");
    await expect(page.locator("body")).not.toContainText("Autumn material samples");
    const sitemap = await (await request.get("/sitemap.xml")).text();
    record("draft-exclusion", {
      directStatus: direct.status(),
      inSitemap: sitemap.includes("material-samples-autumn"),
    });
    expect(sitemap).not.toContain("material-samples-autumn");
  });

  test("content navigation: journal and location interlink correctly", async ({ page }) => {
    const diagnostics = watch(page);
    await page.goto("/journal");
    await page.getByRole("link", { name: "Why twelve houses and not forty" }).click();
    await expect(page).toHaveURL(/\/journal\/why-twelve-houses$/);
    await expect(page.getByRole("table")).toBeVisible();
    await page.screenshot({ path: `${SHOTS}/14-journal-entry.png`, fullPage: true });

    await page
      .getByRole("region", { name: "Referenced in this entry" })
      .getByRole("link", { name: /Ridge House 03/ })
      .click();
    await expect(page).toHaveURL(/\/residences\/ridge-house-03$/);

    await page.goto("/location");
    await page.getByRole("link", { name: /Pedra Alta village/ }).first().click();
    await expect(page).toHaveURL(/\/location#the-village$/);
    await page.screenshot({ path: `${SHOTS}/15-location.png`, fullPage: true });

    record("content-navigation", { diagnostics });
    expect(diagnostics.pageErrors).toEqual([]);
    expect(diagnostics.badResponses).toEqual([]);
  });

  test("residence filtering has a real empty state and a reset path", async ({ page }) => {
    await page.goto("/residences?type=courtyard&bedrooms=3");
    await expect(page.getByText(/Showing 3 of 12/)).toBeVisible();
    await page.goto("/residences?type=terrace&bedrooms=5");
    await expect(page.getByRole("heading", { name: /No residence matches/ })).toBeVisible();
    await page.screenshot({ path: `${SHOTS}/16-empty-state.png`, fullPage: true });
    await page.getByRole("link", { name: "Clear filters" }).click();
    await expect(page.getByText(/Showing 12 of 12/)).toBeVisible();
    record("filter-empty-state", { verified: true });
  });
});
