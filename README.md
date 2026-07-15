# CommonSkills 项目

> **AI Agent 公共技能仓库（CommonSkills）** —— 统一管理跨 Agent 平台的共享技能（Skills），实现一处编写、多处复用。

---

## 📌 项目定位

本仓库集中管理所有可被多个 AI Agent 平台复用的技能（Skill），包括：

- **Kimi**（Work 模式 / Kimi Code IDE 插件）
- **Cursor**
- **Codex**
- **Trae**
- **Qoder**
- 以及任何支持 `~/.agents/skills/` 或 `~/.kimi/skills/` 规范的 Agent 工具

---

## 📁 目录结构

```
CommonSkills/
├── README.md                    # 本文件
├── .gitignore                   # Git 忽略规则
├── scripts/
│   └── sync-to-kimi.sh          # Kimi Work 模式复制同步脚本
│   └── setup-symlinks.ps1       # Windows 软链接批量设置脚本
├── [skill-name-1]/              # 技能目录 1
│   └── SKILL.md                 # 技能主文件（必须）
├── [skill-name-2]/              # 技能目录 2
│   ├── SKILL.md
│   └── references/              # 可选：参考资料
└── ...
```

当前共有 **62 个公共技能**，涵盖：写作、代码开发、数据分析、投研、办公自动化、PPT 生成等。

---

## 🔧 双通道 Agent 加载机制

不同 Agent 平台对技能目录的加载方式不同，本项目采用 **双通道方案**：

### 通道 A：Symbolic Link（软链接）—— 适用于 Cursor / Codex / Trae / Qoder / Kimi Code IDE

这些 Agent 平台扫描本地文件系统时**跟随软链接（Symbolic Link）**，因此采用软链接方式：

| Agent 程序 | 软链接路径 | 指向目标 |
|-----------|-----------|---------|
| Cursor / Codex / Trae / Qoder | `~/.agents/skills/<skill-name>` | `~/CommonSkills/<skill-name>` |
| Kimi Code IDE 插件 | `~/.kimi/skills/<skill-name>` | `~/CommonSkills/<skill-name>` |

**优势**：
- 实时同步：修改 `CommonSkills` 中的源文件，所有 Agent 立即生效
- 零维护：无需手动复制
- 节省磁盘空间

### 通道 B：Native Directory Copy（原生目录复制）—— 适用于 Kimi Work 模式

**Kimi 桌面客户端（Work 模式）的 `daimon` 内核在扫描技能目录时，会跳过 Symbolic Link（软链接）**。因此必须采用**原生目录复制**方式：

| Agent 程序 | 复制目标路径 | 来源 |
|-----------|-----------|------|
| Kimi Work 模式 | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/<skill-name>` | `~/CommonSkills/<skill-name>` |

**特点**：
- 需要复制（不是软链接）
- `daimon` 内核加载时视为原生技能，UI 可正常显示和调用
- 更新后需重新同步

---

## 🚀 快速开始

### 1. 首次设置（Windows）

#### 步骤 1：创建 CommonSkills 软链接（通道 A）

打开 PowerShell（管理员），运行：

```powershell
# 为 ~/.agents/skills/ 创建软链接（Cursor / Codex / Trae / Qoder）
$common = "C:\Users\$env:USERNAME\CommonSkills"
$agents = "C:\Users\$env:USERNAME\.agents\skills"

# 如果目录不存在则创建
if (-not (Test-Path $agents)) { New-Item -ItemType Directory -Path $agents }

# 遍历 CommonSkills 中所有技能，创建软链接
Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $agents $skill
    if (Test-Path $dst) { Remove-Item $dst -Force }
    New-Item -ItemType SymbolicLink -Path $dst -Target $src
}

# 同样为 ~/.kimi/skills/ 创建软链接（Kimi Code IDE 插件）
$kimi = "C:\Users\$env:USERNAME\.kimi\skills"
if (-not (Test-Path $kimi)) { New-Item -ItemType Directory -Path $kimi }
Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $kimi $skill
    if (Test-Path $dst) { Remove-Item $dst -Force }
    New-Item -ItemType SymbolicLink -Path $dst -Target $src
}
```

#### 步骤 2：复制到 Kimi Work 模式（通道 B）

```powershell
# 复制到 Kimi 桌面客户端技能目录
$common = "C:\Users\$env:USERNAME\CommonSkills"
$kimiWork = "C:\Users\$env:USERNAME\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills"

Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $kimiWork $skill
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item -Path $src -Destination $dst -Recurse
}
```

---

## 🔄 自动同步机制（Git Hook）

### 原理

通过 Git Hook 实现：当 `CommonSkills` 仓库更新（pull / merge / checkout）时，**自动触发同步脚本**，确保 Kimi Work 模式的技能目录始终与仓库最新版本一致。

### 已配置的 Hook

| Hook 类型 | 触发时机 | 作用 |
|----------|---------|------|
| `post-merge` | 执行 `git pull` 或 `git merge` 后 | 同步最新技能到 Kimi Work 模式 |
| `post-checkout` | 执行 `git checkout` 切换分支后 | 同步当前分支技能到 Kimi Work 模式 |
| `post-commit` | 执行 `git commit` 后 | 可选：同步本地修改到 Kimi Work 模式 |

### 同步脚本逻辑（`scripts/sync-to-kimi.sh`）

```bash
#!/bin/bash
# 双通道同步脚本
# 通道 A：软链接（已存在，无需操作）
# 通道 B：复制到 Kimi Work 模式目录

COMMON="C:/Users/$(whoami)/CommonSkills"
KIMI_WORK="C:/Users/$(whoami)/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills"

echo "[Sync] 开始同步 CommonSkills -> Kimi Work 模式..."

cd "$COMMON" || exit 1
for skill in */; do
    skill=${skill%/}
    src="$COMMON/$skill"
    dst="$KIMI_WORK/$skill"
    
    # 跳过非目录项和隐藏文件
    [ -d "$src" ] || continue
    [[ "$skill" == .* ]] && continue
    
    # 如果目标是软链接，先删除
    if [ -L "$dst" ]; then
        rm -f "$dst"
        echo "  [移除软链接] $skill"
    fi
    
    # 复制为原生目录
    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "  [已复制] $skill"
done

echo "[Sync] 同步完成。"
```

### 激活 Hook

```bash
# 在 CommonSkills 目录下
cd ~/CommonSkills
chmod +x scripts/sync-to-kimi.sh

# 链接 hook
cp scripts/sync-to-kimi.sh .git/hooks/post-merge
cp scripts/sync-to-kimi.sh .git/hooks/post-checkout
chmod +x .git/hooks/post-merge
chmod +x .git/hooks/post-checkout
```

---

## ➕ 新增技能的标准流程

1. **在 `CommonSkills/` 下创建新技能目录**
   ```bash
   mkdir -p ~/CommonSkills/my-new-skill
   cat > ~/CommonSkills/my-new-skill/SKILL.md << 'EOF'
   ---
   name: my-new-skill
   description: 新技能描述
   version: 1.0.0
   ---
   
   # 新技能内容
   ...
   EOF
   ```

2. **提交到 Git**
   ```bash
   cd ~/CommonSkills
   git add my-new-skill/
   git commit -m "add: my-new-skill"
   git push
   ```

3. **自动同步（Git Hook）**
   - `post-commit` / `post-merge` / `post-checkout` 会自动执行同步脚本
   - Kimi Work 模式目录会复制新增技能
   - 其他 Agent（Cursor/Codex/Trae/Qoder/KimiCodeIDE）通过软链接实时生效

4. **验证**
   - 重启 Kimi 客户端（Work 模式），搜索新技能名称
   - 在 Cursor/Codex/Trae/Qoder 中验证新技能可用
   - 重启 Kimi 客户端，搜索新技能名称
   - 在 Cursor/Codex/Trae/Qoder 中验证新技能可用

---

## 📝 各 Agent 技能目录速查

| Agent | 技能目录 | 加载方式 | 是否需要重启 |
|-------|---------|---------|------------|
| **Kimi Work 模式** | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/` | 复制（原生目录） | ✅ 需要重启客户端 |
| **Kimi Code IDE** | `~/.kimi/skills/` | 软链接 | ❌ 实时生效 |
| **Cursor** | `~/.cursor/skills/` 或 `~/.agents/skills/` | 软链接 | ❌ 实时生效 |
| **Codex** | `~/.codex/skills/` 或 `~/.agents/skills/` | 软链接 | ❌ 实时生效 |
| **Trae** | `~/.trae/skills/` 或 `~/.agents/skills/` | 软链接 | ❌ 实时生效 |
| **Qoder** | `~/.qoder/skills/` 或 `~/.agents/skills/` | 软链接 | ❌ 实时生效 |

> 注：`~/.agents/skills/` 是通用共享目录，被多个 Agent 支持。

---

## ⚠️ 已知限制与注意事项

### 1. Kimi Work 模式不支持软链接

**根本原因**：Kimi 桌面客户端的 `daimon` 内核在扫描 `daimon-share/daimon/skills/` 时，使用 `fs.readdir` 的 `withFileTypes: true` 并检查 `dirent.isSymbolicLink()`，主动跳过所有 Symbolic Link（软链接）和 Junction（目录联接）。

**验证过程**：
- `test-native-daimon`（原生目录）→ ✅ 可加载
- `cubox`（原生目录）→ ✅ 可加载
- `agently-mail`（软链接）→ ❌ 不可加载
- `backend-dev`（软链接）→ ❌ 不可加载

**结论**：只有**原生目录**（非软链接）才能被 Kimi Work 模式加载。

### 2. 配置差异

Kimi 客户端 Work 模式与 Kimi Code IDE 插件使用**不同的配置文件**：
- Kimi Code IDE 插件：`~/.kimi/config.toml`（支持 `extra_skill_dirs`）
- Kimi Work 模式：`daimon-share/daimon/runtime/kimi-code/config.toml`（`extra_skill_dirs` 可能无效）

### 3. 内置技能（builtin-skills）

Kimi 客户端打包了 34 个内置技能（`builtin-skills`），位于：
```
~/AppData/Roaming/kimi-desktop/daimon-bundle/app/daimon/assets/builtin-skills/
```
这些技能有 `builtInSkillsSha256` 校验，不建议修改。

---

## 🔧 故障排查

### 问题：Kimi Work 模式找不到某个技能

**排查步骤**：
1. 确认技能目录在 `daimon-share/daimon/skills/` 下是**原生目录**（不是软链接）
   ```bash
   ls -la ~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/<skill-name>
   # 如果显示 lrwxrwxrwx -> ...，说明是软链接，需要替换为复制
   ```
2. 确认 `SKILL.md` 的 YAML frontmatter 格式正确：
   ```yaml
   ---
   name: skill-name
   description: 技能描述
   version: 1.0.0
   ---
   ```
3. 确认技能目录名与 `SKILL.md` 中的 `name` 一致
4. 重启 Kimi 客户端

### 问题：软链接在其他 Agent 中失效

**排查步骤**：
1. 确认软链接目标路径存在
2. 确认软链接没有被破坏（如目标目录被移动或删除）
3. 重新创建软链接：
   ```bash
   rm -f ~/.agents/skills/<skill-name>
   ln -s ~/CommonSkills/<skill-name> ~/.agents/skills/<skill-name>
   ```

---

## 📚 参考文档

- [yaolifeng.com - symlink_git_personal_agent_skill](https://yaolifeng.com/shorts/symlink_git_personal_agent_skill)
- Kimi Code 官方文档：`.kimi/skills/` 和 `.agents/skills/` 目录规范
- Node.js `fs.readdir` 与 `dirent.isSymbolicLink()` 行为说明

---

## 🏷️ 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-07-15 | 初始建立，支持 Kimi/Cursor/Codex/Trae/Qoder 双通道同步 |

---

*本项目由 ZackAstra 维护，技能来源包括多个 Agent 平台内置技能和自定义技能。*
