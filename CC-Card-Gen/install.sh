#!/usr/bin/env bash
# Install the anki-deck skill as a personal Claude Code skill, plus its Python dependencies.
#
#   ./install.sh               # copy skill to ~/.claude/skills/anki-deck and install deps
#   ./install.sh --skip-deps   # copy the skill only
#
# Set CLAUDE_SKILLS_DIR to install somewhere other than ~/.claude/skills.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/anki-deck"

mkdir -p "$TARGET"
cp -R "$HERE/skills/anki-deck/." "$TARGET/"
echo "Installed skill -> $TARGET"

if [ "${1:-}" = "--skip-deps" ]; then
  exit 0
fi

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "Python 3.9+ was not found. Install it, then rerun this script (or run the pip commands in README.md)." >&2
  exit 1
fi
echo "Installing Python dependencies with $PY ..."
"$PY" -m pip install --upgrade pymupdf chevron frozendict cached-property
# genanki's pyyaml dependency often fails to build on new Python versions and isn't needed
# here (build_deck.py stubs it), so install genanki without dependencies.
"$PY" -m pip install --upgrade --no-deps genanki
echo "Done. In Claude Code, run: /anki-deck <path-to-lecture-folder> depth=exam"
