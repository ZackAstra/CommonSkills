#requires -Version 5.1
<#
.SYNOPSIS
  Stop a bridge started by start-bridge.ps1.

.DESCRIPTION
  Verifies that the PID belongs to the expected Node script (or target path) before
  stopping it. A missing/invalid PID file falls back to the listener on -Port only
  when -Force is supplied. Never kills an unverified process without -Force.

.EXAMPLE
  .\stop-bridge.ps1

.EXAMPLE
  .\stop-bridge.ps1 -Port 8787 -Force
#>
[CmdletBinding()]
param(
    [string]$PidFile,

    [int]$Port = 0,

    [switch]$IncludeTarget,

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

if (-not $PidFile) {
    $stateRoot = if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'a2a-reproxy' } else { $PSScriptRoot }
    $PidFile = Join-Path $stateRoot 'bridge.pid'
}
$PidFile = [System.IO.Path]::GetFullPath($PidFile)

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

function Get-ProcessCommandLine {
    param([int]$ProcessId)
    try {
        $info = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction Stop
        return $info.CommandLine
    } catch {
        return $null
    }
}

function Stop-VerifiedProcess {
    param(
        [int]$ProcessId,
        [string]$ExpectedPath,
        [string]$Label,
        [switch]$AllowUnverified
    )

    $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
    if (-not $process) {
        Write-Host "$Label PID $ProcessId is not running."
        return $true
    }

    if ($ExpectedPath) {
        $commandLine = Get-ProcessCommandLine -ProcessId $ProcessId
        if (-not $commandLine) {
            if (-not $AllowUnverified) {
                throw "Cannot verify $Label PID $ProcessId (command line unavailable). Re-run with -Force if you are certain."
            }
        } elseif ($commandLine.IndexOf($ExpectedPath, [System.StringComparison]::OrdinalIgnoreCase) -lt 0) {
            if (-not $AllowUnverified) {
                throw "$Label PID $ProcessId does not match '$ExpectedPath'. Refusing to stop it. Re-run with -Force if you are certain."
            }
            Write-Warning "$Label PID $ProcessId does not match '$ExpectedPath'; stopping because -Force was supplied."
        }
    } elseif (-not $AllowUnverified) {
        throw "No expected path for $Label PID $ProcessId. Re-run with -Force if you are certain."
    }

    Stop-Process -Id $ProcessId -ErrorAction Stop
    $deadline = (Get-Date).AddSeconds(10)
    while ((Get-Date) -lt $deadline) {
        if (-not (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue)) { break }
        Start-Sleep -Milliseconds 250
    }
    if (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue) {
        if (-not $Force) {
            throw "$Label PID $ProcessId did not stop within 10 seconds. Re-run with -Force."
        }
        Stop-Process -Id $ProcessId -Force -ErrorAction Stop
        Start-Sleep -Milliseconds 500
        if (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue) {
            throw "$Label PID $ProcessId could not be force-stopped."
        }
        Write-Host "$Label PID $ProcessId force-stopped."
    } else {
        Write-Host "$Label PID $ProcessId stopped."
    }
    return $true
}

$metadata = $null
if (Test-Path -LiteralPath $PidFile) {
    try {
        $metadata = Get-Content -LiteralPath $PidFile -Raw | ConvertFrom-Json
    } catch {
        Write-Warning "Could not parse PID file: $PidFile"
    }
}

$bridgePid = $null
$bridgePath = $null
$targetPid = $null
$targetPath = $null
$effectivePort = $Port

if ($metadata) {
    if ($metadata.pid) { $bridgePid = [int]$metadata.pid }
    if ($metadata.script) { $bridgePath = [string]$metadata.script }
    if ($metadata.targetPid) { $targetPid = [int]$metadata.targetPid }
    if ($metadata.targetPath) { $targetPath = [string]$metadata.targetPath }
    if (-not $effectivePort -and $metadata.port) { $effectivePort = [int]$metadata.port }
}

$allowUnverified = [bool]$Force

if (-not $bridgePid -and $effectivePort -gt 0) {
    $listenerPid = Get-ListeningProcessId -PortNumber $effectivePort
    if ($listenerPid) {
        Write-Host "No usable PID file; found listener PID $listenerPid on port $effectivePort."
        $bridgePid = $listenerPid
        $bridgePath = $null
        if (-not $Force) {
            throw "Refusing to stop listener PID $listenerPid without verification. Re-run with -Force if you are certain."
        }
    }
}

if (-not $bridgePid) {
    if (Test-Path -LiteralPath $PidFile) { Remove-Item -LiteralPath $PidFile -Force }
    Write-Host 'Bridge is not running (no PID file and no listener).'
    exit 0
}

if ($IncludeTarget -and $targetPid) {
    Stop-VerifiedProcess -ProcessId $targetPid -ExpectedPath $targetPath -Label 'Target' -AllowUnverified:$allowUnverified | Out-Null
}

Stop-VerifiedProcess -ProcessId $bridgePid -ExpectedPath $bridgePath -Label 'Bridge' -AllowUnverified:$allowUnverified | Out-Null

if (Test-Path -LiteralPath $PidFile) { Remove-Item -LiteralPath $PidFile -Force }
Write-Host 'Bridge stopped.'
