#!/bin/bash
# =============================================================================
# CommonSkills 三通道同步脚本（Git Hook）
# =============================================================================
# 触发时机：git merge / checkout / commit 后（通过 git hook）
# 作用：
#   1. 通道 A（Junction）：Codex CLI 的 .codex/skills —— 确保所有技能有对应的 junction
#   2. 通道 B（复制）：Kimi Work 模式 —— 将 CommonSkills 中的技能复制为原生目录
#   3. 通道 C（软链接）：Cursor/Codex/Trae/Qoder/KimiCodeIDE —— 已存在，无需操作
# =============================================================================
# 异常处理：所有通道独立运行，单个通道失败不影响其他通道和 git 操作
# =============================================================================

COMMON="C:/Users/$(whoami)/CommonSkills"
CODEX_SKILLS="C:/Users/$(whoami)/.codex/skills"
KIMI_WORK="C:/Users/$(whoami)/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills"
SYNC_JUNCTIONS_SCRIPT="$COMMON/scripts/sync-junctions.ps1"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  CommonSkills 三通道同步启动"
echo "  时间: $(date "+%Y-%m-%d %H:%M:%S")"
echo "  来源: $COMMON"
echo "═══════════════════════════════════════════════════════"

# 验证来源目录
cd "$COMMON" 2>/dev/null || {
    echo "[警告] 无法进入 CommonSkills 目录: $COMMON"
    echo "同步已跳过"
    exit 0
}

# ============================================================
# 通道 A：Codex CLI 的 .codex/skills —— 使用 Junction
# 策略：优先使用 PowerShell 辅助脚本，失败则用 cmd mklink 兜底
# ============================================================
echo ""
echo "--- 通道 A（Codex Junction）---"

codex_sync=0
codex_skip=0
codex_error=0
codex_msg=""

# 方法 1：PowerShell 辅助脚本（推荐，更可靠的 Windows 集成）
if [ -f "$SYNC_JUNCTIONS_SCRIPT" ]; then
    ps_output=$(powershell -NoProfile -ExecutionPolicy Bypass -File "$SYNC_JUNCTIONS_SCRIPT" -CommonDir "$COMMON" -CodexSkillsDir "$CODEX_SKILLS" 2>&1)
    ps_exit=$?
    # 解析输出
    while IFS= read -r line; do
        echo "$line"
        # 提取统计信息
        if echo "$line" | grep -q "已创建 Junction"; then
            codex_sync=$((codex_sync + 1))
        elif echo "$line" | grep -q "\[跳过\]"; then
            codex_skip=$((codex_skip + 1))
        fi
    done <<< "$ps_output"
    # 从最后的消息中提取总数
    summary=$(echo "$ps_output" | grep -o "sync=[0-9]* skip=[0-9]* error=[0-9]*" | tail -1)
    if [ -n "$summary" ]; then
        # 从 summary 中解析，但保留我们自己的计数
        :
    fi
    if [ $ps_exit -ne 0 ]; then
        codex_msg="PowerShell method returned exit code $ps_exit"
    fi
else
    echo "  [信息] PowerShell 辅助脚本不存在，使用 cmd mklink 兜底"
    # 方法 2：cmd mklink 兜底
    for skill in */; do
        skill=${skill%/}
        src="$COMMON/$skill"
        dst="$CODEX_SKILLS/$skill"

        [ -d "$src" ] || continue
        [[ "$skill" == .* ]] && continue
        [[ "$skill" == "scripts" ]] && continue

        # 只在目标完全不存在时尝试创建
        if [ -d "$dst" ]; then
            codex_skip=$((codex_skip + 1))
            continue
        fi

        # 确保 .codex/skills 目录存在
        cmd //c "if not exist \"$CODEX_SKILLS\" mkdir \"$CODEX_SKILLS\"" > /dev/null 2>&1 || true

        if cmd //c "mklink /J \"$dst\" \"$src\"" > /dev/null 2>&1; then
            codex_sync=$((codex_sync + 1))
            echo "  [已创建 Junction] $skill"
        else
            codex_error=$((codex_error + 1))
            echo "  [跳过] $skill (无法创建 Junction，可手动运行 scripts/setup-symlinks.ps1)"
        fi
    done
fi

echo "  同步: $codex_sync | 跳过: $codex_skip | 错误: $codex_error"
[ -n "$codex_msg" ] && echo "  备注: $codex_msg"

# ============================================================
# 通道 B：同步到 Kimi Work 目录（原生目录复制，Kimi 不支持软链接）
# ============================================================
echo ""
echo "--- 通道 B（Kimi Work）---"

if [ ! -d "$KIMI_WORK" ]; then
    echo "  [跳过] Kimi Work 技能目录不存在: $KIMI_WORK"
    echo "  [提示] 请先安装并启动 Kimi 桌面客户端"
else
    kimi_sync=0
    kimi_skip=0
    kimi_error=0

    for skill in */; do
        skill=${skill%/}
        src="$COMMON/$skill"
        dst="$KIMI_WORK/$skill"

        [ -d "$src" ] || continue
        [[ "$skill" == .* ]] && continue
        [[ "$skill" == "scripts" ]] && continue

        need_sync=false
        if [ ! -d "$dst" ]; then
            need_sync=true
        elif [ -L "$dst" ]; then
            rm -f "$dst" 2>/dev/null || true
            need_sync=true
        elif [ "$src/SKILL.md" -nt "$dst/SKILL.md" ] 2>/dev/null; then
            need_sync=true
        fi

        if [ "$need_sync" = false ]; then
            kimi_skip=$((kimi_skip + 1))
            continue
        fi

        # 删除旧目标（如果存在）
        [ -d "$dst" ] && rm -rf "$dst" 2>/dev/null || true

        if cp -r "$src" "$dst" 2>/dev/null; then
            kimi_sync=$((kimi_sync + 1))
            echo "  [已同步] $skill"
        else
            kimi_error=$((kimi_error + 1))
            echo "  [错误] 同步失败: $skill"
        fi
    done

    echo "  同步: $kimi_sync | 跳过: $kimi_skip | 错误: $kimi_error"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  三通道同步完成"
echo "  通道 A（Codex Junction）: $codex_sync 同步 / $codex_skip 跳过 / $codex_error 错误"
echo "  通道 B（Kimi Work）:    $kimi_sync 同步 / $kimi_skip 跳过 / $kimi_error 错误"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "[提示] 请重启 Kimi 客户端（Work 模式）以加载新技能"
echo "[提示] 如有异常，运行 scripts/setup-symlinks.ps1 即可修复所有通道"
echo ""
# 始终以 0 退出，不阻塞 git 操作
exit 0