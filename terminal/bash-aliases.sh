# --- agentic-setup aliases : source from ~/.bashrc  (Git Bash / WSL) ---
#   echo 'source ~/agentic-setup/08-terminal-and-parallelism/aliases/bash-aliases.sh' >> ~/.bashrc

AS=~/agentic-setup
CLAUDE_SKILLS="$HOME/.claude/skills"

alias cc='claude --dangerously-skip-permissions'
alias ccp='claude --permission-mode plan'
alias ccr='claude --dangerously-skip-permissions -c'

alias ctx='python "$CLAUDE_SKILLS/context-artifacts/scripts/ctx.py"'
alias route='python "$CLAUDE_SKILLS/manager/scripts/route.py"'
alias nm='python "$CLAUDE_SKILLS/no-mistakes/scripts/nm.py"'
alias aw='bash "$AS/08-terminal-and-parallelism/scripts/aw.sh"'
awcd() { cd "$(aw cd "$1")"; }
alias hydrate-scan='python "$CLAUDE_SKILLS/hydrate/scripts/hydrate.py" scan'
