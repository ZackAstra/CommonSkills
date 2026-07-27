---
name: ct-ppt-generator
description: "Generate China Telecom (中国电信) corporate-style PowerPoint presentations based on user-provided outlines or content ideas. Uses a bundled template (天翼AI产品营销推广训练营汇报模�? with predefined slide layouts (cover, TOC, section title pages). Outputs .pptx files that conform to telecom SOE (央企) visual standards. Trigger: user provides a PPT outline/idea and wants a China Telecom styled presentation, or mentions generating a 电信风格/央企风格 PPT. Supports three style variants: government (汇报), marketing (科技/推介), party (党建)."
name_cn: 电信央企风格PPT生成�?description_cn: 根据用户提供的大纲或思路，基于天翼AI汇报模板生成符合中国电信央企风格的PPT演示文稿
create_source: super-agent-skill-creator
---

# 电信央企风格PPT生成�?
基于天翼AI产品营销推广训练营汇报模板，生成符合中国电信央企风格的PPT�?
## 生成流程

```
用户输入大纲/思路 �?内容预处�?�?确定风格 �?基于模板rearrange �?文本替换 �?输出PPTX
```

### Step 1: 内容预处理（MANDATORY�?
将用户的自然语言输入结构化为大纲JSON�?
```json
{
  "title": "PPT主标�?,
  "subtitle": "副标题（组名/部门�?,
  "date": "2026�?�?,
  "sections": [
    {
      "title": "一、产品理�?,
      "items": ["要点1", "要点2", "要点3"],
      "notes": "章节描述（不超过60字）"
    }
  ]
}
```

规则�?- 每页文字不超�?0字，每条要点不超�?5�?- 目录页最�?个章节条�?- 章节标题页描述不超过60�?
### Step 2: 选择风格

| 风格 | 参数 | 适用场景 | 配色要点 |
|------|------|---------|---------|
| 政务汇报 | `government` | 述职、汇报、政企对接、项目申�?| 电信�?0077BE + 深灰 + �?|
| 科技推介 | `marketing` | 路演、营销、数字化方案 | 电信�?+ 浅青蓝渐�?+ 科技银点缀 |
| 党建文化 | `party` | 党建、廉政、企业文�?| 深蓝 + 正红(少量) + 米白 |

若用户未指定，默认`government`�?
### Step 3: 基于模板生成

**模板结构**�?页，3种页面类型）�?
| 页面类型 | 模板Slide | 说明 |
|---------|-----------|------|
| 封面 | 0 | 主标�?+ 组名 + 日期 |
| 目录 | 1 | �?�?CONTENTS + 3个章节条 |
| 章节标题 | 2 | 章节�?标题 + 描述 |

**生成映射**：`0, 1, 2, 2, 2, ...`（封�?+ 目录 + N个章节标题页复用slide-2�?
执行命令�?```bash
# 1. Rearrange
python <pptx-skill>/scripts/rearrange.py assets/ct-template.pptx working.pptx 0,1,2,2,2

# 2. Inventory
python <pptx-skill>/scripts/inventory.py working.pptx inventory.json

# 3. Replace
python <pptx-skill>/scripts/replace.py working.pptx replacement.json output.pptx
```

也可以直接使用脚本：
```bash
python scripts/ct_ppt_gen.py --outline outline.json --style government --output output.pptx
```

### Step 4: 内容填充规范

**封面（slide-0�?*�?- shape-0: 主标题，44pt 微软雅黑 Bold，居中，颜色随风格变�?- shape-1: 副标题行1(组名) + �?(日期)�?1.35pt 华文细黑 Bold，居中反�?
**目录（slide-1�?*�?- shape-0: "�?�?�?4.8pt Times New Roman Bold
- shape-1: "CONTENTS"�?2.4pt
- shape-2/4/6: 中文数字"一二三"�?0pt 右对�?- shape-3/5/7: 章节名称（去�?X�?前缀），12pt 居中

**章节标题页（slide-2�?*�?- shape-0: 章节标题（如"一、产品理�?），16pt Bold
- shape-1: 章节描述文字，不超过60�?
## 风格规范速查

详见 [references/style-guide.md](references/style-guide.md)，包含：
- 配色方案精确色�?- 字体/字号层级�?- 版式布局黄金规则
- 配图/图标/动效规范
- 避坑总结

## 资源文件

### assets/
- `ct-template.pptx` - 天翼AI产品营销推广训练营汇报模板（7页原版）

### scripts/
- `ct_ppt_gen.py` - 一键生成脚本（封装rearrange→inventory→replace全流程）

### references/
- `style-guide.md` - 电信央企PPT风格完整规范

