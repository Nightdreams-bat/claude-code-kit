---
name: setup-help
description: Guide the user through a manual multi-step setup they must do themselves — deploying a backend, changing domain DNS, configuring a VPS, a SQL migration, filing taxes, any procedure where the agent should NOT act for them. Keeps the current step in focus while always showing the remaining steps so nothing is lost when the user asks follow-ups. Use when the user says "setup help", "walk me through", "help me set up X", "guide me through X step by step".
---

# setup-help

The user is doing the work; you are the guide. This skill exists because agents,
when asked deep follow-up questions about one step, lose track of the steps still
ahead. This format prevents that.

## Rules

- **Never do the step for the user.** No editing their cloud console, no running
  their deploy, no touching credentials. You explain; they act. (You may prep
  local artifacts they'll need — a `requirements.txt`, a config snippet — and put
  text on their clipboard with `Set-Clipboard` when that helps.)
- **One step at a time.** Present the current step in full, then stop and wait.
- **Every reply ends with the two lists** (see format), even a reply that only
  answers a clarifying question. This is the whole point — do not drop it.
- Assume the user may be a complete beginner. Define jargon the first time it
  appears. Short sentences.
- If a step fails, help debug that step before advancing. Don't renumber — add
  sub-steps (3a, 3b) if needed.

## First response

1. Restate the goal in one line.
2. Ask any blocking questions (which host? which OS? do they have an account?).
3. Draft the full step list — as few steps as possible, each a single concrete
   action with a visible success signal ("you'll see a green 'Live' badge").
4. Present **step 1** and the two lists.

## Every response — required format

```
## Current step: <n>. <name>

<what to do, why, exactly what to click/type, what success looks like,
common failure and the fix>

---
**Done so far:** 1. ✅ <name>  2. ✅ <name>
**Still to do:** <n+1>. <name>  ·  <n+2>. <name>  ·  <n+3>. <name>
```

When the user says a step is done, confirm the success signal, then advance.
When all steps are done: a short "you're live" recap + what to check periodically.

## Notes

- Keep the step list in this conversation; re-emit it every turn rather than
  relying on the user to scroll.
- Good default step shape for a deploy: account → connect repo → runtime/build
  config → env vars → first deploy → verify URL → custom domain (optional).
- If the user asks you to just do it, remind them once why this is
  theirs to run (credentials / billing / irreversible), then continue guiding.
