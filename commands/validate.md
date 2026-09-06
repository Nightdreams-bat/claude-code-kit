---
description: Process-lint this project's context/ repo - flag drift between what the docs say and what the work actually is. Usage: /validate
---

Run the context-as-code process linter.

1. Locate the `context/` (or `.context/`) folder by walking up from the current
   working directory. If there is none, tell the user and stop (offer `ctx init`).
2. Run: `python ~/.claude/skills/context-artifacts/scripts/ctx.py validate`
   (adjust path if `ctx` is aliased).
3. Report the output grouped as **DRIFT** (must fix) and **warnings** (should fix).
4. For each DRIFT item, propose the concrete fix (which file, what edit). Do NOT
   apply fixes unless the user says so - some "drift" is the user's call
   (e.g. a spec really is done and the checkbox is just stale).
5. If clean, say so in one line.

Do only this. Then stop.
