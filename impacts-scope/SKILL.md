---
name: impacts-scope
description: 分析突发事件的影响范围，查询事件周边隐患点及受影响的村/社区，并生成自然语言影响范围描述报告。
---

# 事件影响范围分析

根据事件ID分析突发事件的影响范围。只需提供 **事件ID**，系统会自动处理所有内部细节。

## 正确做法

使用 `planclaw impacts` CLI 命令完成分析，**不要**直接调用 Python 函数。

### 方式一：一步到位（推荐）

```bash
planclaw impacts analyze <事件ID>
```

命令会直接输出 `IMPACT_SCOPE=...`，这就是最终影响范围描述，**直接返回**即可。

### 方式二：分步执行（需要查看中间结果时用）

按顺序执行以下命令，**不要**加 `cd`：

```bash
# 1. 初始化工作目录（自动生成目录名）
planclaw impacts init

# 2. 从步骤1的输出中提取 IMPACT_DIR，后续步骤复用该路径
#    输出示例：IMPACT_DIR=C:\Users\xxx\.planclaw\impacts\20250112_143052_123

# 3. 查询事件信息（参数顺序：工作目录 事件ID）
planclaw impacts query-event $IMPACT_DIR <事件ID>

# 4. 分析影响范围
planclaw impacts analyze-scope $IMPACT_DIR

# 5. 生成影响范围描述报告（最后一步）
planclaw impacts generate-report $IMPACT_DIR
```

**获取最终结果**：
`generate-report` 的输出中包含 `REPORT_FILE` 路径，该 JSON 文件中的 `scope_text` 字段即为最终影响范围描述。

如果需要读取文件内容：
```bash
planclaw impacts generate-report $IMPACT_DIR
# 从输出中提取 REPORT_FILE，然后读取其 scope_text 字段
```

**注意**：`generate-report` 命令的输出中已经直接打印了 `scope_text` 内容，如果输出中已包含完整文本，直接返回该文本即可，无需再读取文件。

## 禁止行为

- ❌ **禁止**直接调用 Python 函数（如 `analyze_with_details()`）
- ❌ **禁止**使用 `python -c "import planclaw..."` 直接导入模块
- ❌ **禁止**在命令前加 `cd`（Bash 工具已自动处理工作目录）
- ❌ **禁止**手动构造工作目录路径（除非用户明确指定）
- ❌ **禁止**执行 `planclaw impacts send`（分析到 `generate-report` 即结束）
- ❌ **禁止**调用 LLM 对结果进行二次加工、总结或润色

## 输出规范

获取结果后，**直接返回原始输出**，不要：

- ❌ 调用 LLM 二次加工或润色
- ❌ 生成 Markdown 表格或复杂格式
- ❌ 添加额外章节
- ❌ 扩展或补充数据中未提及的内容

✅ **正确做法**：直接输出 CLI 命令打印的 `scope_text` 原始内容。
