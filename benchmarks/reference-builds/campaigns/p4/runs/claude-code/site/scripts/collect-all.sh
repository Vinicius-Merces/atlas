#!/usr/bin/env bash
# Reproduces the whole evidence tree from a clean build.
set -uo pipefail
cd "$(dirname "$0")/.."

echo "== build =="
npx next build || exit 1

echo "== servers =="
bash scripts/servers.sh || exit 1

status=0
run() {
  echo; echo "== $1 =="
  shift
  "$@" || status=1
}

run "browser flows"    npx playwright test tests/browser-flows.spec.ts --project=desktop-chromium
run "responsive"       npx playwright test tests/responsive.spec.ts --project=desktop-chromium
run "accessibility"    npx playwright test tests/accessibility.spec.ts --project=desktop-chromium
run "api contract"     node scripts/collect-api-contract.mjs
run "seo"              node scripts/collect-seo.mjs
run "structured data"  node scripts/collect-structured-data.mjs
run "performance"      node scripts/collect-performance.mjs
run "security"         node scripts/collect-security.mjs
run "supply chain"     node scripts/collect-supply-chain.mjs
run "content"          node scripts/validate-content.mjs

echo; echo "overall: $([ $status -eq 0 ] && echo PASS || echo 'ATTENTION NEEDED')"
exit $status
