#!/usr/bin/env python3
"""hydrate helper - chunk big sources and do a rough first-pass extraction.

The judgement lives in the `hydrate` skill; this just does the mechanical bits.

    python hydrate.py chunk <file> [--words 5000 --overlap 400]
        -> writes <file>.chunkNN.txt files, prints the list
    python hydrate.py scan <file>
        -> prints lines that look like DECISION / QUESTION / ACTION / DATE, with line numbers
"""
import re
import sys
from pathlib import Path

DECISION_RX = re.compile(r"\b(we (decided|agreed|will|are going to|chose|settled on)|"
                         r"decision:|let's go with|final call|we're not going to|"
                         r"the plan is)\b", re.I)
QUESTION_RX = re.compile(r"\b(open question|still not sure|need to (decide|figure out|check)|"
                         r"tbd|unclear|question is|not decided|we should (probably )?discuss)\b|"
                         r"\?\s*$", re.I)
ACTION_RX = re.compile(r"\b(action item|next step|todo|i'll |i will |you'll |will do |"
                       r"follow up|by (monday|tuesday|wednesday|thursday|friday|next week|eod|tomorrow))\b", re.I)
DATE_RX = re.compile(r"\b(20\d\d[-/]\d\d?[-/]\d\d?|\d\d?\s(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))", re.I)


def chunk(path: Path, words=5000, overlap=400):
    text = path.read_text(encoding="utf-8", errors="replace")
    toks = text.split()
    if len(toks) <= words:
        print(f"{path.name}: {len(toks)} words - no chunking needed.")
        return
    out = []
    i = 0
    n = 0
    while i < len(toks):
        n += 1
        seg = toks[i:i + words]
        p = path.with_suffix(path.suffix + f".chunk{n:02d}.txt")
        p.write_text(" ".join(seg), encoding="utf-8")
        out.append(p.name)
        i += words - overlap
    print(f"{path.name}: {len(toks)} words -> {n} chunks ({words}w, {overlap}w overlap)")
    for o in out:
        print("  " + o)


def scan(path: Path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = 0
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        tags = []
        if DECISION_RX.search(s):
            tags.append("DECISION")
        if QUESTION_RX.search(s):
            tags.append("QUESTION")
        if ACTION_RX.search(s):
            tags.append("ACTION")
        if tags:
            if DATE_RX.search(s):
                tags.append("has-date")
            print(f"L{ln:>4} [{'/'.join(tags)}] {s[:160]}")
            hits += 1
    print(f"\n{hits} candidate lines. This is a ROUGH pass - read the full source and use judgement.")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, target = sys.argv[1], Path(sys.argv[2])
    if not target.exists():
        print(f"no such file: {target}")
        return 2
    if cmd == "chunk":
        w = int(sys.argv[sys.argv.index("--words") + 1]) if "--words" in sys.argv else 5000
        o = int(sys.argv[sys.argv.index("--overlap") + 1]) if "--overlap" in sys.argv else 400
        chunk(target, w, o)
    elif cmd == "scan":
        scan(target)
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
