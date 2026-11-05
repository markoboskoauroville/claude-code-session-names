#!/usr/bin/env bash
# Without the plugin system: copies session_name.py to ~/.claude/session-names/ and adds it as the first SessionStart
# hook in ~/.claude/settings.json (other settings kept).  bash install.sh [PLACE]
set -eu
D="$HOME/.claude/session-names"; mkdir -p "$D"
here=$(cd "$(dirname "$0")" && pwd)
if [ -f "$here/session_name.py" ]; then cp "$here/session_name.py" "$D/"
else curl -fsSL https://raw.githubusercontent.com/markoboskoauroville/claude-code-session-names/main/session_name.py -o "$D/session_name.py"; fi
[ -n "${1:-}" ] && echo "$1" > "$D/place"
python3 - "$HOME/.claude/settings.json" <<'PY'
import json, os, sys
p = sys.argv[1]
try: s = json.load(open(p))
except Exception: s = {}
cmd = "python3 ~/.claude/session-names/session_name.py 2>/dev/null || true"
hooks = s.setdefault("hooks", {}).setdefault("SessionStart", [])
if not hooks: hooks.append({"hooks": []})
for g in hooks: g["hooks"] = [h for h in g.get("hooks", []) if "session_name.py" not in h.get("command", "")]
hooks[0]["hooks"].insert(0, {"type": "command", "command": cmd, "timeout": 10})
os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(s, open(p + ".new", "w"), indent=2); os.replace(p + ".new", p)
PY
echo "Installed. The next new Claude Code session names itself, e.g. $(echo '{"source":"x"}' >/dev/null; echo "${1:-PLACE}")_SES1_$(date +%d)-$(date +%b | tr a-z A-Z)."
