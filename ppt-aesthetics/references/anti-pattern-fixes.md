---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '257499fd-876e-429f-a9de-7b49cd34ec6f'
  PropagateID: '257499fd-876e-429f-a9de-7b49cd34ec6f'
  ReservedCode1: 'b752edec-4875-4e0f-b35e-85c160e183f9'
  ReservedCode2: 'b752edec-4875-4e0f-b35e-85c160e183f9'
---

# 反模式检测与修复手册

本文件汇总 PPT 美观评分中检测的所有反模式（anti-patterns），按 8 维度分类，统一编号。结构化评分脚本 `scripts/score_ppt_pages.py` 和 `scripts/critique_engine.py` 会自动检测带 ✅ 标记的反模式。

> **编号规则**：AP-{维度缩写}-{序号}，维度缩写：WS=whitespace, TS=type_scale, CH=color_harmony, AL=alignment, SP=spacing, IM=imagery, CO=consistency, HI=hierarchy

---

## 一、whitespace 留白维度

### AP-WS-01 ✅ `text_heavy_deck` 整页文字过重
- **现象**：整页文字面积占比 > 60%
- **为什么是问题**：PPT 不是 Word，文字过重导致视觉窒息，观众拒绝阅读
- **检测**：评分脚本计算文字面积占页面比例 > 60%
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --bullets
  ```
  拆分长段落为要点，增加配图或留白区域
- **去重**：与 `low_fill_rate` 不双重扣分——同一页只扣更严重的那一项

### AP-WS-02 ✅ `wall_of_text` 文字墙
- **现象**：单页 > 60 词或 > 400 字符
- **为什么是问题**：信息过载，观众不会读段落
- **检测**：评分脚本统计 `total_words > 60`（英文按空格分词）或 CJK 字符 > 400
- **严重性**：hard（-2.0/维度）
- **维度**：whitespace
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --bullets
  ```
  按句号/分号/感叹号切分长段落，每段加项目符号前缀
- **去重**：与 `text_heavy_deck` 可叠加（不同维度：局部 vs 全局）

### AP-WS-03 ✅ `high_text_density` 文本密度过高
- **现象**：单页文本字符数 > 400（作为 wall_of_text 的回退条件）
- **为什么是问题**：CJK 文本词数少但字符密度高，需要独立阈值
- **检测**：当 `total_words <= 60` 但 `total_text > 400` 字符时触发（elif 逻辑）
- **严重性**：soft（-0.5/维度）
- **维度**：whitespace
- **与 wall_of_text 的关系**：互斥检测——先检查词数 > 60（wall_of_text），不满足再检查字符 > 400（high_text_density）。两者不会同时触发
- **修复**：参考 `wall_of_text` 修复方法，精简文字或拆分到多页

### AP-WS-04 ✅ `low_fill_rate` 有效内容填充率过低
- **现象**：页面有效内容填充率 < 60%，大面积空白
- **为什么是问题**：内容稀疏显得空洞、不专业
- **检测**：评分脚本计算有效内容面积占页面比例 < 60%
- **修复**：
  1. 增加有效内容（补充要点、配图、数据）
  2. 缩小文字框/卡片尺寸，增加视觉密度
  3. 使用 `--spacing-grid` 收紧间距：
     ```bash
     python scripts/fix_ppt.py input.pptx --output out.pptx --spacing-grid --grid-in 0.08
     ```
- **去重**：与 `text_heavy_deck` 不双重扣分

---

## 二、type_scale 字号阶梯维度

### AP-TS-01 ✅ `too_many_fonts` 字体家族过多
- **现象**：一份 PPT 出现 4+ 种字体家族
- **为什么是问题**：每增加一种字体，观众认知负荷增加约 15%
- **检测**：评分脚本统计 deck 级字体家族数 > 4
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing source-han-sans+inter
  ```

### AP-TS-02 ✅ `unprofessional_font` 不专业字体
- **现象**：使用 Comic Sans / Papyrus / Lobster / Impact / 华文彩云 等装饰字体
- **为什么是问题**：装饰字体可读性差，且会被潜意识判定为"业余"
- **检测**：评分脚本内置 `BAD_FONTS` 列表
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing microsoft-yahei+arial
  ```

### AP-TS-03 ✅ `cjk_text_no_cjk_font` 中文文本无中文字体
- **现象**：PPT 里有中文文字，但 run 没有显式设置 CJK 字体
- **为什么是问题**：拉丁字体无中文字形，会回退到系统默认（Windows 宋体）
- **检测**：评分脚本检查 `_is_cjk_text(text) and not _is_cjk_font(font_name)`
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing microsoft-yahei+arial
  ```

### AP-TS-04 ✅ `weak_type_scale` 字号阶梯过弱
- **现象**：标题与正文字号比 < 1.2（Minor Second）
- **为什么是问题**：缺乏视觉层次，标题与正文难以区分
- **检测**：评分脚本计算标题/正文字号比 < 1.2
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --type-scale --ratio 1.25
  ```

### AP-TS-05 ✅ `extreme_type_scale` 字号阶梯过极端
- **现象**：标题与正文字号比 > 3（可能封面元素误入内容页）
- **为什么是问题**：极端比例导致正文过小或标题过大
- **检测**：评分脚本计算标题/正文字号比 > 3
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --type-scale
  ```

---

## 三、color_harmony 色彩和谐维度

### AP-CH-01 ✅ `too_many_colors` 颜色过多
- **现象**：单页或全 deck 使用 6+ 种非中性色
- **为什么是问题**：违反 60-30-10 法则；视觉混乱，无焦点
- **检测**：评分脚本统计非中性色数 > 5
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors --palette forest-exec
  ```

### AP-CH-02 ✅ `ai_purple_palette` AI 紫蓝渐变
- **现象**：背景或按钮使用 #6366F1 / #818CF8 / #A855F7 / #C084FC 等 indigo/violet 色
- **为什么是问题**：AI 工具默认输出的"AI 味"配色，一眼可辨
- **检测**：评分脚本 `_is_ai_purple()` 函数检查 RGB 范围
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors --palette corp-blue
  ```

### AP-CH-03 ✅ `oversaturated_pure_rgb` 纯 RGB 饱和色
- **现象**：使用 #FF0000 / #00FF00 / #0000FF / #FFFF00 等纯色
- **为什么是问题**：饱和度过高，刺眼
- **检测**：评分脚本 `OVERSATURATED_DEFAULTS` 集合
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors --palette mono-clean
  ```

### AP-CH-04 ✅ `overuse_accent` 强调色过度使用
- **现象**：强调色占比 > 40%，违反 60-30-10 法则
- **为什么是问题**：强调色过多等于没有强调
- **检测**：评分脚本计算强调色面积占比 > 40%
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors
  ```

### AP-CH-05 ✅ `pure_black_text` 纯黑文字
- **现象**：文字颜色为 #000000
- **为什么是问题**：纯黑在白底上对比过强，阅读疲劳
- **检测**：评分脚本检查文字颜色 == #000000
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors
  ```
  替换为 800-950 色阶（如 #1A1A1A）

### AP-CH-06 ✅ `pure_white_card` 纯白卡片
- **现象**：卡片填充为 #FFFFFF
- **为什么是问题**：纯白卡片在浅色背景上无层次感
- **检测**：评分脚本检查卡片填充 == #FFFFFF
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors
  ```
  替换为 50-100 色阶（如 #F5F5F5）

### AP-CH-07 ✅ `rainbow_text` 彩虹文字
- **现象**：单页使用 4+ 种不同颜色的文字
- **为什么是问题**：视觉混乱，缺乏色彩纪律
- **检测**：评分脚本统计文字颜色种类 > 3
- **修复**：将单页文字颜色控制在 3 种以内，遵循 60-30-10 法则

### AP-CH-08 ✅ `inconsistent_colors` 跨页配色不一致
- **现象**：不同页面使用不同的配色方案
- **为什么是问题**：破坏整体视觉一致性
- **检测**：评分脚本比较跨页主色差异
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --colors --palette corp-blue
  ```

---

## 四、alignment 对齐维度

### AP-AL-01 ✅ `no_margins` 无页边距
- **现象**：形状/文字距幻灯片边缘 < 0.3in
- **为什么是问题**：内容贴边显得拥挤、廉价；投影时可能被裁切
- **检测**：评分脚本检查每个 shape 的 bbox 与边缘距离 < 0.3in
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --margins --margin-in 0.5
  ```

### AP-AL-02 ✅ `three_equal_cards` 三等卡片
- **现象**：3 个等大的圆角矩形横向排列
- **为什么是问题**：无视觉层级，观众不知道先看哪个
- **检测**：评分脚本检查 3 个 `ROUNDED_RECTANGLE` 同 top、同 width、同 height
- **修复**（机械修复有限，建议人工）：
  - 让 1 个卡片更大或更突出，另外 2 个缩小并淡化
  - 改为 2 大 + 1 小的不对称布局

### AP-AL-03 ✅ `misaligned_elements` 元素未对齐
- **现象**：两个元素差 1-2px 没对齐
- **为什么是问题**：微小错位在投影放大后非常明显，显得不专业
- **检测**：评分脚本检查同组元素坐标差 > 2px
- **修复**：用 PowerPoint "对齐 → 左对齐 / 顶对齐" 功能，或：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --spacing-grid
  ```

---

## 五、spacing 间距维度

### AP-SP-01 ✅ `irregular_spacing` 间距不规则
- **现象**：垂直间距非 4/8px 网格倍数
- **为什么是问题**：间距不规律破坏视觉节奏
- **检测**：评分脚本检查间距 % 0.08in != 0
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --spacing-grid --grid-in 0.08
  ```

### AP-SP-02 ✅ `inconsistent_spacing` 跨页间距不一致
- **现象**：不同页面同类元素间距不同
- **为什么是问题**：破坏整体节奏一致性
- **检测**：评分脚本比较跨页同类间距差异
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --spacing-grid
  ```

### AP-SP-03 ✅ `orphan_widow` 孤行/寡行
- **现象**：段落末尾仅 1-2 个字独占一行
- **为什么是问题**：浪费空间，视觉不美观
- **检测**：评分脚本检查文本框最后一行字符数 < 5
- **修复**：调整行距或文字框宽度避免孤行/寡行

---

## 六、imagery 图像维度

### AP-IM-01 ✅ `low_res_image` 低分辨率图片
- **现象**：图片分辨率 < 800×600
- **为什么是问题**：投影放大后马赛克明显
- **检测**：评分脚本检查图片原始尺寸 < 800×600
- **修复**：替换为分辨率 >= 800x600 的高清图片（标注警告，需人工换图）

### AP-IM-02 ✅ `stretched_image` / `stretched_images` 拉伸图片
- **现象**：图片容器宽高比与图片原始宽高比偏差 > 8%
- **为什么是问题**：人物/Logo/产品图拉伸变形是"业余"最显眼的标志
- **检测**：评分脚本比较 `box_aspect / img_aspect` 比值
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --images
  ```

### AP-IM-03 ✅ `clipart_style` 剪贴画风格
- **现象**：使用低质量剪贴画或卡通图标
- **为什么是问题**：剪贴画风格过时，降低专业感
- **检测**：视觉模型检测（结构化脚本辅助标注）
- **修复**：替换为高质量矢量图标或专业配图

---

## 七、consistency 一致性维度

### AP-CO-01 ✅ `inconsistent_fonts` 跨页字体不一致
- **现象**：不同页面使用不同的字体方案
- **为什么是问题**：破坏整体视觉一致性
- **检测**：评分脚本比较跨页字体差异
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --fonts --pairing source-han-sans+inter
  ```

### AP-CO-02 ✅ `default_template` 默认模板
- **现象**：明显使用 Office 内置模板（如 Wisp / Median / Newsroom）
- **为什么是问题**：默认 = 没用心；观众一眼识别
- **检测**：评分脚本检查模板名称在默认列表中
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --all
  ```

---

## 八、hierarchy 视觉层次维度

### AP-HI-01 ✅ `tiny_text` 文字过小
- **现象**：正文字号 < 12pt
- **为什么是问题**：投影后无法阅读
- **检测**：评分脚本检查字号 < 12pt
- **修复**：将正文字号提升至 12pt 以上

### AP-HI-02 ✅ `no_visual_hierarchy` 无视觉层次
- **现象**：标题、正文、注释使用相同字号/颜色/粗细
- **为什么是问题**：观众无法快速识别信息层级
- **检测**：评分脚本检查标题/正文字号比 < 1.2 且颜色相同
- **修复**：建立标题-正文-注释三级视觉层次

### AP-HI-03 ✅ `long_bullet` 过长要点
- **现象**：单条要点 > 35 字（中文）或 > 12 词（英文）
- **为什么是问题**：要点变段落，失去"要点"意义
- **检测**：评分脚本检查单条要点长度
- **修复**：
  ```bash
  python scripts/fix_ppt.py input.pptx --output out.pptx --bullets
  ```
  CJK 感知拆分

### AP-HI-04 ✅ `too_many_bullets` 要点过多
- **现象**：单页要点 > 6 条
- **为什么是问题**：观众在第 4 条就注意力耗尽
- **检测**：评分脚本统计要点数 > 6
- **修复**：将要点控制在 6 条以内，理想为 3-4 条（标注，不自动删，需人工拆页）

### AP-HI-05 ✅ `bullet_soup` 要点汤
- **现象**：大量无层次、无分组的要点堆叠
- **为什么是问题**：信息无结构，难以理解
- **检测**：评分脚本检查要点数 > 4 且无分组/缩进
- **修复**：将要点分组或使用视觉化布局替代纯列表

### AP-HI-06 ✅ `low_contrast` 低对比度
- **现象**：文字与背景对比度不足
- **为什么是问题**：投影环境下无法阅读
- **检测**：评分脚本计算对比度 < WCAG AA 标准
- **修复**：提高文字与背景的对比度

### AP-HI-07 ✅ `chart_without_message` 图表无结论
- **现象**：图表下方没有结论句
- **为什么是问题**：观众不会自己解读图表
- **检测**：评分脚本检查图表附近无结论性文字
- **修复**：图表下方加一句 14-16pt 强调色结论
- **参见**：[references/chart-aesthetics.md](chart-aesthetics.md) 第 9 节

### AP-HI-08 ✅ `code_without_monospace` 代码无等宽字体
- **现象**：代码片段、文件路径、函数名使用普通正文字体而非等宽字体
- **为什么是问题**：代码辨识度极低，与正文混淆；专业感不足
- **检测**：评分脚本检测文本中的代码模式（文件扩展名、函数调用、路径、CLI 标志）并检查是否使用等宽字体
- **修复**：将代码/路径/函数名文本框字体改为 Consolas / Courier New / Source Code Pro
- **设计规范**：参见 SKILL.md DS-4 代码字体规范

### AP-HI-09 ✅ `key_data_not_emphasized` 关键数据未强调
- **现象**：百分比、大数字、时间值等关键数据使用与正文相同的字号
- **为什么是问题**：核心数据被埋没在段落中，观众无法快速抓取关键信息
- **检测**：评分脚本检测文本中的数字/百分比模式，检查是否存在 ≥1.5 倍正文字号的 run
- **修复**：将关键数据放大至 1.5-2 倍正文字号，同时加粗 + 强调色
- **设计规范**：参见 SKILL.md DS-3 字号阶梯与关键数据强调规范

---

## 九、layout 布局维度（新增）

### AP-LA-01 ✅ `top_text_bottom_image` 固定上文下图
- **现象**：所有文字在上半区、所有图片在下半区
- **为什么是问题**：图文割裂，无法同步对照阅读；阅读动线断裂；图片仅装饰无信息承载
- **检测**：评分脚本比较文字形状重心 y 坐标与图片重心 y 坐标
- **修复**：改为左文右图分栏布局，或使用卡片网格混排图文
- **设计规范**：参见 SKILL.md DS-1 布局网格规范

### AP-LA-02 ✅ `no_card_containers` 内容无卡片容器
- **现象**：>3 个文本块的内容页没有圆角矩形卡片包裹
- **为什么是问题**：文字直接平铺在背景上，信息块边界模糊，无法快速抓取核心重点
- **检测**：评分脚本检查内容页的圆角矩形数量
- **修复**：为每组相关信息添加半透明底色卡片（圆角矩形），划分信息层级
- **设计规范**：参见 SKILL.md DS-1 布局网格规范

### AP-LA-03 ✅ `image_at_edge` 图片紧贴边缘
- **现象**：图片距幻灯片边缘 < 3%
- **为什么是问题**：投屏时极易被裁切
- **检测**：评分脚本检查图片 bbox 与边缘距离
- **修复**：调整图片位置，确保四周至少 3% 安全边距

---

## 十、deck 跨页维度（新增）

### AP-DE-01 ✅ `repeated_chapter_labels` 跨页重复章节标注
- **现象**：同一段短文本（如"01 智能体三阶段演进"）出现在 3+ 页上
- **为什么是问题**：无效视觉噪音，持续占用版面、分散注意力
- **检测**：评分脚本统计跨页短文本出现次数
- **修复**：删除每页重复的章节文字，用底部进度条或页眉导航替代
- **设计规范**：参见 SKILL.md DS-5 品牌元素规范

### AP-DE-02 ✅ `inconsistent_alignment` 跨页对齐不一致
- **现象**：不同页面的左边缘坐标差异 > 0.5 英寸
- **为什么是问题**：没有统一网格，视觉杂乱，缺乏成套规范
- **检测**：评分脚本比较跨页左边缘最小值
- **修复**：统一所有内容页的页边距和内容起始位置

### AP-DE-03 ✅ `no_brand_consistency` 缺少品牌一致性
- **现象**：< 50% 的页面有顶部品牌栏元素
- **为什么是问题**：缺少政企品牌标识，商务正式感不足
- **检测**：评分脚本检查跨页顶部 shape 存在性
- **修复**：在所有内容页添加统一的顶部品牌栏（LOGO + 标题栏）
- **设计规范**：参见 SKILL.md DS-5 品牌元素规范

---

## 暗色主题特殊规则

> 以下反模式在暗色主题 PPT 中有特殊处理，避免误报。

| 反模式 | 浅色主题阈值 | 暗色主题阈值 | 原因 |
|--------|-------------|-------------|------|
| `too_many_colors` | >5 非中性色 | >8 非中性色 | 暗色主题需要更多色阶区分层次 |
| `low_contrast` | 假设白色背景 | 检测实际背景色 | 暗色主题文字为浅色，不能假设白底 |
| `no_margins` | 8% 安全边距 | 3% 安全边距 | 暗色卡片布局中卡片接近全宽是正常设计 |
| `pure_white_card` | 标记为反模式 | 豁免 | 暗色主题中浅色卡片是必要的设计元素 |

**暗色主题检测方式**：评分脚本通过 `_detect_slide_bg_color()` 提取幻灯片背景色，计算 WCAG 亮度值 < 0.2 则判定为暗色主题。

---

## 检测能力汇总

| 编号 | 反模式 ID | 维度 | 自动检测 | 机械修复 | 需人工 |
|------|-----------|------|----------|----------|--------|
| AP-WS-01 | text_heavy_deck | whitespace | ✅ | ✅ fix_ppt.py --bullets | |
| AP-WS-02 | wall_of_text | whitespace | ✅ | ✅ fix_ppt.py --bullets | |
| AP-WS-03 | high_text_density | whitespace | ✅ | ✅ fix_ppt.py --bullets | |
| AP-WS-04 | low_fill_rate | whitespace | ✅ | ✅ fix_ppt.py --spacing-grid | |
| AP-TS-01 | too_many_fonts | type_scale | ✅ | ✅ fix_ppt.py --fonts | |
| AP-TS-02 | unprofessional_font | type_scale | ✅ | ✅ fix_ppt.py --fonts | |
| AP-TS-03 | cjk_text_no_cjk_font | type_scale | ✅ | ✅ fix_ppt.py --fonts | |
| AP-TS-04 | weak_type_scale | type_scale | ✅ | ✅ fix_ppt.py --type-scale | |
| AP-TS-05 | extreme_type_scale | type_scale | ✅ | ✅ fix_ppt.py --type-scale | |
| AP-CH-01 | too_many_colors | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-CH-02 | ai_purple_palette | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-CH-03 | oversaturated_pure_rgb | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-CH-04 | overuse_accent | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-CH-05 | pure_black_text | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-CH-06 | pure_white_card | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-CH-07 | rainbow_text | color_harmony | ✅ | 部分（需人工选色）| |
| AP-CH-08 | inconsistent_colors | color_harmony | ✅ | ✅ fix_ppt.py --colors | |
| AP-AL-01 | no_margins | alignment | ✅ | ✅ fix_ppt.py --margins | |
| AP-AL-02 | three_equal_cards | alignment | ✅ | ❌ | ✅ 改布局 |
| AP-AL-03 | misaligned_elements | alignment | ✅ | ✅ fix_ppt.py --spacing-grid | |
| AP-SP-01 | irregular_spacing | spacing | ✅ | ✅ fix_ppt.py --spacing-grid | |
| AP-SP-02 | inconsistent_spacing | spacing | ✅ | ✅ fix_ppt.py --spacing-grid | |
| AP-SP-03 | orphan_widow | spacing | ✅ | 部分（调整行距/框宽）| |
| AP-IM-01 | low_res_image | imagery | ✅ | （标注警告）| ✅ 换图 |
| AP-IM-02 | stretched_image | imagery | ✅ | ✅ fix_ppt.py --images | |
| AP-IM-03 | clipart_style | imagery | ✅ | （标注）| ✅ 换图 |
| AP-CO-01 | inconsistent_fonts | consistency | ✅ | ✅ fix_ppt.py --fonts | |
| AP-CO-02 | default_template | consistency | ✅ | 部分 fix_ppt.py --all | |
| AP-HI-01 | tiny_text | hierarchy | ✅ | ✅ fix_ppt.py --type-scale | |
| AP-HI-02 | no_visual_hierarchy | hierarchy | ✅ | ✅ fix_ppt.py --type-scale | |
| AP-HI-03 | long_bullet | hierarchy | ✅ | ✅ fix_ppt.py --bullets | |
| AP-HI-04 | too_many_bullets | hierarchy | ✅ | （标注）| ✅ 拆页 |
| AP-HI-05 | bullet_soup | hierarchy | ✅ | （标注）| ✅ 分组 |
| AP-HI-06 | low_contrast | hierarchy | ✅ | 部分（调整颜色）| |
| AP-HI-07 | chart_without_message | hierarchy | ✅ | （标注）| ✅ 加结论 |
| AP-HI-08 | code_without_monospace | hierarchy | ✅ | ✅ 手动改字体 | |
| AP-HI-09 | key_data_not_emphasized | hierarchy | ✅ | ✅ 手动放大字号 | |
| AP-LA-01 | top_text_bottom_image | layout | ✅ | ❌ | ✅ 改布局 |
| AP-LA-02 | no_card_containers | layout | ✅ | ❌ | ✅ 加卡片 |
| AP-LA-03 | image_at_edge | layout | ✅ | ✅ fix_ppt.py --margins | |
| AP-DE-01 | repeated_chapter_labels | deck | ✅ | ❌ | ✅ 删重复标注 |
| AP-DE-02 | inconsistent_alignment | deck | ✅ | ✅ fix_ppt.py --margins | |
| AP-DE-03 | no_brand_consistency | deck | ✅ | ❌ | ✅ 加品牌栏 |

---

## 视觉信号类（非自动检测，需人工判断）

| 现象 | 修复建议 |
|------|----------|
| 渐变背景滥用 | 改用纯色背景 |
| 项目符号海洋（8+ 条） | 拆成 2 页；或砍到 3-4 条 |
| 居中标题页 | 改为左对齐 + 偏上 1/3 位置 |
| 圆角/阴影不一致 | 选一个圆角尺度，全 deck 统一 |
| 动画滥用 | 80% 零动画；仅用 Appear/Fade/Wipe |
| 图标风格混用 | 全 deck 用同一图标库同一风格 |
| 图片风格混用 | 全 deck 用同一图片风格 |
| 拼写错误/中英标点混用 | PowerPoint 拼写检查（F7） |
| 链接未去下划线但不可点击 | 去掉下划线，用 Bold 或强调色 |
| `top_heavy` 内容重心偏上 | 增大卡片高度、下移内容块、增加底部视觉元素 |
| 图片底色与页面背景不统一 | 统一所有配图底色与幻灯片背景一致 |
| 图片荧光发光抢视觉 | 降低插图亮度，保证文字为页面核心视觉主体 |
| 配图仅装饰无信息价值 | 增加标注、分层、业务逻辑拆解 |
| 配色层级单一 | 增加中间过渡色区分二级备注/补充数据/模块分区 |
| 高亮色功能过载 | 每种颜色分配唯一语义角色，参见 SKILL.md DS-2 |
| 章节无视觉过渡 | 章节间加分割色块/全幅图片/分割线 |
| 重点结论无强化容器 | 核心经验/总结内容用底色卡片包裹 |

---

## 标准修复工作流

```bash
# 1. 评分找出所有问题
python scripts/score_ppt_pages.py input.pptx --output report.json

# 2. 一键修复可机械修复的问题
python scripts/fix_ppt.py input.pptx --output fixed.pptx --all \
    --pairing source-han-sans+inter --palette corp-blue

# 3. 渲染对比 before/after
python scripts/render_slides.py input.pptx --output-dir before/
python scripts/render_slides.py fixed.pptx --output-dir after/

# 4. 重新评分验证
python scripts/score_ppt_pages.py fixed.pptx --output report_fixed.json

# 5. 人工处理机械无法修复的问题（three_equal_cards / So what? / 动画等）
#    参考 SKILL.md "人工修复清单"

# 6. 用视觉模型对 after 渲染图做最终评分（详见 SKILL.md）
```