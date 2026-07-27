# 动画美学规范（Animation Aesthetics）

本文件规范 PPT 转场和元素动画的使用，遵循"克制即专业"原则。

## 核心原则

> Garr Reynolds: "If your slide needs animation to be understood, redesign the slide."

1. **80% 页零动画**：大多数页面直接切换，无需元素动画
2. **动画服务于叙事**：仅在有明确叙事目的时使用（如逐步揭示、因果演示）
3. **转场统一**：全 deck 使用同一种转场（推荐"淡出"或"推入"）
4. **时长克制**：元素动画 ≤ 0.5s，转场 ≤ 0.3s

## 转场规范

| 转场类型 | 推荐度 | 适用场景 | 时长 |
|---|---|---|---|
| 淡出（Fade） | ★★★★★ | 通用，所有场景 | 0.3s |
| 推入（Push） | ★★★★ | 章节切换，方向感 | 0.3s |
| 切割（Split） | ★★★ | 对比页，左右分屏 | 0.2s |
| 无（None） | ★★★★ | 快节奏演讲 | 0s |
| 摩天轮/旋转/百叶窗 | ✗ | 禁止 | — |
| 弹跳/飞入/缩放 | ✗ | 禁止 | — |

**铁律**：全 deck 转场类型 ≤ 2 种。

## 元素动画规范

### 允许的动画类型

| 动画 | 用途 | 时长 | 缓动 |
|---|---|---|---|
| 淡入（Appear/Fade In） | 逐步揭示要点 | 0.3-0.5s | Ease Out |
| 擦除（Wipe） | 进度条/时间线 | 0.3-0.5s | Ease Out |
| 路径动画（Motion Path） | 流程图/数据流 | 0.5s | Ease In-Out |

### 禁止的动画类型

| 动画 | 为什么禁止 |
|---|---|
| 弹跳（Bounce） | 幼稚，分散注意力 |
| 旋转（Spin/Rotate） | 无叙事目的，令人眩晕 |
| 闪烁（Blink/Flash） | 干扰阅读，可能触发光敏癫痫 |
| 字母逐个飞入 | 慢且无意义 |
| 缩放弹跳（Grow/Shrink with Bounce） | 过度装饰 |

### 动画节奏

- 逐步揭示要点时，每个要点间隔 0.2-0.3s
- 不要所有元素同时动画（信息过载）
- 不要逐字逐句动画（浪费时间）
- 同一页面动画步骤 ≤ 5 个

## 电信品牌场景

- 电信品牌 PPT 允许封面页使用 1 次品牌动画（如天翼 logo 淡入）
- 数据页面允许图表数据逐系列擦除动画
- 其他页面零动画

## 与 template_fill_pptx 的关系

`template_fill_pptx/transitions.py` 支持在 JSON plan 中指定转场：

```json
{
  "slides": [
    {
      "transition": {"type": "fade", "duration": "300ms"},
      "animations": [
        {"shape": "bullet_1", "type": "appear", "delay": "0ms"},
        {"shape": "bullet_2", "type": "appear", "delay": "300ms"}
      ]
    }
  ]
}
```

## 反模式检测

| 反模式 | 检测方式 | 扣分维度 |
|---|---|---|
| 弹跳/旋转动画 | XML 中 `<p:anim>` 的 `presetClass` | professional_polish -2 |
| 转场类型 > 2 种 | deck 级统计 `<p:transition>` | visual_consistency -2 |
| 单页动画步骤 > 5 | 统计 `<p:anim>` 数量 | content_density -1 |
| 转场时长 > 1s | `<p:transition>` 的 `advTm` | professional_polish -1 |
