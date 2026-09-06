---
name: content-machine
description: 'Turn a human origin - your own spoken or typed take on a topic - into a finished post, thread, or script that sounds like you and is not AI slop, via an idea sweep, a one-at-a-time interview, a draft in your voice, an editor-council score-and-revise loop, and optional repurposing. Use when the user says "content machine", "write this up", "turn this into a post/thread/newsletter", "help me post about X", or has a rough take they want published. Differentiator: the origin must be human words and the human owns the first and last mile - not an autonomous content generator.'
---

# content-machine

> Ported from Alex Lieberman's "content machine" (10X podcast). Two hard rules
> from the episode:
> 1. **The origin must be human.** "The number one difference between AI content
>    that's trash and AI content that's valuable is whether the origin is human."
>    The AI helps with everything *except* the part only you can do: your take.
> 2. **The human owns the first mile and the last mile.** Pick the idea; give
>    your real words; approve the final. Everything between can be assisted.

The way to guarantee it's not slop, regardless of how good models get: the AI
never invents the point of view. It structures, sequences, and checks *your*
words. New model tells get chased forever; a human origin doesn't.

## Layers

```
process layer   (in git, per D:\ content repo)   the pipeline steps + skills below
personal layer  (templates/, edited over time)   voice.md  +  content-lessons.md
```

- **voice.md**: how you sound. Built one of 3 ways: (a) a voice interview the
  machine runs, (b) paste past writing / texts / posts, or (c) start from a
  borrowed voice and let feedback morph it. For this user: start from past
  YouTube scripts + transcripts.
- **content-lessons.md**: after every run the user gives feedback; it's appended
  here; every future draft checks it first. This is the compounding part.

## Pipeline

### 1. Idea (human picks)
Optional sweep for candidates:
- internal: scan the last 7 days of the user's notes / vault / `context/log.md`
  for "spikes" - strong point of view, a story, emotional intensity, a
  lesson/framework, or unusual depth.
- external: `/youtube`, WebSearch across Reddit / HN / X on the topic - what's
  already said, what's missing.
Present ~10 candidate angles. **The user picks one.** The rest go to a backlog
file (don't lose them).

### 2. Interview (one question at a time)
Pick ONE interviewer persona from `personas/interview-panel.md` (Ferriss, Rogan,
Larry King, Stern, Barbaro, Walters - each questions differently). It interviews
the user about the chosen idea, ONE question at a time, pushing back on vague
answers, for ~15-20 min. The user answers by voice (SuperWhisper) or typing.
Capture every answer verbatim into a transcript markdown file - **these are the
raw material; do not paraphrase them away.**

### 3. Research pass (optional, light)
If the take needs grounding: the white-paper / primary source, current takes in
market, contrarian angles, open questions only the user can answer. Feed back to
the user if it changes their view.

### 4. Draft in the user's voice
- Choose format (LinkedIn post / X thread / long post / newsletter / script /
  podcast promo). Load the matching format section from `templates/formats.md`.
- Draft using the user's words from the transcript. **Refine flow and
  transitions; do not replace their phrasing with your own.** Model: Sonnet.
- Check `content-lessons.md` before writing - don't repeat a flagged mistake.

### 5. Editor council (score -> revise loop)
Run the draft past the personas in `personas/editor-council.md` (Housel, Urban,
Puri, Eisenberg, Perell, + a slop detector). Each scores /10 with specific notes.
- score < 9 -> one revision incorporating the notes -> re-score once.
- score >= 9 -> done.
- **One revision loop, not endless.** (Same rule as the review gate - recursive
  loops produce worse output and never ship.)

### 6. Repurpose (optional)
Turn the finished piece into N derivatives (thread from a post, etc.). Each
derivative goes through step 4-5 with its own format skill. Not a copy-paste.

### 7. Feedback -> lessons
Ask the user what the machine did well / badly this run. Append to
`content-lessons.md`. Polish a Fable or Opus pass only if the user wants it.

## Output to the user
```
IDEA: <the angle chosen>   (backlog: N other angles saved)
INTERVIEW: <persona>, <N> questions, transcript at <path>
DRAFT: <format>, <word count>
EDITOR COUNCIL: <score> (was <first score>)  - <one line on what changed>
FINAL: <the piece, in a code block for easy copy>
```

## Anti-patterns
- Generating the take instead of eliciting it. If the user didn't say it, it's not their content.
- Paraphrasing the user's words into "better" phrasing - kills the voice.
- Endless editor-council loops. One revision.
- Publishing/scheduling without the user's explicit approval of the final text.
- Losing the non-chosen ideas - always save them to a backlog.
