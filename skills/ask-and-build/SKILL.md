---
name: ask-and-build
description: 'Before building any non-trivial feature or change, surface the real architectural and product decisions hidden in the request, put them to the user one at a time with options and a recommendation, record each answer as an ADR, then produce a build brief for the implementer. Use when the user proposes a build, says "ask and build", "ask-then-build", "decide first", "what should I decide before building this", or when a request has consequential choices baked in. Differentiator: forward-looking decision drilling that writes ADRs and hands off a brief - not a code-writing skill and not a retrospective review.'
---

# ask-and-build

> Ported from David Ondrej's `ask-then-build` / `before-building` / `next-decision`
> family. The premise from the podcasts: **AI models are great at implementation
> and following a plan. They have no taste and no judgement. You, the human, must
> stay in charge of the decisions.** Frontloading a little decision work buys a
> lot less tech debt and a more scalable codebase.

## When to fire

- The user says "build X", "add X", "make this do Y", "let's ship Z" and X/Y/Z is
  more than a few lines.
- A plan has unresolved choices.
- You're about to make a call the user might regret (storage, data model, sync
  strategy, auth, file layout, public API shape, dependency, platform behaviour,
  cross-platform differences).

Do NOT fire for genuinely trivial changes (copy tweak, one obvious bug fix, a
rename). For those, just do it. Over-asking is its own anti-pattern.

## Phase 1 - Surface the decisions (fast, from the gut first)

1. **Instant pass** (no tools, no file reading): from what the user just said,
   name the **1-3 truly consequential choices** hidden in the idea. Fewer is
   better. Classics: one-off vs. reused later; few lines vs. proper module; the
   biggest thing this could break; same behaviour on every platform vs. not;
   local-only vs. needs a server.
2. **Grounded pass** (now read): `context/_map.md`, relevant `context/decisions/`
   (don't contradict an accepted ADR), `context/conventions/`, and the code the
   change touches. Refine the list - add decisions the code reveals, drop ones
   already settled by an ADR.
3. You should end with **3-7 open decisions**. If more, the scope is too big -
   say so and suggest splitting into an epic.

## Phase 2 - Put them to the user, ONE at a time

For each decision, in this exact layout (blank line between every block -
renderers collapse single newlines):

```
**<Decision title, as a question>?**

<one line of context if needed>

A. <option>

B. <option>

C. <option>

D. <option>   (only if there's a real 4th option)

My pick: <A>. <one-line reason>
```

Then **stop and wait**. Never bundle questions. Never number them "1 of N" unless
you truly know N.

When the user answers:
- Record it immediately as an ADR: `ctx new decision "<title>"` then fill
  Context / Options considered / Decision / Consequences. Set `status: accepted`.
  If the user gave exact wording, use their words verbatim in the Decision
  section (keep their typos) - don't rewrite it.
- If the answer overrides an accepted ADR, write a NEW ADR that supersedes it and
  mark the old one `status: superseded` with a link.
- Move to the next most important open decision.

## Phase 3 - Build brief

After the last answer, produce ONE concise brief for the implementer (or for
`/dispatch`). In this order:

1. **Read first**: `context/_map.md`, the ADRs just written (by number),
   `context/conventions/con-index.md`.
2. **What to build**: numbered, concrete, file-level where useful. Each step
   independently verifiable.
3. **How to validate**: the exact command / manual check with real data, and a
   screenshot if it's visual.
4. **Rules**: follow the ADRs, don't over-add tests, don't touch out-of-scope
   files, don't commit, report back with files changed + proof.

Keep the brief to a single tight paragraph or a short numbered list. If it needs
two paragraphs, the scope is too big - say so.

## Phase 4 - Hand off

- Route the brief through `routing.md` (Phase 3) and either build it in this
  session or `/dispatch` it to a worker.
- After the build, run `/review` (Phase 4 gate) before merge.

## Related manual skills to reach for

- **stop-overthinking**: if you (or the user) are looping on a decision - "if
  there's a critical issue name it, else say we're good, give next steps, be
  concise, think like a practical entrepreneur."
- **decisions**: after building - "which choices did you make that you're not
  confident about, and are there better alternatives?" Only list the genuinely
  uncertain ones.

## Anti-patterns

- Asking about trivia (indent size, variable names) - that's a convention, not a decision.
- Offering fake choices where one option is obviously right - just state it and move on.
- Writing the build brief before all answers are in.
- Bundling 5 questions into one message.
- Deciding the architectural questions yourself because it's faster.
- Not recording the answer as an ADR (then the next session re-litigates it).
