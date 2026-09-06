# claude-code-kit

My personal [Claude Code](https://claude.com/claude-code) setup — **23 skills, 23
slash commands, 7 subagents, and a terminal layer** for running several agents in
parallel. It is a Windows-first, solo-developer adaptation of ideas from people
who published their agentic-engineering workflows (see [CREDITS.md](CREDITS.md)).

Nothing here is a framework. Each piece is a plain markdown file Claude Code reads
directly. Take the three you want and leave the rest.

```
skills/      23 skill packages (SKILL.md + scripts/references)
commands/    23 slash commands  (/careful, /review, /ask-build, …)
agents/      7 subagents        (planner, worker, adversarial reviewer, …)
terminal/    WezTerm config + `aw` git-worktree helper + shell aliases
```

---

## Install

Requires Claude Code, Python 3, and git. `C:` paths below → use `~` on macOS/Linux.

```bash
git clone https://github.com/Nightdreams-bat/claude-code-kit.git
cd claude-code-kit

# skills, commands, agents  (merge into your ~/.claude)
cp -r skills/*    ~/.claude/skills/
cp -r commands/*  ~/.claude/commands/
cp -r agents/*    ~/.claude/agents/
```

Then restart Claude Code. Type `/` to see the commands; skills load on demand by
their description.

**Terminal layer (optional):** copy `terminal/wezterm.lua` to `~/.wezterm.lua`,
paste `terminal/profile-snippet.ps1` into your PowerShell `$PROFILE` (or source
`terminal/bash-aliases.sh` from `~/.bashrc`), and point the `aw` alias at
`terminal/aw.ps1` / `aw.sh`. See the comments in each file.

Some skills shell out to external tools — install only what you use:
`ggshield` (scan-before-publish), `yt-dlp` (youtube-transcript, teach),
`node` (pdf-craft), WezTerm (terminal).

---

## Skills

### Workflow & orchestration

| Skill | What it does | From |
|---|---|---|
| **ask-and-build** | Surfaces the real architectural/product decisions hidden in a build request, drills them one at a time with a recommendation, writes each answer as an ADR, hands the implementer a brief. | David Ondrej |
| **manager** | Run the session as a manager that routes work to worker subagents by an explicit `routing.md`, keeping its own context clean. | Kun |
| **no-mistakes** | Review gate before merge: infer intent, one adversarial pass by a *different, stronger* model, categorise findings (auto-fix / escalate / product-decision), require real proof. | Kun + David Ondrej |
| **context-artifacts** | Create and maintain the `context/` repo — `_map`, ADRs, conventions, epics/specs, work log, self-hydrating master file — kept *separate* from source. | 10X (Lieberman + Dan) |
| **hydrate** | Turn a transcript / brain-dump / article / video into structured knowledge in `context/` and the vault, reconciling contradictions with what's already there. | Flo Crivello / Karpathy |
| **personal-agents** | Set up and tune the recurring agents — daily brief, weekly review, inbox triage, session-log rollup — that do the standing work. | Flo Crivello (Lindy) |
| **content-machine** | Human take → finished post / thread / script in your voice: idea sweep, one-at-a-time interview, draft, editor-council score-and-revise loop. | Alex Lieberman (10X) |

### Learning

| Skill | What it does | From |
|---|---|---|
| **teach** | Teach anything so it *locks in* — two teaching principles applied to every explanation, from a one-liner to a deep dive. Mirrors the lesson into an Obsidian vault. | amosblomqvist/learn |
| **visualize** | Add one *correct*, minimal visual to a lesson — a diagram or geometric picture that renders inline. | amosblomqvist/learn |
| **level-up** | Short adaptive assessment that maps your technical/product knowledge gaps and grows a learning plan. Feeds `teach` and `tutor`. | davidondrej/skills |
| **signal-from-expert** | Surface the few passages from an expert's real body of work that hit your exact situation — verbatim, with sources — then at least one gap where they show you're wrong. | davidondrej/skills |
| **tutor** | Interactive quiz tutor over an Obsidian StudyVault — diagnostic, targeted review, weak-area drills, progress dashboard. | — |
| **tutor-setup** | Turn PDF/text/web sources *or* a source-code project into an Obsidian StudyVault. | — |

### Making things

| Skill | What it does | From |
|---|---|---|
| **diagram-maker** | SVG/HTML or Excalidraw diagrams for concepts, architecture, flows, whiteboards. | open collection |
| **pdf-craft** | PDFs and print documents that look *designed* — a deliberate typographic choice per document, forced to differ across documents. Bundles fonts. | open collection |
| **clone-website** | Reverse-engineer and rebuild one or more sites section-by-section, dispatching parallel builder agents in worktrees. | open collection |

### Config & repo hygiene

| Skill | What it does | From |
|---|---|---|
| **claude-checkup** | Audit, plan, and (only with approval) repair this machine's Claude Code setup — CLAUDE.md bloat, unused MCP servers, misfiring skills, broken hook paths, missed Haiku delegation — plus a 30-day credit rollup. Tier-graded scorecard. | — |
| **scan-before-publish** | Run GitGuardian's `ggshield` over a repo's history *and* working tree before it goes anywhere public. | — |
| **analyze-sessions** | Local analysis of past Claude Code sessions — token/cost rollups, most-used tools, prompt-pattern mining, rendering an old session to readable text. | amosblomqvist/pi-config |

### Debugging & input

| Skill | What it does | From |
|---|---|---|
| **web-debug** | Order-of-operations playbook for debugging a web app through the Chrome browser tools. | amosblomqvist/pi-config |
| **youtube-transcript** | Fetch a video's title, metadata, and full transcript as text/JSON. | amosblomqvist/pi-config |
| **grilling** (`grill-me`) | Relentless round-based interview that maps your plan as a decision tree and refuses to let anything stay silently assumed. | open collection |

---

## Slash commands

**Behaviour one-shots** (apply to the next turn only):
`/careful` · `/concise` · `/no-comments` · `/plan-first` · `/tdd`

**Thinking & utility:**
`/decisions` (what you're unsure about, retrospective) ·
`/next-decision` (drill open decisions, forward-looking) ·
`/prompt-me` (interview me to pull what's in my head) ·
`/stop-overthinking` · `/goal` (write an autonomous-loop contract) ·
`/handoff` (compact the session for a fresh agent) ·
`/file-tree` · `/who` (background check on a person)

**Skill launchers:**
`/ask-build` · `/content` · `/ctx` · `/dispatch` · `/hydrate` · `/level-up` ·
`/review` · `/signal` · `/validate` · `/guard` (toggle the bash guard)

---

## Subagents

| Agent | Model | Role |
|---|---|---|
| **planner** | opus | Goal/epic → sequenced implementation plan; surfaces trade-offs as decisions. No code. |
| **worker-implementer** | sonnet | Implements a well-specified chunk from a full briefing. Stops on design decisions. |
| **reviewer-adversarial** | opus | One thorough adversarial review pass by a stronger model. Real bugs only, no padding. |
| **researcher** | sonnet | Web research → focused, well-sourced brief. Verifies facts before they're taught. |
| **config-auditor** / **config-fixer** / **config-verifier** | sonnet / haiku / sonnet | The three phases of `claude-checkup` — audit, apply one approved fix, verify. |

---

## The parallel-agents model (`terminal/`)

One task = one git worktree = one Claude session. Never two writers on one tree.

```
aw new <name>     # worktree + branch aw/<name>, bootstrap, open a WezTerm tab running claude
aw list
aw done <name>    # from the primary checkout: review the diff, merge --no-ff, clean up
aw drop <name>    # discard, no merge
aw clean          # prune stale worktrees
```

Worktrees live at `D:\worktrees\<repo>-<name>` (off `C:` by design). Cap yourself
at 3–4 parallel agents — beyond that you can't hold the state, which was the whole
point. WezTerm keys use `Ctrl+a` as the leader (`\` / `-` split, `hjkl` move, `z`
zoom, `Ctrl+a n` new claude tab).

---

## Credits & license

Assembled from published work by David Ondrej, Kun, Thorsten Ball, Flo Crivello,
Alex Lieberman, Andrej Karpathy, and the open skill collections
[amosblomqvist/learn](https://github.com/amosblomqvist/learn) and
[amosblomqvist/pi-config](https://github.com/amosblomqvist/pi-config). Full
attribution in [CREDITS.md](CREDITS.md).

MIT — see [LICENSE](LICENSE). Bundled fonts and tools keep their own licenses.
