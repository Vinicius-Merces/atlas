from __future__ import annotations

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("ASTERIA_BASE_URL", "http://127.0.0.1:4173")
OUT = Path(os.environ.get("ASTERIA_EVIDENCE_DIR", str(Path(__file__).parents[1] / "evidence")))
(OUT / "screenshots").mkdir(parents=True, exist_ok=True)
summary = {"base_url": BASE, "console_errors": [], "request_failures": [], "viewports": {}, "flows": {}, "accessibility": {}, "seo": {}, "performance": {}}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, viewport in {"mobile": {"width": 390, "height": 844}, "tablet": {"width": 768, "height": 1024}, "desktop": {"width": 1440, "height": 900}, "wide": {"width": 1728, "height": 1000}}.items():
        page = browser.new_page(viewport=viewport)
        errors: list[str] = []
        failures: list[str] = []
        page.on("console", lambda msg, bucket=errors: bucket.append(msg.text) if msg.type == "error" else None)
        page.on("requestfailed", lambda req, bucket=failures: bucket.append(req.url))
        page.goto(BASE + "/", wait_until="networkidle")
        assert page.locator("h1").is_visible()
        assert page.locator("#visit-form").is_visible()
        page.screenshot(path=str(OUT / "screenshots" / f"home-{name}.png"), full_page=True)
        overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        summary["viewports"][name] = {"overflow": overflow, "h1": page.locator("h1").inner_text()}
        summary["console_errors"].extend(errors)
        summary["request_failures"].extend(failures)
        page.close()

    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(BASE + "/residences.html", wait_until="networkidle")
    page.locator('a[href="/residences/solis.html"]').click()
    page.wait_for_url("**/residences/solis.html")
    assert "412 m²" in page.locator("main").inner_text()
    page.screenshot(path=str(OUT / "screenshots" / "solis-detail.png"), full_page=True)
    summary["flows"]["residence_discovery"] = "pass"

    page.goto(BASE + "/#visit", wait_until="networkidle")
    form = page.locator("#visit-form")
    form.locator('button[type="submit"]').click()
    page.wait_for_timeout(100)
    assert page.evaluate("document.activeElement && document.activeElement.id") == "name"
    summary["flows"]["validation_focus"] = "pass"

    def fill(name: str, email: str, interest: str) -> None:
        form.locator("#name").fill(name)
        form.locator("#email").fill(email)
        form.locator("#phone").fill("+55 11 99999-9999")
        form.locator("#interest").select_option(label=interest)
        form.locator("#consent").check()

    fill("Ada Mercer", "ada@example.com", "Solis")
    form.locator('button[type="submit"]').click()
    page.wait_for_function("document.querySelector('#form-status').dataset.state === 'success'")
    assert [event["event"] for event in page.evaluate("window.asteriaAnalytics")] == ["lead_submitted"]
    page.screenshot(path=str(OUT / "screenshots" / "lead-success.png"), full_page=True)
    summary["flows"]["authoritative_lead_success"] = "pass"
    summary["flows"]["analytics_after_success"] = "pass"

    page.evaluate("window.__ASTERIA_TEST_FAILURE__=true")
    fill("Mara Stone", "mara@example.com", "Atrium")
    form.locator('button[type="submit"]').click()
    page.wait_for_function("document.querySelector('#form-status').dataset.state === 'error'")
    assert len(page.evaluate("window.asteriaAnalytics")) == 1
    page.evaluate("window.__ASTERIA_TEST_FAILURE__=false")
    form.locator('button[type="submit"]').click()
    page.wait_for_function("document.querySelector('#form-status').dataset.state === 'success'")
    assert len(page.evaluate("window.asteriaAnalytics")) == 2
    summary["flows"]["provider_failure_recovery"] = "pass"
    summary["flows"]["no_false_success_event"] = "pass"

    payload = {"name": "Duplicate Test", "email": "dupe@example.com", "phone": "+5511777777777", "interest": "Garden", "consent": True, "idempotency_key": "fixed-duplicate-key-0001"}
    first = page.request.post(BASE + "/api/leads", data=payload)
    second = page.request.post(BASE + "/api/leads", data=payload)
    assert first.status == 201 and second.status == 200
    assert first.json()["lead_id"] == second.json()["lead_id"] and second.json()["duplicate"] is True
    summary["flows"]["duplicate_protection"] = "pass"

    summary["accessibility"] = page.evaluate("""() => ({missingAlt:document.querySelectorAll('img:not([alt])').length,missingLabels:[...document.querySelectorAll('input,select,textarea')].filter(el=>!document.querySelector(`label[for=\"${el.id}\"]`)).length,main:!!document.querySelector('main'),nav:!!document.querySelector('nav'),footer:!!document.querySelector('footer'),lang:document.documentElement.lang})""")
    nav = page.evaluate("""() => {const n=performance.getEntriesByType('navigation')[0];return {domContentLoaded:Math.round(n.domContentLoadedEventEnd),load:Math.round(n.loadEventEnd),resources:performance.getEntriesByType('resource').length}}""")
    summary["performance"] = nav
    for text in page.locator('script[type="application/ld+json"]').all_text_contents():
        json.loads(text)
    summary["seo"]["home_jsonld"] = "valid"
    summary["seo"]["home_canonical"] = page.locator('link[rel="canonical"]').get_attribute("href")

    page.goto(BASE + "/guide.html", wait_until="networkidle")
    for text in page.locator('script[type="application/ld+json"]').all_text_contents():
        json.loads(text)
    summary["seo"]["guide_jsonld"] = "valid"
    summary["seo"]["guide_internal_links"] = page.locator("article a").count()
    summary["seo"]["robots_has_sitemap"] = "Sitemap:" in page.request.get(BASE + "/robots.txt").text()
    summary["seo"]["sitemap_urls"] = page.request.get(BASE + "/sitemap.xml").text().count("<url>")

    degraded = browser.new_page(viewport={"width": 390, "height": 844})
    degraded.route("**/*.svg", lambda route: route.abort())
    degraded.goto(BASE + "/", wait_until="domcontentloaded")
    assert degraded.locator("h1").is_visible() and degraded.locator('a[href="/residences.html"]').first.is_visible()
    summary["flows"]["degraded_media_navigation"] = "pass"
    degraded.close()
    browser.close()

summary["console_errors"] = list(dict.fromkeys(summary["console_errors"]))
summary["request_failures"] = list(dict.fromkeys(summary["request_failures"]))
(OUT / "browser-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
assert not summary["console_errors"]
assert not summary["request_failures"]
assert all(not row["overflow"] for row in summary["viewports"].values())
print(json.dumps(summary, indent=2))
