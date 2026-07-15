#!/bin/bash
# =============================================================================
# CommonSkills -> Kimi Work/Chat 双通道同步脚本
# =============================================================================
# 触发时机：git merge / checkout / commit 后（通过 git hook）
# 作用：
#   1. 通道 A（软链接）：Cursor/Codex/Trae/Qoder/KimiCodeIDE —— 已存在，无需操作
#   2. 通道 B（复制）：Kimi Work/Chat —— 将 CommonSkills 中的技能复制为原生目录
# =============================================================================

set -e

COMMON="C:/Users/$(whoami)/CommonSkills"
KIMI_WORK="C:/Users/$(whoami)/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  CommonSkills 双通道同步启动"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "  来源: $COMMON"
echo "  目标: $KIMI_WORK"
echo "═══════════════════════════════════════════════════════"

# 验证来源目录
cd "$COMMON" || { echo "[错误] 无法进入 CommonSkills 目录: $COMMON"; exit 1; }

# 确保目标目录存在
if [ ! -d "$KIMI_WORK" ]; then
    echo "[错误] Kimi Work 技能目录不存在: $KIMI_WORK"
    echo "[提示] 请确保 Kimi 桌面客户端已安装并至少启动过一次"
    exit 1
fi

sync_count=0
skip_count=0
error_count=0

for skill in */; do
    skill=${skill%/}
    src="$COMMON/$skill"
    dst="$KIMI_WORK/$skill"
    
    # 跳过非目录项
    [ -d "$src" ] || continue
    
    # 跳过隐藏目录和脚本目录
    [[ "$skill" == .* ]] && continue
    [[ "$skill" == "scripts" ]] && continue
    
    # 跳过 README 等文件（非目录项已在上面过滤）
    [ -f "$src" ] && continue
    
    # 检查目标是否已经是原生目录（非软链接）
    if [ -d "$dst" ] && [ ! -L "$dst" ]; then
        # 比较修改时间，如果源文件未更新则跳过
        if [ "$src" -ot "$dst" ] 2>/dev/null; then
            skip_count=$((skip_count + 1))
            continue
        fi
    fi
    
    # 如果目标是软链接，先删除
    if [ -L "$dst" ]; then
        rm -f "$dst"
        echo "  [移除软链接] $skill"
    fi
    
    # 如果目标目录存在，先删除（确保干净复制）
    if [ -d "$dst" ]; then
        rm -rf "$dst"
    fi
    
    # 复制为原生目录
    if cp -r "$src" "$dst" 2>/dev/null; then
        sync_count=$((sync_count + 1))
        echo "  [已同步] $skill"
    else
        error_count=$((error_count + 1))
        echo "  [错误] 同步失败: $skill"
    fi
done

echo "───────────────────────────────────────────────────────"
echo "  同步完成: $sync_count 个技能已同步"
echo "  跳过:     $skip_count 个技能（无需更新）"
echo "  错误:     $error_count 个技能"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "[提示] 请重启 Kimi 客户端（Work/Chat 模式）以加载新技能"
echo "[提示] Cursor/Codex/Trae/Qoder/KimiCodeIDE 通过软链接实时生效，无需重启"
echo ""
