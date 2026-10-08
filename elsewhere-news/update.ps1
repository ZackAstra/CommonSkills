# elsewhere-news skill auto-update script
# Fetches latest SKILL.md from URL, pulls from GitHub remote, updates local copy

param(
    [string]$SkillUrl = "https://elsewhere.news/skill.md",
    [string]$SkillDir = "$env:USERPROFILE\CommonSkills\elsewhere-news",
    [string]$RepoDir = "$env:USERPROFILE\CommonSkills",
    [switch]$CommitAndPush
)

$logDirectory = Join-Path $env:LOCALAPPDATA "ElsewhereNews"
$logPath = Join-Path $logDirectory "update.log"
$errors = [System.Collections.Generic.List[string]]::new()

function Add-UpdateError {
    param([string]$Stage, [string]$Detail)
    $errors.Add("[$Stage] $Detail")
}

function Write-UpdateLog {
    param([string]$Message)
    if (-not (Test-Path -LiteralPath $logDirectory)) {
        New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    }
    "$([DateTime]::Now.ToString('yyyy-MM-dd HH:mm:ss')) $Message" |
        Add-Content -LiteralPath $logPath -Encoding UTF8
}

function Show-UpdateErrorPopup {
    param([System.Collections.Generic.List[string]]$ErrorMessages)
    if (-not $ErrorMessages -or $ErrorMessages.Count -eq 0) {
        return
    }

    $shell = New-Object -ComObject WScript.Shell
    $shell.Popup(
        "Elsewhere News 定时更新遇到问题：`n`n" + ($ErrorMessages -join "`n`n"),
        0,
        "Elsewhere News 更新异常",
        16
    ) | Out-Null
}

try {
    # Step 1: Pull latest from GitHub remote
    Write-UpdateLog "Pulling latest from GitHub remote..."
    Push-Location -LiteralPath $RepoDir
    try {
        $pullOutput = & git pull --ff-only origin main 2>&1
        if ($LASTEXITCODE -ne 0) {
            Add-UpdateError "Git pull" ($pullOutput -join "`n")
        }
    } finally {
        Pop-Location
    }

    if ($errors.Count -gt 0) {
        throw ($errors -join "`n`n")
    }

    $skillFile = Join-Path $SkillDir "SKILL.md"

    # Step 2: Fetch remote skill from URL
    try {
        $response = Invoke-WebRequest -Uri $SkillUrl -UseBasicParsing -TimeoutSec 10
        $remoteContent = $response.Content
    } catch {
        Add-UpdateError "Fetch remote skill" $_.Exception.Message
        throw
    }

    # Extract version from remote
    if ($remoteContent -match '(?m)^version:\s*([\d.]+)') {
        $remoteVersion = [version]$Matches[1]
    } else {
        Add-UpdateError "Parse version" "Could not parse version from remote skill."
        throw
    }

    # Read local version
    if (Test-Path -LiteralPath $skillFile) {
        $localContent = Get-Content $skillFile -Raw -Encoding utf8
        if ($localContent -match '(?m)^version:\s*([\d.]+)') {
            $localVersion = [version]$Matches[1]
        } else {
            $localVersion = $null
        }
    } else {
        $localVersion = $null
    }

    # Compare versions
    if ($localVersion -and $remoteVersion -le $localVersion) {
        Write-UpdateLog "Local skill is up-to-date (v$localVersion). Remote v$remoteVersion - no update needed."
        exit 0
    }

    # Update the local file
    $remoteContent | Out-File -FilePath $skillFile -Encoding utf8 -Force
    Write-UpdateLog "Updated elsewhere-news skill from v$($localVersion -as [string]) to v$remoteVersion"

    # Optionally commit and push to GitHub
    if ($CommitAndPush) {
        Push-Location -LiteralPath $RepoDir
        try {
            $addOutput = & git add -A -- $skillFile 2>&1
            if ($LASTEXITCODE -ne 0) {
                Add-UpdateError "Git add" ($addOutput -join "`n")
                throw
            }

            & git diff --cached --quiet 2>&1 | Out-Null
            $hasChanges = ($LASTEXITCODE -eq 1)
            if ($LASTEXITCODE -gt 1) {
                Add-UpdateError "Git diff" "git diff --cached --quiet exited with $LASTEXITCODE"
                throw
            }

            if ($hasChanges) {
                $commitOutput = & git commit -m "auto-update: elsewhere-news skill v$remoteVersion" 2>&1
                if ($LASTEXITCODE -ne 0) {
                    Add-UpdateError "Git commit" ($commitOutput -join "`n")
                    throw
                }

                $pushOutput = & git push origin main 2>&1
                if ($LASTEXITCODE -ne 0) {
                    Add-UpdateError "Git push" ($pushOutput -join "`n")
                    throw
                }

                Write-UpdateLog "Committed and pushed to GitHub"
            } else {
                Write-UpdateLog "No committed changes after update"
            }
        } finally {
            Pop-Location
        }
    }

    exit 0
} catch {
    if ($errors.Count -eq 0) {
        Add-UpdateError "Update" $_.Exception.Message
    }
    Write-UpdateLog "FAILED: $(($errors -join ' | '))"
    Show-UpdateErrorPopup $errors
    exit 1
}

