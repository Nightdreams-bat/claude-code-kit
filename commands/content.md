---
description: Run the content machine - human origin to finished post/thread/script in your voice, not slop. Usage: /content [topic or "sweep"]
---

The argument is: `$ARGUMENTS`

Load the `content-machine` skill and run its pipeline.

1. IDEA: if `$ARGUMENTS` names a topic, use it. If it's "sweep" or empty, do the
   internal + external idea sweep, present ~10 angles, let the user pick. Save
   the rest to a backlog file.
2. INTERVIEW: pick one persona from `personas/interview-panel.md`; interview the
   user ONE question at a time (~15-20 min); capture answers verbatim.
3. Optional light research pass if the take needs grounding.
4. DRAFT in the user's voice (`templates/voice.md` + the relevant section of
   `templates/formats.md`); check `templates/content-lessons.md` first; Sonnet.
5. EDITOR COUNCIL: score /10 with specific notes; ONE revision if below 9;
   re-score once.
6. Deliver the final in a code block. Offer repurposing.
7. Ask for feedback; append it to `content-lessons.md`.

Never generate the take - elicit it. Never paraphrase the user's words. One
revision loop. Never publish without explicit approval of the final text.
