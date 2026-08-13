#!/usr/bin/env bash
# Boots the production build in four configurations used by the evidence run.
#
#  3100  primary evidence instance (rate capacity raised to 50 so one suite can
#        exercise many journeys from a single source IP; every other setting is
#        the production default)
#  3101  production-default instance (rate capacity 5) — used to prove the limiter
#  3102  ASTERIA_STORE_MODE=fail   — authoritative store failure
#  3103  ASTERIA_BROKER_MODE=fail  — downstream provider failure
set -euo pipefail
cd "$(dirname "$0")/.."

COMMON_ENV=(
  ASTERIA_ORIGIN=https://asteria-residences.example
  ASTERIA_ADMIN_KEY=bench-p4-admin-key-3f9c2a71
  ASTERIA_IP_SALT=bench-p4-salt
)

start() {
  local port=$1; shift
  local db=$1; shift
  env "${COMMON_ENV[@]}" ASTERIA_DB_PATH="./data/$db" "$@" \
    npx next start -p "$port" > "/tmp/asteria-$port.log" 2>&1 &
  echo "started :$port ($db) $*"
}

# Kill any previous instance, including the next-server child processes, so no
# stale process keeps a deleted database inode open.
pkill -9 -f "next start" 2>/dev/null || true
pkill -9 -f "next-server" 2>/dev/null || true
sleep 2
rm -rf data && mkdir -p data

start 3100 primary.db   ASTERIA_RATE_CAPACITY=50
start 3101 ratelimit.db ASTERIA_RATE_CAPACITY=5 ASTERIA_RATE_WINDOW_MS=600000
start 3102 storefail.db ASTERIA_RATE_CAPACITY=50 ASTERIA_STORE_MODE=fail
start 3103 brokerfail.db ASTERIA_RATE_CAPACITY=50 ASTERIA_BROKER_MODE=fail

for port in 3100 3101 3102 3103; do
  for _ in $(seq 1 40); do
    if curl -sf -o /dev/null "http://localhost:$port/"; then break; fi
    sleep 0.5
  done
done
echo "all instances ready"
