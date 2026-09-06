---
description: Surface the real decisions in a build request, drill them one at a time, record ADRs, then produce a build brief. Usage: /ask-build <what you want to build>
---

The argument is: `$ARGUMENTS`

Load the `ask-and-build` skill and run it on `$ARGUMENTS`.

1. Instant gut pass: name the 1-3 consequential choices hidden in the request.
2. Grounded pass: read `context/_map.md`, `context/decisions/`, `context/conventions/`,
   and the affected code. Refine to 3-7 open decisions.
3. Put them to the user ONE at a time (question, options A-D, your pick + reason,
   then STOP). Record each answer as an ADR via `ctx new decision`.
4. After the last answer: produce the one-paragraph build brief (read-first /
   steps / validate / rules).
5. Offer to build it here or `/dispatch` it.

If `$ARGUMENTS` is trivial, say so and just do it - don't run the ceremony.
