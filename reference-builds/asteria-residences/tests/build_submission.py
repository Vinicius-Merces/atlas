from __future__ import annotations
import os
from pathlib import Path
import yaml

BUILD=Path(__file__).parents[1]
RUN=BUILD/'run'
freeze=os.environ['ASTERIA_FREEZE_SHA']
base='reference-builds/asteria-residences/evidence/'

def row(cid,status,evidence=(),notes=None):
    item={'id':cid,'status':status,'evidence':[base+x for x in evidence]}
    if notes:item['notes']=notes
    return item

checks=[
row('marketing-audience-outcome','pass',['screenshots/home-desktop.png']),
row('marketing-required-surfaces','pass',['screenshots/home-desktop.png','screenshots/solis-detail.png']),
row('marketing-prohibited-shortcuts','pass',['source-review.txt']),
row('marketing-content-authority','partial',['source-review.txt'],'Content is deliberately code-owned for the fixed fixture; no editor CMS is required for this calibration.'),
row('marketing-conversion-authority','pass',['browser-summary.json','data/leads.jsonl']),
row('marketing-stack-fit','pass',['source-review.txt']),
row('marketing-routing-core','pass',['source-review.txt']),
row('marketing-routing-public-web','pass',['browser-summary.json','source-review.txt']),
row('marketing-routing-no-theater','pass',['source-review.txt']),
row('marketing-navigation-complete','pass',['browser-summary.json']),
row('marketing-lead-authoritative','pass',['browser-summary.json','data/leads.jsonl']),
row('marketing-content-complete','pass',['screenshots/solis-detail.png','browser-summary.json']),
row('marketing-states-complete','pass',['browser-summary.json']),
row('marketing-visual-thesis','pass',['screenshots/home-desktop.png','screenshots/home-wide.png']),
row('marketing-responsive','pass',['screenshots/home-mobile.png','screenshots/home-tablet.png','screenshots/home-desktop.png','screenshots/home-wide.png','browser-summary.json']),
row('marketing-accessibility','partial',['browser-summary.json'],'Keyboard/focus, labels, semantics, reduced-motion implementation and viewport overflow were checked, but no full contrast/assistive-technology audit was performed.'),
row('marketing-motion-purpose','pass',['source-review.txt']),
row('marketing-visual-regression','pass',['screenshots/home-desktop.png','screenshots/home-mobile.png','screenshots/solis-detail.png']),
row('marketing-form-security','pass',['unit-tests.txt','source-review.txt']),
row('marketing-private-data','pass',['source-review.txt']),
row('marketing-provider-failure','pass',['browser-summary.json']),
row('marketing-duplicate-submit','pass',['browser-summary.json','data/leads.jsonl']),
row('marketing-degraded-assets','pass',['browser-summary.json']),
row('marketing-browser-primary-flow','pass',['browser-summary.json','screenshots/lead-success.png']),
row('marketing-browser-negative-flow','pass',['browser-summary.json']),
row('marketing-browser-console-network','pass',['browser-summary.json']),
row('marketing-production-domain','unverified',notes='Calibration is localhost-only; no public production deployment was created.'),
row('marketing-seo-indexing','partial',['browser-summary.json','source-review.txt'],'Metadata, robots, sitemap and canonicals are exercised locally; deployed crawl/index behavior cannot be verified without a production domain.'),
row('marketing-structured-data','pass',['browser-summary.json']),
row('marketing-performance','pass',['browser-summary.json']),
row('marketing-analytics','pass',['browser-summary.json']),
row('marketing-review-frontend','unverified',notes='The implementing session cannot perform an independent Frontend Craft review.'),
row('marketing-review-production','unverified',notes='The implementing session cannot perform the required independent production/benchmark review.'),
]
submission={
'benchmark_version':1,'spec_id':'premium-marketing-site','execution_mode':'live',
'run':{'runtime':'chatgpt','model':'GPT-5.6 Sol','repository':'Vinicius-Merces/atlas','commit':freeze,'evidence_root':'reference-builds/asteria-residences/evidence','environment_notes':'Isolated P4 calibration on localhost Chromium. No public production deployment; not a Codex or Claude Code target result.','tool_permissions':['GitHub repository read/write','GitHub Actions','Chromium via Playwright']},
'review':{'reviewer':'same-session-calibration-not-independent','outcome':'Changes required','evidence':[base+'browser-summary.json'],'notes':'Diagnostic only. The implementer does not self-issue independent approval.'},
'checks':checks}
RUN.mkdir(exist_ok=True)
(RUN/'submission.yaml').write_text(yaml.safe_dump(submission,sort_keys=False,allow_unicode=True),encoding='utf-8')
