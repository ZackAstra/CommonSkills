# 反向导入 TeleAgent 独有技能到 CommonSkills
# 需要管理员权限运行

$CommonSkills = "C:\Users\zhaox\CommonSkills"
$TeleAgentSkills = "C:\Users\zhaox\.config\TeleAgent\skills"

# TeleAgent 独有技能（需要导入 CommonSkills）
$teleAgentUnique = @(
    "canvas-design","contract-review","ct-ppt-generator","deep-research",
    "diagram-drawing","doc-coauthoring","doc-struct-xmind",
    "frontend-design","infographic","memory-manager","news-aggregator-skill",
    "onboarding","paddleocr-doc-parsing","ppt-aesthetics","print",
    "scheduler","session-action","telecom-ppt-writer","teleppt-pro",
    "web-artifacts-builder"
)

# CommonSkills 中已存在的同名技能（需要 Tele_ 前缀避免冲突）
$existingInCommon = @("skill-creator")

Write-Host "=== 反向导入 TeleAgent 独有技能到 CommonSkills ===" -ForegroundColor Cyan

$imported = 0
$skipped = 0

foreach ($skillName in $teleAgentUnique) {
    $sourcePath = Join-Path $TeleAgentSkills $skillName
    
    # 确定目标名称
    $targetName = $skillName
    if ($skillName -in $existingInCommon) {
        $targetName = "Tele_$skillName"
    }
    
    # 检查目标是否已存在
    $targetPath = Join-Path $CommonSkills $targetName
    if (Test-Path $targetPath) {
        Write-Host "  ⚠ 跳过 $targetName（CommonSkills 中已存在）" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    # 复制技能目录
    Copy-Item -Path $sourcePath -Destination $targetPath -Recurse -Force
    
    # 在 SKILL.md 的 frontmatter 中添加 create_source 标记
    $skillMd = Join-Path $targetPath "SKILL.md"
    if (Test-Path $skillMd) {
        $content = Get-Content $skillMd -Raw
        if ($content -match '^---\s*\n') {
            # 在 frontmatter 末尾添加 create_source
            $content = $content -replace '(^---\s*\n)(.*?)(\n---)', '$1$2' + "`ncreate_source: teleagent" + '$3'
            Set-Content $skillMd -Value $content -Force
            Write-Host "  ✓ 导入 $targetName（已添加 create_source: teleagent 标记）" -ForegroundColor Green
            $imported++
        }
    }
}

Write-Host "`n=== 完成: 导入 $imported 个, 跳过 $skipped 个 ===" -ForegroundColor Cyan
Write-Host "请执行 git add/commit 提交到 CommonSkills 仓库" -ForegroundColor Yellow
