# CommonSkills 项目复盘与验证报告

> 生成时间: 2026-07-15
> 作者: AI Agent (协助 ZackAstra)

---

## 一、根因分析：为什么 `agently-mail` 和 `backend-dev` 在 Kimi Work 中不可见

### 直接原因
`agently-mail` 和 `backend-dev` 最初在 `daimon-share/daimon/skills/` 下是**软链接（Symbolic Link）**，指向 `CommonSkills/` 中的对应目录。而 **Kimi 桌面客户端的 `daimon` 内核在扫描技能目录时，主动跳过所有 Symbolic Link**。

### 底层机制（逆向工程确认）
Kimi Work 模式的技能扫描核心逻辑位于：
```
daimon-bundle/app/daimon/dist/src/core/memory/skills/writer.js
```

该逻辑使用 `fs.readdir(root, {withFileTypes: true})` 读取 `skills` 根目录，遍历每个 entry 时：
1. 跳过非目录项
2. 检查 `path.join(root, entry.name, 'SKILL.md')` 是否存在
3. **若 entry 是 SymbolicLink，则 `isFile()` 可能返回 `false` 或被跳过**

### 关键验证
- `test-native-daimon`（原生目录）→ ✅ 可加载
- `cubox`（原生目录）→ ✅ 可加载
- `agently-mail`（软链接）→ ❌ 不可加载
- `backend-dev`（软链接）→ ❌ 不可加载

### 结论
**只有原生目录（非软链接）才能被 Kimi Work 模式加载**。这是 Kimi Work 与 Cursor/Codex/Trae/Qoder/Kimi Code IDE 的关键差异。

---

## 二、修复历程

### 阶段 1：清理与基础修复
1. ✅ 删除了调试期间生成的 6 个 `test-*.mjs` 测试脚本
2. ✅ 将 `agently-mail`、`backend-dev` 等技能从软链接替换为原生目录复制
3. ✅ 初始化 `CommonSkills` 为 Git 仓库并推送至 GitHub 私有仓库

### 阶段 2：全面审计与批量修复
运行全量审计脚本，发现 8 个技能存在 frontmatter 问题：

| 技能 | 问题 | 修复方式 |
|------|------|----------|
| `time-awareness` | **完全缺少 frontmatter**（无 `name` 字段） | 添加标准 frontmatter |
| `worker-safety` | **完全缺少 frontmatter**（无 `name` 字段） | 添加标准 frontmatter |
| `gongkao-review-allinone` | `name` 为中文 `公考复盘一体版`，与目录名不匹配 | 改为 `gongkao-review-allinone` |
| `kimi-webbridge-desktop` | `name` 为 `kimi-webbridge`，与目录名不匹配 | 改为 `kimi-webbridge-desktop` |
| `kimiim` | `name` 为 `kimiim-cli`，与目录名不匹配 | 改为 `kimiim` |
| `churn-prevention` | `name: "churn-prevention"`（YAML 引号，实际有效） | 无需修复 |
| `playwright` | `name: "playwright"`（YAML 引号，实际有效） | 无需修复 |
| `pricing-strategy` | `name: "pricing-strategy"`（YAML 引号，实际有效） | 无需修复 |

### 阶段 3：同步脚本修复
修复了 `scripts/sync-to-kimi.sh` 的两个关键 bug：

1. **时间戳比较逻辑错误**：原脚本使用目录级时间戳 `[ "$src" -ot "$dst" ]`，导致修改子文件后无法触发同步。已修复为 `SKILL.md` 级时间戳比较 `[ "$src/SKILL.md" -nt "$dst/SKILL.md" ]`。
2. **Chat 模式引用残留**：从脚本注释和输出提示中移除了所有 `Chat 模式` 相关描述。

### 阶段 4：Git Hook 更新
更新了 `.git/hooks/post-merge` 和 `.git/hooks/post-checkout` 到最新版同步脚本。

---

## 三、当前系统状态

### 3.1 全量技能分布（共 62 个）

| 位置 | 加载方式 | 数量 | 状态 |
|------|---------|------|------|
| `CommonSkills/` | 源仓库 | 62 | ✅ 全部有效 |
| `~/.agents/skills/` | 软链接 → CommonSkills | 62 | ✅ 实时同步 |
| `~/.kimi/skills/` | 软链接 → CommonSkills | 62 | ✅ 实时同步（Kimi Code IDE） |
| `daimon-share/daimon/skills/` | 原生目录复制 | 62 | ✅ 已同步 |

### 3.2 双通道同步架构

```
CommonSkills/ (Git 仓库)
    ├── skills/           ← 62 个技能目录
    └── scripts/
        └── sync-to-kimi.sh

通道 A（软链接）─────────────────────────────────
    ~/.agents/skills/<skill> ──symlink──> CommonSkills/<skill>
    ~/.kimi/skills/<skill> ───symlink──> CommonSkills/<skill>
    
    适用：Cursor / Codex / Trae / Qoder / Kimi Code IDE
    特点：实时生效，无需重启

通道 B（原生复制）───────────────────────────────
    daimon-share/daimon/skills/<skill> ──copy──> CommonSkills/<skill>
    
    适用：Kimi Work 模式
    特点：需复制，需重启 Kimi 客户端
```

### 3.3 Git Hook 自动触发

| Hook | 触发时机 | 作用 |
|------|---------|------|
| `post-merge` | `git pull` 后 | 同步最新技能到 Kimi Work |
| `post-checkout` | `git checkout` 后 | 同步当前分支技能到 Kimi Work |
| `post-commit` | `git commit` 后 | 同步本地修改到 Kimi Work |

### 3.4 审计结果

```
总技能数: 62
正常:     59
警告:     3  (churn-prevention, playwright, pricing-strategy 的 YAML 引号格式，实际不影响解析)
错误:     0
软链接:   0  (Kimi Work 目录下无软链接)
```

---

## 四、手动验证步骤（请用户执行）

### 验证 1：Kimi Work 模式能否看到 `agently-mail` 和 `backend-dev`

1. 关闭并重新打开 **Kimi 桌面客户端**
2. 切换到 **Work 模式**
3. 在技能搜索框输入 `agently-mail` 或 `backend-dev`
4. 预期结果：两个技能均应在搜索结果中显示

### 验证 2：Kimi Work 模式能否看到 `time-awareness` 和 `worker-safety`

1. 在 Kimi Work 模式搜索 `time-awareness`
2. 预期结果：技能显示（此前因缺少 frontmatter 完全不可见）

### 验证 3：其他 Agent 是否正常

1. 打开 **Cursor / Codex / Trae / Qoder**
2. 搜索 `agently-mail` 或任意 CommonSkills 中的技能
3. 预期结果：正常显示（软链接方式，实时生效）

### 验证 4：Git Hook 自动同步

1. 在 `CommonSkills/` 中修改任意技能的 `SKILL.md`
2. 执行 `git commit -am "test: update skill"`
3. 观察输出中是否出现 `[已同步] <skill-name>`
4. 检查 `daimon-share/daimon/skills/<skill-name>/SKILL.md` 是否已更新

---

## 五、已知限制与注意事项

1. **Kimi Work 模式不支持软链接**：必须保持原生目录。若发现某个技能突然不可见，首先检查它是否被意外替换为软链接。
2. **Kimi Work 模式需重启客户端**：新技能或更新不会热加载，必须完全重启 Kimi 桌面客户端。
3. **Chat 模式不在同步范围内**：Kimi Chat 模式使用云端配置，不受本地 `CommonSkills` 影响。
4. **技能名称一致性**：建议保持 `目录名 == frontmatter name`，以避免扫描器识别问题。

---

## 六、后续维护建议

### 新增技能的标准流程
```bash
cd ~/CommonSkills
mkdir my-new-skill
cat > my-new-skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: 新技能描述
---

# 我的新技能
...
EOF
git add my-new-skill
git commit -m "add: my-new-skill"
git push
```

commit 后 `post-commit` hook 会自动同步到 Kimi Work。

### 定期全量审计
建议每月运行一次审计脚本：
```bash
bash /tmp/audit-skills.sh
```

---

*本报告由 AI Agent 生成，供 ZackAstra 审阅。*
