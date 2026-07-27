---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '966c0b83-8583-4b27-a67a-3ca364b7bea0'
  PropagateID: '966c0b83-8583-4b27-a67a-3ca364b7bea0'
  ReservedCode1: '356719a1-c1a3-4af6-a56b-1c40b4ebd8f4'
  ReservedCode2: '356719a1-c1a3-4af6-a56b-1c40b4ebd8f4'
---

# HTML交互版生成指南

> 当用户需要HTML交互版PPT时，使用本指南从已生成的PPTX内容转换。

## 触发条件

用户明确提到以下任一关键词：
- "交互版"、"网页版"、"HTML版"
- "在线演示"、"可互动"
- "frontend-slides"、"open-slide"

## 方案选择

| 场景 | 技能 | 优势 |
|------|------|------|
| 静态展示+丰富动效 | frontend-slides | 零依赖HTML，12种预设，键盘导航，动画丰富 |
| 高度定制交互 | open-slide | React组件，设计系统，热重载，精细控制 |

**默认使用 frontend-slides**（更快、更轻量），仅在用户明确要求React定制时使用 open-slide。

## 转换流程

### 方案A：frontend-slides（默认）

1. 从已生成PPTX的 spec_lock.md 和 notes/ 提取内容大纲
2. 读取 telecom-formal-brand 的配色作为 frontend-slides 的 CSS 变量
3. 使用 frontend-slides 的 workflow 生成 HTML：
   - Style preset 选择：从12个预设中选最接近正式汇报的（如 editorial/minimal/corporate）
   - 配色覆盖为电信品牌色
   - 内容直接从 spec_lock 的页面内容填充
4. 输出单个 HTML 文件

### 方案B：open-slide

1. 初始化 open-slide 项目：`npx @open-slide/cli init <slide-id>`
2. 设置 design system：
   ```tsx
   export const design: DesignSystem = {
     palette: { bg: '#F5F7FA', text: '#333333', accent: '#0077BE' },
     fonts: {
       display: 'Microsoft YaHei, sans-serif',
       body: 'Microsoft YaHei, sans-serif',
     },
     typeScale: { hero: 160, body: 36 },
     radius: 4,
   };
   ```
3. 逐页编写 React 组件，内容从 spec_lock 提取
4. 启动开发服务器预览

## 配色适配规则

从 PPTX 的电信品牌色映射到 HTML CSS 变量：

| PPTX 角色 | HEX | CSS 变量 |
|-----------|-----|---------|
| primary | #0077BE | --accent / --primary |
| bg | #F5F7FA | --bg |
| text | #333333 | --text |
| border | #E2E8F0 | --border |
| muted | #64748B | --muted |
| surface | #FFFFFF | --card-bg |

## 内容适配规则

1. **标题** → HTML slide heading（h1/h2）
2. **要点** → HTML list items（ul/li）
3. **指标卡** → CSS grid + 大数字样式
4. **图表** → 用HTML/CSS复刻简化版（柱状图用div高度，饼图用conic-gradient）
5. **页饰** → 通过页面模板实现（顶部蓝色header + 底部footer）
6. **动效** → reveal animations (IntersectionObserver)，保持克制

## 质量校验

- [ ] 所有页面一屏展示，无滚动
- [ ] 电信蓝主色一致
- [ ] 1920x1080 和 1280x720 均可正常显示
- [ ] 键盘导航（→←↑↓）正常
- [ ] 每页一结论

> AI生成