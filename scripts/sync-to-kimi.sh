#!/bin/bash
# =============================================================================
# CommonSkills -> Kimi Work 模式 & Codex 三通道同步脚本
# =============================================================================
# 触发时机：git merge / checkout / commit 后（通过 git hook）
# 作用：
#   1. 通道 A（Junction）：Codex CLI 的 .codex/skills —— 确保所有技能有对应的 junction
#   2. 通道 B（复制）：Kimi Work 模式 —— 将 CommonSkills 中的技能复制为原生目录
#   3. 通道 C（软链接）：Cursor/Codex/Trae/Qoder/KimiCodeIDE —— 已存在，无需操作
# =============================================================================

set -e

COMMON="C:/Users/$(whoami)/CommonSkills"
CODEX_SKILLS="C:/Users/$(whoami)/.codex/skills"
KIMI_WORK="C:/Users/$(whoami)/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  CommonSkills 三通道同步启动"
echo "  时间: $(date "+%Y-%m-%d %H:%M:%S")"
echo "  来源: $COMMON"
echo "═══════════════════════════════════════════════════════"

cd "$COMMON" || { echo "[错误] 无法进入 CommonSkills 目录: $COMMON"; exit 1; }

# ============================================================
# 通道 A：确保 .codex/skills 下有对应的 junction
# 只创建不存在的 junction，绝不删除已有的
# ============================================================
echo ""
echo "--- 通道 A（Codex Junction）---"

codex_sync=0
codex_skip=0
codex_error=0

for skill in */; do
    skill=${skill%/}
    src="$COMMON/$skill"
    dst="$CODEX_SKILLS/$skill"

    [ -d "$src" ] || continue
    [[ "$skill" == .* ]] && continue
    [[ "$skill" == "scripts" ]] && continue

    # 如果目标已存在，跳过（无论是 junction 还是真实目录）
    if [ -d "$dst" ]; then
        codex_skip=$((codex_skip + 1))
        continue
    fi

    # 创建 junction（Windows 下用 cmd /c mklink /J）
    if cmd //c "mklink /J \"$dst\" \"$src\"" > /dev/null 2>&1; then
        codex_sync=$((codex_sync + 1))
        echo "  [已创建 Junction] $skill"
    else
        codex_error=$((codex_error + 1))
        echo "  [错误] 创建 Junction 失败: $skill"
    fi
done

echo "  同步: $codex_sync | 跳过: $codex_skip | 错误: $codex_error"

# ============================================================
# 通道 B：同步到 Kimi Work 目录
# ============================================================
echo ""
echo "--- 通道 B（Kimi Work）---"

if [ ! -d "$KIMI_WORK" ]; then
    echo "[跳过] Kimi Work 技能目录不存在: $KIMI_WORK"
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
            # Kimi 需要原生目录，不是软链接，删除后重建
            rm -f "$dst"
            need_sync=true
        elif [ "$src/SKILL.md" -nt "$dst/SKILL.md" ] 2>/dev/null; then
            need_sync=true
        fi

        if [ "$need_sync" = false ]; then
            kimi_skip=$((kimi_skip + 1))
            continue
        fi

        if [ -d "$dst" ]; then
            rm -rf "$dst"
        fi

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
echo ""