---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '458ae912-a411-4af8-be77-622aabdf2ff7'
  PropagateID: '458ae912-a411-4af8-be77-622aabdf2ff7'
  ReservedCode1: '206dc896-0c32-4091-98c4-ca301b4152c4'
  ReservedCode2: '206dc896-0c32-4091-98c4-ca301b4152c4'
---

# PPT 制作执行参考文档

> 阶段：Phase 3 — 拿到台本蓝图后
> 目标：按计划逐步构建 PPTX，先图后文，每段快速质检

## 1. 输入

来自 Phase 2（ppt-planning）的台本蓝图：
- 风格/配色/字体定义
- 逐页蓝图（布局 + 文字 + 配图）

## 2. 制作顺序：先图后文

```
Step 1: 生成所有配图（PIL/ImageGen/diagram）
Step 2: 裁剪配图（去除白边，控制宽高比）
Step 3: 构建 PPTX（布局 + 嵌入配图 + 填入文字）
Step 4: 配图覆盖率门禁检查
Step 5: fix_ppt.py 统一修复
Step 6: 评分验证
Step 7: 交付 + 清理
```

## 3. Step 1-2：配图生成与裁剪

### 3.1 PIL 生成结构化示意图

适用于：流程图、时间线、对比图、架构图、决策卡片

```bash
python generate_illustrations.py  # 生成 PIL 配图
python gen_illustrations.py <dir> --config config.json --output-dir cropped/ --max-aspect-ratio 3.5
```

### 3.2 ImageGen 生成概念图

适用于：无法用几何图形表达的概念性内容

- 由 Agent 调用 ImageGen 工具生成
- 生成后用 gen_illustrations.py 裁剪白边
- ImageGen 不可用时，PIL 示意图作为备选

### 3.3 裁剪规则

- 去除图片周围的白边
- 宽高比上限 3.5:1（超出则纵向填充白边）
- 目标分辨率 ≥ 800×600

## 4. Step 3：构建 PPTX

### 4.1 模板选择

使用 `assets/PPT模板.pptx` 中的 Layout：
- Layout 0：封面
- Layout 1：仅标题（含分割线装饰）
- Layout 2：标题+文本（含分割线装饰）
- Layout 3：尾页

### 4.2 布局关键参数

```
标题区：y=0.15, h=0.65, bottom=0.80 < 分割线 y=0.88
正文区：y=1.10+（分割线以下）
右侧配图：left≈6.5-7.0, width≈5.5-5.8
全幅配图：left≈6.5, width≈6.2
```

### 4.3 文字排版规范

- 标题：22pt，电信红 #E60012，加粗
- 正文：14pt，深灰 #282828
- 使用卡片容器（add_table）而非空方块（add_bg + add_rich_textbox）
- 清理模板空占位符（clean_empty_placeholders）

### 4.4 等宽字体规则

当页面包含代码路径、函数名、文件目录时：
- 等宽内容使用 Consolas 或 Courier New
- 行内代码片段前后加空格与正文区分

## 5. Step 4：配图覆盖率门禁

```bash
python gate_image_coverage.py <input.pptx> --threshold 0.3 --verbose
```

- < 30%：FAIL（红色），需增加配图
- 30%-50%：FAIR（黄色），建议增加
- ≥ 50%：GOOD（绿色）

## 6. Step 5：fix_ppt.py 修复

```bash
# 基础修复（不含 type-scale 和 spacing-grid）
python fix_ppt.py <input.pptx> -o <output.pptx> \
    --all --fonts --pairing microsoft-yahei+arial \
    --margins --margin-in 0.5 --images --bullets

# 含 web-design 法则的完整修复
python fix_ppt.py <input.pptx> -o <output.pptx> \
    --all --type-scale --ratio 1.25 --spacing-grid \
    --fonts --pairing microsoft-yahei+arial \
    --margins --margin-in 0.5 --images --bullets
```

**注意**：`--all` 不包含 `--type-scale` 和 `--spacing-grid`，需显式指定。

**电信风格重要**：不要使用 `--colors` 或 `--palette`，默认 corp-blue 会与电信红冲突。

## 7. Step 6：评分验证

```bash
python score_ppt_pages.py <input.pptx> --scenario telecom --output score.json
```

评分维度（9 维度，权重按场景不同）：

| 维度 | 电信权重 | 说明 |
|------|----------|------|
| whitespace | 9% | 留白 |
| type_scale | 13% | 字号阶梯 |
| color_harmony | 18% | 配色和谐 |
| alignment | 13% | 对齐 |
| spacing | 9% | 间距 |
| imagery | 5% | 图像 |
| consistency | 13% | 一致性 |
| hierarchy | 10% | 层次 |
| layout | 10% | 布局 |

## 8. Step 7：交付与清理

- 输出最终 PPTX 到用户指定路径
- 清理 `.temp/` 中的中间文件
- 报告最终评分和反模式清单

## 9. 电信风格特殊规范

### 9.1 颜色使用

- 电信红 #E60012：仅限标题、左侧垂直条、底部线、徽章、卡片装饰线
- 禁止大面积红色填充、红色边框、浅红色背景

### 9.2 模板装饰元素

Layout 1/2 的分割线装饰图片位于 y=0.88, h=0.07：
- 标题 bottom < 0.88 不压线
- 正文 top > 1.10 在分割线下方
- fix_ppt.py 已有 `_detect_layout_exclusion_zones()` 感知装饰

### 9.3 内容密度

- 每页文字块不超过 5 个
- 内容填充率 60%-70%
- 使用 add_table() 创建卡片，避免空方块