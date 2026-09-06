# Credits

This kit is a personal synthesis. Very little of the *thinking* here is original —
it is assembled from people who published their agentic-engineering setups and
from open skill collections. This file records who each piece comes from.

If you recognize your work and want the credit changed, expanded, or removed,
open an issue.

## Workflow skills — synthesized from five published setups

The `context-artifacts`, `manager`, `no-mistakes`, `ask-and-build`, `hydrate`,
`personal-agents` and `content-machine` skills (plus the guardrail and
SessionStart hooks referenced in the docs) are a Windows/solo adaptation of ideas
from these sources. Each skill's `SKILL.md` names its origin in a blockquote at
the top.

| Idea taken | Person | Where it came from |
|---|---|---|
| Guardrail hook, `ask-then-build` / decide-before-building, one review pass by a different model, model-per-task, terminal YOLO aliases, ADRs in `docs/adr/`, "tell the model not to add tests", git-worktree parallelism | **David Ondrej** | *My Agentic Engineering Workflow* + [github.com/davidondrej/skills](https://github.com/davidondrej/skills) |
| Manager/worker agent + explicit routing rules, the `no mistakes` review pipeline, "wrap CLIs to be token-efficient; CLIs beat MCP", WezTerm as the base terminal | **Kun** (ex-Meta, builds *first mate*) | *L8 Principal* podcast |
| "Models are done — stop micromanaging, spend effort on *what* to build and on the markdown", "the backlog is dead — launch an agent", near-empty `AGENTS.md`, minimal MCP | **Thorsten Ball** (Amp / Sourcegraph) | *Agentic Engineering by a 10x dev* |
| Self-hydrating knowledge (feed transcripts into a running master-context file), personal-life agents (daily brief, triage), "work *on* the machine, not *in* it" | **Flo Crivello** (Lindy) | *Ex-Uber dev's Multi-Agent Workflow* |
| Context-as-code / "meta-harness" (a repo separate from code holding typed markdown), SessionStart hook as "benevolent prompt injection", `/validate` as linting for your process, one skill per artifact type, human owns first + last mile | **Alex Lieberman + Dan** | *10X* podcast |
| The LLM-wiki pattern that `hydrate` builds on | **Andrej Karpathy** | "LLM wiki" / building-your-own-wiki notes |

## Learning skills

| Skill | Ported from |
|---|---|
| `teach`, `visualize` | [github.com/amosblomqvist/learn](https://github.com/amosblomqvist/learn) ("How I Use AI to Learn Things"), originally a `pi` configuration |
| `level-up`, `signal-from-expert` | [github.com/davidondrej/skills](https://github.com/davidondrej/skills), adapted to run on WebSearch/WebFetch instead of a paid API |
| `analyze-sessions`, `web-debug`, `youtube-transcript` | ported in spirit from [github.com/amosblomqvist/pi-config](https://github.com/amosblomqvist/pi-config) |
| `tutor`, `tutor-setup` | built around the Obsidian StudyVault layout that `teach` writes to |

## Skills without a single clear upstream

`diagram-maker`, `pdf-craft`, `clone-website`, `grilling` / `grill-me`,
`scan-before-publish`, `claude-checkup` were assembled from publicly shared Claude
skills and common practice. `diagram-maker` carries an `openclaw` metadata tag
from whichever collection it originally shipped in. If one of these is yours,
tell me and I'll attribute it properly.

## Tools these skills call

- **ggshield** — GitGuardian (`scan-before-publish`)
- **yt-dlp** — (`youtube-transcript`, `teach`)
- **WezTerm** — Wez Furlong (`terminal/`)
- **Excalidraw** format — Excalidraw contributors (`diagram-maker`)
- Fonts bundled with `pdf-craft`: IBM Plex (SIL OFL), Newsreader (SIL OFL), Sora
  (SIL OFL), Atkinson Hyperlegible (Braille Institute license). Each font's
  license travels with the file.

## The rest

Everything else — the packaging, the Windows adaptation, the routing heuristics,
the specific prompts — is by **Nightdreams-bat**, and freely reusable under the
MIT license.
