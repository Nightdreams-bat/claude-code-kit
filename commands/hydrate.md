---
description: Turn a source (transcript, brain-dump, article, video, screenshots) into structured knowledge in context/ and the vault. Usage: /hydrate <path, URL, or pasted text>
---

The argument is: `$ARGUMENTS`

Load the `hydrate` skill and run its workflow on `$ARGUMENTS`.

1. Ingest (youtube-transcript for YT URLs, WebFetch for articles, Read for
   PDFs/images/files, `hydrate.py chunk` for anything over ~6000 words).
2. Extract the four buckets (entities / durable facts / decisions / open
   questions) + action items, each dated. `hydrate.py scan <file>` for a rough
   first pass.
3. Reconcile against `context/master.md` and `context/decisions/` - FLAG every
   contradiction to the user, never overwrite silently.
4. Write: update `master.md`, `ctx new decision` for real decisions, `ctx log`
   it. Personal/cross-project material -> Obsidian via the second-brain plugin.
5. Report the short summary (counts + contradictions + ADR numbers).

If there is no `context/` dir and this is project work, offer `ctx init` first.
If it is personal, route straight to the Obsidian vault.
