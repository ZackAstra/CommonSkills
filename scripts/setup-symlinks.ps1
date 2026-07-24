# CommonSkills 多通道批量设置与修复脚本
# 用法：powershell -ExecutionPolicy Bypass .\scripts\setup-symlinks.ps1
# 作用：修复所有通道，确保所有 Agent 可加载 CommonSkills 中的技能

$common = "C:\Users\$env:USERNAME\CommonSkills"
$repoDir = $common
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  CommonSkills 全通道修复工具"
Write-Host "═══════════════════════════════════════════════════════"

# ============================================================
# 通道 A1: ~/.agents/skills/ (Cursor / Codex / Trae / Qoder)
# ============================================================
$agents = "C:\Users\$env:USERNAME\.agents\skills"
if (-not (Test-Path $agents)) {
    New-Item -ItemType Directory -Path $agents -Force | Out-Null
    Write-Host "[创建] $agents"
}

Write-Host ""
Write-Host "--- 通道 A1: ~/.agents/skills/ (Cursor/Codex/Trae/Qoder) ---"

$count = 0
Get-ChildItem $common -Directory | Where-Object { $_.Name -ne 'scripts' -and $_.Name -notmatch '^\.' } | ForEach-Object {
    $skill = $_.Name
    $src = $_.FullName
    $dst = Join-Path $agents $skill
    
    if (Test-Path $dst) {
        $item = Get-Item $dst -ErrorAction SilentlyContinue
        if ($item.LinkType -eq "SymbolicLink" -and (Get-Item $dst).Target -eq $src) {
            return  # Already correct
        }
        Remove-Item $dst -Force -Recurse -ErrorAction SilentlyContinue
    }
    try {
        New-Item -ItemType SymbolicLink -Path $dst -Target $src -ErrorAction Stop | Out-Null
        Write-Host "  [已创建] $skill"
        $count++
    } catch {
        Write-Host "  [失败] $skill - $_"
    }
}
Write-Host "  完成: $count 个技能"

# ============================================================
# 通道 A2: ~/.kimi/skills/ (Kimi Code IDE 插件)
# ============================================================
$kimi = "C:\Users\$env:USERNAME\.kimi\skills"
if (-not (Test-Path $kimi)) {
    New-Item -ItemType Directory -Path $kimi -Force | Out-Null
    Write-Host "[创建] $kimi"
}

Write-Host ""
Write-Host "--- 通道 A2: ~/.kimi/skills/ (Kimi Code IDE 插件) ---"

$count = 0
Get-ChildItem $common -Directory | Where-Object { $_.Name -ne 'scripts' -and $_.Name -notmatch '^\.' } | ForEach-Object {
    $skill = $_.Name
    $src = $_.FullName
    $dst = Join-Path $kimi $skill
    
    if (Test-Path $dst) {
        $item = Get-Item $dst -ErrorAction SilentlyContinue
        if ($item.LinkType -eq "SymbolicLink" -and (Get-Item $dst).Target -eq $src) {
            return
        }
        Remove-Item $dst -Force -Recurse -ErrorAction SilentlyContinue
    }
    try {
        New-Item -ItemType SymbolicLink -Path $dst -Target $src -ErrorAction Stop | Out-Null
        Write-Host "  [已创建] $skill"
        $count++
    } catch {
        Write-Host "  [失败] $skill - $_"
    }
}
Write-Host "  完成: $count 个技能"

# ============================================================
# 通道 A3: ~/.codex/skills/ (Codex CLI) - 使用 Junction
# ============================================================
$codex = "C:\Users\$env:USERNAME\.codex\skills"
if (-not (Test-Path $codex)) {
    New-Item -ItemType Directory -Path $codex -Force | Out-Null
    Write-Host "[创建] $codex"
}

Write-Host ""
Write-Host "--- 通道 A3: ~/.codex/skills/ (Codex CLI Junction) ---"

$count = 0
Get-ChildItem $common -Directory | Where-Object { $_.Name -ne 'scripts' -and $_.Name -notmatch '^\.' } | ForEach-Object {
    $skill = $_.Name
    $src = $_.FullName
    $dst = Join-Path $codex $skill
    
    if (Test-Path $dst) {
        $item = Get-Item $dst -ErrorAction SilentlyContinue
        if ($item.LinkType -eq "Junction" -and $item.Target -eq $src) {
            Write-Host "  [已存在] $skill"
            $count++
            return  # Already correct, skip
        }
        # Wrong type or target - remove and recreate
        Remove-Item $dst -Force -Recurse -ErrorAction SilentlyContinue
    }
    try {
        New-Item -ItemType Junction -Path $dst -Target $src -ErrorAction Stop | Out-Null
        Write-Host "  [已创建] $skill"
        $count++
    } catch {
        Write-Host "  [失败] $skill - $_"
    }
}
Write-Host "  完成: $count 个技能"

# ============================================================
# 通道 B: Kimi Work 模式复制
# ============================================================
$kimiWork = "C:\Users\$env:USERNAME\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills"
if (-not (Test-Path $kimiWork)) {
    Write-Host ""
    Write-Host "--- 通道 B: Kimi Work ---"
    Write-Host "  [跳过] Kimi Work 技能目录不存在"
    Write-Host "  [提示] 请先安装并启动 Kimi 桌面客户端"
} else {
    Write-Host ""
    Write-Host "--- 通道 B: Kimi Work (原生目录复制) ---"

    $count = 0
    Get-ChildItem $common -Directory | Where-Object { $_.Name -ne 'scripts' -and $_.Name -notmatch '^\.' } | ForEach-Object {
        $skill = $_.Name
        $src = $_.FullName
        $dst = Join-Path $kimiWork $skill

        $needSync = $false
        if (-not (Test-Path $dst)) {
            $needSync = $true
        } else {
            $item = Get-Item $dst -ErrorAction SilentlyContinue
            if ($item.LinkType -eq "SymbolicLink" -or $item.LinkType -eq "Junction") {
                Remove-Item $dst -Force -Recurse -ErrorAction SilentlyContinue
                $needSync = $true
            } elseif ((Get-Item "$src\SKILL.md").LastWriteTime -gt (Get-Item "$dst\SKILL.md").LastWriteTime) {
                Remove-Item $dst -Force -Recurse -ErrorAction SilentlyContinue
                $needSync = $true
            }
        }
        
        if (-not $needSync) {
            return
        }
        
        try {
            Copy-Item -Path $src -Destination $dst -Recurse -ErrorAction Stop
            Write-Host "  [已复制] $skill"
            $count++
        } catch {
            Write-Host "  [失败] $skill - $_"
        }
    }
    Write-Host "  完成: $count 个技能"
}

# ============================================================
# Git Hooks 安装
# ============================================================
Write-Host ""
Write-Host "--- Git Hooks 安装 ---"

$hookSrc = Join-Path $common "scripts\sync-to-kimi.sh"
$hooksDir = Join-Path $repoDir ".git\hooks"
$hookTypes = @("post-merge", "post-commit", "post-checkout")

if (Test-Path $hookSrc) {
    $hookCount = 0
    foreach ($hookType in $hookTypes) {
        $hookDst = Join-Path $hooksDir $hookType
        try {
            $content = Get-Content $hookSrc -Raw -ErrorAction Stop
            [System.IO.File]::WriteAllText($hookDst, $content, $utf8NoBom)
            Write-Host "  [已安装] $hookType"
            $hookCount++
        } catch {
            Write-Host "  [失败] $hookType - $_"
        }
    }
    Write-Host "  完成: $hookCount 个 hook"
} else {
    Write-Host "  [跳过] 源脚本不存在: $hookSrc"
}

# ============================================================
# Summary
# ============================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  全通道修复完成"
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "[提示] Cursor/Codex/Trae/Qoder/KimiCodeIDE 技能已生效（软链接）"
Write-Host "[提示] Codex CLI 技能已生效（Junction）"
Write-Host "[提示] Kimi Work 模式需要重启客户端以加载新技能（复制）"
Write-Host ""

if ($Host.Name -eq "ConsoleHost") {
    Read-Host "按 Enter 键退出..."
}