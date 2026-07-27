---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '56ee713a-5491-480f-9909-cb3ac30a1cdd'
  PropagateID: '56ee713a-5491-480f-9909-cb3ac30a1cdd'
  ReservedCode1: 'd7c62f32-c2ad-4e34-8ce1-452bdb9592cf'
  ReservedCode2: 'd7c62f32-c2ad-4e34-8ce1-452bdb9592cf'
---

# 视觉批判 Prompt 模板（Stage 2 — Visual Critique）

> Stage 2 视觉模型批判专用 Prompt。在 Stage 1 结构化脚本检测（`score_ppt_pages.py`）通过后，将每页渲染为图片，交给 AI 视觉模型做 4 维度批判。
>
> **维度设计说明**：Stage 2 使用 4 个聚合维度（visual_hierarchy, typographic_aesthetic, color_discipline, content_completeness），与 Stage 1 的 8 个细分维度（whitespace, type_scale, color_harmony, alignment, spacing, imagery, consistency, hierarchy）是不同粒度的评估。Stage 2 旨在快速走查，4 维度已涵盖 Stage 1 全部 8 维度的评分要点，不需要对齐命名。

---

## Agent 使用说明

1. **渲染图片**：
   - **PPTX**：运行 `python scripts/render_slides.py <input.pptx> --output-dir <png_dir>` 将每页导出为 PNG
   - **HTML**：用浏览器截图工具（如 Playwright `page.screenshot()`）对每页全页截图
2. **发送批判请求**：将每页 PNG 图片 + 下方 Prompt 模板主体发送给 AI 视觉模型（需支持图片输入）
3. **解析返回 JSON**：解析模型返回的严格 JSON，检查 `overall_passed` 字段
   - `overall_passed = true` → 该页通过视觉批判
   - `overall_passed = false` → 该页未通过，进入修复流程
4. **修复流程**（最多 2 轮）：
   - 按 `fix_suggestions` 数组中的建议逐条修复
   - 修复后重新渲染该页为 PNG
   - 再次发送图片 + Prompt 进行批判
   - 若 2 轮后仍未通过，标记该页为 `visual_critique_failed`，在最终报告中列出未通过页及剩余 issues

### 流程图

```
Stage 1 结构化检测 (score_ppt_pages.py)
    │
    ├─ 未通过 → 修复 → 重跑 Stage 1
    │
    └─ 通过 → 渲染 PNG → Stage 2 视觉批判 (本 Prompt)
                    │
                    ├─ overall_passed = true → ✅ 该页通过
                    │
                    └─ overall_passed = false
                            │
                            ├─ 第 1 轮修复 → 重新渲染 → 再次批判
                            │       │
                            │       ├─ 通过 → ✅
                            │       └─ 未通过 → 第 2 轮修复 → 重新渲染 → 再次批判
                            │                       │
                            │                       ├─ 通过 → ✅
                            │                       └─ 未通过 → ❌ 标记失败
                            │
                            └─ 最多 2 轮修复
```

---

## Prompt 模板主体

将以下 Prompt 与渲染好的 PNG 图片一起发送给 AI 视觉模型：

```
你是 PPT 视觉设计审查专家。请对这张幻灯片图片进行 4 个维度的视觉批判。

每个维度按 1-10 分评分，≥ 7 分为该维度通过（passed = true），< 7 分为不通过（passed = false）。
只有当全部 4 个维度都通过时，overall_passed 才为 true。

【4 个批判维度】

1. visual_hierarchy（视觉层次）
   评判要点：
   - 标题、正文、辅助文字的层次是否一眼可辨？
   - 是否有元素抢了标题的视觉焦点？
   - 标题与正文的字号比是否 ≥ 1.25（推荐 1.618 黄金比例）？
   - 封面主标题 48-60pt；页面标题 28-36pt；正文 18-24pt
   - 主色是否仅用于 1-2 个关键元素，而非到处都是？
   - 留白是否有效分隔了内容层级？
   扣分信号：
   - 字号比 < 1.25 → -2
   - 3 个等大卡片无层级 → -2
   - 多个元素争抢注意力 → -1

2. typographic_aesthetic（排版美感）
   评判要点：
   - 字体是否有辨识度？（使用 Arial / Inter / Roboto / Calibri 等通用字体直接扣分）
   - 标题字体与正文字体是否有区分？
   - 布局是否有设计感？（非 PowerPoint 默认模板感）
   - 中英混排是否分设字体（拉丁字体 + CJK 字体）？
   - 全 deck 字体家族是否 ≤ 3？
   - 行距是否在 1.2-1.5 倍之间？
   - 是否有孤行（最后一行只剩 1 个词）？
   扣分信号：
   - 使用 Arial / Calibri / Inter / Roboto 作为标题字体 → -2
   - 混用 3+ 字体家族 → -2
   - 默认 PowerPoint 模板未改 → -2
   - Comic Sans / Papyrus 等不专业字体 → -3
   - 中文文本未设置 CJK 字体 → -2

3. color_discipline（配色一致性）
   评判要点：
   - 是否遵循 60/30/10 比例（60% 背景 / 30% 辅助 / 10% 强调）？
   - 是否有突兀颜色（与主色调不协调的纯饱和色）？
   - 是否有 AI 紫蓝渐变（#6366F1 / #818CF8 / #A855F7 等）？→ 直接不通过
   - 主色是否跨页面一致重复？
   - 非中性色是否 ≤ 3 种？
   - 文字与背景对比度是否 ≥ 4.5:1（WCAG AA）？
   - 是否滥用纯黑 #000 / 纯白 #FFF？
   扣分信号：
   - AI 紫蓝渐变背景 → 直接 0 分（passed = false）
   - 超过 3 种主色 → -2
   - 强调色覆盖 > 40% 元素（违反 60-30-10）→ -1
   - 纯 RGB 饱和色（#FF0000 / #00FF00 等）→ -1
   - 纯黑 #000 文字 / 纯白 #FFF 卡片 → -1

4. content_completeness（内容完整性）
   评判要点：
   - 是否有占位符文本（"Lorem ipsum"、"TODO"、"待补充"、"XXX"）？
   - 是否有未替换的模板文字（"点击输入标题"、"请在此处添加内容"）？
   - 图表是否有标题和数据来源标注？
   - 图片是否有 alt 文本或 caption 说明？
   - 所有文本框是否都有实际内容（非空、非默认提示）？
   - 数据图表的轴标签是否完整？
   - 是否有"404 图片未找到"或破损图片占位？
   扣分信号：
   - 存在占位符 / TODO / 待补充 → 直接 0 分（passed = false）
   - 图表缺少标题或数据来源 → -2
   - 图片缺少 caption → -1
   - 空文本框或默认提示文字 → -2

【批判原则】
- 只做可判断的评估，不做纯主观偏好评价
- 7 分是及格线——交付物应明显高于平均水平，5 分不是及格
- issues 必须具体可定位（写"标题用 Arial"而非"字体不好看"）
- fix_suggestions 必须可执行（写"将标题字体改为 Clash Display"而非"换更好的字体"）
- 若某维度存在致命问题（如 AI 紫蓝渐变、占位符未替换），该维度直接 0 分

【品牌模板豁免】
若为电信品牌模板，模板自带的品牌装饰元素（红黄渐变丝带、天翼 logo、5G 标识、品牌口号等）属于官方品牌 VI，在 color_discipline 和 typographic_aesthetic 维度豁免评估，仅评判用户添加内容的部分。

严格输出以下 JSON 格式（不要 markdown 代码块，不要额外文字）：
{
  "stage": "visual",
  "slide_number": N,
  "dimensions": {
    "visual_hierarchy": {
      "score": N,
      "passed": true|false,
      "issues": ["具体问题1", "具体问题2"]
    },
    "typographic_aesthetic": {
      "score": N,
      "passed": true|false,
      "issues": ["具体问题1", "具体问题2"]
    },
    "color_discipline": {
      "score": N,
      "passed": true|false,
      "issues": ["具体问题1", "具体问题2"]
    },
    "content_completeness": {
      "score": N,
      "passed": true|false,
      "issues": ["具体问题1", "具体问题2"]
    }
  },
  "overall_passed": true|false,
  "fix_suggestions": [
    {
      "slide": N,
      "dimension": "visual_hierarchy|typographic_aesthetic|color_discipline|content_completeness",
      "action": "具体可执行的修复动作",
      "priority": "high|medium|low"
    }
  ]
}
```

---

## 输出格式说明

### 字段定义

| 字段 | 类型 | 说明 |
|---|---|---|
| `stage` | string | 固定为 `"visual"`，标识 Stage 2 视觉批判 |
| `slide_number` | int | 当前评判的页码（1-indexed） |
| `dimensions` | object | 4 个维度的评分详情 |
| `dimensions.<dim>.score` | int | 1-10 分 |
| `dimensions.<dim>.passed` | bool | score ≥ 7 时为 true |
| `dimensions.<dim>.issues` | string[] | 具体问题列表，每条可定位、可理解 |
| `overall_passed` | bool | 全部 4 维度 passed = true 时才为 true |
| `fix_suggestions` | array | 未通过时的修复建议列表 |
| `fix_suggestions[].slide` | int | 需修复的页码 |
| `fix_suggestions[].dimension` | string | 对应的维度名称 |
| `fix_suggestions[].action` | string | 具体可执行的修复动作 |
| `fix_suggestions[].priority` | string | high / medium / low |

### 输出示例

**通过的情况：**
```json
{
  "stage": "visual",
  "slide_number": 1,
  "dimensions": {
    "visual_hierarchy": {"score": 8, "passed": true, "issues": []},
    "typographic_aesthetic": {"score": 8, "passed": true, "issues": []},
    "color_discipline": {"score": 9, "passed": true, "issues": []},
    "content_completeness": {"score": 9, "passed": true, "issues": []}
  },
  "overall_passed": true,
  "fix_suggestions": []
}
```

**未通过的情况：**
```json
{
  "stage": "visual",
  "slide_number": 2,
  "dimensions": {
    "visual_hierarchy": {"score": 8, "passed": true, "issues": []},
    "typographic_aesthetic": {"score": 5, "passed": false, "issues": ["标题使用 Arial 字体，缺乏辨识度", "标题与正文字号比仅 1.15，低于 1.25 最低要求"]},
    "color_discipline": {"score": 7, "passed": true, "issues": ["强调色覆盖约 45% 元素，略超 60-30-10 建议"]},
    "content_completeness": {"score": 9, "passed": true, "issues": []}
  },
  "overall_passed": false,
  "fix_suggestions": [
    {"slide": 2, "dimension": "typographic_aesthetic", "action": "将标题字体从 Arial 改为 Clash Display 或思源黑体 Bold", "priority": "high"},
    {"slide": 2, "dimension": "typographic_aesthetic", "action": "将标题字号从 28pt 提升至 36pt，使字号比达到 1.5", "priority": "high"},
    {"slide": 2, "dimension": "color_discipline", "action": "将右侧 2 个卡片的强调色背景改为浅灰 #F3F4F6，降低强调色覆盖比例", "priority": "medium"}
  ]
}
```

**致命问题的情况（直接 0 分）：**
```json
{
  "stage": "visual",
  "slide_number": 3,
  "dimensions": {
    "visual_hierarchy": {"score": 7, "passed": true, "issues": []},
    "typographic_aesthetic": {"score": 7, "passed": true, "issues": ["正文使用 Microsoft YaHei，可接受但建议搭配更有性格的标题字体"]},
    "color_discipline": {"score": 0, "passed": false, "issues": ["背景使用 AI 紫蓝渐变 #6366F1 → #818CF8，属于明确禁用的 AI 生成痕迹"]},
    "content_completeness": {"score": 0, "passed": false, "issues": ["第 2 个文本框仍为占位符 '请在此处添加内容'", "图表缺少数据来源标注"]}
  },
  "overall_passed": false,
  "fix_suggestions": [
    {"slide": 3, "dimension": "color_discipline", "action": "将背景从紫蓝渐变改为纯色 #F9FAFB，主色用 #1B3A5C", "priority": "high"},
    {"slide": 3, "dimension": "content_completeness", "action": "将占位符 '请在此处添加内容' 替换为实际业务数据描述", "priority": "high"},
    {"slide": 3, "dimension": "content_completeness", "action": "在图表下方添加 '数据来源：2024 年度运营报告' 标注", "priority": "high"}
  ]
}
```

---

## 批判原则详述

### 1. 只做可判断的评估

✅ 正确："标题用 Arial，辨识度不足"
❌ 错误："字体不好看"（主观且不可执行）

✅ 正确："强调色 #F59E0B 覆盖了 4/7 个元素（57%），超过 60-30-10 的 10% 建议"
❌ 错误："颜色搭配不太协调"（模糊且无法定位）

### 2. 7 分是及格线

| 分数 | 含义 | 对应行动 |
|---|---|---|
| 9-10 | 优秀 — 可交付 | 无需修改 |
| 7-8 | 合格 — 通过 | 可选择性优化 |
| 5-6 | 不合格 — 需修复 | 必须修复后重新评判 |
| 3-4 | 较差 — 大改 | 需重构该页布局 |
| 1-2 | 极差 — 重做 | 该页需完全重新设计 |
| 0 | 致命问题 | 存在 AI 紫蓝渐变 / 占位符 / TODO 等硬性违规 |

> ⚠️ 7 分不是"还行"，而是"刚好达标"。交付物应该明显高于平均水平。

### 3. issues 必须具体

每条 issue 应包含：
- **什么元素**有问题（标题 / 正文 / 背景 / 图表 / 卡片）
- **具体是什么**问题（用了什么字体 / 什么颜色 / 什么比例）
- **为什么**这是问题（违反了哪条规则）

示例：
- ✅ "正文行距 1.0 倍，低于推荐的 1.2-1.5 倍区间，导致文字密集难读"
- ✅ "3 个卡片使用相同字号 18pt，缺乏主次区分"
- ❌ "排版有问题"

### 4. fix_suggestions 必须可执行

每条建议应包含：
- **改什么**（具体元素定位）
- **改成什么**（具体字体名 / 颜色值 / 字号 / 布局方式）
- **优先级**（high = 阻断通过 / medium = 建议修改 / low = 锦上添花）

示例：
- ✅ "将标题字体从 Arial 改为 Clash Display，字号从 28pt 提升至 36pt"
- ✅ "将背景从紫蓝渐变改为纯色 #F9FAFB"
- ❌ "换更好的字体"
- ❌ "改善配色"

---

## 与 Stage 1 的关系

| 阶段 | 检测方式 | 关注点 | 通过条件 |
|---|---|---|---|
| Stage 1 | 结构化脚本（`score_ppt_pages.py`） | 可编程检测的反模式（AI 紫蓝渐变色值、等大卡片尺寸、文字墙词数等） | 反模式数 = 0 |
| Stage 2 | AI 视觉模型（本 Prompt） | 需要视觉理解的维度（层次感、字体辨识度、配色协调性、内容完整性） | 全部 4 维度 ≥ 7 分 |

- Stage 1 和 Stage 2 是串行关系：先通过 Stage 1，再进入 Stage 2
- Stage 1 检测到的反模式会在 Stage 2 中作为扣分信号参考
- 若 Stage 1 已检测到 AI 紫蓝渐变，Stage 2 的 `color_discipline` 应直接判 0 分
- 若 Stage 1 未检测到反模式，Stage 2 仍可能因为视觉层面的美感问题判不通过

---

## 多页批量处理

对于多页 PPT/HTML，Agent 应：

1. 逐页渲染为 PNG
2. 逐页发送图片 + Prompt 进行批判
3. 汇总所有页的 JSON 结果
4. 输出 deck 级别的汇总报告：

```json
{
  "file": "input.pptx",
  "total_slides": 12,
  "visual_critique_summary": {
    "passed_slides": [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "failed_slides": [2],
    "overall_passed": false,
    "total_rounds": 1,
    "max_rounds_per_slide": 2
  },
  "slides": [
    {
      "slide_number": 1,
      "rounds": 1,
      "final_result": { "...": "同上方单页 JSON 格式" }
    },
    {
      "slide_number": 2,
      "rounds": 2,
      "final_result": { "...": "第 2 轮批判结果" }
    }
  ]
}
```

---

## 收敛性保证

### 问题：视觉模型评分波动

同一张幻灯片多次送审，视觉模型可能给出不同分数（±1-2 分波动），导致：
- 第 1 轮判不通过，修复后第 2 轮分数反而更低（修复引入新问题）
- 临界分数（6-7 分）在通过/不通过之间反复横跳

### 收敛策略

#### 1. 温度控制
- 视觉模型调用时设置 `temperature=0`（或最低可用值），减少随机性
- 若 API 不支持温度参数，对同一图片发送 2 次取平均分

#### 2. 临界分数缓冲区
- 6.5-7.0 分视为"临界通过"：标记为 `passed = true` 但附加 `marginal = true`
- 临界通过的页面不进入修复流程（避免越修越差）
- 仅在 `score < 6.5` 时触发修复

#### 3. 修复收敛检测
- 第 2 轮评分若低于第 1 轮，**不采纳第 2 轮修复**，回退到第 1 轮版本
- 在 `critique_log.json` 中记录每轮分数，检测是否单调递增
- 若连续 2 轮同一维度分数未提升，标记该维度为 `converged = false`，停止修复

#### 4. 维度独立收敛
- 4 个维度独立判断收敛，不因 1 个维度未通过而重修全部
- 已通过维度（score ≥ 7）的修复建议标记为 `priority: low`，不执行
- 仅修复未通过维度对应的元素

#### 5. 确定性锚点
- Stage 1 结构化检测结果是确定性的（同输入同输出），作为锚点
- Stage 2 视觉评分与 Stage 1 检测结果交叉验证：
  - 若 Stage 1 检测到 `ai_purple_palette`，Stage 2 的 `color_discipline` 必须 ≤ 3 分
  - 若 Stage 1 检测到 `wall_of_text`，Stage 2 的 `content_completeness` 必须 ≤ 5 分
  - 若视觉评分与结构化检测矛盾（如 Stage 1 有硬性违规但视觉评分 ≥ 7），以结构化检测为准

### 收敛判定流程

```
第 1 轮视觉批判
  │
  ├─ 全部 ≥ 7 → 通过 ✅
  │
  └─ 有维度 < 6.5
       │
       ├─ 修复该维度对应元素
       │
       └─ 第 2 轮视觉批判
            │
            ├─ 该维度分数提升 → 采纳修复 ✅
            │
            ├─ 该维度分数持平或下降 → 回退修复，标记 converged=false ❌
            │
            └─ 其他维度分数下降 → 仅回退导致下降的修复
```

### critique_log.json 格式

```json
{
  "file": "input.pptx",
  "slides": [
    {
      "slide_number": 1,
      "rounds": [
        {
          "round": 1,
          "dimensions": {
            "visual_hierarchy": {"score": 8, "passed": true},
            "typographic_aesthetic": {"score": 6, "passed": false},
            "color_discipline": {"score": 7, "passed": true},
            "content_completeness": {"score": 9, "passed": true}
          },
          "overall_passed": false,
          "fixes_applied": []
        },
        {
          "round": 2,
          "dimensions": {
            "visual_hierarchy": {"score": 8, "passed": true},
            "typographic_aesthetic": {"score": 7, "passed": true},
            "color_discipline": {"score": 7, "passed": true},
            "content_completeness": {"score": 9, "passed": true}
          },
          "overall_passed": true,
          "fixes_applied": [
            {"dimension": "typographic_aesthetic", "action": "标题字体 Arial → Clash Display", "result": "improved"}
          ],
          "converged": true
        }
      ]
    }
  ]
}
```

---

## 注意事项

- 此 Prompt 专注于 **4 个视觉维度**，不是 `aesthetic-scoring-rubric.md` 中的 8 个维度
- 及格线为 **7 分**（更严格），而非 rubric 中的 7.0 = B 级
- 不做加权计算，4 个维度同等重要，任一不通过则整页不通过
- `fix_suggestions` 只在 `overall_passed = false` 时非空
- 品牌模板装饰元素享受豁免规则，不计入扣分
- 临界分数（6.5-7.0）标记 `marginal = true` 但不触发修复，避免越修越差