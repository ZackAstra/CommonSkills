<#
.SYNOPSIS
    TeleAgent ↔ CommonSkills 双向技能同步脚本
.DESCRIPTION
    维护 TeleAgent 与 CommonSkills 之间的技能双向同步：
    1. 检查并修复 CS_* junction 完整性
    2. 将 TeleAgent 新增/修改的独有技能同步回 CommonSkills
    3. 更新 TeleAgent 的 skills-metadata.json
.PARAMETER Action
    check   - 仅检查状态，不执行操作
    sync    - 执行完整同步（默认）
    restore - 从备份恢复 TeleAgent 原始技能目录
.PARAMETER TeleAgentPath
    TeleAgent 技能目录路径（默认: C:\Users\zhaox\.config\TeleAgent\skills）
.PARAMETER CommonSkillsPath
    CommonSkills 仓库路径（默认: C:\Users\zhaox\CommonSkills）
.PARAMETER MetaFilePath
    TeleAgent skills-metadata.json 路径
.EXAMPLE
    .\sync-teleagent.ps1 -Action check
    .\sync-teleagent.ps1 -Action sync
.NOTES
    需要管理员权限运行（TeleAgent .config 目录受保护）
#>

param(
    [ValidateSet('check', 'sync', 'restore')]
    [string]$Action = 'sync',
    [string]$TeleAgentSkills = "C:\Users\zhaox\.config\TeleAgent\skills",
    [string]$CommonSkills = "C:\Users\zhaox\CommonSkills",
    [string]$MetaFile = "C:\Users\zhaox\.local\share\TeleAgent\skills-metadata.json",
    [string]$BackupDir = "C:\Users\zhaox\CommonSkills\_backup\teleagent",
    [string]$TeleAgentExe = "D:\Program Files\TeleAgent\TeleAgent.exe"
)

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal]::new(
    [Security.Principal.WindowsIdentity]::GetCurrent()
)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Warning "此脚本需要管理员权限运行！"
    Write-Warning "请以管理员身份重新运行 PowerShell 并重试。"
    exit 1
}

# 检查路径
$paths = @($TeleAgentSkills, $CommonSkills, $MetaFile)
foreach ($p in $paths) {
    if (-not (Test-Path $p)) {
        Write-Error "路径不存在: $p"
        exit 1
    }
}

# 获取 CommonSkills 中的所有技能目录
$commonSkillDirs = Get-ChildItem $CommonSkills -Directory | Where-Object {
    $_.Name -notin @('.git', 'scripts', '_backup')
}

# 获取 TeleAgent 中已有的技能名称
$teleSkillDirs = Get-ChildItem $TeleAgentSkills -Directory | Select-Object -ExpandProperty Name

function Invoke-Check {
    Write-Host "=== 检查 TeleAgent ↔ CommonSkills 同步状态 ===" -ForegroundColor Cyan
    Write-Host ""

    # 检查 CS_* junction 完整性
    Write-Host "--- CS_* Junction 完整性检查 ---" -ForegroundColor Yellow
    $missingJunctions = @()
    $brokenJunctions = @()

    foreach ($skill in $commonSkillDirs) {
        $csName = "CS_$($skill.Name)"
        $junctionPath = Join-Path $TeleAgentSkills $csName

        if (-not (Test-Path $junctionPath)) {
            $missingJunctions += $csName
        } else {
            $item = Get-Item $junctionPath -Force
            if (-not ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
                $brokenJunctions += $csName
            }
        }
    }

    if ($missingJunctions.Count -eq 0) {
        Write-Host "  ✓ 所有 CS_* junction 均存在" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ 缺失 $($missingJunctions.Count) 个 junction:" -ForegroundColor Yellow
        $missingJunctions | ForEach-Object { Write-Host "    - $_" }
    }

    if ($brokenJunctions.Count -gt 0) {
        Write-Host "  ⚠ $($brokenJunctions.Count) 个 junction 已损坏:" -ForegroundColor Yellow
        $brokenJunctions | ForEach-Object { Write-Host "    - $_" }
    }

    # 检查 TeleAgent 新技能
    Write-Host ""
    Write-Host "--- TeleAgent 独有技能检查 ---" -ForegroundColor Yellow
    $teleUnique = @(
        "canvas-design","contract-review","ct-ppt-generator","deep-research",
        "diagram-drawing","doc-coauthoring","doc-struct-xmind",
        "frontend-design","infographic","memory-manager","news-aggregator-skill",
        "onboarding","paddleocr-doc-parsing","ppt-aesthetics","print",
        "scheduler","session-action","telecom-ppt-writer","teleppt-pro",
        "web-artifacts-builder"
    )

    $newSkills = @()
    $modifiedSkills = @()
    foreach ($skillName in $teleUnique) {
        $commonPath = Join-Path $CommonSkills $skillName
        $telePath = Join-Path $TeleAgentSkills $skillName
        if (-not (Test-Path $commonPath)) {
            $newSkills += $skillName
        }
    }

    if ($newSkills.Count -eq 0) {
        Write-Host "  ✓ 所有 TeleAgent 独有技能已在 CommonSkills 中" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ $($newSkills.Count) 个新技能待导入:" -ForegroundColor Yellow
        $newSkills | ForEach-Object { Write-Host "    - $_" }
    }

    return @{
        MissingJunctions = $missingJunctions
        BrokenJunctions = $brokenJunctions
        NewSkills = $newSkills
    }
}

function Invoke-Sync {
    Write-Host "=== 执行 TeleAgent ↔ CommonSkills 同步 ===" -ForegroundColor Cyan

    # 1. 修复缺失的 junction
    $missingCount = 0
    foreach ($skill in $commonSkillDirs) {
        $csName = "CS_$($skill.Name)"
        $junctionPath = Join-Path $TeleAgentSkills $csName
        if (-not (Test-Path $junctionPath)) {
            New-Item -ItemType Junction -Path $junctionPath -Target $skill.FullName -Force | Out-Null
            Write-Host "  ✓ 创建 junction: $csName" -ForegroundColor Green
            $missingCount++
        }
    }
    if ($missingCount -eq 0) {
        Write-Host "  ✓ 所有 junction 已就绪" -ForegroundColor Green
    }

    # 2. 同步 TeleAgent 独有技能到 CommonSkills
    Write-Host ""
    Write-Host "--- 同步 TeleAgent 独有技能到 CommonSkills ---" -ForegroundColor Yellow
    $teleUnique = @(
        "canvas-design","contract-review","ct-ppt-generator","deep-research",
        "diagram-drawing","doc-coauthoring","doc-struct-xmind",
        "frontend-design","infographic","memory-manager","news-aggregator-skill",
        "onboarding","paddleocr-doc-parsing","ppt-aesthetics","print",
        "scheduler","session-action","telecom-ppt-writer","teleppt-pro",
        "web-artifacts-builder"
    )

    $importedCount = 0
    $conflictSkills = @("skill-creator")  # 需要 Tele_ 前缀

    foreach ($skillName in $teleUnique) {
        $targetName = $skillName
        if ($skillName -in $conflictSkills) {
            $targetName = "Tele_$skillName"
        }

        $sourcePath = Join-Path $TeleAgentSkills $skillName
        $targetPath = Join-Path $CommonSkills $targetName

        # 检查是否需要更新 (比较 SKILL.md 的修改时间)
        $sourceMd = Join-Path $sourcePath "SKILL.md"
        $targetMd = Join-Path $targetPath "SKILL.md"

        if (-not (Test-Path $targetPath)) {
            # 新技能，复制
            Copy-Item -Path $sourcePath -Destination $targetPath -Recurse -Force
            Write-Host "  ✓ 导入 $targetName" -ForegroundColor Green
            $importedCount++
        } elseif ((Get-Item $sourceMd).LastWriteTime -gt (Get-Item $targetMd).LastWriteTime) {
            # 已修改，更新
            Copy-Item -Path $sourcePath\* -Destination $targetPath -Recurse -Force
            Write-Host "  ✓ 更新 $targetName" -ForegroundColor Green
            $importedCount++
        }
    }
    if ($importedCount -eq 0) {
        Write-Host "  ✓ 所有技能已是最新" -ForegroundColor Green
    }

    # 3. 更新 skills-metadata.json
    Write-Host ""
    Write-Host "--- 更新 skills-metadata.json ---" -ForegroundColor Yellow
    $meta = Get-Content $MetaFile -Raw | ConvertFrom-Json
    $updatedMeta = @{}
    $meta.PSObject.Properties | ForEach-Object { $updatedMeta[$_.Name] = $_.Value }

    $now = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $addedCount = 0
    foreach ($skill in $commonSkillDirs) {
        $csName = "CS_$($skill.Name)"
        $skillMdPath = "$TeleAgentSkills\$csName\SKILL.md"
        if (-not $updatedMeta.ContainsKey($csName)) {
            $updatedMeta[$csName] = @{
                source = "common-skills"
                reviewStatus = "clean"
                addedAt = $now
                updatedAt = $now
                location = $skillMdPath
            }
            $addedCount++
        }
    }
    if ($addedCount -gt 0) {
        $updatedMeta | ConvertTo-Json -Depth 5 | Set-Content $MetaFile -Force
        Write-Host "  ✓ 新增 $addedCount 个 CS_* 技能注册" -ForegroundColor Green
    } else {
        Write-Host "  ✓ skills-metadata.json 已是最新" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "=== 同步完成 ===" -ForegroundColor Cyan
    Write-Host "请重启 TeleAgent 以加载最新技能" -ForegroundColor Yellow
}

function Invoke-Restore {
    Write-Host "=== 从备份恢复 TeleAgent 原始技能目录 ===" -ForegroundColor Cyan
    $backups = Get-ChildItem $BackupDir -Directory | Sort-Object LastWriteTime -Descending
    if ($backups.Count -eq 0) {
        Write-Error "未找到备份文件"
        exit 1
    }

    $latestBackup = $backups[0].FullName
    Write-Host "  从 $latestBackup 恢复..." -ForegroundColor Yellow

    # 删除所有 CS_* junction
    Get-ChildItem $TeleAgentSkills -Directory | Where-Object { $_.Name -like 'CS_*' } | ForEach-Object {
        Remove-Item $_.FullName -Force -Recurse
        Write-Host "  ✓ 删除 junction: $($_.Name)" -ForegroundColor Green
    }

    # 恢复原始技能
    Copy-Item -Path "$latestBackup\*" -Destination $TeleAgentSkills -Recurse -Force
    Write-Host "  ✓ 恢复完成" -ForegroundColor Green
}

# 主逻辑
switch ($Action) {
    'check'  { Invoke-Check }
    'sync'   {
        $status = Invoke-Check
        if ($status.MissingJunctions.Count -gt 0 -or $status.NewSkills.Count -gt 0) {
            Invoke-Sync
        } else {
            Write-Host "所有技能已同步，无需操作。" -ForegroundColor Green
        }
    }
    'restore' { Invoke-Restore }
}
