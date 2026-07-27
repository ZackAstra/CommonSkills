---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '7817d624-3ff8-4a9f-92dc-53e65f7ecb2a'
  PropagateID: '7817d624-3ff8-4a9f-92dc-53e65f7ecb2a'
  ReservedCode1: '0e0ba748-6dff-40e8-873d-c1d03acc3c44'
  ReservedCode2: '0e0ba748-6dff-40e8-873d-c1d03acc3c44'
---

# PPT 字体搭配库（中文 + 拉丁）

本文件提供 5 套经过验证的中英文字体搭配方案，每套含 CJK 标题/正文 + 拉丁标题/正文 + 数字字体，可直接用于 `scripts/fix_ppt.py --pairing <id>` 或手工套用。

## 字体选择铁律

### 1. 一份 PPT 最多 2 个字体家族
- 1 个标题字体 + 1 个正文字体
- 通过字号、字重、颜色在同一字体家族里做层级，不靠换字体
- 唯一例外：品牌 Logo 字体不计入 2 种之内

### 2. 中英混排必须分设字体
中文好看的字，英文配上去像乱入——中文系统会用中文字体里的英文部分渲染，效果通常很简陋。

**正确做法**：每个 run 同时设拉丁字体名 + 东亚字体名（`<a:ea>` 元素），由 PowerPoint 自动选用。`fix_ppt.py` 已实现此机制。

### 3. 中英文之间加半角空格
"用iPhone拍照" → "用 iPhone 拍照"。中文出版界规范，眼睛在中英文切换时有喘息空间。

### 4. 数字用专用字体
表格里的数字不要用中文字体——切换到 DIN / Helvetica / Arial 等专为数字设计的字体，对齐感和专业度瞬间提升。

### 5. 字号落差 ≥ 1.5 倍
- 标题 48pt → 正文 26pt（1.85 倍）— 视觉层次清晰
- 标题 30pt → 正文 26pt（1.15 倍）— 观众多看 0.5 秒才能判断哪个是标题
- 推荐阶梯比例：1.618（黄金比例）

---

## 推荐字号阶梯（13.33×7.5in 16:9 标准幻灯片）

| 元素 | 字号 | 字重 | 用途 |
|---|---|---|---|
| 封面主标题 | 48-60pt | Bold | "这一页讲什么" |
| 章节分隔页 | 36-44pt | Bold | 大章节号/标题 |
| 页面主标题 | 28-36pt | Bold | 内容页标题 |
| 副标题 | 24-28pt | Regular/Semibold | 补充说明 |
| 关键结论句 | 24-28pt | Medium + 强调色 | 居中独句结论页 |
| 正文要点 | 18-24pt | Regular | 具体内容 |
| 图片标注 | 14-18pt | Regular | 图说 |
| 数据来源/脚注 | 10-12pt | Light | 引用 |

**投影场景**：字号整体上调 1.5 倍。24pt 在笔记本清楚，投影到 3 米宽幕布上相当于笔记本 11pt——完全看不清。

---

## 字体搭配方案

### 方案 1：`source-han-sans+inter` 思源黑体 + Inter（现代科技，跨平台首选）

| 角色 | 字体 | 备注 |
|---|---|---|
| CJK 标题/正文 | Source Han Sans CN（思源黑体）| Adobe + Google 联合开发，**免费商用**，7 个字重 |
| 拉丁标题/正文 | Inter | 2017 后兴起的屏幕阅读字体，开源 |
| 数字 | DIN Alternate | 等宽数字，对齐感强 |

**适用场景**：互联网、科技、SaaS、产品发布、跨平台演示（Windows/Mac/Linux/iOS/Android 全平台原生支持）。
**优点**：思源黑体是目前唯一真正跨平台的免费中文字体家族；Inter 是开源新世代屏幕字体的标杆。
**缺点**：需要用户预先安装思源黑体（系统不自带）；PowerPoint 不嵌入时会回退到雅黑。
**安装**：<https://github.com/adobe-fonts/source-han-sans/releases> / <https://rsms.me/inter/>

### 方案 2：`microsoft-yahei+arial` 微软雅黑 + Arial（Windows 默认，零安装）

| 角色 | 字体 | 备注 |
|---|---|---|
| CJK 标题/正文 | Microsoft YaHei（微软雅黑）| Windows Vista 起预装 |
| 拉丁标题/正文 | Arial | 全平台通用 |
| 数字 | Arial | |

**适用场景**：Windows 内部汇报、不预知接收方字体环境、客户现场打开 PPT 必须正常显示。
**优点**：零安装，所有 Windows 都有；雅黑屏幕可读性优于宋体。
**缺点**：跨 Mac 平台会回退到苹方/Helvetica（视觉略有差异）；不够"设计感"。
**注意**：发给 Mac 用户前用「文件 → 选项 → 保存 → 嵌入字体」或导出 PDF。

### 方案 3：`pingfang+helvetica` 苹方 + Helvetica（Mac 默认，跨端注意）

| 角色 | 字体 | 备注 |
|---|---|---|
| CJK 标题/正文 | PingFang SC（苹方）| macOS / iOS 预装 |
| 拉丁标题/正文 | Helvetica | Mac 预装 |
| 数字 | Helvetica Neue | |

**适用场景**：Mac + Keynote 用户、Apple 生态内分发、TED 风格演讲。
**优点**：苹方是 Apple 设计的现代黑体，屏幕表现极佳；零安装（在 Mac 上）。
**缺点**：Windows 没有苹方，会回退到宋体（视觉灾难）。**必须导出 PDF 或嵌入字体**。
**Windows 接收方**：要么换方案 1 或 2，要么用 PDF 锁定版式。

### 方案 4：`songti+georgia` 宋体 + Georgia（学术 / 政府 / 传统品牌）

| 角色 | 字体 | 备注 |
|---|---|---|
| CJK 标题/正文 | SimSun（宋体）| Windows 预装 |
| 拉丁标题/正文 | Georgia | 衬线，屏幕可读性优于 Times |
| 数字 | Georgia | |

**适用场景**：学术论文答辩、政府工作报告、传统文化品牌（茶叶、陶瓷、中式家具）、博物馆策展。
**优点**：庄重感、权威感；适合正式场合。
**缺点**：宋体在屏幕小于 20pt 时横画会丢失；不适合现代商业/科技。
**禁忌**：不要用于 95 后产品介绍——会有"上个时代"的观感。

### 方案 5：`fz-xiaobiaosong+fangsong` 方正小标宋 + 仿宋（党政公文，正式严肃）

| 角色 | 字体 | 备注 |
|---|---|---|
| CJK 标题 | FZXiaoBiaoSong-B05S（方正小标宋）| 党政公文标准标题字体 |
| CJK 正文 | FangSong（仿宋）| 党政公文标准正文字体 |
| 拉丁标题/正文 | Times New Roman | 公文标准 |
| 数字 | Times New Roman | |

**适用场景**：党政机关汇报、国企公文、人大/政协会议材料、正式外交场合。
**优点**：符合《党政机关公文格式》（GB/T 9704-2012）规范。
**缺点**：极度正式，不适合任何商业/创意场景。
**注意**：方正字体需方正授权；个人/党政内部使用通常免费，商业发布需购买。

---

## 字体快速选择流程图

```
做什么类型的演示？
  ├─ 互联网/科技/SaaS      → source-han-sans+inter（首选）或 microsoft-yahei+arial（兜底）
  ├─ 投资路演/咨询/金融     → microsoft-yahei+arial（Windows 兼容）或 source-han-sans+inter
  ├─ 学术/论文答辩          → songti+georgia
  ├─ 党政/国企/公文         → fz-xiaobiaosong+fangsong
  ├─ Apple 生态内分发       → pingfang+helvetica
  ├─ 跨平台必显一致         → source-han-sans+inter（唯一真跨平台）+ 导出 PDF
  ├─ 品牌/创意              → Helvetica/Inter + 你的品牌字体（确认商用授权）
  └─ 年轻/潮流              → 站酷快乐体/思源柔黑 + 苹方
```

---

## 按风格定位选字体（web-design-engineer 视角）

补充上面的快速选择，按 Web 设计师的风格定位分类。所有字体均**免费可商用**。

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

1. **一页最多 2-3 种字体**，其余层级靠字号/字重/字距完成（与上文铁律一致）
2. **数字专用字体**：默认字体的数字通常缺乏性格（如苹方的数字很平），特意挑选的数字字体能让关键数据跳脱出来。推荐 DIN Alternate / Lexend / Outfit
3. **字体声明顺序**（Web CSS / PPT XML 同理）：英文字体优先，中文字体在后
   - Web: `font-family: "Inter", "Noto Sans SC", sans-serif;`
   - PPT: `<a:latin typeface="Inter"/>` + `<a:ea typeface="Microsoft YaHei"/>`
   - 原因：英文字体不含汉字，中文字体含 a-z 英文和数字。把英文放第一，英文/数字用英文字体渲染；汉字回退到中文字体
4. **衬线 + 非衬线混用**：英文 Serif（Playfair Display 等）作装饰用于标题/品牌，Sans-serif 用于正文保证可读性。Luma AI、Perplexity 都用这种手法
5. **UI 友好字体**：选上下间距对称的字体，减少对齐还原问题（Inter / Geist / SF Pro 都是 UI 友好）

### 字号阶梯 Type Scale（web-design-engineer 核心法则）

选定基础字号（PPT 正文通常 18-24pt），按固定比例向上递增。详见 [web-design-principles.md](web-design-principles.md) §1。

| 比例 | 名称 | 视觉效果 | PPT 适用场景 |
|---|---|---|---|
| 1.25 | Major Third | 层级温和 | 商务/咨询/数据汇报（推荐默认）|
| 1.333 | Perfect Fourth | 对比明显 | 学术/政府/正式 |
| 1.5 / 1.618 | 黄金比例 | 极具张力 | 产品发布/营销/路演（仅封面和章节页）|

以正文 20pt 为基础，Major Third (1.25) 阶梯：正文 20pt → 副标题 25pt → 页面标题 31pt → 章节标题 39pt → 封面 49pt。

用 `fix_ppt.py --type-scale --ratio 1.25` 自动把字号吸附到阶梯。

---

## 避坑清单（打死都不要用的字体）

| 字体 | 为什么不要 |
|---|---|
| Comic Sans / Comic Sans MS | 看起来像小学生手写，全世界最被设计师鄙视 |
| Papyrus | "古埃及"风格，只适合做埃及旅游 PPT |
| Lobster / 其他花体字 | 可读性极差，小写基本认不出 |
| Impact | 只能在 meme 图里用，正经 PPT 会显得像恶搞 |
| Times New Roman（在屏幕场景）| 报纸印刷字体，屏幕阅读体验差；且默认字体=不用心 |
| 华文彩云 | 装饰过度，专业场合违和 |
| 方正姚体 / 华文行楷 | 书法味浓，仅适合特定文化场景 |
| 默认主题字体未改 | "我打开 PowerPoint 没动过"的信号 |

---

## 跨平台字体回退方案

### 回退链定义

每种字体搭配方案都有明确的跨平台回退链，确保在任何操作系统上都有可接受的渲染结果：

| 方案 | Windows 回退链 | macOS 回退链 | Linux 回退链 |
|---|---|---|---|
| source-han-sans+inter | Source Han Sans CN → Microsoft YaHei → SimHei | Source Han Sans CN → PingFang SC → Hiragino Sans | Source Han Sans CN → Noto Sans CJK SC → WenQuanYi Micro Hei |
| microsoft-yahei+arial | Microsoft YaHei → SimHei → Arial | PingFang SC → Helvetica → Arial | Noto Sans CJK SC → Liberation Sans → Arial |
| pingfang+helvetica | PingFang SC（需安装）→ Microsoft YaHei → Arial | PingFang SC → Helvetica Neue → Helvetica | Noto Sans CJK SC → Liberation Sans → Helvetica |
| songti+georgia | SimSun → NSimSun → Georgia | Songti SC → STSong → Georgia | Noto Serif CJK SC → WenQuanYi Zen Hei → Georgia |
| fz-xiaobiaosong+fangsong | FZXiaoBiaoSong → SimSun → FangSong → TNR | STSong → Songti SC → FangSong SC → TNR | Noto Serif CJK SC → WenQuanYi Zen Hei → TNR |

### python-pptx 回退链实现

在 `fix_ppt.py` 中，字体设置应同时指定主字体和回退字体：

```xml
<!-- 标题 run 示例：思源黑体 + Inter，含回退 -->
<a:r>
  <a:rPr lang="zh-CN">
    <a:latin typeface="Inter"/>
    <a:ea typeface="Source Han Sans CN"/>
    <!-- PowerPoint 自动回退：若 Inter 不可用 → Arial；若思源不可用 → 雅黑 -->
  </a:rPr>
  <a:t>标题文字</a:t>
</a:r>
```

> **注意**：python-pptx 的 `<a:latin>` 和 `<a:ea>` 只支持指定一个字体名，不支持 CSS 风格的逗号分隔回退链。实际回退由 PowerPoint 运行时根据系统字体表决定。因此：
> 1. **首选方案**：在目标机器上预装字体（思源黑体 + Inter）
> 2. **次选方案**：嵌入字体（`python-pptx` 设置 `presentation.embed_true_type_fonts`）
> 3. **兜底方案**：选择目标平台原生字体（Windows 用雅黑，Mac 用苹方）

### 场景：你用 Mac 做的 PPT，要发给 Windows 同事

| 优先级 | 方案 |
|---|---|
| 1（最佳）| 直接用方案 1（思源黑体 + Inter），全平台原生支持 |
| 2 | 用方案 2（雅黑 + Arial）+ Mac 也安装雅黑（可下载）|
| 3 | 导出 PDF 发送（字体嵌入，版式锁定）|
| 4 | PowerPoint "文件 → 选项 → 保存 → 嵌入字体"（部分字体因版权无法嵌入）|
| 5（最后底线）| 在封面备注"本 PPT 使用 XX 字体，请安装后查看"+ 附 PDF 参考版 |

### 场景：你用 Windows 做 PPT，要发给 Mac 同事

| 优先级 | 方案 |
|---|---|
| 1 | 用方案 1（思源黑体 + Inter），跨平台一致 |
| 2 | 用方案 3（苹方 + Helvetica）——但 Windows 自己也得装苹方 |
| 3 | 导出 PDF |

---

## 在 fix_ppt.py 中使用

```bash
# 套用思源黑体 + Inter（推荐，跨平台）
python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing source-han-sans+inter

# 套用雅黑 + Arial（Windows 兼容兜底）
python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing microsoft-yahei+arial

# 套用党政公文规范字体
python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing fz-xiaobiaosong+fangsong
```

## 在评分流程中的角色

1. **评分阶段**：检测 anti-pattern `unprofessional_font`（Comic Sans / Papyrus 等）/ `cjk_text_no_cjk_font`（中文文本但无 CJK 字体）
2. **修复阶段**：根据 PPT 场景选择对应方案（参考上表"适用场景"）
3. **验证阶段**：重新评分 → 确认 `cjk_text_no_cjk_font` 消失，字体家族数 ≤ 3

---

## 从 HTML 幻灯片模板提取的字体搭配（方案 6-10）

> 以下搭配从 `assets/html-templates/` 的 34 套模板中精选，使用 Google Fonts，适合 HTML→PNG→PPTX 流程。PPTX 直出场景需替换为系统字体（见回退列）。详见 [html-template-catalog.md](html-template-catalog.md)。

### 方案 6：`cormorant+work-sans` 科摩兰 + Work Sans（文学/编辑/画廊）

| 元素 | Google Font | 系统回退 | 字重 |
|---|---|---|---|
| 拉丁标题 | Cormorant Garamond | Georgia | 400/700 |
| 拉丁正文 | Work Sans | Arial | 300/400 |
| 数字/代码 | JetBrains Mono | Consolas | 400 |
| CJK 标题 | — | 宋体/思源宋体 | 400 |
| CJK 正文 | — | 微软雅黑/思源黑体 | 300 |

**风格**：文学、优雅、温暖、经典 | **适用**：品牌故事、画廊/博物馆、顾问交付物

### 方案 7：`playfair+inter` Playfair + Inter（投资/古典/学术）

| 元素 | Google Font | 系统回退 | 字重 |
|---|---|---|---|
| 拉丁标题 | Playfair Display | Georgia | 400/700 |
| 拉丁正文 | Inter | Arial | 300/400 |
| CJK 标题 | — | 思源宋体 | 400 |
| CJK 正文 | — | 思源黑体 | 300 |

**风格**：古典、克制、自信 | **适用**：投资论文、白皮书、画廊/文化

### 方案 8：`source-serif+dm-sans` Source Serif + DM Sans（研究/学术/双语）

| 元素 | Google Font | 系统回退 | 字重 |
|---|---|---|---|
| 拉丁标题 | Source Serif 4 | Georgia | 400/700 |
| 拉丁正文 | DM Sans | Arial | 300/400 |
| 数字/代码 | IBM Plex Mono | Consolas | 300 |
| CJK 标题 | Noto Serif SC | 思源宋体 | 300 |
| CJK 正文 | Noto Sans SC | 思源黑体 | 300 |

**风格**：学术、沉稳、双语 | **适用**：研究综合、白皮书、投资者报告 | **中英双语原生支持**

### 方案 9：`bricolage+fraunces` Bricolage + Fraunces（温暖/餐饮/社区）

| 元素 | Google Font | 系统回退 | 字重 |
|---|---|---|---|
| 拉丁标题 | Bricolage Grotesque | Arial | 400/700 |
| 拉丁斜体 | Fraunces | Georgia italic | 400 |
| 拉丁正文 | Bricolage Grotesque | Arial | 400 |
| CJK 正文 | — | 微软雅黑 | 300 |

**风格**：温暖、亲密、现代编辑 | **适用**：晚宴系列活动、餐厅品牌、会员制推销

### 方案 10：`shrikhand+zilla` Shrikhand + Zilla Slab（创意/头脑风暴/即兴）

| 元素 | Google Font | 系统回退 | 字重 |
|---|---|---|---|
| 拉丁标题 | Shrikhand | Impact | 400 |
| 拉丁副标题 | Zilla Slab | Georgia | 300 |
| 手写体 | Caveat | Comic Sans | 400 |
| 拉丁正文 | Zilla Slab | Georgia | 300 |

**风格**：顽皮、创意、工作室 | **适用**：头脑风暴、创意机构资质、设计思维工作坊