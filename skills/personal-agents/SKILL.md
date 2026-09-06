---
name: personal-agents
description: 'Set up, run, and tune the recurring personal agents - daily brief, weekly review, inbox triage, session-log rollup - that run on a schedule and do the standing work so the human only handles judgement. Use when the user says "set up my daily brief", "personal agents", "morning routine", "weekly review agent", "automate my inbox", "run this every day", or wants a new recurring agent. Differentiator: standing life/ops automation via scheduled routines - not a one-off task and not project code.'
---

# personal-agents

> Ported from Flo Crivello / Lindy and the "routines" idea. The principle from
> the podcasts: **work ON the machine, not IN it** (Ray Dalio). Your job is to
> set up the agent machine and then get out of it, dropping back in only for the
> decisions that need you. Also: humans are bad at memory and consistency;
> agents are great at both - hand those tasks over.

## What runs (the standard set)

| Routine | Cadence | Does |
|---|---|---|
| `daily-brief` | every morning | calendar today + overdue tasks + `context/log.md` deltas across active projects + "what's likely on your mind" -> one short message |
| `weekly-review` | Friday PM | what shipped this week, what's stuck & why, decisions made (ADRs added), top 3 for next week -> a review note in the vault |
| `inbox-triage` | 2-3x/day | label incoming mail, draft replies to the ones that need one (draft only, never send), flag anything urgent |
| `session-log-rollup` | nightly | summarise the day's Claude Code sessions (via `analyze-sessions`) into each project's `context/log.md` so tomorrow's SessionStart hook is current |

Routine specs are in `07-personal-agents/routines/*.md`. Each is a self-contained
prompt for a scheduled agent.

## Setup

These run as **scheduled cloud agents** (the `/schedule` skill) or, for anything
that needs local files, as a `/loop` on this machine.

1. Pick which routines you want. Start with `daily-brief` only; add others once
   it's proven useful.
2. For each: `/schedule` and paste the routine spec as the agent prompt, set the
   cron time (the spec suggests one).
3. `inbox-triage` needs the Gmail connector (this user has `mcp__claude_ai_Gmail`).
   `weekly-review` writes to the Obsidian vault (second-brain plugin).
   `session-log-rollup` and anything touching `context/` must run locally -
   use `/loop` with a long interval or a local scheduled task, not a cloud agent.
4. Verify each routine once by running it manually before trusting the schedule.

## Tuning

- If a routine's output is noise, make its spec more specific about what to
  include and what to skip. Vague routine = vague output.
- `daily-brief` should be readable in 20 seconds. If it's longer, it's doing too
  much - split it.
- Never let a routine take an irreversible action (send email, merge, deploy,
  delete). Draft / propose / flag only. The human does the last click.
- Review the routine set monthly. Kill the ones you skim past.

## Adding a new routine

1. Write a spec like the ones in `routines/` - name, cadence, exact steps,
   output format, hard "never do X" rules.
2. Test it manually.
3. `/schedule` it (cloud) or `/loop` it (local).
4. Add it to the table above.

## Anti-patterns
- A routine that needs you to read it carefully every time - defeats the purpose.
- Routines that act without a human in the loop on anything that matters.
- Ten routines you set up once and never read.
- Cloud-scheduling something that needs local file access (it'll fail silently).
