---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'd45751de-a627-4074-9c2b-893eccb79656'
  PropagateID: 'd45751de-a627-4074-9c2b-893eccb79656'
  ReservedCode1: '36c085bc-0628-4c2a-8be6-396377c653a0'
  ReservedCode2: '36c085bc-0628-4c2a-8be6-396377c653a0'
---

# HTML 幻灯片模板库编目

> 来源：[beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates)（MIT 协议，3.4k stars）
> 本地路径：`assets/html-templates/templates/<slug>/`
> 元数据：`assets/html-templates/index.json`

## 概述

本库包含 34 套经过专业设计的 HTML 幻灯片模板，每套含 Google Fonts 字体栈、CSS 自定义属性设计令牌、响应式布局。模板通过 HTML→PNG→PPTX 流程转为 PowerPoint，或直接作为 Web 演示使用。

### 与 PPTX 布局模板的关系

| 维度 | `layout-templates.md`（PPTX 导向） | `html-template-catalog.md`（HTML 导向） |
|---|---|---|
| 输出格式 | .pptx（python-pptx 直接生成） | .html → .png → .pptx（截图组装） |
| 设计自由度 | 受 python-pptx API 限制 | CSS 完全自由，视觉效果更丰富 |
| 字体 | 系统字体（宋体/雅黑/Inter 等） | Google Fonts（需网络加载） |
| 动画/交互 | 无 | 可含 CSS 动画和 JS 交互 |
| 适用场景 | 数据密集型、快速生成 | 设计导向、高质量视觉呈现 |
| 评分用途 | 元素位置/间距结构评分参考 | 视觉审美评分参考标准 |

**结论**：两者共存互补，根据场景选择。

---

## 模板选择工作流

遵循仓库 AGENTS.md 定义的三步流程：

1. **询问用户场景**：场合（occasion）+ 情绪（mood）+ 正式度（formality）
2. **从 index.json 筛选**：按 mood/occasion/formality/density/scheme 匹配
3. **推荐 2-3 个候选**：展示 slug、tagline、配色预览，让用户选择

---

## 模板分类速查

### 按明暗分类

| 分类 | 模板 |
|---|---|
| **浅色（light）** | soft-editorial, biennale-yellow, block-frame, blue-professional, bold-poster, capsule, cartesian, cobalt-grid, creative-mode, daisy-days, neo-grid-bold, peoples-platform, pin-and-paper, playful, raw-grid, retro-windows, retro-zine, sakura-chroma, scatterbrain, stencil-tablet, long-table |
| **深色（dark）** | 8-bit-orbit, broadside, pink-script, studio |
| **混合（mixed）** | coral, editorial-forest, editorial-tri-tone, emerald-editorial, grove, mat, monochrome, signal, vellum |

### 按正式度分类

| 分类 | 模板 |
|---|---|
| **高（high）** | biennale-yellow, cartesian, cobalt-grid, monochrome, signal, soft-editorial, vellum |
| **中高（medium-high）** | blue-professional, editorial-tri-tone, emerald-editorial, grove, broadside, mat, stencil-tablet |
| **中（medium）** | editorial-forest, bold-poster, coral, creative-mode, capsule, long-table, pink-script, studio |
| **中低（medium-low）** | block-frame, peoples-platform, retro-zine, pin-and-paper |
| **低（low）** | 8-bit-orbit, daisy-days, playful, retro-windows, sakura-chroma, scatterbrain |

### 按内容密度分类

| 分类 | 模板 |
|---|---|
| **高（high）** | monochrome, signal, neo-grid-bold, raw-grid, scatterbrain, block-frame |
| **中（medium）** | 大多数模板 |
| **低（low）** | bold-poster, cartesian, pink-script, soft-editorial, vellum |

### 支持中英双语的模板

以下模板内置 Noto Sans SC / Noto Serif SC 字体栈，适合中英混排场景：

broadside, grove, mat, monochrome, signal, studio, vellum, sakura-chroma

---

## 模板详细编目### 8-Bit Orbit (`8-bit-orbit`)

> Pixel-art neon arcade aesthetic on a deep navy void.

| 属性 | 值 |
|---|---|
| 正式度 | 低 |
| 内容密度 | 中（均衡） |
| 明暗 | 深色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：gaming pitch, hackathon demo, web3 / crypto deck, indie product launch, developer tools, synthwave brand

**情绪关键词**：retro-tech, playful, cyberpunk, energetic

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--neon-pink` | `#F0A6CA` | 正文/墨色 |

**完整色板**（6 色）：`#0A0E27` `#0F1B3D` `#5EDCF4` `#E2D5F2` `#F0A6CA` `#F4D03F`

**字体栈**：
- `Chakra Petch`
- `Space Mono`
- `Tektur`

**字体令牌**：
- `--pixel-size`: `4px`
- `--font-display`: `'Tektur', cursive`
- `--font-body`: `'Chakra Petch', sans-serif`
- `--font-mono`: `'Space Mono', monospace`

**设计令牌总数**：10 个 CSS 自定义属性

**宽高比**：1

**最适合**：Anything that should feel like a CRT screen at 2am: cyberpunk, gaming, web3, indie dev tools, hackathon demos. Just as good for a tech talk that wants to lean into nostalgic-digital craft, a synthwave brand deck, or a creative review that wants to feel like a console.

**避免用于**：Contexts where the dark neon palette would actively work against the message — quiet institutional finance disclosures, healthcare patient-facing materials, traditional luxury.

---

### Biennale Yellow (`biennale-yellow`)

> Solar yellow on warm parchment with deep indigo serif and atmospheric sun-glow gradients.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 否 |

**适用场景**：exhibition or biennale, arts institution programme, design or typography conference, literary or curatorial publication, studio annual report, museum season announcement

**情绪关键词**：editorial, atmospheric, warm, cultural-institution, poster-like

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#E9E5DB` | 背景/纸张 |
| `--paper-deep` | `#DCD6C4` | 背景/纸张 |
| `--ink` | `#1B2566` | 正文/墨色 |

**完整色板**（8 色）：`#0a0a0a` `#1B2566` `#DCD6C4` `#E26B4A` `#E9E5DB` `#F0DA7C` `#F1EE2E` `#F8F39B`

**字体栈**：
- `Instrument Serif`
- `Archivo`
- `JetBrains Mono`

**设计令牌总数**：8 个 CSS 自定义属性

**最适合**：Anything that should feel like an art-biennale poster or a museum's annual programme: exhibition decks, arts-institution announcements, design conference brochures, curatorial pitches, literary publications, studio retrospectives. Equally good for any deck wanting Dutch-editorial atmosphere with an unmistakable single-color signature.

**避免用于**：Decks that need visual punch or saturated multi-color energy — the warm-paper canvas and one-yellow palette are intentionally quiet and atmospheric.

---

### BlockFrame (`block-frame`)

> Neobrutalist deck with pastel-neon color blocks and chunky black borders.

| 属性 | 值 |
|---|---|
| 正式度 | 中低 |
| 内容密度 | 高（信息密集） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：creative agency pitch, indie SaaS launch, designer portfolio, brand redesign, modern startup deck

**情绪关键词**：bold, playful, graphic, fresh

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--pink` | `#FE90E8` | 正文/墨色 |

**完整色板**（8 色）：`#000000` `#99E885` `#C0F7FE` `#F7CB46` `#FE90E8` `#FFDC8B` `#FFFDF5` `#FFFFFF`

**字体栈**：
- `Space Grotesk`
- `Inter`

**设计令牌总数**：13 个 CSS 自定义属性

**宽高比**：1

**最适合**：Anything that should feel pop-graphic and design-led: indie SaaS launches, agency credentials, creative reviews, brand redesigns. Also a strong unexpected pick for tech, finance, or research when the speaker wants to land as confident and contemporary rather than buttoned-up.

**避免用于**：Contexts that require quiet institutional restraint or traditional weight (regulated disclosures, formal legal briefs).

---

### Blue Professional (`blue-professional`)

> Cream paper background with electric cobalt blue accents; clean modern professional.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：B2B SaaS pitch, consulting deliverable, internal review, advisory pitch, investor update

**情绪关键词**：professional, modern, calm, trustworthy

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#fdfae7` | 背景/纸张 |
| `--accent-light` | `rgba(30, 43, 250, 0.08)` | 强调色 |
| `--accent-medium` | `rgba(30, 43, 250, 0.15)` | 强调色 |
| `--border` | `rgba(30, 43, 250, 0.2)` |  |
| `--card-bg` | `rgba(30, 43, 250, 0.04)` | 背景/纸张 |

**完整色板**（7 色）：`#059669` `#111111` `#1e2bfa` `#6b6b6b` `#9a9a9a` `#dc2626` `#fdfae7`

**字体栈**：
- `Space Grotesk`
- `Inter`

**设计令牌总数**：9 个 CSS 自定义属性

**最适合**：Anything that should feel modern-considered and lightly authoritative: B2B SaaS pitches, consulting deliverables, advisory updates, investor reports. Also a clean, tasteful choice whenever you want to read as professional without going stiff — research synthesis, internal reviews, brand work for service businesses.

**避免用于**：Contexts where the deck should feel hot, playful, or intentionally informal — the cool electric-blue restraint will read as overly polished.

---

### Bold Poster (`bold-poster`)

> Editorial poster aesthetic with massive Shrikhand display and a single fire-engine red accent.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 低（大字报/少量元素） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：brand manifesto, creative-led pitch, magazine / editorial, founder vision deck, art / culture

**情绪关键词**：bold, editorial, loud, confident

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#FFFFFF` | 背景/纸张 |

**完整色板**（4 色）：`#1C1410` `#D8000F` `#F5F2EF` `#FFFFFF`

**字体栈**：
- `Shrikhand`
- `Libre Baskerville`
- `Space Grotesk`

**设计令牌总数**：4 个 CSS 自定义属性

**最适合**：Anything that should land like a magazine cover: brand manifestos, founder vision decks, editorial / cultural pitches, creative reviews. Excellent any time you want a few words to feel like a poster — including unexpected fits like a tech keynote or a finance manifesto that wants to be quotable.

**避免用于**：Decks that need to communicate dense information per slide — the layout is built around a few large statements, not paragraphs of detail.

---

### Broadside (`broadside`)

> Dark editorial canvas with a single fire orange accent and bilingual Latin/Chinese type stack.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 中（均衡） |
| 明暗 | 深色 |
| 幻灯片数 | 20 |
| 含 deck-stage.js | 否 |

**适用场景**：brand manifesto, founder vision deck, magazine / cultural pitch, design talk, bilingual EN/CN deck, campaign launch

**情绪关键词**：editorial, dramatic, loud, newspaper

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#111111` | 背景/纸张 |
| `--c-bg-alt` | `#1a1a18` | 背景/纸张 |
| `--c-bg-light` | `#111111` | 背景/纸张 |
| `--c-bg-light-alt` | `#1a1a18` | 背景/纸张 |
| `--c-bg-orange` | `#e85d26` | 背景/纸张 |
| `--c-accent` | `#e85d26` | 强调色 |
| `--c-border` | `#282826` |  |
| `--c-border-light` | `#282826` |  |

**完整色板**（11 色）：`#111` `#111111` `#1a1a18` `#282826` `#2a1810` `#3a3a38` `#505048` `#555550` `#888880` `#e85d26` `#f0ece5`

**字体栈**：
- `Barlow`
- `IBM Plex Mono`
- `Noto Sans SC`

**设计令牌总数**：35 个 CSS 自定义属性

**最适合**：Anything that should land like a broadside newspaper headline: brand manifestos, magazine and cultural pitches, design talks, bilingual EN/CN decks, founder vision statements. Also a striking pick for tech, research, or business decks that want a dramatic single-accent editorial feel.

**避免用于**：Decks that need to feel quiet, warm, or institutionally traditional — the dark canvas with fire-orange accent commits to drama.

---

### Capsule (`capsule`)

> Modular pill-shaped cards on warm bone with a full pastel-pop palette.

| 属性 | 值 |
|---|---|
| 正式度 | 中低 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：lifestyle brand, creator portfolio, DTC product launch, wellness or beauty pitch, Y2K-tinged brand work

**情绪关键词**：playful, modern, warm, fresh, fun

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#F5F5F0` | 背景/纸张 |

**完整色板**（12 色）：`#1A1A1A` `#1E1E1E` `#8BB4F7` `#A06CE8` `#A8E6CF` `#C4D94E` `#C5B5E0` `#E85D4E` `#F2D160` `#F5B895` `#F5F5F0` `#fff`

**字体栈**：
- `Bodoni Moda`
- `Space Grotesk`

**字体令牌**：
- `--font-display`: `'Bodoni Moda', serif`
- `--font-body`: `'Space Grotesk', sans-serif`

**设计令牌总数**：14 个 CSS 自定义属性

**最适合**：Anything that should feel modular, modern, and a little Y2K: lifestyle brands, creator portfolios, DTC launches, beauty / wellness, agency credentials. Also fun for a playful tech demo or a research deck that wants pop-art clarity instead of gravitas.

**避免用于**：Contexts that require traditional institutional weight — the capsule shapes and pastel pops actively soften authority.

---

### Cartesian (`cartesian`)

> Quiet warm-neutral palette with classical Playfair serifs; tasteful and unhurried.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 低（大字报/少量元素） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：investment thesis, white paper, advisory deliverable, research report, book / longform pitch, gallery / cultural

**情绪关键词**：quiet, considered, elegant, warm-minimal

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg-primary` | `#ede8e0` | 背景/纸张 |
| `--bg-secondary` | `#e2dbd1` | 背景/纸张 |
| `--accent` | `#8a8178` | 强调色 |

**完整色板**（6 色）：`#1a1a1a` `#5a5a5a` `#8a8178` `#b8b0a4` `#e2dbd1` `#ede8e0`

**字体栈**：
- `Playfair Display`
- `Inter`

**设计令牌总数**：6 个 CSS 自定义属性

**宽高比**：4/3) 

**最适合**：Anything that should feel quiet, considered, and grown-up: investment theses, white papers, advisory work, longform research, gallery / cultural decks. Also a strong choice for editorial features, founder reflections, or any deck where restraint is the message — including across tech and finance.

**避免用于**：Decks that need visual heat, multiple accents, or a sense of urgency — the warm-neutral palette is intentionally low-energy.

---

### Cobalt Grid (`cobalt-grid`)

> Electric cobalt serifs on a graph-paper canvas, anchored by stair-stepped pixel-glitch decorations and slim hairline rules.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 否 |

**适用场景**：design trend or research report, studio annual or seasonal bulletin, creative agency capabilities deck, art or architecture publication, academic / curatorial publication, newsletter or zine pitch

**情绪关键词**：editorial, design-research, studious, modernist, tech-print, monochrome

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#F0EBDE` | 背景/纸张 |
| `--paper-2` | `#E6E0CE` | 背景/纸张 |
| `--ink` | `#1F2BE0` | 正文/墨色 |
| `--ink-soft` | `#5560E5` | 正文/墨色 |

**完整色板**（5 色）：`#0a0a0a` `#1F2BE0` `#5560E5` `#E6E0CE` `#F0EBDE`

**字体栈**：
- `Newsreader`
- `Hanken Grotesk`
- `DM Mono`

**设计令牌总数**：6 个 CSS 自定义属性

**最适合**：Anything that should feel like a quietly serious design / research bulletin, art publication, or curated trend report. Strong for studio annuals, agency capabilities decks, design-research publications, architecture / art / academic decks, and any deck wanting one strict accent colour and a printed-ledger calmness rather than corporate polish.

**避免用于**：Decks that need warmth, multi-colour energy, or a casual / playful voice — the strict cobalt + cream + grid palette is intentionally austere.

---

### Coral (`coral`)

> Cream and coral on near-black, set in oversized Bebas Neue.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中（均衡） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：fashion / beauty pitch, fitness brand, F&B brand deck, lifestyle launch, creative agency

**情绪关键词**：bold, warm, modern, confident

**完整色板**（7 色）：`#1A1A1A` `#6B6B6B` `#B0B0B0` `#D44A4A` `#E85D5D` `#E8E0D4` `#F5F0E8`

**字体栈**：
- `Bebas Neue`
- `Inter`

**设计令牌总数**：7 个 CSS 自定义属性

**最适合**：Anything that should feel warm-graphic and editorial: fashion, beauty, fitness, F&B, lifestyle brands, agency credentials. Just as strong for a creator portfolio, a manifesto, or a tech / research deck that wants warmth and a single bold accent instead of corporate cool.

**避免用于**：Contexts that should feel quiet or institutional — the coral accent and oversized Bebas Neue commit hard to a confident magazine voice.

---

### Creative Mode (`creative-mode`)

> Cream paper canvas with confident multi-color (green, pink, orange, yellow) accents and Archivo Black display.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中高 |
| 明暗 | 浅色 |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 是 |

**适用场景**：creative agency pitch, design studio deck, ad shop credentials, brand creative review, concept presentation

**情绪关键词**：creative, confident, playful, design-led

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--pink` | `#F06CA8` | 正文/墨色 |
| `--pink-dark` | `#D14E8B` | 正文/墨色 |
| `--ink` | `#0F0F0F` | 正文/墨色 |
| `--ink-2` | `#2A2A2A` | 正文/墨色 |

**完整色板**（12 色）：`#000` `#0F0F0F` `#136636` `#1F8A4C` `#2A2A2A` `#D14E8B` `#E4DCC4` `#E85A1F` `#EFE9D9` `#F06CA8` `#F5C518` `#FBD0E3`

**字体栈**：
- `Archivo Black`
- `Space Grotesk`
- `JetBrains Mono`

**设计令牌总数**：11 个 CSS 自定义属性

**最适合**：Anything that should feel design-led and confident: creative agency pitches, design studio decks, ad shop credentials, brand creative reviews, art-direction reviews. Also a great unexpected pick for a tech talk, research findings, or finance review when the speaker wants to lead with taste rather than convention.

**避免用于**：Contexts that demand institutional restraint and a quiet authority — the saturated multi-accent palette will read as expressive, not formal.

---

### Daisy Days (`daisy-days`)

> Cheerful pastel deck with hand-drawn daisies, stars, and rainbows. Friendly, soft, and warm.

| 属性 | 值 |
|---|---|
| 正式度 | 低 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：education / classroom, kids product launch, wellness program, community workshop, creator portfolio (craft / illustration), team kickoff, wedding / baby shower planning

**情绪关键词**：cheerful, playful, warm, sunny, wholesome

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--soft-pink` | `#F7C8D4` | 正文/墨色 |
| `--border` | `#2D2D2D` |  |
| `--border-width` | `3px` |  |

**完整色板**（21 色）：`#000` `#1E1E1C` `#232323` `#2D2D2D` `#6B6B6B` `#7ECDC0` `#85C5FE` `#8DE3B7` `#A8D8F0` `#A8E6CF` `#C6E3F6` `#D4A5E8` `#F5F0E6` `#F7C8D4` `#F8635F`
  …及另外 6 色

**字体栈**：
- `Fredoka One`
- `Quicksand`

**字体令牌**：
- `--font-display`: `'Fredoka One',cursive`
- `--font-body`: `'Quicksand',sans-serif`

**设计令牌总数**：19 个 CSS 自定义属性

**最适合**：Anything that should feel friendly, soft, and joyful: educational content, kids and family, wellness programs, community workshops, creator portfolios for craft / illustration. Also lovely for an unexpected playful internal kickoff, a wedding planning deck, or any moment where warmth is the message — including across tech or business contexts.

**避免用于**：Contexts where the audience explicitly expects authority and precision — the hand-drawn pastel SVG decorations are the opposite of buttoned-up.

---

### Editorial Forest (`editorial-forest`)

> Forest green, dusty pink, and warm cream meet Source Serif 4 in a quiet, intentional quarterly-review deck.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中（均衡） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 是 |

**适用场景**：quarterly review, internal readout, studio update, creative agency deck, research recap

**情绪关键词**：editorial, quiet, considered, warm, intentional

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--pink` | `#e89cb1` | 正文/墨色 |
| `--pink-deep` | `#d27e96` | 正文/墨色 |
| `--ink` | `#1a1a17` | 正文/墨色 |

**完整色板**（9 色）：`#111` `#1a1a17` `#243a21` `#2e4a2a` `#3a5a36` `#d27e96` `#e6dcc4` `#e89cb1` `#efe7d4`

**字体栈**：
- `Source Serif 4`
- `JetBrains Mono`

**设计令牌总数**：10 个 CSS 自定义属性

**最适合**：Anything that should feel like a considered editorial — quarterly reviews, internal readouts, studio updates, creative-agency presentations. Equally good for any deck that wants to feel warm and unhurried rather than corporate, including research recaps, book or program announcements, and team retrospectives.

**避免用于**：Contexts that need to feel urgent, punchy, or sales-driven — the palette and rhythm are intentionally quiet.

---

### Editorial Tri-Tone (`editorial-tri-tone`)

> Three-color editorial system: dusty pink, mustard cream, and deep burgundy, set in Bricolage + Instrument Serif.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 中（均衡） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 是 |

**适用场景**：editorial / magazine pitch, fashion brand deck, lifestyle media, literary / cultural, art direction review

**情绪关键词**：editorial, warm, intentional, moody

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--pink` | `#F2B6C6` | 正文/墨色 |
| `--pink-deep` | `#F2B6C6` | 正文/墨色 |
| `--ink` | `#7A1F35` | 正文/墨色 |

**完整色板**（3 色）：`#7A1F35` `#F2B6C6` `#F2D86A`

**字体栈**：
- `Bricolage Grotesque`
- `Instrument Serif`
- `JetBrains Mono`

**设计令牌总数**：11 个 CSS 自定义属性

**最适合**：Anything that should feel like a fashion-magazine spread: editorial pitches, fashion brand decks, lifestyle media, art direction reviews. Equally good for any deck — including tech, research, or business — that wants tri-tone discipline and serif/sans contrast instead of the usual neutrals.

**避免用于**：Decks that need to read as soft or comforting — the burgundy/pink/cream tri-tone is intentionally high-contrast and styled.

---

### Emerald Editorial (`emerald-editorial`)

> A magazine-cover business deck: emerald + navy + paper, double-rule masthead ornaments, and a bold Bodoni-style display serif.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 中（均衡） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 是 |

**适用场景**：leadership presentation, quarterly review, strategy readout, planning office deck, executive briefing

**情绪关键词**：editorial, considered, confident, magazine-cover

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#3CD896` | 背景/纸张 |
| `--bg-2` | `#2DC684` | 背景/纸张 |
| `--bg-3` | `#25B377` | 背景/纸张 |
| `--ink` | `#0F1A5C` | 正文/墨色 |
| `--ink-2` | `#1B2774` | 正文/墨色 |
| `--ink-3` | `#3A4593` | 正文/墨色 |
| `--paper` | `#F1E9D6` | 背景/纸张 |

**完整色板**（8 色）：`#0F1A5C` `#0a0a0a` `#1B2774` `#25B377` `#2DC684` `#3A4593` `#3CD896` `#F1E9D6`

**字体栈**：
- `Bodoni Moda`
- `Playfair Display`
- `DM Serif Display`
- `Rozha One`
- `Yeseva One`
- `Manrope`

**字体令牌**：
- `--display-font`: `'Bodoni Moda', serif`

**设计令牌总数**：10 个 CSS 自定义属性

**最适合**：Anything that should feel like the front of a serious magazine, including but not limited to leadership readouts, planning-office reviews, and strategy briefings. The double-rule masthead ornament gives it editorial gravitas without making it stiff — also a great unexpected pick for product launches or research recaps that want to feel considered rather than corporate.

**避免用于**：Contexts that need to read as quiet, neutral, or institutionally restrained — the emerald field is too saturated to disappear into the background.

---

### Grove (`grove`)

> Forest-green canvas with cream type, classical Playfair serifs, and a single rust accent.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 中（均衡） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 12 |
| 含 deck-stage.js | 否 |

**适用场景**：sustainability brand, wellness brand, outdoor / nature product, winery or restaurant, literary or arts deck, advisory deliverable, bilingual EN/CN deck

**情绪关键词**：organic, considered, warm, literary, natural

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#192b1b` | 背景/纸张 |
| `--c-bg-alt` | `#1e3221` | 背景/纸张 |
| `--c-bg-light` | `#e8e4d6` | 背景/纸张 |
| `--c-bg-light-alt` | `#dedad0` | 背景/纸张 |
| `--c-accent` | `#c8524a` | 强调色 |
| `--c-border` | `rgba(212, 207, 191, 0.12)` |  |
| `--c-border-light` | `rgba(25, 43, 27, 0.14)` |  |

**完整色板**（6 色）：`#192b1b` `#1e3221` `#c8524a` `#d4cfbf` `#dedad0` `#e8e4d6`

**字体栈**：
- `Jost`
- `Playfair Display`
- `JetBrains Mono`
- `Noto Serif SC`
- `Noto Sans SC`

**设计令牌总数**：34 个 CSS 自定义属性

**最适合**：Anything that should feel organic, considered, and grown-up: sustainability and wellness brands, outdoor / nature products, wineries and restaurants, literary or arts decks, advisory deliverables, bilingual EN/CN reports. Also a calm, distinctive choice for tech, research, or business decks that want patience over urgency.

**避免用于**：Decks that need neon energy or rapid-fire pop — the forest-green canvas and Playfair serif commit to a slow, classical voice.

---

### Long Table (`long-table`)

> Warm cream and rust-red supper-club aesthetic with bold uppercase grotesk headlines, Fraunces serifs, and pill-shaped outlined buttons.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 否 |

**适用场景**：supper club or dinner series, event or community gathering, small hospitality / restaurant brand, creative studio open house, membership or subscription pitch, wine or food brand catalogue, modern lifestyle brand

**情绪关键词**：warm, intimate, modern, friendly, small-batch, social, hospitality

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#FAF1E2` | 背景/纸张 |
| `--paper-d` | `#F2E5CF` | 背景/纸张 |
| `--paper-vd` | `#E8D7B6` | 背景/纸张 |
| `--ink` | `#B53D2A` | 正文/墨色 |
| `--ink-dp` | `#8E2D1F` | 正文/墨色 |

**完整色板**（6 色）：`#0a0a0a` `#8E2D1F` `#B53D2A` `#E8D7B6` `#F2E5CF` `#FAF1E2`

**字体栈**：
- `Bricolage Grotesque`
- `Fraunces`

**设计令牌总数**：6 个 CSS 自定义属性

**最适合**：Anything that should feel like a warm, intimate, modern hospitality / community brand: supper clubs, dinner series, small restaurants, creative-studio events, membership pitches, lifestyle and wine brands. Equally good for any deck wanting a single warm accent colour, mixed-weight typography, and a social-media-aware modern-editorial voice.

**避免用于**：Decks that need corporate polish, technical density, or a cold / minimalist register — the rust-red palette and bold serif mix are intentionally warm and people-facing.

---

### Mat (`mat`)

> Dark sage canvas with bone paper and burnt-orange accent; mid-century modern with wood undertones.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中（均衡） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 9 |
| 含 deck-stage.js | 否 |

**适用场景**：design studio credentials, architecture / interior brand, ceramics or craft brand, furniture pitch, advisory deliverable, bilingual EN/CN deck

**情绪关键词**：warm-modern, considered, tactile, mid-century

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#232e26` | 背景/纸张 |
| `--c-bg-alt` | `#2e3d30` | 背景/纸张 |
| `--c-bg-light` | `#ede6d0` | 背景/纸张 |
| `--c-bg-light-alt` | `#e4dac4` | 背景/纸张 |
| `--c-accent` | `#c07030` | 强调色 |
| `--c-border` | `rgba(240, 232, 210, 0.12)` |  |
| `--c-border-light` | `rgba(30, 40, 32, 0.14)` |  |

**完整色板**（8 色）：`#1e2820` `#232e26` `#2e3d30` `#7a4e24` `#c07030` `#e4dac4` `#ede6d0` `#f0e8d2`

**字体栈**：
- `Bricolage Grotesque`
- `DM Sans`
- `DM Mono`
- `Noto Sans SC`

**设计令牌总数**：35 个 CSS 自定义属性

**最适合**：Anything that should feel mid-century, tactile, and intentional: design studio credentials, architecture / interior brands, ceramics / craft / furniture, advisory decks. Also a warm, distinctive choice for tech, research, or business decks that want a considered analog feel instead of digital-cool.

**避免用于**：Contexts that need fast tech energy or institutional restraint — the muted sage and burnt-orange palette is intentionally warm and slow.

---

### Monochrome (`monochrome`)

> Ivory ledger paper with all-black type; Lora serif headlines, Jost body, no color at all.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 高（信息密集） |
| 明暗 | 浅色 |
| 幻灯片数 | 18 |
| 含 deck-stage.js | 否 |

**适用场景**：user research synthesis, white paper, longform report, academic deck, policy brief, advisory deliverable, bilingual EN/CN deck

**情绪关键词**：restrained, literary, archival, ledger

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#fafadf` | 背景/纸张 |
| `--c-bg-alt` | `#f2f2d2` | 背景/纸张 |
| `--c-bg-light` | `#fafadf` | 背景/纸张 |
| `--c-bg-light-alt` | `#f0f0d4` | 背景/纸张 |
| `--c-bg-cream` | `#f5f0e4` | 背景/纸张 |
| `--c-accent` | `#1a1a16` | 强调色 |
| `--c-border` | `#1a1a16` |  |
| `--c-border-light` | `#1a1a16` |  |

**完整色板**（7 色）：`#1a1a16` `#5e5e54` `#8a8a80` `#f0f0d4` `#f2f2d2` `#f5f0e4` `#fafadf`

**字体栈**：
- `Jost`
- `JetBrains Mono`
- `Lora`
- `Noto Serif SC`
- `Noto Sans SC`

**设计令牌总数**：39 个 CSS 自定义属性

**最适合**：Anything that should feel like a hand-typeset ledger: user research synthesis, white papers, longform reports, academic and policy briefs, advisory deliverables, bilingual EN/CN reports. Equally good for tech, design, or brand decks that want their words to be the only thing on the page.

**避免用于**：Decks that need visual personality or color-led storytelling — the all-ink palette is intentionally austere.

---

### Neo-Grid Bold (`neo-grid-bold`)

> Editorial neo-brutalism with a single neon yellow accent on off-white paper.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 高（信息密集） |
| 明暗 | 浅色 |
| 幻灯片数 | 13 |
| 含 deck-stage.js | 是 |

**适用场景**：product launch, design review, founder pitch, brand deck, consulting findings, conference talk

**情绪关键词**：confident, punchy, editorial, modern

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#ECECE8` | 背景/纸张 |
| `--ink` | `#0A0A0A` | 正文/墨色 |
| `--paper` | `#F5F4EF` | 背景/纸张 |
| `--accent` | `#E6FF3D` | 强调色 |

**完整色板**（12 色）：`#0A0A0A` `#0a0a0a` `#0b0b0b` `#111` `#1a1a1a` `#1f1f1f` `#2a2a2a` `#8A8A85` `#E6FF3D` `#ECECE8` `#F5F4EF` `#fff`

**字体栈**：
- `Space Grotesk`
- `JetBrains Mono`

**设计令牌总数**：6 个 CSS 自定义属性

**宽高比**：16 / 10

**最适合**：Anything that should feel confident and editorial-graphic: design-led pitches, brand work, founder talks, conference keynotes. Excellent for stat-heavy slides, comparisons, and process flows. Just as strong for tech, research, or finance when the speaker wants to read as design-led rather than corporate.

**避免用于**：Contexts that need to feel quiet, traditional, or warm — the neon-yellow accent and uppercase display commit to a confident editorial voice.

---

### People's Platform (Block & Bold) (`peoples-platform`)

> Activist poster energy: blue, orange, red on cream, with Alfa Slab + Caveat Brush.

| 属性 | 值 |
|---|---|
| 正式度 | 中低 |
| 内容密度 | 中高 |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 是 |

**适用场景**：cultural commentary, manifesto, community / civic deck, design talk, campaign pitch, founder vision

**情绪关键词**：activist, loud, graphic, honest

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#F5F2EA` | 背景/纸张 |
| `--ink` | `#0E0E14` | 正文/墨色 |

**完整色板**（10 色）：`#0E0E14` `#111` `#1B1BB0` `#2C2CDC` `#B7281C` `#E83A2A` `#E89321` `#F2A03A` `#F4E9D6` `#F5F2EA`

**字体栈**：
- `Alfa Slab One`
- `Archivo Narrow`
- `Caveat Brush`
- `DM Mono`

**设计令牌总数**：9 个 CSS 自定义属性

**最适合**：Anything that should feel honest, loud, and graphic: cultural commentary, manifestos, civic and community decks, design talks, campaign pitches. Excellent for founder-vision moments, mission statements, or any deck — including across industries — that wants protest-poster energy instead of corporate polish.

**避免用于**：Contexts where institutional restraint is the actual goal — the saturated political-poster palette commits hard to expressive energy.

---

### Pin & Paper (`pin-and-paper`)

> Yellow paper with safety-pin illustrations, ink-blue handwritten Caveat, paper-grain texture.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 11 |
| 含 deck-stage.js | 是 |

**适用场景**：research findings with personality, qualitative report, founder reflection, creator essay deck, workshop debrief

**情绪关键词**：crafted, handmade, warm, thoughtful, literary

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#EFE56A` | 背景/纸张 |
| `--paper-2` | `#F5ECA0` | 背景/纸张 |
| `--paper-3` | `#E8D85A` | 背景/纸张 |
| `--ink` | `#1F3A8A` | 正文/墨色 |
| `--ink-soft` | `#2D4FB8` | 正文/墨色 |
| `--ink-line` | `#3457C4` | 正文/墨色 |

**完整色板**（14 色）：`#0E1430` `#1F3A8A` `#1a1a1a` `#2D4FB8` `#3457C4` `#6B7A2E` `#C2342B` `#C9A66B` `#D8702A` `#E8D85A` `#EFE56A` `#F5ECA0` `#F8F1D6` `#FBE6A4`

**字体栈**：
- `Caveat`
- `Space Grotesk`
- `DM Mono`

**设计令牌总数**：12 个 CSS 自定义属性

**最适合**：Anything that should feel hand-crafted, warm, and literary: qualitative research findings, founder reflections, longform brand stories, workshop debriefs. The signature safety-pin illustrations and paper-grain texture make it especially good for any deck — including tech or business — that wants personality and warmth over polish.

**避免用于**：Decks that need to feel digital-native polished or rigorously data-driven — handwritten Caveat is intentionally informal.

---

### Pink Script — After Hours (`pink-script`)

> Black canvas, hot pink accent, pearl-cream paper, Instrument Serif headlines: late-night editorial luxury.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 低（大字报/少量元素） |
| 明暗 | 深色 |
| 幻灯片数 | 9 |
| 含 deck-stage.js | 是 |

**适用场景**：fashion brand deck, creator personal brand, after-hours product (nightlife / dating / spirits), luxury launch, editorial feature

**情绪关键词**：nocturnal, moody, intentional, luxe, expressive

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--ink` | `#060507` | 正文/墨色 |
| `--ink-2` | `#0F0D11` | 正文/墨色 |
| `--paper` | `#F5EDF1` | 背景/纸张 |
| `--pink` | `#ED3D8C` | 正文/墨色 |
| `--pink-2` | `#FF66A8` | 正文/墨色 |
| `--pink-deep` | `#B81D67` | 正文/墨色 |

**完整色板**（10 色）：`#000` `#050306` `#060507` `#0A0709` `#0F0D11` `#1A1218` `#B81D67` `#ED3D8C` `#F5EDF1` `#FF66A8`

**字体栈**：
- `DM Serif Display`
- `Inter`
- `JetBrains Mono`

**设计令牌总数**：9 个 CSS 自定义属性

**宽高比**：1

**最适合**：Anything that should feel nocturnal, intentional, and a little luxe: fashion brand decks, creator personal brands, after-hours / nightlife / spirits launches, luxury product reveals, editorial features. Also a striking unexpected pick for a tech keynote, research synthesis, or business pitch that wants to land with magnetic confidence.

**避免用于**：Daytime corporate-professional and traditional B2B contexts where the dark canvas with hot-pink accent reads as too styled or too expressive.

---

### Playful (`playful`)

> Sun-warm peach background with Syne display: a friendly indie launch deck.

| 属性 | 值 |
|---|---|
| 正式度 | 低 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：creator portfolio, indie product launch, lifestyle brand, small-business pitch, newsletter / community

**情绪关键词**：warm, approachable, indie, friendly

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#F0C8A0` | 背景/纸张 |
| `--bg-alt` | `#E8B88E` | 背景/纸张 |
| `--accent` | `#1A1A1A` | 强调色 |

**完整色板**（4 色）：`#1A1A1A` `#E8B88E` `#F0C8A0` `#F7DEC6`

**字体栈**：
- `Space Grotesk`
- `Syne`

**设计令牌总数**：5 个 CSS 自定义属性

**最适合**：Anything that should feel warm, indie, and approachable: creator portfolios, indie product launches, lifestyle brands, small-business pitches, newsletter / community decks. Also welcoming for any deck — including tech or research — that wants to feel friendly and human rather than corporate.

**避免用于**：Contexts where institutional credibility matters more than warmth — the peach palette is intentionally informal.

---

### Raw Grid (`raw-grid`)

> Neo-brutalist deck with thick borders, offset shadows, and a pink/sage/ink palette.

| 属性 | 值 |
|---|---|
| 正式度 | 中低 |
| 内容密度 | 高（信息密集） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：startup pitch, accelerator demo day, founder pitch, indie product launch, brand deck, creator portfolio

**情绪关键词**：raw, punchy, energetic, confident

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--pink` | `#f2d4cf` | 正文/墨色 |

**完整色板**（6 色）：`#0a0a0a` `#333333` `#e5edd6` `#f2d4cf` `#f5f5f5` `#ffffff`

**设计令牌总数**：9 个 CSS 自定义属性

**最适合**：Anything that should feel direct and graphic-confident: founder pitches, accelerator demos, brand decks, indie launches, creator portfolios. Strong for stat slides, comparison tables, and process flows. Equally good for tech, research, or finance when the speaker wants the deck to feel scrappy-confident rather than buttoned-up.

**避免用于**：Contexts that need to feel soft, warm, or intentionally quiet — the brutalist borders and offset shadows commit to a graphic voice.

---

### Retro Windows (`retro-windows`)

> Windows 95 chrome: gray title bars, MS Sans Serif, pixel typography, full nostalgia.

| 属性 | 值 |
|---|---|
| 正式度 | 低 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：retro gaming pitch, Y2K brand, creator portfolio (90s aesthetic), tech-history talk, shitpost-but-make-it-fancy deck

**情绪关键词**：nostalgic, retro, geeky, playful

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg-gray` | `#c0c0c0` | 背景/纸张 |
| `--bg-light` | `#d4d0c8` | 背景/纸张 |
| `--bg-dark` | `#808080` | 背景/纸张 |

**完整色板**（18 色）：`#000000` `#000080` `#0000a0` `#008000` `#008080` `#1084d0` `#222222` `#404040` `#505050` `#555` `#800000` `#808000` `#808080` `#a0a0a0` `#c0c0c0`
  …及另外 3 色

**字体栈**：
- `VT323`
- `Press Start 2P`

**设计令牌总数**：17 个 CSS 自定义属性

**最适合**：Anything that should feel knowingly nostalgic: retro gaming, Y2K-aesthetic brands, creator portfolios with a 90s vibe, tech-history talks, deliberately tongue-in-cheek decks. A great choice anywhere a playful retro reference is the entire point.

**避免用于**：Decks that need to read as modern, elegant, or institutionally credible — the Win95 chrome will always read as a costume.

---

### Retro Zine (`retro-zine`)

> Beige paper with green accent and Bebas Neue + Caveat: a riso-printed zine in HTML form.

| 属性 | 值 |
|---|---|
| 正式度 | 中低 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：indie zine / publication, music or arts brand, creator portfolio, small-batch / craft launch, cultural / community deck

**情绪关键词**：crafted, lo-fi, underground, warm-retro

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--bg` | `#C8B99A` | 背景/纸张 |
| `--bg-dark` | `#B8A98A` | 背景/纸张 |

**完整色板**（6 色）：`#008F4D` `#00A85D` `#1A1A1A` `#B8A98A` `#C8B99A` `#F4EFE6`

**字体栈**：
- `Bebas Neue`
- `Caveat`
- `Space Grotesk`

**设计令牌总数**：7 个 CSS 自定义属性

**最适合**：Anything that should feel printed, lo-fi, and crafted: indie zines and publications, music / arts brands, creator portfolios, small-batch craft launches, community decks. Also a great underdog choice for tech, research, or business decks that want a riso-print warmth instead of digital polish.

**避免用于**：Contexts that demand digital-native polish or fast modern-tech energy — the layered zine aesthetic intentionally feels handmade.

---

### Sakura Chroma (`sakura-chroma`)

> Vintage Japanese cassette-package aesthetic: cream paper, diagonal rainbow ribbons, condensed bold type, JIS-style spec checkboxes.

| 属性 | 值 |
|---|---|
| 正式度 | 低 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 8 |
| 含 deck-stage.js | 否 |

**适用场景**：product launch or catalogue, indie hardware or analog studio brand, music label or release schedule, creative studio annual report, magazine or zine pitch, vintage-flavored brand campaign

**情绪关键词**：retro, playful, kawaii-tech, warm, tactile, product-catalogue

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#F1E6CB` | 背景/纸张 |
| `--paper-dk` | `#E5D6B0` | 背景/纸张 |
| `--ink` | `#3A2516` | 正文/墨色 |
| `--pink` | `#E54489` | 正文/墨色 |

**完整色板**（10 色）：`#0e0e0e` `#3A2516` `#3D9F47` `#3F8BC4` `#E5392A` `#E54489` `#E5D6B0` `#F09131` `#F0BC2A` `#F1E6CB`

**字体栈**：
- `Big Shoulders Display`
- `Albert Sans`
- `JetBrains Mono`
- `Noto Sans JP`

**设计令牌总数**：10 个 CSS 自定义属性

**宽高比**：1 forces height to match the
       width set per-petal below, so percentages on the parent stay
       useful but the shape is always round. */
    position: absolute

**最适合**：Anything that should feel like a vintage Japanese cassette package or a TDK / Sony / Sakura Color product catalogue: indie hardware brand decks, music-label release schedules, analog studio retrospectives, zine and magazine pitches, kawaii-tech product launches, creative-studio annual reports. Equally good for any deck wanting bold colour, condensed display type, and a tactile printed-product personality.

**避免用于**：Decks that need restrained, corporate, or quiet typography — the bold condensed lockups, ribbon stripes, and primary-colour palette are intentionally loud and product-page-y.

---

### Scatterbrain (`scatterbrain`)

> Post-it inspired: pastel sticky notes, Caveat handwriting, Shrikhand and Zilla Slab type stack.

| 属性 | 值 |
|---|---|
| 正式度 | 低 |
| 内容密度 | 高（信息密集） |
| 明暗 | 浅色 |
| 幻灯片数 | 10 |
| 含 deck-stage.js | 否 |

**适用场景**：brainstorm / workshop, creative agency credentials, design-thinking session, ideation pitch, art-direction review

**情绪关键词**：playful, creative, warm, messy-on-purpose, workshop

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--pink` | `#ffc9c9` | 正文/墨色 |
| `--pink-deep` | `#ff9f9f` | 正文/墨色 |
| `--paper` | `#f7f5f0` | 背景/纸张 |
| `--ink` | `#2d2a26` | 正文/墨色 |
| `--ink-light` | `#5c5750` | 正文/墨色 |

**完整色板**（31 色）：`#1864ab` `#2d2a26` `#2f9e44` `#4dabf7` `#5c5750` `#69db7c` `#74c0fc` `#8ce99a` `#a5d8ff` `#b2f2bb` `#c92a2a` `#c9b8a0` `#ced4da` `#d0bfff` `#d4c5b0`
  …及另外 16 色

**字体栈**：
- `Shrikhand`
- `Zilla Slab`
- `Caveat`

**设计令牌总数**：16 个 CSS 自定义属性

**宽高比**：4/3

**最适合**：Anything that should feel like a designer's whiteboard: brainstorms, workshops, creative-agency credentials, design-thinking sessions, ideation pitches, art-direction reviews. Equally fun for any deck — including tech, research, or business — that wants to read as in-progress thinking rather than polished conclusions.

**避免用于**：Contexts that demand precision and institutional weight — the post-it sticky-note aesthetic intentionally reads as warm and unfinished.

---

### Signal (`signal`)

> Deep navy canvas with bone paper and a single muted-gold accent; institutional with quiet weight.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 高（信息密集） |
| 明暗 | 混合（深色区域+浅色内容） |
| 幻灯片数 | 18 |
| 含 deck-stage.js | 否 |

**适用场景**：investor deck, consulting deliverable, board presentation, legal / policy brief, academic deck, advisory pitch, bilingual EN/CN deck

**情绪关键词**：institutional, trustworthy, considered, weighty

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#1c2644` | 背景/纸张 |
| `--c-bg-alt` | `#232f55` | 背景/纸张 |
| `--c-bg-light` | `#f0ece3` | 背景/纸张 |
| `--c-bg-light-alt` | `#e6e0d4` | 背景/纸张 |
| `--c-accent` | `#c8a870` | 强调色 |
| `--c-border` | `#2e3d5c` |  |
| `--c-border-light` | `#cac4b4` |  |

**完整色板**（16 色）：`#1a2030` `#1c2644` `#232f55` `#2d3f55` `#2e3d5c` `#3d5475` `#4e5a6e` `#526880` `#5a6270` `#8a96a8` `#9aa0a8` `#c8a870` `#cac4b4` `#e2dcd0` `#e6e0d4`
  …及另外 1 色

**字体栈**：
- `Source Serif 4`
- `DM Sans`
- `IBM Plex Mono`
- `Noto Serif SC`
- `Noto Sans SC`

**设计令牌总数**：35 个 CSS 自定义属性

**最适合**：Anything that should feel weighty, considered, and credibly institutional: investor decks, board presentations, consulting deliverables, legal / policy briefs, advisory pitches. Also a strong choice for tech, research, or brand work that wants to read as quietly authoritative rather than loud.

**避免用于**：Contexts that should feel hot, fast, or intentionally playful — the navy + gold restraint commits to a sober voice.

---

### Soft Editorial (`soft-editorial`)

> Cormorant Garamond serif on warm paper with sage, blush, and lemon accents.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 低（大字报/少量元素） |
| 明暗 | 浅色 |
| 幻灯片数 | 12 |
| 含 deck-stage.js | 是 |

**适用场景**：editorial feature, longform brand story, gallery or museum, literary pitch, advisory deliverable, wedding / lifestyle media

**情绪关键词**：literary, elegant, quiet, warm-classical

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--paper` | `#F2EEDF` | 背景/纸张 |
| `--paper-2` | `#ECE6D2` | 背景/纸张 |
| `--ink` | `#2A241B` | 正文/墨色 |
| `--ink-soft` | `#5C5345` | 正文/墨色 |
| `--pink` | `#E1A4C2` | 正文/墨色 |

**完整色板**（10 色）：`#1a1a1a` `#2A241B` `#5C5345` `#B7C7A8` `#C9BEDC` `#D6DD63` `#E1A4C2` `#E8C9B6` `#ECE6D2` `#F2EEDF`

**字体栈**：
- `Cormorant Garamond`
- `Work Sans`

**设计令牌总数**：9 个 CSS 自定义属性

**宽高比**：1/1.2

**最适合**：Anything that should feel literary, elegant, and unhurried: editorial features, longform brand stories, gallery / museum decks, advisory deliverables, wedding / lifestyle media, founder essays. Equally good for tech, research, or business decks that want a Sunday-supplement warmth instead of corporate polish.

**避免用于**：Decks that need visual heat or punch — the warm-paper palette and Cormorant serif are intentionally quiet.

---

### Stencil & Tablet (`stencil-tablet`)

> Bone paper with stencil-cut headlines and a six-color earth palette: archaeology meets brand.

| 属性 | 值 |
|---|---|
| 正式度 | 中高 |
| 内容密度 | 中（均衡） |
| 明暗 | 浅色 |
| 幻灯片数 | 11 |
| 含 deck-stage.js | 是 |

**适用场景**：museum / cultural institution, art / architecture brand, longform research, heritage / craft brand, manifesto

**情绪关键词**：archival, earthy, tactile, considered, graphic

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--ink` | `#0A0A0A` | 正文/墨色 |
| `--paper` | `#F4EFE0` | 背景/纸张 |

**完整色板**（12 色）：`#000000` `#0A0A0A` `#1a1a1a` `#2D7E73` `#3F73B7` `#6F7A2E` `#A06A3C` `#C73B7A` `#D8A93B` `#E2DCC9` `#EE7A2E` `#F4EFE0`

**字体栈**：
- `Bowlby One`
- `Stardos Stencil`
- `Barlow Condensed`
- `Inter`

**设计令牌总数**：11 个 CSS 自定义属性

**最适合**：Anything that should feel archival, tactile, and weighty-graphic: museum and cultural-institution decks, art / architecture brands, longform research, heritage and craft brands, manifestos. A great choice anytime — including across tech and business — when you want the deck to feel like a field manual rather than a slide deck.

**避免用于**：Contexts that demand digital-native polish or playful pop — the stencil-cut display and earth-tone palette commit to a deliberate analog feel.

---

### Studio (`studio`)

> Black canvas with electric-yellow type; high-voltage design studio aesthetic.

| 属性 | 值 |
|---|---|
| 正式度 | 中 |
| 内容密度 | 中（均衡） |
| 明暗 | 深色 |
| 幻灯片数 | 12 |
| 含 deck-stage.js | 否 |

**适用场景**：design studio credentials, creative agency pitch, brand showcase, art-direction review, fashion / sneaker brand, bilingual EN/CN deck

**情绪关键词**：electric, bold, graphic, design-led, high-contrast

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#1c1c1c` | 背景/纸张 |
| `--c-bg-alt` | `#242422` | 背景/纸张 |
| `--c-bg-light` | `#f5d200` | 背景/纸张 |
| `--c-bg-light-alt` | `#f0cc00` | 背景/纸张 |
| `--c-accent` | `#f5d200` | 强调色 |
| `--c-border` | `#2e2e2c` |  |
| `--c-border-light` | `rgba(28, 28, 28, 0.18)` |  |

**完整色板**（5 色）：`#1c1c1c` `#242422` `#2e2e2c` `#f0cc00` `#f5d200`

**字体栈**：
- `Barlow`
- `IBM Plex Mono`
- `Noto Sans SC`

**设计令牌总数**：34 个 CSS 自定义属性

**最适合**：Anything that should feel electric and design-led: studio credentials, creative agency pitches, brand showcases, art-direction reviews, fashion / sneaker brand work. Also a striking unexpected choice for tech, research, or business decks where the speaker wants the deck to *be* a brand statement.

**避免用于**：Contexts that should feel quiet or institutional — the black-and-electric-yellow palette is the loudest in the library.

---

### Vellum (`vellum`)

> Deep navy canvas with warm-yellow Cormorant serifs and a single dusty teal accent. A quiet, scholarly aesthetic.

| 属性 | 值 |
|---|---|
| 正式度 | 高 |
| 内容密度 | 低（大字报/少量元素） |
| 明暗 | 深色 |
| 幻灯片数 | 9 |
| 含 deck-stage.js | 否 |

**适用场景**：research findings, white paper or longform report, academic or university deck, advisory deliverable, literary or editorial pitch, founder reflection / vision deck, bilingual EN/CN deck

**情绪关键词**：scholarly, literary, considered, quiet, intellectual

**配色令牌**：

| 令牌名 | 值 | 用途 |
|---|---|---|
| `--c-bg` | `#2a3870` | 背景/纸张 |
| `--c-bg-alt` | `#343f80` | 背景/纸张 |
| `--c-bg-light` | `#2a3870` | 背景/纸张 |
| `--c-bg-light-alt` | `#343f80` | 背景/纸张 |
| `--c-accent` | `#3a7878` | 强调色 |
| `--c-border` | `rgba(232, 216, 92, 0.20)` |  |
| `--c-border-light` | `rgba(232, 216, 92, 0.20)` |  |

**完整色板**（7 色）：`#1f2858` `#2a3870` `#343f80` `#34407a` `#3a7878` `#E8D85C` `#F5E168`

**字体栈**：
- `Cormorant Garamond`
- `DM Sans`
- `Courier Prime`
- `Noto Serif SC`
- `Noto Sans SC`

**设计令牌总数**：36 个 CSS 自定义属性

**最适合**：Anything that should feel scholarly, literary, and quietly intelligent: research synthesis, white papers, academic and policy briefs, advisory deliverables, longform editorial pieces, founder reflections. Equally strong for any deck — including tech, business, or creator work — that wants a calm, considered atmosphere instead of energetic visuals.

**避免用于**：Contexts that need visual heat or pop — the navy + warm-yellow Cormorant aesthetic is intentionally low-tempo.

---
