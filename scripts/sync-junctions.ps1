# CommonSkills - Codex Junction Sync Helper
# PowerShell helper for creating/verifying junctions in .codex/skills
# Called by the bash post-merge/post-commit/post-checkout hooks

param(
    [Parameter(Mandatory)]
    [string]$CommonDir,
    
    [Parameter(Mandatory)]
    [string]$CodexSkillsDir,
    
    [string]$LogFile = ""
)

$results = @{ sync = 0; skip = 0; error = 0 }
$errors = @()

# Ensure Codex skills directory exists
if (-not (Test-Path $CodexSkillsDir)) {
    try {
        New-Item -ItemType Directory -Path $CodexSkillsDir -Force -ErrorAction Stop | Out-Null
    } catch {
        return @{ sync = 0; skip = 0; error = 0; message = "Cannot create directory: $_" }
    }
}

# Get all skill directories from CommonSkills
$skills = Get-ChildItem $CommonDir -Directory | Where-Object { 
    $_.Name -notmatch '^\.' -and $_.Name -ne 'scripts' 
}

foreach ($skill in $skills) {
    $skillName = $skill.Name
    $src = $skill.FullName
    $dst = Join-Path $CodexSkillsDir $skillName
    
    # Check if destination already exists
    if (Test-Path $dst) {
        $item = Get-Item $dst -ErrorAction SilentlyContinue
        if ($item -and $item.LinkType -eq "Junction") {
            $target = $item.Target
            if ($target -eq $src) {
                # Junction exists and points to correct location
                $results.skip++
                continue
            }
            # Wrong target - remove and recreate
            try {
                Remove-Item $dst -Force -ErrorAction Stop
            } catch {
                $results.skip++
                continue
            }
        } elseif ($item -and $item.LinkType -eq "SymbolicLink") {
            # Symbolic link - remove and create junction
            try {
                Remove-Item $dst -Force -ErrorAction Stop
            } catch {
                $results.skip++
                continue
            }
        } else {
            # Real directory - skip (don't touch user's real directories)
            $results.skip++
            continue
        }
    }
    
    # Create junction
    try {
        $null = New-Item -ItemType Junction -Path $dst -Target $src -Force -ErrorAction Stop
        $results.sync++
        Write-Host "  [已创建 Junction] $skillName"
    } catch {
        $results.error++
        $errMsg = "Junction creation failed for $skillName`: $_"
        $errors += $errMsg
        Write-Host "  [跳过] $skillName - $_"
    }
}

$results.message = "sync=$($results.sync) skip=$($results.skip) error=$($results.error)"
if ($errors.Count -gt 0) {
    $results.errors = $errors
}
return $results