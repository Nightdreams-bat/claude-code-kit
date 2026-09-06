---
name: signal-from-expert
description: >-
  Surface the few passages from a world-class expert's body of work that hit the user's exact
  current situation — with verbatim quotes and source pointers — plus at least one gap where the
  expert shows the user is wrong or missing something. Use when the user says "signal from
  expert", "what would <person> say about this", "pull <expert> on <topic>", or wants an
  outside authority pressure-tested against their own raw thinking. Invoke with /signal.
  Differentiator vs /research: not a neutral memo — a targeted match between one expert's real
  words and the user's real notes, ending in a challenge.
---

# Signal from Expert

Read the user's raw thinking in full, find what a specific expert actually wrote that speaks to
it, and report only the passages that land — then name where the expert says the user is wrong.

## What to get from the user (ask once, only for what's missing)

1. **Corpus** — the user's own raw thinking to analyse. A file, a folder, a date range of daily
   notes, or "this conversation". Example: `<vault>/Daily/` last 14 days, or a pasted brain-dump.
2. **Expert + topic** — who, and on what. Example: "Paul Graham on what to build",
   "Rich Hickey on simplicity", "Charlie Munger on this pricing decision".
3. **URLs (optional)** — specific essays/talks/threads the user wants included for certain.

## Procedure

**1 — Read the corpus completely.** No skimming. Also check the Obsidian vault
(`$OBSIDIAN_VAULT_PATH`) for related notes via `obsidian_search` — the user's own past
conclusions are part of the corpus. Write a 3–5 line statement of the user's actual situation,
position, and open questions. Show it to the user before going further only if the corpus was
ambiguous.

**2 — Find 5–8 real sources from the expert.** Use `WebSearch` for essays, talks, interviews,
long-form threads. Prefer primary writing over summaries of it. Add any URLs the user gave.
`WebFetch` each one and **read it in full**. If a source turns out irrelevant, drop it and find
another — aim for 5–8 genuinely on-point pieces, not 5–8 links.

**3 — Match.** Pull only the passages that hit the user's exact situation. For each:
  - the **verbatim quote** (short — the load-bearing sentence or two, not a paragraph)
  - the source (title + URL, and the section if long)
  - one line: *how* it applies to the user's situation, pointing at the corpus
    (`daily/2026-09-01.md`: "…their line about X").

A passage that's merely on-topic doesn't qualify. It has to change how the user should act.

**4 — The gap (required).** Name at least one place where the expert's work shows the user is
**wrong, missing something, or asking the wrong question**. This is the most valuable part —
do not soften it or skip it because the match section already looks useful.

**5 — Read-out.** 3–5 sentences on what the passages mean *together* for the user's next move.

## Output shape

```markdown
**Situation** — 2–3 sentences, in the user's own framing.

**Signal** (3–6 items max)
- "<verbatim quote>" — <Source title>, <url>
  → <how it applies, with a corpus pointer>

**Where you're off**
- <the gap. Direct. Quote the expert. Say what the user should reconsider.>

**Together** — 3–5 sentences. The synthesised move.
```

## Rules

- Quotes must be verbatim and real. If you can't fetch a real source, say so — never
  paraphrase-then-quote or reconstruct a passage from memory.
- Scrape wide, report narrow. A long list of quotes is a failure. 3–6 that matter.
- No "I searched", "I found", "I read 8 essays" narration. Just the signal.
- If the expert genuinely has nothing precise to say about the situation, say that plainly
  rather than stretching loose passages to fit.
- Save the read-out to the vault (`obsidian_capture` or a note under `Learning/` or the
  relevant project) so the challenge compounds.
