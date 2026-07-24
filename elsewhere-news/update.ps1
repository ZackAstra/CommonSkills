# elsewhere-news skill auto-update script
# Fetches latest SKILL.md from URL and updates local copy if version is newer

param(
    [string]$SkillUrl = "https://elsewhere.news/skill.md",
    [string]$SkillDir = "$env:USERPROFILE\CommonSkills\elsewhere-news",
    [switch]$CommitAndPush
)

$skillFile = Join-Path $SkillDir "SKILL.md"

# Fetch remote skill
try {
    $response = Invoke-WebRequest -Uri $SkillUrl -UseBasicParsing -TimeoutSec 10
    $remoteContent = $response.Content
} catch {
    Write-Warning "Failed to fetch remote skill: $_"
    exit 1
}

# Extract version from remote
if ($remoteContent -match '(?m)^version:\s*([\d.]+)') {
    $remoteVersion = [version]$Matches[1]
} else {
    Write-Warning "Could not parse version from remote skill"
    exit 1
}

# Read local version
if (Test-Path $skillFile) {
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
    Write-Host "Local skill is up-to-date (v$localVersion). Remote v$remoteVersion - no update needed."
    exit 0
}

# Update the local file
$remoteContent | Out-File -FilePath $skillFile -Encoding utf8 -Force
Write-Host "Updated elsewhere-news skill from v$($localVersion -as [string]) to v$remoteVersion"

# Also update the junction in .codex/skills (it's a junction, so it's already synced)

# Optionally commit and push to GitHub
if ($CommitAndPush) {
    Push-Location $env:USERPROFILE\CommonSkills
    git add -A
    git commit -m "auto-update: elsewhere-news skill v$remoteVersion"
    git push origin main
    Pop-Location
    Write-Host "Committed and pushed to GitHub"
}

exit 0
