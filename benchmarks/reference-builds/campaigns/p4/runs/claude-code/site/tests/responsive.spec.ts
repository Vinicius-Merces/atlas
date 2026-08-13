import { test, expect } from "@playwright/test";
import { mkdirSync, writeFileSync } from "node:fs";

/**
 * responsive-layout-audit + visual-regression-review evidence.
 *
 * Deterministic full-page captures at five viewports for every critical route,
 * plus programmatic assertions that composition survives rather than merely
 * stacking: no horizontal overflow, no clipped text, tap targets large enough,
 * body measure inside its bound.
 */

const OUT = "../evidence/responsive";
const REG = "../evidence/visual-regression";
mkdirSync(OUT, { recursive: true });
mkdirSync(REG, { recursive: true });

const VIEWPORTS = [
  { id: "phone-360", width: 360, height: 780, scale: 3 },
  { id: "phone-414", width: 414, height: 896, scale: 2 },
  { id: "tablet-768", width: 768, height: 1024, scale: 2 },
  { id: "laptop-1280", width: 1280, height: 800, scale: 1 },
  { id: "wide-1920", width: 1920, height: 1080, scale: 1 },
];

const ROUTES = [
  { id: "home", path: "/" },
  { id: "residences", path: "/residences" },
  { id: "residence-detail", path: "/residences/ridge-house-04" },
  { id: "location", path: "/location" },
  { id: "journal", path: "/journal" },
  { id: "journal-entry", path: "/journal/why-twelve-houses" },
  { id: "enquire", path: "/enquire" },
  { id: "privacy", path: "/privacy" },
];

type Measurement = {
  route: string;
  viewport: string;
  documentWidth: number;
  viewportWidth: number;
  horizontalOverflow: number;
  overflowingSelectors: string[];
  smallTapTargets: { text: string; width: number; height: number }[];
  longestLineChars: number;
  longestSample: string;
  headingSizePx: number;
};

const measurements: Measurement[] = [];

for (const viewport of VIEWPORTS) {
  test.describe(`viewport ${viewport.id}`, () => {
    test.use({
      viewport: { width: viewport.width, height: viewport.height },
      deviceScaleFactor: viewport.scale,
      isMobile: viewport.width < 768,
      hasTouch: viewport.width < 768,
    });

    for (const route of ROUTES) {
      test(`${route.id} composes at ${viewport.id}`, async ({ page }) => {
        await page.goto(route.path, { waitUntil: "networkidle" });
        // Freeze the one animation so captures are byte-stable.
        await page.addStyleTag({
          content: `*,*::before,*::after{animation:none !important;transition:none !important}`,
        });
        await page.waitForTimeout(120);

        const data = await page.evaluate(() => {
          const doc = document.documentElement;
          const viewportWidth = doc.clientWidth;
          const overflowing: string[] = [];
          document.querySelectorAll<HTMLElement>("body *").forEach((element) => {
            const rect = element.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) return;
            if (rect.right > viewportWidth + 1 || rect.left < -1) {
              const id = element.id ? `#${element.id}` : "";
              const cls =
                typeof element.className === "string" && element.className
                  ? `.${element.className.split(/\s+/).slice(0, 1).join(".")}`
                  : "";
              overflowing.push(`${element.tagName.toLowerCase()}${id}${cls}`);
            }
          });

          const smallTapTargets: { text: string; width: number; height: number }[] = [];
          document
            .querySelectorAll<HTMLElement>("a, button, input, select, textarea, [role=button]")
            .forEach((element) => {
              const rect = element.getBoundingClientRect();
              if (rect.width === 0 || rect.height === 0) return;
              const inProse = element.closest("p, li, dd, figcaption, address, nav ol");
              if (inProse) return; // inline text links are exempt from the 24px rule
              // Honeypot and other aria-hidden decoys are deliberately tiny and
              // are removed from the accessibility tree and the tab order.
              if (element.closest('[aria-hidden="true"]')) return;
              if (element.getAttribute("tabindex") === "-1" && rect.width <= 2) return;
              if (rect.height < 24 || rect.width < 24) {
                smallTapTargets.push({
                  text: (element.textContent ?? "").trim().slice(0, 40),
                  width: Math.round(rect.width),
                  height: Math.round(rect.height),
                });
              }
            });

          // Longest ACTUAL rendered line, measured with a Range so the number
          // reflects the text line box rather than its container.
          let longest = 0;
          let longestSample = "";
          const BLOCK = new Set([
            "P", "DIV", "UL", "OL", "LI", "H1", "H2", "H3", "H4", "TABLE", "SECTION",
            "FIGURE", "BLOCKQUOTE", "DL", "DD", "DT", "ASIDE", "NAV", "ARTICLE", "FORM",
          ]);
          document.querySelectorAll<HTMLElement>("p, li, dd").forEach((element) => {
            const text = (element.textContent ?? "").trim();
            if (text.length < 90) return;
            // Only measure elements whose content is a single text flow; a
            // container of block children has no meaningful "line".
            if (Array.from(element.children).some((child) => BLOCK.has(child.tagName))) return;
            if (element.closest('[aria-hidden="true"]')) return;
            const style = getComputedStyle(element);
            const fontSize = parseFloat(style.fontSize);
            const range = document.createRange();
            range.selectNodeContents(element);
            const rects = Array.from(range.getClientRects());
            if (!rects.length) return;
            // Average glyph advance for the rendered font, sampled from the
            // widest full line rather than assumed.
            const widest = Math.max(...rects.map((r) => r.width));
            const chars = widest / (fontSize * 0.48);
            if (chars > longest) {
              longest = chars;
              longestSample = text.slice(0, 60);
            }
          });

          const h1 = document.querySelector("h1");
          return {
            documentWidth: Math.round(doc.scrollWidth),
            viewportWidth,
            overflowing: Array.from(new Set(overflowing)).slice(0, 12),
            smallTapTargets,
            longestLineChars: Math.round(longest),
            longestSample,
            headingSizePx: h1 ? Math.round(parseFloat(getComputedStyle(h1).fontSize)) : 0,
          };
        });

        const measurement: Measurement = {
          route: route.id,
          viewport: viewport.id,
          documentWidth: data.documentWidth,
          viewportWidth: data.viewportWidth,
          horizontalOverflow: Math.max(0, data.documentWidth - data.viewportWidth),
          overflowingSelectors: data.overflowing,
          smallTapTargets: data.smallTapTargets,
          longestLineChars: data.longestLineChars,
          longestSample: data.longestSample,
          headingSizePx: data.headingSizePx,
        };
        measurements.push(measurement);
        writeFileSync(
          `${OUT}/measure--${route.id}--${viewport.id}.json`,
          JSON.stringify(measurement, null, 2),
        );

        await page.screenshot({
          path: `${REG}/${route.id}--${viewport.id}.png`,
          fullPage: true,
          animations: "disabled",
        });

        // Assertions
        expect(measurement.horizontalOverflow, `horizontal overflow on ${route.id}`).toBeLessThanOrEqual(1);
        expect(measurement.overflowingSelectors, `overflowing elements on ${route.id}`).toEqual([]);
        expect(measurement.smallTapTargets, `small tap targets on ${route.id}`).toEqual([]);
        expect(measurement.longestLineChars, `measure on ${route.id}`).toBeLessThanOrEqual(80);
        expect(measurement.headingSizePx).toBeGreaterThan(24);
      });
    }
  });
}
