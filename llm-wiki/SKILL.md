---
name: llm-wiki
description: "LLM Wiki知识库：构建/查询相互链接的 Markdown 知识库。"
metadata:
  tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative]
  category: research
---

# LLM Wiki 知识库

构建并维护一个持久的、持续累积的知识库，其形式为相互链接的 Markdown 文件。

与传统的 RAG（检索增强生成，每次查询都需重新发现知识）不同，Wiki 一次编译知识并保持其最新性。交叉引用已就位，矛盾之处已被标记，综合内容反映了所有已摄取的信息。

**分工：** 人类负责策划来源并指导分析。代理负责总结、交叉引用、归档并维护一致性。

## 此技能何时激活

在以下情况下使用此技能，当用户：
- 要求创建、构建或启动一个 Wiki 或知识库
- 要求将某个来源摄取、添加或处理到其 Wiki 中
- 提出问题时，如果在配置的路径存在一个现有 Wiki
- 要求对其 Wiki 进行检查、审计或健康检查
- 在研究语境下引用其 Wiki、知识库或"笔记"

## Wiki 位置

Wiki 根目录固定在 `~/.planclaw/wiki`。不同领域分别放在子目录里，例如 `revision/`、`xxx/`。

```bash
WIKI="$HOME/.planclaw/wiki"
```

Wiki 只是一个包含 Markdown 文件的目录——可以在任何文本编辑器中打开。无需数据库，无需特殊工具。

## 架构：三层(必须遵守目录架构)

```
wiki/
├── SCHEMA.md           # 约定、结构规则、领域配置
├── index.md            # 分节内容目录，包含单行摘要
├── log.md              # 按时间顺序记录操作日志（仅追加，按年轮转）
├── raw/                # 第一层：不可变的源材料
│   ├── articles/       # 网页文章、剪报
│   ├── papers/         # PDF、world论文
│   ├── transcripts/    # 会议记录、访谈
│   └── assets/         # 源文件引用的图片、图表
├── entities/           # 第二层：实体页面（人物、组织、产品、模型）
├── concepts/           # 第二层：概念/主题页面
├── comparisons/        # 第二层：并列分析
└── queries/            # 第二层：值得保存的已归档查询结果
```

**第一层 — 原始来源：** 不可变。代理读取但绝不修改这些内容。
**第二层 — Wiki：** 代理拥有的 Markdown 文件。由代理创建、更新和交叉引用。
**第三层 — 模式：** `SCHEMA.md` 定义了结构、约定和标签分类法。

## 恢复现有 Wiki（至关重要——每次会话都执行此操作）

当用户拥有现有 Wiki 时，**在做任何事之前，务必先自我定位**：

① **读取 `SCHEMA.md`** —— 理解领域、约定和标签分类法。
② **读取 `index.md`** —— 了解存在哪些页面及其摘要。
③ **扫描最近的 `log.md`** —— 阅读最后 20-30 条记录，以了解近期活动。

```bash
WIKI="$HOME/.planclaw/wiki"
# 会话开始时进行定向读取
Read "$WIKI/SCHEMA.md"
Read "$WIKI/index.md"
Read "$WIKI/log.md" offset=<最后30行>
```

只有完成定向后，才能进行摄取、查询或检查。这能防止：
- 为已存在的实体创建重复页面
- 缺少对现有内容的交叉引用
- 与模式约定相矛盾
- 重复已记录的工作

对于大型 Wiki（100+ 页面），在创建任何新内容之前，还应快速对相关主题执行 `SearchFiles`。

## 初始化新 Wiki

当用户要求创建或启动 Wiki 时：

1. 确定 Wiki 路径为 `~/.planclaw/wiki`
2. 创建上述目录结构
3. 询问用户此 Wiki 涵盖的领域——务必具体
4. 编写针对该领域定制的 `SCHEMA.md`（参见下方模板）
5. 编写初始 `index.md`，包含分节标题
6. 编写初始 `log.md`，包含创建条目
7. 确认 Wiki 已就绪，并建议首先摄取哪些来源

### SCHEMA.md 模板

根据用户领域进行调整。模式约束代理行为并确保一致性：

```markdown
# Wiki 模式

## 领域
[此 Wiki 涵盖的内容——例如，"AI/ML 研究"、"个人健康"、"创业情报"]

## 约定
- 文件名：小写，连字符，无空格（例如，`transformer-architecture.md`）
- 每个 Wiki 页面以 YAML 前置元数据开始（见下文）
- 使用 `[[wikilinks]]` 在页面间链接（每个页面至少 2 个出站链接）
- 更新页面时，务必更新 `updated` 日期
- 每个新页面都必须添加到 `index.md` 的对应节中
- 每个操作都必须追加到 `log.md`
- **出处标记：** 在综合了 3 个以上来源的页面上，对于来自特定来源的段落，在其末尾添加 `^[raw/articles/source-file.md]`。这使读者无需重读整个原始文件即可追溯每个声明。在 `sources:` 前置元数据已足够的单一来源页面上为可选。

## 前置元数据
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary
  tags: [from taxonomy below]
  sources: [raw/articles/source-name.md]
  # Optional quality signals:
  confidence: high | medium | low        # how well-supported the claims are
  contested: true                        # set when the page has unresolved contradictions
  contradictions: [other-page-slug]      # pages this one conflicts with
  ---
  ```

`confidence` 和 `contested` 是可选的，但推荐用于观点浓厚或快速变化的话题。检查会高亮 `contested: true` 和 `confidence: low` 的页面以供审阅，这样薄弱的声明就不会悄然固化为公认的 Wiki 事实。

### raw/ 前置元数据

原始来源也获得一个小的前置元数据块，以便重新摄取时能检测差异：

```markdown
---
source_url: https://example.com/article   # 原始 URL（如果适用）
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

`sha256:` 允许将来对同一 URL 重新摄取时，在内容未更改时跳过处理，并在内容已更改时标记差异。仅对正文（第二个 `---` 之后的所有内容）进行计算，而非前置元数据本身。

## 标签分类法
[为该领域定义 10-20 个顶级标签。在使用新标签前，务必将它们添加至此。]

AI/ML 示例：
- 模型: model, architecture, benchmark, training
- 人员/组织: person, company, lab, open-source
- 技术: optimization, fine-tuning, inference, alignment, data
- 元信息: comparison, timeline, controversy, prediction

规则：页面上的每个标签都必须出现在此分类法中。如果需要新标签，先在此处添加，然后再使用。这能防止标签泛滥。

## 页面阈值
- **创建页面**：当实体/概念出现在 2 个以上来源中，或是某个来源的核心内容时
- **添加到现有页面**：当来源提及已涵盖的内容时
- **不为**顺便提及、次要细节或领域之外的内容**创建页面**
- **拆分页面**：当其超过 ~200 行时——拆分为带有交叉链接的子主题
- **归档页面**：当其内容已完全被取代时——移至 `_archive/`，从索引中移除

## 实体页面
每个显著实体一页。包含：
- 概览 / 它是什么
- 关键事实和日期
- 与其他实体的关系（`[[wikilinks]]`）
- 来源引用

## 概念页面
每个概念或主题一页。包含：
- 定义 / 解释
- 当前知识状态
- 未决问题或争论
- 相关概念（`[[wikilinks]]`）

## 比较页面
并列分析。包含：
- 正在比较什么以及为何比较
- 比较维度（推荐表格格式）
- 结论或综合
- 来源

## 更新策略
当新信息与现有内容冲突时：
1. 检查日期——新来源通常取代旧来源
2. 如果确实矛盾，注明两种立场及其日期和来源
3. 在前置元数据中标记矛盾：`contradictions: [page-name]`
4. 在检查报告中标记供用户审阅
```

### index.md 模板

索引按类型分节。每个条目为一行：wikilink + 摘要。

```markdown
# Wiki 索引

> 内容目录。每个 Wiki 页面按其类型列出，并附有单行摘要。
> 进行任何查询前，先读此文件以查找相关页面。
> 最后更新：YYYY-MM-DD | 总页面数：N

## 实体
<!-- 节内按字母顺序 -->

## 概念

## 比较

## 查询
```

**扩展规则：** 当任何节超过 50 个条目时，按首字母或子领域拆分为子节。当索引总共超过 200 个条目时，创建一个 `_meta/topic-map.md`，按主题对页面进行分组以实现更快导航。

### log.md 模板

```markdown
# Wiki 日志

> 所有 Wiki 操作的按时间顺序记录。仅追加。
> 格式：`## [YYYY-MM-DD] 操作 | 主题`
> 操作：ingest, update, query, lint, create, archive, delete
> 当此文件超过 500 个条目时，进行轮转：重命名为 log-YYYY.md，然后重新开始。

## [YYYY-MM-DD] create | Wiki 已初始化
- 领域: [domain]
- 已使用 SCHEMA.md、index.md、log.md 创建结构
```

## 核心操作

### 1. 摄取（Ingest）

当用户提供来源（URL、文件、粘贴内容）时，将其集成到 Wiki：

   - URL → 使用 `WebExtract` 获取 Markdown，保存至 `raw/articles/`
   - PDF → 使用 `WebExtract`（可处理 PDF），保存至 `raw/papers/`
   - 粘贴的文本 → 保存到适当的 `raw/` 子目录
   - 文件命名需具描述性：`raw/articles/planclaw-llm-wiki-2026.md`
   - **添加原始前置元数据**（`source_url`, `ingested`, 正文的 `sha256`）。
     对同一 URL 重新摄取时：重新计算 sha256，与存储值比较——如果相同则跳过，如果不同则标记差异并更新。这在每次重新摄取时进行，成本很低，能捕获到静默的源更改。

② **与用户讨论要点** —— 哪些有趣，对该领域有何意义。（在自动化/cron 上下文中跳过此步——直接继续。）

③ **检查现有内容** —— 搜索 index.md 并使用 `SearchFiles` 查找已提及实体/概念的现有页面。这是区分持续增长的 Wiki 和一堆重复文件的关键。

④ **编写或更新 Wiki 页面：**
   - **新实体/概念：** 仅当满足 SCHEMA.md 中的页面阈值（2 个以上来源提及，或对于某个来源至关重要）时，才创建页面
   - **现有页面：** 添加新信息，更新事实，更新 `updated` 日期。
     当新信息与现有内容冲突时，遵循更新策略。
   - **交叉引用：** 每个新建或更新的页面必须通过 `[[wikilinks]]` 链接到至少 2 个其他页面。检查现有页面是否链接回来。
   - **标签：** 只能使用 SCHEMA.md 分类法中的标签。
   - **出处：** 在综合了 3 个以上来源的页面上，对声明可追溯到特定来源的段落，添加 `^[raw/articles/source.md]` 标记。
   - **置信度：** 对于观点浓厚、快速变化或单一来源的声明，在前置元数据中设置 `confidence: medium` 或 `low`。除非声明在多个来源中得到充分支持，否则不要标记为 `high`。

⑤ **更新导航：**
   - 将新页面按字母顺序添加到 `index.md` 的正确节下
   - 更新索引头中的"总页面数"和"最后更新"日期
   - 追加至 `log.md`：`## [YYYY-MM-DD] ingest | 来源标题`
   - 在日志条目中列出创建或更新的每个文件

⑥ **报告更改内容** —— 向用户列出创建或更新的每个文件。

单个来源可能触发 5-15 个 Wiki 页面的更新。这是正常且期望的——这就是累积效应。

### 2. 查询

当用户询问关于 Wiki 领域的问题时：

① **读取 `index.md`** 以识别相关页面。
② **对于拥有 100+ 页面的 Wiki**，还应使用 `SearchFiles` 在所有 `.md` 文件中搜索关键词——仅靠索引可能会遗漏相关内容。
③ **使用 `Read` 读取相关页面**。
④ **从编译的知识中综合回答**。引用你所依据的 Wiki 页面："基于 [[page-a]] 和 [[page-b]]..."
⑤ **将宝贵的答案归档**——如果答案是一次实质性的比较、深度探究或新颖的综合，则在 `queries/` 或 `comparisons/` 中创建一个页面。不要归档琐碎查询——只归档那些难以重新推导的答案。
⑥ **更新 log.md**，记录查询及是否已归档。

### 3. 检查（Lint）

当用户要求检查、审计或健康检查 Wiki 时：

① **孤立页面：** 查找没有来自其他页面的入站 `[[wikilinks]]` 的页面。
```python
# 对此使用 execute_code — 在所有 Wiki 页面上进行程序化扫描
import os, re
from collections import defaultdict
wiki = "~/.planclaw/wiki"
# 扫描 entities/、concepts/、comparisons/、queries/ 中的所有 .md 文件
# 提取所有 [[wikilinks]] — 构建入站链接映射
# 入站链接为零的页面即为孤立页面
```

② **损坏的 wikilinks：** 查找指向不存在页面的 `[[links]]`。

③ **索引完整性：** 每个 Wiki 页面都应出现在 `index.md` 中。比对文件系统和索引条目。

④ **前置元数据验证：** 每个 Wiki 页面必须包含所有必填字段（title, created, updated, type, tags, sources）。标签必须来自分类法。

⑤ **陈旧内容：** `updated` 日期比提及相同实体的最新来源早了 >90 天的页面。

⑥ **矛盾：** 相同主题上存在冲突声明的页面。查找共享标签/实体但陈述不同事实的页面。高亮所有带有 `contested: true` 或 `contradictions:` 前置元数据的页面以供用户审阅。

⑦ **质量信号：** 列出带有 `confidence: low` 的页面，以及任何仅引用单一来源但未设置置信度字段的页面——这些是需要寻找佐证或降级为 `confidence: medium` 的候选。

⑧ **源差异：** 对于 `raw/` 中每个带有 `sha256:` 前置元数据的文件，重新计算哈希并标记不匹配的情况。不匹配表明原始文件被编辑过（不应该——raw/ 是不可变的），或者从已更改的 URL 摄取了内容。非硬性错误，但值得报告。

⑨ **页面大小：** 标记超过 200 行的页面——拆分的候选。

⑩ **标签审计：** 列出所有正在使用的标签，标记任何不在 SCHEMA.md 分类法中的标签。

⑪ **日志轮转：** 如果 log.md 超过 500 个条目，将其轮转。

⑫ **报告发现**，包含具体文件路径和操作建议，按严重程度分组（损坏链接 > 孤立页面 > 源差异 > 争议页面 > 陈旧内容 > 样式问题）。

⑬ **追加至 log.md：** `## [YYYY-MM-DD] lint | 发现 N 个问题`

## 使用 Wiki 进行工作

### 搜索

```bash
# 通过内容查找页面
SearchFiles "transformer" path="$WIKI" file_glob="*.md"

# 通过文件名查找页面
SearchFiles "*.md" target="files" path="$WIKI"

# 通过标签查找页面
SearchFiles "tags:.*alignment" path="$WIKI" file_glob="*.md"

# 最近活动
Read "$WIKI/log.md" offset=<最后20行>
```

### 批量摄取

当一次摄取多个来源时，批量处理更新：
1. 首先读取所有来源
2. 识别所有来源中的所有实体和概念
3. 一次性检查所有这些内容（一次搜索，而非 N 次）的现有页面
4. 一次性创建/更新页面（避免冗余更新）
5. 最后一次性更新 index.md
6. 为整个批次编写一条日志记录

### 归档

当内容完全被取代或领域范围变化时：
1. 如果 `_archive/` 目录不存在，创建它
2. 将页面及其原始路径移至 `_archive/`（例如，`_archive/entities/old-page.md`）
3. 从 `index.md` 中移除
4. 更新任何链接到它的页面——将 wikilink 替换为纯文本 + "（已归档）"
5. 记录归档操作

## 常见陷阱

- **绝不修改 `raw/` 中的文件**——来源是不可变的。更正写入 Wiki 页面。
- **务必首先进行定向**——在新会话中执行任何操作前，先读取 SCHEMA + index + 最近的日志。
  跳过这步会导致重复和遗漏交叉引用。
- **务必更新 index.md 和 log.md**——跳过这步会使 Wiki 退化。这些是导航的主干。
- **不要为顺便提及创建页面**——遵循 SCHEMA.md 中的页面阈值。在脚注中出现一次的名字不值得拥有一个实体页面。
- **不要创建没有交叉引用的页面**——孤立的页面不可见。每个页面必须链接到至少 2 个其他页面。
- **前置元数据是必需的**——它支持搜索、过滤和陈旧检测。
- **标签必须来自分类法**——自由形式的标签会沦为噪音。先将新标签添加到 SCHEMA.md，然后再使用。
- **保持页面可扫描**——Wiki 页面应能在 30 秒内读完。超过 200 行的页面需拆分。将详细分析移至专门的深度探究页面。
- **批量更新前先询问**——如果一次摄取会触及 10 个以上的现有页面，先与用户确认范围。
- **轮转日志**——当 log.md 超过 500 个条目时，将其重命名为 `log-YYYY.md` 并重新开始。代理应在检查时检查日志大小。
- **明确处理矛盾**——不要静默覆盖。注明两种声明及其日期，在前置元数据中标记，并旗标以提醒用户审阅。
