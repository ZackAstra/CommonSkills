---
name: ppt-aesthetics
description: "PPT 美观评分与修复技能。渲染 PPTX 为图片、用 AI 视觉模型 + 结构化脚本对每页美观度打分（9 维度评分 + 59 种反模式自动检测，覆盖 10 类检测维度）、用 python-pptx 自动修复常见问题（统一字体/配色/页边距/图片拉伸/拆分长段落/套用主题背景/字号阶梯 Type Scale/间距网格 4-8px）。借鉴 web-design-engineer 审美法则（Major Third 字号阶梯、60-30-10 配色、50-950 色阶系统、4/8px 间距节奏）。提供 7 套配色方案（含电信红）、5 套中英文字体搭配、8 套布局模板、图表美学规范、反模式修复手册。支持电信风格 PPT 生成（严格使用内置电信模板、电信红色强制规范 #E60012）。触发词：PPT审美, PPT美化, PPT评分, PPT打分, PPT修复, PPT好看吗, 给PPT打分, 美化PPT, PPT设计, PPT排版, 前端设计规范导PPT, 组件截图放PPT, SVG素材导PPT, 电信风格PPT, 电信模板PPT, 红色主题电信PPT, 电信红PPT"
name_cn: PPT审美-支持电信风格
description_cn: 渲染+评分+修复 PPT 美观度（9 维度评分、59 种反模式检测（10 类）、自动修复、配色/字体/布局库，借鉴 web-design-engineer 审美），支持电信风格 PPT 生成（严格使用内置电信模板、电信红色强制规范 #E60012、7场景权重含telecom）
create_source: super-agent-skill-creator
---

# PPT审美 (pptAesthetics)

把任意 PPT 渲染成图片，用「结构化脚本 + AI 视觉模型」对每页美观度打分；用 python-pptx 自动修复可机械修复的问题（字体、配色、页边距、图片拉伸、长段落拆分、背景统一、**字号阶梯 Type Scale**、**间距网格 4-8px**）。借鉴 **web-design-engineer 审美法则**（Major Third 字号阶梯、60-30-10 配色、50-950 色阶系统、4/8px 间距节奏）。配 7 套配色方案（含电信红）、5 套中英文字体搭配、8 套布局模板、**34 套 HTML 幻灯片模板**（来源于 beautiful-html-templates，支持 HTML→PNG→PPTX 流程）、图表美学规范、反模式修复手册。

## 核心方法论：先设计后制作

> Adapted from [obra/superpowers](https://github.com/obra/superpowers) — "Design before code" methodology, adapted for PPT creation: **Design before making slides.**

### 核心哲学

- **设计在先** — 理解再做，不在做的过程中理解
- **系统化优于即兴** — 流程高于猜测
- **证据优于声称** — 验证后再宣布完成
- **视觉优于文字** — Picture Superiority Effect：图片比纯文字记忆率高 6 倍
- **YAGNI** — You Aren't Gonna Need It，去掉不必要的幻灯片和装饰

### The Workflow

当启动任何 PPT 制作任务时，遵循以下序列：

```
1. Design Brainstorming  → 构思 PPT 视觉设计，获得用户审批
2. Page Planning         → 把设计拆解为逐页蓝图（布局+配图+文字），产出台本
3. PPT Execution         → 先图后文，逐页构建（配图→排版→文字），每段快速质检
4. Aesthetic Review      → 9 维度评分 + 反模式检测，对标设计文档
5. Score Verification    → 全量评分达标才交付，证据优先
6. Deliver & Cleanup     → 输出最终 PPTX + 报告，清理临时文件
```

**进入任何阶段前，先检查当前应处于哪个阶段。** 哪怕只有 1% 的可能性某个阶段需要执行，就读取对应参考文档。

### 阶段优先级

当多个阶段可能同时适用时：

1. **流程阶段先行**（design-brainstorming） — 决定"怎么做"
2. **执行阶段其次**（ppt-execution） — 指导实际操作

"帮我做个 PPT" → 先 brainstorming，再 execution。
"修一下这个丑 PPT" → 先评分（工作流 1），再修复（工作流 2）。

### 参考文档导航

| 阶段 | 参考文档 | 何时阅读 |
|------|---------|---------|
| 设计构思 | [references/ppt-brainstorming.md](references/ppt-brainstorming.md) | 制作任何新 PPT 之前 — 构思内容与视觉方案 |
| 逐页规划 | [references/ppt-planning.md](references/ppt-planning.md) | 设计审批后、制作 PPT 之前 — 产出台本蓝图 |
| 制作执行 | [references/ppt-execution.md](references/ppt-execution.md) | 拿到台本蓝图后 — 按计划逐步构建 |
| 美学评分 | [references/aesthetic-scoring-rubric.md](references/aesthetic-scoring-rubric.md) | 评分时（含视觉模型 Prompt、维度标准、反模式扣分） |
| 反模式修复 | [references/anti-pattern-fixes.md](references/anti-pattern-fixes.md) | 修复时（每个反模式的检测+修复方法） |
| 图标使用 | [references/icon-style-guide.md](references/icon-style-guide.md) | 使用图标时（风格/尺寸/颜色/格式规范） |
| 动画转场 | [references/animation-aesthetics.md](references/animation-aesthetics.md) | 使用动画时（克制原则+允许/禁止清单） |
| 多语言排版 | [references/multilingual-typography.md](references/multilingual-typography.md) | 中英/中日韩混排时（字体分设+间距+标点） |
| 无障碍 | [references/accessibility-guide.md](references/accessibility-guide.md) | 对比度+色盲安全+Alt文本+阅读顺序 |
| 图片处理 | [references/image-guidelines.md](references/image-guidelines.md) | 选择/裁剪/遮罩/AI生成规范 |

### 硬门禁（Hard Gate）

```
未经设计审批，不得创建 PPTX 文件、生成配图、或执行任何制作操作。
这适用于所有 PPT 项目，无论其看起来多么简单。
```

**违反规则的字面意思就是违反规则的精神。**

### 红线规则 — STOP 并遵循流程

| 想法 | 现实 |
|------|------|
| "这个 PPT 太简单，不需要设计" | 简单项目恰恰是未审查假设造成最多浪费的地方 |
| "先做出来再调整" | 先做后改 = 重做，不是调整 |
| "我直接开始写内容" | 内容没有视觉方向 = 文字堆砌 |
| "先配图等设计定下来再改" | 方向不确定的配图 = 全部作废 |
| "先建 PPT 再补图" | 配图门禁强制：配图未达标禁止进入 PPT 构建步骤 |

### 强制规则

1. **NO 制作无设计** — 必须先 brainstorming 获得用户审批
2. **NO 配图后补** — 必须先生成配图再构建 PPT（先图后文）
3. **NO 交付无评分** — 必须评分验证达标后才交付
4. **NO 跳过清理** — 必须执行 C1-C4 清理 Checklist
5. **NO "太简单"例外** — 每个项目都走流程，设计可以很短但不能没有

---

## 何时使用

- 用户说"做个 PPT / 帮我生成 PPT / 制作幻灯片" → 走**设计→规划→制作工作流**（先 brainstorming 获得设计审批，再 ppt-planning 产出台本，再 ppt-execution 逐步构建）
- 用户问"PPT 好看吗 / 给 PPT 打分 / PPT 评分 / 评估这个 PPT" → 走**评分工作流**
- 用户说"美化 PPT / 修复 PPT / PPT 太丑 / 改善这个 PPT" → 走**修复工作流**（含评分验证）
- 用户说"PPT 评分 + 修复" → 走**完整工作流**（评分→修复→再评分验证）
- 用户说"电信风格 / 电信模板 / 中国电信风格 PPT / 红色主题电信" → 走**电信风格工作流**（严格使用内置模板、电信红 #E60012 强制规范）
- 用户给前端项目（Tailwind / Storybook / CSS 变量）要转 PPT 主题 → 走**前端 Token 工作流**（次要）
- 用户要把组件截图/SVG 素材放 PPT → 走**资产捕获工作流**（次要）

> **所有生成工作流（1-6）完成后自动执行工作流 7（自我批判交付）**，除非用户显式要求跳过。

## 决策树

```
用户给了 PPTX 吗？
├─ 是 → 用户想要什么？
│   ├─ 打分     → 评分工作流
│   ├─ 美化     → 修复工作流（含评分验证）
│   ├─ 打分+美化 → 完整工作流
│   └─ 电信风格 → 电信风格工作流
└─ 否 → 用户想做什么？
    ├─ 做个新 PPT ─→ 【设计→规划→制作工作流】
    │                ├─ Phase 1: ppt-brainstorming（设计构思，获得审批）
    │                ├─ Phase 2: ppt-planning（逐页规划，产出台本）
    │                ├─ Phase 3: ppt-execution（先图后文，逐步构建）
    │                ├─ Phase 4: 评分验证（工作流 1）
    │                └─ Phase 5: 交付清理
    ├─ 电信风格/电信模板 → 电信风格工作流
    ├─ 前端项目 → 前端 Token 工作流
    └─ 截图/描述 → 直接咨询 [references/]
```

## PPT 制作执行准则：先图后文（强制）

> 适用于**所有 PPT 新建/生成场景**，是 ppt-execution 阶段的核心纪律。PPT 是视觉沟通工具，不是文字阅读工具。**禁止生成纯文字 PPT**——每一页都应有视觉素材支撑，避免沦为"Word 文档投影"。
>
> **这些规则在 ppt-brainstorming（设计构思）和 ppt-planning（逐页规划）阶段之后、ppt-execution（制作执行）阶段中强制执行。** 设计阶段确定"做什么"，规划阶段确定"怎么做"，执行阶段严格按规划实施。

### 核心流程

```
[1. 内容大纲规划]   → 确定每页主题与关键信息点（只列要点，不写全文）
        │
        v
[2. 自动配图建议+数据提取]  → 运行 suggest_illustrations.py，基于内容自动推荐配图类型、
        │              生成方式、嵌入位置，**并提取结构化配图数据**。
        │              ├─ data_status="auto" → 数据已自动提取，可直接生成
        │              └─ data_status="manual" → 需 Agent 手动补充 data 字段
        │              （见下方"内容感知配图建议"章节）
        v
[3. 配图生成]       → PIL 类型：gen_pil_illustrations.py --from-pptx 一键生成（自动条目）
        │              │  Agent 只需补充 data_status="manual" 的页面
        │              ├─ SVG 类型：LLM 写 SVG → svg_to_pptx.py
        │              └─ ImageGen 类型：Agent 调用 ImageGen → gen_illustrations.py 后处理
        │              （所有输出必须写入 .temp/illustrations/，不得输出到其他位置）
        v
[? 配图门禁检查]   → 配图覆盖率 ≥ 30%？NO → 禁止构建 PPT，必须补齐配图
        │                YES ↓
        v
[4. 审图]           → 用 image_understanding 逐张审核生成结果：
        │              - 技术图：检查结构完整、箭头/标签无重叠、色彩正确
        │              - 场景图：检查主题相关、风格统一、无畸变
        │              不合格 → 重新生成；最多重试 2 次
        v
[5. 构建视觉化 PPT] → ppt-master SVG→PPTX 流水线 或 python-pptx 精确构建：
        │              逐页写 SVG → SVG 质检 → finalize_svg.py → svg_to_pptx.py
        │              输出原生可编辑 PPTX（非图片幻灯片）
        │
        v
[6. 评分验证]       → 走工作流 1，确保无 text_heavy_deck 反模式
```

### ImageGen 调用说明（关键）

**ImageGen 是延迟加载工具（deferred tool），不能直接调用**。必须按以下步骤：

1. **加载 schema**：先用 `ToolSearch` 加载 ImageGen 的参数 schema
   ```
   ToolSearch(tool_names: ["ImageGen"])
   ```
2. **调用工具**：用 `DeferExecuteTool` 调用，每页配图单独一次调用
   ```
   DeferExecuteTool(
     toolName: "ImageGen",
     params: { prompt: "<page-specific prompt>" }
   )
   ```
3. **保存配图**：每次调用返回的图片路径，必须复制/移动到 `.temp/illustrations/`，文件名按页号命名（如 `page_03_cover.png`）

**配图 prompt 模板**（每页按此结构撰写）：
```
[主题关键词]，[视觉风格：扁平/线性/照片感/抽象]，[主色调：与企业品牌色一致]，
[构图：宽幅/居中/分屏]，[氛围：专业/科技/温暖]，[避免：写实人物/版权素材/文字水印]
画幅比例 16:9，高分辨率
```

**调用次数计算**：
- N 页 PPT → 配图规划阶段确定需要 M 张配图（M ≈ N × 0.7，数据页可用 python-pptx 原生图表抵充）
- 一次性批量调用 M 次 DeferExecuteTool（可并行）

**降级策略**（ImageGen 调用失败时）：
1. **重试**：单张配图失败，重试 2 次
2. **占位**：仍失败 → 该页改用图标/几何形状色块占位（不得留空堆文字）
3. **豁免**：仅封面/封底/目录页可豁免配图要求（封面用模板自带背景也算配图）

### 配图门禁检查（强制，不得跳过）

**在步骤 3（批量生成配图）与步骤 5（构建 PPT）之间，必须执行以下检查：**

```
门禁阈值：有图页数 / 总页数 ≥ 30%（默认；可通过 --threshold 调整）
          "有图"定义：幻灯片上存在 MSO_SHAPE_TYPE.PICTURE 类型 shape，
                       且图片面积 ≥ 幻灯片面积 × 2%（排除微型装饰图标）
          覆盖率等级：<30% LOW（红色警告）| 30-50% FAIR | ≥50% GOOD

脚本门禁：python scripts/gate_image_coverage.py input.pptx --threshold 0.3

验证：
  IF 覆盖率 < 阈值:
      STOP —— 禁止进入"构建 PPT"步骤
      补齐缺失配图后重新检查，直到达标才能继续
  ELSE:
      记录配图清单到 .temp/illustration_manifest.json，继续步骤 5
```

**门禁不达标的处理**：不得"先建 PPT 再补图"，必须回到步骤 2-3 补齐配图。

### 内容感知配图建议（自动化）

> **核心脚本**：`suggest_illustrations.py` — 分析 PPTX 内容，自动推荐配图类型、**提取配图数据**、生成方式和嵌入位置。
>
> **解决的问题**：之前的配图流程是 100% 手动的——Agent 必须逐页分析内容、手动决定配图类型、手动写配置文件、**手动从页面文本中提取标签/阶段/项目等数据填入配置**。现在脚本自动完成这些工作，Agent 只需审阅和微调。

**使用方式**：
```powershell
# 分析已有 PPTX，输出配图建议 JSON（含提取的结构化数据）
python scripts/suggest_illustrations.py input.pptx -o .temp/suggestions.json --verbose

# 指定场景（影响配色和风格推荐）
python scripts/suggest_illustrations.py input.pptx -o .temp/suggestions.json --scenario telecom
# --scenario 可选：telecom（电信红黄）、tech（科技蓝）、neutral（中性灰绿），默认 neutral
```

**输出 JSON 包含**：
- `suggestions[]`：每页的配图建议（内容类型、配图类型、生成方式、嵌入位置、优先级、提示词）
- `gen_config[]`：可直接用于 `gen_pil_illustrations.py --config` 或 `gen_illustrations.py --config` 的配置，**已包含提取的 `data` 字段和 `style` 字段**
- `embed_config[]`：可直接用于 `embed_illustrations.py --config` 的配置
- `summary`：按生成方式和配图类型的统计摘要，含 `data_extraction` 统计

**数据提取能力**（`data` 字段）：

脚本不仅推荐配图类型，还自动从页面文本中提取生成配图所需的结构化数据：

| 配图类型 | 提取的数据 | 提取规则 |
|----------|-----------|---------|
| timeline | `stages[]`：每阶段的标签和子标签 | 识别"阶段1/Phase 1/第一阶段"等序号关键词，分割为阶段列表 |
| comparison | `items[]`：对比项的标签 | 识别"/""与""vs""对比"等分隔符，提取2-N个对比项 |
| hierarchy | `levels[]`：层级标签 | 识别缩进层级、编号层级（1.→1.1→1.1.1），构建树形结构 |
| flowchart | `steps[]`：步骤标签 | 识别"步骤1/Step/①②③"等序号关键词 |
| infographic | `items[]`：信息项标签+值 | 识别"XX%"/"XX元"等数值+单位组合 |
| list | `items[]`：列表项标签 | 识别编号列表（1.2.3.）或符号列表（?-*） |

**`data_status` 字段**：每条建议的 `data_status` 标识数据提取状态：
- `auto`：自动提取成功，`data` 字段可直接用于生成配图
- `manual`：无法自动提取，Agent 需手动补充 `data` 字段后再生成

**`style` 字段**：由 `--scenario` 参数控制，影响 `gen_pil_illustrations.py` 的配色方案：
- `telecom`：电信红(#E60012)+黄(#FFB800)渐变，白色文字
- `tech`：科技蓝(#0066CC)+青(#00CCFF)渐变，白色文字
- `neutral`：灰绿(#2D5016)+金(#B8860B)，深色文字

**内容类型检测规则**（标题关键词优先，正文关键词辅助）：

| 内容类型 | 标题关键词（3x权重） | 正文关键词（1x权重） | 推荐配图 | 生成方式 |
|----------|---------------------|---------------------|----------|---------|
| cover | 首页位置 | 目录/提纲/概览 | 场景大图/背景图 | ImageGen |
| ending | 末页位置/谢谢/Q&A | 感谢/结束 | 收尾呼应图 | ImageGen |
| timeline | 阶段/演进/发展/迭代升级 | 时间线/历程/趋势 | 时间线示意图 | PIL |
| process | 步骤/闭环/pipeline | 回路/循环/运转 | 流程图 | PIL |
| comparison | 对比/区别/vs/比较/转向 | 差异/优劣/对照 | 对比图 | PIL |
| hierarchy | 结构/目录/要素/架构 | 层次/体系/模块 | 结构图 | PIL |
| data | 数据/指标 | 百分比/增长/统计 | 数据可视化 | python-pptx |
| concept | 是什么/定义/核心/标准/经验/案例 | 概念/原理/本质 | 概念示意图 | ImageGen |
| list | （无特定关键词） | 3+ 编号/项目符号 | 图标卡片组 | PIL |

**标题消歧规则**（优先级高于打分）：
- 标题含"对比|区别|vs" → comparison（覆盖 timeline）
- 标题含"结构|目录|要素|架构" → hierarchy（覆盖 process）
- 标题含"标准|法则|规范|经验|案例" → concept（覆盖 timeline/process）

**位置启发式规则**：

| 文字量 | 位置策略 | 坐标（英寸） |
|--------|---------|-------------|
| 封面/时间线/对比 | 全宽 | left=0.8, top=1.0, width=11.7 |
| 正文>200字 | 右侧缩小 | left=8.2, top=1.5, width=4.5 |
| 正文80-200字 | 右侧标准 | left=7.5, top=1.2, width=5.3 |
| 正文>0且<80字 | 右侧加大 | left=6.7, top=1.2, width=6.0 |
| 仅标题 | 居中或全宽 | left=3.5, top=1.5, width=6.3 |

**Agent 工作流**（含数据提取）：
1. 构建"纯文字 PPTX"（仅标题+正文，无配图）
2. 运行 `suggest_illustrations.py --scenario <场景>` 获取建议 + 数据提取
3. 审阅建议，检查 `data_status`：`auto` 的直接用，`manual` 的手动补充 `data`
4. 按 `data_status=auto` 的建议，运行 `gen_pil_illustrations.py --from-pptx` 一键生成 PIL 配图
5. 对 `generation_method=ImageGen` 的页面，调用 ImageGen + `gen_illustrations.py` 后处理
6. 用输出的 `embed_config` 驱动 `embed_illustrations.py` 嵌入
7. 走配图门禁 → 构建 → 评分流程

### 配图工具链（5 个脚本）

配图从建议到生成到嵌入到门禁，由以下 5 个脚本组成自动化管道：

| 脚本 | 职责 | 触发时机 |
|------|------|---------|
| `suggest_illustrations.py` | **内容感知配图建议 + 数据提取**：分析文本→推荐类型/方式/位置→自动提取标签/阶段/项目等结构化数据 | 纯文字 PPTX 构建后、配图生成前 |
| `gen_pil_illustrations.py` | **PIL 配图生成**：支持 `--from-pptx` 一键模式（自动调用 suggest→映射类型→生成），也支持 `--config` 手动模式 | suggest 输出后，或手动编写配置后 |
| `gen_illustrations.py` | ImageGen 后处理：白边裁剪 + 按页号重命名 | Agent 调用 ImageGen 生成 PNG 后 |
| `embed_illustrations.py` | JSON 配置驱动的 `add_picture()` 嵌入 | 配图门禁通过后、构建 PPT 时 |
| `gate_image_coverage.py` | 配图覆盖率门禁检测（≥30%，可调） | 配图完成后、构建 PPT 前 |

**管道流程**：
```
纯文字 PPTX（已构建标题+正文）
        │
        v
suggest_illustrations.py input.pptx -o .temp/suggestions.json --scenario telecom
        │  分析每页内容，输出配图建议（类型/方式/位置/提示词）
        │  自动提取结构化数据（stages/items/steps 等）→ data 字段
        │  同时输出 gen_config[]（含 data+style）和 embed_config[]
        │  data_status: auto=可直接生成, manual=需人工补充
        v
┌─ data_status=auto 的 PIL 类型页面 ─────────────────────────┐
│  gen_pil_illustrations.py --from-pptx input.pptx            │
│      --output-dir .temp/illu --scenario telecom --verbose   │
│  一键生成：自动调用 suggest → 类型映射 → 数据验证 → PIL 渲染 │
└─────────────────────────────────────────────────────────────┘
        │
┌─ generation_method=ImageGen 的页面 ─────────────────────────┐
│  Agent 调用 ImageGen → gen_illustrations.py 后处理           │
└─────────────────────────────────────────────────────────────┘
        │
        v
embed_illustrations.py input.pptx -o illustrated.pptx --config embed_config.json --images dir/ --clean-placeholders
        │  按 JSON 配置 add_picture() 嵌入，清理空占位符
        v
gate_image_coverage.py illustrated.pptx --threshold 0.3
        │  覆盖率 ≥ 30%？PASS → 继续；FAIL → 补图
        v
后续：fix_ppt.py → 评分验证 → 交付
```

**embed_config.json 格式**：
```json
[
  {"slide": 2, "image": "02_timeline.png", "left": 7.5, "top": 2.0, "width": 5.3},
  {"slide": 6, "image": "06_staircase.png", "position": "right"},
  {"slide": 10, "image": "10_structure.png", "position": "full"}
]
```
- 精确模式：指定 `left`/`top`/`width`（高度自动按比例计算）
- 预设模式：指定 `position` = `right`/`left`/`center`/`full`（自动计算位置和尺寸）

### 配图类型速查

| 页面类型 | 必备配图 | 生成方式 | 生成指引 |
|---|---|---|---|
| 封面页 | 场景大图 / 抽象背景图 | **ImageGen** | 主题关键词 + 专业风格 + 宽幅构图 |
| 章节分隔页 | 章节主题意境图 | **ImageGen** | 章节关键词 + 简洁意境 + 大留白 |
| 概念阐述页 | 概念示意图 / 流程图 / 架构图 | **SVG** | 用 LLM 生成 SVG 代码，直接嵌入 PPTX（svg_to_pptx.py）；参见下方"SVG 技术图生成"章节 |
| 数据展示页 | 数据可视化图表（柱/折/饼/雷达等） | **python-pptx 原生**（主）/ **SVG**（辅） | 优先用 python-pptx 原生图表（可编辑数据）；复杂布局或装饰性图表面板可用 SVG 生成后 svg_to_pptx.py 嵌入 |
| 案例展示页 | 案例场景图 / 产品截图 | **ImageGen** | 真实场景感 + 专业光效 |
| 总结/结尾页 | 呼应封面的收尾图 | **ImageGen** | 与封面风格统一 + 收束感 |

> **SVG优先原则**：架构图、流程图、概念示意图、数据流图等"技术图"一律用 SVG 方式生成（精确可控、风格统一、矢量可编辑，直接嵌入 PPTX）；场景图、照片感配图用 ImageGen 补充。

### 红线规则

1. **禁止纯文字页** — 每页文字面积占比 ≤ 60%；整页有效内容填充率须在 60%–70% 区间（详见 [references/element-ratio-scoring.md](references/element-ratio-scoring.md)）；超过即触发 `text_heavy_deck` / `low_fill_rate` 反模式
2. **非数据页必须有配图** — 概念/阐述/案例页至少 1 张配图或示意图
3. **数据页以图表为主** — 优先用 python-pptx 原生图表，辅以 ≤ 3 句结论性文字
4. **配图先于排版** — 必须先批量生成配图再构建 PPT；**不得先写文字再找图凑**
5. **配图风格统一** — 同一份 PPT 所有配图保持一致视觉风格（扁平/线性/照片感），禁止混搭
6. **文字是辅助** — 每页文字不超过 5 行/50 词，关键信息用 14-16pt 强调色结论句呈现
7. **配图覆盖率 ≥ 30%** — N 页 PPT 中有效配图（ImageGen 配图 + python-pptx 原生图表）总数 ≥ 总页数 × 0.3；纯文字页 ≤ 2 页（封面/封底除外）；目录页、章节分隔页可豁免配图但不豁免视觉素材（可用色块/图标/装饰条）；覆盖率 ≥ 50% 为 GOOD 级别
8. **配图门禁强制** — 配图生成未达标时，禁止进入 PPT 构建步骤；违反此规则导致的"先写文字后补图"行为视为流程违规

### 设计系统强制规范（Design System Gate）

> **以下规则在 brainstorming 阶段必须确定，planning 阶段必须体现，execution 阶段必须执行。违反任一规则 = 流程违规，评分时自动触发反模式扣分。**
>
> 这些规则来自实际 PPT 制作中反复出现的问题，每条规则都对应至少一个评分脚本可检测的反模式。

#### DS-1 布局网格规范

| 规则 | 要求 | 违反触发 |
|------|------|----------|
| **禁止上文下图** | 内容页不得使用"文字全在上半区、图片全在下半区"的固定布局；必须使用左文右图分栏、卡片网格、或图文混排 | `top_text_bottom_image` |
| **内容必须有容器** | >3 个文本块的内容页必须使用半透明卡片（圆角矩形）包裹信息，禁止文字直接平铺在背景上 | `no_card_containers` |
| **统一左边缘** | 所有内容页的正文左边缘坐标差 ≤ 0.5 英寸，使用统一页边距 | `inconsistent_alignment` |
| **图片不贴边** | 图片距幻灯片边缘 ≥ 3% 安全边距 | `image_at_edge` |
| **禁止空方块** | 卡片/容器背景面积与内部内容面积之比不得超过 1.67:1（即填充率 ≥ 60%）。**禁止使用 `add_bg()` + `add_rich_textbox()` 组合创建固定高度的卡片背景再加文字**——这是空方块的根因。卡片高度必须由内容自然撑开，或使用 `add_table()` 表格布局替代（表格行高自动适配内容） | `hollow_container` / `low_fill_rate` |

> **空方块预防核心规则**：凡是呈现"列表型"、"对比型"、"参数型"内容（如术语释义、维度对比、趋势罗列），**优先使用 `add_table()` 表格布局**，禁止使用 `add_bg()` + `add_rich_textbox()` 卡片组合。表格行高自动适配内容，从根本上消除空方块。

#### DS-2 色彩角色分配规范

每种颜色必须有且仅有一个语义角色，禁止同一颜色承担多种功能：

| 角色 | 用途 | 占比参考 |
|------|------|----------|
| 背景色 | 页面底色 | 100% 页面 |
| 卡片色 | 信息容器底色 | 30-40% 内容区 |
| 标题文字色 | 一级/二级标题 | 标题元素 |
| 正文文字色 | 段落/要点 | 正文元素 |
| 辅助文字色 | 注释/备注/页码 | ≤10% 文字 |
| 强调色 | 关键词高亮/数据强调 | ≤10% 文字 |
| 警示色 | 痛点/警告/对比 | ≤5% 文字 |

> **禁止**：强调色同时用于插图描边、进度条、图标填充、关键词高亮——这会导致"色彩功能过载"，观众无法通过颜色快速分辨信息等级。

#### DS-3 字号阶梯与关键数据强调规范

| 层级 | 字号 | 用途 |
|------|------|------|
| L1 大标题 | 36-48pt | 页面标题 |
| L2 副标题 | 24-28pt | 章节标题/小节标题 |
| L3 正文 | 16-18pt | 要点/段落 |
| L4 备注 | 12-14pt | 注释/页码/来源 |

**关键数据强调规则（强制）**：
- 百分比（70%、320ms）、大数字（13000+、20份）、时间值等关键数据必须使用 **≥1.5 倍正文字号** 显示
- 关键数据同时使用**加粗 + 强调色**双重强调
- 违反 → `key_data_not_emphasized` 反模式

#### DS-4 代码字体规范

代码片段、文件路径（SKILL.md、config.json）、函数名（def ai_code_assistant()）、CLI 命令（--flag）、技术术语（GPT-4o、OpenClaw）必须使用**等宽字体**（Consolas / Courier New / Source Code Pro）。

> 违反 → `code_without_monospace` 反模式。等宽字体提升代码辨识度，与正文形成视觉区分。

#### DS-5 品牌元素规范

| 元素 | 要求 | 适用页面 |
|------|------|----------|
| 品牌 LOGO | 每页右上角或左上角 | 全部内容页 |
| 页眉品牌栏 | 顶部 60-80px 高的品牌色条 | 全部内容页 |
| 章节进度条 | 底部进度条显示当前章节位置 | 全部内容页 |
| 章节标注 | **禁止每页重复章节文字**；用进度条/页眉导航替代 | 全部内容页 |

> 违反 → `repeated_chapter_labels` + `no_brand_consistency` 反模式

#### DS-6 配图一致性规范

| 规则 | 要求 |
|------|------|
| 底色统一 | 所有配图底色必须与幻灯片背景色一致；深色主题用深底配图，禁止白底插图混入 |
| 亮度克制 | 配图亮度不得超过正文文字亮度；禁止荧光发光特效抢夺视觉焦点 |
| 信息承载 | 配图必须有标注/分层/业务逻辑，禁止纯装饰无信息价值的插图 |
| 风格统一 | 全 deck 统一一种视觉风格（扁平/线性/照片感），禁止混搭 |

#### DS-7 章节过渡规范

章节之间必须有视觉过渡：章节分隔页使用色块/分割线/全幅图片，不得直接从上一章节内容页跳到下一章节内容页。

#### DS-8 暗色主题特殊规则

| 规则 | 要求 | 原因 |
|------|------|------|
| 非中性色阈值 | 允许 8 种非中性色（浅色主题为 5 种） | 暗色主题需要更多色阶区分层次 |
| 对比度检查 | 使用 WCAG 对比度公式，检测实际背景色 | 禁止假设白色背景 |
| 中间过渡色 | 必须有浅蓝灰/浅灰等中间色区分二级备注 | 避免色彩层级单一 |
| 辅助文字亮度 | 浅灰色辅助文字亮度 ≥ 60%（适配投屏远距离观看） | 避免投影模糊 |

---

## SVG 技术图生成（LLM→SVG→PPTX）

> 适用于配图类型速查表中标记为 **SVG** 的页面（架构图/流程图/概念示意图/数据流图等）。灵感来源于 [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) 和 [ppt-master](https://github.com/hugohe3/ppt-master) 项目。

### 核心原理

LLM 直接生成 SVG 代码（纯文本），再通过 ppt-master 的 `svg_to_pptx.py` 转为原生可编辑 PPTX。SVG 是文本格式，LLM 生成精度远高于 ImageGen 的像素级生成，且风格完全可控。无需中间 PNG 转换步骤。

### 生成工作流

```
[1. 分类]     → 根据配图类型速查表判断该页用 SVG 还是 ImageGen
       │
       v
[2. 写 SVG]   → LLM 用 Python list 方式生成 SVG 代码（见下方技术规则）
       │
       v
[3. 验证]     → python -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')"
       │
       v
[4. 审图]     → image_understanding 审核结构/色彩/标签是否正确
       │              不合格 → 修改 SVG 重审；最多重试 2 次
       v
[5. 入 PPTX]  → svg_to_pptx.py 将 SVG 转为原生 PPTX 元素（直接嵌入，无需转 PNG）
```

### 备选：SVG→PNG（仅在需要独立 PNG 时使用）

若某些场景需要独立的 PNG 文件（如 `image_understanding` 审图需要 PNG 输入），可用以下方式转换：

```bash
# 方案 A：puppeteer（推荐，Windows 可用，需 Node.js）
# npm install puppeteer  # 首次安装
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
  const svg = require('fs').readFileSync('.temp/illustrations/diagram.svg', 'utf-8');
  await page.setContent('<img src=\"data:image/svg+xml;base64,' + Buffer.from(svg).toString('base64') + '\" style=\"width:100%\" />', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: '.temp/illustrations/diagram.png', type: 'png', omitBackground: true, fullPage: true });
  await browser.close();
  console.log('PNG exported');
})();
"

# 方案 B：cairosvg（若系统已安装 Cairo 库）
# python -c "import cairosvg; cairosvg.svg2png(url='.temp/illustrations/diagram.svg', write_to='.temp/illustrations/diagram.png', scale=2)"

# 方案 C：rsvg-convert（若已安装）
# rsvg-convert -w 1920 .temp/illustrations/diagram.svg -o .temp/illustrations/diagram.png
```

### SVG 技术规则

**1. 生成方式（强制）**：使用 Python list 逐行拼接，不得直接输出大段 SVG 字符串
```python
lines = []
lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600">')
lines.append('  <defs>...</defs>')
# ... 每行单独 append ...
lines.append('</svg>')
with open('.temp/illustrations/diagram.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
```

**2. ViewBox 标准**：`0 0 960 600`（标准）、`0 0 960 800`（高图）、`0 0 1200 600`（宽图）

**3. 字体**：禁止 `@import` 外部字体（cairosvg 无法获取）；用内联 `<style>` 指定系统字体栈。

**4. 电信风格配色**（SVG 内硬编码）：
| 用途 | 颜色 |
|------|------|
| 标题/强调 | `#E60012`（中国电信红，品牌标准色） |
| 主色边框 | `#E60012` |
| 背景 | `#FFFFFF` |
| 次要文字 | `#333333` |
| 辅助线 | `#E0E0E0` |
| 数据流箭头 | `#2563EB` |
| 控制流箭头 | `#EA580C` |

**5. 语义形状词汇**：
| 概念 | 形状 |
|------|------|
| 用户/人 | 圆 + 身体路径 |
| LLM/模型 | 圆角矩形 + 双边框 |
| Agent/编排器 | 六边形 |
| 数据库/存储 | 圆柱体 |
| 工具/函数 | 齿轮矩形 |
| API/网关 | 六边形（单边框） |
| 决策 | 菱形 |
| 外部服务 | 虚线边框矩形 |

**6. 箭头语义**：
| 流类型 | 颜色 | 线型 | 含义 |
|--------|------|------|------|
| 主数据流 | `#2563EB` | 2px 实线 | 请求/响应 |
| 控制/触发 | `#EA580C` | 1.5px 实线 | 系统间调用 |
| 内存读 | `#059669` | 1.5px 实线 | 检索 |
| 内存写 | `#059669` | 1.5px 虚线 `5,3` | 存储 |
| 异步/事件 | `#6B7280` | 1.5px 虚线 `4,2` | 非阻塞 |

**7. 文字最小 12px**，标签 13-14px，子标签 11px，标题 16-18px

**8. 箭头标签**：优先偏移放置（距箭头线 6-8px），仅在偏移后仍与其他元素冲突时才加背景矩形

**9. CJK 文字注意**：cairosvg 可能无法渲染中文，若 SVG 内含中文文字：
- 方案 A：中文文字改用英文/拼音标注
- 方案 B：转 PNG 改用 `rsvg-convert -w 1920 file.svg -o file.png`
- 方案 C（最高保真）：用 puppeteer（headless Chrome）渲染

### SVG 验证

```bash
# XML 语法验证
python -c "import xml.etree.ElementTree as ET; ET.parse('.temp/illustrations/diagram.svg')" && echo "Valid XML"

# SVG→PPTX 渲染验证（ppt-master 管线）
python scripts/svg_to_pptx.py --input .temp/svg_output/ --output .temp/_test.pptx && echo "Renders OK" && del .temp\_test.pptx
```

---

## 临时文件清理（强制）

> 适用于**所有工作流**。技能执行过程中产生的大量中间文件仅用于过程校验，交付后必须清理，**仅保留最终输出的 PPTX 文件**。
>
> ?? **不得跳过以下任意步骤。每步必须执行并通过验证条件后才可继续下一步。**

### 须保留 vs 须删除

**仅保留**：最终输出的 `.pptx`（`*_fixed.pptx` 或用户指定文件名）

**须全部删除**（统一写入 `.temp/`，不得散落）：

| 文件类型 | 路径模式 |
|---|---|
| 渲染 PNG | `.temp/render_*/slide_*.png` |
| 渲染清单 | `.temp/render_*/render_manifest.json` |
| 评分报告 | `.temp/*_report*.json` `.temp/*_report*.md` |
| 对比报告 | `.temp/compare_*.json` `.temp/compare_*.md` |
| AI 生成配图（ImageGen） | `.temp/illustrations/*.png`（非 SVG 生成） |
| SVG 源文件 | `.temp/illustrations/*.svg` |
| SVG→PNG 配图 | `.temp/illustrations/*.png`（SVG 转换产出） |
| SVG 逐页输出（ppt-master） | `.temp/svg_output/` |
| SVG 后处理输出（ppt-master） | `.temp/svg_final/` |
| Before/after 对比图 | `.temp/before/` `.temp/after/` |
| 过渡 PPTX | `.temp/*_before.pptx` `.temp/*_intermediate.pptx` |
| 模板设计规格书 | `.temp/template_design_spec.json` |
| 页面版式映射 | `.temp/page_plan.json` |

### 强制清理 Checklist（4 步，每步不得跳过）

**Step C1：确认最终 PPTX 存在且可读**

```
动作：检查最终 .pptx 文件是否存在 + 文件大小 > 0
验证：文件路径有效 && size > 0 → 通过
失败处理：终止清理，保留 .temp/ 供排查，向用户报告失败原因
```

**Step C2：列出待删除清单**

```
动作：扫描 .temp/ 目录，列出本次任务产生的全部文件（含子目录）
验证：清单 ≠ 空 → 确认后继续（若 .temp/ 已为空则跳至 C4）
```

**Step C3：逐类删除**

```
动作：按上表"须全部删除"分类，逐类删除 .temp/ 下对应的文件和子目录
验证：删除后再次扫描 .temp/，确认上述 13 类文件均已清除
      若仍有残留 → 再次删除残留项 → 再验证（最多重试 2 次）
失败处理（重试 2 次后仍有残留）：向用户报告残留文件列表，由用户决定是否手动清理
```

**Step C4：报告交付路径**

```
动作：向用户输出最终 PPTX 的完整绝对路径
格式："已交付：<绝对路径>（临时文件已清理）"
验证：路径已在输出中呈现 → 完成
```

> **异常安全**：若 Step C1 确认最终 PPTX 不存在或不可读，**终止清理**，保留 `.temp/` 供排查，向用户明确报告失败，等待用户确认后再决定是否清理。

---

## 环境

依赖（一次性安装到隔离 venv，不污染用户环境）：

```bash
# Python 依赖（或 pip install -r scripts/requirements.txt）
pip install --target <venv>/Lib/site-packages \
    python-pptx Pillow PyMuPDF pywin32 lxml XlsxWriter
```

> **注意**：示例命令中使用 `python` 调用脚本。请根据实际环境替换为完整的 Python 路径（如 `C:\Python314\python.exe`）。

渲染后端（按可用性优先级）：
- **LibreOffice (soffice)** — 跨平台、沙箱内可用，本技能默认方案。PPTX → PDF → PyMuPDF → PNG。
- **PowerPoint COM (pywin32)** — Windows + 装了 PowerPoint 时保真度最高，但**沙箱内无法启动 COM 服务**，需要桌面会话。

`scripts/render_slides.py --method auto` 会先尝试 PowerPoint COM，失败则回退 LibreOffice。

---

## Workflow 1: 评分

### Step 1: 渲染 PPTX 为图片

```powershell
python scripts/render_slides.py <input.pptx> --output-dir .temp/render/ --dpi 150 --method libreoffice
```

### Step 2: 结构化评分

```powershell
python scripts/score_ppt_pages.py <input.pptx> --scenario <scenario> --output .temp/score_report.json
```

**9 维度加权评分**（满分 10）：

| 维度 | 权重 | 检测方式 |
|------|------|---------|
| whitespace（留白与填充率） | 13% | 元素占比量化（含视觉均衡度子维度，30% 权重） |
| type_scale（字号阶梯） | 14% | Major Third 比例检测 |
| color_harmony（配色和谐） | 14% | 60-30-10 规则 + 色阶系统 |
| alignment（对齐） | 14% | 网格对齐检测 |
| spacing（间距节奏） | 9% | 4/8px 网格检测 |
| imagery（配图质量） | 9% | 配图覆盖率 + 拉伸检测 |
| consistency（一致性） | 9% | 跨页字体/配色/风格统一 |
| hierarchy（视觉层次） | 8% | 标题-正文-注释三级层次 |
| layout（布局） | 10% | 容器填充率、象限空白、图片触边检测 |

> **元素占比与 9 维度整合方式（方案 B）**：元素占比（页面填充率/容器填充率/视觉均衡度）作为 `whitespace` 维度的子维度，占该维度 30% 权重。即 whitespace = 0.7 × 留白评分 + 0.3 × 元素占比评分。layout 维度独立评估页面元素空间分布（空旷容器、空白象限、触边问题）。详见 [references/element-ratio-scoring.md](references/element-ratio-scoring.md)。

**59 种反模式自动检测**（按 10 维度分类，编号规则 AP-{维度缩写}-{序号}）：

| # | 编号 | 反模式 ID | 维度 | 严重度 | 扣分 |
|---|------|-----------|------|--------|------|
| 1 | AP-WS-01 | `text_heavy_deck` | whitespace | 严重 | -3 |
| 2 | AP-WS-02 | `wall_of_text` | whitespace | 高危 | -1.5 |
| 3 | AP-WS-03 | `high_text_density` | whitespace | 中危 | -1 |
| 4 | AP-WS-04 | `low_fill_rate` | whitespace | 中危 | -1.5 |
| 5 | AP-TS-01 | `too_many_fonts` | type_scale | 严重 | -2 |
| 6 | AP-TS-02 | `unprofessional_font` | type_scale | 严重 | -2 |
| 7 | AP-TS-03 | `cjk_text_no_cjk_font` | type_scale | 高危 | -1.5 |
| 8 | AP-TS-04 | `weak_type_scale` | type_scale | 高危 | -1.5 |
| 9 | AP-TS-05 | `extreme_type_scale` | type_scale | 中危 | -1 |
| 10 | AP-CH-01 | `too_many_colors` | color_harmony | 严重 | -2 |
| 11 | AP-CH-02 | `ai_purple_palette` | color_harmony | 中危 | -1 |
| 12 | AP-CH-03 | `oversaturated_pure_rgb` | color_harmony | 中危 | -1 |
| 13 | AP-CH-04 | `overuse_accent` | color_harmony | 中危 | -1 |
| 14 | AP-CH-05 | `pure_black_text` | color_harmony | 低危 | -0.5 |
| 15 | AP-CH-06 | `pure_white_card` | color_harmony | 低危 | -0.5 |
| 16 | AP-CH-07 | `rainbow_text` | color_harmony | 高危 | -1.5 |
| 17 | AP-CH-08 | `inconsistent_colors` | color_harmony | 高危 | -1.5 |
| 18 | AP-AL-01 | `no_margins` | alignment | 中危 | -1 |
| 19 | AP-AL-02 | `three_equal_cards` | alignment | 中危 | -1 |
| 20 | AP-AL-03 | `misaligned_elements` | alignment | 高危 | -1.5 |
| 21 | AP-SP-01 | `irregular_spacing` | spacing | 中危 | -1 |
| 22 | AP-SP-02 | `inconsistent_spacing` | spacing | 中危 | -1 |
| 23 | AP-SP-03 | `orphan_widow` | spacing | 低危 | -0.5 |
| 24 | AP-IM-01 | `low_res_image` | imagery | 中危 | -1 |
| 25 | AP-IM-02 | `stretched_image` | imagery | 严重 | -2 |
| 26 | AP-IM-03 | `clipart_style` | imagery | 中危 | -1 |
| 27 | AP-CO-01 | `inconsistent_fonts` | consistency | 严重 | -2 |
| 28 | AP-CO-02 | `default_template` | consistency | 低危 | -0.5 |
| 29 | AP-HI-01 | `tiny_text` | hierarchy | 高危 | -1.5 |
| 30 | AP-HI-02 | `no_visual_hierarchy` | hierarchy | 严重 | -2 |
| 31 | AP-HI-03 | `long_bullet` | hierarchy | 中危 | -1 |
| 32 | AP-HI-04 | `too_many_bullets` | hierarchy | 高危 | -1.5 |
| 33 | AP-HI-05 | `bullet_soup` | hierarchy | 中危 | -1 |
| 34 | AP-HI-06 | `low_contrast` | hierarchy | 中危 | -1 |
| 35 | AP-HI-07 | `chart_without_message` | hierarchy | 中危 | -1 |
| 36 | AP-HI-08 | `code_without_monospace` | hierarchy | 中危 | -1 |
| 37 | AP-HI-09 | `key_data_not_emphasized` | hierarchy | 中危 | -1 |
| 38 | AP-LA-01 | `top_text_bottom_image` | layout | 高危 | -1.5 |
| 39 | AP-LA-02 | `no_card_containers` | layout | 中危 | -1 |
| 40 | AP-LA-03 | `image_at_edge` | layout | 低危 | -0.5 |
| 41 | AP-LA-04 | `bare_text_no_card` | layout | 中危 | -1 |
| 42 | AP-LA-05 | `table_no_zebra` | layout | 中危 | -1 |
| 43 | AP-LA-06 | `table_weak_header` | layout | 中危 | -1 |
| 44 | AP-LA-07 | `mixed_numbering` | layout | 低危 | -0.5 |
| 45 | AP-LA-08 | `unbalanced_layout` | layout | 中危 | -1 |
| 46 | AP-DE-01 | `repeated_chapter_labels` | deck | 中危 | -1 |
| 47 | AP-DE-02 | `inconsistent_alignment` | deck | 高危 | -1.5 |
| 48 | AP-DE-03 | `no_brand_consistency` | deck | 中危 | -1 |
| 49 | AP-DE-04 | `inconsistent_margins` | deck | 高危 | -1.5 |
| 50 | AP-DE-05 | `inconsistent_section_pos` | deck | 中危 | -1 |
| 51 | AP-DE-06 | `cover_ending_mismatch` | deck | 中危 | -1 |
| 52 | AP-DE-07 | `density_outlier` | deck | 中危 | -1 |
| 53 | AP-DE-08 | `no_header_navigation` | deck | 高危 | -1.5 |
| 54 | AP-LA-09 | `hollow_container` | layout | 高危 | -2 |
| 55 | AP-WS-05 | `high_fill_rate` | whitespace | 低危 | -0.5 |
| 56 | AP-WS-06 | `empty_quadrant` | whitespace | 中危 | -1 |
| 57 | AP-LA-10 | `top_heavy` | layout | 中危 | -1 |
| 58 | AP-DE-09 | `deck_too_many_fonts` | deck | 高危 | -1.5 |
| 59 | AP-DE-10 | `deck_too_many_colors` | deck | 高危 | -1.5 |

> **去重规则**：
> 1. `text_heavy_deck`（整页文字面积占比 > 60%）与 `low_fill_rate`（有效内容填充率 < 60%）不双重扣分——同一页只扣更严重的那一项。
> 2. `hollow_container`（容器内部填充率 < 60%）与 `low_fill_rate` **可叠加**（不同维度：容器级 vs 页面级）。
> 3. `wall_of_text`（单文本框 > 120 词）与 `text_heavy_deck` 可叠加（不同维度：局部 vs 全局）。
> 4. deck 级反模式（AP-DE-*）与同名 page 级反模式不双重扣分——`deck_too_many_fonts` 与 `too_many_fonts` 只在 deck 级扣一次；`deck_too_many_colors` 与 `too_many_colors` 同理。
> 5. `empty_quadrant`（某象限完全无内容）与 `low_fill_rate`（填充率 < 60%）不双重扣分——同一页只扣更严重的 `low_fill_rate`；若填充率 >= 60% 仍有空象限，才扣 `empty_quadrant`。

**场景化权重切换**（`--scenario` 参数）：

| 场景 | whitespace | type_scale | color_harmony | alignment | spacing | imagery | consistency | hierarchy | layout |
|------|-----------|------------|---------------|-----------|---------|---------|-------------|-----------|--------|
| executive | 18% | 9% | 9% | 13% | 9% | 5% | 9% | 18% | 10% |
| marketing | 9% | 9% | 18% | 9% | 9% | 13% | 9% | 14% | 10% |
| data | 5% | 9% | 9% | 13% | 9% | 9% | 9% | 27% | 10% |
| creative | 13% | 13% | 18% | 5% | 9% | 13% | 5% | 14% | 10% |
| gov | 5% | 18% | 9% | 18% | 9% | 5% | 13% | 13% | 10% |
| telecom | 9% | 13% | 18% | 13% | 9% | 5% | 13% | 10% | 10% |
| default | 13% | 14% | 14% | 14% | 9% | 9% | 9% | 8% | 10% |

### Step 3: 视觉模型评分（可选）

对每页渲染图片，用 AI 视觉模型按 4 维度打分（visual_hierarchy、color_harmony、alignment_spacing、imagery_quality），与结构化评分加权合并。

### Step 4: 输出报告

评分报告包含：
- 每页 9 维度分数 + 加权总分
- 反模式命中列表（含严重度、位置、扣分）
- 整体评分 + 改进建议
- **Token 输出**：提取设计 token（color.primary、font.heading、font.body、spacing.base、radius.card、elevation.shadow）

---

## Workflow 2: 修复

### Step 1: 评分（先评后修）

走工作流 1，获取评分报告和反模式列表。

### Step 2: 自动修复

```powershell
python scripts/fix_ppt.py <input.pptx> --output <fixed.pptx> --all --pairing <pairing> --palette <palette> --margin-in 0.5
```

**修复能力**：

| 修复项 | 参数 | 说明 |
|--------|------|------|
| 字体统一 | `--fonts --pairing <id>` | 按 font-pairings.md 方案统一 |
| 配色统一 | `--colors --palette <id>` | 按 color-palettes.md 方案统一 |
| 页边距 | `--margins --margin-in <n>` | 统一页边距（英寸） |
| 图片拉伸 | `--images` | 检测并修复拉伸图片 |
| 段落拆分 | `--bullets` | 长段落拆为要点 |
| 背景统一 | `--theme-bg --bg-hex <hex>` | 统一背景色 |
| 字号阶梯 | `--type-scale --ratio <r>` | Major Third 等比例阶梯 |
| 间距网格 | `--spacing-grid --grid-in <n>` | 4/8px 间距对齐 |

### Step 3: 验证

```powershell
python scripts/render_slides.py <fixed.pptx> --output-dir .temp/after/ --dpi 150
python scripts/score_ppt_pages.py <fixed.pptx> --scenario <scenario> --output .temp/score_report_after.json
```

对比修复前后评分，确认改善。

---

## Workflow 3: 完整（评分 + 修复）

1. 走工作流 1（评分）
2. 走工作流 2（修复）
3. 再走工作流 1（验证修复效果）
4. 输出对比报告（before/after 评分 + 改善幅度）

---

## Workflow 4: 电信风格 PPT 生成

> 严格遵循电信风格设计范式，使用内置电信模板，电信红色强制规范 #E60012。

### 电信风格设计范式

**核心原则**：电信风格 PPT 不使用全幅配图，而是以**红白装饰 + Emoji 图标卡片 + 精确坐标布局**为视觉核心。

**强制规则**：
1. **使用 Blank 布局** — 不使用模板自带版式，仅用 Blank 布局 + 手动放置元素
2. **电信红 #E60012** — 品牌标准色，用于标题、装饰条、强调元素（**硬性约束，不得替换**）
3. **红白配色** — 白色背景 + 电信红装饰 + 深灰文字
4. **Logo 右上角** — 每页右上角放置电信 Logo（2.1×0.6 英寸，从 `assets/logo.png` 提取）
5. **Emoji 图标卡片** — 用 Emoji 替代图标库，每张卡片含 Emoji + 标题 + 描述
6. **不用全幅配图** — 电信风格不用全幅背景图，用色块/装饰条/Emoji 卡片营造视觉

### 电信红色强制规范

**#E60012 是中国电信品牌标准色，在电信风格 PPT 中具有最高优先级。**

1. **主色锁定**：所有电信风格 PPT 中，主色（primary）必须为 `#E60012`，不得替换为其他红色
2. **配图色调约束**：ImageGen 生成的配图中，若包含红色元素，必须与 `#E60012` 色调一致
3. **fix_ppt.py 硬性约束**：`fix_ppt.py --palette telecom-red` 会强制将所有主色替换为 `#E60012`，不受用户自定义覆盖
4. **模板 VI 元素豁免**：模板自带的 VI 元素（Logo、装饰条等）保持原色，不强制替换

### 电信风格精确坐标（5 种页面类型）

**类型 A：封面页**
```
Logo:        Left=8.9", Top=0.3", Width=2.1", Height=0.6"
主标题:      Left=0.8", Top=2.0", Width=8.4", Height=1.2"  Font=微软雅黑 36pt Bold #333333
副标题:      Left=0.8", Top=3.3", Width=8.4", Height=0.6"  Font=微软雅黑 18pt #666666
红色装饰条:  Left=0.8", Top=1.8", Width=2.0", Height=0.06" Fill=#E60012
日期/部门:   Left=0.8", Top=4.2", Width=4.0", Height=0.4"  Font=微软雅黑 12pt #999999
```

**类型 B：内容页（3 卡片）**
```
Logo:        Left=8.9", Top=0.3", Width=2.1", Height=0.6"
页标题:      Left=0.6", Top=0.3", Width=8.0", Height=0.5"  Font=微软雅黑 24pt Bold #333333
红色装饰条:  Left=0.6", Top=0.85", Width=1.5", Height=0.04" Fill=#E60012
卡片1:       Left=0.6", Top=1.2", Width=2.7", Height=自适应  Fill=#F5F5F5  Radius=0.1"
  Emoji:     Left=1.5", Top=1.4", Width=0.8", Height=0.8"  Font=Segoe UI Emoji 32pt
  卡片标题:  Left=0.8", Top=2.3", Width=2.3", Height=0.4"  Font=微软雅黑 14pt Bold #333333
  卡片描述:  Left=0.8", Top=2.8", Width=2.3", Height=自适应  Font=微软雅黑 11pt #666666
卡片2:       Left=3.6", Top=1.2", Width=2.7", Height=自适应  (同卡片1结构，Left偏移3.0")
卡片3:       Left=6.6", Top=1.2", Width=2.7", Height=自适应  (同卡片1结构，Left偏移6.0")
```
> **自适应高度规则**：卡片高度应根据内容自动适配，不再使用固定3.8"。
> 推荐使用 `add_table()` 构建卡片内容，表格行会自动高度适配。
> 如使用 `add_bg() + add_rich_textbox()`，卡片高度 = 文本实际高度 + 上下内边距(0.3")。
> **禁止**声明大于文本实际高度2.5倍的卡片高度。

**类型 B2：内容页（2 卡片 + 右侧要点）**
```
Logo:        Left=8.9", Top=0.3", Width=2.1", Height=0.6"
页标题:      Left=0.6", Top=0.3", Width=8.0", Height=0.5"  Font=微软雅黑 24pt Bold #333333
红色装饰条:  Left=0.6", Top=0.85", Width=1.5", Height=0.04" Fill=#E60012
卡片1:       Left=0.6", Top=1.2", Width=4.0", Height=自适应  Fill=#F5F5F5  Radius=0.1"
卡片2:       Left=0.6", Top=自适应(卡片1底部+0.3"), Width=4.0", Height=自适应  Fill=#F5F5F5  Radius=0.1"
右侧要点区:  Left=5.0", Top=1.2", Width=4.4", Height=自适应
  要点1:     Left=5.2", Top=1.4", Width=4.0", Height=0.5"  Font=微软雅黑 13pt #333333
  要点2:     Left=5.2", Top=2.0", Width=4.0", Height=0.5"  Font=微软雅黑 13pt #333333
  要点3:     Left=5.2", Top=2.6", Width=4.0", Height=0.5"  Font=微软雅黑 13pt #333333
```

**类型 C：数据展示页**
```
Logo:        Left=8.9", Top=0.3", Width=2.1", Height=0.6"
页标题:      Left=0.6", Top=0.3", Width=8.0", Height=0.5"  Font=微软雅黑 24pt Bold #333333
红色装饰条:  Left=0.6", Top=0.85", Width=1.5", Height=0.04" Fill=#E60012
数据卡片1:   Left=0.6", Top=1.2", Width=2.0", Height=1.2"  Fill=#E60012  (白字)
  数值:      Left=0.7", Top=1.3", Width=1.8", Height=0.6"  Font=微软雅黑 28pt Bold #FFFFFF
  标签:      Left=0.7", Top=1.9", Width=1.8", Height=0.3"  Font=微软雅黑 10pt #FFFFFF
数据卡片2:   Left=2.8", Top=1.2", Width=2.0", Height=1.2"  Fill=#E60012  (同上)
数据卡片3:   Left=5.0", Top=1.2", Width=2.0", Height=1.2"  Fill=#E60012  (同上)
数据卡片4:   Left=7.2", Top=1.2", Width=2.0", Height=1.2"  Fill=#E60012  (同上)
图表区:      Left=0.6", Top=2.7", Width=8.6", Height=2.5"  (python-pptx 原生图表)
```

**类型 D：总结页**
```
Logo:        Left=8.9", Top=0.3", Width=2.1", Height=0.6"
主标题:      Left=0.8", Top=1.5", Width=8.4", Height=0.8"  Font=微软雅黑 28pt Bold #333333
红色装饰条:  Left=0.8", Top=2.4", Width=2.0", Height=0.06" Fill=#E60012
总结要点:    Left=0.8", Top=2.7", Width=8.4", Height=2.0"  Font=微软雅黑 14pt #333333
  要点1-4:   逐行排列，行间距 0.5"
```

### 全局装饰规则

| 元素 | 规范 |
|------|------|
| Logo | 每页右上角，2.1×0.6"，从 `assets/logo.png` |
| 红色装饰条 | 标题下方，宽 1.5-2.0"，高 0.04-0.06"，Fill=#E60012 |
| 页码 | 右下角，微软雅黑 9pt #999999 |
| 卡片圆角 | Radius=0.1"（python-pptx 用 `shape.adjustments[0] = 0.1`） |
| 卡片背景 | #F5F5F5（浅灰），数据卡片用 #E60012（白字） |
| 字体 | 标题：微软雅黑 Bold；正文：微软雅黑 Regular |
| 配色 | 主色 #E60012，文字 #333333/#666666，辅助 #999999，背景 #FFFFFF/#F5F5F5 |

### Emoji 图标速查（电信风格卡片用）

| 类别 | Emoji | 适用场景 |
|------|-------|---------|
| 技术 | ????????? | 技术架构、系统、工具 |
| 数据 | ???????? | 数据分析、报表、指标 |
| 安全 | ??????? | 安全、认证、加密 |
| 网络 | ?????? | 网络、通信、连接 |
| 云 | ?????? | 云计算、云服务 |
| 用户 | ?????? | 用户、团队、协作 |
| 创新 | ?????? | 创新、目标、战略 |
| 成功 | ???? | 成功、认证、评级 |
| 警告 | ????? | 风险、告警、重要 |
| 流程 | ?????? | 流程、转换、循环 |

### 电信风格工作流步骤

1. **读取模板**：从 `assets/PPT模板.pptx` 获取幻灯片尺寸（13.333×7.5 英寸），**不使用其母版版式**
2. **规划页面类型**：根据内容确定每页用类型 A/B/B2/C/D
3. **生成配图**（如需）：技术图用 SVG→PPTX，场景图用 ImageGen
4. **构建 PPTX**：用 python-pptx 按"电信风格精确坐标"逐页构建
5. **空方块门控检查**（必须通过才能继续）：
   - 运行 `score_ppt_pages.py` 检查 `hollow_container` 反模式
   - 如有页面命中 `hollow_container`，**必须修复后重新构建**，不得跳过
   - 修复方法：将 `add_bg() + add_rich_textbox()` 替换为 `add_table()` 布局
6. **评分验证**：走工作流 1，`--scenario telecom`
7. **交付清理**：走清理 Checklist

---

## Workflow 5: 前端 Token → PPT

1. 读取前端项目的设计 token（Tailwind config / CSS 变量 / Storybook）
2. 按 [references/design-token-mapping.md](references/design-token-mapping.md) 映射为 PPT 参数
3. 用映射后的参数走工作流 2 修复，或走工作流 4 生成电信风格 PPT

---

## Workflow 6: 资产捕获

1. 截取前端组件截图 / SVG 素材
2. 保存到 `.temp/illustrations/`
3. 走工作流 2 或 4 将资产嵌入 PPT

---

## 多版本对比

用 `compare_ppt_versions.py` 对 2+ 个 PPTX 横向排名：

```powershell
python scripts/compare_ppt_versions.py `
    --input v1.pptx v2.pptx v3.pptx `
    --labels "原版" "调色版" "重排版" `
    --scenario marketing `
    --output .temp/compare_report.json `
    --md .temp/compare_report.md
```

输出包含：
- **排名**：按加权总分排序
- **Token 差异表**：哪些设计 token 在版本间不一致
- **反模式对比**：每个版本命中了哪些反模式
- **推荐结论**：综合冠军 + 单维度冠军 + 合并建议

### Step 4: 应用合并建议

报告会给出"用 vX 的 A + vY 的 B"的合并建议，可结合工作流 2（修复）落地：
- 用 `fix_ppt.py --palette <id>` 把推荐配色应用到最优版本
- 用 `fix_ppt.py --type-scale --ratio <r>` 把推荐字号阶梯应用到最优版本

### 输出示例

```json
{
  "versions": [
    {"label": "原版", "file": "v1.pptx", "final_score": 7.2},
    {"label": "调色版", "file": "v2.pptx", "final_score": 7.8},
    {"label": "重排版", "file": "v3.pptx", "final_score": 6.9}
  ],
  "ranking": ["调色版", "原版", "重排版"],
  "scenario_champion": {"scenario": "marketing", "winner": "调色版"},
  "token_diff": {
    "color.primary": {"原版": "1B3A5C", "调色版": "0F4C81", "重排版": "1B3A5C"},
    "color.accent": {"原版": "F59E0B", "调色版": "F59E0B", "重排版": "EF4444"}
  },
  "merge_suggestion": "See Markdown report for details"
}
```

### 限制

- **结构评分 vs 视觉评分**：本脚本只做结构评分（反模式 + token），不调用视觉模型。如需视觉评分，需上游 agent 对每个版本分别跑 `render_slides.py` + 视觉模型，再人工合并。
- **MVP 版本**：当前仅支持结构评分排名，未集成雷达图绘制（报告输出 JSON 数据，可由上游 agent 用其他工具绘制）。

---

## 设计变量映射（场景 → 风格）

| PPT 场景 | `--scenario` | DESIGN_VARIANCE | VISUAL_DENSITY | 推荐布局 | 推荐配色 |
|---|---|---|---|---|---|
| 高管摘要 / 董事会 | `executive` | 3-4 | 2-3 | 居中、对称、极简、大字 | mono-clean / deep-stage |
| 产品发布 / 营销 deck | `marketing` | 6-7 | 3-4 | 分屏、大图、留白慷慨 | charcoal-modern / forest-exec |
| 技术架构评审 | `data` | 5-6 | 5-7 | 网格密集、图多、多区 | slate-pro / charcoal-modern |
| 创意作品集 / 代理商提案 | `creative` | 8-9 | 2-4 | 不对称、杂志感、艺术留白 | deep-stage / 自定义 |
| 数据密集季报 | `data` | 4-5 | 6-8 | 图表为主、紧凑表格、仪表盘 | mono-clean / corp-blue |
| 党政公文 / 政府汇报 | `gov` | 2-3 | 4-5 | 居中对称、章节分明、严肃 | corp-blue + fz-xiaobiaosong+fangsong |
| 电信风格 / 电信汇报 | `telecom` | 3-5 | 4-6 | 严格遵循电信风格设计范式（Blank布局+红白装饰+Emoji卡片）、不用全幅配图 | telecom-red + microsoft-yahei+arial |
| 其他 / 不确定 | `default` | — | — | 按内容判断 | 按内容判断 |

> `--scenario` 参数会同步影响 `score_ppt_pages.py` 的权重和 `compare_ppt_versions.py` 的排名。详见 [references/aesthetic-scoring-rubric.md](references/aesthetic-scoring-rubric.md) 的"场景化权重切换"小节。

---

## 配色调和规则

**分档调和**（7 套配色统一适用）：

| 色彩数量 | 调和策略 | 示例 |
|----------|---------|------|
| 0 色（纯黑白） | 无需调和 | mono-clean |
| 1-2 色 | 互补色或同色系深浅 | telecom-red（#E60012 + 深浅变体） |
| 3-5 色 | 60-30-10 法则 | 主色 60% + 辅色 30% + 强调色 10% |
| ≥6 色 | 必须有统一色相轴或灰度锚点 | 数据可视化色板 |

**去重规则**：`rainbow_text`（单页 ≥6 色）与 `inconsistent_colors`（跨页配色不统一）不双重扣分——同一页只扣更严重的那一项。

---

## 与 pptx / ppt-master 技能的关系

本技能与 `pptx` 技能和 `ppt-master` 技能协作：
- `pptAesthetics` 技能负责**视觉质量规则**（评分 + 修复 + 设计资产 + 配图生成）
- `ppt-master` 技能负责**PPT 构建机制**（SVG→PPTX 流水线：逐页 SVG → `finalize_svg.py` → `svg_to_pptx.py`，产出原生可编辑 PPTX）
- `pptx` 技能负责**简单 PPT 操作**（版式、文本框、形状、图表的粗粒度创建/修改）

新建 PPT 时（先图后文）：规划大纲 → 双轨生成配图（技术图用 SVG→PNG，场景图用 ImageGen）→ 审图 → 用 `ppt-master` 的 SVG→PPTX 流水线构建原生 PPTX（逐页写 SVG，配图嵌入为 `<image>` 引用，`svg_to_pptx.py` 转换）→ 评分验证 → 交付。

修改已有 PPT 时：用 `ppt-master` 的 `template_fill_pptx.py` 纯 OOXML 填充路径，或者直接走工作流 1+2 评分修复。

---

## 参考文档索引

| 文件 | 何时读 |
|---|---|
| [references/ppt-brainstorming.md](references/ppt-brainstorming.md) | 制作任何新 PPT 之前 — 构思内容与视觉方案 |
| [references/ppt-planning.md](references/ppt-planning.md) | 设计审批后、制作 PPT 之前 — 产出台本蓝图 |
| [references/ppt-execution.md](references/ppt-execution.md) | 拿到台本蓝图后 — 按计划逐步构建 |
| [references/aesthetic-scoring-rubric.md](references/aesthetic-scoring-rubric.md) | 评分时（含视觉模型 Prompt、维度标准、反模式扣分） |
| [references/anti-pattern-fixes.md](references/anti-pattern-fixes.md) | 修复时（每个反模式的检测+修复方法） |
| [references/web-design-principles.md](references/web-design-principles.md) | **借鉴 web-design-engineer 审美**（Type Scale 字号阶梯、60-30-10 配色、4/8px 间距节奏、icon 与配图）|
| [references/color-palettes.md](references/color-palettes.md) | 选配色时（7 套方案 + 50-950 色阶系统 + 数据可视化配色 + 色盲安全色板 + 电信红 telecom-red） |
| [references/font-pairings.md](references/font-pairings.md) | 选字体时（5 套中英文搭配 + 按风格定位分类 + Type Scale 阶梯 + 避坑清单 + 跨平台回退） |
| [references/layout-templates.md](references/layout-templates.md) | 设计/重排布局时（8 套 PPTX 布局 + 尺寸表 + 反模式布局） |
| [references/html-template-catalog.md](references/html-template-catalog.md) | **HTML 幻灯片模板选型**（34 套模板编目 + 设计令牌 + 配色/字体/情绪 + 模板选择工作流） |
| [references/chart-aesthetics.md](references/chart-aesthetics.md) | 涉及图表时（数据墨水比 + 各图表类型规范 + So what? 法则） |
| [references/design-token-mapping.md](references/design-token-mapping.md) | 前端项目转 PPT 时（次要场景，token → PPT API 映射） |
| [references/element-ratio-scoring.md](references/element-ratio-scoring.md) | **元素占比量化评分**（3 分独立模块：页面填充率/容器填充率/视觉均衡度，含评分表、理论依据、豁免规则、达标硬性指标、实测案例） |
| [references/critique_prompt.md](references/critique_prompt.md) | 视觉模型批判时（4 维度视觉批判 Prompt 模板 + 收敛性保证） |
| [references/icon-style-guide.md](references/icon-style-guide.md) | 使用图标时（4 种风格规范 + 尺寸/颜色/对齐/格式 + 反模式） |
| [references/animation-aesthetics.md](references/animation-aesthetics.md) | 使用动画/转场时（克制原则 + 允许/禁止动画清单 + 节奏规范） |
| [references/multilingual-typography.md](references/multilingual-typography.md) | 中英/中日韩/中阿混排时（字体分设 + 间距规则 + 标点规范 + RTL） |
| [references/accessibility-guide.md](references/accessibility-guide.md) | 无障碍设计时（对比度 + 色盲安全 + Alt 文本 + 阅读顺序） |
| [references/image-guidelines.md](references/image-guidelines.md) | 选择/处理图片时（分辨率 + 裁剪 + 遮罩 + AI 生成规范） |

## 资产索引

| 资产 | 用途 |
|---|---|
| [assets/PPT模板.pptx](assets/PPT模板.pptx) | 电信风格 PPT 模板（仅用于获取幻灯片尺寸，不使用其母版版式）|
| [assets/logo.png](assets/logo.png) | 电信品牌 Logo（从参考PPT提取），每页右上角放置 2.1×0.6 英寸 |
| [assets/html-templates/](assets/html-templates/) | **34 套 HTML 幻灯片模板库**（beautiful-html-templates，MIT 协议）|
| [assets/html-templates/index.json](assets/html-templates/index.json) | 模板元数据（slug、mood、occasion、formality、density、scheme）|
| [assets/html-templates/AGENTS.md](assets/html-templates/AGENTS.md) | 模板选择工作流（询问→筛选→推荐→构建）|

## 脚本索引

| 脚本 | 用途 |
|---|---|
| [scripts/render_slides.py](scripts/render_slides.py) | PPTX → PNG（LibreOffice / PowerPoint COM 双后端） |
| [scripts/score_ppt_pages.py](scripts/score_ppt_pages.py) | 结构化评分（59 种反模式自动检测 + 视觉评分 Prompt 嵌入 + **Token 输出** + **场景权重**） |
| [scripts/compare_ppt_versions.py](scripts/compare_ppt_versions.py) | **多版本对比**（2+ PPTX 横向排名 + Token 差异表 + 反模式对比 + 合并建议） |
| [scripts/fix_ppt.py](scripts/fix_ppt.py) | PPT 自动修复（字体/配色/页边距/图片/段落/背景 + 字号阶梯 + 间距网格） |
| [scripts/critique_engine.py](scripts/critique_engine.py) | **结构化批判引擎**（7→9 维度反模式映射 + hard/soft issue 分类 + 迭代修复控制） |
| [scripts/svg_to_pptx.py](scripts/svg_to_pptx.py) | **SVG→PPTX 导出**（源自 ppt-master，逐页 SVG 转原生可编辑 PPTX，含 `svg_to_pptx/` 子包） |
| [scripts/finalize_svg.py](scripts/finalize_svg.py) | **SVG 后处理**（icon 内联化、图片裁切嵌入、文本压平、圆角矩形转路径，含 `svg_finalize/` 子包） |
| [scripts/template_fill_pptx.py](scripts/template_fill_pptx.py) | **PPTX 模板填充**（纯 OOXML 填充路径：分析→脚手架→校验→应用，含 `template_fill_pptx/` 子包） |
| [scripts/gen_illustrations.py](scripts/gen_illustrations.py) | **ImageGen 后处理**（白边裁剪 + 按页号重命名，Agent 调用 ImageGen 后执行） |
| [scripts/suggest_illustrations.py](scripts/suggest_illustrations.py) | **内容感知配图建议**（分析 PPTX 文本→自动推荐配图类型/生成方式/嵌入位置，含标题加权打分+消歧规则） |
| [scripts/gen_pil_illustrations.py](scripts/gen_pil_illustrations.py) | **PIL 配图模板**（内置时间线/对比图/结构图/流程图/金字塔/大字报 6 种模板，JSON 配置驱动，无需手写 PIL 代码） |
| [scripts/embed_illustrations.py](scripts/embed_illustrations.py) | **配图嵌入**（JSON 配置驱动 `add_picture()`，支持精确坐标和位置预设，含 `--clean-placeholders`） |
| [scripts/gate_image_coverage.py](scripts/gate_image_coverage.py) | **配图覆盖率门禁**（检测 PPTX 中图片/SVG等效配图覆盖率是否 ≥ 阈值，默认 30%，含 LOW/FAIR/GOOD 分级） |

## 快速命令参考

```bash
# 评分（含场景权重）—— 所有临时输出必须写入 .temp/
python scripts/score_ppt_pages.py input.pptx --scenario marketing --output .temp/score_report.json
python scripts/render_slides.py input.pptx --output-dir .temp/render/ --dpi 150 --method libreoffice

# 多版本对比
python scripts/compare_ppt_versions.py \
    --input v1.pptx v2.pptx v3.pptx \
    --labels "原版" "调色版" "重排版" \
    --scenario marketing \
    --output .temp/compare_report.json \
    --md .temp/compare_report.md

# 修复（基础一键全修）
# ?? --all 不包含 --type-scale 和 --spacing-grid（会显著重排布局），需显式指定
python scripts/fix_ppt.py input.pptx --output fixed.pptx --all \
    --pairing source-han-sans+inter --palette corp-blue --margin-in 0.5

# 修复（含 web-design-engineer 法则：字号阶梯 + 间距网格）
python scripts/fix_ppt.py input.pptx --output fixed.pptx \
    --all --type-scale --ratio 1.25 --spacing-grid \
    --pairing source-han-sans+inter --palette corp-blue

# 修复（电信风格强制配色）
python scripts/fix_ppt.py input.pptx --output fixed.pptx \
    --all --palette telecom-red --pairing microsoft-yahei+arial

# 单项修复
python scripts/fix_ppt.py input.pptx --output fixed.pptx --fonts --pairing microsoft-yahei+arial
python scripts/fix_ppt.py input.pptx --output fixed.pptx --colors --palette forest-exec
python scripts/fix_ppt.py input.pptx --output fixed.pptx --margins --margin-in 0.5
python scripts/fix_ppt.py input.pptx --output fixed.pptx --images
python scripts/fix_ppt.py input.pptx --output fixed.pptx --bullets
python scripts/fix_ppt.py input.pptx --output fixed.pptx --theme-bg --bg-hex 0F1419
python scripts/fix_ppt.py input.pptx --output fixed.pptx --type-scale --ratio 1.618   # 黄金比例
python scripts/fix_ppt.py input.pptx --output fixed.pptx --spacing-grid --grid-in 0.08

# 结构化批判
python scripts/critique_engine.py input.pptx --output critique_report.json

# 验证—— 临时输出写入 .temp/
python scripts/render_slides.py fixed.pptx --output-dir .temp/after/
python scripts/score_ppt_pages.py fixed.pptx --scenario marketing --output .temp/score_report_after.json

# Dry-run（只看不改）
python scripts/fix_ppt.py input.pptx --all --dry-run

# ── 配图工具链 ──
# Step 1: ImageGen 后处理（白边裁剪 + 重命名）
python scripts/gen_illustrations.py .temp/illustrations/ --config .temp/illu_config.json --output-dir .temp/illustrations/cropped/

# Step 2: 配图嵌入（JSON 配置驱动）
python scripts/embed_illustrations.py input.pptx -o illustrated.pptx --config .temp/embed_config.json --images .temp/illustrations/cropped/

# Step 3: 配图覆盖率门禁
python scripts/gate_image_coverage.py illustrated.pptx --threshold 0.3 --verbose
python scripts/gate_image_coverage.py illustrated.pptx --json  # JSON 输出（管道集成）
```

## 限制与已知问题

1. **PowerPoint COM 在沙箱内不可用** — 沙箱内强制用 LibreOffice，部分 SmartArt / 复杂渐变 / 嵌入字体可能渲染偏差
2. **python-pptx 修改图表有限** — 图表系列颜色受 theme 控制，`fix_ppt.py --colors` 对图表内部的修改可能不完整
3. **3 等卡片无法机械修复** — 布局意图判断超出脚本能力，需人工或 AI 重排
4. **主题字体解析依赖 theme XML** — 默认 python-pptx 创建的 deck 可能无显式 major/minor font，导致 `cjk_text_no_cjk_font` 误报（实际用了 Calibri 默认主题）
5. **图表 So what? / 数据来源无法机械添加** — 需人工或 AI 生成结论句
6. **--type-scale 用浮点比例** — Major Third 1.25 等比例在 Pt 取整后可能出现 1.2488 这样的浮点比值；评分脚本用 1.2 作下限容忍此误差
7. **--spacing-grid 会重排布局** — 可能改变视觉关系，建议先 `--dry-run` 预览再应用
8. **Token 提取限制** — `radius.card_in` / `elevation.card_shadow_pt` 当前留空（需读 shape XML adj 值，后续完善）；`color.primary` 在多色 deck 上可能误判（要求频次 ≥ 2 可缓解）
9. **多版本对比只做结构评分** — `compare_ppt_versions.py` 不调用视觉模型，如需视觉评分需上游 agent 分别跑 `render_slides.py` + 视觉模型再人工合并
10. **critique_engine.py 维度映射已对齐** — 已从 7 维度升级为 9 维度（whitespace, type_scale, color_harmony, alignment, spacing, imagery, consistency, hierarchy, layout），反模式映射已扩展至 43 种（含 layout、deck 两个新检测类别）

如发现这些问题影响输出质量，在评分报告中明确标注，让用户决定是否人工介入。

---

## Workflow 7: Self-Critique Delivery (Mandatory)

> **强制工作流** — 每次执行工作流 1-6 生成 PPT 后，自动接工作流 7。用户显式说"跳过批判 / 不要自我批判 / 直接出稿"时跳过。

### 触发条件

- **强制触发**：工作流 1-6 的任何生成交付后自动执行
- **Escape hatch**：用户消息含"跳过批判"、"不要自我批判"、"直接出稿"、"skip critique" → 跳过本工作流
- 不可由用户误触发跳过：仅明确的跳过意图才生效

### Stage 1: Structural Detection (critique_engine.py)

1. 调用结构化检测引擎：
   ```powershell
   python scripts/critique_engine.py <output.pptx> --output critique_report.json
   ```

2. 解析返回的 JSON：
   - 读取 `hard_issues` 和 `soft_issues` 计数
   - 读取每页的 `issues` 列表
   - 读取 `dimension_scores` 各维度评分

3. **迭代控制**：
   - 如果 `hard_issues == 0` → 直接进入 Stage 2
   - 如果 `hard_issues > 0` → 对每个 hard issue 调用 `fix_ppt.py` 修复 → 重新检测
   - **最多 2 轮**迭代
   - **收敛提前终止**：`hard_issues < 3` 时停止迭代，进入 Stage 2
   - 第 2 轮后仍有 hard issues → 记录未解决问题，继续进入 Stage 2

4. 每轮迭代的输入/输出：
   - 输入：上一轮修复后的 PPTX 文件
   - 输出：新的 critique_report.json
   - 修复命令：`python scripts/fix_ppt.py <input.pptx> --issues critique_report.json --output <fixed.pptx>`

### Stage 2: Visual Model Critique (critique_prompt.md)

1. **渲染 PPTX 为图片**：
   ```powershell
   python scripts/render_slides.py <output.pptx> --format png --dpi 150
   ```

2. **对每页图片执行视觉批判**：
   - 读取 `references/critique_prompt.md` 中的 Prompt 模板
   - 将渲染图片 + Prompt 发送给 AI 视觉模型
   - 解析返回的 JSON（4 维度评分 + 问题列表）

3. **迭代控制**：
   - 如果所有维度 `passed == true` → 交付
   - 如果有维度 `passed == false` → 应用修复建议 → 重新渲染 → 重新批判
   - **最多 2 轮**迭代
   - 第 2 轮后仍有未通过维度 → 记录未解决问题，交付

### 输出

最终交付物：
1. **PPTX 文件**（经过两阶段批判+修复后的最终版本）
2. **critique_log.json**（与 PPTX 同目录），结构如下：

```json
{
  "file": "output.pptx",
  "created_at": "ISO-8601 timestamp",
  "rounds": [
    {
      "round": 1,
      "stage": "structural",
      "issues_found": 5,
      "issues_fixed": 4,
      "issues_remaining": 1,
      "converged": false
    },
    {
      "round": 2,
      "stage": "structural",
      "issues_found": 1,
      "issues_fixed": 1,
      "issues_remaining": 0,
      "converged": true
    },
    {
      "round": 1,
      "stage": "visual",
      "issues_found": 2,
      "issues_fixed": 2,
      "issues_remaining": 0,
      "converged": true
    }
  ],
  "final_status": "passed",
  "unresolved_issues": []
}
```

### 特殊情况处理

- **critique_engine.py 执行失败**：记录错误，跳过 Stage 1，直接进入 Stage 2
- **render_slides.py 执行失败**：记录错误，跳过 Stage 2，仅交付 Stage 1 结果
- **fix_ppt.py 修复失败**：记录未修复问题，继续下一轮检测
- **视觉模型不可用**：跳过 Stage 2，仅交付 Stage 1 结果

