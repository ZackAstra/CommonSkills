# -*- coding: utf-8 -*-
"""gen_pil_illustrations.py — PIL 配图模板脚本

职责：根据 JSON 配置，用 PIL 生成常见示意图（时间线/对比图/结构图/流程图）。
      Agent 只需编写配置，无需每次从零编写 PIL 代码。

使用方式：
  python gen_pil_illustrations.py --config config.json --output-dir output/

config.json 格式：
  [
    {
      "type": "timeline",
      "output": "02_timeline.png",
      "width": 2400,
      "height": 1350,
      "style": {
        "bg_color": "#FFFFFF",
        "accent_color": "#E60012",
        "text_color": "#333333",
        "font_path": "C:/Windows/Fonts/msyh.ttc",
        "font_size_title": 28,
        "font_size_label": 22
      },
      "data": {
        "title": "智能体演进",
        "stages": [
          {"label": "流程编排型", "sub": "2023年中", "desc": "Dify/Coze"},
          {"label": "窗口式", "sub": "2023年下半年", "desc": "Cursor/ZCode"},
          {"label": "桌面型", "sub": "2024年初至今", "desc": "TeleClaw"}
        ]
      }
    },
    {
      "type": "comparison",
      "output": "06_comparison.png",
      "data": {
        "title": "能力对比",
        "columns": [
          {"label": "流程编排型", "items": ["能输出", "应变≈0"]},
          {"label": "窗口式", "items": ["能应变", "单窗口"]},
          {"label": "桌面型", "items": ["能联动", "跨场景"]}
        ]
      }
    },
    ...
  ]

支持的 type:
  - timeline:    横向时间线，3-5 个阶段节点
  - comparison:  左右/多栏对比图
  - structure:   层级结构图（树形或嵌套矩形）
  - flowchart:   简化流程图（3-5 步）
  - pyramid:     金字塔/三角层级图
  - infographic: 数据大字报（1-3 个大数据指标）
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is required.  pip install Pillow", file=sys.stderr)
    sys.exit(1)


# ── Default style ──

DEFAULT_STYLE = {
    "bg_color": "#FFFFFF",
    "accent_color": "#E60012",
    "secondary_color": "#2563EB",
    "text_color": "#282828",
    "light_bg": "#F5F5F5",
    "font_path": "C:/Windows/Fonts/msyh.ttc",
    "font_size_title": 28,
    "font_size_label": 22,
    "font_size_small": 16,
}


def _parse_color(hex_str):
    """Parse hex color string to (R, G, B) tuple."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def _load_font(style, size_key="font_size_label"):
    """Load font with fallback."""
    font_path = style.get("font_path", DEFAULT_STYLE["font_path"])
    font_size = style.get(size_key, DEFAULT_STYLE[size_key])
    try:
        return ImageFont.truetype(font_path, font_size)
    except Exception:
        try:
            return ImageFont.truetype(font_path, font_size - 4)
        except Exception:
            return ImageFont.load_default()


# ── Drawing helpers ──

def _draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    if fill:
        draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
        draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
        draw.pieslice([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=fill)
        draw.pieslice([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=fill)
        draw.pieslice([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=fill)
        draw.pieslice([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + r, y0, x1 - r, y0], fill=outline, width=width)
        draw.line([x0 + r, y1, x1 - r, y1], fill=outline, width=width)
        draw.line([x0, y0 + r, x0, y1 - r], fill=outline, width=width)
        draw.line([x1, y0 + r, x1, y1 - r], fill=outline, width=width)


def _draw_centered_text(draw, text, cx, cy, font, fill):
    """Draw text centered at (cx, cy)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=fill)


# ── Illustration generators ──

def draw_timeline(img, data, style):
    """Draw horizontal timeline with 3-5 stages."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    accent = _parse_color(style.get("accent_color", DEFAULT_STYLE["accent_color"]))
    text_color = _parse_color(style.get("text_color", DEFAULT_STYLE["text_color"]))
    font_label = _load_font(style, "font_size_label")
    font_small = _load_font(style, "font_size_small")

    stages = data.get("stages", [])
    n = len(stages)
    if n == 0:
        return

    # Timeline line
    margin_x = 180
    line_y = h * 0.55
    line_x0 = margin_x
    line_x1 = w - margin_x
    draw.line([(line_x0, line_y), (line_x1, line_y)], fill=accent, width=4)

    # Arrow at end
    arrow_size = 20
    draw.polygon([
        (line_x1, line_y),
        (line_x1 - arrow_size, line_y - arrow_size // 2),
        (line_x1 - arrow_size, line_y + arrow_size // 2),
    ], fill=accent)

    # Stage nodes
    gap = (line_x1 - line_x0) / max(n - 1, 1) if n > 1 else 0
    for i, stage in enumerate(stages):
        cx = int(line_x0 + i * gap) if n > 1 else w // 2

        # Circle node
        r = 18
        draw.ellipse([cx - r, int(line_y) - r, cx + r, int(line_y) + r], fill=accent)

        # Label above
        label = stage.get("label", "")
        _draw_centered_text(draw, label, cx, int(line_y - 50), font_label, text_color)

        # Sub-label below line
        sub = stage.get("sub", "")
        _draw_centered_text(draw, sub, cx, int(line_y + 40), font_small, text_color)

        # Description further below
        desc = stage.get("desc", "")
        if desc:
            _draw_centered_text(draw, desc, cx, int(line_y + 70), font_small, accent)

    # Title
    title = data.get("title", "")
    if title:
        font_title = _load_font(style, "font_size_title")
        _draw_centered_text(draw, title, w // 2, 60, font_title, text_color)


def draw_comparison(img, data, style):
    """Draw multi-column comparison."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    accent = _parse_color(style.get("accent_color", DEFAULT_STYLE["accent_color"]))
    sec = _parse_color(style.get("secondary_color", DEFAULT_STYLE["secondary_color"]))
    text_color = _parse_color(style.get("text_color", DEFAULT_STYLE["text_color"]))
    light_bg = _parse_color(style.get("light_bg", DEFAULT_STYLE["light_bg"]))
    font_label = _load_font(style, "font_size_label")
    font_small = _load_font(style, "font_size_small")

    columns = data.get("columns", [])
    n = len(columns)
    if n == 0:
        return

    margin = 120
    gap = 40
    col_w = (w - 2 * margin - (n - 1) * gap) / n
    top_y = 120

    colors = [accent, sec, _parse_color("#059669")]
    for i, col in enumerate(columns):
        x = margin + i * (col_w + gap)
        color = colors[i % len(colors)]

        # Header bar
        header_h = 60
        _draw_rounded_rect(draw, (x, top_y, x + col_w, top_y + header_h),
                           radius=8, fill=color)
        _draw_centered_text(draw, col.get("label", ""), int(x + col_w / 2),
                           int(top_y + header_h / 2), font_label, (255, 255, 255))

        # Items
        items = col.get("items", [])
        item_y = top_y + header_h + 15
        for j, item in enumerate(items):
            item_h = 50
            bg = light_bg if j % 2 == 0 else _parse_color("#FFFFFF")
            _draw_rounded_rect(draw, (x, item_y, x + col_w, item_y + item_h),
                               radius=4, fill=bg)
            _draw_centered_text(draw, item, int(x + col_w / 2),
                               int(item_y + item_h / 2), font_small, text_color)
            item_y += item_h + 8

    # Title
    title = data.get("title", "")
    if title:
        font_title = _load_font(style, "font_size_title")
        _draw_centered_text(draw, title, w // 2, 50, font_title, text_color)


def draw_structure(img, data, style):
    """Draw hierarchical structure (nested rectangles or tree)."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    accent = _parse_color(style.get("accent_color", DEFAULT_STYLE["accent_color"]))
    text_color = _parse_color(style.get("text_color", DEFAULT_STYLE["text_color"]))
    font_label = _load_font(style, "font_size_label")
    font_small = _load_font(style, "font_size_small")

    layers = data.get("layers", [])
    n = len(layers)
    if n == 0:
        return

    margin_x = 100
    top_y = 120
    gap = 20

    for i, layer in enumerate(layers):
        y = top_y + i * (80 + gap)
        # Each layer is a full-width bar, progressively narrower
        indent = i * 60
        x0 = margin_x + indent
        x1 = w - margin_x - indent

        color = accent if i == 0 else _parse_color(style.get("secondary_color", DEFAULT_STYLE["secondary_color"]))
        _draw_rounded_rect(draw, (x0, y, x1, y + 70), radius=8,
                           outline=color, width=3)
        label = layer.get("label", "")
        _draw_centered_text(draw, label, (x0 + x1) // 2, y + 35, font_label, color)

        # Draw connecting line to next layer
        if i < n - 1:
            mid_x = (x0 + x1) // 2
            draw.line([(mid_x, y + 70), (mid_x, y + 70 + gap)],
                     fill=text_color, width=2)

    # Title
    title = data.get("title", "")
    if title:
        font_title = _load_font(style, "font_size_title")
        _draw_centered_text(draw, title, w // 2, 50, font_title, text_color)


def draw_flowchart(img, data, style):
    """Draw simple flowchart with 3-5 steps."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    accent = _parse_color(style.get("accent_color", DEFAULT_STYLE["accent_color"]))
    sec = _parse_color(style.get("secondary_color", DEFAULT_STYLE["secondary_color"]))
    text_color = _parse_color(style.get("text_color", DEFAULT_STYLE["text_color"]))
    font_label = _load_font(style, "font_size_label")
    font_small = _load_font(style, "font_size_small")

    steps = data.get("steps", [])
    n = len(steps)
    if n == 0:
        return

    margin_x = 150
    box_w = (w - 2 * margin_x - (n - 1) * 80) / n
    box_h = 80
    cy = h // 2

    colors = [accent, sec, _parse_color("#059669"), _parse_color("#D97706"), accent]
    for i, step in enumerate(steps):
        x = margin_x + i * (box_w + 80)
        y = cy - box_h // 2
        color = colors[i % len(colors)]

        # Box
        _draw_rounded_rect(draw, (x, y, x + box_w, y + box_h), radius=10, fill=color)
        label = step.get("label", "")
        _draw_centered_text(draw, label, int(x + box_w / 2), int(y + box_h / 2),
                           font_label, (255, 255, 255))

        # Arrow to next
        if i < n - 1:
            ax0 = x + box_w + 5
            ax1 = x + box_w + 75
            draw.line([(ax0, cy), (ax1, cy)], fill=text_color, width=3)
            draw.polygon([(ax1, cy), (ax1 - 12, cy - 8), (ax1 - 12, cy + 8)],
                        fill=text_color)

        # Description below
        desc = step.get("desc", "")
        if desc:
            _draw_centered_text(draw, desc, int(x + box_w / 2), int(y + box_h + 30),
                               font_small, text_color)

    # Title
    title = data.get("title", "")
    if title:
        font_title = _load_font(style, "font_size_title")
        _draw_centered_text(draw, title, w // 2, 50, font_title, text_color)


def draw_pyramid(img, data, style):
    """Draw pyramid/triangle layers."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    accent = _parse_color(style.get("accent_color", DEFAULT_STYLE["accent_color"]))
    text_color = _parse_color(style.get("text_color", DEFAULT_STYLE["text_color"]))
    font_label = _load_font(style, "font_size_label")

    layers = data.get("layers", [])
    n = len(layers)
    if n == 0:
        return

    cx = w // 2
    top_y = 100
    bottom_y = h - 80
    max_half_w = w // 2 - 120

    colors = [
        accent,
        _parse_color(style.get("secondary_color", DEFAULT_STYLE["secondary_color"])),
        _parse_color("#059669"),
        _parse_color("#D97706"),
        _parse_color("#7C3AED"),
    ]

    for i, layer in enumerate(layers):
        frac_top = i / n
        frac_bot = (i + 1) / n
        y_top = int(top_y + frac_top * (bottom_y - top_y))
        y_bot = int(top_y + frac_bot * (bottom_y - top_y))
        half_w_top = int(frac_top * max_half_w)
        half_w_bot = int(frac_bot * max_half_w)

        points = [
            (cx - half_w_top, y_top),
            (cx + half_w_top, y_top),
            (cx + half_w_bot, y_bot),
            (cx - half_w_bot, y_bot),
        ]
        color = colors[i % len(colors)]
        draw.polygon(points, fill=color)

        label = layer.get("label", "")
        label_y = (y_top + y_bot) // 2
        _draw_centered_text(draw, label, cx, label_y, font_label, (255, 255, 255))

    # Title
    title = data.get("title", "")
    if title:
        font_title = _load_font(style, "font_size_title")
        _draw_centered_text(draw, title, w // 2, 40, font_title, text_color)


def draw_infographic(img, data, style):
    """Draw data infographic (1-3 big numbers)."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    accent = _parse_color(style.get("accent_color", DEFAULT_STYLE["accent_color"]))
    text_color = _parse_color(style.get("text_color", DEFAULT_STYLE["text_color"]))
    font_label = _load_font(style, "font_size_title")
    font_small = _load_font(style, "font_size_small")

    metrics = data.get("metrics", [])
    n = len(metrics)
    if n == 0:
        return

    margin = 120
    gap = 40
    card_w = (w - 2 * margin - (n - 1) * gap) / n
    cy = h // 2

    for i, metric in enumerate(metrics):
        x = margin + i * (card_w + gap)
        card_h = 200
        y = cy - card_h // 2

        # Card background
        _draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), radius=12,
                           outline=accent, width=3)

        # Big number
        value = metric.get("value", "")
        font_big = _load_font(style, "font_size_title")
        # Try to make the number even bigger
        try:
            font_big = ImageFont.truetype(
                style.get("font_path", DEFAULT_STYLE["font_path"]), 48)
        except Exception:
            pass
        _draw_centered_text(draw, value, int(x + card_w / 2), int(y + card_h * 0.4),
                           font_big, accent)

        # Label
        label = metric.get("label", "")
        _draw_centered_text(draw, label, int(x + card_w / 2), int(y + card_h * 0.75),
                           font_small, text_color)


# ── Dispatcher ──

TYPE_HANDLERS = {
    "timeline": draw_timeline,
    "comparison": draw_comparison,
    "structure": draw_structure,
    "flowchart": draw_flowchart,
    "pyramid": draw_pyramid,
    "infographic": draw_infographic,
}

# Also map suggestion_types from suggest_illustrations.py to PIL template types
SUGGESTION_TYPE_MAP = {
    "timeline": "timeline",
    "comparison_diagram": "comparison",
    "structure_diagram": "structure",
    "flowchart": "flowchart",
    "data_chart": "infographic",
    "concept_illustration": "infographic",
    "icon_cards": "comparison",
    "scene_image": None,  # Cannot auto-generate with PIL
    "closing_image": None,  # Cannot auto-generate with PIL
}


def process_entry(entry, output_dir):
    """Process one config entry and save the resulting image."""
    illu_type = entry.get("type", "timeline")
    
    # Map suggestion types to PIL template types
    pil_type = SUGGESTION_TYPE_MAP.get(illu_type, illu_type)
    if pil_type is None:
        print(f"  SKIP: type '{illu_type}' cannot be auto-generated with PIL", file=sys.stderr)
        return False
    
    handler = TYPE_HANDLERS.get(pil_type)
    if handler is None:
        print(f"  WARNING: Unknown PIL type '{pil_type}' (from '{illu_type}'), skipping", file=sys.stderr)
        return False

    width = entry.get("width", 2400)
    height = entry.get("height", 1350)
    style = {**DEFAULT_STYLE, **entry.get("style", {})}
    data = entry.get("data", {})
    output = entry.get("output", f"{pil_type}.png")

    # Validate data is present
    if not data:
        print(f"  SKIP: {output} — no data (data_status={entry.get('data_status', 'unknown')})",
              file=sys.stderr)
        return False

    # Create image
    bg_color = _parse_color(style.get("bg_color", DEFAULT_STYLE["bg_color"]))
    img = Image.new("RGB", (width, height), bg_color)

    # Draw
    handler(img, data, style)

    # Save
    out_path = Path(output_dir) / output
    img.save(str(out_path), "PNG")
    print(f"  OK: {output} ({width}x{height})")
    return True


# ── Auto-generate from PPTX ──

def auto_generate_from_pptx(pptx_path, output_dir, scenario="default", verbose=False):
    """从 PPTX 一键生成所有可自动提取数据的配图。
    
    流程：suggest_illustrations.py 分析 → 过滤 auto 条目 → 渲染。
    返回: (auto_count, skipped_list)
    """
    # Lazy import to avoid circular dependency at module level
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from suggest_illustrations import analyze_pptx
    
    if verbose:
        print(f"Auto-generate: analyzing {pptx_path} ...", file=sys.stderr)
    
    result = analyze_pptx(pptx_path, verbose=verbose, scenario=scenario)
    
    auto_entries = []
    manual_entries = []
    non_pil_entries = []
    
    for entry in result.get("gen_config", []):
        ds = entry.get("data_status", "none")
        gm = ""  # generation_method not in gen_config; check by type
        illu_type = entry.get("type", "")
        
        # Check if this type can be handled by PIL
        pil_type = SUGGESTION_TYPE_MAP.get(illu_type)
        if pil_type is None:
            non_pil_entries.append(entry)
            continue
        
        if ds == "auto" and entry.get("data"):
            auto_entries.append(entry)
        elif ds == "manual":
            manual_entries.append(entry)
        elif entry.get("data"):
            # Has data but no status flag — still try
            auto_entries.append(entry)
        else:
            manual_entries.append(entry)
    
    if verbose:
        print(f"  Auto-extracted: {len(auto_entries)} pages", file=sys.stderr)
        print(f"  Need manual data: {len(manual_entries)} pages", file=sys.stderr)
        print(f"  Non-PIL (SVG/ImageGen): {len(non_pil_entries)} pages", file=sys.stderr)
    
    # Generate auto entries
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    success = 0
    for entry in auto_entries:
        ok = process_entry(entry, output_dir)
        if ok:
            success += 1
    
    # Report
    de = result.get("summary", {}).get("data_extraction", {})
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"自动配图生成报告", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"总页数: {result['total_slides']}", file=sys.stderr)
    print(f"数据自动提取: {de.get('auto', 0)} 页", file=sys.stderr)
    print(f"数据需手动补充: {de.get('manual', 0)} 页", file=sys.stderr)
    print(f"生成成功: {success}/{len(auto_entries)} 张", file=sys.stderr)
    
    if manual_entries:
        print(f"\n需要手动补充 data 的页面:", file=sys.stderr)
        for e in manual_entries:
            print(f"  P{e['slide']:2d}: {e['type']} → 需手动填写 data 字段", file=sys.stderr)
    
    if non_pil_entries:
        print(f"\n非 PIL 类型（需 Agent 用 SVG/ImageGen 生成）:", file=sys.stderr)
        for e in non_pil_entries:
            print(f"  P{e['slide']:2d}: {e['type']}", file=sys.stderr)
    
    return success, manual_entries


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Generate PIL illustrations from JSON config or directly from PPTX."
    )
    
    # Mode 1: from JSON config (original)
    # Mode 2: from PPTX (new --from-pptx)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config",
                       help="JSON config file specifying illustrations (original mode)")
    group.add_argument("--from-pptx",
                       help="Auto-generate illustrations from PPTX file (auto mode)")
    
    parser.add_argument("--output-dir", default=".",
                        help="Output directory for generated PNGs (default: current)")
    parser.add_argument("--scenario", default="default",
                        help="Brand/scenario for style (e.g. telecom, tech; default: default)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed progress")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.from_pptx:
        # Auto mode: analyze PPTX + generate
        if not Path(args.from_pptx).exists():
            print(f"ERROR: File not found: {args.from_pptx}", file=sys.stderr)
            sys.exit(1)
        auto_count, skipped = auto_generate_from_pptx(
            args.from_pptx, output_dir, scenario=args.scenario, verbose=args.verbose
        )
        print(f"\nAuto-generated {auto_count} illustration(s) -> {output_dir}")
        if skipped:
            print(f"{len(skipped)} page(s) need manual data — edit gen_config and re-run with --config")
    else:
        # Original mode: from JSON config
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)

        if not isinstance(config, list):
            print("ERROR: config must be a JSON array", file=sys.stderr)
            sys.exit(1)

        success = 0
        for entry in config:
            ok = process_entry(entry, output_dir)
            if ok:
                success += 1

        print(f"\nGenerated {success}/{len(config)} illustration(s) -> {output_dir}")


if __name__ == "__main__":
    main()
