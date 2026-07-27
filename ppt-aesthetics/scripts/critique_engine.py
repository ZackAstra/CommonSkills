#!python3
"""
critique_engine.py — PPTX & HTML 结构化检测引擎

对 PPTX / HTML 文件进行 8 维度结构化评分，输出评分 + 问题清单。
8 维度：whitespace, type_scale, color_harmony, alignment, spacing, imagery, consistency, hierarchy
PPTX 复用 score_ppt_pages 的 analyze_slide / summarize_deck / _resolve_theme_fonts。
HTML 使用 BeautifulSoup4 + 正则解析，不依赖浏览器。
无状态函数，不负责迭代控制。

Usage:
    python critique_engine.py <file> [--palette #HEX1,#HEX2] [--density-mode low|high] [--output report.json]
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    BeautifulSoup = None  # type: ignore
    Tag = None  # type: ignore

sys.stdout.reconfigure(encoding="utf-8")

# Add the scripts dir to path so we can import score_ppt_pages
_SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SCRIPTS_DIR))

from score_ppt_pages import (
    analyze_slide,
    summarize_deck,
    _resolve_theme_fonts,
    _is_neutral_color,
    _color_family,
)
from pptx import Presentation
from pptx.util import Inches, Pt, Emu

EMU_PER_INCH = 914400

# --------------------------------------------------------------------------- #
# Anti-pattern → dimension mapping
# --------------------------------------------------------------------------- #
_AP_TO_DIMENSION: dict[str, str] = {
    "wall_of_text": "whitespace",
    "high_text_density": "whitespace",
    "text_heavy_deck": "whitespace",
    "low_fill_rate": "whitespace",
    "high_fill_rate": "whitespace",
    "empty_quadrant": "whitespace",
    "too_many_fonts": "type_scale",
    "unprofessional_font": "type_scale",
    "cjk_text_no_cjk_font": "type_scale",
    "weak_type_scale": "type_scale",
    "extreme_type_scale": "type_scale",
    "too_many_colors": "color_harmony",
    "ai_purple_palette": "color_harmony",
    "oversaturated_pure_rgb": "color_harmony",
    "overuse_accent": "color_harmony",
    "pure_black_text": "color_harmony",
    "pure_white_card": "color_harmony",
    "rainbow_text": "color_harmony",
    "inconsistent_colors": "color_harmony",
    "no_margins": "alignment",
    "three_equal_cards": "alignment",
    "misaligned_elements": "alignment",
    "irregular_spacing": "spacing",
    "inconsistent_spacing": "spacing",
    "low_res_image": "imagery",
    "stretched_image": "imagery",
    "stretched_images": "imagery",
    "clipart_style": "imagery",
    "tiny_text": "hierarchy",
    "no_visual_hierarchy": "hierarchy",
    "long_bullet": "hierarchy",
    "too_many_bullets": "hierarchy",
    "bullet_soup": "hierarchy",
    "inconsistent_fonts": "consistency",
    "default_template": "consistency",
    "orphan_widow": "spacing",
    "low_contrast": "hierarchy",
    "chart_without_message": "hierarchy",
    "hollow_container": "layout",
    "no_card_containers": "layout",
    "bare_text_no_card": "layout",
    "unbalanced_layout": "layout",
    "image_at_edge": "layout",
    "table_no_zebra": "layout",
    "table_weak_header": "layout",
    "key_data_not_emphasized": "hierarchy",
    "code_without_monospace": "hierarchy",
    "mixed_numbering": "layout",
    # Deck-level anti-patterns (AP-DE-*)
    "repeated_chapter_labels": "consistency",
    "inconsistent_alignment": "alignment",
    "no_brand_consistency": "consistency",
    "inconsistent_margins": "alignment",
    "inconsistent_section_pos": "alignment",
    "cover_ending_mismatch": "consistency",
    "density_outlier": "whitespace",
    "no_header_navigation": "hierarchy",
    "deck_too_many_fonts": "type_scale",
    "deck_too_many_colors": "color_harmony",
    # Additional page-level patterns
    "top_heavy": "layout",
    "top_text_bottom_image": "layout",
}

_AP_SEVERITY_CATEGORY: dict[str, str] = {
    "wall_of_text": "hard",
    "high_text_density": "soft",
    "text_heavy_deck": "hard",
    "low_fill_rate": "hard",
    "high_fill_rate": "soft",
    "empty_quadrant": "hard",
    "too_many_fonts": "hard",
    "unprofessional_font": "hard",
    "cjk_text_no_cjk_font": "hard",
    "too_many_colors": "hard",
    "ai_purple_palette": "soft",
    "oversaturated_pure_rgb": "soft",
    "no_margins": "soft",
    "three_equal_cards": "soft",
    "weak_type_scale": "hard",
    "extreme_type_scale": "soft",
    "overuse_accent": "soft",
    "pure_black_text": "soft",
    "pure_white_card": "soft",
    "rainbow_text": "hard",
    "inconsistent_colors": "hard",
    "misaligned_elements": "hard",
    "long_bullet": "soft",
    "too_many_bullets": "hard",
    "irregular_spacing": "soft",
    "inconsistent_spacing": "soft",
    "low_res_image": "soft",
    "stretched_image": "soft",
    "stretched_images": "hard",
    "clipart_style": "soft",
    "tiny_text": "hard",
    "no_visual_hierarchy": "hard",
    "bullet_soup": "soft",
    "inconsistent_fonts": "hard",
    "default_template": "soft",
    "orphan_widow": "soft",
    "low_contrast": "soft",
    "chart_without_message": "soft",
    "hollow_container": "hard",
    "no_card_containers": "hard",
    "bare_text_no_card": "soft",
    "unbalanced_layout": "hard",
    "image_at_edge": "soft",
    "table_no_zebra": "soft",
    "table_weak_header": "soft",
    "key_data_not_emphasized": "soft",
    "code_without_monospace": "soft",
    "mixed_numbering": "soft",
    # Deck-level anti-patterns (AP-DE-*)
    "repeated_chapter_labels": "soft",
    "inconsistent_alignment": "hard",
    "no_brand_consistency": "soft",
    "inconsistent_margins": "hard",
    "inconsistent_section_pos": "soft",
    "cover_ending_mismatch": "soft",
    "density_outlier": "soft",
    "no_header_navigation": "hard",
    "deck_too_many_fonts": "hard",
    "deck_too_many_colors": "hard",
    # Additional page-level patterns
    "top_heavy": "soft",
    "top_text_bottom_image": "hard",
}


def _parse_anti_pattern_key(ap: str) -> str:
    """Extract the anti-pattern key from a string like 'wall_of_text: ...'."""
    return ap.split(":", 1)[0].strip()


def _suggestion_for(key: str) -> str:
    """Human-readable suggestion for an anti-pattern."""
    suggestions = {
        "wall_of_text": "将长文本拆分为多个要点或使用分段布局",
        "high_text_density": "精简文字或拆分到多页",
        "text_heavy_deck": "减少文字面积占比至 60% 以下，增加配图或留白",
        "low_fill_rate": "增加有效内容填充率至 60% 以上，避免大面积空白",
        "high_fill_rate": "减少内容密度，增加留白，目标填充率 60-70%",
        "empty_quadrant": "调整布局使内容分布在四个象限，避免大片空白区域",
        "too_many_fonts": "将全页字体控制在 2-3 种以内",
        "unprofessional_font": "替换为专业字体（如思源黑体、Inter）",
        "cjk_text_no_cjk_font": "为中文字符指定中文字体（如思源黑体）",
        "too_many_colors": "将颜色控制在 3-5 种以内",
        "ai_purple_palette": "减少靛蓝/紫色使用，使用更克制的品牌色",
        "oversaturated_pure_rgb": "使用加灰/降低饱和度的色调替代纯色",
        "no_margins": "为页面添加 8%-12% 的安全边距（百分比制）",
        "three_equal_cards": "给卡片赋予不同的视觉权重（大小/颜色/层级）",
        "weak_type_scale": "将标题与正文字号比提升至 >= 1.25（Major Third）",
        "extreme_type_scale": "检查超大字号是否属于封面元素误入内容页",
        "overuse_accent": "减少强调色使用面积，遵循 60-30-10 法则",
        "pure_black_text": "将 #000000 替换为近黑色（如 #1A1A1A）",
        "pure_white_card": "将纯白卡片填充替换为近白色（如 #F5F5F5）",
        "rainbow_text": "将单页颜色控制在 3 种以内，遵循 60-30-10 法则",
        "inconsistent_colors": "统一跨页配色方案，使用同一调色板",
        "misaligned_elements": "将元素对齐到统一的网格线",
        "long_bullet": "将长要点拆分为多条，中文每条 <= 25 字，英文 <= 12 词",
        "too_many_bullets": "将要点控制在 6 条以内，理想为 3-4 条",
        "irregular_spacing": "将垂直间距对齐到 0.08in (4px) 网格倍数",
        "inconsistent_spacing": "统一跨页间距节奏，对齐到 4/8px 网格",
        "low_res_image": "替换为分辨率 >= 800x600 的高清图片",
        "stretched_image": "调整图片比例使其不变形",
        "stretched_images": "调整图片比例使其不变形",
        "clipart_style": "替换为高质量矢量图标或专业配图",
        "tiny_text": "将正文字号提升至 12pt 以上",
        "no_visual_hierarchy": "建立标题-正文-注释三级视觉层次",
        "bullet_soup": "将要点分组或使用视觉化布局替代纯列表",
        "inconsistent_fonts": "统一跨页字体方案，使用同一字体搭配",
        "default_template": "替换默认模板，使用品牌定制模板",
        "orphan_widow": "调整行距或文字框宽度避免孤行/寡行",
        "low_contrast": "提高文字与背景的对比度，确保 WCAG AA 标准",
        "chart_without_message": "为图表添加结论性标题或 So what? 标注",
        "hollow_container": "将 add_bg()+add_rich_textbox() 替换为 add_table()，让容器高度自适应内容",
        "no_card_containers": "为超过3个文本块的页面添加半透明卡片容器",
        "bare_text_no_card": "为独立文本块添加卡片背景容器",
        "unbalanced_layout": "调整元素分布，使四个象限视觉重量均衡",
        "image_at_edge": "将图片内移至距边缘 >= 3% 的位置",
        "table_no_zebra": "为表格添加隔行变色（斑马纹）提升可读性",
        "table_weak_header": "加强表头视觉权重（加粗、底色、字号）",
        "key_data_not_emphasized": "对关键数据使用品牌色或加粗强调",
        "code_without_monospace": "为代码片段指定等宽字体",
        "mixed_numbering": "统一编号体系，避免混用数字/字母/罗马数字",
        # Deck-level anti-patterns
        "repeated_chapter_labels": "统一章节标签样式和措辞",
        "inconsistent_alignment": "统一跨页对齐方式（左对齐/居中）",
        "no_brand_consistency": "确保品牌色、Logo、字体的跨页一致性",
        "inconsistent_margins": "统一跨页页边距到相同数值",
        "inconsistent_section_pos": "统一章节标题/标签的跨页位置",
        "cover_ending_mismatch": "确保封面与结尾页风格一致",
        "density_outlier": "调整内容密度异常页，使其接近全页均值",
        "no_header_navigation": "添加统一的页眉导航标识",
        "deck_too_many_fonts": "将全文档字体种类控制在 3 种以内",
        "deck_too_many_colors": "将全文档配色控制在 5 种以内",
        # Additional page-level patterns
        "top_heavy": "调整布局使内容垂直分布更均衡，避免顶部过重",
        "top_text_bottom_image": "将文上图下的布局改为并列或上下反转",
    }
    return suggestions.get(key, f"修复检测到的视觉问题")


def _build_issues_from_anti_patterns(
    anti_patterns: list[str],
) -> list[dict]:
    """Convert score_ppt_pages anti_pattern strings to our issue format."""
    issues = []
    for ap in anti_patterns:
        key = _parse_anti_pattern_key(ap)
        dimension = _AP_TO_DIMENSION.get(key)
        severity = _AP_SEVERITY_CATEGORY.get(key, "soft")
        if dimension is None:
            continue
        auto_fixable = True
        # Non-auto-fixable: images that need replacement, etc.
        if key in ("low_res_image", "stretched_image", "unprofessional_font"):
            auto_fixable = False
        issues.append({
            "severity": severity,
            "dimension": dimension,
            "element": key,
            "problem": ap[:120],
            "suggestion": _suggestion_for(key),
            "auto_fixable": auto_fixable,
        })
    return issues


# --------------------------------------------------------------------------- #
# Additional dimension checks beyond anti-patterns
# --------------------------------------------------------------------------- #
_PLACEHOLDER_PATTERNS = re.compile(
    r"\b(TODO|TBD|XXX|FIXME|HACK|占位|待补充|待定|Lorem Ipsum|lorem ipsum)\b",
    re.IGNORECASE,
)


def _check_alignment(layout_signals: dict) -> list[dict]:
    """Soft-alignment check: left_edges/top_edges should align to 0.08in grid."""
    issues = []
    left_edges = layout_signals.get("left_edges_in", [])
    top_edges = layout_signals.get("top_edges_in", [])
    grid = 0.08  # 4px in inches
    for which, edges in [("left", left_edges), ("top", top_edges)]:
        for i, e in enumerate(edges):
            # Only flag if far from grid AND there are enough points
            # to make the pattern meaningful (at least 2 points)
            if len(edges) < 2:
                break
            if abs(e - round(e / grid) * grid) > 0.02:
                issues.append({
                    "severity": "soft",
                    "dimension": "alignment",
                    "element": f"shape_{i}_{which}_edge",
                    "problem": f"元素 {which} 边缘 {e:.3f}in 未对齐到 {grid}in 网格",
                    "suggestion": f"吸附元素 {which} 边缘到最近的 0.08in 格点",
                    "auto_fixable": True,
                })
        if len(edges) < 2:
            break  # don't continue checking if we already broke
    return issues


def _check_color_palette(
    colors_used: dict[str, int],
    palette: list[str] | None,
) -> list[dict]:
    """Hard-check: all colors must be within palette (if provided)."""
    issues = []
    if palette is None or not palette:
        return issues
    # Normalize palette to uppercase without #
    palette_norm = {c.upper().lstrip("#") for c in palette}
    for color_hex in colors_used:
        ch = color_hex.upper().lstrip("#")
        if ch not in palette_norm:
            issues.append({
                "severity": "hard",
                "dimension": "color_harmony",
                "element": f"color_{ch}",
                "problem": f"颜色 #{ch} 不在指定调色板中",
                "suggestion": f"将 #{ch} 替换为调色板中最接近的颜色",
                "auto_fixable": True,
            })
    return issues


def _check_placeholder(text_blocks: list[dict]) -> list[dict]:
    """Hard-check for placeholder text patterns."""
    issues = []
    for tb in text_blocks:
        text = tb.get("text", "")
        if _PLACEHOLDER_PATTERNS.search(text):
            issues.append({
                "severity": "hard",
                "dimension": "hierarchy",
                "element": tb.get("shape_name", "(unknown)"),
                "problem": f"文本含占位符: {text[:60]}",
                "suggestion": "替换为实际内容",
                "auto_fixable": False,
            })
    return issues


def _check_completeness(
    text_blocks: list[dict],
    images: list[dict],
) -> list[dict]:
    """Soft-check: charts without data source, images without context."""
    issues = []
    full_text = " ".join(tb.get("text", "") for tb in text_blocks)

    # Check for missing data source mentions in chart-like slides
    chart_keywords = ["图表", "chart", "统计", "statistics", "distribution", "增长", "趋势"]
    source_keywords = ["数据来源", "来源", "data source", "source:", "源自"]
    has_chart_keyword = any(kw in full_text for kw in chart_keywords)
    has_source = any(kw in full_text for kw in source_keywords)
    if has_chart_keyword and not has_source:
        issues.append({
            "severity": "soft",
            "dimension": "hierarchy",
            "element": "page",
            "problem": "包含图表关键词但未注明数据来源",
            "suggestion": "添加数据来源标注",
            "auto_fixable": False,
        })

    # Check images with no alt text or context
    for img in images:
        bbox = img.get("bbox_in")
        if bbox and not img.get("stretch"):
            # Image without context — flag if no text nearby
            # For simplicity, flag if no text blocks reference the image
            has_nearby_label = False
            # We don't have spatial analysis here, so skip this heuristic
            pass

    return issues


def _check_type_scale_direct(layout_signals: dict) -> list[dict]:
    """Direct type_scale check from layout signals."""
    issues = []
    fs_range = layout_signals.get("font_size_range_pt")
    if fs_range and len(fs_range) == 2:
        fs_min, fs_max = fs_range[0], fs_range[1]
        if fs_min > 0 and fs_max / fs_min < 1.2:
            issues.append({
                "severity": "hard",
                "dimension": "type_scale",
                "element": "type_scale",
                "problem": (
                    f"标题/正文字号比 {fs_max}/{fs_min}={fs_max/fs_min:.2f} < 1.2，"
                    f"视觉层级不足"
                ),
                "suggestion": f"将标题字号提升至 {fs_min * 1.25:.0f}pt 以上",
                "auto_fixable": True,
            })
    return issues


def _check_color_balance(colors_used: dict[str, int]) -> list[dict]:
    """Soft 60-30-10 balance check."""
    issues = []
    all_colors = list(colors_used.keys())
    non_neutral = [h for h in all_colors if not _is_neutral_color(h)]
    if len(non_neutral) > 3:
        issues.append({
            "severity": "soft",
            "dimension": "color_harmony",
            "element": "color_balance",
            "problem": (
                f"使用了 {len(non_neutral)} 种非中性色，"
                f"建议控制在 1-2 种强调色"
            ),
            "suggestion": "减少非中性色数量至 1-2 种，遵循 60-30-10 法则",
            "auto_fixable": True,
        })
    return issues


# --------------------------------------------------------------------------- #
# Scoring engine
# --------------------------------------------------------------------------- #
DIMENSIONS = [
    "whitespace", "type_scale", "color_harmony", "alignment",
    "spacing", "imagery", "consistency", "hierarchy", "layout",
]


def _compute_slide_score(issues: list[dict]) -> tuple[float, dict[str, float]]:
    """Compute 0-10 score for one slide based on its issues.

    Each dimension starts at 10. Hard issues -2, soft issues -0.5.
    Clamp to 0-10, then average across all 9 dimensions.
    """
    dim_scores = {}
    for dim in DIMENSIONS:
        score = 10.0
        for iss in issues:
            if iss.get("dimension") != dim:
                continue
            if iss.get("severity") == "hard":
                score -= 2.0
            else:
                score -= 0.5
        dim_scores[dim] = max(0.0, score)
    avg = sum(dim_scores.values()) / len(dim_scores)
    return round(avg, 2), dim_scores


def _count_hard_soft(issues: list[dict]) -> tuple[int, int]:
    hard = sum(1 for i in issues if i.get("severity") == "hard")
    soft = sum(1 for i in issues if i.get("severity") == "soft")
    return hard, soft


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #
def critique_pptx(
    file_path: str,
    palette: list[str] | None = None,
) -> dict:
    """Analyze a PPTX file and return structured critique.

    Args:
        file_path: Path to the .pptx file.
        palette: Optional list of hex colors (with or without #) defining
                 the allowed palette.

    Returns:
        dict with keys: stage, file, overall_score, total_issues,
            hard_issues, soft_issues, converged, slides, dimension_scores.
    """
    pptx_path = Path(file_path)
    if not pptx_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    prs = Presentation(str(pptx_path))
    slide_w_in = prs.slide_width / EMU_PER_INCH
    slide_h_in = prs.slide_height / EMU_PER_INCH

    theme_major, theme_minor = _resolve_theme_fonts(prs)

    slides_output = []
    all_slide_scores = []
    all_dimension_scores: dict[str, list[float]] = {d: [] for d in DIMENSIONS}
    total_hard = 0
    total_soft = 0

    for idx, slide in enumerate(prs.slides):
        analysis = analyze_slide(
            slide, idx, slide_w_in, slide_h_in,
            theme_major_font=theme_major, theme_minor_font=theme_minor,
        )

        # --- Build issues from anti_patterns ---
        issues = _build_issues_from_anti_patterns(
            analysis.get("anti_patterns", [])
        )

        # --- Additional dimension checks ---
        layout_signals = analysis.get("layout_signals", {})
        text_blocks = analysis.get("text_blocks", [])
        colors_used = analysis.get("colors_used", {})
        images = analysis.get("images", [])

        # Alignment grid check (soft)
        issues.extend(_check_alignment(layout_signals))

        # Color palette check (hard if palette provided)
        issues.extend(_check_color_palette(colors_used, palette))

        # Placeholder check (hard)
        issues.extend(_check_placeholder(text_blocks))

        # Completeness check (soft)
        issues.extend(_check_completeness(text_blocks, images))

        # Direct type_scale check (hard) — may overlap with anti-pattern,
        # dedup handles that below
        issues.extend(_check_type_scale_direct(layout_signals))

        # Color balance check (soft)
        issues.extend(_check_color_balance(colors_used))

        # --- Deduplicate by problem text ---
        seen_problems: set[str] = set()
        deduped = []
        for iss in issues:
            key = iss["problem"]
            if key not in seen_problems:
                seen_problems.add(key)
                deduped.append(iss)
        issues = deduped

        # --- Score ---
        slide_score, dim_scores = _compute_slide_score(issues)
        hard, soft = _count_hard_soft(issues)

        all_slide_scores.append(slide_score)
        for d in DIMENSIONS:
            all_dimension_scores[d].append(dim_scores[d])

        total_hard += hard
        total_soft += soft

        slides_output.append({
            "slide": idx + 1,
            "score": slide_score,
            "hard_issues": hard,
            "soft_issues": soft,
            "issues": issues,
        })

    # --- Aggregate ---
    overall_score = (
        round(sum(all_slide_scores) / len(all_slide_scores), 2)
        if all_slide_scores else 0.0
    )
    dimension_scores = {
        d: round(sum(v) / len(v), 2) if v else 10.0
        for d, v in all_dimension_scores.items()
    }

    # converged: last slide has < 3 hard issues
    last_hard = slides_output[-1]["hard_issues"] if slides_output else 0
    converged = last_hard < 3

    return {
        "stage": "structural",
        "file": pptx_path.name,
        "overall_score": overall_score,
        "total_issues": total_hard + total_soft,
        "hard_issues": total_hard,
        "soft_issues": total_soft,
        "converged": converged,
        "slides": slides_output,
        "dimension_scores": dimension_scores,
    }


# --------------------------------------------------------------------------- #
# HTML critique
# --------------------------------------------------------------------------- #

# Regex patterns for HTML parsing
_RE_HEX_COLOR = re.compile(r"#([0-9A-Fa-f]{6})\b")
_RE_RGB_COLOR = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")
_RE_FONT_SIZE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)\s*(px|pt)", re.IGNORECASE)
_RE_LEFT = re.compile(r"(?:left|margin-left)\s*:\s*(-?\d+(?:\.\d+)?)\s*px", re.IGNORECASE)
_RE_TOP = re.compile(r"(?:top|margin-top)\s*:\s*(-?\d+(?:\.\d+)?)\s*px", re.IGNORECASE)
_RE_PLACEHOLDER_HTML = re.compile(
    r"\b(TODO|TBD|XXX|FIXME|HACK|占位|待补充|待定|Lorem\s+Ipsum|lorem\s+ipsum)\b",
    re.IGNORECASE,
)


def _normalize_color_hex(match_str: str, r: int = 0, g: int = 0, b: int = 0) -> str:
    """Normalize a color to uppercase 6-digit hex without #."""
    if match_str:
        return match_str.upper()
    return f"{r:02X}{g:02X}{b:02X}"


def _extract_colors_from_text(text: str) -> list[str]:
    """Extract all color values from a CSS/text string as uppercase hex (no #)."""
    colors = []
    for m in _RE_HEX_COLOR.finditer(text):
        colors.append(m.group(1).upper())
    for m in _RE_RGB_COLOR.finditer(text):
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        colors.append(f"{r:02X}{g:02X}{b:02X}")
    return colors


def _extract_font_sizes_from_text(text: str) -> list[float]:
    """Extract font-size values in pt from a CSS/text string."""
    sizes = []
    for m in _RE_FONT_SIZE.finditer(text):
        val = float(m.group(1))
        unit = m.group(2).lower()
        if unit == "px":
            val = val * 0.75  # px → pt (1px = 0.75pt at 96dpi)
        sizes.append(val)
    return sizes


def _extract_position_values(text: str) -> list[tuple[str, float]]:
    """Extract (property, value) pairs for left/top/margin-left/margin-top."""
    results = []
    for m in _RE_LEFT.finditer(text):
        results.append(("left", float(m.group(1))))
    for m in _RE_TOP.finditer(text):
        results.append(("top", float(m.group(1))))
    return results


def _check_html_alignment(soup: BeautifulSoup, slide_el, slide_idx: int) -> list[dict]:
    """Check 8px grid alignment for elements within a slide."""
    issues = []
    if soup is None:
        return issues
    elements = slide_el.find_all(attrs={"style": True}) if hasattr(slide_el, 'find_all') else []
    for i, el in enumerate(elements):
        style = el.get("style", "")
        if not style:
            continue
        pos_values = _extract_position_values(style)
        for prop, val in pos_values:
            if abs(val - round(val / 8) * 8) > 0.5:
                issues.append({
                    "severity": "soft",
                    "dimension": "alignment",
                    "element": f"slide_{slide_idx}_el_{i}_{prop}",
                    "problem": f"元素 {prop}={val}px 未对齐到 8px 网格",
                    "suggestion": f"将 {prop} 吸附到最近的 8px 格点 ({round(val / 8) * 8}px)",
                    "auto_fixable": True,
                })
    return issues


def _check_html_color(soup: BeautifulSoup, slide_el, slide_idx: int, palette: list[str] | None) -> list[dict]:
    """Check colors against palette (hard) and 60-30-10 balance (soft)."""
    issues = []
    if soup is None:
        return issues

    # Gather all style text from the slide element and its children
    style_texts = []
    if hasattr(slide_el, 'get'):
        style_texts.append(slide_el.get("style", ""))
    if hasattr(slide_el, 'find_all'):
        for child in slide_el.find_all(attrs={"style": True}):
            style_texts.append(child.get("style", ""))

    # Also check <style> tags within the document
    for style_tag in soup.find_all("style"):
        if style_tag.string:
            style_texts.append(style_tag.string)

    all_colors: list[str] = []
    for st in style_texts:
        all_colors.extend(_extract_colors_from_text(st))

    if not all_colors:
        return issues

    color_counts: Counter = Counter(all_colors)

    # Hard: off-palette colors
    if palette:
        palette_norm = {c.upper().lstrip("#") for c in palette}
        for color_hex in color_counts:
            if color_hex not in palette_norm:
                issues.append({
                    "severity": "hard",
                    "dimension": "color_harmony",
                    "element": f"color_{color_hex}",
                    "problem": f"颜色 #{color_hex} 不在指定调色板中",
                    "suggestion": f"将 #{color_hex} 替换为调色板中最接近的颜色",
                    "auto_fixable": True,
                })

    # Soft: 60-30-10 balance check
    non_neutral = [c for c in color_counts if not _is_neutral_color(c)]
    if len(non_neutral) > 3:
        issues.append({
            "severity": "soft",
            "dimension": "color_harmony",
            "element": "color_balance",
            "problem": f"使用了 {len(non_neutral)} 种非中性色，建议控制在 1-2 种强调色",
            "suggestion": "减少非中性色数量至 1-2 种，遵循 60-30-10 法则",
            "auto_fixable": True,
        })
    elif non_neutral:
        total = sum(color_counts.values())
        if total > 0:
            sorted_colors = sorted(non_neutral, key=lambda c: color_counts[c], reverse=True)
            dominant_pct = color_counts[sorted_colors[0]] / total * 100
            if dominant_pct > 70 and len(sorted_colors) >= 2:
                issues.append({
                    "severity": "soft",
                    "dimension": "color_harmony",
                    "element": "color_balance",
                    "problem": f"主色占比 {dominant_pct:.0f}%，60-30-10 比例偏移",
                    "suggestion": "调整色彩比例至 60% 主色 + 30% 辅色 + 10% 强调色",
                    "auto_fixable": True,
                })

    return issues


def _check_html_type_scale(soup: BeautifulSoup, slide_el, slide_idx: int) -> list[dict]:
    """Check font-size ratio < 1.2 (hard)."""
    issues = []
    if soup is None:
        return issues

    style_texts = []
    if hasattr(slide_el, 'get'):
        style_texts.append(slide_el.get("style", ""))
    if hasattr(slide_el, 'find_all'):
        for child in slide_el.find_all(attrs={"style": True}):
            style_texts.append(child.get("style", ""))
    for style_tag in soup.find_all("style"):
        if style_tag.string:
            style_texts.append(style_tag.string)

    all_sizes: list[float] = []
    for st in style_texts:
        all_sizes.extend(_extract_font_sizes_from_text(st))

    if len(all_sizes) >= 2:
        fs_min = min(all_sizes)
        fs_max = max(all_sizes)
        if fs_min > 0 and fs_max / fs_min < 1.2:
            issues.append({
                "severity": "hard",
                "dimension": "type_scale",
                "element": f"slide_{slide_idx}_type_scale",
                "problem": f"最大/最小字号比 {fs_max:.1f}/{fs_min:.1f}={fs_max/fs_min:.2f} < 1.2，视觉层级不足",
                "suggestion": f"将标题字号提升至 {fs_min * 1.25:.0f}pt 以上",
                "auto_fixable": True,
            })
    return issues


def _check_html_whitespace(slide_el, slide_idx: int, density_mode: str | None) -> list[dict]:
    """Check element count per slide (hard)."""
    issues = []
    mode = density_mode or "low"
    threshold = 8 if mode == "high" else 6
    # Count child elements that have style or visible content
    child_count = 0
    if hasattr(slide_el, 'find_all'):
        child_count = len(slide_el.find_all())
    if child_count > threshold:
        issues.append({
            "severity": "hard",
            "dimension": "whitespace",
            "element": f"slide_{slide_idx}_density",
            "problem": f"页面元素数 {child_count} 超过 {mode} 密度阈值 {threshold}",
            "suggestion": f"精简页面元素至 {threshold} 个以内",
            "auto_fixable": True,
        })
    return issues


def _check_html_hierarchy(soup: BeautifulSoup, slide_el, slide_idx: int) -> list[dict]:
    """Check for placeholder text (hard)."""
    issues = []
    if soup is None:
        return issues
    text_content = slide_el.get_text() if hasattr(slide_el, 'get_text') else ""
    if _RE_PLACEHOLDER_HTML.search(text_content):
        issues.append({
            "severity": "hard",
            "dimension": "hierarchy",
            "element": f"slide_{slide_idx}_placeholder",
            "problem": f"文本含占位符: {text_content[:60].strip()}",
            "suggestion": "替换为实际内容",
            "auto_fixable": False,
        })
    return issues


def _check_html_alignment_stage(soup: BeautifulSoup, html_text: str) -> list[dict]:
    """Check for 1920×1080 fixed stage and 16:9 aspect ratio (hard)."""
    issues = []
    has_1920 = bool(re.search(r"1920", html_text))
    has_1080 = bool(re.search(r"1080", html_text))
    has_aspect_169 = bool(re.search(r"aspect-ratio\s*:\s*16\s*/\s*9", html_text, re.IGNORECASE))
    has_transform_scale = bool(re.search(r"transform\s*:\s*scale\(", html_text, re.IGNORECASE))

    # Determine if a fixed-stage reference exists
    has_stage_dims = has_1920 and has_1080
    has_stage_ref = has_1920 or has_1080 or has_aspect_169

    if has_stage_dims:
        # Fixed dimensions present — check if ratio is 16:9
        ratio = 1920 / 1080
        if abs(ratio - 16 / 9) > 0.01:
            issues.append({
                "severity": "hard",
                "dimension": "alignment",
                "element": "stage",
                "problem": f"舞台宽高比 {ratio:.3f} 不等于 16:9 ({16 / 9:.3f})",
                "suggestion": "调整舞台宽高为 16:9 比例",
                "auto_fixable": True,
            })
    elif has_aspect_169:
        # Has aspect-ratio 16/9 — no fixed dims but ratio is fine
        pass
    else:
        # No fixed stage or aspect-ratio reference at all
        issues.append({
            "severity": "hard",
            "dimension": "alignment",
            "element": "stage",
            "problem": "未检测到 1920×1080 固定舞台或 16:9 宽高比",
            "suggestion": "添加 1920×1080 固定尺寸舞台或 aspect-ratio: 16/9",
            "auto_fixable": True,
        })
        if not has_transform_scale:
            issues.append({
                "severity": "hard",
                "dimension": "alignment",
                "element": "scale",
                "problem": "未检测到 transform scale 缩放适配",
                "suggestion": "添加 transform: scale() 实现响应式缩放",
                "auto_fixable": True,
            })

    return issues


def _check_html_imagery(soup: BeautifulSoup, slide_el, slide_idx: int) -> list[dict]:
    """Check img without alt (soft), charts without caption (soft)."""
    issues = []
    if soup is None:
        return issues

    # img without alt
    if hasattr(slide_el, 'find_all'):
        for i, img in enumerate(slide_el.find_all("img")):
            if not img.get("alt"):
                issues.append({
                    "severity": "soft",
                    "dimension": "imagery",
                    "element": f"slide_{slide_idx}_img_{i}",
                    "problem": "img 标签缺少 alt 属性",
                    "suggestion": "添加描述性 alt 属性",
                    "auto_fixable": False,
                })

        # table/canvas/svg without caption
        chart_tags = slide_el.find_all(["table", "canvas", "svg"])
        for i, chart in enumerate(chart_tags):
            tag_name = chart.name if hasattr(chart, 'name') else str(type(chart))
            # Check if there's a <figcaption> or nearby caption text
            parent = chart.parent if hasattr(chart, 'parent') else None
            has_caption = False
            if parent and hasattr(parent, 'find'):
                if parent.find("figcaption") or parent.find("caption"):
                    has_caption = True
            if not has_caption:
                # Check if the previous sibling has caption-like text
                prev = chart.find_previous_sibling()
                if prev and hasattr(prev, 'get') and prev.get("class"):
                    classes = prev.get("class", [])
                    if isinstance(classes, list) and any("caption" in c.lower() for c in classes):
                        has_caption = True
            if not has_caption:
                issues.append({
                    "severity": "soft",
                    "dimension": "hierarchy",
                    "element": f"slide_{slide_idx}_{tag_name}_{i}",
                    "problem": f"{tag_name} 元素缺少 caption 标注",
                    "suggestion": "为图表添加说明文字或 <figcaption>",
                    "auto_fixable": False,
                })

    return issues


def critique_html(
    file_path: str,
    density_mode: str | None = None,
    palette: list[str] | None = None,
) -> dict:
    """Analyze an HTML file and return structured critique.

    Args:
        file_path: Path to the .html file.
        density_mode: "low" (threshold=6) or "high" (threshold=8).
                     None defaults to "low".
        palette: Optional list of hex colors defining the allowed palette.

    Returns:
        dict with same structure as critique_pptx.
    """
    if BeautifulSoup is None:
        raise ImportError("beautifulsoup4 is required for HTML critique. Install with: pip install beautifulsoup4")

    html_path = Path(file_path)
    if not html_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    html_text = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_text, "html.parser")

    # Find slides: elements with class "slide" or data-slide attribute
    slides_html = soup.find_all(class_="slide")
    if not slides_html:
        slides_html = soup.find_all(attrs={"data-slide": True})
    if not slides_html:
        # Treat the whole document as a single slide
        slides_html = [soup]

    slides_output = []
    all_slide_scores = []
    all_dimension_scores: dict[str, list[float]] = {d: [] for d in DIMENSIONS}
    total_hard = 0
    total_soft = 0

    # Stage-fit is a global check (applies to the whole document)
    stage_issues = _check_html_alignment_stage(soup, html_text)

    for idx, slide_el in enumerate(slides_html):
        issues = []

        # Per-slide checks
        issues.extend(_check_html_alignment(soup, slide_el, idx))
        issues.extend(_check_html_color(soup, slide_el, idx, palette))
        issues.extend(_check_html_type_scale(soup, slide_el, idx))
        issues.extend(_check_html_whitespace(slide_el, idx, density_mode))
        issues.extend(_check_html_hierarchy(soup, slide_el, idx))
        issues.extend(_check_html_imagery(soup, slide_el, idx))

        # Add global stage_fit issues to the first slide only
        if idx == 0:
            issues.extend(stage_issues)

        # Deduplicate by problem text
        seen_problems: set[str] = set()
        deduped = []
        for iss in issues:
            key = iss["problem"]
            if key not in seen_problems:
                seen_problems.add(key)
                deduped.append(iss)
        issues = deduped

        # Score
        slide_score, dim_scores = _compute_slide_score(issues)
        hard, soft = _count_hard_soft(issues)

        all_slide_scores.append(slide_score)
        for d in DIMENSIONS:
            all_dimension_scores[d].append(dim_scores[d])

        total_hard += hard
        total_soft += soft

        slides_output.append({
            "slide": idx + 1,
            "score": slide_score,
            "hard_issues": hard,
            "soft_issues": soft,
            "issues": issues,
        })

    # Aggregate
    overall_score = (
        round(sum(all_slide_scores) / len(all_slide_scores), 2)
        if all_slide_scores else 0.0
    )
    dimension_scores = {
        d: round(sum(v) / len(v), 2) if v else 10.0
        for d, v in all_dimension_scores.items()
    }

    last_hard = slides_output[-1]["hard_issues"] if slides_output else 0
    converged = last_hard < 3

    return {
        "stage": "structural",
        "file": html_path.name,
        "overall_score": overall_score,
        "total_issues": total_hard + total_soft,
        "hard_issues": total_hard,
        "soft_issues": total_soft,
        "converged": converged,
        "slides": slides_output,
        "dimension_scores": dimension_scores,
    }


# --------------------------------------------------------------------------- #
# Unified entry point
# --------------------------------------------------------------------------- #
def critique(file_path: str, file_type: str | None = None, **kwargs) -> dict:
    """Auto-detect file type and call the appropriate critique function.

    Args:
        file_path: Path to the file.
        file_type: "pptx", "html", or None (auto-detect by extension).
        **kwargs: Passed to the underlying critique function.

    Returns:
        dict with the same structure as critique_pptx / critique_html.
    """
    if file_type is None:
        ext = Path(file_path).suffix.lower()
        file_type = "pptx" if ext == ".pptx" else "html" if ext == ".html" else "unknown"
    if file_type == "pptx":
        return critique_pptx(file_path, **kwargs)
    elif file_type == "html":
        return critique_html(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    import argparse
    ap = argparse.ArgumentParser(description="PPTX & HTML 结构化检测引擎")
    ap.add_argument("file_path", help="文件路径 (.pptx 或 .html)")
    ap.add_argument("--palette", "-p", default=None,
                    help="调色板颜色列表，逗号分隔 (如 #D8000F,#1C1410)")
    ap.add_argument("--density-mode", "-d", default=None, choices=["low", "high"],
                    help="密度模式: low (阈值6) 或 high (阈值8)，仅对 HTML 有效")
    ap.add_argument("--output", "-o", default=None,
                    help="输出 JSON 文件路径")
    args = ap.parse_args()

    # Parse palette
    palette = None
    if args.palette:
        palette = [c.strip() for c in args.palette.split(",") if c.strip()]

    # Build kwargs
    kwargs = {}
    if palette:
        kwargs["palette"] = palette
    if args.density_mode:
        kwargs["density_mode"] = args.density_mode

    result = critique(args.file_path, **kwargs)
    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    print(json_str)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json_str, encoding="utf-8")
        print(f"\nReport saved to: {out_path}")


if __name__ == "__main__":
    main()
