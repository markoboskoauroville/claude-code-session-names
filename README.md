# Session names for Claude Code

Every Claude Code session names itself by **where it runs, the day's number, and the date**:

    MAC_SES1_05-NOV      the first session on the Mac on 5 November
    MAC_SES2_05-NOV      the next one, or a second tab, or after /clear
    VM_SES1_05-NOV       the first on the virtual machine
    PIXEL7_SES1_06-NOV   a new day starts at 1 again

So the session list (and Remote Control on your phone) reads at a glance.

- **One counter per place and day**, locked, so tabs opened at the same moment never get the same number.
- **`/clear`** takes the next number; a **resumed, continued or compacted** session keeps its name.
- It works however the session was started (a terminal tab, a launcher, Termux on a phone), because it is a
  `SessionStart` hook that answers `sessionTitle`.

## Install

As a plugin (inside Claude Code):

    /plugin marketplace add markoboskoauroville/claude-code-session-names
    /plugin install session-names@session-names

Or as a plain hook in `~/.claude/settings.json` (macOS, Linux, Termux; needs `python3`):

    curl -fsSL https://raw.githubusercontent.com/markoboskoauroville/claude-code-session-names/main/install.sh | bash -s -- MAC

The word at the end is the place (`MAC`, `VM`, `PIXEL7`, ...). Without it: `$CLAUDE_SESSION_PLACE`, then
`~/.claude/session-names/place`, then `MAC` on macOS, `PHONE` in Termux, else the host name.

## Files

- `session_name.py`: the hook (standard library only). Counters live in `~/.claude/session-names/`.
- `hooks/hooks.json`, `.claude-plugin/`: the plugin.
- `install.sh`: the plain-hook install.

MIT licence. Made by Mantra Productions with Claude Code.
