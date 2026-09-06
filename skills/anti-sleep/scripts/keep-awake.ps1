#requires -Version 5
<#
  keep-awake.ps1 — prevent Windows from sleeping / blanking the screen while
  long unattended agent runs are in progress. Windows equivalent of macOS `caffeinate`.

  Usage:
    keep-awake.ps1 -Hours 3            # hold wake lock for 3h (foreground; run in background)
    keep-awake.ps1 -Action status      # is a lock currently held? how long left?
    keep-awake.ps1 -Action stop        # release the lock now

  Mechanism: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED),
  re-asserted every 60s. The OS clears the state automatically when this process exits,
  so a crash or kill can never leave the machine permanently awake.
#>
[CmdletBinding()]
param(
  [double]$Hours = 3,
  [ValidateSet('start','status','stop')]
  [string]$Action = 'start'
)

$ErrorActionPreference = 'Stop'
$pidFile = Join-Path $env:TEMP 'claude-anti-sleep.pid'

function Get-Lock {
  if (-not (Test-Path $pidFile)) { return $null }
  try {
    $d = Get-Content $pidFile -Raw | ConvertFrom-Json
    $p = Get-Process -Id $d.pid -ErrorAction SilentlyContinue
    if (-not $p) { Remove-Item $pidFile -Force -ErrorAction SilentlyContinue; return $null }
    return $d
  } catch { Remove-Item $pidFile -Force -ErrorAction SilentlyContinue; return $null }
}

switch ($Action) {
  'status' {
    $d = Get-Lock
    if (-not $d) { Write-Output 'anti-sleep: no wake lock held.'; exit 0 }
    $ends = [DateTime]::Parse($d.ends)
    $left = $ends - (Get-Date)
    if ($left.TotalSeconds -le 0) { Write-Output "anti-sleep: lock (pid $($d.pid)) is past its end time; releasing is pending." }
    else { Write-Output ("anti-sleep: wake lock held by pid {0}, ends {1} ({2:hh\:mm\:ss} left)." -f $d.pid, $ends.ToString('HH:mm'), $left) }
    exit 0
  }
  'stop' {
    $d = Get-Lock
    if (-not $d) { Write-Output 'anti-sleep: nothing to stop.'; exit 0 }
    Stop-Process -Id $d.pid -Force -ErrorAction SilentlyContinue
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    Write-Output "anti-sleep: released wake lock (pid $($d.pid))."
    exit 0
  }
  'start' {
    $existing = Get-Lock
    if ($existing) {
      Stop-Process -Id $existing.pid -Force -ErrorAction SilentlyContinue
      Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
    if ($Hours -le 0 -or $Hours -gt 24) { throw "-Hours must be between 0 and 24 (got $Hours)." }

    Add-Type -Namespace Win32 -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true)]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
    $ES_CONTINUOUS = [uint32]2147483648
    $ES_SYSTEM_REQUIRED = [uint32]0x00000001
    $ES_DISPLAY_REQUIRED = [uint32]0x00000002
    $hold = $ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_DISPLAY_REQUIRED

    $ends = (Get-Date).AddHours($Hours)
    @{ pid = $PID; ends = $ends.ToString('o'); started = (Get-Date).ToString('o') } |
      ConvertTo-Json | Set-Content $pidFile -Encoding UTF8

    Write-Output ("anti-sleep: holding wake lock until {0} ({1}h). Ctrl+C or 'keep-awake.ps1 -Action stop' to release." -f $ends.ToString('HH:mm'), $Hours)
    try {
      while ((Get-Date) -lt $ends) {
        [void][Win32.Power]::SetThreadExecutionState($hold)
        Start-Sleep -Seconds 60
      }
      Write-Output "anti-sleep: reached end time; releasing wake lock."
    } finally {
      [void][Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS)
      Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
  }
}
