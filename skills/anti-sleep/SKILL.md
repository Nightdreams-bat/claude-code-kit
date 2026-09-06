---
name: anti-sleep
description: Keep Windows awake (no sleep, no screen blank) while long unattended agent runs, /loop jobs, or overnight builds are in progress. Use when the user says "anti-sleep", "keep the machine awake", "don't let it sleep", "caffeinate", or is about to leave agents running while away.
---

# anti-sleep

Windows equivalent of macOS `caffeinate`. Holds a system + display wake lock via
`SetThreadExecutionState`, re-asserted every 60s, for a bounded duration (default
3h). The OS clears the lock automatically when the process exits, so a kill or
crash can never leave the machine permanently awake.

Script: `scripts/keep-awake.ps1` — always run it, never regenerate the logic inline.

## Steps

1. **Start a lock.** Ask for a duration only if the user didn't give one; default 3h.
   Run in the background (it blocks for the whole duration):
   ```
   pwsh -File "~/.claude/skills/anti-sleep/scripts/keep-awake.ps1" -Hours 3
   ```
   Starting again replaces any existing lock. Report the end time back to the user.

2. **Check status** — is a lock held, how long is left:
   ```
   pwsh -File "~/.claude/skills/anti-sleep/scripts/keep-awake.ps1" -Action status
   ```

3. **Release early:**
   ```
   pwsh -File "~/.claude/skills/anti-sleep/scripts/keep-awake.ps1" -Action stop
   ```

## Notes

- `-Hours` accepts fractions (`0.5` = 30 min); max 24.
- State file: `%TEMP%\claude-anti-sleep.pid` (pid + end time). Stale files are
  self-healed on the next call.
- This does **not** change the user's power plan — it's a temporary runtime
  override that leaves system settings untouched.
- If the user instead wants to *find and open* the Windows sleep settings, just
  open `ms-settings:powersleep` — no script needed.
- Pair with `/loop` or `/goal`: start the lock, kick off the loop, tell the user
  when the lock expires so they know the safe window.
