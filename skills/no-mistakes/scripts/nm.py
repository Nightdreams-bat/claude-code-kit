#!/usr/bin/env python3
"""nm - "no mistakes" gate: stage the working tree into a review branch + commit,
then print everything the review pipeline needs.

Ported from Kun's `no mistakes` (L8 Principal podcast). This script is only the
git plumbing + evidence gathering; the actual adversarial review is driven by the
`no-mistakes` skill.

    python nm.py            interactive: shows the plan, asks before committing
    python nm.py -y         auto: create branch + commit, no prompt
    python nm.py -m "msg"   set the commit message (else derived from changes)

Output: the new branch name, the diff stat, changed files, current-branch base,
whether a rebase onto origin is needed, and a review checklist.
"""
import subprocess
import sys
from datetime import datetime


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return r.stdout.strip()


def main():
    argv = sys.argv[1:]
    auto = "-y" in argv
    msg = None
    if "-m" in argv:
        msg = argv[argv.index("-m") + 1]

    # sanity
    inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0:
        sys.exit("not a git repository")

    base = git("rev-parse", "--abbrev-ref", "HEAD")
    status = git("status", "--porcelain")
    if not status:
        print("working tree is clean - nothing to gate.")
        return 0

    tracked = [f for f in git("diff", "--name-only", "HEAD").splitlines() if f]
    untracked = [f for f in git("ls-files", "--others", "--exclude-standard").splitlines() if f]
    changed = sorted(set(tracked) | set(untracked))
    full_stat = git("diff", "--stat", "HEAD").strip()

    if not msg:
        msg = f"nm: {len(changed)} file(s) - " + ", ".join(changed[:3]) + ("..." if len(changed) > 3 else "")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch = f"nm/{ts}"

    print(f"base branch     : {base}")
    print(f"review branch   : {branch}")
    print(f"commit message  : {msg}")
    print(f"changed files   : {len(changed)}")
    for c in changed:
        print(f"  {c}")
    print(f"\ndiff --stat:\n{full_stat or '(binary or rename only)'}")

    # origin freshness
    has_origin = subprocess.run(["git", "remote", "get-url", "origin"],
                                capture_output=True, text=True).returncode == 0
    if has_origin:
        subprocess.run(["git", "fetch", "-q", "origin"], capture_output=True)
        try:
            behind = git("rev-list", "--count", f"HEAD..origin/{base}", check=False)
            if behind and behind != "0":
                print(f"\nNOTE: local {base} is {behind} commit(s) behind origin/{base} - "
                      f"rebase the review branch onto origin/{base} before merging.")
        except Exception:
            pass

    if not auto:
        try:
            ans = input("\ncreate branch + commit? [y/N] ").strip().lower()
        except EOFError:
            ans = "n"
        if ans != "y":
            print("aborted - no changes made.")
            return 1

    git("checkout", "-b", branch)
    git("add", "-A")
    git("commit", "-q", "-m", msg)
    print(f"\ncommitted on {branch}. base = {base}.")
    print("""
REVIEW CHECKLIST (drive with the `no-mistakes` skill):
  1. State the ORIGINAL INTENT in one sentence (from the conversation / the ask).
  2. Adversarial review by a DIFFERENT, stronger model than the author.
     - one pass, never recursive; do not invent bugs to look thorough.
  3. Categorise findings: auto-fix trivial | escalate judgement calls to the user
     | product-behaviour changes -> ask the user.
  4. Run `ctx validate` (context drift) and the project's tests/linters.
  5. PROOF: paste real test output or attach a screenshot. "Should work" != proof.
  6. Docs: README / comments / types still accurate after this change?
  7. Only then: open the PR / merge to """ + base + """.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
