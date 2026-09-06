---
name: no-mistakes
description: Run the "no mistakes" review gate on a diff before it merges - infer the original intent, get one adversarial review pass from a DIFFERENT stronger model, categorise findings (auto-fix / escalate / product-decision), require real proof (test output or screenshot), check doc + context drift, then prepare the PR. Use before merging any non-trivial AI-written change, when the user says "review this", "is this safe to ship", "nm", "check before merge", or after a worker reports an implementation back. Skip only for throwaway/demo code or a one-line change you're certain about.
---

# no-mistakes

> Ported from Kun's `no mistakes` pipeline (L8 Principal podcast). The premise:
> "The bottleneck isn't coding anymore. It's reviewing thousands of lines of
> AI-written code to make sure you're not shipping slop." If you review every
> line yourself, your throughput is capped by how much diff you can read per day.
> So: a pipeline reviews it *for* you and hands you something you can judge fast.
>
> Kun's own stats: ~1000 changes across 59 repos, **63% got a fix from this gate**;
> the biggest hitters were the adversarial review step and stale-documentation.

## When to run it

- **Run it**: any change that's more than a few lines, anything touching logic,
  data, auth, money, or a public interface; production code with real users.
- **Skip it**: a weekend demo, a throwaway script, a one-line copy tweak you're
  certain about. Kun: "there's an inevitable cost of quality - decide per project
  how much you care." Don't gate a prototype; always gate production.
- **Never**: run this recursively. One pass. Models will invent imaginary bugs if
  you loop them ("find the 5 biggest issues" always returns 5, even on clean code).

## The pipeline

### 0. Stage the change
```
python ~/.claude/skills/no-mistakes/scripts/nm.py -y
```
Creates a `nm/<timestamp>` branch off the current branch, commits the working
tree, prints the diff stat + changed files + whether an origin rebase is needed.

### 1. Infer the original intent
State, in ONE sentence, what the user actually asked for. Sources, in order:
the current conversation, the commit messages, the relevant `context/specs/`
entry, the `context/log.md`. This intent is the spec the review judges against -
"did the change do what was asked, all of it, and nothing harmful beyond it".
Write it down explicitly; a wrong intent makes the whole review wrong.

### 2. Adversarial review - by a different, stronger model
Dispatch the `reviewer-adversarial` agent (or a `general-purpose` subagent on a
model **different from and >= the author's**: Sonnet-authored -> review with Opus;
Fable-authored -> review with Opus). Give it: the diff/branch, the INTENT from
step 1, and `context/_map.md` + `context/conventions/`.

Instruct it (this is in the agent def, restate if using general-purpose):
- Find real correctness bugs, intent mismatches, concrete edge cases, convention
  violations, stale docs, security issues. Rank by severity.
- **Do not invent problems to look thorough.** "No blocking issues" is a valid
  result. A good reviewer says "ship it"; a bad one always finds five things.
- Each finding: `file:line - defect - failure scenario (inputs -> wrong output) - fix`.
- Separate BLOCKING from non-blocking. Verify against the real code, not the diff.

### 3. Categorise the findings
| Finding type | Action |
|---|---|
| Trivial + obvious fix (null check, typo, off-by-one, missing await) | **auto-fix** on the branch, note it |
| Real bug, non-obvious fix, or multiple valid fixes | **escalate to the user** with options |
| Fixing it changes product behaviour / scope / UX | **ask the user** - this is their call, not yours |
| Non-blocking (style, nice-to-have) | list them, do not act, do not block |

### 4. Proof of done
Do NOT accept "should work". Produce actual evidence:
- run the project's tests + linters; paste the output.
- run `ctx validate` (Phase 2) - fix any DRIFT.
- for anything visual/behavioural: take a screenshot (use the browser tools or
  ask the user to run it) - light theme + dark theme if UI.
- for a CLI/API: run it, paste the real output.

### 5. Documentation + context drift
- README, inline comments, type signatures, `context/` files: still true after
  this change? Stale docs were the #2 finding class in Kun's data. Fix them on
  the branch.
- `ctx log "<what shipped>"`.

### 6. Prepare the merge
- If behind origin: rebase the `nm/` branch onto `origin/<base>`.
- Open a PR (`gh pr create`) with: the intent (step 1), the review summary, the
  proof (step 4), and the list of non-blocking items deferred.
- Babysit CI if there is any; report red -> fix -> green.
- Then hand back to the user for the merge click (or merge if they've said to).

## Output to the user (keep it short - this is the point)
```
INTENT: <one sentence>
REVIEW (<reviewer model>): <N blocking, M non-blocking>
  auto-fixed: <list>
  NEEDS YOUR CALL: <list with options>   <- the only part that needs their attention
  deferred (non-blocking): <list>
PROOF: <tests X/Y passed | screenshot attached | command output below>
DRIFT: <ctx validate result>
PR: <url or "ready to open">
```

## Anti-patterns
- Recursive review (Fable -> GPT -> Fable -> ...). You'll never ship, and the
  models hallucinate bugs. One pass.
- Reviewing with the same model that wrote the code.
- Gating a throwaway prototype (wastes limit).
- Accepting "should work" as proof.
- Dumping the raw reviewer output on the user instead of the categorised summary.
- Auto-fixing something that changes product behaviour.
