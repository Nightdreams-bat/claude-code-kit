#!/usr/bin/env python3
"""ctx - the context-as-code CLI. Agent-facing AND human-facing.

Modelled on 10X's `10x context` / `10x validate` CLI. Follows the axi principles
(Kun): token-efficient plain-text output, minimal default schema, does one thing
per subcommand, exit code says pass/fail.

Usage (run from anywhere inside a project that has a context/ dir):
    python ctx.py map                      # print the orientation packet
    python ctx.py new decision "Use SQLite not Postgres"
    python ctx.py new spec     "Offline sync engine"
    python ctx.py new epic     "v2 rewrite"
    python ctx.py new convention "error-handling"
    python ctx.py log "shipped the guard hook; enabled globally"
    python ctx.py status                   # one-line counts
    python ctx.py validate                 # process lint -> exit 1 on drift
    python ctx.py init                     # scaffold a context/ dir here

Install: copy to ~/.claude/skills/context-artifacts/scripts/ctx.py  (or D:\bin)
and add an alias `ctx` (see 08-terminal-and-parallelism/aliases).
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

FINAL_DECISION_STATES = {"accepted", "final", "superseded", "rejected", "done"}
ACTIVE_SPEC_STATES = {"in-progress", "in progress", "in-review", "in review", "active"}
ALL_SPEC_STATES = ACTIVE_SPEC_STATES | {"draft", "done", "blocked", "cancelled"}


def find_ctx(start: Path = None):
    cur = (start or Path.cwd()).resolve()
    for _ in range(30):
        for name in ("context", ".context"):
            if (cur / name / "_map.md").exists():
                return cur / name
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def slug(s: str):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "untitled"


def next_num(d: Path, glob: str):
    n = 0
    for f in d.glob(glob):
        m = re.match(r"(\d+)", f.name)
        if m:
            n = max(n, int(m.group(1)))
    return f"{n + 1:04d}"


def read(p: Path):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def field(text: str, key: str):
    for line in text.splitlines()[:20]:
        low = line.lower().strip().lstrip("-* ")
        if low.startswith(key.lower() + ":"):
            return line.split(":", 1)[1].strip().strip("*` ")
    return ""


# ---------------------------------------------------------------- commands

def cmd_init(_):
    root = Path.cwd() / "context"
    if (root / "_map.md").exists():
        print(f"already initialised: {root}")
        return 0
    for sub in ("decisions", "conventions", "specs"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    (root / "_map.md").write_text(_MAP_TEMPLATE, encoding="utf-8")
    (root / "log.md").write_text("# Work log\n<!-- newest first; `ctx log \"...\"` prepends a dated entry -->\n\n", encoding="utf-8")
    (root / "master.md").write_text(_MASTER_TEMPLATE, encoding="utf-8")
    (root / "conventions" / "con-index.md").write_text(
        "# Conventions index\n\nEvery `con-*.md` in this folder is a rule agents MUST follow.\n\n| file | rule (one line) |\n|---|---|\n", encoding="utf-8")
    print(f"created {root}\n  edit context/_map.md first - it is what the SessionStart hook injects.")
    return 0


def cmd_map(ctx):
    # same content the hook prints, minus the framing
    print(f"# context map for {ctx.parent.name}\n")
    print(read(ctx / "_map.md").strip() or "(empty _map.md)")
    dec = ctx / "decisions"
    if dec.is_dir():
        opend = [f for f in sorted(dec.glob("*.md"))
                 if (field(read(f), "status").lower() or "proposed") not in FINAL_DECISION_STATES]
        if opend:
            print("\n## open decisions")
            for f in opend:
                print(f"- {f.name}: {field(read(f), 'status') or 'proposed'}")
    log = ctx / "log.md"
    if log.exists():
        tail = [l for l in read(log).splitlines() if l.strip()][-15:]
        print("\n## recent log\n" + "\n".join(tail))
    return 0


def cmd_status(ctx):
    d = len(list((ctx / "decisions").glob("*.md"))) if (ctx / "decisions").is_dir() else 0
    od = 0
    if (ctx / "decisions").is_dir():
        od = sum(1 for f in (ctx / "decisions").glob("*.md")
                 if (field(read(f), "status").lower() or "proposed") not in FINAL_DECISION_STATES)
    s = len(list((ctx / "specs").glob("*.md"))) if (ctx / "specs").is_dir() else 0
    c = len(list((ctx / "conventions").glob("con-*.md"))) if (ctx / "conventions").is_dir() else 0
    loglines = len([l for l in read(ctx / "log.md").splitlines() if l.strip().startswith("- ")])
    print(f"context={ctx}  decisions={d} (open {od})  specs={s}  conventions={c}  log_entries={loglines}")
    return 0


def cmd_new(ctx, args):
    if len(args) < 2:
        print("usage: ctx new <decision|spec|epic|convention> \"title\"")
        return 2
    kind, title = args[0], " ".join(args[1:])
    today = date.today().isoformat()
    if kind == "decision":
        d = ctx / "decisions"
        num = next_num(d, "*.md")
        p = d / f"{num}-{slug(title)}.md"
        p.write_text(_DECISION_TEMPLATE.format(num=num, title=title, date=today), encoding="utf-8")
    elif kind in ("spec", "epic"):
        d = ctx / "specs"
        num = next_num(d, f"{kind}-*.md")
        p = d / f"{kind}-{num}-{slug(title)}.md"
        tpl = _EPIC_TEMPLATE if kind == "epic" else _SPEC_TEMPLATE
        p.write_text(tpl.format(num=num, title=title, date=today), encoding="utf-8")
    elif kind == "convention":
        d = ctx / "conventions"
        p = d / f"con-{slug(title)}.md"
        p.write_text(_CONVENTION_TEMPLATE.format(title=title, date=today), encoding="utf-8")
    else:
        print(f"unknown kind: {kind}")
        return 2
    print(f"created {p.relative_to(ctx.parent)}")
    return 0


def cmd_log(ctx, args):
    if not args:
        print("usage: ctx log \"what happened\"")
        return 2
    msg = " ".join(args)
    stamp = date.today().isoformat()
    logf = ctx / "log.md"
    lines = read(logf).splitlines() or ["# Work log", ""]
    entry = f"- **{stamp}** {msg}"
    # insert directly above the first existing "- " entry, else append at end
    idx = next((i for i, l in enumerate(lines) if l.startswith("- **")), None)
    if idx is None:
        lines.append(entry)
    else:
        lines.insert(idx, entry)
    logf.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("logged.")
    return 0


def cmd_validate(ctx):
    """Process lint. Flags DRIFT: authored state disagreeing with derived state,
    plus structural problems. Exit 1 if anything found."""
    problems = []
    warn = []

    # decisions
    dec = ctx / "decisions"
    if dec.is_dir():
        for f in sorted(dec.glob("*.md")):
            t = read(f)
            st = field(t, "status").lower()
            if not st:
                problems.append(f"{f.name}: no `status:` field (proposed/accepted/rejected/superseded)")
            if "## consequences" not in t.lower() and "## trade" not in t.lower():
                warn.append(f"{f.name}: no Consequences/Trade-offs section")
            if re.search(r"\bTODO\b|\bTBD\b|<fill|<[a-z][^>\n]{3,}>", t):
                warn.append(f"{f.name}: still contains a <placeholder> / TODO / TBD - fill it in")

    # specs: derived vs authored status
    spec = ctx / "specs"
    if spec.is_dir():
        for f in sorted(spec.glob("spec-*.md")):
            t = read(f)
            authored = field(t, "status").lower()
            boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", t, re.M)
            if boxes:
                done = all(b.lower() == "x" for b in boxes)
                any_done = any(b.lower() == "x" for b in boxes)
                derived = "done" if done else ("in-progress" if any_done else "draft")
                if authored in ("done",) and not done:
                    problems.append(f"{f.name}: status=done but {boxes.count(' ')} checkbox(es) unchecked (derived={derived})")
                if authored in ("draft", "") and any_done:
                    problems.append(f"{f.name}: status={authored or 'missing'} but work has started (derived=in-progress)")
            if authored and authored not in ALL_SPEC_STATES:
                warn.append(f"{f.name}: unusual status '{authored}'")

    # conventions referenced but missing
    con = ctx / "conventions"
    if con.is_dir():
        idx = read(con / "con-index.md")
        for ref in re.findall(r"con-[a-z0-9-]+\.md", idx):
            if not (con / ref).exists():
                problems.append(f"con-index.md references {ref} which does not exist")
        for f in con.glob("con-*.md"):
            if f.name != "con-index.md" and f.name not in idx:
                warn.append(f"{f.name} not listed in con-index.md")

    # stale log
    logf = ctx / "log.md"
    if logf.exists():
        dates = re.findall(r"\*\*(\d{4}-\d{2}-\d{2})\*\*", read(logf))
        if dates:
            last = max(dates)
            days = (date.today() - date.fromisoformat(last)).days
            if days > 10:
                warn.append(f"log.md last entry was {days} days ago - is context current?")

    # _map freshness
    if not read(ctx / "_map.md").strip():
        problems.append("_map.md is empty - the SessionStart hook has nothing to inject")

    for p in problems:
        print(f"DRIFT  {p}")
    for w in warn:
        print(f"warn   {w}")
    if not problems and not warn:
        print("validate: clean")
    print(f"\n{len(problems)} drift, {len(warn)} warnings")
    return 1 if problems else 0


# ---------------------------------------------------------------- templates

_MAP_TEMPLATE = """# _map.md - project orientation (injected into every session)

Keep this SHORT and CURRENT. This is the single highest-value file in the repo.

## What this project is
<one paragraph: the product, who it is for, what done looks like>

## Where things are
- source code: <path / repo>
- deploy / hosting: <where, or "local only">
- context repo: this folder

## The 3-5 things an agent must not get wrong
1. <invariant>
2. <invariant>

## Current focus
<what we are working on right now>

## Pointers
- decisions/  - why the architecture is the way it is (ADRs)
- conventions/ - rules agents MUST follow when writing code
- specs/      - epics and detailed specs for in-flight work
- log.md      - running work log (newest first)
- master.md   - the self-hydrating knowledge base (maintained by /hydrate)
"""

_MASTER_TEMPLATE = """# master.md - self-hydrating knowledge base

Maintained by the `hydrate` skill. Do not hand-edit large sections; feed sources
through `/hydrate` and let it reconcile. Humans are bad at memory - the agent
holds it here.

## Entities
(people, services, accounts, external systems - name: one-line description)

## Durable facts
(things that are true and unlikely to change; each with a date)

## Open questions
(unresolved; each with who/what would resolve it)

## Recently changed
(rolling: what this file learned in the last few hydrations)
"""

_DECISION_TEMPLATE = """# ADR {num}: {title}

status: proposed
date: {date}
deciders: <you>

## Context
<what forces are at play; what problem needs a decision; state of the project now>

## Options considered
1. **<option A>** - <pros> / <cons>
2. **<option B>** - <pros> / <cons>

## Decision
<the option chosen, stated plainly>

## Consequences
- <what becomes easier>
- <what becomes harder / what we are now locked into>
- <what would make us revisit this>
"""

_SPEC_TEMPLATE = """# spec-{num}: {title}

status: draft
date: {date}
epic: <epic-NNNN or "none">

## Goal
<one paragraph: what this delivers and why>

## Non-goals
- <explicitly out of scope>

## Approach
<the technical shape: components, data flow, key types>

## Decisions this depends on
- ADR <NNNN>

## Tickets
- [ ] <smallest shippable step>
- [ ] <next>
- [ ] tests where they genuinely matter (do NOT over-test - see conventions)
- [ ] update docs / README
- [ ] update context/log.md

## Proof of done
<the visible evidence that will show this works: test output, screenshot, command>
"""

_EPIC_TEMPLATE = """# epic-{num}: {title}

status: active
date: {date}

## Outcome
<what is true when this epic is done>

## Milestones
- [ ] <milestone 1> -> spec-<NNNN>
- [ ] <milestone 2>

## Risks / unknowns
- <risk>
"""

_CONVENTION_TEMPLATE = """# con: {title}

added: {date}

## Rule
<the rule, imperative voice: "Always ...", "Never ...">

## Why
<the reasoning - so a future agent knows when the rule can bend>

## Examples
- good: <...>
- bad: <...>
"""


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cmd, rest = args[0], args[1:]
    if cmd == "init":
        return cmd_init(rest)
    ctx = find_ctx()
    if not ctx:
        print("no context/ dir found walking up from here. Run `ctx init` to create one.")
        return 2
    return {
        "map": lambda: cmd_map(ctx),
        "status": lambda: cmd_status(ctx),
        "new": lambda: cmd_new(ctx, rest),
        "log": lambda: cmd_log(ctx, rest),
        "validate": lambda: cmd_validate(ctx),
    }.get(cmd, lambda: (print(f"unknown command: {cmd}"), 2)[1])()


if __name__ == "__main__":
    sys.exit(main())
