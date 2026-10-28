#!/usr/bin/env bash
# check.sh — full local verification. CI runs the same steps.
set -u
cd "$(dirname "$0")"
fail=0

echo "=== 1. generated rule files ==="
python3 tools/build_rules.py >/dev/null && echo "  OK   build_rules.py" || { echo "  FAIL"; fail=1; }

echo "=== 2. session packs ==="
python3 tools/make_corpus.py >/dev/null && echo "  OK   make_corpus.py" || { echo "  FAIL"; fail=1; }
n=$(ls -1 context/packs/session_pack_*.md 2>/dev/null | wc -l)
echo "  packs: $n"
[ "$n" -ge 12 ] || { echo "  FAIL too few packs"; fail=1; }

echo "=== 3. trigger audit (model-facing vocabulary) ==="
python3 tools/trigger_audit.py --strict | tail -6 || fail=1

echo "=== 4. inject smoke test ==="
python3 tools/inject.py --task "check.sh smoke test" --packs 2 --out out/check_smoke.txt >/dev/null \
  && echo "  OK   inject.py" || { echo "  FAIL"; fail=1; }
[ -s out/check_smoke.txt ] || { echo "  FAIL empty output"; fail=1; }

echo "=== 5. manifest ==="
python3 tools/make_manifest.py >/dev/null
python3 tools/verify_manifest.py | tail -4 || fail=1

echo "=== 6. syntax ==="
for f in bootstrap.sh check.sh verify/check_artifacts.sh tools/yt_audio.sh; do
  bash -n "$f" && echo "  OK   bash -n $f" || { echo "  FAIL $f"; fail=1; }
done
python3 -m compileall -q tools verify tests && echo "  OK   python compileall" || { echo "  FAIL"; fail=1; }

echo "=== 7. unit tests ==="
if command -v pytest >/dev/null 2>&1 || python3 -c 'import pytest' 2>/dev/null; then
  python3 -m pytest -q tests/ || fail=1
else
  echo "  SKIP pytest not installed (CI will run it)"
fi

echo "=== 8. bootstrap dry-run ==="
T=$(mktemp -d); bash bootstrap.sh "$T" >/dev/null 2>&1
cnt=$(find "$T" -type f | wc -l); echo "  installed $cnt files"
[ "$cnt" -ge 8 ] || { echo "  FAIL"; fail=1; }
rm -rf "$T"

echo
[ "$fail" -eq 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit "$fail"
