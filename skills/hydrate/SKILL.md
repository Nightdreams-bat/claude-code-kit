---
name: hydrate
description: 'Turn any raw source - a meeting transcript, voice-note brain-dump, article, YouTube video, chat log, PDF, screenshot batch, research brief - into structured knowledge in the project context repo, updating master.md, decisions, conventions, specs, the log, and the Obsidian vault, and reconciling contradictions with what is already there. Use when the user pastes or points at a source and wants it captured, says "hydrate this", "ingest this", "add this to the context", "process this transcript", "what should we keep from this", or after any meeting or research session. Differentiator: the vault rewrites itself around the new source - not a plain note-taker and not a summariser.'
---

# hydrate

> Ported from Flo Crivello / Lindy ("automatic hydration", the self-building
> company wiki) and Karpathy's LLM-wiki pattern. The premise from the podcast:
> **humans are terrible at memory** - eyewitness testimony is the least reliable
> evidence there is, childhood memories are half-invented. Stop trying to
> remember what was decided in the last meeting. Feed it to the agent and let it
> maintain the knowledge base. The agent that has "been in every meeting" becomes
> irreplaceable.

## What it maintains

Primary target: the project's `context/` repo (Phase 2).
```
context/master.md        <- the self-hydrating knowledge base (Entities / Durable facts / Open questions / Recently changed)
context/decisions/       <- if the source contains a decision
context/conventions/     <- if the source establishes a rule
context/specs/           <- if the source defines new work
context/log.md           <- a one-line "hydrated <source> on <date>" entry
```
Secondary target (this user has obsidian-second-brain installed): route
person/project/idea material into the Obsidian vault via that plugin's
`/obsidian-save`, `/obsidian-person`, `/obsidian-project`, or `obsidian_capture`.
Personal (non-project) sources go to the vault, not `context/`.

## Workflow

### 1. Ingest the source
| Source type | How to get the text |
|---|---|
| Pasted text / brain-dump | use as-is |
| YouTube URL | `youtube-transcript` skill (or `/youtube`) |
| PDF | Read tool with `pages` |
| Article URL | WebFetch |
| Screenshot batch | Read each image |
| Meeting transcript file | Read it; if huge, `scripts/hydrate.py chunk <file>` |
| Voice note (already transcribed by SuperWhisper etc.) | use as-is |

For anything over ~6000 words: `python scripts/hydrate.py chunk <file>` splits it
into overlapping chunks; process each, then merge findings before writing.

### 2. Extract - four buckets
Read the whole source. Pull out, with a date on each item:
- **Entities**: people, companies, services, accounts, systems mentioned. One line each.
- **Durable facts**: things now true and unlikely to change soon. (Not "we
  talked about X" - only "X is true".)
- **Decisions**: anything settled. Candidate ADRs.
- **Open questions**: unresolved, each with what/who would resolve it.
- **Action items**: concrete next steps -> `context/log.md` or a spec or the
  Obsidian board via `/obsidian-task`.

`python scripts/hydrate.py scan <file>` gives a rough first pass (lines that look
like decisions / questions / actions) - a starting point, not the answer.

### 3. Reconcile against what's already known
Before writing, read `context/master.md` and the relevant `decisions/`. For each
extracted item:
- **New** -> add it.
- **Confirms existing** -> update the date, don't duplicate.
- **Contradicts existing** -> this is the important case. Flag it explicitly to
  the user: "master.md says X (from <date>); this source says Y. Which is
  current?" Do NOT silently overwrite. Once resolved, update master.md and, if a
  decision changed, write a superseding ADR.

### 4. Write
- `master.md`: merge into the four sections. Keep it tight - it's a living index,
  not an archive. Move anything bulky into its own file and link it.
- Add a rolling entry under `master.md` "Recently changed": "<date> - learned
  <one line> from <source>".
- New decision -> `ctx new decision`, fill it, `status: accepted` (or `proposed`
  if the user still needs to confirm).
- New rule -> `ctx new convention`.
- `ctx log "hydrated <source name> - <one line of what changed>"`.
- Personal / cross-project material -> Obsidian via the second-brain plugin.

### 5. Report
```
HYDRATED: <source> (<N words / M chunks>)
  + entities: <count new>
  + facts: <count new>
  ! contradictions: <list - RESOLVED with user or FLAGGED>
  decisions written: ADR <nums>
  actions: <where they went>
master.md updated. ctx log written.
```

## Anti-patterns
- Dumping the raw summary into master.md. Extract, don't transcribe.
- Silently overwriting a contradicting fact. Always flag it.
- Letting master.md grow unbounded. It's an index; archive the bulk.
- Putting personal/life stuff in a project's `context/`. That goes to the vault.
- Re-hydrating the same source twice (check `log.md` first).
