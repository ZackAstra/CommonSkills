---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '89a29cd4-ef57-4f7d-8074-90e28295e725'
  PropagateID: '89a29cd4-ef57-4f7d-8074-90e28295e725'
  ReservedCode1: 'fcbbda61-4ecd-4da0-a54b-0175d0b522c6'
  ReservedCode2: 'fcbbda61-4ecd-4da0-a54b-0175d0b522c6'
---

# Web 设计法则的 PPT 适配（web-design-engineer 审美迁移）

本文件把 web-design-engineer / 前端工程师的 4 大审美法则（字号阶梯、60-30-10 配色、间距节奏、icon 与配图）翻译成 PPT 可执行的规则。Web 与 PPT 的关键差异在每节开头标注。

> 灵感来源：少数派《AI 编程颜值急救课：4 个设计法则》（sspai.com/post/105156），Material Design，Tailwind CSS 标准色阶系统。

---

## 法则 1：字号阶梯 Type Scale

### Web 原则
选定一个**基础字号**（Base Size，Web 通常 16px），按一个**固定比例**（Ratio）向上递增，生成一套有数学美感的字号系统。

| 比例 | 名称 | 视觉效果 | 适用场景 |
|---|---|---|---|
| 1.25 | Major Third | 层级温和，对比不夸张 | SaaS、工具、博客（绝大多数）|
| 1.333 | Perfect Fourth | 对比明显 | 文章页、需要强调标题 |
| 1.5 / 1.618 | 黄金比例 | 极具张力 | Marketing 营销页、Landing Page |

### PPT 适配
PPT 没有 CSS `rem`，但同样适用阶梯比例。PPT 的"基础字号"是**正文**（不是 16px，而是 18-24pt），向上按比例生成标题/副标题/封面字号。

**推荐 PPT 字号阶梯**（以正文 20pt 为基础）：

| 元素 | Major Third (1.25) | Perfect Fourth (1.333) | 黄金比例 (1.618) |
|---|---|---|---|
| 正文 body | 20pt | 20pt | 20pt |
| 副标题 subtitle | 25pt | 27pt | 32pt |
| 页面标题 H2 | 31pt | 36pt | 52pt |
| 章节标题 H1 | 39pt | 47pt | 84pt（过大，慎用）|
| 封面主标题 | 49pt | 63pt | — |

**推荐选择**：
- **商务/咨询/数据汇报** → Major Third (1.25)，专业克制
- **学术/政府/正式** → Perfect Fourth (1.333)，标题突出
- **产品发布/营销/路演** → 黄金比例 (1.618)，视觉冲击（仅用于封面和章节页，内容页降回 1.25）

### 检测规则（评分脚本）
- 计算 `max_font_size / min_font_size`（同页最大与最小正文字号）
- 若比值 < 1.25 → `weak_type_scale`：字号层级过弱，无视觉重点
- 若 1.25 ≤ 比值 ≤ 2.5 → 健康
- 若比值 > 3 → `extreme_type_scale`：字号落差过大，可能封面字号误用到内容页

### 修复（fix_ppt.py --type-scale）
- 读 deck 内出现频率最高的字号作为"基础字号"（base）
- 按 `--ratio 1.25 | 1.333 | 1.618`（默认 1.25）重排所有字号：
  - `< base × 1.1` → 保持为 body
  - `base × 1.1 ~ 1.4` → subtitle = base × ratio
  - `base × 1.4 ~ 2.0` → H2 = base × ratio²
  - `> base × 2.0` → H1 = base × ratio³

---

## 法则 2：60-30-10 配色法则

### Web 原则
- **60% 背景色**：中性色（白/浅灰/深灰），保证耐看和留白感
- **30% 辅助色**：卡片背景、次级按钮、文本选中态——强调色的邻近色或深浅变体，**不应高饱和**
- **10% 强调色**：CTA 按钮、链接、高亮图标——品牌主色或对比色

### PPT 适配
PPT 没有滚动页面，"60-30-10"按**单页元素面积**估算：

| 角色 | 面积占比 | PPT 对应 |
|---|---|---|
| 60% 背景 | 整张幻灯片底色 | `slide.background.fill` |
| 30% 辅助 | 卡片/表格/图表次系列/分隔线 | shape fill（surface 色）+ secondary 色 |
| 10% 强调 | 关键数字/CTA/高亮数据点 | accent 色（每页仅 1-2 处）|

**关键差异**：PPT 的"60% 背景"几乎一定是幻灯片底色（不可能像 Web 那样有大量留白区域显示 body 背景）。所以 PPT 的 60-30-10 更准确地说是**非背景元素的 30-10 分配**：30% 的元素用辅助色（卡片、次级文字），10% 用强调色。

### 色阶生成（Kigen / Tailwind 50-950 系统）
从单一品牌色生成 11 阶色板：

| 色阶 | 用途 | PPT 对应 |
|---|---|---|
| 50-100 | 最浅 | 卡片底色、表单背景（避免纯白生硬）|
| 200-300 | 较浅 | 边框、分隔线、输入框背景 |
| 400-600 | 中间 | 普通实色按钮、图标、Logo（**主色在这里**）|
| 600-800 | 较深 | Hover 状态、暗色模式背景 |
| 800-950 | 最深 | 标题与正文文字（替代纯黑提升质感）|

**PPT 应用**：
- 正文文字用 800-950 而非纯黑 #000
- 卡片底色用 50-100 而非纯白 #FFF
- 主色用 500-600
- 强调色 hover/活跃态用 700

工具：<https://uicolors.app/create>（输入 hex 自动生成 50-950 色阶，含 Tailwind 类名）

### 检测规则（评分脚本）
- 统计非中性色数量（`_color_family != "neutral"`）
- 若 > 3 → 违反 60-30-10（已有 `too_many_colors` 反模式）
- 检测是否使用纯黑 #000 / 纯白 #FFF 作为文字/卡片色 → 建议改用 800-950 / 50-100
- 检测强调色出现频率：若 accent 色出现在 > 5 个元素 → `overuse_accent`：强调色被滥用，失去强调作用

### 修复（fix_ppt.py --colors）
- 已有逻辑：把 oversaturated 纯 RGB 替换为 palette 色
- 新增：把 #000 文字色替换为 palette.text（通常 #1A1A1A），把 #FFF 卡片色替换为 palette.surface（通常 #F5F5F5）

---

## 法则 3：排版布局与间距节奏

### Web 原则

#### 3.1 栅格系统
- 定义统一内容宽度和左右边距，正文区有稳定视觉重心，不贴边
- 关键信息（标题、正文、卡片、页脚）落在同一套对齐线
- 栅格灵活：Hero 大图等装饰元素可适度溢出

#### 3.2 行长
- 英文正文：45-75 字符/行（约 10 词）
- 中文正文：35-45 汉字/行（中文是高密度方块字）
- 行长、字号、行高三者动态平衡：行高 1.8+ 时可容忍略宽行长
- 警惕 AI 在专有名词中间断句、行末孤儿词

#### 3.3 间距节奏（格式塔亲密度法则）
- 彼此靠近的元素被认知为同一组
- 不是所有内容等距排列——相关内容紧密分组，不相关内容拉开距离
- **4px / 8px 倍数系统**：4, 8, 12, 16, 24, 32, 48, 64, 80, 128...

| 间距 | Web 用途 | Tailwind 类 |
|---|---|---|
| 4px / 8px | 组件内部紧密间距 | gap-1, gap-2 |
| 16px | 卡片内边距、列表项 | p-4, gap-4 |
| 24px / 32px | 区块/组件分隔 | mb-6, mb-8 |
| 64-128px | 大区域呼吸感 | py-20, py-32 |

### PPT 适配

#### 3.1 PPT 栅格
PPT 是固定 13.33×7.5in 画布，栅格更刚性：
- **12 列网格**：每列 ≈ 0.89in，槽 0.17in
- **安全边距**：左右 0.67in、上下 0.5in
- **内容区**：12.0 × 6.5in
- 已在 [layout-templates.md](layout-templates.md) 详述

#### 3.2 PPT"行长"
PPT 不滚动，"行长"对应**单条要点的字数**和**单页要点数**：

| 维度 | 推荐值 | 上限 |
|---|---|---|
| 单条要点字数（中文）| 15-25 字 | 35 字 |
| 单条要点字数（英文）| 8-12 词 | 15 词 |
| 单页要点数 | 3-4 条 | 6 条 |
| 单页总字数 | ≤ 60 字 | 80 字 |

**超出即触发**：
- 单条 > 35 字 → `long_bullet`：要点过长，应拆分
- 单页 > 6 条 → `too_many_bullets`：要点过多
- 单页 > 60 词或 > 400 字符 → `wall_of_text`（已有反模式）

#### 3.3 PPT 间距（4/8 倍数 = 0.04/0.08in 倍数）
Web 的 4px/8px 在 PPT 中对应（96 DPI 换算）：
- 4px ≈ 0.042in → 取 **0.04in**
- 8px ≈ 0.083in → 取 **0.08in**

**PPT 间距倍数表**（基于 0.08in）：

| 间距 (in) | 用途 | 对应 Web |
|---|---|---|
| 0.04 | 图标与文字紧贴 | 4px / gap-1 |
| 0.08 | 列表项内紧密分组 | 8px / gap-2 |
| 0.16 | 卡片内边距 | 16px / p-4 |
| 0.24 | 要点之间分隔 | 24px / mb-6 |
| 0.32 | 区块/卡片之间 | 32px / mb-8 |
| 0.64 | 大区域呼吸 | 64px / py-16 |
| 0.96 | 章节分隔 | 96px / py-24 |

### 检测规则（评分脚本）
- **间距非 4/8 倍数检测**：取同页所有 shape 间距（垂直相邻 shape 的 top 差、水平相邻的 left 差），若 > 50% 间距不在 0.04/0.08 倍数 ±0.02in 范围内 → `irregular_spacing`：间距无节奏
- **行长检测**：单条要点 > 35 字 → `long_bullet`
- **孤儿词检测**：要点最后一行只剩 1-2 字 → `orphan_word`（PPT 难以机械检测，主要靠视觉模型）

### 修复（fix_ppt.py --spacing-grid）
- 把所有 shape 的 left/top/width/height 吸附到最近的 0.08in 倍数
- 保留页边距 0.5in 不动（避免内容贴边）
- 谨慎使用：会改变布局，建议先 `--dry-run` 预览

---

## 法则 4：Icon 与配图

### Web 原则

#### 4.1 Icon
- **一致性**：同一套图标库，线条粗细、填充/描边风格统一
- **4px 网格**：图标外框 16/20/24/32px
- **视觉对齐**：图标比文字大 2-4px（14px 文字配 16px 图标）
- **适当间距**：图标与文字 gap-1 (4px) 或 gap-2 (8px)

#### 4.2 配图
- **高质量**：拒绝模糊、噪点、拉伸变形
- **色调匹配**：图片色温与品牌色呼应（科技冷色、生活暖色）
- **防变形**：`object-cover`（Fill 填充）
- **响应式**：srcset + sizes
- **性能**：单图 1500-2500px、<500KB；现代格式 WebP/AVIF

### PPT 适配

#### 4.1 PPT Icon
PPT 没有 CSS `gap`，但同样适用：

| 规则 | PPT 实现 |
|---|---|
| 同一图标库 | 全 deck 用 Phosphor / Hugeicons / Lucide 同一风格（全 outline 或全 filled）|
| 4px 网格 | 图标尺寸 0.17in (16px) / 0.21in / 0.25in (24px) / 0.33in (32px) |
| 视觉对齐 | 14pt 文字配 0.21in 图标；18pt 文字配 0.25in 图标 |
| 适当间距 | 图标与文字间距 0.04-0.08in |

**插入方式**：SVG 矢量插入（Office 2019+/WPS 原生支持）；老版本转 EMF。详见 [design-token-mapping.md](design-token-mapping.md) SVG Vector Asset Export 节。

#### 4.2 PPT 配图
| 规则 | PPT 实现 |
|---|---|
| 高质量 | 最低 1920×1080；投影场景 2560×1440+ |
| 防变形 | 锁定宽高比（右键 → 大小和位置 → 锁定纵横比）；`fix_ppt.py --images` 自动修复 |
| 色调匹配 | 全 deck 用同一图片风格（照片/插画/3D 渲染不混用）；照片统一加同款滤镜 |
| 全出血图 | 图片占满幻灯片 + 半透明遮罩 + 文字（见 [layout-templates.md](layout-templates.md) 布局 6）|

**图片拉伸检测**（已有 `stretched_image` 反模式）：
- 比较 shape 容器宽高比 vs 图片原始宽高比
- 偏差 > 8% → 拉伸/压缩

### 检测规则（评分脚本）
- 图片拉伸检测（已有）
- 新增：图片像素量检测——若图片原始尺寸 < 800×600 → `low_res_image`：图片分辨率过低，投影会模糊
- 新增：图片风格混用检测（需视觉模型）——照片+插画+3D 混用 → `mixed_image_style`

### 修复（fix_ppt.py --images）
- 已有：调整容器高度匹配图片宽高比（保持宽度不变）
- 新增：低分辨率图片标注警告（无法机械提升分辨率，只能标注让用户换图）

---

## 法则汇总：web-design-engineer 审美 → PPT 检测/修复映射

| Web 法则 | PPT 检测（score_ppt_pages.py）| PPT 修复（fix_ppt.py）|
|---|---|---|
| Type Scale 1.25/1.333/1.618 | `weak_type_scale` / `extreme_type_scale` | `--type-scale --ratio 1.25` |
| 60-30-10 配色 | `too_many_colors` / `overuse_accent` / `pure_black_text` / `pure_white_card` | `--colors --palette <id>` |
| 50-950 色阶 | `pure_black_text` / `pure_white_card` | `--colors`（替换 #000/#FFF）|
| 栅格对齐 | `no_margins` / `irregular_grid`（已有部分）| `--margins --margin-in 0.5` |
| 行长（中文 35-45 字）| `long_bullet` / `too_many_bullets` / `wall_of_text` | `--bullets`（拆分长段落）|
| 4/8 倍数间距 | `irregular_spacing` | `--spacing-grid` |
| Icon 4px 网格 | （视觉模型检测）| 人工统一图标库 |
| Icon 视觉对齐 | （视觉模型检测）| 人工调整 |
| 配图防变形 | `stretched_image`（已有）| `--images`（已有）|
| 配图高质量 | `low_res_image` | 标注警告 |
| 配图色调匹配 | `mixed_image_style`（视觉模型）| 人工统一风格 |

---

## 推荐字体（按风格定位分类，免费可商用）

补充 [font-pairings.md](font-pairings.md) 的字体清单，按 Web 设计工程师的风格定位分类：

| 风格定位 | 适用场景 | 推荐英文字体 | 推荐中文字体 |
|---|---|---|---|
| 现代通用 | 工具软件、后台、文档、覆盖大多数场景 | SF Pro / Open Sans / Montserrat / Poppins / Lato / Raleigh / Manrope / Work Sans / **Inter** / Geist | 苹方 / 思源黑体 / 阿里普惠体 / HarmonyOS Sans / MiSans / vivo Sans / OPPO Sans / 微软雅黑 / 冬青黑体 |
| 科技/极客 | 开发者工具、Web3、技术博客、终端风 | Orbitron / Audiowide / Tektur / Michroma / Nova Square / Wallpoet / **Space Grotesk** / **JetBrains Mono** / Fira Code | 思源黑体 / HarmonyOS Sans / MiSans |
| 优雅人文 | 知识库、阅读类、营销落地页 | **Playfair Display** / Merriweather / Lora / EB Garamond / Libre Baskerville / Noto Serif / PT Serif / Crimson Text / Source Serif 4 / Cormorant Garamond | 思源宋体 / 方正书宋 / 华文宋体 |
| 图形化 | 品牌 Logo 字体 | Rubik Glitch / Rubik Broken Fax / Rubik 80s Fade / Monoton / Headland One | （按品牌定制）|
| 复古像素 | 复古品牌、装饰、怀旧、Y2K | Pixelify Sans / Press Start 2P / VT323 / DotGothic16 / Jersey 10 / Tiny5 / Bytesized | （按品牌定制）|
| 温暖友好 | 儿童、教育、社区、生活方式、零售、女性向 | Comfortaa / Nunito / Lato / Karla / Jost / Bree Serif / Smooch Sans / Averia Serif Libre / **Lexend** / Caveat | 阿里普惠体 / OPPO Sans / 圆体系列 |
| 数字专用 | 需要突出的数据 | Open Sans / Montserrat / **Lexend** / Outfit / Alexandria / Readex_Pro / Reddit Sans / Sansation / Albert Sans / HarmonyOS Sans / **DIN Alternate** | （同英文）|

### 字体搭配 Tips（来自 web-design-engineer）
1. **一页最多 2-3 种字体**，其余层级靠字号/字重/字距完成
2. **数字专用字体**：默认字体的数字通常缺乏性格（如苹方的数字很平），特意挑选的数字字体能让关键数据跳脱出来
3. **字体声明顺序**（Web CSS / PPT XML 同理）：英文字体优先，中文字体在后
   - Web: `font-family: "Inter", "Noto Sans SC", sans-serif;`
   - PPT: `<a:latin typeface="Inter"/>` + `<a:ea typeface="Microsoft YaHei"/>`
   - 原因：英文字体不含汉字，中文字体含 a-z 英文和数字。把英文放第一，英文/数字用英文字体渲染；汉字回退到中文字体
4. **衬线 + 非衬线混用**：英文 Serif（Playfair Display 等）作装饰用于标题/品牌，Sans-serif 用于正文保证可读性。Luma AI、Perplexity 都用这种手法
5. **UI 友好字体**：选上下间距对称的字体，减少对齐还原问题（Inter / Geist / SF Pro 都是 UI 友好）

### PPT 字体子集化
Web 中文字体文件大，建议子集化到 200KB 内。PPT 不需要子集化（字体不嵌入文件则按系统字体渲染），但**跨平台分发时**需注意：
- 用思源黑体（全平台原生支持）→ 无需嵌入
- 用苹方 → Mac 原生，Windows 缺失 → 必须导出 PDF 或嵌入字体
- 用微软雅黑 → Windows 原生，Mac 缺失 → 同上

---

## 在评分/修复流程中的角色

### 评分阶段
1. 结构化脚本自动检测：`weak_type_scale` / `overuse_accent` / `pure_black_text` / `pure_white_card` / `long_bullet` / `too_many_bullets` / `irregular_spacing` / `low_res_image`
2. AI 视觉模型补充检测：`mixed_image_style` / `orphan_word` / Icon 风格不一致

### 修复阶段
1. `fix_ppt.py --type-scale --ratio 1.25` 重排字号阶梯
2. `fix_ppt.py --colors --palette <id>` 套用 60-30-10 配色 + 替换纯黑/纯白
3. `fix_ppt.py --spacing-grid` 间距吸附到 4/8 倍数
4. `fix_ppt.py --bullets` 拆分长要点
5. `fix_ppt.py --images` 修复拉伸图片

### 人工修复
- Icon 风格统一（换同一图标库）
- 图片风格统一（照片/插画/3D 不混用）
- 字体搭配按风格定位选择（参考上表）

---

## 参考
- 少数派《AI 编程颜值急救课：4 个设计法则》<https://sspai.com/post/105156>
- Typescale 工具 <https://typescale.com/>
- Kigen Color Generator / uicolors.app <https://uicolors.app/create>
- Tailwind CSS 标准色阶系统 <https://tailwindcss.com/docs/customizing-colors>
- Material Design Color System <https://m3.material.io/styles/color/system/overview>
- 格式塔亲密度法则（Gestalt Proximity）