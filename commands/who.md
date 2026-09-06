---
description: Quick background check on a person — who they are, real track record, is the story legit. Usage: /who <name, handle, or URL>
---

The argument is: `$ARGUMENTS`

Vet a person. Seed = `$ARGUMENTS` (a name, handle, profile URL, or description). If missing or
ambiguous (two people share the name), ask once — don't guess a different person.

Research in parallel:
- `WebSearch` their name across X/Twitter, LinkedIn, GitHub, personal site, news.
- `WebFetch` the strongest 3–5 sources and read them.
- Check the Obsidian vault (`obsidian_search`) — the user may already have a note on them.

Scrape wide, report narrow. Keep only the ~3 facts that explain who this person actually is.

Output — hard cap ~120 words after the header:

```markdown
**Full name** — [@handle](url) · [LinkedIn](url) · [GitHub](url) · [Site](url)

**Who:** one sentence — where they are, what they do now.

**Track record:** ≤3 bullets. Only what explains them. Dates. Label "their claim" vs "verified".

**Verdict:** one line — the honest archetype (builder / operator / marketer / researcher /
investor / grifter / hobbyist…), whether the story holds, and why.
```

Rules: real track record beats bio. Self-reported numbers stay labelled as claims. Ignore
congrats, logo spam, follower-count flexing. Omit a missing profile link rather than faking it.
Offer to save the dossier as a vault person-note.
