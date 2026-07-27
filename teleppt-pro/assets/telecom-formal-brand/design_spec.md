---
brand_id: telecom-formal
kind: brand
summary: "China Telecom formal reporting identity — internal work reports, government briefings, SOE standard presentations. Primary blue #0077BE, Microsoft YaHei typography, stroke icons, restrained professional tone."
primary_color: "#0077BE"
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'c79919a4-40a5-41c4-8744-81e4b02a1913'
  PropagateID: 'c79919a4-40a5-41c4-8744-81e4b02a1913'
  ReservedCode1: '989dbfad-610c-43e3-92ea-73b87e745d11'
  ReservedCode2: '989dbfad-610c-43e3-92ea-73b87e745d11'
---

# China Telecom Formal Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints. Internal layouts should be rich and varied; only the visual identity (colors, fonts, logo, tone) is locked.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | China Telecom (中国电信) |
| Use Cases | 内部工作报告、领导汇报、政企方案、科创汇报、项目评审、年中/年度总结 |
| Tone | 正式、严谨、克制、结论先行、数据支撑 |

## II. Color Scheme

| Role | HEX | Provenance | Notes |
|---|---|---|---|
| primary | `#0077BE` | fact | 电信主蓝 — 标题栏、章节号背景、重点色块 |
| primary-light | `#3399D6` | fact | 浅蓝渐变 — 装饰线条、辅助色块、渐变叠加 |
| neutral-dark | `#333333` | fact | 深灰 — 正文文字、图表基色 |
| bg | `#F5F7FA` | fact | 浅灰底色 — 页面背景 |
| bg-white | `#FFFFFF` | fact | 纯白 — 卡片背景、文字反白底 |
| accent-red | `#C00000` | convention | 正红点缀 — 仅用于党建/红头文件场景的标题栏、角标、分隔线；正式汇报中克制使用 |
| accent-tech | `#C0C8D0` | convention | 科技银 — 科技/数字化场景的线条/光效点缀 |
| surface | `#FFFFFF` | convention | 白色 — 卡片、内容面板背景 |
| border | `#E2E8F0` | convention | 浅灰边框 — 卡片边框、分割线 |
| muted-text | `#64748B` | convention | 石板灰 — 次要文字、图表标签 |

**配色原则**：
- 全册最多3种主色（蓝/灰/白），不混用
- 电信蓝 #0077BE 仅用于标题栏、重点标记、章节号；不铺大面积蓝底正文
- 内容页以浅底深字为主（白底/浅灰底 + 深灰字）
- accent-red (C00000) 仅限党建场景点缀，正式汇报中不使用大面积红色
- 页面背景优先 #F5F7FA 浅灰，重要页面可用 #FFFFFF 纯白

## III. Typography

| Role | Family | Weight |
|---|---|---|
| title | `"Microsoft YaHei", "微软雅黑", "Helvetica Neue", Arial, sans-serif` | 600–700 |
| body | `"Microsoft YaHei", "微软雅黑", "Helvetica Neue", Arial, sans-serif` | 400 |
| english-title | `"Times New Roman", Georgia, serif` | 700 |
| english-body | `"Times New Roman", Georgia, serif` | 400 |

> 微软雅黑是中国电信央企PPT的标准字体，所有展示设备和办公电脑预装。标题加粗(Bold 600-700)，正文常规(Regular 400)。英文/数字场景使用 Times New Roman 做强调。无需嵌入字体。

**字号规范（PPT场景换算）**：

| 用途 | 字号范围 |
|---|---|
| 封面大标题 | 28–36pt |
| 页面标题 | 22–26pt |
| 一级正文 | 14–16pt |
| 二级/标注 | 10–12pt |
| 目录英文 | 22–44pt |
| 章节号 | 20pt Bold |

严禁：艺术字体、花体、手写体。

## IV. Logo

中国电信在每页页脚显示LOGO + 页码 + 单位/部门。

| 文件 | 形式 | 用途 |
|---|---|---|
| 电信LOGO | 天翼标识 + "中国电信"文字 | 页脚左侧，高度约20px |

- 封面：LOGO居中或右下角，尺寸可适当放大
- 每页：页脚左侧LOGO + 中间单位名 + 右侧页码
- LOGO底色与页面背景一致，不做反色处理
- 安全间距：LOGO周围至少0.5×高度留白

> 注意：实际LOGO文件需从电信品牌素材库获取。生成时可用占位矩形+文字标注"中国电信LOGO"替代。

## V. Voice & Tone

- Formality: 正式-专业
- Person: 我们 (Chinese)，避免第二人称
- Emoji: 严禁
- Abbreviations: 首次出现全称，括号注明缩写（如"人工智能(AI)"、"政企客户(DICT)"
- Data: 优先展示具体数字和指标，避免模糊表述
- Structure: 结论先行 → 论据支撑 → 行动建议
- Jargon: 使用电信内部术语（研发、政企、自研、产数、AI+、云中台等），不做外来词替换

## VI. Icon Style

- Preference: stroke（线性/描边图标）
- 图标风格：扁平化、简约商务
- 主题匹配：通信、网络、基站、云、算力、大数据、AI、5G
- 推荐库：tabler / lucide（stroke风格，与电信正式调性一致）

严禁：卡通图标、3D图标、emoji图标、手绘风格图标。

## VII. Page Furniture (页饰)

每页必须包含的电信标准页饰元素（作为品牌约束，在 ppt-master 的 design_spec 中锁定义）：

| 元素 | 位置 | 样式 |
|---|---|---|
| 标题栏 | 页面顶部 | 电信蓝(#0077BE)色带，高度约48px，左侧白色标题文字 |
| 页脚栏 | 页面底部 | 浅灰(#F5F7FA)底色，高度约32px，左侧LOGO，中间单位名，右侧页码 |
| 装饰线 | 标题栏下 | 浅蓝(#3399D6)细分隔线，1-2px |
| 角装饰 | 右下角 | 可选，浅灰色几何线条点缀 |

**封面页例外**：封面不使用标准标题栏和页脚栏，使用全幅电信蓝渐变背景 + 居中标题 + LOGO。

**章节标题页**：可使用电信蓝渐变全幅背景 + 大号章节号 + 章节名，但必须与封面视觉呼应。

这些页饰元素通过 ppt-master 的 spec_lock.md 在每页生成时强制引用，确保视觉一致性。

> AI生成