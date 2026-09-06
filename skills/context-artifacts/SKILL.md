---
name: context-artifacts
description: Create and maintain a project's "context-as-code" repo - the context/ folder that lives SEPARATE from source code and holds the _map, ADRs (decisions), conventions, epics/specs, the work log, and the self-hydrating master file. Use whenever starting a new project, making an architectural decision, adding a coding rule, planning a feature, finishing a work session, or when the SessionStart context packet looks stale or wrong. Also use when the user says "write this down", "add an ADR", "log this", "update the context", "spec this out", or "why is it built this way".
---

# context-artifacts

> Ported from the 10X podcast (Alex Lieberman + Dan, "meta-harness / context as code")
> and Kun's "first mate is an agents.md + scripts" pattern. The core claim:
> **the markdown is worth more than the code.** Code can be regenerated from a
> good context repo; a codebase stripped of intent cannot be regenerated into a
> good context repo. Spend a higher share of your time engineering the markdown
> than writing code.

## Mental model

A project has two repos (or two top-level folders):

```
myproject/            <- source code. Regenerable. Agents rewrite it freely.
myproject-context/    (or myproject/context/)  <- intent. Hand-curated. The source of truth.
    _map.md           orientation - injected into EVERY session by the hook
    decisions/        ADRs: NNNN-title.md - WHY the architecture is this way
    conventions/      con-*.md + con-index.md - rules agents MUST follow when coding
    specs/            epic-NNNN-*.md and spec-NNNN-*.md - in-flight work, ticket by ticket
    log.md            running work log, newest first
    master.md         self-hydrating knowledge base (the /hydrate skill maintains this)
```

The `ctx` CLI (`scripts/ctx.py`, aliased `ctx`) is the agent-facing AND
human-facing interface to this folder. Prefer it over hand-creating files - it
numbers things, applies templates, and keeps the index in sync.

## The CLI

```
ctx init                              scaffold context/ in the current project
ctx map                               print the orientation packet (what the hook injects)
ctx status                            one-line counts (decisions/open, specs, conventions, log)
ctx new decision "Use SQLite not PG"  new ADR in decisions/ (status: proposed)
ctx new spec     "Offline sync"       new spec-NNNN in specs/ (status: draft)
ctx new epic     "v2 rewrite"         new epic-NNNN in specs/
ctx new convention "error-handling"   new con-error-handling.md in conventions/
ctx log "shipped the guard hook"      prepend a dated line to log.md
ctx validate                          PROCESS LINT - exit 1 on drift (see below)
```

## When to write which artifact

| Situation | Artifact | Command |
|---|---|---|
| Starting a project | `_map.md` (fill it in fully) | `ctx init` then edit |
| You are about to make a choice you might regret later (DB, framework, auth model, file layout, sync strategy, deploy target) | **ADR** | `ctx new decision "..."` |
| You corrected the agent on a coding style / pattern and don't want to repeat it | **convention** | `ctx new convention "..."` |
| A feature is more than ~1 session of work | **epic** + one or more **specs** | `ctx new epic` / `ctx new spec` |
| You finished a work session, shipped something, hit a blocker | **log entry** | `ctx log "..."` |
| You ingested a transcript / doc / research | feed to `/hydrate` (it updates `master.md`) | - |

Do NOT create an artifact for trivia. An ADR for "we use 2-space indent" is
noise; that's a one-liner in `con-style.md`. Reserve ADRs for decisions with
**consequences you're now locked into.**

## Rules for each artifact

### _map.md  (the highest-value file)
- Keep it under ~40 lines. It is injected into every session; every line costs tokens forever.
- Must always answer: what is this, where is the code, what must an agent never get wrong, what are we working on now.
- Update it the moment "current focus" changes. A stale `_map.md` actively misleads every future session.

### decisions/ (ADRs)
- Immutable once `status: accepted`. To change a decision, write a NEW ADR that supersedes it and set the old one's `status: superseded` with a link.
- Always fill **Consequences** - "what becomes harder / what we're now locked into / what would make us revisit". This is the part future-you needs.
- Status lifecycle: `proposed` -> `accepted` | `rejected`. Later maybe `superseded`.
- The SessionStart hook surfaces every non-final ADR as "OPEN DECISION - needs resolution". Don't leave decisions `proposed` forever; decide or reject.

### conventions/ (con-*.md)
- Imperative voice. "Always ...", "Never ...". One rule per file.
- Always include **Why** - so a future agent knows when the rule is allowed to bend.
- Register every `con-*.md` in `con-index.md` (one-line summary per row). `ctx validate` flags unregistered ones.
- These are the rails. When the agent writes code, it reads `con-index.md` first.

### specs/ (epic-* and spec-*)
- A spec has a **Tickets** checklist and a **Proof of done**. `ctx validate` derives status from the checkboxes and flags it if the authored `status:` disagrees ("drift").
- `status:` values: `draft` -> `in-progress` -> `in-review` -> `done` (or `blocked` / `cancelled`).
- Keep specs small. If a spec has >8 tickets, it's an epic - split it.
- "tests where they genuinely matter (do NOT over-test)" is in the template on purpose - see the over-testing convention.

### log.md
- Newest first. One line per entry: what happened, not a diary.
- End every real work session with a `ctx log`. The SessionStart hook injects the last ~20 lines, so this is how the next session knows what just happened.

### master.md
- Do not hand-write large sections. Feed sources through `/hydrate`; it reconciles and dedupes.
- Structure: Entities / Durable facts / Open questions / Recently changed.

## `ctx validate` - process linting

Run it before you consider a chunk of work "done", and wire it into the review
gate (Phase 4). It reports two levels:

- **DRIFT** (exit 1): authored state disagrees with reality. E.g. `spec status:done`
  but unchecked tickets; ADR with no `status:`; `con-index.md` references a file
  that doesn't exist; `_map.md` empty.
- **warn** (exit 0): smells. Stale log (>10 days), unregistered convention,
  placeholder text left in an ADR, missing Consequences section.

This is "linting for your SDLC", not for your code - it catches the class of bug
where the docs and the work have silently diverged.

## Standard workflow

1. **New project**: `ctx init`, then fully write `_map.md`. Add `con-*.md` for
   any non-obvious rule. This takes 20-30 min and is the highest-leverage time
   you'll spend.
2. **Before a feature**: `ctx new epic`, break into `ctx new spec`s. For each
   real decision inside, run `/ask-build` (Phase 5) which produces ADRs.
3. **During work**: the SessionStart hook has already briefed you. Read the full
   `context/` files for anything non-trivial. Keep specs' checkboxes current.
4. **End of session**: `ctx log "..."`, tick spec boxes, run `ctx validate`,
   fix drift, commit the context repo.
5. **After ingesting anything** (meeting, article, research): `/hydrate <source>`.

## Anti-patterns

- Treating `context/` as write-once. It rots. It must be maintained every session.
- Putting secrets or credentials in `context/`. Never. Reference their location only.
- Giant `_map.md`. Move detail into `decisions/` and `conventions/`; keep the map an index.
- ADRs with no Consequences, or left `proposed` for weeks.
- Skipping `ctx log` because "it was a small change" - small changes are exactly what future-you forgets.
