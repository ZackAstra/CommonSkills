#requires -Version 5.1
<#
.SYNOPSIS
  Read-only discovery of an installed app: process, executable, command line,
  listening ports, and candidate config files.

.DESCRIPTION
  No files are modified and no config contents are read. Searches user/program
  roots with a bounded depth, plus the executable directory when a process is found.
  Use the result to locate the live profile; confirm with the app's logs/args/UI.

.EXAMPLE
  .\discover-app.ps1 -ProcessName node

.EXAMPLE
  .\discover-app.ps1 -Name opencode -MaxDepth 2 -MaxFiles 20

.EXAMPLE
  .\discover-app.ps1 -Name DSH -Roots $env:LOCALAPPDATA,$env:APPDATA -Json
#>
[CmdletBinding()]
param(
    [string]$Name,

    [string]$ProcessName,

    [string[]]$Roots,

    [int]$MaxDepth = 2,

    [int]$MaxFiles = 40,

    [switch]$Json
)

$ErrorActionPreference = 'Continue'

if (-not $Name -and -not $ProcessName) {
    throw 'Provide -Name and/or -ProcessName. Examples: -ProcessName node, -Name opencode.'
}

$notes = New-Object System.Collections.Generic.List[string]
$processRecords = New-Object System.Collections.Generic.List[object]
$portRecords = New-Object System.Collections.Generic.List[object]
$candidates = New-Object System.Collections.Generic.List[object]
$searchRoots = New-Object System.Collections.Generic.List[string]

function Add-Note {
    param([string]$Message)
    $notes.Add($Message)
}

# --- Processes -------------------------------------------------------------
try {
    $all = Get-CimInstance Win32_Process -ErrorAction Stop
    $matched = @($all | Where-Object {
        ($ProcessName -and $_.Name -like "*$ProcessName*") -or
        ($Name -and $_.CommandLine -and $_.CommandLine -like "*$Name*" -and
            $_.CommandLine -notlike "*$PSCommandPath*" -and $_.ProcessId -ne $PID)
    } | Select-Object -First 20)

    foreach ($item in $matched) {
        $processRecords.Add([pscustomobject]@{
            ProcessId      = [int]$item.ProcessId
            Name           = $item.Name
            ExecutablePath = $item.ExecutablePath
            CommandLine    = $item.CommandLine
            CreationDate   = $item.CreationDate
        })
    }
} catch {
    Add-Note "CIM process query failed: $($_.Exception.Message)"
    if ($ProcessName) {
        try {
            $fallback = @(Get-Process -Name "*$ProcessName*" -ErrorAction Stop | Select-Object -First 20)
            foreach ($item in $fallback) {
                $processRecords.Add([pscustomobject]@{
                    ProcessId      = [int]$item.Id
                    Name           = $item.ProcessName
                    ExecutablePath = $item.Path
                    CommandLine    = $null
                    CreationDate   = $item.StartTime
                })
            }
        } catch {
            Add-Note "Process fallback query failed: $($_.Exception.Message)"
        }
    }
}

if ($processRecords.Count -eq 0) {
    Add-Note 'No matching process found. The app may be stopped; file search still runs.'
}

# --- Listening ports -------------------------------------------------------
$pids = @($processRecords | ForEach-Object { $_.ProcessId })
if ($pids.Count -gt 0) {
    try {
        $listeners = @(Get-NetTCPConnection -State Listen -ErrorAction Stop |
            Where-Object { $pids -contains [int]$_.OwningProcess })
        foreach ($listener in $listeners) {
            $portRecords.Add([pscustomobject]@{
                LocalAddress = $listener.LocalAddress
                LocalPort    = [int]$listener.LocalPort
                ProcessId    = [int]$listener.OwningProcess
            })
        }
    } catch {
        Add-Note "Port query failed: $($_.Exception.Message)"
    }
}

# --- Candidate config files ------------------------------------------------
if ($Name) {
    if ($Roots) {
        foreach ($root in $Roots) {
            if ($root -and (Test-Path -LiteralPath $root)) { $searchRoots.Add((Resolve-Path -LiteralPath $root).Path) }
        }
    } else {
        foreach ($root in @($env:APPDATA, $env:LOCALAPPDATA, $env:ProgramData, $env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:USERPROFILE)) {
            if ($root -and (Test-Path -LiteralPath $root)) { $searchRoots.Add($root) }
        }
    }
    foreach ($process in $processRecords) {
        if ($process.ExecutablePath) {
            $exeDir = Split-Path -Parent $process.ExecutablePath
            if ($exeDir -and (Test-Path -LiteralPath $exeDir)) { $searchRoots.Add($exeDir) }
        }
    }

    $uniqueRoots = @($searchRoots | Select-Object -Unique)
    $excludeNames = @('node_modules', '.git', 'cache', 'logs', 'tmp', 'temp', 'crashpad', 'gpucache')
    $configExtensions = @('.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.config', '.env')
    $seen = New-Object System.Collections.Generic.HashSet[string]

    function Add-CandidateFiles {
        param([string]$Directory)

        try {
            $files = @(Get-ChildItem -LiteralPath $Directory -File -Recurse -Depth 1 -ErrorAction SilentlyContinue |
                Where-Object { $configExtensions -contains $_.Extension.ToLowerInvariant() -and $_.Length -lt 5MB } |
                Select-Object -First $MaxFiles)
        } catch {
            Add-Note "Could not list files in ${Directory}: $($_.Exception.Message)"
            return
        }

        foreach ($file in $files) {
            if ($seen.Add($file.FullName)) {
                $candidates.Add([pscustomobject]@{
                    Path          = $file.FullName
                    Name          = $file.Name
                    Extension     = $file.Extension
                    Size          = [long]$file.Length
                    LastWriteTime = $file.LastWriteTime
                    Directory     = $Directory
                })
            }
        }
    }

    foreach ($root in $uniqueRoots) {
        try {
            $matchedDirs = @(Get-ChildItem -LiteralPath $root -Directory -Recurse -Depth $MaxDepth `
                -Filter "*$Name*" -ErrorAction SilentlyContinue |
                Where-Object { $excludeNames -notcontains $_.Name.ToLowerInvariant() } |
                Select-Object -First 20)
        } catch {
            Add-Note "Could not search ${root}: $($_.Exception.Message)"
            continue
        }

        if ((Split-Path -Leaf $root) -like "*$Name*") { $matchedDirs += Get-Item -LiteralPath $root }

        foreach ($directory in ($matchedDirs | Select-Object -Unique FullName)) {
            Add-CandidateFiles -Directory $directory.FullName
        }

        # Root-level config files whose names mention the app.
        try {
            $rootFiles = @(Get-ChildItem -LiteralPath $root -File -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -like "*$Name*" -and $configExtensions -contains $_.Extension.ToLowerInvariant() -and $_.Length -lt 5MB } |
                Select-Object -First $MaxFiles)
            foreach ($file in $rootFiles) {
                if ($seen.Add($file.FullName)) {
                    $candidates.Add([pscustomobject]@{
                        Path          = $file.FullName
                        Name          = $file.Name
                        Extension     = $file.Extension
                        Size          = [long]$file.Length
                        LastWriteTime = $file.LastWriteTime
                        Directory     = $root
                    })
                }
            }
        } catch {
            Add-Note "Could not list root files in ${root}: $($_.Exception.Message)"
        }
    }
}

# --- Output ----------------------------------------------------------------
$result = [ordered]@{
    query      = [ordered]@{
        name        = $Name
        processName = $ProcessName
        roots       = @($searchRoots | Select-Object -Unique)
        maxDepth    = $MaxDepth
        maxFiles    = $MaxFiles
    }
    processes  = @($processRecords | Sort-Object ProcessId)
    ports      = @($portRecords | Sort-Object LocalPort)
    candidates = @($candidates | Sort-Object LastWriteTime -Descending | Select-Object -First $MaxFiles)
    notes      = @($notes)
}

if ($Json) {
    $result | ConvertTo-Json -Depth 6
    exit 0
}

Write-Host 'Processes:'
if ($result.processes.Count -eq 0) {
    Write-Host '  (none)'
} else {
    $result.processes | Format-Table ProcessId, Name, ExecutablePath -AutoSize | Out-String | Write-Host
    foreach ($process in $result.processes) {
        if ($process.CommandLine) { Write-Host "  [$($process.ProcessId)] $($process.CommandLine)" }
    }
}

Write-Host 'Listening ports:'
if ($result.ports.Count -eq 0) {
    Write-Host '  (none)'
} else {
    $result.ports | Format-Table LocalAddress, LocalPort, ProcessId -AutoSize | Out-String | Write-Host
}

Write-Host 'Candidate config files (read-only; contents not parsed):'
if ($result.candidates.Count -eq 0) {
    Write-Host '  (none; narrow -Roots or increase -MaxDepth)'
} else {
    $result.candidates | Format-Table LastWriteTime, Size, Path -AutoSize | Out-String | Write-Host
}

if ($result.notes.Count -gt 0) {
    Write-Host 'Notes:'
    foreach ($note in $result.notes) { Write-Host "  - $note" }
}

Write-Host 'Confirm the live profile from process arguments/logs/UI before editing.'
Write-Host 'Command lines may contain secrets; redact before sharing.'
