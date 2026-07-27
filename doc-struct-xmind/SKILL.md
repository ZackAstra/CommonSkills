---
name: doc-struct-xmind
description: >
  Extract document structure from docx/pdf/markdown, generate a hierarchical Markdown outline,
  and convert to XMind 2020+ mind map (.xmind) with blue-theme professional styling.
  Supports extracting heading background colors from docx and mapping to same-color flags in xmind.
  Use when user wants to: (1) extract table of contents or heading structure from a document,
  (2) create a mind map from a document's structure, (3) convert a structured Markdown to XMind,
  (4) generate a structured tree diagram from a technical document.
  Triggers: '梳理文章结构', '提取目录', '生成思维导图', '文档结构�?, '导出xmind',
  '结构目录', '文档大纲', 'make mind map from document', 'extract structure'.
name_cn: 文档结构梳理与XMind导出
description_cn: 从文档中提取标题结构，生成层级Markdown大纲并转换为蓝色系专业样式的XMind思维导图
create_source: super-agent-skill-creator
---

# 文档结构梳理�?XMind 导出

## 核心流程（三步链路）

```
源文�?docx/pdf) �?结构化Markdown �?XMind 2020+ (.xmind)
```

### 第一步：提取文档结构 �?Markdown

1. **读取源文�?*，提取全部标题（Heading 1-6）和标题下方的正文段�?2. **提取标题底色**：从 docx 中读�?run-level highlight/shading，建�?`{标题: 旗帜ID}` 映射
3. **生成 Markdown 结构�?*，规则：
   - 所有子项展开为编号标题（�?`### 3.1.1 xxx`），不使用列表形�?   - **章节编号统一阿拉伯数�?*：中文数�?一�?�?1 "，无编号的章节自动补编号
   - **严格保留原文描述**：括号内容、正文描述完整照�?   - **不添加自撰总结**：原文无描述的标题不加任何编造内�?   - Skill/算法/智能�?等能力单元提升为独立编号标题
   - 过滤 AIGC 水印行（`> AI生成`�?4. 非标题行的正文段落聚合为紧邻上方标题节点�?notes 描述

### 第二步：Markdown �?XMind

调用 `scripts/md2xmind.py`�?
```bash
python scripts/md2xmind.py <input.md> <output.xmind> [--right N] [--theme blue|green|red]
```

参数说明�?- `--right N`：右侧分支数，默认自动均等划�?- `--theme`：主题色，默�?blue

### 第三步：验证输出

�?Python 读取 xmind �?content.json，确认：
- 一级分支数与文档章节数一�?- 左右分支分配正确（左侧前 N 章，右侧�?M 章）
- notes 描述�?markers 标记正确
- 旗帜仅在有底色的标题上出�?
---

## 方法论与关键经验

### Markdown 结构树生成原�?
| 原则 | 说明 | 反模�?|
|------|------|--------|
| 编号展开 | 所有子项用标题层级表达�?## 3.1.1�?| 用列�?`- 3.1.1` 代替标题 |
| 阿拉伯数�?| 章节编号统一用阿拉伯数字�?/2/3...�?| 混用中文数字"一/�?�? |
| 原文保留 | 括号内容、能力描述照搬原�?| 自撰总结附加到标�?|
| 能力提升 | Skill/算法/智能体为独立编号标题 | �?Skill 埋在描述文本�?|
| 描述聚合 | 连续非标题行合并为前一个节点的 notes | 每行独立处理导致碎片�?|
| 水印过滤 | 跳过 `> AI生成` �?| 水印混入 xmind notes |
| 底色映射 | 仅有底色的标题插入同色旗�?| 所有标题都插旗�?|

### 中文数字转阿拉伯数字

- "一�?�?1 "�?十一�?�?11 "（必须跟顿号/空格，避免误匹配"一网统�?�?- 无编号前缀的章节自动补编号（如"自动化治�?�?3 自动化治�?�?- 原文已有阿拉伯编号的保持不变

### XMind 2020+ 格式要点

| 要点 | 正确做法 | 常见错误 |
|------|----------|----------|
| 文件格式 | content.json（JSON�?| content.xml（旧版XML，无法打开�?|
| 必需文件 | content.json + metadata.json + manifest.json | 缺少 manifest 导致识别失败 |
| 布局 | `org.xmind.ui.map.unbalanced` + right-number | 用默�?map 布局无法左右�?|
| 左侧排序 | children 数组中左侧部分需 **反序** | 正序导致左侧从上到下 N->1 |
| 折叠标记 | `branch: "folded"` | 用其他字段名无效 |
| notes 格式 | `{"plain": {"content": "..."}}` | 直接写字符串无效 |
| 旗帜映射 | �?docx highlight/shading 提取底色→旗�?| 死板地按层级分配旗帜 |

### unbalanced 布局的左右均等分配规�?
核心目标�?*从左到右、从上到下，从小到大升序排列**

XMind unbalanced 布局�?children 数组中：
- **�?right-number �?* �?渲染�?*右侧**，从上到下按数组顺序
- **剩余部分** �?渲染�?*左侧**，从下到上按数组顺序

实现"左侧1-8、右�?-15"的代码：
```
left_count = ceil(15/2) = 8    # 左侧放前8个（1~8�?right_count = floor(15/2) = 7  # 右侧放后7个（9~15�?
right_branches = all[8:]        # [9,10,11,12,13,14,15] 正序
left_branches = all[:8]         # [1,2,3,4,5,6,7,8]
left_branches.reverse()        # [8,7,6,5,4,3,2,1] �?渲染从末尾往上即 1~8

children = right_branches + left_branches
right-number = 7
```

### 旗帜映射规则

| docx 底色 | XMind 旗帜 | 说明 |
|-----------|-----------|------|
| highlight=yellow | flag-yellow | 黄色高亮 |
| highlight=green | flag-green | 绿色高亮 |
| highlight=blue | flag-blue | 蓝色高亮 |
| highlight=red | flag-red | 红色高亮 |
| shading fill (非白) | 同色 flag | 段落底纹 |
| **无底�?* | **不插旗帜** | 原文没有底色就不加旗�?|

---

## 样式规范（默认蓝色主题）

| 元素 | 属�?|
|------|------|
| 字体 | Microsoft YaHei（微软雅黑） |
| 中心主题 | 填充 #DCE6F2，边�?#558ED5 5pt，圆角矩�?|
| 一级分支（章节�?| 填充 #DCE6F2，边�?#558ED5 2pt，圆角矩�?|
| 连接�?| 曲线 `org.xmind.branchConnection.curve`�?pt #558ED5 |
| 旗帜 | 仅在有底色的标题插入同色旗帜 |
| 深层叶子节点 | notes > 80字自动折�?|

### 三套可选主�?
- **blue**（默认）：蓝色系，适合技术文档、方案文�?- **green**：绿色系，适合环保/生�?规划�?- **red**：红色系，适合电信/央企/党建类（#E60012 近似�?
---

## 脚本

### scripts/md2xmind.py

Markdown �?XMind 2020+ 转换器，支持�?- 六级标题解析�?级映射为5级）+ notes 聚合 + AIGC 水印过滤
- 三套主题（blue/green/red�?- 左右均等布局 + 左侧反序，实现从左到右升�?- 底色→旗帜映射：�?docx 提取标题底色，仅在有底色时插入同色旗�?- 深层节点自动折叠

```bash
python scripts/md2xmind.py input.md output.xmind --right 7 --theme blue
```

---

## 典型用户请求与响�?
| 用户请求 | 执行路径 |
|----------|----------|
| "梳理这篇文章的结构，生成xmind" | 提取docx(含底�? �?生成MD �?调用md2xmind.py(传入hl_map) |
| "把这个markdown转成思维导图" | 直接调用md2xmind.py |
| "提取文档目录�? | 提取docx �?生成MD（不转xmind�?|
| "结构目录导出xmind，左�?章右�?�? | 提取 �?生成MD �?`--right 7` |
| "换成红色主题" | 提取 �?生成MD �?`--theme red` |

