# TeleAgent ↔ CommonSkills 双向同步初始化脚本
# 需要管理员权限运行

$CommonSkills = "C:\Users\zhaox\CommonSkills"
$TeleAgentSkills = "C:\Users\zhaox\.config\TeleAgent\skills"
$BackupDir = "C:\Users\zhaox\CommonSkills\_backup\teleagent"
$MetaFile = "C:\Users\zhaox\.local\share\TeleAgent\skills-metadata.json"

Write-Host "=== Step 1: 备份 TeleAgent 原始技能目录 ===" -ForegroundColor Cyan
if (-not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null }
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item -Path "$TeleAgentSkills\*" -Destination "$BackupDir\_backup-$timestamp" -Recurse -Force
Write-Host "  ✓ 已备份到 $BackupDir\_backup-$timestamp" -ForegroundColor Green

Write-Host "`n=== Step 2: 创建 CommonSkills → TeleAgent 的 junction 软链接 ===" -ForegroundColor Cyan
$commonSkills = Get-ChildItem $CommonSkills -Directory | Where-Object { $_.Name -notin @('.git','scripts','_backup') }
$junctionCount = 0
$skipCount = 0

foreach ($skill in $commonSkills) {
    $skillName = $skill.Name
    $csName = "CS_$skillName"
    $teleAgentPath = Join-Path $TeleAgentSkills $csName
    
    if (Test-Path $teleAgentPath) {
        Write-Host "  ⚠ 跳过 $csName（已存在）" -ForegroundColor Yellow
        $skipCount++
        continue
    }
    
    New-Item -ItemType Junction -Path $teleAgentPath -Target $skill.FullName -Force | Out-Null
    Write-Host "  ✓ 创建 junction: $csName → $skillName" -ForegroundColor Green
    $junctionCount++
}

Write-Host "`n  === 总计: 创建 $junctionCount 个 junction, 跳过 $skipCount 个 ===" -ForegroundColor Green

Write-Host "`n=== Step 3: 更新 skills-metadata.json ===" -ForegroundColor Cyan
if (Test-Path $MetaFile) {
    $meta = Get-Content $MetaFile -Raw | ConvertFrom-Json
    $updatedMeta = @{}
    $meta.PSObject.Properties | ForEach-Object { $updatedMeta[$_.Name] = $_.Value }
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    foreach ($skill in $commonSkills) {
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
            Write-Host "  ✓ 注册 $csName" -ForegroundColor Green
        }
    }
    $updatedMeta | ConvertTo-Json -Depth 5 | Set-Content $MetaFile -Force
    Write-Host "  ✓ skills-metadata.json 已更新" -ForegroundColor Green
}

Write-Host "`n=== 初始化完成! ===" -ForegroundColor Cyan
Write-Host "请重启 TeleAgent 以加载新技能" -ForegroundColor Yellow
