#!/usr/bin/env bash
# bootstrap.sh — install execute-first rules into any project.
# Usage:
#   bash bootstrap.sh /path/to/project
#   bash bootstrap.sh .            # current dir
#   bash bootstrap.sh . --force    # overwrite existing rule files
set -u

REPO="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-.}"
FORCE="${2:-}"

[ -d "$REPO/SYSTEM_PROMPT.md" ] 2>/dev/null || true
if [ ! -f "$REPO/SYSTEM_PROMPT.md" ]; then echo "ERROR: repo files nahi mile: $REPO"; exit 1; fi
mkdir -p "$TARGET" || { echo "ERROR: cannot create $TARGET"; exit 1; }

copy() { # src dst
  local s="$1" d="$2"
  if [ -f "$d" ] && [ "$FORCE" != "--force" ]; then
    echo "  skip (already exists): $d   [--force to overwrite]"
  else
    mkdir -p "$(dirname "$d")"
    cp "$s" "$d" && echo "  installed: $d"
  fi
}

echo "Installing execute-first rules into: $TARGET"
copy "$REPO/AGENTS.md"                          "$TARGET/AGENTS.md"
copy "$REPO/CLAUDE.md"                          "$TARGET/CLAUDE.md"
copy "$REPO/.cursorrules"                       "$TARGET/.cursorrules"
copy "$REPO/.cursor/rules/execute-first.mdc"    "$TARGET/.cursor/rules/execute-first.mdc"
copy "$REPO/.github/copilot-instructions.md"    "$TARGET/.github/copilot-instructions.md"
copy "$REPO/SYSTEM_PROMPT.md"                   "$TARGET/EXECUTE_FIRST.md"
copy "$REPO/COLD_START.md"                      "$TARGET/COLD_START.md"
copy "$REPO/START_HERE.md"                      "$TARGET/START_HERE.md"

echo
echo "Done. Ab is project me naya agent session kholo — rules apne aap load honge."
echo "Agar chat-only session hai to START_HERE.md wali line paste karo."
