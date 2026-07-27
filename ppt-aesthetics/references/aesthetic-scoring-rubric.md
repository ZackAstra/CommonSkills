---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'b432d8ef-72d6-42f5-8b81-1c1f5ca1527b'
  PropagateID: 'b432d8ef-72d6-42f5-8b81-1c1f5ca1527b'
  ReservedCode1: 'efb85ad7-35fa-41de-b143-cb74097da5cb'
  ReservedCode2: 'efb85ad7-35fa-41de-b143-cb74097da5cb'
---

# PPT 美观评分准则（Aesthetic Scoring Rubric）

AI 视觉模型 + 结构化脚本对 PPT 页面美观度评分的标准。每个维度 1-10 分，加权得到总分，对应 A-F 等级。

## 评分流程概览

```
PPTX ─┬─> scripts/score_ppt_pages.py ──> 结构化分析（自动检测反模式）
      │
      └─> scripts/render_slides.py ───> PNG 图片
                                          │
                                          v
                                   AI 视觉模型（用下方 Prompt）
                                          │
                                          v
                                   8 维度评分 + 等级
                                          │
              结构化反模式 + 视觉评分 ───> 综合报告 + 修复建议
```

## 8 个评分维度

### 1. 视觉层级 Visual Hierarchy（权重 20%）

评估信息优先级的清晰度。

| 分数 | 标准 |
|---|---|
| 9-10 | 强焦点立即可见；标题/副标题/正文通过字号、字重、颜色清晰区分；视线自然跟随设计意图 |
| 7-8 | 清晰的主次区分；多数元素优先级合理；少量模糊 |
| 5-6 | 有层级但不一致；2+ 元素争抢注意力 |
| 3-4 | 层级扁平；分不清主次；字号过于接近 |
| 1-2 | 无可辨识层级；所有元素同等权重；混乱 |

**关键信号**：
- 标题 vs 正文：字号差 ≥ 1.5 倍（推荐 1.618 黄金比例）
- 主色仅用于 1-2 个关键元素，不是到处都是
- 留白分隔内容层级
- 封面主标题 48-60pt；页面标题 28-36pt；正文 18-24pt

### 2. 对齐与网格 Alignment & Grid（权重 15%）

评估结构精度和视觉对齐。

| 分数 | 标准 |
|---|---|
| 9-10 | 所有元素对齐到一致网格；页边距完全相同；零"浮游元素"（无对齐伙伴的元素）|
| 7-8 | 网格可见；1-2 处微小错位不分散注意力 |
| 5-6 | 大致对齐；部分元素显得随意摆放 |
| 3-4 | 多处错位；页边距不一致；元素漂移 |
| 1-2 | 无网格痕迹；随机摆放；潦草 |

**关键信号**：
- 文本块左边缘对齐
- 距幻灯片边缘页边距一致（推荐 0.67in 左右、0.5in 上下）
- 元素共享水平/垂直基线
- 无元素无意触碰幻灯片边缘
- 12 列网格：每列 ≈ 0.89in，槽 0.17in

### 3. 配色克制 Color Discipline（权重 15%）

评估颜色克制与协调。

| 分数 | 标准 |
|---|---|
| 9-10 | 单一主色一致使用；中性基底（白/灰/深）；无杂色；适度低饱和 |
| 7-8 | 主色主导，少量变化；多数调色板协调 |
| 5-6 | 2 个主色但尚算和谐；或 1 个主色使用不一致 |
| 3-4 | 多种不相关颜色；彩虹效果；撞色；过饱和 |
| 1-2 | 随机色彩泛滥；无可辨识调色板；刺眼霓虹；AI 紫蓝渐变 |

**关键信号**：
- 最多 1 个主色 + 中性色（60-30-10 法则）
- 无纯黑 #000 / 纯白 #FFF 背景除非有意为之
- 文字与背景对比度 ≥ 4.5:1（WCAG AA）
- 主色跨元素一致重复
- 禁用 AI 紫蓝渐变（#6366F1 / #818CF8 / #A855F7 等）

### 4. 字体品质 Typography Quality（权重 15%）

评估字体选择、搭配、字号、间距。

| 分数 | 标准 |
|---|---|
| 9-10 | 专业字体搭配（最多 2 家族）；标题字体有性格；正文字体高度可读；行距舒适；无孤行 |
| 7-8 | 字体选择得当；字号合理；少量间距问题 |
| 5-6 | 字体可接受但通用（Arial/Calibri 默认）；字号可但无差异化 |
| 3-4 | 混用 3+ 字体家族；字号不一致；间距拥挤或松散；难读 |
| 1-2 | 系统默认字体无思考；Comic Sans 级别选择；字号不可读 |

**关键信号**：
- 全 deck 最多 2 字体家族
- 标题字体与正文字体有区分
- 中文 PPT 推荐：思源黑体 / 微软雅黑 / 苹方（黑体系列）
- 中英混排必须分设字体（拉丁字体 + `<a:ea>` 东亚字体）
- 行距 1.2-1.5 倍
- 无孤行（最后一行只剩 1 个词）
- 正文不用全大写

### 5. 留白 Whitespace（权重 10%）

评估负空间运用。**双向检测**：既要避免拥挤（空白太少），也要避免空旷（元素占页面比例过低）。

| 分数 | 标准 |
|---|---|
| 9-10 | 自信运用留白；每个元素都有空间；元素面积占页面 40-70%；页边距充裕；视觉重量分布均衡 |
| 7-8 | 间距良好；某区域略拥挤或略空但整体通透；元素面积占比在 30-80% |
| 5-6 | 间距适中但不慷慨；幻灯片感觉"被填满"或大面积空白（元素面积 < 30%） |
| 3-4 | 拥挤（元素触碰，无视觉休息）或空旷（元素面积 < 20%，像漂浮在汪洋中） |
| 1-2 | 塞满（无页边距，令人窒息）或几乎空白（仅零星小元素，页面浪费） |

**关键信号**：
- 幻灯片空白面积 15-40%（即元素面积占 60-85%）为最佳区间
- 空白面积 > 50% 视为空旷，按比例扣分
- 空白面积 < 10% 视为拥挤，按比例扣分
- 四周至少 0.5in 页边距
- 不同内容块之间有空间
- 不是从边到边填满
- 有意留空区域（尤其高 VARIANCE 场景）
- **空旷检测**：若某象限（1/4 页面）内无任何可见元素，视为布局失衡

### 6. 视觉一致性 Visual Consistency（权重 10%）

评估设计决策是否统一应用。

| 分数 | 标准 |
|---|---|
| 9-10 | 单一圆角系统；单一阴影风格；单一按钮风格；统一图标尺寸；统一间距；系统感强 |
| 7-8 | 多数一致；1-2 处偏差不破坏系统 |
| 5-6 | 部分不一致；圆角按钮旁挨着方角卡片；同类卡片阴影深度不同 |
| 3-4 | 单页多种竞争风格；隐喻混乱 |
| 1-2 | 随机；每个元素样式都不同；无系统 |

**关键信号**：
- 所有卡片同一圆角半径
- 所有按钮同一风格（实心/幽灵）
- 所有图标同一尺寸和线宽
- 分隔线和边框同一颜色和粗细

### 7. 内容密度 Content Density（权重 10%）

评估幻灯片内容是否服务于一个清晰目的。

| 分数 | 标准 |
|---|---|
| 9-10 | 一页一信息；最多 3 个关键元素；3 秒内可 grasp |
| 7-8 | 核心信息清晰；辅助细节存在但从属 |
| 5-6 | 多个信息争抢；幻灯片试图做太多 |
| 3-4 | 信息过载；项目符号繁重；文字墙 |
| 1-2 | 完全不可读；段落长度文本；无法视觉解析 |

**关键信号**：
- 最多 6 个项目符号（理想 3-4 个）
- 单块正文 ≤ 25 字
- 数据可视化而非列表
- 一页一结论
- 单页词数 ≤ 60

### 8. 专业度 Professional Polish（权重 5%）

评估区分专业与业余的收尾细节。

| 分数 | 标准 |
|---|---|
| 9-10 | 微妙阴影/深度；精致色阶；无对齐 off-by-one；高级感；细节考究可见 |
| 7-8 | 干净执行；少量粗糙边缘；高于平均 |
| 5-6 | 功能可用但通用；默认 PowerPoint 模板质量 |
| 3-4 | 可见粗糙边缘；元素尺寸不匹配；未打磨 |
| 1-2 | 明显潦草；无打磨努力；令人尴尬 |

**关键信号**：
- 卡片用微妙阴影（不是重落影）
- 浅色背景用主色 tint（不是全饱和）
- 图标在容器内居中对齐
- 无拉伸或像素化图片
- 无默认模板感

---

## AI 视觉评分 Prompt

把下面这段 Prompt 与渲染好的 PNG 一起送给视觉模型：

```
分析这张 PPT 幻灯片图片的美观度。按以下 8 个维度打分（1-10）并给出一句中文理由。

维度与权重（与结构化脚本评分同维度，便于分数合并）：
1. whitespace (15%) 留白 — 负空间是否充分？不拥挤？页边距是否充裕？元素面积占页面 60-70%？无象限完全空白？
2. type_scale (15%) 字号阶梯 — 标题/副标题/正文是否有 Major Third (1.25×) 以上阶梯？字号比是否 ≥ 1.25？
3. color_harmony (15%) 配色和谐 — 是否遵循 60-30-10？无 AI 紫蓝渐变？无纯黑 #000 / 纯白 #FFF 滥用？
4. alignment (10%) 对齐与网格 — 元素是否对齐到一致网格？页边距是否均匀？间距是否遵循 4/8px 节奏？
5. spacing (10%) 间距 — 元素间距是否一致？段落间距是否合理？
6. imagery (10%) 图像完整性 — 图片是否高清无拉伸？无占位符？图表有数据来源？
7. consistency (10%) 视觉一致 — 圆角、阴影、按钮、图标尺寸/风格是否统一？
8. hierarchy (15%) 层次 — 是否有清晰焦点？3 等大卡片？占位符文本(TODO/TBD)？字号无层级？

等级映射：8.5-10=A, 7.0-8.4=B, 5.5-6.9=C, 4.0-5.4=D, 1.0-3.9=F

品牌模板豁免规则：
- **电信品牌模板装饰条**（红黄渐变丝带/色带、天翼 logo、5G 标识、品牌口号）属于中国电信官方品牌 VI，不应视为配色杂乱或精致度缺陷。评分时在 `color_harmony`、`consistency` 维度中**豁免**模板自带装饰元素的影响，仅评估用户添加内容的配色一致性和精致度。

附加扣分（自动检测到以下反模式时，对应维度 -1 到 -3 分）：
- AI 紫蓝渐变背景（#6366F1 / #818CF8 等）→ color_harmony -2
- 3 个等大卡片无层级 → hierarchy -2
- 文字墙（>40 词正文）→ whitespace -2
- Comic Sans / Papyrus 等不专业字体 → type_scale -3
- 图片拉伸变形 → imagery -2
- 内容触碰边缘无页边距 → whitespace -2
- 超过 3 种主色 → color_harmony -2
- 3D 图表 → imagery -2
- 默认 PowerPoint 模板未改 → consistency -2
- 页面填充率 < 40%（空旷）或 > 85%（拥挤）→ whitespace -2
- 象限空白（1/4 页面无元素）→ whitespace -1

严格输出 JSON（不要 markdown 代码块）：
{
  "dimensions": {
    "whitespace": {"score": N, "reason": "..."},
    "type_scale": {"score": N, "reason": "..."},
    "color_harmony": {"score": N, "reason": "..."},
    "alignment": {"score": N, "reason": "..."},
    "spacing": {"score": N, "reason": "..."},
    "imagery": {"score": N, "reason": "..."},
    "consistency": {"score": N, "reason": "..."},
    "hierarchy": {"score": N, "reason": "..."}
  },
  "weighted_total": N,
  "overall_grade": "A|B|C|D|F",
  "top_3_issues": ["...", "...", "..."],
  "improvement_suggestion": "..."
}
```

`scripts/score_ppt_pages.py` 输出的 JSON 报告中也包含此 Prompt（`vision_scoring_prompt` 字段）。

---

## 等级映射

| 加权总分 | 等级 | 含义 |
|---|---|---|
| 8.5 - 10.0 | A | 优秀 — 可交付 |
| 7.0 - 8.4 | B | 良好 — 小幅优化 |
| 5.5 - 6.9 | C | 一般 — 显著改进 |
| 4.0 - 5.4 | D | 低于平均 — 大改 |
| 1.0 - 3.9 | F | 需重做 |

---

## 反模式自动扣分

由 `scripts/score_ppt_pages.py` 自动检测并扣分（详见 [anti-pattern-fixes.md](anti-pattern-fixes.md)）：

| 反模式 | 检测方法 | 扣分维度 |
|---|---|---|
| AI 紫蓝渐变 | RGB 范围匹配 | color_discipline -2 |
| 3 等大卡片 | 同 top/width/height 的圆角矩形 | visual_hierarchy -2 |
| 文字墙 | 单页 > 60 词 | content_density -2 |
| 不专业字体 | BAD_FONTS 列表 | typography_quality -3 |
| 图片拉伸 | box_aspect vs img_aspect 偏差 > 8% | professional_polish -2 |
| 无页边距 | shape 距边缘 < 0.3in | whitespace -2 |
| 颜色过多 | 非中性色 > 5 | color_discipline -2 |
| 纯 RGB 饱和色 | #FF0000 / #00FF00 等 | color_discipline -1 |
| 字体家族过多 | deck 级 > 4 | typography_quality -2 |
| 中文文本无 CJK 字体 | has_cjk_text and not cjk_font | typography_quality -2 |

---

## 综合评分计算

```
final_score = weighted_total - sum(anti_pattern_penalties)
final_grade = grade_mapping(final_score)
```

**示例**：
- 视觉模型给出 weighted_total = 7.2（B）
- 结构化脚本检测到：ai_purple_palette (-2) + wall_of_text (-2) = -4
- final_score = 7.2 - 4 = 3.2 → F

→ 这种情况下结构化扣分过重，需人工调和。推荐做法：
- 若 weighted_total ≥ 7.0 且反模式 ≤ 2 个：取 weighted_total
- 若反模式 ≥ 3 个：final_score = weighted_total - min(反模式扣分总和, 3.0)
- 始终在报告中同时列出 weighted_total 和反模式扣分明细，由人工/用户最终判断

---

## 中文 PPT 特有评分考量

### 中英混排
- 检查中文与英文之间是否有半角空格（"用 iPhone 拍照" 而非 "用iPhone拍照"）
- 检查中文文本是否设置了 CJK 字体（`<a:ea>` 元素）
- 检查中英文字号是否协调（中文字号通常比英文略大 1-2pt 视觉平衡）

### 字号习惯
- 中文 PPT 字号普遍比英文 PPT 大 2-4pt（中文字符密度高，小字难读）
- 推荐中文正文 ≥ 20pt；英文正文 ≥ 18pt
- 中文标题 ≥ 32pt；英文标题 ≥ 28pt

### 字体回退
- 评分时需考虑字体回退风险：若 PPT 用了苹方但目标设备是 Windows，渲染会回退到宋体
- 评分报告中应标注"字体跨平台风险"作为改进建议

### 中文标点
- 中文段落应用全角标点（，。；：？！）
- 中英混排段落：英文部分用半角标点，中文部分用全角标点
- 数字与单位之间用半角空格（"23 %" → "23%"，但 "23 kg" 保留空格）

---

## 评分报告格式

`scripts/score_ppt_pages.py` 输出的 JSON 报告 + 视觉模型评分应合并为：

```json
{
  "file": "input.pptx",
  "total_slides": 12,
  "deck_summary": {
    "deck_font_families": ["Microsoft YaHei", "Arial"],
    "deck_font_count": 2,
    "deck_color_count": 5,
    "deck_top_colors": [["1B3A5C", 23], ...],
    "deck_anti_patterns": []
  },
  "slides": [
    {
      "slide_number": 1,
      "structural": {
        "anti_patterns": [],
        "layout_signals": {...}
      },
      "vision": {
        "dimensions": {...},
        "weighted_total": 8.2,
        "overall_grade": "B",
        "top_3_issues": [...],
        "improvement_suggestion": "..."
      },
      "final_score": 8.2,
      "final_grade": "B"
    }
  ],
  "deck_grade": "B",
  "deck_avg_score": 7.8,
  "worst_slides": [3, 7, 11],
  "top_repair_priorities": [
    "Slide 3: wall_of_text → fix_ppt.py --bullets",
    "Slide 7: ai_purple_palette → fix_ppt.py --colors --palette corp-blue",
    "Slide 11: stretched_image → fix_ppt.py --images"
  ]
}
```

---

## Token 报告格式（改进项 2）

> 借鉴自 UI 页面打分方法的 Token 差异表理念（CSDN 博客），把设计决策结构化为标准化 Token，便于多版本对比和与前端项目对接。

`scripts/score_ppt_pages.py` 在每页 slide 的 JSON 输出中新增 `tokens` 字段，提取以下 Token：

### Token 字段表

| Token | 说明 | 提取规则 |
|---|---|---|
| `color.primary` | 主色 | deck 内非中性色出现频率最高且频次 ≥ 2 |
| `color.accent` | 辅助色 | 非中性色出现频率第二且频次 ≥ 2 |
| `color.neutral_darkest` | 中性色最深（文字色） | 中性色中亮度最低 |
| `color.neutral_lightest` | 中性色最浅（背景色） | 中性色中亮度最高 |
| `color.background` | 背景 | 同 neutral_lightest（python-pptx 背景提取有限） |
| `typography.heading_font` | 标题字体 | 出现频率最高的字体（简化） |
| `typography.body_font` | 正文字体 | 同 heading_font（若 deck 未区分） |
| `typography.heading_size_pt` | 标题字号 | 同页最大字号 |
| `typography.body_size_pt` | 正文字号 | 同页最小字号 |
| `typography.type_scale_ratio` | 字号阶梯比 | heading_size / body_size |
| `radius.card_in` | 卡片圆角 | TODO（需读 XML adj 值，当前留空） |
| `radius.button_in` | 按钮圆角 | TODO |
| `radius.card_count` | 圆角矩形数 | ROUNDED_RECTANGLE 形状数 |
| `elevation.card_shadow_pt` | 卡片阴影 | TODO（需读 XML，当前留空） |
| `elevation.modal_shadow_pt` | 弹层阴影 | TODO |
| `spacing.margin_in` | 页边距 | 所有 shape 距边缘最小值 |
| `spacing.grid_step_in` | 网格步长 | 标称 0.08in（4/8px 节奏） |

### Token 输出示例

```json
{
  "tokens": {
    "color": {
      "primary": "1B3A5C",
      "accent": "F59E0B",
      "neutral_darkest": "1F2937",
      "neutral_lightest": "F9FAFB",
      "background": "F9FAFB"
    },
    "typography": {
      "heading_font": "Microsoft YaHei",
      "body_font": "Microsoft YaHei",
      "heading_size_pt": 36,
      "body_size_pt": 20,
      "type_scale_ratio": 1.8
    },
    "radius": {
      "card_in": null,
      "button_in": null,
      "card_count": 4
    },
    "elevation": {
      "card_shadow_pt": null,
      "modal_shadow_pt": null
    },
    "spacing": {
      "margin_in": 0.5,
      "grid_step_in": 0.08
    }
  }
}
```

### Token 使用场景

1. **多版本对比**：`compare_ppt_versions.py` 会读取各版本的 tokens，生成 token 差异表（见工作流 6）
2. **前端项目对接**：前端项目用 Tailwind / CSS 变量定义设计 Token，PPT 的 tokens 字段提供共同语言
3. **诊断报告**：报告读者看到"主色 #1B3A5C，标题 36pt，正文 20pt，比例 1.8"比看到"颜色过多"更具体

### 已知限制

- `radius.card_in` / `elevation.card_shadow_pt` 当前留空（需读 shape XML，后续完善）
- `color.primary` 在多色 deck 上可能误判（要求频次 ≥ 2 可缓解）
- `typography.heading_font` 简化为"出现频率最高的字体"，未严格区分标题/正文（后续可按字号阈值细化）

---

## 场景化权重切换（改进项 4）

> 借鉴自 UI 打分方法的场景权重切换理念（标准权重 vs 应用商店权重），针对 PPT 场景定义 6 套预设权重。

### 使用方法

```bash
python scripts/score_ppt_pages.py input.pptx --scenario marketing --output report.json
```

### 7 套预设场景权重

| Scenario | whitespace | type_scale | color_harmony | alignment | spacing | imagery | consistency | hierarchy |
|---|---|---|---|---|---|---|---|---|
| **default**（默认） | 15% | 15% | 15% | 15% | 10% | 10% | 10% | 10% |
| **executive**（高管摘要） | 20% | 10% | 10% | 15% | 10% | 5% | 10% | 20% |
| **marketing**（营销 deck） | 10% | 10% | 20% | 10% | 10% | 15% | 10% | 15% |
| **data**（数据密集） | 5% | 10% | 10% | 15% | 10% | 10% | 10% | 30% |
| **gov**（党政公文） | 5% | 20% | 10% | 20% | 10% | 5% | 15% | 15% |
| **creative**（创意作品集） | 15% | 15% | 20% | 5% | 10% | 15% | 5% | 15% |
| **telecom**（电信品牌） | 10% | 15% | 20% | 15% | 10% | 5% | 15% | 10% |

### 场景选择建议

| PPT 场景 | `--scenario` | 选择理由 |
|---|---|---|
| 董事会 / 高管摘要 | `executive` | 留白和层级最重要（董事会要快速 grasp） |
| 产品发布 / 营销 deck | `marketing` | 配色和图像最重要（视觉冲击力） |
| 技术架构评审 | `data` | 信息密度和层次最重要（数据要充分） |
| 数据密集季报 | `data` | 同上 |
| 党政公文 / 政府汇报 | `gov` | 对齐和字体最重要（严肃规范） |
| 创意作品集 / 代理商提案 | `creative` | 图像、配色、留白最重要（艺术感） |
| 中国电信品牌交付物 | `telecom` | 品牌色一致性和专业度最重要 |
| 其他 / 不确定 | `default` | 平衡评估 |

### 场景对 Prompt 的影响

当指定 `--scenario` 时，脚本输出的 `vision_scoring_prompt` 会：
1. 按场景权重重排维度描述
2. 加入场景提示语（如"本 PPT 为高管摘要场景，重点评估信息传递效率和视觉克制"）
3. 反模式扣分规则不变（保证检测一致性）

---

## PPT 微调点速查清单（改进项 3）

> 借鉴自 UI 页面打分方法的"微调点速查清单"理念（CSDN 博客），改造为 PPT 场景的 10 维清单。适用于"多版本细微差异对比"，逐项核对可见差异。

### 1. 标题区 / 页眉
- 标题字号 / 字重 / 字距是否一致
- 标题对齐方式（左 / 中 / 右）是否一致
- 标题与副标题的间距、对齐基线
- 页眉装饰元素（线条 / 色块 / 图标）的位置与粗细
- 章节序号格式（"1" / "第一章" / "一、"）是否统一

### 2. 封面区 / 章节页
- 封面主标题字号（推荐 48-60pt）
- 封面副标题、署名、日期的位置与对齐
- 封面背景（纯色 / 图片 / 渐变）的选择
- 章节页是否有视觉差异化（避免与内容页雷同）
- 封面留白是否慷慨（避免塞满）

### 3. 正文区 / 内容布局
- 正文区页边距是否一致（推荐 0.5in 上下、0.67in 左右）
- 正文区是否使用一致网格（12 列网格）
- 内容块间距是否均匀
- 一页是否只表达一个核心信息
- 项目符号数量是否 ≤ 6 个

### 4. 配色
- 主色是否单一（60-30-10 法则）
- 主色饱和度是否一致（不要一页深蓝一页亮蓝）
- 中性灰阶是否使用同一套色阶系统（50-950）
- 是否有 AI 紫蓝渐变（#6366F1 等，应禁用）
- 数据可视化配色是否色盲安全

### 5. 字体
- 全 deck 字体家族是否 ≤ 3
- 中英混排是否分设字体（拉丁 + CJK）
- 标题与正文字号差是否 ≥ 1.5 倍
- 字号是否套用 Type Scale 阶梯（1.25 / 1.333 / 1.618）
- 是否有 Comic Sans 等不专业字体

### 6. 对齐 / 网格
- 文本块左边缘是否对齐
- 元素是否共享水平 / 垂直基线
- 是否有"浮游元素"（无对齐伙伴）
- 页边距是否一致
- 网格步长是否套用 4/8px 节奏（PPT 中为 0.04in / 0.08in）

### 7. 图表
- 图表是否有"So what?"结论句（14-16pt 强调色）
- 图表是否有数据来源（9-10pt 浅灰）
- 图表类型是否匹配数据特征（分类用柱状、趋势用折线、占比用环图）
- 图表配色是否与 deck 主色一致
- 是否禁用了 3D 图表、网格线、图表边框

### 8. 图标 / 图片
- 图标风格是否统一（线性 / 扁平 / 拟物不混用）
- 图标尺寸是否一致
- 图片宽高比是否未变形（偏差 ≤ 8%）
- 图片是否统一应用了圆角 / 阴影
- 图标库是否同一套（不要混用 Material Icons 和 Font Awesome）

### 9. 页脚 / 页码
- 页脚信息是否一致（公司名 / 日期 / 页码）
- 页码位置 / 字号 / 字体是否统一
- 页脚是否与主内容有足够间距
- 是否有不必要的水印

### 10. 一致性
- 圆角系统是否统一（所有卡片同一 radius）
- 阴影系统是否统一（所有卡片同一 elevation）
- 按钮风格是否统一（实心 / 幽灵不混用）
- 分隔线 / 边框是否同一颜色和粗细
- 转场动画是否克制（80% 页零动画）

### 使用方法

1. 在版本对比时，对每个版本逐项打勾 ✓ / ✗ / ~（部分符合）
2. 统计每个版本的符合项数，作为辅助判断
3. 重点列出"~"项最多的版本，标注"细节未打磨"
4. 与 8 维度评分配合使用：维度分看综合，清单看细节

### 清单与 8 维度评分的对应关系

| 微调点清单 | 主要影响的 8 维度 |
|---|---|
| 1. 标题区 / 2. 封面区 | visual_hierarchy, professional_polish |
| 3. 正文区 | alignment_grid, whitespace, content_density |
| 4. 配色 | color_discipline |
| 5. 字体 | typography_quality |
| 6. 对齐 / 网格 | alignment_grid |
| 7. 图表 | content_density, professional_polish |
| 8. 图标 / 图片 | visual_consistency, professional_polish |
| 9. 页脚 / 页码 | visual_consistency |
| 10. 一致性 | visual_consistency |

清单是"诊断单"，维度分是"体检指标"——清单帮助定位具体问题，维度分帮助量化严重程度。

---

## 自我批判维度定义

> 适用于工作流 7（自我批判交付）。Stage 1 由 `critique_engine.py` 自动检测，Stage 2 由 AI 视觉模型判断。

### Stage 1: 结构化检测（8 维度）

| 维度 | key | 严重度 | 检测方式 | 扣分 |
|---|---|---|---|---|
| 留白 | `whitespace` | soft | 空白面积占比 + 元素面积占比 + 象限空白检测 | -0.5/问题 |
| 字号阶梯 | `type_scale` | hard | 标题→正文 font_size 比例 < 1.2 为断裂 | -2/问题 |
| 配色一致性 | `color_harmony` | hard/soft | 颜色是否在调色板内 + 60-30-10 比例 | -2（超出调色板）/ -0.5（比例偏移） |
| 对齐与网格 | `alignment` | soft | shape.left/top 是否 4/8px 对齐 | -0.5/问题 |
| 间距 | `spacing` | soft | 元素间距是否一致 + 页边距是否充裕 | -0.5/问题 |
| 图像完整性 | `imagery` | hard | 图片拉伸/破损/占位符/图表无数据来源 | -2/问题 |
| 视觉一致性 | `consistency` | soft | 圆角/阴影/按钮风格是否统一 | -0.5/问题 |
| 层次 | `hierarchy` | hard | 3 等大卡片/占位符文本(TODO/TBD/XXX)/字号无层级 | -2/问题 |

**评分规则**：
- 每维度 0-10 分，10 分为无问题
- 最低 0 分（不出现负分）
- 页面分 = 8 维度等权平均
- 总分 = 各页算术平均

### Stage 2: 视觉模型批判（4 维度）

| 维度 | key | 通过阈值 | 评判要点 |
|---|---|---|---|
| 视觉层次 | `visual_hierarchy` | ≥ 7/10 | 标题/正文/辅助文字层次一眼可辨，字号比 ≥ 1.25 |
| 排版美感 | `typographic_aesthetic` | ≥ 7/10 | 字体有辨识度，布局有设计感，非"AI slop" |
| 配色一致性 | `color_discipline` | ≥ 7/10 | 60/30/10 比例，无突兀颜色，无 AI 紫蓝渐变 |
| 内容完整性 | `content_completeness` | ≥ 7/10 | 无占位符/TODO，图表有数据来源 |

**通过条件**：4 个维度全部 ≥ 7 分。

### 迭代控制

- 最多 2 轮（Stage 1 和 Stage 2 各自独立计数）
- 收敛条件：`hard_issues < 3` 则提前终止
- 第 2 轮后仍有问题：输出报告，标注未解决问题，交付
- 每轮记录到 `critique_log.json`