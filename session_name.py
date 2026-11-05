#!/usr/bin/env python3
"""Claude Code session names: every session names itself PLACE_SES<n>_DD-MON, e.g. MAC_SES1_05-NOV.

A SessionStart hook. A new session or /clear takes the next number of the day (one locked counter per place and
day, so tabs opened together never share a number); a resumed, compacted or forked session keeps its name.

PLACE, the first that is set:
  $CLAUDE_SESSION_PLACE (or $MANTRA_PLACE)
  ~/.claude/session-names/place (one word, e.g. VM or PIXEL7)
  ~/.claude/mantra/device-name (mac -> MAC, vm-machine -> VM, nothing-phone -> NOTHING, pixel7 -> PIXEL7)
  MAC on macOS, PHONE in Termux, else the host name in capitals.
"""
import datetime, fcntl, json, os, platform, socket, sys

try:
    src = json.load(sys.stdin).get("source", "startup")
except Exception:
    src = "startup"
if src not in ("startup", "clear"):
    sys.exit(0)                                   # resume, compact, fork: the name stays

D = os.path.expanduser("~/.claude/session-names")
PLACES = {"mac": "MAC", "vm-machine": "VM", "nothing-phone": "NOTHING", "pixel7": "PIXEL7"}


def first_line(p):
    try:
        return open(os.path.expanduser(p)).readline().strip()
    except OSError:
        return ""


place = os.environ.get("CLAUDE_SESSION_PLACE") or os.environ.get("MANTRA_PLACE") or first_line(D + "/place")
if not place:
    dev = first_line("~/.claude/mantra/device-name")
    place = PLACES.get(dev) or dev.upper().replace("-", "").replace(" ", "")
if not place:
    if platform.system() == "Darwin":
        place = "MAC"
    elif "com.termux" in os.environ.get("PREFIX", ""):
        place = "PHONE"
    else:
        place = socket.gethostname().split(".")[0].upper()

day = datetime.date.today()
stamp = f"{day.day:02d}-{day.strftime('%b').upper()}"
os.makedirs(D, exist_ok=True)
with open(os.path.join(D, f"{place}_{day.isoformat()}.count"), "a+") as f:
    fcntl.flock(f, fcntl.LOCK_EX)
    f.seek(0)
    n = int(f.read().strip() or 0) + 1
    f.seek(0); f.truncate(); f.write(str(n)); f.flush()

print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "sessionTitle": f"{place}_SES{n}_{stamp}"}}))
