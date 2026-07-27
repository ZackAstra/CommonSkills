# 前端设计 Token 到 PPT 主题的映射（次要场景）

> **注意**：这是技能的次要工作流——当你需要把**已有前端项目**的设计规范（Tailwind / CSS 变量 / Storybook）同步到 PPT 时使用。大多数"美化 PPT"场景不需要这个，直接用 [color-palettes.md](color-palettes.md) + [font-pairings.md](font-pairings.md) 的现成方案即可。

提取前端设计 token 并映射到 PPT 主题设置，保证视觉一致性。

## 1. Color Token Mapping

### Source: CSS Variables / Tailwind Config / Storybook

| Frontend Token | Example Value | PPT Target | PPT API (python-pptx) |
|---|---|---|---|
| `--color-primary` / `primary-500` | `#3B82F6` | Theme accent color | `slide.theme.color_map[MSO_THEME_COLOR.ACCENT_1]` |
| `--color-primary-dark` / `primary-700` | `#1D4ED8` | Accent dark variant | `MSO_THEME_COLOR.ACCENT_1` + tint |
| `--color-primary-light` / `primary-100` | `#DBEAFE` | Accent light variant | `MSO_THEME_COLOR.ACCENT_1` + lighten |
| `--color-bg` / `bg-default` | `#FFFFFF` / `#0A0A0A` | Slide background | `slide.background.fill.solid()` |
| `--color-surface` / `bg-card` | `#F8FAFC` / `#1E293B` | Card / content area fill | Shape `fill.solid()` |
| `--color-text` / `text-primary` | `#0F172A` / `#F1F5F9` | Body text | `MSO_THEME_COLOR.DARK_1` / `LIGHT_1` |
| `--color-text-muted` / `text-secondary` | `#64748B` / `#94A3B8` | Subtitle / caption text | RGBColor direct |
| `--color-border` / `border-default` | `#E2E8F0` / `#334155` | Shape border / divider | Shape `line.color` |
| `--color-success` | `#10B981` | Positive indicator | RGBColor direct |
| `--color-warning` | `#F59E0B` | Warning indicator | RGBColor direct |
| `--color-error` | `#EF4444` | Error / alert indicator | RGBColor direct |

### Extraction Workflow

1. Locate project design tokens:
   - Tailwind: `tailwind.config.js` / `tailwind.config.ts` → `theme.extend.colors`
   - CSS Variables: `src/styles/tokens.css` / `src/styles/variables.css`
   - Storybook: `/.storybook/preview.js` → `theme` config
   - Design system package: `node_modules/<pkg>/dist/tokens.json`
2. Parse hex/rgb values from token files.
3. Map to PPT theme using table above.
4. Apply via python-pptx theme XML or direct RGBColor assignment.

### Dark Mode Handling

When frontend has dark mode (`prefers-color-scheme: dark`):
- If the PPT is for screen projection (dark room): use dark-mode tokens.
- If the PPT is for print / daylight projection: use light-mode tokens.
- Default: light-mode tokens for business PPT.

## 2. Typography Mapping

| Frontend Token | Example | PPT Target | PPT API |
|---|---|---|---|
| `--font-display` | `Geist`, `Outfit`, `Satoshi` | Title / Heading font | `font.name = "Geist"` |
| `--font-body` | `Inter`, `system-ui` | Body text font | `font.name = "Inter"` |
| `--font-mono` | `JetBrains Mono`, `Geist Mono` | Code / data font | `font.name = "JetBrains Mono"` |
| `font-size-display` | `3.5rem` (56px) | Title size | `font.size = Pt(36)` |
| `font-size-h1` | `2.25rem` (36px) | Section heading | `font.size = Pt(28)` |
| `font-size-h2` | `1.5rem` (24px) | Sub-heading | `font.size = Pt(20)` |
| `font-size-body` | `1rem` (16px) | Body text | `font.size = Pt(14)` |
| `font-size-caption` | `0.75rem` (12px) | Caption / note | `font.size = Pt(10)` |
| `font-weight-bold` | `700` | Heading weight | `font.bold = True` |
| `font-weight-medium` | `500` | Emphasis weight | `font.bold = False` + color |
| `line-height-tight` | `1.1` | Headings | `space_after = Pt(4)` |
| `line-height-normal` | `1.5` | Body | `space_after = Pt(6)` |
| `letter-spacing-tight` | `-0.02em` | Display headings | `font.spacing = Pt(-0.5)` |
| `letter-spacing-wide` | `0.08em` | Eyebrow labels | `font.spacing = Pt(2)` + uppercase |

### Font Availability

- Installed system fonts: use directly via `font.name`.
- Web fonts (Geist, Satoshi, etc.): user must install locally first; provide download link.
- Fallback chain in PPT: primary → Arial → SimSun (CJK).

## 3. Spacing and Layout Mapping

| Frontend Token | CSS Value | PPT Equivalent |
|---|---|---|
| `spacing-page-x` | `px-6` / `px-8` (24-32px) | Slide margin: 0.5-0.67 inch (Left/Right) |
| `spacing-page-y` | `py-12` / `py-16` (48-64px) | Top/Bottom margin: 0.5-0.75 inch |
| `spacing-section` | `py-24` / `gap-16` | Section break: 1.0-1.5 inch vertical gap |
| `spacing-card-padding` | `p-6` / `p-8` (24-32px) | Shape internal margin: 0.25-0.33 inch |
| `spacing-element` | `gap-4` / `gap-6` (16-24px) | Element gap: 0.17-0.25 inch |
| `spacing-tight` | `gap-2` / `gap-3` (8-12px) | Tight gap: 0.08-0.12 inch |
| `max-width-content` | `max-w-4xl` (896px) | Content area width: 8.5-9.5 inch |
| `max-width-page` | `max-w-7xl` (1280px) | Full slide width: 13.33 inch (16:9) |

### Grid System

- 12-column grid at 16:9 (13.33 x 7.5 inch) → each column ≈ 0.89 inch with 0.17 inch gutters.
- Common layouts:
  - Full width: 12 columns
  - Split 50/50: 6 + 6 columns
  - Sidebar: 4 + 8 columns
  - Bento 3-col: 4 + 4 + 4 columns

## 4. Shape and Component Mapping

| Frontend Component | CSS Properties | PPT Shape Style |
|---|---|---|
| Card | `border-radius: 12px`, `box-shadow: 0 1px 3px`, `border: 1px solid` | Rounded rectangle, corner radius ≈ 0.12 inch, subtle shadow, thin border |
| Button (primary) | `bg-primary text-white rounded-lg px-6 py-3` | Rounded rectangle, accent fill, white text, corner radius ≈ 0.1 inch |
| Button (ghost) | `border border-border text-text` | Rounded rectangle, no fill, border color, corner radius ≈ 0.1 inch |
| Badge / Tag | `text-xs uppercase tracking-wider bg-accent/10` | Small rounded rectangle, light accent fill, uppercase small text |
| Divider | `border-t border-border` | Horizontal line shape, border color, width 0.75pt |
| Avatar | `rounded-full w-10 h-10` | Oval shape, 0.42 x 0.42 inch |
| Input field | `border border-border rounded-md px-4 py-2` | Rounded rectangle, white fill, border, placeholder text inside |
| Toast / Alert | `bg-surface border-l-4 border-accent` | Rectangle with left accent bar, surface fill |

### Shadow Scale

| Frontend Class | CSS Value | PPT Shadow Preset |
|---|---|---|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | No shadow (too subtle for PPT) |
| `shadow` | `0 1px 3px rgba(0,0,0,0.1)` | Offset: 1pt, Blur: 3pt, Alpha 15% |
| `shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Offset: 2pt, Blur: 5pt, Alpha 20% |
| `shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Offset: 4pt, Blur: 8pt, Alpha 25% |
| `shadow-xl` | `0 20px 25px rgba(0,0,0,0.1)` | Offset: 6pt, Blur: 12pt, Alpha 30% |

## 5. Design Variance → PPT Style Presets

From taste-skill's three-dial system, map to PPT composition style:

| DESIGN_VARIANCE | PPT Layout Style |
|---|---|
| 1-3 (Predictable) | Centered titles, symmetrical cards, equal grid, standard corporate |
| 4-7 (Offset) | Left-aligned titles, 60/40 split, staggered element sizes, overlapping shapes |
| 8-10 (Asymmetric) | Magazinesque layouts, large white-space zones, break-grid elements, artistic crop |

| VISUAL_DENSITY | PPT Content Density |
|---|---|
| 1-3 (Airy) | One idea per slide, generous margins, large type, minimalist |
| 4-7 (Balanced) | 2-3 elements per slide, standard margins, clear hierarchy |
| 8-10 (Dense) | Data slides OK, compact spacing, multi-zone layouts, dashboard-like |

## 6. Consistency Audit Checklist

After applying tokens to PPT, verify:

- [ ] All accent colors come from the mapped token set (no arbitrary colors)
- [ ] Font family consistent: max 2 fonts (display + body)
- [ ] Corner radius consistent across all shapes (pick one scale: 0 / 0.08 / 0.12 inch)
- [ ] Margins and spacing follow the mapped spacing scale
- [ ] Shadow style consistent (one shadow depth for all cards)
- [ ] Dark/light theme consistent across all slides (no mid-deck flip)