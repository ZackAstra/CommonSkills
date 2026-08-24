---
name: img2editable-pptx
description: 依据参考图（截图/照片/设计稿）1:1 复刻生成 SVG，并无损转换为"全原生形状、可编辑"的 PPTX。适用于架构图、流程图、结构图、拓扑图等各类图示的复刻与矢量化。当用户说"1:1复刻这张图为可编辑PPT"、"把截图转成PPT"、"复刻架构图/流程图"时使用。全程不依赖 LibreOffice。
---

# 参考图 → 1:1 复刻 SVG → 可编辑 PPTX

把一张参考图（架构图、流程图等）复刻为 SVG，再转换为**每个元素都可编辑**的原生形状 PPTX。

## 核心原则

- **单一事实源是 SVG**：所有布局都在 SVG 里完成，PPTX 由转换器机械生成；要改图就改 SVG，重跑转换器即可再生成。
- **不依赖 LibreOffice / Office 做生成**：生成只靠 python-pptx；本机 PowerPoint COM 只用来做渲染校验。
- **参考图中的位图内容**（界面截图、照片、复杂插画）：用 PIL 按区域裁剪为 PNG，以独立图片形状插入；若暂时拿不到原图文件，先生成带标注的占位图，后续替换重跑即可。
- **配色默认不动**，布局美化（对齐、间距、圆角统一）需先与用户确认范围。

## 环境检查（开工前）

```bash
python -c "import pptx, PIL; print('ok')"   # python-pptx + Pillow
# 校验渲染：PowerPoint COM（Windows + Office）
powershell -NoProfile -Command "try { \$p = New-Object -ComObject PowerPoint.Application; \$p.Quit(); 'COM OK' } catch { 'NO COM' }"
```

SVG 预览 PNG（可选）：playwright + chromium headless 截图，或任一可用浏览器。

## 工作流程

### 1. 分析参考图，规划坐标

- 用视觉读图，量出各面板/框/箭头/文字的像素位置，以参考图原始分辨率作为 SVG 的 `viewBox`（如 `0 0 1044 537`），坐标即像素，1:1 最省事。
- 列出全部元素清单：面板、框、文本、箭头、图标、位图区域。
- 参考图里**未正常显示/缺失的图标**，用语义合适的矢量图标补齐（如：Skill=星光、流程=节点树、工具=扳手、知识库=书本）。

### 2. 裁剪位图区域（如有）

参考图必须落盘为文件才能裁剪——**聊天里粘贴的图片不在磁盘上**，先向用户要文件。

```python
from PIL import Image
img = Image.open("ref.png")
img.crop((x1, y1, x2, y2)).save("_crops/region1.png")   # 坐标按参考图像素
```

拿不到文件时，先用 PIL 生成带"占位-待替换截图"标注的占位图，流程不中断。

### 3. 绘制 SVG

- 浅色背景图用浅色主题，深色架构图可参考 baoyu-diagram 的深色设计系统；**配色跟随参考图**。
- 图标用简单 stroke path（Feather/Lucide 风格），放在 `<g transform="translate(x,y)">` 里。
- 渐变面板：`<defs><linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">` + `fill="url(#panelGrad)"`。
- 半透明装饰箭头：直接写 `opacity`，转换器会按底色预混合。
- 文本：`text-anchor="middle"` 居中，y 为基线；多行文本用多个 `<text>`。
- 位图：`<image x y width height href="_crops/xxx.png"/>`（相对 SVG 的路径）。

### 4. 转换为可编辑 PPTX

```bash
python {baseDir}/scripts/svg2pptx_editable.py <input.svg> [output.pptx]
```

转换器把每个 SVG 元素映射为原生形状（见下"元素映射"），输出即完全可编辑。

### 5. PowerPoint COM 渲染校验，迭代到一致

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File {baseDir}/scripts/render_pptx.ps1 `
  -pptx "绝对路径\out.pptx" -png "绝对路径\check.png"
```

用视觉模型把 `check.png` 与参考图**逐区域比对**（全图 + 局部放大），发现偏差 → 改 SVG → 重跑 4~5。一般 2~3 轮收敛。重点检查：图标是否显示、文字垂直位置、箭头位置、层级遮挡。

## 元素映射（转换器已内置）

| SVG | PPTX | 关键处理 |
|---|---|---|
| `rect` | 圆角/直角矩形 | `rx`→`adjustments[0]=rx/min(w,h)`；dasharray→虚线 |
| `text` | 文本框 | y 是基线，上抬 ~1em；px→pt 按 `幻灯片宽pt/viewBox宽` |
| `polygon` | freeform | `opacity` 与底色预混合成实色 |
| `path` | freeform | 贝塞尔/圆弧采样为 12~14 段折线 |
| `circle` | 椭圆形状 | |
| `line` | 直线连接符 | |
| `image` | 图片形状 | href 相对 SVG 解析 |
| `<g transform>` | 坐标预变换 | translate/scale 组合，含属性继承 |
| `linearGradient` | 渐变填充 | 两 stop + 角度换算 |

## 踩坑清单（重要）

1. **属性继承**：`stroke/fill/font-size` 常写在父级 `<g>` 上，解析时必须沿树传递继承属性，否则图标描边丢失、形状隐形。
2. **transform 顺序**：`transform="translate(x,y) scale(s)"` 语义是**先 scale 后 translate**（矩阵左乘），按书写顺序套坐标会把元素放飞。
3. **CSS 单位**：`<style>` 里 `font-size: 26px` 带 px 后缀，解析时 strip。
4. **文本基线**：SVG 的 y 是基线，PPTX 文本框是顶边，需上抬约 1em；中文按全角宽度估算文本框宽。
5. **PPTX 无 opacity API**：半透明色提前与背景色做 alpha 混合。
6. **中文字体**：run 同时设置 `font.name` 和 `a:ea` 东亚字体为"微软雅黑"，否则中文回落默认字体。
7. **LibreOffice 不可依赖**：headless 转换在此类环境常静默失败/挂起；校验一律走 PowerPoint COM。

## 文件

- `scripts/svg2pptx_editable.py` — 通用 SVG→可编辑 PPTX 转换器（命令行传任意 SVG，自动解析 viewBox）
- `scripts/render_pptx.ps1` — PowerPoint COM 渲染 pptx 首页为 PNG 的校验脚本

## 输出约定

- SVG：`{工作目录}/diagram/{topic}.svg`
- PPTX：同名 `-editable.pptx`
- 裁剪图：`diagram/_crops/`
- 校验图：`_{topic}_check.png`（临时，可删）
