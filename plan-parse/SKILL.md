---
name: plan-parse
description: 使用 planclaw parser CLI 命令解析中文应急预案文档并提取结构化知识图谱数据，最后发送到Kafka。系统使用状态文件自动管理流水线,智能体只需记住 parser_dir 路径。系统会使用完整文档内容进行实体提取,确保不遗漏Person、FamilyHousehold等实体。当用户需要解析应急预案DOCX文件、提取实体构建知识图谱并推送到Kafka时使用此技能。
---

# 应急预案解析技能 (Plan Parse)

解析中文应急预案文档（应急预案）为结构化知识图谱数据，遵循预定义的schema，并将结果发送到Kafka。

## 🚨 严格执行规范

**本技能要求智能体必须严格遵守以下规则，违反任何一条都视为执行失败：**

### 规则1：只能使用 CLI 命令
- ✅ **允许**：使用 `planclaw parser <subcommand>` 命令
- ❌ **禁止**：直接调用 Python 函数（如 `extract_entities()`, `build_relations()`）
- ❌ **禁止**：使用 Python 脚本处理数据
- ❌ **禁止**：使用任何非 `planclaw parser` 的命令

### 规则2：只需记住 parser_dir
- ✅ **正确**：只需记住一个变量 `parser_dir`
- ✅ **正确**：所有中间文件路径由系统自动管理
- ❌ **错误**：手动提取和记住多个路径变量
- **要求**：从 `init` 命令输出提取 `PARSER_DIR`，后续命令只需这一个参数

### 规则3：必须按顺序执行，不能跳步
- 执行顺序：init → download → convert → load-schema → extract-entities → build-relations → verify → send
- 每一步必须等待上一步成功完成后才能执行
- 系统会自动检查前置条件，如果跳步会报错
- send 步骤支持重试（最多3次），如果Kafka发送失败可以直接重试

### 规则4：使用 status 命令查看进度
- 如果不确定当前进度，使用 `planclaw parser status <parser_dir>`
- status 命令会显示当前状态和下一步建议
- 失败的步骤可以直接重试

### 规则5：禁止使用不存在的命令
- ❌ **禁止**：`planclaw parser validate`（不存在）
- ❌ **禁止**：`planclaw parser export`（不存在）
- ❌ **禁止**：`planclaw parser schema`（不存在）
- ✅ **允许**：只能使用本文档明确列出的命令

## 概述

本技能指导你通过 **8步流水线** 解析应急预案DOCX文档并发送到Kafka：

```
init: 初始化工作目录
  ↓
download: 下载文档
  ↓
convert: 转换为Markdown
  ↓
load-schema: 加载Schema
  ↓
extract-entities: 提取实体
  ↓
build-relations: 构建关系
  ↓
verify: 验证结果
  ↓
send: 发送到Kafka
```

系统使用 `.pipeline_state.json` 自动追踪流水线状态，智能体只需记住 `parser_dir` 路径。

## 核心工作流程

### 步骤0：初始化工作目录

**命令格式**：
```bash
planclaw parser init <parser_dir> [--file-id <file_id>]
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径（必需）
- `--file-id`：文件唯一标识符（可选，不提供时自动生成UUID）

**输出格式**：
```
PARSER_DIR=<parser_dir>
FILE_ID=<uuid>
STATE_FILE=<parser_dir>/.pipeline_state.json
Parser directory initialized successfully
```

**关键要求**：
- 必须从输出中提取 `PARSER_DIR=` 后面的完整路径
- 系统会自动生成UUID作为 `FILE_ID`（如果未提供）
- 后续所有命令都必须使用这个路径作为参数
- 状态文件会自动创建在 `<parser_dir>/.pipeline_state.json`

**示例**：
```bash
planclaw parser init C:\Users\xxx\.planclaw\parser-dongan
# 输出: 
# PARSER_DIR=C:\Users\xxx\.planclaw\parser-dongan
# FILE_ID=76aec2d4-1933-43e9-94e2-a8187d72ebd9
# 记住: parser_dir=C:\Users\xxx\.planclaw\parser-dongan
```

---

### 步骤1：下载文档

**命令格式**：
```bash
planclaw parser download <input_path> <parser_dir>
```

**参数说明**：
- `<input_path>`：输入DOCX文件的完整路径
- `<parser_dir>`：从步骤0提取的 PARSER_DIR

**输出格式**：
```
DOCX_PATH=<parser_dir>/source.docx
FILE_SIZE=<size_in_bytes>
NEXT_STEP=convert
Document downloaded successfully
```

**关键要求**：
- 输出中的 `NEXT_STEP` 提示下一步应该执行的命令
- 无需记住 DOCX_PATH，系统会自动管理

**示例**：
```bash
planclaw parser download "D:\预案\东安县横塘防洪预案.docx" $parser_dir
# 输出: NEXT_STEP=convert
```

---

### 步骤2：转换为Markdown

**命令格式**：
```bash
planclaw parser convert <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**输出格式**：
```
MARKDOWN_PATH=<parser_dir>/source.md
NEXT_STEP=load-schema
Document converted successfully
```

**关键要求**：
- 只需提供 parser_dir，系统自动从状态文件读取 docx_path
- 无需记住 MARKDOWN_PATH

**示例**：
```bash
planclaw parser convert $parser_dir
# 输出: NEXT_STEP=load-schema
```

---

### 步骤3：加载Schema

**命令格式**：
```bash
planclaw parser load-schema <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**输出格式**：
```
SCHEMA_FILE=<parser_dir>/schema.json
ENTITY_COUNT=<number>
NEXT_STEP=extract-entities
Schema loaded successfully
```

**关键要求**：
- 只需提供 parser_dir，系统自动从状态文件读取 markdown_path
- 无需记住 SCHEMA_FILE

**示例**：
```bash
planclaw parser load-schema $parser_dir
# 输出: NEXT_STEP=extract-entities
```

---

### 步骤4：提取实体

**命令格式**：
```bash
planclaw parser extract-entities <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**输出格式**：
```
Loading schema from: <schema_path>
Initializing Anthropic client...
Starting entity extraction...
Processing batch_1: EmergencyPlan, Region, ...
Processing batch_2: ...
Processing batch_3: ...
Processing batch_4_groups_persons: WorkGroup, Person
  Extracting Person in batches...
    Batch: 指挥部人员
      LLM response length: 1234 chars
      Extracted 5 persons
    Batch: 县级责任人
      LLM response length: 2345 chars
      Extracted 8 persons
    ...
  Total Person entities extracted: 45
Processing batch_5: FamilyHousehold
  Extracting FamilyHousehold in batches...
    Batch 1/3 (length: 45000 chars)
      LLM response length: 3456 chars
      Extracted 12 households
    ...
  Total FamilyHousehold entities extracted: 38
...
ENTITIES_FILE=<parser_dir>/entities_extracted.json
Total entities: <number>
Entity types: <number>
Entity extraction completed successfully
NEXT_STEP=build-relations
```

**关键要求**：
- 只需提供 parser_dir，系统自动从状态文件读取所需路径
- 无需记住 ENTITIES_FILE
- **此步骤耗时较长**（需要调用LLM），建议在后台运行
- **Person和FamilyHousehold实体使用分批提取**：
  - Person按6个角色类别分批（指挥部人员、县级/乡镇级/村级/组级责任人、其他人员）
  - FamilyHousehold按文档章节分批（每批最多50000字符）
  - 每个批次独立调用LLM，避免响应被截断
  - 单批次失败不影响其他批次
- **调试文件**：系统会自动保存LLM响应到 `<parser_dir>/debug_*_response.json` 文件
- Windows系统会自动设置UTF-8编码以支持中文输出
- **系统会使用完整文档内容进行提取**，确保不遗漏任何实体
- Person实体会从文档中的人员表格、责任人名单等处提取
- FamilyHousehold会提取所有住户信息，包括姓名、地址、电话、人数等

**后台运行建议**：
```bash
# 由于此步骤耗时较长（可能需要5-15分钟），建议使用后台任务
# 系统会在完成后通知你
```

**示例**：
```bash
planclaw parser extract-entities $parser_dir
# 输出: NEXT_STEP=build-relations
```

---

### 步骤5：构建关系

**命令格式**：
```bash
planclaw parser build-relations <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**输出格式**：
```
RELATIONS_FILE=<parser_dir>/relations_built.json
Total relations: <number>
Relation building completed successfully
NEXT_STEP=verify
```

**关键要求**：
- 只需提供 parser_dir，系统自动从状态文件读取所需路径
- 无需记住 RELATIONS_FILE
- **此步骤耗时较长**（需要调用LLM），建议在后台运行
- Windows系统会自动设置UTF-8编码以支持中文输出

**示例**：
```bash
planclaw parser build-relations $parser_dir
# 输出: NEXT_STEP=verify
```

---

### 步骤6：验证结果

**命令格式**：
```bash
planclaw parser verify <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**功能说明**：
- 验证并去重实体数据（基于schema配置的dedup_keys）
- 验证并去重关系数据（基于三元组：head名称、relation、tail名称）
- 检查schema约束（unique、limit）
- 生成验证后的数据文件（entities_validated.json, relations_validated.json）
- 输出详细的验证报告（去重统计、约束违规）

**输出格式**：
```
============================================================
Parsing Results Verification
============================================================
Parser Directory: <parser_dir>

Entities:
  Original: <number>
  Validated: <number>
  Duplicates removed: <number>

Relations:
  Original: <number>
  Validated: <number>
  Duplicates removed: <number>

Entity Deduplication Details:
  - Person: 150 → 120 (-30)
  - FamilyHousehold: 80 → 75 (-5)
  ...

Unique Constraint Violations (merged):
  - EmergencyPlan: found 2, merged into 1

Relation Constraint Violations:
  - EmergencyPlan.hasCommander: limit: 1, found 2 [warning]

Validated files saved:
  - <parser_dir>/entities_validated.json
  - <parser_dir>/relations_validated.json
============================================================
Verification completed successfully
NEXT_STEP=send
```

**关键要求**：
- 只需提供 parser_dir，系统自动从状态文件读取所需路径
- 验证成功后生成 entities_validated.json 和 relations_validated.json
- send 命令会优先使用验证后的文件
- 验证成功后，下一步是 send（发送到Kafka）

**示例**：
```bash
planclaw parser verify $parser_dir
# 输出: NEXT_STEP=send
```

---

### 步骤7：发送到Kafka

**命令格式**：
```bash
planclaw parser send <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**输出格式**：
```
============================================================
Sending Relations to Kafka
============================================================
Parser Directory: <parser_dir>
Thread ID: <thread_id>
Total Relations: <number>
Regions: <region_list>
Topic: <kafka_topic>
============================================================
Successfully sent message to Kafka
PIPELINE_STATUS=completed
```

**关键要求**：
- 只需提供 parser_dir，系统自动从状态文件读取所需信息
- 支持失败重试：如果发送失败，可以重新运行此命令（最多3次）
- 发送成功后，整个流水线标记为 completed

**示例**：
```bash
planclaw parser send $parser_dir
# 输出: PIPELINE_STATUS=completed
```

---

### 查询状态

**命令格式**：
```bash
planclaw parser status <parser_dir>
```

**参数说明**：
- `<parser_dir>`：解析器工作目录路径

**输出格式**：
```
============================================================
Pipeline Status
============================================================
File ID: <id>
Status: in_progress
Current Step: 2 (convert)

Step Details:
------------------------------------------------------------
[✓] init (completed)
  Started: 2024-01-01 10:00:00
  Completed: 2024-01-01 10:00:01

[✓] download (completed)
  Started: 2024-01-01 10:00:02
  Completed: 2024-01-01 10:00:05
  Inputs: input_path=/path/to/input.docx
  Outputs: docx_path=/path/to/source.docx, file_size=12345

[→] convert (in_progress)
  Started: 2024-01-01 10:00:06

[ ] load_schema (pending)
[ ] extract_entities (pending)
[ ] build_relations (pending)
[ ] verify (pending)

============================================================
Next Step: Wait for convert to complete, then run load-schema
NEXT_STEP=load-schema
```

**关键要求**：
- 使用此命令查看当前进度和下一步建议
- 如果某步失败，会显示错误信息
- 失败的步骤可以直接重试

---

## 智能体使用指南

### 关键原则

**只需记住一个变量**: `parser_dir`

所有中间文件路径（docx_path, markdown_path, schema_file, entities_file, relations_file）由系统自动管理，无需手动提取和记住。

### 典型执行流程

```bash
# 1. 初始化并记住 parser_dir
planclaw parser init /path/to/parser
# 记住: parser_dir=/path/to/parser

# 2. 下载文档
planclaw parser download /path/to/input.docx $parser_dir

# 3-8. 后续命令只需 parser_dir
planclaw parser convert $parser_dir
planclaw parser load-schema $parser_dir
planclaw parser extract-entities $parser_dir
planclaw parser build-relations $parser_dir
planclaw parser verify $parser_dir
planclaw parser send $parser_dir
```

### 错误恢复

如果某步失败：

1. 使用 `planclaw parser status $parser_dir` 查看当前状态
2. 查看失败步骤的错误信息
3. 直接重试失败的命令（系统会自动检查前置条件）

示例：
```bash
# 如果 extract-entities 失败
planclaw parser status $parser_dir
# 查看错误信息后，直接重试
planclaw parser extract-entities $parser_dir
```

### 输出说明

每个命令输出包含：
- `KEY=value` 格式的环境变量（供脚本使用）
- `NEXT_STEP` 提示下一步应该执行的命令
- 人类可读的状态信息

智能体只需：
1. 从 init 命令提取 `PARSER_DIR`
2. 后续命令使用这个 `parser_dir`
3. 按照 `NEXT_STEP` 提示执行下一步

### 常见错误

❌ **错误示例1：手动提取多个路径**
```bash
# 不要这样做
planclaw parser convert $parser_dir
# 然后提取 MARKDOWN_PATH=xxx
# 然后记住 markdown_path=xxx
```

✅ **正确做法：只记住 parser_dir**
```bash
# 只需这样做
planclaw parser convert $parser_dir
# 系统自动管理路径，无需提取
```

❌ **错误示例2：跳过步骤**
```bash
# 不要这样做
planclaw parser init $parser_dir
planclaw parser extract-entities $parser_dir  # 跳过了 download/convert/load-schema
```

✅ **正确做法：按顺序执行**
```bash
# 按顺序执行
planclaw parser init $parser_dir
planclaw parser download $input_path $parser_dir
planclaw parser convert $parser_dir
planclaw parser load-schema $parser_dir
planclaw parser extract-entities $parser_dir
```

---

## 技术细节

### 状态文件结构

系统使用 `.pipeline_state.json` 追踪流水线状态：

```json
{
  "version": "1.0",
  "file_id": "dongan-hengtang-flood",
  "parser_dir": "/path/to/parser",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:05:00",
  "current_step": 2,
  "status": "in_progress",
  "pipeline": [
    {
      "step": 0,
      "name": "init",
      "status": "completed",
      "started_at": "2024-01-01T10:00:00",
      "completed_at": "2024-01-01T10:00:01",
      "inputs": {},
      "outputs": {}
    },
    {
      "step": 1,
      "name": "download",
      "status": "completed",
      "started_at": "2024-01-01T10:00:02",
      "completed_at": "2024-01-01T10:00:05",
      "inputs": {
        "input_path": "/path/to/input.docx"
      },
      "outputs": {
        "docx_path": "/path/to/parser/source.docx",
        "file_size": 12345
      }
    }
  ]
}
```

### 前置条件检查

系统自动检查每步的前置条件：
- `download` 需要 `init` 完成
- `convert` 需要 `download` 完成
- `load-schema` 需要 `convert` 完成
- `extract-entities` 需要 `load-schema` 完成
- `build-relations` 需要 `extract-entities` 完成
- `verify` 需要 `build-relations` 完成
- `send` 需要 `verify` 完成

如果前置条件不满足，命令会报错并提示需要先执行哪个步骤。

### 幂等性保护

已完成的步骤不能重复执行（除非先重置状态）。如果尝试重复执行，系统会报错。

**例外**：`send` 步骤支持失败重试，如果发送失败（status=failed），可以重新运行最多3次。

---

## Schema配置

### 实体去重配置（dedup_keys）

Schema支持为每个实体类型配置去重键（dedup_keys），用于在verify步骤识别和合并重复实体。

**配置格式**：
```yaml
entities:
  Person:
    dedup_keys: ["person_name", "person_phone_number"]
    properties:
      - person_name
      - person_phone_number
      - person_role
```

**配置说明**：
- `dedup_keys`：可选字段，指定用于去重的属性列表
- 如果未配置，系统使用默认策略（Person: name+phone, FamilyHousehold: name+address等）
- 去重时会对属性值进行标准化（去除空格、转小写）

**已配置的实体类型**：
- EmergencyPlan: `["emergency_plan_name"]`
- Region: `["region_name", "region_code"]`
- CommandStructure: `["command_structure_member_introduction"]`
- Person: `["person_name", "person_phone_number"]`
- FamilyHousehold: `["household_name", "household_address"]`
- HazardPoint: `["hazard_point_name", "hazard_point_location"]`
- Shelter: `["shelter_name", "shelter_address"]`
- WorkGroup: `["work_group_name"]`
- ThreeTierPackage: `["three_tier_package_area_name"]`

**如何选择去重键**：
1. 选择能唯一标识实体的属性组合
2. 优先选择稳定的属性（不易变化）
3. 避免选择可能为空的属性
4. 对于人员，建议使用 name + phone 组合
5. 对于地点，建议使用 name + address 组合

### 关系约束配置

Schema支持为关系配置约束，在verify步骤进行验证。

**约束类型**：
- `limit`: 限制关系数量（如 `limit: 1` 表示最多1个）
- `unique`: 要求关系唯一（如 `unique: true` 表示必须唯一）

**配置示例**：
```yaml
entities:
  EmergencyPlan:
    as_head_relations:
      - relation: "hasCommander"
        limit: 1
        unique: true
        tail: "Person"
```

**验证行为**：
- `limit` 违规：输出警告（warning），不阻止流程
- `unique` 违规：输出错误（error），不阻止流程
- 所有违规信息都会在verify步骤的报告中显示

---

## 常见问题

### Q: 如何查看当前进度？
A: 使用 `planclaw parser status <parser_dir>` 命令。

### Q: 某步失败了怎么办？
A: 直接重试失败的命令，系统会自动检查前置条件。如果是 `extract-entities` 或 `build-relations` 步骤失败，可能是因为超时（默认1800秒），建议使用后台任务运行。如果是 `send` 步骤失败，可以直接重试（最多3次）。

### Q: Kafka 发送失败怎么办？
A: `send` 步骤支持失败重试。如果发送失败，系统会显示错误信息和剩余重试次数。直接重新运行 `planclaw parser send <parser_dir>` 即可重试。最多允许3次尝试。

### Q: 如何查看 Kafka 发送的详细信息？
A: `send` 命令会输出以下信息：
- Thread ID（基于 file_id）
- 发送的关系数量
- Region 信息
- Kafka topic 名称
- 发送状态（成功/失败）

### Q: send 步骤使用什么作为 Kafka message key？
A: 使用格式 `graph_extract_plan_{file_id}`，其中 `file_id` 是在 `init` 步骤生成的唯一标识符。

### Q: 可以跳过某些步骤吗？
A: 不可以，必须按顺序执行所有步骤。

### Q: 如何重新开始整个流程？
A: 删除整个 `<parser_dir>` 目录，然后重新执行 init 命令。

### Q: 状态文件在哪里？
A: 在 `<parser_dir>/.pipeline_state.json`。

### Q: 为什么不需要手动提取路径？
A: 系统使用状态文件自动管理所有中间路径，智能体只需记住 parser_dir。

### Q: Windows上出现编码错误怎么办？
A: 系统已自动处理UTF-8编码问题。如果仍然出现 `UnicodeDecodeError`，请确保使用最新版本的代码。

### Q: extract-entities 或 build-relations 步骤超时怎么办？
A: 这两个步骤需要调用LLM，耗时较长（可能需要5-15分钟）。建议使用后台任务运行，或者增加超时时间。系统会使用完整文档内容进行提取，确保提取所有实体（包括Person、FamilyHousehold等）。

### Q: verify步骤做了什么？
A: verify步骤会：
1. 去重实体（基于schema配置的dedup_keys）
2. 去重关系（基于三元组：head名称、relation、tail名称）
3. 验证schema约束（unique、limit）
4. 生成验证后的数据文件（entities_validated.json, relations_validated.json）
5. 输出详细的验证报告

### Q: 如何配置实体去重规则？
A: 在schema.yaml中为实体添加dedup_keys字段：
```yaml
entities:
  Person:
    dedup_keys: ["person_name", "person_phone_number"]
```
如果未配置，系统使用默认策略。

### Q: verify步骤性能如何？
A: 系统针对大规模数据进行了优化：
- 使用元组作为去重键（比字符串快20-30%）
- 分块处理大型列表（chunk_size=1000）
- 早期退出优化（无重复时跳过处理）
- 使用defaultdict优化关系分组
- 预期性能：16000实体+30000关系 < 3分钟

### Q: send步骤使用的是原始数据还是验证后的数据？
A: send步骤优先使用验证后的数据（entities_validated.json, relations_validated.json）。如果验证文件不存在，会fallback到原始文件并输出警告。

### Q: 如何查看详细的错误信息？
A: 使用 `planclaw parser status <parser_dir>` 命令，会显示失败步骤的详细错误信息。

### Q: 为什么Person实体或FamilyHousehold实体为空或不完整？
A: 旧版本存在两个问题：1) 文档截断（只使用前8000字符）；2) LLM响应被token限制截断导致JSON不完整。新版本已修复，使用分批提取机制：
- Person按6个角色类别分批提取（指挥部人员、县级/乡镇级/村级/组级责任人、其他人员）
- FamilyHousehold按文档章节分批提取（每批最多50000字符）
- 每个批次独立调用LLM，避免响应截断
- 如果遇到此问题，请确保使用最新版本代码，并重新运行解析流程

### Q: 提取实体需要多长时间？
A: 
- 简单实体（EmergencyPlan、Region等）：几秒到几十秒
- 复杂实体（Person、FamilyHousehold、HazardPoint等）：可能需要5-15分钟
- Person和FamilyHousehold使用分批提取，每批需要单独调用LLM，总时间会更长
- 总体时间取决于文档大小和实体数量
- 建议使用后台任务运行耗时较长的步骤

### Q: 什么是分批提取？为什么需要分批？
A: 分批提取是将大型实体类型（Person、FamilyHousehold）拆分成多个小批次，分别调用LLM提取，最后合并结果。原因：
- 避免LLM响应被token限制截断（max_tokens=4096）
- 提高提取准确性和完整性
- 单批次失败不影响其他批次
- 系统会自动显示每个批次的进度和提取数量

### Q: 如何查看分批提取的调试信息？
A: 系统会自动保存调试文件到 `<parser_dir>` 目录：
- `debug_Person_batch_<N>_response.json`：Person批次N的LLM响应
- `debug_FamilyHousehold_batch_<N>_response.json`：FamilyHousehold批次N的LLM响应
- 这些文件包含完整的LLM响应，用于排查提取问题

---

## 故障排查

### 问题1: 路径相关错误
**症状**: `Error: Path escapes workspace` 或 `State file not found`

**原因**: 路径处理问题

**解决方案**:
1. 确保使用从 `init` 命令输出的完整 `PARSER_DIR` 路径
2. 不要手动修改路径
3. 使用绝对路径而不是相对路径

### 问题2: 编码错误
**症状**: `UnicodeDecodeError: 'gbk' codec can't decode`

**原因**: Windows默认使用GBK编码

**解决方案**:
- 系统已自动处理，确保使用最新版本代码
- 如果问题仍存在，可以在命令前添加 `chcp 65001 &&` 设置UTF-8编码

### 问题3: 步骤超时
**症状**: `Error: Timeout (1800s)`

**原因**: `extract-entities` 和 `build-relations` 步骤需要调用LLM，耗时较长（可能需要5-15分钟）

**解决方案**:
- 使用后台任务运行这些步骤
- 等待任务完成后，使用 `status` 命令查看结果
- 系统会使用完整文档内容进行提取，确保不遗漏实体

### 问题4: 步骤状态为 failed
**症状**: `Error: Previous step 'xxx' is not completed (status: failed)`

**原因**: 前一个步骤执行失败

**解决方案**:
1. 使用 `planclaw parser status <parser_dir>` 查看失败原因
2. 修复问题后，直接重试失败的步骤
3. 如果无法修复，删除 parser_dir 重新开始

### 问题5: Schema配置错误
**症状**: `Warning: dedup_keys references property not in entity definition`

**原因**: dedup_keys中引用的属性不存在于实体的properties列表中

**解决方案**:
1. 检查schema.yaml中的dedup_keys配置
2. 确保dedup_keys中的属性名与properties列表中的名称完全匹配
3. 如果属性确实不存在，从dedup_keys中移除或添加到properties列表

### 问题6: verify步骤性能慢
**症状**: verify步骤耗时超过预期（>3分钟）

**原因**: 数据量过大或系统资源不足

**解决方案**:
1. 检查实体和关系数量（使用status命令）
2. 系统已针对16000实体+30000关系优化，超过此规模可能需要更长时间
3. 确保系统有足够内存（建议至少2GB可用内存）
4. 如果数据量远超预期，考虑分批处理文档

### 问题7: 约束违规警告
**症状**: verify步骤输出 "Relation Constraint Violations" 或 "Unique Constraint Violations"

**原因**: 数据违反了schema中定义的约束（limit、unique）

**解决方案**:
1. 这些是警告信息，不会阻止流程继续
2. 检查违规信息，确认是否为预期行为
3. 如果不是预期行为，可能需要：
   - 调整schema约束配置
   - 检查LLM提取逻辑是否正确
   - 手动修正数据
4. 如果是预期行为（如确实有多个指挥长），可以忽略警告
