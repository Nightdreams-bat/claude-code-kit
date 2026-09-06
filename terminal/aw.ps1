<#
aw - "agent worktree" helper for running several Claude Code sessions in parallel
on one repo without collisions. Windows / PowerShell.

Ported from Ondrej's git-worktree skill + the Kun/AMP "one task = one worktree =
one agent" model. cmux/herder are macOS-only; this + WezTerm is the Windows path.

Worktrees live on D: (C: is space-constrained):  D:\worktrees\<repo>-<name>

Usage:
  aw new  <name>            create worktree + branch aw/<name>, bootstrap, open a WezTerm tab running claude
  aw list                   list worktrees for this repo
  aw cd   <name>            print the path (use:  cd (aw cd foo) )
  aw done <name>            (run from primary checkout) merge aw/<name> --no-ff, remove worktree, delete branch
  aw drop <name>            remove worktree + branch WITHOUT merging (discard)
  aw clean                  git worktree prune + list stale

Put `Set-Alias aw 'D:\agentic-setup\08-terminal-and-parallelism\scripts\aw.ps1'`
(or copy to D:\bin and add to PATH) in your PowerShell profile.
#>
param([Parameter(Position=0)][string]$Cmd, [Parameter(Position=1)][string]$Name)

$ErrorActionPreference = 'Stop'
$WT_ROOT = 'D:\worktrees'

function Repo-Root { (git rev-parse --show-toplevel 2>$null) }
function Repo-Name { Split-Path -Leaf (Repo-Root) }
function Common-Dir { git rev-parse --path-format=absolute --git-common-dir 2>$null }
function Is-Primary {
    (git rev-parse --path-format=absolute --git-dir) -eq (Common-Dir)
}
function Remove-Worktree {
    param([string]$Dest, [switch]$Force)
    $args = @('worktree','remove'); if ($Force) { $args += '--force' }; $args += $Dest
    & git @args 2>$null
    if (Test-Path $Dest) {
        # Windows holds a lock while a shell/agent has the worktree as its cwd.
        Write-Warning "could not delete $Dest - close the WezTerm tab / shell sitting in it, then run: aw clean"
        git worktree prune 2>$null
    }
}

if (-not (Repo-Root)) { Write-Error 'not inside a git repository'; exit 1 }

switch ($Cmd) {
  'new' {
    if (-not $Name) { Write-Error 'usage: aw new <name>'; exit 1 }
    $repo = Repo-Name
    $branch = "aw/$Name"
    $dest = Join-Path $WT_ROOT "$repo-$Name"
    if (Test-Path $dest) { Write-Error "$dest already exists"; exit 1 }
    New-Item -ItemType Directory -Force -Path $WT_ROOT | Out-Null

    # base off the current branch's upstream default (main/master) if it exists
    $base = (git symbolic-ref --short HEAD)
    git worktree add -b $branch "$dest" $base
    Write-Host "worktree: $dest  (branch $branch off $base)"

    # bootstrap: copy gitignored env/secret files (copy, never symlink)
    $primary = Split-Path -Parent (Common-Dir)
    Get-ChildItem -Path $primary -Force -File -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -match '^\.env' -or $_.Name -eq '.envrc' } |
      ForEach-Object {
        Copy-Item $_.FullName (Join-Path $dest $_.Name) -Force
        Write-Host "  copied $($_.Name)"
      }

    # run a repo-provided setup script if present
    foreach ($s in @('scripts\setup-worktree.ps1','scripts\setup-worktree.sh')) {
      $sp = Join-Path $dest $s
      if (Test-Path $sp) {
        Write-Host "  running $s"
        if ($s.EndsWith('.ps1')) { & $sp } else { bash $sp }
        break
      }
    }

    # open a WezTerm tab in the worktree, running claude in yolo mode
    $wez = Get-Command wezterm -ErrorAction SilentlyContinue
    if ($wez) {
      wezterm cli spawn --cwd "$dest" -- pwsh -NoExit -Command "claude --dangerously-skip-permissions" | Out-Null
      Write-Host "opened WezTerm tab -> claude running in $repo-$Name"
    } else {
      Write-Host "WezTerm not found. cd into it yourself:  cd `"$dest`"  then  claude"
    }
  }

  'list' {
    git worktree list
  }

  'cd' {
    if (-not $Name) { Write-Error 'usage: aw cd <name>'; exit 1 }
    Write-Output (Join-Path $WT_ROOT "$((Repo-Name))-$Name")
  }

  'done' {
    if (-not $Name) { Write-Error 'usage: aw done <name>'; exit 1 }
    if (-not (Is-Primary)) { Write-Error 'run `aw done` from the PRIMARY checkout, not a worktree'; exit 1 }
    $branch = "aw/$Name"
    $dest = Join-Path $WT_ROOT "$((Repo-Name))-$Name"
    git fetch -q --all 2>$null
    Write-Host "diff summary for $branch :"
    git --no-pager diff --stat "HEAD...$branch"
    $ok = Read-Host "merge $branch into $(git symbolic-ref --short HEAD)? [y/N]"
    if ($ok -ne 'y') { Write-Host 'aborted.'; exit 1 }
    git merge --no-ff $branch
    Remove-Worktree $dest
    git branch -d $branch
    Write-Host "merged and cleaned up $Name."
  }

  'drop' {
    if (-not $Name) { Write-Error 'usage: aw drop <name>'; exit 1 }
    $branch = "aw/$Name"
    $dest = Join-Path $WT_ROOT "$((Repo-Name))-$Name"
    Remove-Worktree $dest -Force
    git branch -D $branch 2>$null
    Write-Host "discarded $Name (worktree + branch removed, unmerged work gone)."
  }

  'clean' {
    git worktree prune -v
    $tracked = (git worktree list --porcelain | Select-String '^worktree ' | ForEach-Object { $_.Line -replace '^worktree ', '' })
    if (Test-Path $WT_ROOT) {
      Get-ChildItem $WT_ROOT -Directory | Where-Object { $_.Name -like "$((Repo-Name))-*" } | ForEach-Object {
        $p = $_.FullName -replace '\\', '/'
        if ($tracked -notcontains $p) {
          try { Remove-Item -Recurse -Force $_.FullName -ErrorAction Stop; Write-Host "removed stale $($_.Name)" }
          catch { Write-Warning "stale $($_.Name) still locked - close its tab" }
        }
      }
    }
    git worktree list
  }

  default {
    Write-Host @'
aw new <name> | list | cd <name> | done <name> | drop <name> | clean
'@
  }
}
