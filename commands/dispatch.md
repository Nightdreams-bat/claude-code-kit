---
description: Act as the manager - route a task to the right model/worker and dispatch it as a background subagent. Usage: /dispatch <task description>
---

The argument is: `$ARGUMENTS`

You are now the **manager** (load the `manager` skill's rules).

1. If `$ARGUMENTS` is empty, ask what to dispatch and stop.
2. Route it: run `python ~/.claude/skills/manager/scripts/route.py "$ARGUMENTS"`
   (or reason it through `routing.md` yourself). State the chosen model, effort,
   and worker profile with a one-line reason.
3. Build the full worker briefing (GOAL / CONTEXT / MODEL / DELIVERABLE /
   CONSTRAINTS / PROOF - template in the `manager` skill). Pull the CONTEXT from
   `context/` and this conversation - the worker starts cold.
4. Spawn it with the `Agent` tool: `subagent_type` = the profile, `model` = the
   routed model (explicit). It runs in the background.
5. Report: `dispatched "<short>" -> {model} {profile} worker [running]`. Then keep
   going / hand back to the user. Do NOT block waiting for it.
6. When it reports back later: integrate, `ctx log` it, surface only decisions or
   blockers to the user.

If the task is actually a 5-minute job or needs no special model, say so and just
do it in this session instead of dispatching.
