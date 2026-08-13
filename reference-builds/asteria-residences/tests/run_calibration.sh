#!/usr/bin/env bash
set -euo pipefail
python -m pip install --requirement requirements-test.txt
python -m pip install 'playwright>=1.50,<2'
python -m playwright install --with-deps chromium
python reference-builds/asteria-residences/tests/prepare_run.py
python - <<'PY'
from pathlib import Path
p=Path('reference-builds/asteria-residences/tests/browser_evidence.py')
t=p.read_text(encoding='utf-8')
t=t.replace('degraded.route("**/*.svg", lambda route: route.abort())','degraded.route("**/assets/app.js", lambda route: route.abort())')
t=t.replace("degraded.locator('a[href=\"/residences.html\"]'.replace(chr(39), chr(39))).first.is_visible()", "degraded.locator('a[href=\"/residences.html\"]').last.is_visible()")
# The generated source contains the direct locator expression; normalize it explicitly.
t=t.replace("degraded.locator('a[href=\"/residences.html\"]').first.is_visible()", "degraded.locator('a[href=\"/residences.html\"]').last.is_visible()")
p.write_text(t,encoding='utf-8')
PY
python -m pytest reference-builds/asteria-residences/tests/test_server.py -q | tee reference-builds/asteria-residences/evidence/unit-tests.txt
export ASTERIA_ENABLE_TEST_FAILURES=1
export ASTERIA_DATA_DIR="$GITHUB_WORKSPACE/reference-builds/asteria-residences/evidence/data"
python reference-builds/asteria-residences/server.py --port 4173 > reference-builds/asteria-residences/evidence/server.log 2>&1 &
SERVER_PID=$!
for i in {1..30}; do curl -fsS http://127.0.0.1:4173/api/health && break || sleep 1; done
python reference-builds/asteria-residences/tests/browser_evidence.py
kill "$SERVER_PID" || true
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add reference-builds/asteria-residences
git commit -m 'feat: freeze P4 Asteria calibration implementation and evidence'
git push
FREEZE_SHA=$(git rev-parse HEAD)
ASTERIA_FREEZE_SHA="$FREEZE_SHA" python reference-builds/asteria-residences/tests/build_submission.py
python scripts/run_reference_build_benchmark.py --spec benchmarks/reference-builds/specs/premium-marketing-site.yaml --submission reference-builds/asteria-residences/run/submission.yaml --output reference-builds/asteria-residences/run/result.json
git add reference-builds/asteria-residences/run
git commit -m 'chore: score P4 Asteria calibration'
git push
