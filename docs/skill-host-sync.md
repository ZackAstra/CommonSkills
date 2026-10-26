# 技能宿主同步约定（Junction / 复制 / 写穿透）

本文说明 CommonSkills 与各宿主（Codex、Kimi、Cursor、Trae、Qoder、CodeFree 等）之间的技能同步约定，以及当宿主"被动更新"技能时应该怎么处理。

## 1. 单一真源原则

- 仓库 `C:\Users\zhaox\CommonSkills\<skill>\` 中的**真实文件**是唯一真源，纳入 Git。
- 各宿主技能目录**不保存独立副本**，而是通过目录 Junction 指向仓库中的技能目录。
- 因此同一个技能在所有宿主中始终是同一份内容，改一处即全局生效。

## 2. 不要在仓库内创建链接

不要在 `CommonSkills` 内部把某个技能目录做成 Junction/软链接（例如把仓库的 `kimi-webbridge/` 指向 `~/.codex/skills/kimi-webbridge`）。原因：

- Git 不记录 Junction 语义，会把链接当作普通目录递归索引进去，提交的是重复内容而不是链接。
- 换机器或重新 `git clone` 后该目录会变成实体副本，问题被复制到新环境。
- 反向链接会让"哪边是真源"变得不可判定。

正确方向只有一个：**仓库是实体目录，宿主指向仓库**。

## 3. 巡检：宿主副本是否已统一

```powershell
$hosts = @(
  "$env:USERPROFILE\.codex\skills",
  "$env:USERPROFILE\.kimi\skills",
  "$env:USERPROFILE\.openclaw\skills",
  "$env:USERPROFILE\.kimi_openclaw\workspace\skills",
  "$env:USERPROFILE\.cursor\skills",
  "$env:USERPROFILE\.qwen\skills",
  "$env:USERPROFILE\.trae\skills",
  "$env:USERPROFILE\.qoder\skills",
  "$env:USERPROFILE\.codefree\common\config\skills"
)
foreach ($h in $hosts) {
  $p = Join-Path $h 'kimi-webbridge'
  if (Test-Path $p) {
    $i = Get-Item $p -Force
    $isLink = [bool]($i.Attributes -band [IO.FileAttributes]::ReparsePoint)
    "{0} | link={1} | target={2} | readable={3}" -f $h, $isLink, $i.Target, (Test-Path (Join-Path $p 'SKILL.md'))
  }
}
```

判定标准：`link=True`、`target` 指向仓库、`readable=True`。出现 `link=False` 表示该宿主又产生了一份真实副本。

## 4. 修复：把宿主真实副本改回 Junction

真实副本先移动到备份区，再建立 Junction，**不要直接删除**：

```powershell
$repo   = 'C:\Users\zhaox\CommonSkills\kimi-webbridge'
$target = "$env:USERPROFILE\.codex\skills\kimi-webbridge"
$backup = Join-Path $env:USERPROFILE ".skill-backups\kimi-webbridge-$(Get-Date -Format yyyyMMdd-HHmmss)"

Move-Item -LiteralPath $target -Destination $backup
New-Item -ItemType Junction -Path $target -Target $repo | Out-Null
```

注意：

- 目标已存在且 `LinkType` 为 `Junction`/`SymbolicLink` 时，只能删除链接本身（`[IO.Directory]::Delete($path, $false)`），不能递归删除，否则会删掉仓库内容。
- Junction 在本机不需要管理员权限；Windows 符号链接则需要开发者模式或管理员。
- 同一技能不要同时保留 `<name>` 和 `<name>-desktop` 两个目录，避免宿主出现同名技能。

## 5. 宿主被动更新技能（写穿透）

部分宿主（如 Kimi 系）会自行下载或更新技能。若其技能目录是指向仓库的 Junction，更新会**穿透写入仓库**，表现为 `git status` 里出现无意的技能修改、`SKILL.md` frontmatter 丢失、`.fingerprint` 被删除等。历史上 `time-awareness`、`worker-safety`、`kimiim` 就因此被回退过。

两种处置方式，按影响面从小到大选择：

### 方式 A：隔离写路径（推荐）

保留"宿主读仓库"的能力，但把宿主的写目录换到独立位置，使更新只落在隔离区。

以 Kimi Code 为例（`~/.kimi-code/skills` 原本整体指向仓库根）：

1. 新建 `~/.kimi-code/skills-local`。
2. 把 `~/.kimi-code/skills` 从指向仓库根改为指向 `skills-local`。
3. 在 `~/.kimi-code/config.toml` 中保留只读加载：

   ```toml
   merge_all_available_skills = true
   extra_skill_dirs = ["C:\\Users\\zhaox\\CommonSkills"]
   ```

4. 重启宿主，确认仓库技能仍可见（可直接询问"你能看到哪些以 t 开头的技能"来验证）。

效果：宿主更新写进 `skills-local`，仓库不再被改写；技能仍然全部可读。

### 方式 B：改为复制（仅适用于明确不支持链接的宿主）

Kimi Work 模式会主动跳过 Junction（见 README「Kimi Work 模式不支持软链接」），这类宿主只能使用原生目录复制。此时该副本与仓库不再共享，需要在同步脚本中保持单向复制（仓库 → 宿主），并避免反向写回。

## 6. 提交前的检查清单

1. `git status` 中是否出现非预期的技能改动？若有，先确认来源宿主，再决定隔离该宿主或还原文件。
2. 修改的技能是否只改了内容、没有丢 frontmatter（`name` / `description`）？
3. 是否误把 `.bundle-version`、`.fingerprint`、`.env`、根目录 `*.zip` 等宿主状态或发布产物加入提交？
4. 一次提交只包含一个主题（技能内容 / 同步机制 / 文档），便于回滚。

