#!/usr/bin/env bash
# aw - "agent worktree" helper (Git Bash / WSL / macOS). Windows-primary version
# is aw.ps1. Worktrees live on D: (C: is space-constrained).
#
#   aw new <name>    create worktree + branch aw/<name>, bootstrap, open a claude session
#   aw list          list worktrees
#   aw cd <name>     print the path
#   aw done <name>   (from primary) merge aw/<name> --no-ff, remove worktree, delete branch
#   aw drop <name>   discard worktree + branch, no merge
#   aw clean         prune
#
# alias:  alias aw='bash ~/agentic-setup/08-terminal-and-parallelism/scripts/aw.sh'
set -euo pipefail
WT_ROOT="${AW_ROOT:-/d/worktrees}"

repo_root() { git rev-parse --show-toplevel 2>/dev/null; }
repo_name() { basename "$(repo_root)"; }
common_dir() { git rev-parse --path-format=absolute --git-common-dir 2>/dev/null; }
is_primary() { [ "$(git rev-parse --path-format=absolute --git-dir)" = "$(common_dir)" ]; }
rm_worktree() { # $1=dest  $2=--force (optional)
  git worktree remove ${2:-} "$1" 2>/dev/null || true
  if [ -e "$1" ]; then
    echo "could not delete $1 - close the tab/shell sitting in it, then: aw clean" >&2
    git worktree prune 2>/dev/null || true
  fi
}

repo_root >/dev/null || { echo "not inside a git repository" >&2; exit 1; }
cmd="${1:-help}"; name="${2:-}"

case "$cmd" in
  new)
    [ -n "$name" ] || { echo "usage: aw new <name>" >&2; exit 1; }
    repo="$(repo_name)"; branch="aw/$name"; dest="$WT_ROOT/$repo-$name"
    [ -e "$dest" ] && { echo "$dest exists" >&2; exit 1; }
    mkdir -p "$WT_ROOT"
    base="$(git symbolic-ref --short HEAD)"
    git worktree add -b "$branch" "$dest" "$base"
    echo "worktree: $dest (branch $branch off $base)"
    primary="$(dirname "$(common_dir)")"
    for f in "$primary"/.env* "$primary"/.envrc; do
      [ -f "$f" ] && cp "$f" "$dest/$(basename "$f")" && echo "  copied $(basename "$f")"
    done
    for s in scripts/setup-worktree.sh scripts/setup-worktree.ps1; do
      [ -f "$dest/$s" ] && { echo "  running $s"; (cd "$dest" && bash "$s"); break; }
    done
    if command -v wezterm >/dev/null 2>&1; then
      wezterm cli spawn --cwd "$dest" -- bash -c 'claude --dangerously-skip-permissions; exec bash' >/dev/null
      echo "opened WezTerm tab -> claude in $repo-$name"
    else
      echo "cd \"$dest\" && claude"
    fi
    ;;
  list) git worktree list ;;
  cd) [ -n "$name" ] || { echo "usage: aw cd <name>" >&2; exit 1; }
      echo "$WT_ROOT/$(repo_name)-$name" ;;
  done)
    [ -n "$name" ] || { echo "usage: aw done <name>" >&2; exit 1; }
    is_primary || { echo "run from the PRIMARY checkout" >&2; exit 1; }
    branch="aw/$name"; dest="$WT_ROOT/$(repo_name)-$name"
    git --no-pager diff --stat "HEAD...$branch"
    read -rp "merge $branch into $(git symbolic-ref --short HEAD)? [y/N] " ok
    [ "$ok" = y ] || { echo aborted; exit 1; }
    git merge --no-ff "$branch"
    rm_worktree "$dest"
    git branch -d "$branch"
    echo "merged and cleaned up $name." ;;
  drop)
    [ -n "$name" ] || { echo "usage: aw drop <name>" >&2; exit 1; }
    rm_worktree "$WT_ROOT/$(repo_name)-$name" --force
    git branch -D "aw/$name" 2>/dev/null || true
    echo "discarded $name." ;;
  clean) git worktree prune -v; git worktree list ;;
  *) echo "aw new <name> | list | cd <name> | done <name> | drop <name> | clean" ;;
esac
