# --- agentic-setup aliases : paste into your PowerShell profile ---
# open it with:  notepad $PROFILE     (create it if missing)
# reload with:   . $PROFILE

$AS = 'D:\agentic-setup'

# --- Claude Code launchers (Ondrej's "one-letter alias for the long command") ---
function cc  { claude --dangerously-skip-permissions @args }         # yolo (guard hook still blocks catastrophes)
function ccp { claude --permission-mode plan @args }                 # plan mode
function ccr { claude --dangerously-skip-permissions -c @args }      # resume last, yolo

# --- context-as-code CLI (Phase 2) ---
function ctx { python "$env:USERPROFILE\.claude\skills\context-artifacts\scripts\ctx.py" @args }

# --- model routing heuristic (Phase 3) ---
function route { python "$env:USERPROFILE\.claude\skills\manager\scripts\route.py" @args }

# --- review gate (Phase 4) ---
function nm { python "$env:USERPROFILE\.claude\skills\no-mistakes\scripts\nm.py" @args }

# --- agent worktrees (Phase 8) ---
function aw { & "$AS\08-terminal-and-parallelism\scripts\aw.ps1" @args }
function awcd { Set-Location (aw cd @args) }                          # awcd foo -> cd into that worktree

# --- knowledge hydration helper (Phase 6) ---
function hydrate-scan { python "$env:USERPROFILE\.claude\skills\hydrate\scripts\hydrate.py" scan @args }

Write-Host "agentic-setup aliases loaded: cc ccp ccr | ctx route nm | aw awcd | hydrate-scan" -ForegroundColor DarkGray
