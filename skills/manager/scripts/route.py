#!/usr/bin/env python3
"""route - suggest a Claude model + effort for a task description.

A cheap keyword heuristic, not an oracle. It exists so the manager's routing is
consistent and so you can sanity-check your gut. Reads routing.md rules; prints
model, effort, worker profile, and the reason.

    python route.py "fix the race condition in the sync queue"
    python route.py "rename all uses of fooBar to foo_bar across the repo"
    python route.py "design the offline sync engine"
"""
import sys

RULES = [
    # (any-of keywords, model, effort, profile, reason)
    (("design", "architect", "data model", "schema design", "api design", "from scratch",
      "rewrite", "novel", "greenfield", "sync strategy", "framework choice"),
     "fable-5.1", "xhigh", "self / planner",
     "hard-design: taste matters, lasting consequences -> Fable. Output ADRs via /ask-build."),
    (("plan", "break down", "epic", "sequence", "roadmap", "spec out", "scope"),
     "opus-5", "xhigh", "planner",
     "planning a feature -> Opus (Fable only if genuinely novel)."),
    (("race", "deadlock", "heisenbug", "corrupt", "subtle", "works locally", "intermittent",
      "flaky", "memory leak", "only in prod", "hard bug", "deep bug"),
     "opus-5", "xhigh", "self",
     "deep bug: needs max reasoning depth -> Opus xhigh (or /fast)."),
    (("review", "adversarial", "check the diff", "audit the change"),
     "opus-5 (must differ from author)", "high", "reviewer-adversarial",
     "review: use a DIFFERENT, stronger model than the author. One pass, never recursive."),
    (("research", "best way to", "what's the best", "scope the library", "compare options",
      "verify", "is it true", "look up", "find out"),
     "researcher agent", "-", "researcher",
     "research/verify: never answer from memory - dispatch the researcher agent."),
    (("rename", "codemod", "find and replace", "format", "lint", "boilerplate", "scaffold",
      "mechanical", "bulk", "across all files", "regenerate types"),
     "haiku-4.5", "medium", "worker-implementer (mechanical)",
     "bulk mechanical + unambiguous + you'll review the diff -> Haiku."),
    (("explain", "what does", "summarize", "digest", "read the", "walk me through", "understand"),
     "sonnet-5", "medium", "self",
     "explain/summarize -> Sonnet medium (Haiku if it's a huge dump for gist only)."),
    (("draft", "write a post", "thread", "content", "blog", "tweet"),
     "sonnet-5 draft -> fable/opus polish", "high", "content-machine",
     "content: Sonnet draft then one polish pass. Origin must be human words."),
]

DEFAULT = ("sonnet-5", "high", "worker-implementer",
           "daily implementation (the default for ~90% of work) -> Sonnet high.")


def route(task: str):
    t = task.lower()
    for kws, model, effort, profile, reason in RULES:
        if any(k in t for k in kws):
            return model, effort, profile, reason
    return DEFAULT


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    task = " ".join(sys.argv[1:])
    model, effort, profile, reason = route(task)
    print(f"task    : {task}")
    print(f"model   : {model}")
    print(f"effort  : {effort}")
    print(f"profile : {profile}")
    print(f"reason  : {reason}")
    print("\n(heuristic - override with judgement; when limit is low, drop one row: fable->opus->sonnet)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
