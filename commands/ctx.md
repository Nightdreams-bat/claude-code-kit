---
description: Run the context-as-code CLI (map / status / new / log / validate / init). Usage: /ctx <subcommand> [args]
---

The argument is: `$ARGUMENTS`

`ctx` manages this project's `context/` folder (the intent repo that lives
separate from source code). Run:

```
python ~/.claude/skills/context-artifacts/scripts/ctx.py $ARGUMENTS
```

(or the `ctx` alias if installed).

Subcommands: `map`, `status`, `new <decision|spec|epic|convention> "title"`,
`log "message"`, `validate`, `init`.

If `$ARGUMENTS` is empty, run `ctx status` then `ctx map`.

After running, briefly interpret the output for the user. If they just created an
artifact, open it and help them fill it in following the `context-artifacts`
skill. Then stop.
