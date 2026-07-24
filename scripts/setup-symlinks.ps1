# 用于 PowerShell 的 Windows 多通道批量设置脚本
# 设置 ~/.agents/skills/、~/.kimi/skills/、~/.codex/skills/ 下的链接，指向 CommonSkills
# 并安装 Git hooks 实现自动同步

$common = "C:\Users\$env:USERNAME\CommonSkills"
$repoDir = $common

# ============================================================
# 通道 A1: ~/.agents/skills/ (Cursor / Codex / Trae / Qoder)
# ============================================================
$agents = "C:\Users\$env:USERNAME\.agents\skills"
if (-not (Test-Path $agents)) {
    New-Item -ItemType Directory -Path $agents -Force
    Write-Host "[创建] $agents"
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  设置 ~/.agents/skills/ 软链接 (Cursor/Codex/Trae/Qoder)"
Write-Host "═══════════════════════════════════════════════════════"

$count = 0
Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $agents $skill
    
    if ($skill -eq "scripts") { return }
    
    if (Test-Path $dst) {
        Remove-Item $dst -Force -Recurse
    }
    New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
    $count++
    Write-Host "  [已创建] $skill"
}
Write-Host "  完成: $count 个技能"

# ============================================================
# 通道 A2: ~/.kimi/skills/ (Kimi Code IDE 插件)
# ============================================================
$kimi = "C:\Users\$env:USERNAME\.kimi\skills"
if (-not (Test-Path $kimi)) {
    New-Item -ItemType Directory -Path $kimi -Force
    Write-Host "[创建] $kimi"
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  设置 ~/.kimi/skills/ 软链接 (Kimi Code IDE 插件)"
Write-Host "═══════════════════════════════════════════════════════"

$count = 0
Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $kimi $skill
    
    if ($skill -eq "scripts") { return }
    
    if (Test-Path $dst) {
        Remove-Item $dst -Force -Recurse
    }
    New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
    $count++
    Write-Host "  [已创建] $skill"
}
Write-Host "  完成: $count 个技能"

# ============================================================
# 通道 A3: ~/.codex/skills/ (Codex CLI) - 使用 Junction
# ============================================================
$codex = "C:\Users\$env:USERNAME\.codex\skills"
if (-not (Test-Path $codex)) {
    New-Item -ItemType Directory -Path $codex -Force
    Write-Host "[创建] $codex"
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  设置 ~/.codex/skills/ Junction (Codex CLI)"
Write-Host "═══════════════════════════════════════════════════════"

$count = 0
Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $codex $skill
    
    if ($skill -eq "scripts") { return }
    
    # Junction 已存在则跳过，不删除
    if (Test-Path $dst) {
        Write-Host "  [已存在] $skill"
        $count++
        return
    }
    New-Item -ItemType Junction -Path $dst -Target $src | Out-Null
    $count++
    Write-Host "  [已创建] $skill"
}
Write-Host "  完成: $count 个技能"

# ============================================================
# 通道 B: Kimi Work 模式复制
# ============================================================
$kimiWork = "C:\Users\$env:USERNAME\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills"
if (-not (Test-Path $kimiWork)) {
    Write-Host ""
    Write-Host "[警告] Kimi Work 技能目录不存在，请先安装并启动 Kimi 桌面客户端"
    Write-Host "       $kimiWork"
} else {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════"
    Write-Host "  复制到 Kimi Work 模式目录"
    Write-Host "═══════════════════════════════════════════════════════"
    
    $count = 0
    Get-ChildItem $common -Directory | ForEach-Object {
        $skill = $_.Name
        $src = Join-Path $common $skill
        $dst = Join-Path $kimiWork $skill
        
        if ($skill -eq "scripts") { return }
        
        if (Test-Path $dst) {
            Remove-Item $dst -Force -Recurse
        }
        Copy-Item -Path $src -Destination $dst -Recurse
        $count++
        Write-Host "  [已复制] $skill"
    }
    Write-Host "  完成: $count 个技能"
}

# ============================================================
# Git Hooks 安装：将 scripts/sync-to-kimi.sh 安装到 .git/hooks/
# ============================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  安装 Git Hooks"
Write-Host "═══════════════════════════════════════════════════════"

$hookSrc = Join-Path $common "scripts\sync-to-kimi.sh"
$hooksDir = Join-Path $repoDir ".git\hooks"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

$hookTypes = @("post-merge", "post-commit", "post-checkout")

if (Test-Path $hookSrc) {
    foreach ($hookType in $hookTypes) {
        $hookDst = Join-Path $hooksDir $hookType
        $content = Get-Content $hookSrc -Raw
        [System.IO.File]::WriteAllText($hookDst, $content, $utf8NoBom)
        Write-Host "  [已安装] $hookType"
    }
    Write-Host "  完成: $($hookTypes.Count) 个 hook 已安装"
} else {
    Write-Host "  [跳过] 源脚本不存在: $hookSrc"
}

# ============================================================
# 完成
# ============================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  全部设置完成"
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "[提示] Cursor/Codex/Trae/Qoder/KimiCodeIDE 技能已生效（软链接）"
Write-Host "[提示] Codex CLI 技能已生效（Junction）"
Write-Host "[提示] Kimi Work 模式需要重启客户端以加载新技能（复制）"
Write-Host ""

if ($Host.Name -eq "ConsoleHost") {
    Read-Host "按 Enter 键退出..."
}