---
description: Keep Windows awake while agents run unattended. Usage: /anti-sleep [hours|stop|status]
---

The argument is: `$ARGUMENTS`

Load the `anti-sleep` skill.

- No argument or a number → start a wake lock (default 3h) via
  `scripts/keep-awake.ps1 -Hours N`, run in the background. Report the end time.
- `stop` → release the lock (`-Action stop`).
- `status` → report whether a lock is held and how long is left (`-Action status`).
