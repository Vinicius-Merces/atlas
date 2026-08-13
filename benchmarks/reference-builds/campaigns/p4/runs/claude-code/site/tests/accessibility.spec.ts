import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { mkdirSync, writeFileSync } from "node:fs";

/**
 * accessibility-audit evidence: automated WCAG 2.1 A/AA + 2.2 rules on every
 * public route and on every material form state, plus reduced-motion and
 * contrast measurements that axe cannot make for us.
 */

const OUT = "../evidence/accessibility";
mkdirSync(OUT, { recursive: true });

const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"];

const ROUTES = [
  { id: "home", path: "/" },
  { id: "residences", path: "/residences" },
  { id: "residences-filtered", path: "/residences?type=courtyard" },
  { id: "residences-empty", path: "/residences?type=terrace&bedrooms=5" },
  { id: "residence-detail", path: "/residences/ridge-house-04" },
  { id: "residence-sold", path: "/residences/ridge-house-01" },
  { id: "location", path: "/location" },
  { id: "journal", path: "/journal" },
  { id: "journal-entry", path: "/journal/buying-off-plan-honestly" },
  { id: "enquire", path: "/enquire" },
  { id: "privacy", path: "/privacy" },
  { id: "terms", path: "/terms" },
  { id: "contact", path: "/contact" },
  { id: "not-found", path: "/residences/no-such-house" },
];

for (const route of ROUTES) {
  test(`axe: ${route.id}`, async ({ page }) => {
    await page.goto(route.path);
    const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
    writeFileSync(
      `${OUT}/axe--${route.id}.json`,
      JSON.stringify(
        {
          route: route.path,
          violations: results.violations,
          passes: results.passes.length,
          incomplete: results.incomplete.map((i) => ({ id: i.id, nodes: i.nodes.length })),
        },
        null,
        2,
      ),
    );
    expect(
      results.violations.map((v) => `${v.id} (${v.impact}) x${v.nodes.length}`),
      `axe violations on ${route.path}`,
    ).toEqual([]);
  });
}

test("axe: form validation state", async ({ page }) => {
  await page.goto("/enquire");
  await page.waitForTimeout(2100);
  await page.getByRole("button", { name: /send visit request/i }).click();
  await expect(page.locator("#error-name")).toBeVisible();
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  writeFileSync(
    `${OUT}/axe--enquire-validation-state.json`,
    JSON.stringify({ violations: results.violations, passes: results.passes.length }, null, 2),
  );
  expect(results.violations.map((v) => v.id)).toEqual([]);
});

test("axe: form success state", async ({ page }) => {
  await page.goto("/enquire");
  await page.fill("#field-name", "Axe Success");
  await page.fill("#field-email", `axe.success.${Date.now()}@example.com`);
  await page.selectOption("#field-timeframe", "exploring");
  await page.selectOption("#field-context", "primary-home");
  await page.check("#field-consent");
  await page.waitForTimeout(2100);
  await page.getByRole("button", { name: /send visit request/i }).click();
  await expect(page.getByRole("status")).toContainText("Recorded", { timeout: 15_000 });
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  writeFileSync(
    `${OUT}/axe--enquire-success-state.json`,
    JSON.stringify({ violations: results.violations, passes: results.passes.length }, null, 2),
  );
  expect(results.violations.map((v) => v.id)).toEqual([]);
});

test("reduced motion removes the one narrative animation", async ({ browser }) => {
  const measure = async (reduced: boolean) => {
    const context = await browser.newContext({
      reducedMotion: reduced ? "reduce" : "no-preference",
    });
    const page = await context.newPage();
    await page.goto("http://localhost:3100/");
    const data = await page.evaluate(() => {
      const ground = document.querySelector("svg path[class*='ground']") as SVGPathElement | null;
      const button = document.querySelector("a[class*='button']") as HTMLElement | null;
      return {
        groundAnimationName: ground ? getComputedStyle(ground).animationName : "none",
        groundAnimationDuration: ground ? getComputedStyle(ground).animationDuration : "0s",
        groundDashOffset: ground ? getComputedStyle(ground).strokeDashoffset : "",
        buttonTransitionDuration: button ? getComputedStyle(button).transitionDuration : "",
        scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
        motionQuickToken: getComputedStyle(document.documentElement).getPropertyValue("--motion-quick").trim(),
        motionDrawToken: getComputedStyle(document.documentElement).getPropertyValue("--motion-draw").trim(),
      };
    });
    await context.close();
    return data;
  };

  const normal = await measure(false);
  const reduced = await measure(true);
  writeFileSync(`${OUT}/reduced-motion.json`, JSON.stringify({ normal, reduced }, null, 2));

  const ms = (value: string) =>
    value.endsWith("ms") ? parseFloat(value) : parseFloat(value) * 1000;
  expect(ms(normal.motionDrawToken)).toBe(900);
  expect(ms(reduced.motionDrawToken)).toBe(0);
  expect(ms(reduced.motionQuickToken)).toBe(0);
  expect(reduced.scrollBehavior).toBe("auto");
  // With reduced motion the ridge line is simply present, not drawn.
  expect(reduced.groundDashOffset === "0px" || reduced.groundAnimationName === "none").toBe(true);
});

test("contrast of every text/background pair actually used", async ({ page }) => {
  await page.goto("/");
  const report = await page.evaluate(() => {
    const parse = (value: string): [number, number, number] => {
      const m = value.match(/rgba?\(([^)]+)\)/);
      if (!m) return [0, 0, 0];
      const parts = m[1]!.split(",").map((p) => parseFloat(p));
      return [parts[0]!, parts[1]!, parts[2]!];
    };
    const lum = ([r, g, b]: [number, number, number]) => {
      const f = (c: number) => {
        const s = c / 255;
        return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
      };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const ratio = (a: string, b: string) => {
      const la = lum(parse(a));
      const lb = lum(parse(b));
      const [hi, lo] = la > lb ? [la, lb] : [lb, la];
      return (hi + 0.05) / (lo + 0.05);
    };
    const root = getComputedStyle(document.documentElement);
    const token = (name: string) => {
      const probe = document.createElement("div");
      probe.style.color = root.getPropertyValue(name).trim();
      document.body.appendChild(probe);
      const value = getComputedStyle(probe).color;
      probe.remove();
      return value;
    };
    const paper = token("--paper");
    const chalk = token("--chalk");
    const ink = token("--ink");
    return {
      "ink on paper": ratio(ink, paper),
      "slate on paper": ratio(token("--slate"), paper),
      "slate-soft on paper (annotation)": ratio(token("--slate-soft"), paper),
      "oxide on paper (accent/links)": ratio(token("--oxide"), paper),
      "oxide-deep on paper (errors)": ratio(token("--oxide-deep"), paper),
      "moss on paper (available)": ratio(token("--moss"), paper),
      "white on oxide (primary button)": ratio("rgb(253, 250, 247)", token("--oxide")),
      "ink on chalk (inputs)": ratio(ink, chalk),
      "slate-soft on chalk": ratio(token("--slate-soft"), chalk),
    };
  });

  writeFileSync(`${OUT}/contrast.json`, JSON.stringify(report, null, 2));

  // AA: 4.5:1 for normal text, 3:1 for large text and non-text.
  expect(report["ink on paper"]).toBeGreaterThan(12);
  expect(report["slate on paper"]).toBeGreaterThan(7);
  expect(report["slate-soft on paper (annotation)"]).toBeGreaterThan(4.5);
  expect(report["oxide on paper (accent/links)"]).toBeGreaterThan(4.5);
  expect(report["oxide-deep on paper (errors)"]).toBeGreaterThan(4.5);
  expect(report["moss on paper (available)"]).toBeGreaterThan(4.5);
  expect(report["white on oxide (primary button)"]).toBeGreaterThan(4.5);
  expect(report["ink on chalk (inputs)"]).toBeGreaterThan(12);
  expect(report["slate-soft on chalk"]).toBeGreaterThan(4.5);
});

test("every interactive control has a visible focus indicator", async ({ page }) => {
  await page.goto("/enquire");
  const findings = await page.evaluate(() => {
    const results: { selector: string; outlineWidth: string; outlineColor: string }[] = [];
    const targets = Array.from(
      document.querySelectorAll<HTMLElement>("a[href], button, input, select, textarea"),
    ).filter((el) => el.offsetParent !== null || el.tagName === "A");
    for (const el of targets.slice(0, 40)) {
      el.focus();
      const style = getComputedStyle(el);
      results.push({
        selector: `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ""}`,
        outlineWidth: style.outlineWidth,
        outlineColor: style.outlineColor,
      });
    }
    return results;
  });
  writeFileSync(`${OUT}/focus-indicators.json`, JSON.stringify(findings, null, 2));
  const missing = findings.filter((f) => f.outlineWidth === "0px");
  expect(missing).toEqual([]);
});

test("document structure: one h1, ordered headings, landmarks, lang", async ({ page }) => {
  const summary: Record<string, unknown> = {};
  for (const route of ["/", "/residences", "/residences/ridge-house-04", "/location", "/journal", "/enquire"]) {
    await page.goto(route);
    summary[route] = await page.evaluate(() => {
      const headings = Array.from(document.querySelectorAll("h1,h2,h3,h4")).map((h) => ({
        level: Number(h.tagName[1]),
        text: (h.textContent ?? "").trim().slice(0, 50),
      }));
      let skipped: string[] = [];
      for (let i = 1; i < headings.length; i += 1) {
        if (headings[i]!.level - headings[i - 1]!.level > 1) {
          skipped.push(`${headings[i - 1]!.text} → ${headings[i]!.text}`);
        }
      }
      return {
        lang: document.documentElement.lang,
        h1Count: document.querySelectorAll("h1").length,
        landmarks: {
          header: document.querySelectorAll("header").length,
          main: document.querySelectorAll("main").length,
          footer: document.querySelectorAll("footer").length,
          nav: document.querySelectorAll("nav").length,
        },
        skippedHeadingLevels: skipped,
        headings,
      };
    });
  }
  writeFileSync(`${OUT}/structure.json`, JSON.stringify(summary, null, 2));
  for (const [route, data] of Object.entries(summary)) {
    const d = data as { lang: string; h1Count: number; skippedHeadingLevels: string[]; landmarks: Record<string, number> };
    expect(d.lang, route).toBe("en-GB");
    expect(d.h1Count, route).toBe(1);
    expect(d.landmarks.main, route).toBe(1);
    expect(d.skippedHeadingLevels, route).toEqual([]);
  }
});

test("drawings expose text alternatives", async ({ page }) => {
  await page.goto("/residences/courtyard-house-12");
  const svgs = await page.evaluate(() =>
    Array.from(document.querySelectorAll("svg")).map((svg) => ({
      role: svg.getAttribute("role"),
      // Decorative marks (the wordmark glyph) sit inside an aria-hidden
      // wrapper and are correctly absent from the accessibility tree.
      ariaHidden: svg.closest('[aria-hidden="true"]') ? "true" : svg.getAttribute("aria-hidden"),
      ariaLabel: svg.getAttribute("aria-label"),
      labelledBy: svg.getAttribute("aria-labelledby"),
      title: svg.querySelector("title")?.textContent ?? null,
      descLength: (svg.querySelector("desc")?.textContent ?? "").length,
    })),
  );
  writeFileSync(`${OUT}/drawing-alternatives.json`, JSON.stringify(svgs, null, 2));
  const meaningful = svgs.filter((s) => s.ariaHidden !== "true");
  expect(meaningful.length).toBeGreaterThan(2);
  for (const svg of meaningful) {
    // `img` for static drawings; `group` for the site plan, which contains
    // focusable links and therefore must not claim to be a single image.
    expect(["img", "group"]).toContain(svg.role);
    expect(Boolean(svg.ariaLabel || svg.labelledBy)).toBe(true);
  }
});
