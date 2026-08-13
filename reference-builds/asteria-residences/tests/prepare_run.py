from __future__ import annotations
from pathlib import Path

BUILD=Path(__file__).parents[1]
SITE=BUILD/'site'
EVID=BUILD/'evidence'
(EVID/'data').mkdir(parents=True,exist_ok=True)

privacy='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privacy — Asteria</title><link rel="canonical" href="http://127.0.0.1:4173/privacy.html"><link rel="stylesheet" href="/assets/styles.css"></head><body><main class="shell page-hero"><p class="eyebrow">Privacy</p><h1>A small, explicit data boundary.</h1><p class="lede">This fictional calibration uses visit details only to exercise its request flow. A real launch requires jurisdiction-specific retention, rights and controller information.</p><p><a href="/">Return home</a></p></main></body></html>'''
(SITE/'privacy.html').write_text(privacy,encoding='utf-8')
(SITE/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: http://127.0.0.1:4173/sitemap.xml\n',encoding='utf-8')
urls=['/','/residences.html','/residences/solis.html','/guide.html','/privacy.html']
xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>http://127.0.0.1:4173{u}</loc></url>' for u in urls)+'</urlset>'
(SITE/'sitemap.xml').write_text(xml,encoding='utf-8')
review='''Workflow: site-from-brief-delivery
Stack: authored HTML/CSS/JS plus Python standard-library service; no frontend package dependency chain.
Server: validation, request-size cap, rate limit, idempotency, private persistence, test-only failure injection.
Public web: canonical metadata, robots, sitemap, WebSite/Residence/Article JSON-LD.
Frontend thesis: limestone/mineral editorial system, original vector scenes, restrained reveal motion, reduced-motion override.
Not routed: authenticated SaaS tenancy, payments, RLS, queues or privileged admin primitives.
'''
(EVID/'source-review.txt').write_text(review,encoding='utf-8')
