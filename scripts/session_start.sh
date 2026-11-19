#!/usr/bin/env bash
# Claude Code SessionStart hook (.claude/settings.json): in a cloud session, prepare the
# environment before the agent starts, so no session spends turns installing. Local
# sessions are left alone: the owner's machine runs `make setup` when it needs to.
set -uo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
log="${TMPDIR:-/tmp}/make-setup.log"
if make -C "${CLAUDE_PROJECT_DIR:-.}" setup >"$log" 2>&1; then
  echo "Environment ready: make setup succeeded."
else
  echo "make setup failed; see $log before running make check."
fi
exit 0
