---
description: Write a tight autonomous-loop contract (objective / constraints / validate / stop) to hand to /loop or an overnight agent. Usage: /goal <what you want done>
---

The argument is: `$ARGUMENTS`

Turn `$ARGUMENTS` into a **specification with a verifiable stop condition** — the thing that
makes an autonomous run safe. This produces the contract; the user launches it themselves
(`/loop` in autonomous mode, or a fresh agent, or a scheduled run).

## First, gate it

Only worth an autonomous loop if ALL THREE hold:
1. >30 min of mechanical work.
2. A **verifiable stop condition** — tests pass, coverage hits N, build green, eval ≥ X.
3. Repo is agent-ready — working build, real tests, `context/_map.md` present.

If any fails, say so and just do the task inline instead. Don't emit a contract.

## Inspect before writing

Read the relevant code, `context/_map.md`, `context/conventions/`, and any open ADRs. The
hand-written version of a goal always under-specifies — surface the hidden assumptions,
constraints, and edge cases first.

## Emit the contract

Plain markdown, one line per item, real newlines. **Do not prefix with `/loop` or `/goal`** —
the user adds that. Template:

```
**Objective:** <one sentence, one concrete outcome>
**Read first:** <exact files / spec / ADR>
**Constraints:** <what must NOT change — public API, files, libs, conventions>
**Validate:** `<exact shell command>` after every change
**Document:** write concise targeted docs for each change — new .md or focused updates
**Checkpoints:** work in checkpoints; log progress briefly each one
**Stop when:** <verifiable condition>, OR when a change needs a human/product decision
**Do not:** delete, skip, weaken, or narrow tests to make the goal pass. Do not refactor
unrelated code. Do not add dependencies. Do not create new ADRs.
```

## Rules

- One objective, one stop condition. Not a backlog.
- The anti-reward-hacking line and the no-new-ADRs line are mandatory — keep them verbatim.
- Literal strings for paths, commands, issue numbers.
- If the objective needs more than ~4000 chars, put the detail in `GOAL_BRIEF.md` and make the
  objective point at it.
- Tell the user: review the full diff before merging — long autonomy means more code to check,
  not less. And on the first run, pick a 30-min scoped task to learn how it actually stops.
