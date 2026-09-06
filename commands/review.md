---
description: Run the no-mistakes review gate on the current working-tree changes before merging. Usage: /review [intent note]
---

The argument (optional intent hint) is: `$ARGUMENTS`

Load the `no-mistakes` skill and run its pipeline on the current uncommitted
changes:

1. `python ~/.claude/skills/no-mistakes/scripts/nm.py -y` to stage onto an `nm/` branch.
2. Infer the ORIGINAL INTENT (use `$ARGUMENTS` if given, else the conversation +
   commits + `context/specs/`). State it in one sentence.
3. Dispatch the `reviewer-adversarial` agent (model different from + >= the
   author's) with the diff, the intent, and `context/` conventions.
4. Categorise findings: auto-fix trivial, escalate judgement calls, flag
   product-behaviour changes for the user.
5. Proof: run tests + linters + `ctx validate`; screenshot anything visual.
6. Fix doc/context drift; `ctx log` it.
7. Prepare the PR (rebase if behind origin). Hand back the short categorised
   summary - not the raw reviewer dump.

One pass only. Never recursive. If the change is genuinely trivial/throwaway, say
so and skip the gate.
