---
description: Toggle or check bash-guard (dangerous-command blocking). Usage: /guard on|off|status
---

The argument is: `$ARGUMENTS`

bash-guard is a PreToolUse hook at `~/.claude/hooks/bash-guard.py`. It is ON when
the file `~/.claude/hooks/.bash-guard-off` does NOT exist, and OFF when it does.

- If the argument is `off`: create `~/.claude/hooks/.bash-guard-off` (write the word "off" into it). Confirm it is now OFF.
- If the argument is `on`: delete `~/.claude/hooks/.bash-guard-off` if present. Confirm it is now ON.
- If the argument is `status` or empty: check whether the file exists and report ON or OFF, plus a one-line reminder that the change takes effect on the next Bash call (no restart needed).

Do only this. Then stop.
