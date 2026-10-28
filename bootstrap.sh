#!/usr/bin/env bash
# bootstrap.sh — install the convention files into a target repository.
# Usage: bash bootstrap.sh /path/to/project [--force]
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-.}"
FORCE="${2:-}"

if [ ! -f "$ROOT/core/RULES.md" ]; then
  echo "ERROR: run this from the repository root (core/RULES.md missing)"; exit 1
fi
mkdir -p "$TARGET/.github" "$TARGET/.cursor/rules" "$TARGET/context" 2>/dev/null || {
  echo "ERROR: cannot write to $TARGET"; exit 1; }

copy() {
  local src="$1" dst="$2"
  if [ -f "$dst" ] && [ "$FORCE" != "--force" ]; then
    echo "  skip (exists): $dst"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst" && echo "  installed: $dst"
  fi
}

echo "Installing execution conventions into: $TARGET"
copy "$ROOT/AGENTS.md"                            "$TARGET/AGENTS.md"
copy "$ROOT/CLAUDE.md"                            "$TARGET/CLAUDE.md"
copy "$ROOT/GEMINI.md"                            "$TARGET/GEMINI.md"
copy "$ROOT/.cursorrules"                         "$TARGET/.cursorrules"
copy "$ROOT/.cursor/rules/execute-first.mdc"      "$TARGET/.cursor/rules/execute-first.mdc"
copy "$ROOT/.github/copilot-instructions.md"      "$TARGET/.github/copilot-instructions.md"
copy "$ROOT/SYSTEM_PROMPT.md"                     "$TARGET/EXECUTION_CONVENTIONS.md"
copy "$ROOT/START_HERE.md"                        "$TARGET/START_HERE.md"
copy "$ROOT/prompt_english.txt"                   "$TARGET/prompt_english.txt"
copy "$ROOT/prompt_hinglish.txt"                  "$TARGET/prompt_hinglish.txt"
copy "$ROOT/context/README.md"                    "$TARGET/context/README.md"

echo
echo "Done. For a chat-only session, paste the contents of START_HERE.md"
echo "as the first message, or run: python3 tools/inject.py --task \"...\""
