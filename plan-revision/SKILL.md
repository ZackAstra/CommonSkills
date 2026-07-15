---
name: plan-revision
description: ⚠️ ⚠️ ⚠️ 【优先使用，不要与 plan-parse 混淆】预案修订功能：从数据库查询所有应急预案，根据规则批量检查是否需要修订，生成修订建议并发送到 Kafka！不需要 DOCX 文件！不需要解析文件！不需要 plan-parse！
---

# 预案修订检查技能

## 🚨 🚨 🚨 极其重要：与 plan-parse 的区别

| <br />    | plan-revision（此技能） | plan-parse          |
| --------- | ------------------ | ------------------- |
| **用途**    | 批量检查已有预案是否需要修订     | 解析单个 DOCX 文件并提取知识图谱 |
| **数据来源**  | 从**数据库**查询         | 从**DOCX 文件**解析      |
| **需要文件吗** | ❌ 不需要任何文件          | ✅ 需要 DOCX 文件路径      |
| **适用场景**  | "检查所有预案是否需要修订"     | "解析这个 DOCX 文件"      |

### 触发此技能的关键词

- "检查所有预案是否需要修订"
- "预案修订检查"
- "批量检查预案"
- "根据规则检查预案"

### 不要触发此技能的场景

- 不要搜索 DOCX 文件
- 不要使用 plan-parse 命令
- 不要解析文件

---

## 严格执行规范

- **规则 1：只能使用 CLI 命令**
  - ✅ 允许：使用 `planclaw revision <子命令>`
  - ❌ 禁止：直接调用 Python 函数
  - ❌ 禁止：直接使用 Python 处理
  - ❌ 禁止：使用任何非 `planclaw revision` 开头的命令

### **规则 2：只需记住 revision\_dir**

✅ 正确：只需记住 `revision_dir` 一个变量

- ❌ 错误：手动提取和记住多个路径变量
- 要求：从 `init` 输出提取 `REVISION_DIR`，后续命令只需这一个参数
- **规则 3：必须按顺序执行，不能跳步**
  - 顺序：init → load-rules → query-plans → match-rules → verify → send
  - 每步需要上一步成功完成
  - 系统自动检查前置条件
- **规则 4：使用 status 查看进度**
  - 不确定当前进度时使用 `status` 命令
- **规则 5：规则数量限制**
  - 规则最多 6 条

---

## 核心工作流程

### 步骤 1：初始化工作目录

**命令格式**

```bash
planclaw revision init [revision_dir] [--revision-id <revision_id>]
```

**参数说明**

- `[revision_dir]`：**可选**的工作目录路径。
  - 如果不传：系统会在默认目录 `~/.planclaw/work-revision` 下自动创建带时间戳的新目录 `revision-YYYYMMDDHHMMSS`
  - 如果传目录路径：
    - 如果目录名符合 `revision-YYYYMMDDHHMMSS` 格式且不存在，直接使用
    - 其他情况会在该目录下创建新的 `revision-YYYYMMDDHHMMSS` 子目录
  - 建议**直接不传参数**，让系统自动管理！

**最简单使用方式（推荐）**

```bash
# 什么都不传，系统自动在 ~/.planclaw/work-revision 下创建带时间戳的目录
planclaw revision init
```

**输出格式**

```
REVISION_DIR=<revision_dir>
REVISION_ID=<uuid>
STATE_FILE=<revision_dir>/.revision_state.json
修订工作目录初始化成功
```

**关键要求**

1. 从输出提取 `REVISION_DIR` 变量

- 后续所有命令都用这个参数

---

### 步骤 2：加载修订规则

**命令格式**

```bash
planclaw revision load-rules [<rules_path>] <revision_dir>
```

**参数说明**

- `<rules_path>`：规则 JSON 文件路径（**可选**，不提供时使用默认示例规则）
- `<revision_dir>`：修订工作目录（必须）

**说明**

- 如果 `<rules_path>` 省略，系统会自动查找并使用内置的 `example_rules.json`
- 建议第一次使用时，可以直接省略规则路径测试功能

**输出格式**

```
使用默认规则文件: <path>
RULES_FILE=<revision_dir>/rules_loaded.json
规则数量: 3
规则: 法规变更检查, 机构变更检查, 附件资源检查
规则加载成功
NEXT_STEP=query-plans
```

---

### 步骤 3：查询所有预案

**命令格式**

```bash
planclaw revision query-plans <revision_dir>
```

**说明**

- 从数据库查询所有未删除的预案
- 保存预案基本信息到 JSON 文件

**输出格式**

```
PLANS_FILE=<revision_dir>/plans_queried.json
预案数量: <count>
预案查询成功
NEXT_STEP=match-rules
```

---

### 步骤 4：匹配规则

**命令格式**

```bash
planclaw revision match-rules <revision_dir>
```

**说明**

- 基于预案元数据进行规则匹配检查
- 支持的规则类型：
  - 法规变更检查：检查 `pre_valid_date` 是否超过 1 年
  - 机构变更检查：检查 `create_time` 是否超过 2 年
  - 附件资源检查：检查 `pre_files_url` 是否为空
  - 通用检查：其他规则都会生成修订建议
- 生成修订建议（如果需要）

**输出格式**

```
MATCH_RESULTS_FILE=<revision_dir>/match_results.json
匹配完成，需要修订的预案: <count>
NEXT_STEP=verify
```

---

### 步骤 5：验证结果

**命令格式**

```bash
planclaw revision verify <revision_dir>
```

**输出格式**

```
============================================================
验证完成
待发送任务数: <count>
VERIFIED_FILE=<revision_dir>/results_verified.json
============================================================
NEXT_STEP=send
```

---

### 步骤 6：发送到 Kafka

**命令格式**

```bash
planclaw revision send <revision_dir>
```

**输出格式**

```
============================================================
发送成功
Topic: pre_revise_task
发送任务数: <count>
Task ID: <uuid>
============================================================
PIPELINE_STATUS=completed
```

---

## 查询状态命令

```bash
planclaw revision status <revision_dir>
```

---

## 使用场景

当用户想要：

1. 检查所有预案是否需要更新
2. 进行法规变更、机构变更等检查
3. 生成修订任务发送到后端

时，使用此技能。
