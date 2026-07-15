# 用于 PowerShell 的 Windows 软链接批量设置脚本
# 设置 ~/.agents/skills/ 和 ~/.kimi/skills/ 下的软链接，指向 CommonSkills

$common = "C:\Users\$env:USERNAME\CommonSkills"

# --- 通道 A: ~/.agents/skills/ (Cursor / Codex / Trae / Qoder) ---
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
    
    # 跳过 scripts 目录
    if ($skill -eq "scripts") { return }
    
    # 如果已存在，先删除
    if (Test-Path $dst) {
        Remove-Item $dst -Force -Recurse
    }
    
    # 创建软链接
    New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
    $count++
    Write-Host "  [已创建] $skill"
}
Write-Host "  完成: $count 个技能"

# --- 通道 A: ~/.kimi/skills/ (Kimi Code IDE 插件) ---
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
    
    # 跳过 scripts 目录
    if ($skill -eq "scripts") { return }
    
    # 如果已存在，先删除
    if (Test-Path $dst) {
        Remove-Item $dst -Force -Recurse
    }
    
    # 创建软链接
    New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
    $count++
    Write-Host "  [已创建] $skill"
}
Write-Host "  完成: $count 个技能"

# --- 通道 B: Kimi Work 模式复制 ---
$kimiWork = "C:\Users\$env:USERNAME\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills"
if (-not (Test-Path $kimiWork)) {
    Write-Host ""
    Write-Host "[警告] Kimi Work 技能目录不存在，请先安装并启动 Kimi 桌面客户端"
    Write-Host "       $kimiWork"
} else {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════"
    Write-Host "  复制到 Kimi Work 模式目录（Chat 模式不受影响）"
    Write-Host "═══════════════════════════════════════════════════════"
    
    $count = 0
    Get-ChildItem $common -Directory | ForEach-Object {
        $skill = $_.Name
        $src = Join-Path $common $skill
        $dst = Join-Path $kimiWork $skill
        
        # 跳过 scripts 目录
        if ($skill -eq "scripts") { return }
        
        # 如果已存在，先删除（包括软链接）
        if (Test-Path $dst) {
            Remove-Item $dst -Force -Recurse
        }
        
        # 复制为原生目录
        Copy-Item -Path $src -Destination $dst -Recurse
        $count++
        Write-Host "  [已复制] $skill"
    }
    Write-Host "  完成: $count 个技能"
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  全部设置完成"
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "[提示] Cursor/Codex/Trae/Qoder/KimiCodeIDE 技能已生效（软链接）"
Write-Host "[提示] Kimi Work 模式需要重启客户端以加载新技能（复制）"
Write-Host ""

# 暂停显示结果（如果是双击运行）
if ($Host.Name -eq "ConsoleHost") {
    Read-Host "按 Enter 键退出..."
}
