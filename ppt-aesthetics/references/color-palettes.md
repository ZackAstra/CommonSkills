---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '3c24c081-ab45-49eb-9901-14c7d3445aa7'
  PropagateID: '3c24c081-ab45-49eb-9901-14c7d3445aa7'
  ReservedCode1: '8b774383-dbbb-42aa-b2ae-b6ebd87f4091'
  ReservedCode2: '8b774383-dbbb-42aa-b2ae-b6ebd87f4091'
---

# PPT 配色方案库

本文件提供 7 套经过验证的专业配色方案，每套含主色 / 辅助色 / 强调色 / 中性色族，可直接用于 `scripts/fix_ppt.py --palette <id>` 或手工套用。

## 配色原则

### 60-30-10 法则
- **60% 中性背景**（白/浅灰/深炭灰）
- **30% 主色 + 辅助色**（标题、关键元素、图表主系列）
- **10% 强调色**（每页仅用于 1-2 个最需要先看到的元素）

### 对比度（WCAG 2.2 AA）
- 正文与背景最小对比比 **4.5:1**
- 大标题（24pt+）最小对比比 **3:1**
- 工具：<https://palettechecker.com/> / <https://webaccessibility.co/accessible-color-palette-generator/>

### 颜色角色
| 角色 | 用途 | 选择标准 |
|---|---|---|
| 主色 primary | 标题、主导视觉、图表主系列 | 品牌色板中最深/最饱和 |
| 辅助色 secondary | 子标题、图表次系列、卡片描边 | 与主色同色系或互补，不竞争 |
| 强调色 accent | 高亮数据点、CTA、关键数字 | 与主色形成对比（暖色 vs 冷色）|
| 背景 bg | 幻灯片底色 | 接近白 (#FFFFFF / #F5F5F5) 或接近黑 (#0F1419) |
| 表面色 surface | 卡片、内容区填充 | 比 bg 略深/略浅一档 |
| 正文 text | 主要文字 | 接近黑 (#1A1A1A) 或接近白 (#F1F5F9) |
| 次要文字 text_muted | 副标题、注释、来源 | 灰阶中段 |
| 分隔线 border | 描边、表格线 | 浅灰，与背景区分但不抢眼 |

---

## 方案 1：corp-blue 企业蓝（咨询 / 金融 / 战略）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#1B3A5C` | 海军蓝 — 大标题、章节背景 |
| secondary | `#4A90D9` | 中蓝 — 子标题、图表次系列 |
| accent | `#E8792B` | 暖橙 — 关键数字、CTA |
| bg | `#FFFFFF` | 白底 |
| surface | `#F4F6F9` | 浅蓝灰卡片底 |
| text | `#1A1A1A` | 近黑正文 |
| text_muted | `#5A6675` | 蓝灰副文字 |
| border | `#D6DCE5` | 浅蓝灰描边 |

**适用场景**：麦肯锡/BCG 风格交付物、董事会演示、QBR、金融建模汇报。
**禁忌**：不要再加紫色或绿色——会破坏专业克制感。

---

## 方案 2：forest-exec 森林绿（ESG / 医疗 / 可持续）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#2D4A3E` | 深森林绿 |
| secondary | `#6B9E8A` | 鼠尾草绿 |
| accent | `#D4A843` | 金色 |
| bg | `#FFFFFF` | 白底 |
| surface | `#F2F5F2` | 浅绿灰 |
| text | `#1A2620` | 深绿黑 |
| text_muted | `#5C6B62` | 灰绿 |
| border | `#D5DCD7` | 浅绿描边 |

**适用场景**：ESG 报告、医疗/生物医药、农业、可持续发展、CSR 汇报。
**禁忌**：不要与亮红搭配（红绿撞色 + 色盲不友好）。

---

## 方案 3：charcoal-modern 炭灰现代（科技 / SaaS / 产品）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#333333` | 炭灰 |
| secondary | `#737373` | 中灰 |
| accent | `#0078D4` | 亮蓝（Microsoft 风）|
| bg | `#FFFFFF` | 白底 |
| surface | `#F5F5F5` | 浅灰 |
| text | `#1A1A1A` | 近黑 |
| text_muted | `#5A5A5A` | 中深灰 |
| border | `#D9D9D9` | 浅灰描边 |

**适用场景**：科技公司产品发布、SaaS 仪表盘截图、API 文档、Demo 录屏配图。
**禁忌**：accent 蓝只用在 CTA 和关键数据上，不要用于正文链接色（视觉噪音）。

---

## 方案 4：slate-pro 石板专业（法律 / 咨询 / 风险）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#3C3C50` | 深石板 |
| secondary | `#7A7A8E` | 浅石板 |
| accent | `#C84B31` | 锈红 |
| bg | `#FFFFFF` | 白底 |
| surface | `#F3F3F6` | 浅石板灰 |
| text | `#1F1F2E` | 深石板黑 |
| text_muted | `#5C5C70` | 中石板 |
| border | `#D6D6DD` | 浅石板描边 |

**适用场景**：法律意见书、合规培训、风险矩阵、内控汇报。
**禁忌**：accent 锈红有警示意味，慎用于非风险内容。

---

## 方案 5：mono-clean 单色极简（数据密集 / 投资 / 季度复盘）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#1A1A1A` | 近黑 |
| secondary | `#B0B0B0` | 浅灰 |
| accent | `#2196F3` | 蓝（数据强调）|
| bg | `#FFFFFF` | 白底 |
| surface | `#F7F7F7` | 极浅灰 |
| text | `#1A1A1A` | 近黑 |
| text_muted | `#707070` | 中灰 |
| border | `#DDDDDD` | 浅灰描边 |

**适用场景**：投资路演数据页、季报、仪表盘密集表格、KPI 看板。
**禁忌**：表格内不要再用 3-4 种颜色——靠 accent 蓝高亮一行/一列即可。

---

## 方案 6：deep-stage 深色舞台（高管主题演讲 / 大会场）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#FFFFFF` | 白（深底上的"主色"）|
| secondary | `#B8B8C8` | 浅冷灰 |
| accent | `#FF6B35` | 暖橙红 |
| bg | `#0F1419` | 近黑深底 |
| surface | `#1A2230` | 深蓝灰卡片 |
| text | `#F1F5F9` | 近白正文 |
| text_muted | `#94A3B8` | 浅蓝灰副文字 |
| border | `#2A3445` | 深描边 |

**适用场景**：Apple/Google 风格主题演讲、产品发布会、TED 演讲、年会主旨发言。
**禁忌**：仅限大屏投影 + 暗房环境；不适用于打印或亮光会议室（白纸黑字反而清晰）。

---

## 方案 7：telecom-red 电信红（中国电信品牌 / 政企 / 运营商）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#E60012` | 电信红 — 大标题、章节背景、品牌标识 |
| secondary | `#1B3A5C` | 海军蓝 — 子标题、图表次系列 |
| accent | `#FFB800` | 金色 — 关键数字、CTA、高亮 |
| bg | `#FFFFFF` | 白底 |
| surface | `#FFF5F5` | 极浅红卡片底 |
| text | `#1A1A1A` | 近黑正文 |
| text_muted | `#5A5A5A` | 中灰副文字 |
| border | `#F0D0D0` | 浅红描边 |

**适用场景**：中国电信品牌交付物、政企汇报、运营商年度报告、5G/云网产品发布、内部培训。
**禁忌**：
- 电信红 `#E60012` 仅用于标题、品牌标识和关键强调，**禁止大面积填充**（>30% 面积即违反 60-30-10 法则）
- 不要与深紫或亮绿搭配（破坏品牌专业感）
- 深色背景页可用 `#FF1A2E`（电信红提亮 10%）替代 `#E60012`，确保深底可读性

**电信红 50-950 色阶**：

| 色阶 | Hex（近似）| PPT 用途 |
|---|---|---|
| 50 | #FFF5F5 | 极浅红卡片底 |
| 100 | #FFE0E0 | 浅红卡片底 |
| 200 | #FFB3B3 | 边框/分隔线 |
| 300 | #FF8080 | 次要边框 |
| 400 | #FF4D4D | 次级图标 |
| 500 | #FF1A2E | 辅助红（深底用）|
| 600 | #E60012 | **电信红主色** |
| 700 | #B8000E | 深红（hover）|
| 800 | #8A000A | 深背景 |
| 900 | #5C0007 | 标题文字 |
| 950 | #330004 | 正文文字（替代 #000）|

---

## 数据可视化配色（图表专用）

图表配色与幻灯片配色解耦——图表需要更多可区分的系列色，但仍受主色族约束。

### 单系列图表
- 只用 primary；空数据用 secondary 灰阶。

### 2-5 系列图表
```
primary → secondary → accent → primary 的浅色 tint → secondary 的浅色 tint
```
例如 corp-blue 方案：`#1B3A5C → #4A90D9 → #E8792B → #A8C5E0 → #B0D0EB`

### 6+ 系列图表
**不要用 6 种颜色**——改用：
- 分面（small multiples）：每系列一个小图
- 强调法：所有系列用 secondary 灰，仅 1 个关键系列用 primary
- 分类轴：把系列拆到不同幻灯片

### 禁忌配色
- ❌ 纯 RGB（`#FF0000` / `#00FF00` / `#0000FF`）— 饱和度过高，刺眼
- ❌ 红绿配对区分数据 — 8% 男性红绿色盲无法区分
- ❌ AI 紫蓝渐变（`#6366F1` / `#818CF8` / `#A855F7`）— 一眼 AI 味
- ❌ 彩虹色板（7 色 ROYGBIV）— 顺序型数据用彩虹是数据可视化大忌
- ❌ 同时用 3 种饱和度相近的暖色 — 视觉打架

### 推荐：色盲安全的离散色板
来自 Okabe-Ito（学界公认的色盲友好色板）：

| 顺序 | Hex | 颜色 |
|---|---|---|
| 1 | `#0072B2` | 蓝 |
| 2 | `#D55E00` | 朱红 |
| 3 | `#009E73` | 蓝绿 |
| 4 | `#CC79A7` | 粉紫 |
| 5 | `#F0E442` | 黄 |
| 6 | `#56B4E9` | 天蓝 |
| 7 | `#E69F00` | 橙 |

适合需要 5-7 个可区分系列且色盲友好的图表。

---

## 从品牌色快速生成方案

无品牌指南时，从 Logo 提取 3 色：

1. **主色**：Logo 中最深/最饱和的色 → 取 Logo 同色或加深 20%
2. **辅助色**：Logo 中次主色 → 或主色降饱和 30%
3. **强调色**：与主色对比的暖色（主色冷 → 强调暖；主色暖 → 强调冷）

然后用以下网站生成完整中性色族：
- <https://www.sixtythirtyten.co/>
- <https://palettechecker.com/>
- <https://coolors.co/>

---

## 50-950 色阶系统（web-design-engineer 核心法则）

从单一品牌色生成 11 阶色板（对应 Tailwind CSS 标准色阶）。这是 web-design-engineer 防止"配色混乱"的核心工具。

### 色阶用途映射

| 色阶 | 用途 | PPT 对应 |
|---|---|---|
| 50-100 | 最浅 | 卡片底色、表单背景（避免纯白 #FFF 的生硬冷漠感）|
| 200-300 | 较浅 | 边框、分隔线、输入框背景、次要卡片背景 |
| 400-600 | 中间 | 普通实色按钮、图标、Logo（**主色在这里**）|
| 600-800 | 较深 | Hover/活跃态、暗色模式背景 |
| 800-950 | 最深 | 标题与正文文字（**替代纯黑 #000 提升质感**）|

### 关键原则
- **正文文字用 800-950 而非纯黑 #000**——纯黑显得生硬，深灰（如 #1A1A1A）更温暖精致
- **卡片底色用 50-100 而非纯白 #FFF**——纯白冷漠，带一点品牌倾向的浅色更高级
- **主色用 500-600**——既不太浅（看不清）也不太深（压抑）
- **强调色 hover/活跃态用 700**——比主色深一档提供交互反馈

### 生成工具
- **uicolors.app** <https://uicolors.app/create> — 输入 hex 自动生成 50-950 色阶，含 Tailwind 类名，可直接复制
- **Kigen Color Generator** — 输入 RGB 生成 11 阶，可调色阶数量
- **Tailwind CSS Colors** <https://tailwindcss.com/docs/customizing-colors> — 标准色阶参考

### 示例：corp-blue 主色 #1B3A5C 的 50-950 色阶

| 色阶 | Hex（近似）| PPT 用途 |
|---|---|---|
| 50 | #F0F4F8 | 极浅卡片底 |
| 100 | #DAE3EE | 浅卡片底 |
| 200 | #B5C6DC | 边框/分隔线 |
| 300 | #8FA9C9 | 次要边框 |
| 400 | #6988B6 | 次级图标 |
| 500 | #4A6CA3 | 辅助色 |
| 600 | #1B3A5C | **主色**（标题、主图表系列）|
| 700 | #152E48 | 深主色（hover）|
| 800 | #0F1F30 | 深背景 |
| 900 | #0A141F | 标题文字 |
| 950 | #050A10 | 正文文字（替代 #000）|

### 在评分/修复中的角色
- **评分**：检测 `pure_black_text`（#000000）和 `pure_white_card`（#FFFFFF 卡片）→ 建议改用 800-950 / 50-100
- **修复**：`fix_ppt.py --colors` 已自动把 #000 文字替换为 palette.text（通常 #1A1A1A，即 900-950 区间），把 #FFF 卡片替换为 palette.surface（通常 #F5F5F5，即 50-100 区间）

## 在 fix_ppt.py 中使用

```bash
# 套用 forest-exec 方案修复 PPT 配色
python scripts/fix_ppt.py input.pptx --output out.pptx --colors --palette forest-exec

# 套用 deep-stage 并加自定义背景
python scripts/fix_ppt.py input.pptx --output out.pptx --all --palette deep-stage --bg-hex 0F1419
```

## 在 SKILL.md 评分流程中的角色

1. **评分阶段**：检测 anti-pattern `ai_purple_palette` / `oversaturated_pure_rgb` / `too_many_colors`
2. **修复阶段**：选择最贴合 PPT 场景的方案（参考上表"适用场景"）
3. **验证阶段**：重新渲染 → 重新评分 → 确认 `too_many_colors` / `oversaturated_pure_rgb` 消失

---

## 从 HTML 幻灯片模板提取的配色方案

> 以下配色方案从 `assets/html-templates/` 的 34 套模板中精选，适合 HTML→PNG→PPTX 流程或作为视觉评分参考。详见 [html-template-catalog.md](html-template-catalog.md)。

### 方案 8：editorial-navy 编辑蓝（学术/咨询/深沉型）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#1F2BE0` | 钴蓝 — 大标题、装饰线条 |
| accent | `#5560E5` | 浅钴蓝 — 子标题、图表次系列 |
| bg | `#F0EBDE` | 羊皮纸 — 幻灯片底色 |
| surface | `#E6E0CE` | 深羊皮纸 — 卡片底色 |
| text | `#0a0a0a` | 近黑正文 |
| text_muted | `#5560E5` | 浅钴蓝注释 |

**来源**：Cobalt Grid 模板 | **正式度**：高 | **密度**：中

### 方案 9：signal-navy 信号蓝（投资者/董事会/政策）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#1c2644` | 深海军蓝 — 全幅背景 |
| secondary | `#232f55` | 浅海军蓝 — 交替背景 |
| accent | `#c8a870` | 暗金 — 强调色（唯一亮色） |
| surface_light | `#f0ece3` | 暖纸白 — 内容区底色 |
| surface_light_alt | `#e6e0d4` | 深暖白 — 交替内容区 |
| text | `#f0ece3` | 暖白正文（深底上） |
| text_muted | `#4e5a6e` | 蓝灰副文字 |

**来源**：Signal 模板 | **正式度**：高 | **密度**：高 | **支持中英双语**

### 方案 10：emerald-edit 翡翠编辑（领导力/战略/杂志封面）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#0F1A5C` | 深海军蓝 — 正文、标题 |
| accent_bg | `#3CD896` | 翡翠绿 — 大幅背景色块 |
| accent_bg2 | `#2DC684` | 深翡翠 — 交替背景 |
| accent_bg3 | `#25B377` | 最深翡翠 — 第三层背景 |
| text_on_green | `#F1E9D6` | 暖纸白 — 绿底上的文字 |

**来源**：Emerald Editorial 模板 | **正式度**：中高 | **密度**：中

### 方案 11：studio-electric 工作室电光（设计/创意/品牌展示）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#1c1c1c` | 近黑 — 全幅背景 |
| secondary | `#242422` | 深灰 — 交替背景 |
| accent | `#f5d200` | 电黄 — 标题、强调（唯一亮色）|
| accent_alt | `#f0cc00` | 深电黄 — 次级强调 |
| text | `#f5d200` | 电黄正文（黑底上）|

**来源**：Studio 模板 | **正式度**：中 | **密度**：中 | **支持中英双语**

### 方案 12：biennale-yellow 双年展黄（文化/艺术/策展）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#1B2566` | 靛蓝 — 正文、标题 |
| accent | `#F1EE2E` | 日光黄 — 装饰、强调 |
| accent_warm | `#F0DA7C` | 暖黄 — 次级装饰 |
| bg | `#E9E5DB` | 暖纸 — 幻灯片底色 |
| surface | `#DCD6C4` | 深暖纸 — 卡片底色 |
| text_muted | `#0a0a0a` | 近黑副文字 |

**来源**：Biennale Yellow 模板 | **正式度**：高 | **密度**：中

### 方案 13：neo-grid 新网格（新粗野/产品/品牌）

| 角色 | Hex | 用途 |
|---|---|---|
| primary | `#0A0A0A` | 近黑 — 正文/标题 |
| accent | `#E6FF3D` | 荧光黄绿 — 唯一强调色 |
| bg | `#ECECE8` | 冷灰白 — 幻灯片底色 |
| surface | `#F5F4EF` | 暖白 — 内容区底色 |

**来源**：Neo-Grid Bold 模板 | **正式度**：中 | **密度**：高