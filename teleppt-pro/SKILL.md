---
name: teleppt-pro
description: "End-to-end telecom-style PPT generation pipeline: text input �?design direction selection (huashu-design constrained to formal styles) �?China Telecom brand fusion �?ppt-master SVG generation with rich layouts �?PPTX export. Use when user wants to create a China Telecom styled presentation from text/outline/file with professional internal layouts. Triggers: '做电信PPT', '电信汇报PPT', '生成汇报演示', '制作电信风格PPT', 'teleppt', or any request combining telecom branding with rich presentation output. Primary PPTX, optional HTML via frontend-slides/open-slide."
name_cn: 电信PPT大师
description_cn: 从文案到电信风格PPT全流程生成——电信品牌背�?丰富内部排版，一键出�?create_source: super-agent-skill-creator
---

# 电信PPT大师 (teleppt-pro)

从文案到PPT的全流程生成器：电信品牌视觉锁定 + huashu-design 正式设计方向 + ppt-master 丰富排版引擎�?
## 核心理念

**电信�?+ 丰富�?* —�?电信模板提供品牌视觉（配色、字体、LOGO、页饰），huashu-design 提供设计哲学方向，ppt-master 提供自由排版能力，三者融合产�?电信身份+丰富版式"的汇报PPT�?
## 五阶段工作流

```
Phase 1          Phase 2           Phase 3            Phase 4           Phase 5
内容输入        设计方向选择       品牌融合            PPT生成          可选增�?───────�?      ────────�?       ────────�?        ────────�?       ────────�?文本/文件  �? huashu-design  �?电信品牌+设计方向 �?ppt-master管线 �?HTML�?评审
              (正式流派约束)   (brand preset融合)  (SVG→PPTX)     (可�?
```

---

### Phase 1: 内容输入与结构化

**输入接受**：用户可提供以下任一形式——文本描述、内容大纲、Word/PDF/Markdown文件�?
1. 如用户提供了非Markdown文件（PDF/DOCX等），使�?ppt-master �?`scripts/source_to_md/` 转换
2. 将内容结构化为大纲JSON�?
```json
{
  "title": "汇报标题",
  "subtitle": "一句话主题",
  "report_date": "2026�?�?,
  "unit": "中国电信XX分公�?,
  "style_variant": "formal-blue | innovation-red | gov-enterprise",
  "sections": [
    {
      "title": "一、工作回�?,
      "subtitle": "指标、项目、成�?,
      "pages": [
        {
          "title": "科创指标完成情况",
          "type": "metrics | bullets | comparison | timeline | matrix",
          "content": ["要点1", "要点2"]
        }
      ]
    }
  ]
}
```

**风格变体选择**�?
| 变体 | 参数 | 适用场景 |
|------|------|---------|
| formal-blue | 电信�?0077BE + 浅灰�?| 工作报告、领导汇报、年度总结 |
| innovation-red | 电信�?+ 正红点缀 | 科创/研发/AI+/党建 |
| gov-enterprise | 电信�?+ 暖色辅助 | 政企/DICT/客户/商机 |

�?**BLOCKING**: 确认大纲结构和风格变体后，继续下一阶段�?
---

### Phase 2: 设计方向选择

加载设计约束：`Read references/design-constraint-formal.md`

**严格约束**：仅从信息建筑派(01-04)和极简主义�?09-12)中推�?个方向，禁用运动诗学/实验先锋/东方哲学流派�?
执行 huashu-design �?Phase 1-4（理解→重述→推�?方向→视觉Demo），但增加以下约束：

1. **推荐话术**必须强调"正式汇报场景"+"电信配色锁定"
2. **3个Demo**使用电信�?#0077BE)主色 + 用户的实际内容生�?3. **差异化策�?*：信息建筑派1�?+ 极简主义�?�?+ 混合1�?
Demo生成路径�?个并行Agent，每个生成一个HTML Demo并截图。配色强制使用电信品牌色�?
�?**BLOCKING**: 用户选择设计方向后继续�?
---

### Phase 3: 品牌融合

加载融合指南：`Read references/brand-fusion-guide.md`

**核心操作**：将电信品牌身份 + 用户选定的设计方向融合为 ppt-master 的品牌预设�?
1. 复制品牌预设�?ppt-master 项目�?
```bash
cp -r ${SKILL_DIR}/assets/telecom-formal-brand/* <project_path>/templates/
```

2. 品牌预设（`kind: brand`）自动锁定：配色（电信蓝主色+浅灰�?深灰字）、字体（微软雅黑）、页饰（标题�?页脚+LOGO）、语调（正式严谨�?
3. 设计方向影响 Second Layer 参数（辅助色、卡片圆角、间距等），参见 `references/brand-fusion-guide.md` 三层约束模型

**融合结果**�?- 不变量：电信配色/字体/页饰/语调（铁律层�?- 可调量：排版节奏/视觉层次/指标卡样式（调味层）
- 自由量：内容布局/图表选择/信息密度（执行层�?
---

### Phase 4: PPT生成（ppt-master管线�?
**完全委托 ppt-master 技能执�?*，按�?Step 1-7 顺序推进，关键适配点：

| ppt-master步骤 | teleppt-pro适配 |
|----------------|----------------|
| Step 1: 内容处理 | 使用Phase 1的内容（已转Markdown�?|
| Step 2: 项目初始�?| 格式默认 `ppt169`，import-sources |
| Step 3: 模板选项 | 触发！复�?`${SKILL_DIR}/assets/telecom-formal-brand/` 到项目templates/（kind:brand路径�?|
| Step 4: Strategist | Eight Confirmations 预填电信默认值（参见brand-fusion-guide §Step 3），用户可微调辅助色 |
| Step 5: 图片获取 | 按需执行 |
| Step 6: Executor | 每页spec_lock回读校验电信品牌参数；页饰元素（标题�?页脚）强制包含；内容区自由排�?|
| Step 7: 后处理导�?| PPTX输出到工作目�?|

**封面�?*：电信蓝渐变背景(#0077BE�?3399D6) + 居中白色标题 + LOGO
**章节�?*：电信蓝全幅或左蓝右白双�?+ 大号章节�?+ 章节�?**内容�?*：电信蓝标题�?+ 自由排版内容�?+ LOGO页脚

�?**BLOCKING**: Eight Confirmations需用户确认后继续�?
---

### Phase 5: 可选增�?
**5A: HTML交互�?*

触发条件：用户要�?交互�?�?网页�?�?HTML�?

加载指南：`Read references/html-output-guide.md`

- 默认使用 frontend-slides（零依赖HTML，更快）
- 配色覆盖为电信品牌色
- 内容�?spec_lock 提取
- 需要React定制时使�?open-slide

**5B: 设计评审**

触发条件：用户要�?评审"�?review"�?检查设计质�?

- 使用 huashu-design �?Phase 7（设计后评审�?- 5维度打分，重点检查：品牌一致性、视觉层级、正式感
- 评审须额外验证电信品牌参数是否完整保�?
**5C: 迭代修改**

- 用户提出修改意见�?这页数据不够突出"�?配色太深"等）
- 直接修改 spec_lock.md 参数 + 重新生成对应页面
- 无需重新走全流程

## 参考文件索�?
| 文件 | 何时读取 |
|------|---------|
| `references/design-constraint-formal.md` | Phase 2 开始——约束huashu-design的推荐范�?|
| `references/brand-fusion-guide.md` | Phase 3 开始——品牌与设计方向的融合规�?|
| `references/html-output-guide.md` | Phase 5A——HTML版生成指�?|
| `assets/telecom-formal-brand/design_spec.md` | Phase 3——ppt-master品牌预设源文�?|

## 关键约束速查

1. **配色铁律**：主�?0077BE、正�?333333、背�?F5F7FA/#FFFFFF——永不更�?2. **字体铁律**：微软雅�?Bold(标题) + Regular(正文)——永不更�?3. **页饰铁律**：每页必须包含电信蓝标题�?LOGO页脚——永不省�?4. **设计流派**：仅信息建筑�?极简主义派——禁用运�?实验/东方流派
5. **一页一结论**：标题是判断句或行动句，不超�?行文�?6. **数字真实**：用户没给数据时�?待补�?，不编�?7. **图标风格**：stroke线条图标(tabler/lucide)，禁用卡�?3D/emoji

