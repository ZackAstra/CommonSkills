# -*- coding: utf-8 -*-
"""gen_illustrations.py — ImageGen 后处理脚本

职责：Agent 调用 ImageGen 生成图片后，本脚本对指定目录中的原始 PNG 进行后处理：
  1. 检测并裁剪白边（ImageGen 常产出 2048×2048 含大面积白边的图）
  2. 按配置表重命名为约定格式（如 02_timeline.png）
  3. 输出处理报告

使用方式：
  python gen_illustrations.py <input_dir> [--config config.json] [--output-dir output_dir]

Agent 工作流：
  1. Agent 调用 ImageGen → 产出 raw image1.png, image2.png ... 到 input_dir
  2. Agent 编写 config.json 指定每张图的页号和类型
  3. 本脚本读取 config + 目录中的 PNG，裁剪白边 + 重命名 → output_dir

config.json 格式：
  [
    {"source": "image1.png", "slide": 2,  "type": "timeline"},
    {"source": "image2.png", "slide": 6,  "type": "staircase"},
    {"source": "image3.png", "slide": 10, "type": "skill_structure"},
    ...
  ]
  若 source 字段缺失，则按目录中 PNG 文件的修改时间顺序与 config 条目一一对应。

也可不传 config，脚本将所有 PNG 按修改时间排序输出为 raw_01.png, raw_02.png ...
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops
except ImportError:
    print("ERROR: Pillow is required.  pip install Pillow", file=sys.stderr)
    sys.exit(1)


# ── White-border detection and cropping ──

def _is_whiteish(pixel, threshold=245):
    """Check if a pixel is close to white."""
    return all(c >= threshold for c in pixel[:3])


def detect_content_bbox(img, threshold=245, margin=5):
    """Detect the bounding box of non-white content in an image.
    
    Returns (left, top, right, bottom) in pixel coordinates,
    or None if the entire image appears white.
    """
    if img.mode == "RGBA":
        # Convert to RGB for white detection (ignore alpha)
        rgb = img.convert("RGB")
    else:
        rgb = img

    width, height = rgb.size
    pixels = rgb.load()

    left, top = width, height
    right, bottom = 0, 0

    # Sample every 2nd pixel for speed on large images
    step = 2 if width * height > 500_000 else 1
    
    for y in range(0, height, step):
        for x in range(0, width, step):
            if not _is_whiteish(pixels[x, y], threshold):
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if right <= left or bottom <= top:
        return None  # Entirely white

    # Expand to include the sampled-but-skipped pixels
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(width - 1, right + step + margin)
    bottom = min(height - 1, bottom + step + margin)

    return (left, top, right, bottom)


def crop_white_border(img, threshold=245, margin=5, min_crop_ratio=0.05,
                      max_aspect_ratio=3.5):
    """Crop white border from image. Returns (cropped_image, crop_info).
    
    crop_info: {
        'original_size': (w, h),
        'content_bbox': (left, top, right, bottom) or None,
        'cropped_size': (w, h),
        'white_removed_pct': float,  # percentage of area removed
        'aspect_guard_applied': bool,  # whether aspect ratio guard triggered
        'pre_guard_size': (w, h) or None,  # size before aspect guard padding
    }
    
    max_aspect_ratio: maximum allowed width/height ratio after cropping.
        If the cropped image exceeds this ratio (e.g. a narrow horizontal
        strip like a timeline), white padding is added vertically to bring
        the aspect ratio within bounds. Default 3.5 means max 3.5:1.
        Set to 0 or None to disable.
    """
    orig_w, orig_h = img.size
    bbox = detect_content_bbox(img, threshold, margin)
    
    if bbox is None:
        return img, {
            'original_size': (orig_w, orig_h),
            'content_bbox': None,
            'cropped_size': (orig_w, orig_h),
            'white_removed_pct': 0.0,
            'aspect_guard_applied': False,
            'pre_guard_size': None,
        }
    
    left, top, right, bottom = bbox
    content_area = (right - left) * (bottom - top)
    orig_area = orig_w * orig_h
    removed_pct = round((1 - content_area / orig_area) * 100, 1)

    # Skip crop if less than min_crop_ratio of area is white border
    if removed_pct < min_crop_ratio:
        return img, {
            'original_size': (orig_w, orig_h),
            'content_bbox': bbox,
            'cropped_size': (orig_w, orig_h),
            'white_removed_pct': removed_pct,
            'aspect_guard_applied': False,
            'pre_guard_size': None,
        }

    cropped = img.crop((left, top, right + 1, bottom + 1))
    pre_guard_size = None
    aspect_guard_applied = False

    # Aspect ratio guard: if cropped image is too wide/flat, pad vertically
    if max_aspect_ratio and max_aspect_ratio > 0:
        cw, ch = cropped.size
        current_ratio = cw / ch
        if current_ratio > max_aspect_ratio:
            # Calculate required height to meet max_aspect_ratio
            target_h = int(round(cw / max_aspect_ratio))
            if target_h > ch:
                # Center the content vertically on a white canvas
                from PIL import Image as _Img
                padded = _Img.new(img.mode, (cw, target_h), (255, 255, 255))
                paste_y = (target_h - ch) // 2
                padded.paste(cropped, (0, paste_y))
                pre_guard_size = (cw, ch)
                cropped = padded
                aspect_guard_applied = True
                # Recalculate: padded image may be larger than original,
                # clamp removed_pct to 0 (negative values are confusing)
                padded_area = cw * target_h
                removed_pct = max(0.0, round((1 - padded_area / orig_area) * 100, 1))

    return cropped, {
        'original_size': (orig_w, orig_h),
        'content_bbox': bbox,
        'cropped_size': cropped.size,
        'white_removed_pct': removed_pct,
        'aspect_guard_applied': aspect_guard_applied,
        'pre_guard_size': pre_guard_size,
    }


# ── Config handling ──

def load_pngs_sorted(directory):
    """Load all PNG files in directory sorted by modification time (oldest first)."""
    pngs = sorted(
        Path(directory).glob("*.png"),
        key=lambda p: p.stat().st_mtime,
    )
    return pngs


def match_config_to_files(config, png_files):
    """Match config entries to actual PNG files.
    
    If config has 'source' field, match by filename.
    Otherwise, match by order (config[i] → png_files[i]).
    """
    matched = []
    file_index = {p.name: p for p in png_files}
    used_files = set()
    
    # First pass: match by source filename
    for entry in config:
        source = entry.get("source")
        if source and source in file_index:
            matched.append((file_index[source], entry))
            used_files.add(source)
    
    # Second pass: remaining entries get files by order
    remaining_files = [p for p in png_files if p.name not in used_files]
    remaining_entries = [e for e in config if not e.get("source") or e.get("source") not in file_index]
    
    for png_path, entry in zip(remaining_files, remaining_entries):
        matched.append((png_path, entry))
    
    return matched


# ── Output naming ──

def target_filename(entry, index):
    """Generate target filename from config entry.
    
    Format: {slide:02d}_{type}.png  or  raw_{index:02d}.png
    """
    slide = entry.get("slide")
    illu_type = entry.get("type", "illu")
    
    if slide is not None:
        return f"{int(slide):02d}_{illu_type}.png"
    else:
        return f"raw_{index:02d}.png"


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Post-process ImageGen PNGs: crop white borders and rename."
    )
    parser.add_argument("input_dir", help="Directory containing raw ImageGen PNGs")
    parser.add_argument("--config", help="JSON config file mapping images to slides")
    parser.add_argument("--output-dir", help="Output directory (default: input_dir/cropped)")
    parser.add_argument("--threshold", type=int, default=245,
                        help="White pixel threshold 0-255 (default: 245)")
    parser.add_argument("--margin", type=int, default=8,
                        help="Pixel margin around detected content (default: 8)")
    parser.add_argument("--min-crop", type=float, default=3.0,
                        help="Minimum %% of white area to trigger crop (default: 3)")
    parser.add_argument("--max-aspect-ratio", type=float, default=3.5,
                        help="Max width/height ratio after crop; pads white if exceeded (default: 3.5, 0 to disable)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without writing files")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"ERROR: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else input_dir / "cropped"
    
    # Load PNGs
    png_files = load_pngs_sorted(input_dir)
    if not png_files:
        print(f"No PNG files found in {input_dir}")
        sys.exit(0)
    
    print(f"Found {len(png_files)} PNG file(s) in {input_dir}")

    # Load config if provided
    config = None
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"Loaded config with {len(config)} entries from {args.config}")

    # Match config to files
    if config:
        matched = match_config_to_files(config, png_files)
    else:
        matched = [(p, {}) for p in png_files]
    
    # Process each pair
    report = []
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, (png_path, entry) in enumerate(matched):
        img = Image.open(png_path)
        img.load()  # Ensure fully loaded before potential crop
        
        cropped, info = crop_white_border(img, args.threshold, args.margin, args.min_crop,
                                          args.max_aspect_ratio)
        
        out_name = target_filename(entry, idx + 1)
        out_path = output_dir / out_name
        
        info['source_file'] = png_path.name
        info['target_file'] = out_name
        
        if not args.dry_run:
            cropped.save(out_path, "PNG")
            info['saved'] = True
        else:
            info['saved'] = False
        
        report.append(info)
        
        crop_pct = info['white_removed_pct']
        status = f"cropped {crop_pct}% white" if crop_pct >= args.min_crop else "no significant white border"
        guard_msg = ""
        if info.get('aspect_guard_applied'):
            pg = info['pre_guard_size']
            guard_msg = f"  [ASPECT-GUARD: {pg[0]}x{pg[1]} -> padded to {info['cropped_size'][0]}x{info['cropped_size'][1]}]"
        print(f"  {png_path.name} -> {out_name}  "
              f"({info['original_size'][0]}x{info['original_size'][1]} -> "
              f"{info['cropped_size'][0]}x{info['cropped_size'][1]})  {status}{guard_msg}")

    # Summary
    total_cropped = sum(1 for r in report if r['white_removed_pct'] >= args.min_crop)
    total_guarded = sum(1 for r in report if r.get('aspect_guard_applied'))
    total_area_saved = sum(
        max(0, r['original_size'][0] * r['original_size'][1] - r['cropped_size'][0] * r['cropped_size'][1])
        for r in report
    )
    print(f"\nSummary: {len(report)} images processed, {total_cropped} cropped, "
          f"{total_guarded} aspect-guard padded")
    print(f"Total area saved: {total_area_saved:,} pixels")
    
    # Write report JSON
    report_path = output_dir / "gen_report.json"
    if not args.dry_run:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
