#requires -Version 5.1
<#
.SYNOPSIS
  Start an A2A bridge (or any local Node HTTP service) in the background, manually.

.DESCRIPTION
  Checks Node and the port, starts the bridge hidden, waits for /health (and an
  optional /ready), and writes a PID/metadata file. It never installs autostart.
  If the port is occupied it refuses to kill anything; use stop-bridge.ps1 or
  choose another port.

.EXAMPLE
  .\start-bridge.ps1 -BridgeScript .\bridge.mjs -Port 8787

.EXAMPLE
  .\start-bridge.ps1 -BridgeScript .\bridge.mjs -Port 8787 -ReadyPath /ready

.EXAMPLE
  .\start-bridge.ps1 -BridgeScript .\bridge.mjs -Port 8787 -TargetCommand "<target-exe>"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BridgeScript,

    [int]$Port = 8787,

    [string]$HealthPath = '/health',

    [string]$ReadyPath = '',

    [string]$LogDirectory,

    [string]$PidFile,

    [hashtable]$Environment = @{},

    [string]$TargetCommand,

    [string[]]$TargetArguments = @(),

    [int]$HealthTimeoutSeconds = 30
)

$ErrorActionPreference = 'Stop'

if (-not $LogDirectory -or -not $PidFile) {
    $stateRoot = if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'a2a-reproxy' } else { $PSScriptRoot }
    if (-not $LogDirectory) { $LogDirectory = Join-Path $stateRoot 'logs' }
    if (-not $PidFile) { $PidFile = Join-Path $stateRoot 'bridge.pid' }
}
$HealthPath = '/' + $HealthPath.TrimStart('/')
if ($ReadyPath) { $ReadyPath = '/' + $ReadyPath.TrimStart('/') }

$BridgeScript = (Resolve-Path -LiteralPath $BridgeScript -ErrorAction Stop).Path
$LogDirectory = [System.IO.Path]::GetFullPath($LogDirectory)
$PidFile = [System.IO.Path]::GetFullPath($PidFile)

$nodeCommand = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCommand) {
    throw 'Node.js was not found in PATH. Install Node.js or add it to PATH.'
}
$nodePath = if ($nodeCommand.Path) { $nodeCommand.Path } else { $nodeCommand.Source }

function Get-ListeningProcessId {
    param([int]$PortNumber)
    try {
        $connection = Get-NetTCPConnection -LocalPort $PortNumber -State Listen -ErrorAction Stop |
            Select-Object -First 1
        if ($connection) { return [int]$connection.OwningProcess }
    } catch {
        return $null
    }
    return $null
}

$existingPid = Get-ListeningProcessId -PortNumber $Port
if ($existingPid) {
    $matchesPidFile = $false
    if (Test-Path -LiteralPath $PidFile) {
        try {
            $existing = Get-Content -LiteralPath $PidFile -Raw | ConvertFrom-Json
            if ([int]$existing.pid -eq $existingPid -and $existing.script -eq $BridgeScript) {
                $matchesPidFile = $true
            }
        } catch {
            $matchesPidFile = $false
        }
    }
    if ($matchesPidFile) {
        Write-Host "Bridge is already running on port $Port (PID $existingPid)."
        exit 0
    }
    throw "Port $Port is already in use by PID $existingPid. Refusing to kill it. Run stop-bridge.ps1 or choose another port."
}

New-Item -ItemType Directory -Force -Path $LogDirectory | Out-Null
$pidDirectory = Split-Path -Parent $PidFile
if ($pidDirectory) { New-Item -ItemType Directory -Force -Path $pidDirectory | Out-Null }

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$stdoutLog = Join-Path $LogDirectory "bridge-$stamp.out.log"
$stderrLog = Join-Path $LogDirectory "bridge-$stamp.err.log"
$healthUrl = "http://127.0.0.1:$Port$HealthPath"
$readyUrl = if ($ReadyPath) { "http://127.0.0.1:$Port$ReadyPath" } else { '' }

$savedEnvironment = @{}
foreach ($name in $Environment.Keys) {
    $savedEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
    [Environment]::SetEnvironmentVariable($name, [string]$Environment[$name], 'Process')
}

try {
    $argumentList = @('"' + $BridgeScript + '"')
    $process = Start-Process `
        -FilePath $nodePath `
        -ArgumentList $argumentList `
        -WorkingDirectory (Split-Path -Parent $BridgeScript) `
        -WindowStyle Hidden `
        -RedirectStandardOutput $stdoutLog `
        -RedirectStandardError $stderrLog `
        -PassThru
} finally {
    foreach ($name in $savedEnvironment.Keys) {
        [Environment]::SetEnvironmentVariable($name, $savedEnvironment[$name], 'Process')
    }
}

function Wait-HttpOk {
    param(
        [string]$Url,
        [int]$TimeoutSeconds,
        [System.Diagnostics.Process]$Process
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ($Process.HasExited) { return $false }
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) { return $true }
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
    return $false
}

$failedUrl = $null
if (-not (Wait-HttpOk -Url $healthUrl -TimeoutSeconds $HealthTimeoutSeconds -Process $process)) {
    $failedUrl = $healthUrl
} elseif ($readyUrl -and -not (Wait-HttpOk -Url $readyUrl -TimeoutSeconds $HealthTimeoutSeconds -Process $process)) {
    $failedUrl = $readyUrl
}

if ($failedUrl) {
    $stdoutTail = if (Test-Path -LiteralPath $stdoutLog) { Get-Content -LiteralPath $stdoutLog -Tail 20 } else { @() }
    $stderrTail = if (Test-Path -LiteralPath $stderrLog) { Get-Content -LiteralPath $stderrLog -Tail 20 } else { @() }
    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }
    $details = @($stdoutTail) + @($stderrTail) -join [Environment]::NewLine
    throw "Bridge did not become ready at $failedUrl within $HealthTimeoutSeconds seconds.`n$details"
}

function Write-BridgeMetadata {
    param($Data)
    $json = $Data | ConvertTo-Json -Depth 4
    [System.IO.File]::WriteAllText($PidFile, $json, (New-Object System.Text.UTF8Encoding($false)))
}

$metadata = [ordered]@{
    pid       = $process.Id
    script    = $BridgeScript
    port      = $Port
    health    = $healthUrl
    ready     = $readyUrl
    stdout    = $stdoutLog
    stderr    = $stderrLog
    startedAt = (Get-Date).ToString('o')
}
Write-BridgeMetadata -Data $metadata

if ($TargetCommand) {
    try {
        $targetPath = (Resolve-Path -LiteralPath $TargetCommand -ErrorAction Stop).Path
        $targetProcess = Start-Process -FilePath $targetPath -ArgumentList $TargetArguments -PassThru
        $metadata.targetPid = $targetProcess.Id
        $metadata.targetPath = $targetPath
        Write-BridgeMetadata -Data $metadata
    } catch {
        Write-Warning "Bridge is running (PID $($process.Id)), but the target failed to start: $($_.Exception.Message)"
        throw
    }
}

Write-Host 'Bridge started.'
Write-Host "  PID:      $($process.Id)"
Write-Host "  URL:      http://127.0.0.1:$Port"
Write-Host "  Health:   $healthUrl"
if ($readyUrl) { Write-Host "  Ready:    $readyUrl" }
Write-Host "  Logs:     $stdoutLog"
Write-Host "            $stderrLog"
Write-Host "  PID file: $PidFile"
if ($TargetCommand) {
    Write-Host "  Target:   PID $($metadata.targetPid) ($($metadata.targetPath))"
} else {
    Write-Host '  Target:   not started (pass -TargetCommand to start it)'
}
Write-Host 'Autostart is not configured.'
