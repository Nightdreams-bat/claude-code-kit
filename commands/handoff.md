---
description: Compact this session into a copy-pasteable handoff for a fresh agent. Usage: /handoff [focus]
---

The optional focus is: `$ARGUMENTS`

Write a complete handoff so a fresh agent with zero memory can continue without
re-asking or repeating mistakes. Output it as ONE fenced code block, and also
save it to `%TEMP%\handoff-<8char>.md` (tell the user the path).

Principles: state not instructions ("X is done", never "do X next"); reference
don't duplicate (point at ADRs/specs/PRs by path); capture the WHY and the dead
ends; redact secrets; cut anything obvious from reading the code.

Sections: Goal / Background / Current State (DONE|PARTIAL|NOT STARTED) / Key
Decisions & why / Traps & Dead Ends / Relevant Files (path:lines - what's there) /
Open Work (as state + dependencies) / Prompt for the Fresh Agent (declarative,
ends with "read every file listed above before acting").
