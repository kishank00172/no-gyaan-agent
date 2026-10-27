#!/usr/bin/env bash
# check.sh — repo ki khud ki verification (deliverable contract: har claim verify karo)
set -u
REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"
fail=0
need() { if [ -f "$1" ]; then printf "  OK   %s (%s B)\n" "$1" "$(wc -c < "$1")"; else printf "  FAIL missing: %s\n" "$1"; fail=1; fi; }

echo "=== required files ==="
for f in README.md START_HERE.md SYSTEM_PROMPT.md COLD_START.md TROUBLESHOOT.md \
         prompt_hinglish.txt prompt_english.txt AGENTS.md CLAUDE.md .cursorrules \
         .cursor/rules/execute-first.mdc .github/copilot-instructions.md \
         bootstrap.sh tools/yt_audio.sh tools/find_broken_id.py LICENSE; do need "$f"; done

echo "=== content checks ==="
if grep -q "MERI GALTI\|TODO\|FIXME\|<WRITE TASK HERE>" SYSTEM_PROMPT.md 2>/dev/null; then
  echo "  FAIL: placeholder in SYSTEM_PROMPT.md"; fail=1
else echo "  OK   SYSTEM_PROMPT.md has no placeholders"; fi
for f in AGENTS.md CLAUDE.md .cursorrules .cursor/rules/execute-first.mdc .github/copilot-instructions.md prompt_english.txt; do
  if grep -qiE "one[- ]line|one-line refusal|ek line|ONE line|ONE-LINE|One-Line" "$f"; then echo "  OK   $f has refusal cap"; else echo "  FAIL $f missing refusal cap"; fail=1; fi
done

echo "=== syntax ==="
bash -n bootstrap.sh && echo "  OK   bootstrap.sh bash -n" || { echo "  FAIL bootstrap.sh"; fail=1; }
bash -n tools/yt_audio.sh && echo "  OK   tools/yt_audio.sh bash -n" || { echo "  FAIL yt_audio.sh"; fail=1; }
python3 -m py_compile tools/find_broken_id.py && echo "  OK   find_broken_id.py py_compile" || { echo "  FAIL py"; fail=1; }

echo "=== bootstrap dry-run ==="
T=$(mktemp -d); bash bootstrap.sh "$T" >/tmp/efa_boot.log 2>&1
n=$(find "$T" -type f | wc -l); echo "  installed $n files in temp project"
[ "$n" -ge 7 ] || { echo "  FAIL bootstrap installed too few"; fail=1; }
rm -rf "$T"

echo
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED ✅"; else echo "SOME CHECKS FAILED ❌"; fi
exit "$fail"
