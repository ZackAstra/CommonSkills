---
name: doc-struct-xmind
version: 2.0.0
description: >
  Extract document structure from docx/pdf/markdown, generate a hierarchical Markdown outline,
  and convert to XMind 2020+ mind map (.xmind) with professional styling.
  Supports extracting heading background colors from docx and mapping to same-color flags in xmind.
  Use when user wants to: (1) extract table of contents or heading structure from a document,
  (2) create a mind map from a document's structure, (3) convert a structured Markdown to XMind,
  (4) generate a structured tree diagram from a technical document.
  Triggers: '梳理文章结构', '提取目录', '生成思维导图', '文档结构树', '导出xmind',
  '结构目录', '文档大纲', 'make mind map from document', 'extract structure'.
name_cn: 文档结构梳理与XMind导出
description_cn: 从文档中提取标题结构，生成层级Markdown大纲并转换为专业样式的XMind思维导图
create_source: super-agent-skill-creator
---

# 文档结构梳理与 XMind 导出

## 核心流程（三步链路）

```
源文档(docx/pdf) → 结构化Markdown → XMind 2020+ (.xmind)
```

### 第一步：提取文档结构 → Markdown

1. **读取源文档**，提取全部标题（Heading 1-6）和标题下方的正文段落
2. **提取标题底色**：从 docx 中读取 run-level highlight/shading，建立 `{标题: 旗帜ID}` 映射
3. **生成 Markdown 结构树**，遵循以下约束：
   - **标题层级完整保留**：`#` 为中心主题，`##` ~ `#######` 对应源文档 H1 ~ H6（共7级，超出Markdown标准的 `#######` 由 md2xmind.py 扩展解析）
   - **章节编号统一阿拉伯数字**：中文数字"一、"→"1 "，无编号的章节自动补编号
   - **内容忠实原文**：标题文字、括号内容、正文描述完整照搬，不添加自撰总结
   - **能力单元独立化**：源文档中被嵌在描述文本中的能力单元（如 Skill、算法、智能体等），提升为独立标题节点，与源文档层级对齐
   - **水印过滤**：跳过 `> AI生成` 等AIGC水印行
4. 非标题行的正文段落聚合为紧邻上方标题节点的 notes 描述

### 第二步：Markdown → XMind

调用 `scripts/md2xmind.py`：

```bash
python scripts/md2xmind.py <input.md> <output.xmind> [--right N] [--theme blue|green|red]
```

参数说明：
- `--right N`：右侧分支数，默认自动均等划分
- `--theme`：主题色，默认 blue

### 第三步：验证输出

用 Python 读取 xmind 内 content.json，确认：
- 一级分支数与文档章节数一致
- 左右分支分配正确
- notes 描述和 markers 标记正确
- 旗帜仅在有底色的标题上出现

---

## 方法论与关键经验

### Markdown 结构树生成原则

| 原则 | 说明 | 反模式 |
|------|------|--------|
| 层级完整 | 源文档N级标题 → Markdown第N+1级标题（#为中心），全部保留不截断 | 截断深层标题导致父子变兄弟 |
| 阿拉伯数字 | 章节编号统一用阿拉伯数字（1/2/3...） | 混用中文数字"一/二/三" |
| 忠实原文 | 标题文字、括号内容、能力描述照搬原文 | 自撰总结附加到标题 |
| 能力独立 | 源文档中被埋在描述中的能力单元，提升为同级独立标题节点 | 将能力单元留在描述文本中 |
| 描述聚合 | 连续非标题行合并为前一个节点的 notes | 每行独立处理导致碎片化 |
| 水印过滤 | 跳过 `> AI生成` 等AIGC水印行 | 水印混入 xmind notes |
| 底色映射 | 仅源文档有底色的标题插入同色旗帜 | 所有标题都插旗帜或按层级分配 |

### 中文数字转阿拉伯数字

- "一、"→"1 "，"十一、"→"11 "（必须跟顿号/空格，避免误匹配"一网统揽"等正文中的"一"）
- 无编号前缀的章节自动补编号（如"自动化治理"→"3 自动化治理"）
- 原文已有阿拉伯编号的保持不变

### XMind 2020+ 格式要点

| 要点 | 正确做法 | 常见错误 |
|------|----------|----------|
| 文件格式 | content.json（JSON） | content.xml（旧版XML，无法打开） |
| 必需文件 | content.json + metadata.json + manifest.json | 缺少 manifest 导致识别失败 |
| 布局 | `org.xmind.ui.map.unbalanced` + right-number | 用默认 map 布局无法左右分 |
| 左侧排序 | children 数组中左侧部分需 **反序** | 正序导致左侧从上到下 N->1 |
| 折叠标记 | `branch: "folded"` | 用其他字段名无效 |
| notes 格式 | `{"plain": {"content": "..."}}` | 直接写字符串无效 |
| 旗帜映射 | 仅从源文档提取有底色的标题 → 同色旗帜 | 死板地按层级分配旗帜 |

### unbalanced 布局的左右均等分配规则

核心目标：**从左到右、从上到下，从小到大升序排列**

XMind unbalanced 布局的 children 数组中：
- **前 right-number 个** → 渲染在**右侧**，从上到下按数组顺序
- **剩余部分** → 渲染在**左侧**，从下到上按数组顺序

通用公式：
```
total = 一级分支总数
left_count = ceil(total / 2)      # 左侧放前 left_count 个（编号 1 ~ left_count）
right_count = total - left_count   # 右侧放后 right_count 个（编号 left_count+1 ~ total）

right_branches = all[left_count:]   # 右侧正序
left_branches = all[:left_count]
left_branches.reverse()             # 左侧反序（XMind 从数组末尾往上渲染）

children = right_branches + left_branches
right-number = right_count
```

### 旗帜映射规则

从源文档 docx 中提取标题的 highlight/shading 底色，映射为 XMind 同色旗帜：

| 源文档底色类型 | 映射规则 |
|---------------|---------|
| highlight=yellow/green/blue/red | → flag-yellow / flag-green / flag-blue / flag-red |
| shading fill（非白、非auto） | 近似色映射：蓝灰系→flag-blue, 绿系→flag-green, 橙系→flag-red, 黄系→flag-yellow |
| **无底色** | **不插旗帜** |

---

## 样式规范

| 元素 | 属性 |
|------|------|
| 字体 | Microsoft YaHei（微软雅黑） |
| 中心主题 | 填充 #DCE6F2，边框 #558ED5 5pt，圆角矩形 |
| 一级分支（章节） | 填充 #DCE6F2，边框 #558ED5 2pt，圆角矩形 |
| 连接线 | 曲线 `org.xmind.branchConnection.curve`，1pt #558ED5 |
| 旗帜 | 仅在有底色的标题插入同色旗帜 |
| 深层节点 | 含较长 notes 的叶子节点自动折叠（脚本内置规则） |

### 三套可选主题

- **blue**（默认）：蓝色系，适合技术文档、方案文档
- **green**：绿色系，适合环保/生态/规划类文档
- **red**：红色系，适合政务/党建/品牌类文档

---

## 脚本

### scripts/md2xmind.py

Markdown → XMind 2020+ 转换器，支持：
- 七级标题解析 + notes 聚合 + AIGC 水印过滤
- 三套主题（blue/green/red）
- 左右均等布局 + 左侧反序，实现从左到右升序
- 底色→旗帜映射：由调用方传入 hl_map，仅在有底色时插入同色旗帜
- 深层节点自动折叠

```bash
python scripts/md2xmind.py input.md output.xmind --right 7 --theme blue
```

---

## 典型用户请求与响应

| 用户请求 | 执行路径 |
|----------|----------|
| "梳理这篇文章的结构，生成xmind" | 提取docx(含底色) → 生成MD → 调用md2xmind.py(传入hl_map) |
| "把这个markdown转成思维导图" | 直接调用md2xmind.py |
| "提取文档目录树" | 提取docx → 生成MD（不转xmind） |
| "结构目录导出xmind，左侧8章右侧7章" | 提取 → 生成MD → `--right 7` |
| "换成红色主题" | 提取 → 生成MD → `--theme red` |

---

## 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | - | 初始版本 |
| 1.1.0 | 2026-08-10 | 支持7级标题（#######），修复H6父子层级丢失问题 |
| 2.0.0 | 2026-08-10 | 移除硬业务逻辑规则：删除行业特定关键词硬编码（FLAG_RED_KEYWORDS）、折叠阈值硬编码改为脚本内置可维护逻辑、旗帜由hl_map驱动而非层级；统一SKILL与脚本描述一致性；主题适用场景泛化 |
