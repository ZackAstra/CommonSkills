#!/usr/bin/env python3
"""
中国电信央企风格PPT生成器
基于天翼AI产品营销推广训练营汇报模板，生成符合电信央企风格的PPT

用法:
  python ct_ppt_gen.py --outline outline.json [--style government|marketing|party] [--output output.pptx]

outline.json 格式:
{
  "title": "PPT主标题",
  "subtitle": "副标题（组名/部门）",
  "date": "2026年5月",
  "sections": [
    {
      "title": "一、产品理解",
      "items": ["要点1", "要点2"],
      "notes": "备注内容"
    }
  ]
}
"""

import json
import sys
import os
import copy
import re
from pathlib import Path

# 模板路径
SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR.parent / "assets"
TEMPLATE_PATH = ASSETS_DIR / "ct-template.pptx"

# 配色方案定义
COLOR_SCHEMES = {
    "government": {
        "name": "正式汇报/政企方案",
        "primary": "0077BE",       # 电信深蓝
        "accent": "3399D6",        # 浅蓝渐变
        "text_dark": "333333",     # 深灰文字
        "bg_light": "F5F7FA",      # 浅灰底色
        "white": "FFFFFF",
        "section_num_bg": "0077BE", # 章节号背景
        "section_bar_bg": "0077BE", # 章节条背景
    },
    "marketing": {
        "name": "数字化/云网/算力/AI",
        "primary": "0077BE",
        "accent": "3399D6",
        "text_dark": "333333",
        "bg_light": "F5F7FA",
        "white": "FFFFFF",
        "section_num_bg": "0077BE",
        "section_bar_bg": "0077BE",
    },
    "party": {
        "name": "党建/合规/企业文化",
        "primary": "0077BE",
        "red_accent": "C00000",     # 正红点缀
        "text_dark": "333333",
        "bg_light": "FFF8F0",       # 米白
        "white": "FFFFFF",
        "section_num_bg": "C00000", # 章节号背景用红
        "section_bar_bg": "C00000",
    }
}

# 中文数字映射
CN_NUMS = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]


def get_cn_num(index):
    """获取中文数字（从1开始）"""
    if 1 <= index <= 10:
        return CN_NUMS[index]
    return str(index)


def hex_to_rgb(hex_color):
    """将16进制颜色转为RGB元组"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    """将RGB转为16进制颜色"""
    return f"{r:02X}{g:02X}{b:02X}"


def parse_outline(outline_path):
    """解析大纲JSON文件"""
    with open(outline_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def validate_outline(data):
    """验证大纲数据完整性"""
    required = ["title", "sections"]
    for key in required:
        if key not in data:
            raise ValueError(f"大纲缺少必填字段: {key}")
    if not data["sections"]:
        raise ValueError("sections不能为空")
    for i, sec in enumerate(data["sections"]):
        if "title" not in sec:
            raise ValueError(f"第{i+1}个section缺少title")
    return True


def build_outline_json(data, style="government"):
    """
    根据大纲数据生成完整的内容映射
    返回结构: {slide_index: {shape_index: paragraphs}}
    """
    scheme = COLOR_SCHEMES.get(style, COLOR_SCHEMES["government"])
    sections = data["sections"]
    num_sections = len(sections)

    # 构建幻灯片序列: 封面 → 目录 → (章节标题页 → 内容页...)...
    # 模板结构: slide0=封面, slide1=目录, slide2=章节标题页
    # 对于N个section: 1封面 + 1目录 + N*(1目录+1章节) - 但实际模板每section有目录页+标题页

    result = {
        "meta": {
            "title": data.get("title", "汇报材料"),
            "subtitle": data.get("subtitle", ""),
            "date": data.get("date", ""),
            "style": style,
            "num_sections": num_sections,
            "sections": sections,
            "scheme": scheme,
            "slide_mapping": []  # 决定用模板的哪些slide
        }
    }

    return result


def generate_replacement_data(data, style="government"):
    """
    生成模板替换数据（供pptx skill的replace.py使用）
    
    模板7页结构:
      slide-0: 封面 (shape-0=标题, shape-1=组名+日期)
      slide-1: 目录 (shape-0=目 录, shape-1=CONTENTS, shape-2~7=三个目录条目)
      slide-2: 章节标题页 (shape-0=章节标题, shape-1=描述)
      slide-3: 目录 (同slide-1)
      slide-4: 章节标题页 (同slide-2)
      slide-5: 目录 (同slide-1)
      slide-6: 章节标题页 (同slide-2)
    """
    scheme = COLOR_SCHEMES.get(style, COLOR_SCHEMES["government"])
    sections = data["sections"]
    num_sections = len(sections)
    
    result = {}
    
    # === Slide 0: 封面 ===
    result["slide-0"] = {
        "shape-0": {
            "paragraphs": [
                {
                    "text": data.get("title", "汇报材料"),
                    "alignment": "CENTER",
                    "font_name": "微软雅黑",
                    "font_size": 44.0,
                    "bold": True,
                    "color": scheme.get("section_num_bg", "0077BE"),
                    "line_spacing": 66.0
                }
            ]
        },
        "shape-1": {
            "paragraphs": [
                {
                    "text": data.get("subtitle", ""),
                    "alignment": "CENTER",
                    "font_name": "华文细黑",
                    "font_size": 21.35,
                    "bold": True,
                    "theme_color": "BACKGROUND_1"
                },
                {
                    "text": data.get("date", ""),
                    "alignment": "CENTER",
                    "font_name": "华文细黑",
                    "font_size": 21.35,
                    "bold": True,
                    "theme_color": "BACKGROUND_1"
                }
            ]
        }
    }
    
    # === 生成目录页和章节标题页 ===
    # 构建 rearrange 的slide映射
    # 模板: 0=封面, 1=目录, 2=章节标题页
    # 需要: 封面 + 目录 + (章节标题页)*N
    # 如果section > 3，目录需要特殊处理
    
    # 最多支持3个section的目录（模板限制）
    # 如果超过3个section，后续section复用目录页但只显示前3个
    max_toc_sections = min(num_sections, 3)
    
    # 目录页替换（slide-1）
    toc_shape = {}
    # 目录标题保持
    toc_shape["shape-0"] = {
        "paragraphs": [
            {
                "text": "目 录",
                "font_name": "Times New Roman",
                "font_size": 44.8,
                "bold": True,
                "color": scheme.get("section_num_bg", "0077BE"),
                "line_spacing": 44.8
            }
        ]
    }
    toc_shape["shape-1"] = {
        "paragraphs": [
            {
                "text": "CONTENTS",
                "font_name": "Times New Roman",
                "font_size": 22.4,
                "color": scheme.get("section_num_bg", "0077BE"),
                "line_spacing": 22.4
            }
        ]
    }
    
    # 目录条目
    for i in range(max_toc_sections):
        num_shape_idx = 2 + i * 2  # shape-2, shape-4, shape-6
        name_shape_idx = 3 + i * 2  # shape-3, shape-5, shape-7
        
        section_title = sections[i]["title"]
        # 提取章节号
        cn_num = get_cn_num(i + 1)
        
        toc_shape[f"shape-{num_shape_idx}"] = {
            "paragraphs": [
                {
                    "text": cn_num,
                    "alignment": "RIGHT",
                    "font_name": "Times New Roman",
                    "font_size": 20.0,
                    "bold": True,
                    "line_spacing": 20.0
                }
            ]
        }
        toc_shape[f"shape-{name_shape_idx}"] = {
            "paragraphs": [
                {
                    "text": section_title.replace(f"{cn_num}、", "").replace("一、", "").replace("二、", "").replace("三、", ""),
                    "alignment": "CENTER",
                    "font_name": "微软雅黑" if i == max_toc_sections - 1 else "Times New Roman",
                    "bold": True,
                    "line_spacing": 12.0
                }
            ]
        }
    
    # 超过3个section时的处理：只显示前3个
    if num_sections <= 3:
        result["slide-1"] = toc_shape
    else:
        # 对于多于3个section的情况，保留目录只显示前3个
        result["slide-1"] = toc_shape

    # 章节标题页替换
    # rearrange后的slide序列: 0(封面), 1(目录), 2(章节1), 3(章节2), 4(章节3), ...
    # 所以章节slide索引 = 2 + i
    for i, section in enumerate(sections):
        slide_key = f"slide-{2 + i}"
        
        section_title = section["title"]
        section_desc = section.get("notes", section.get("items", []))
        if isinstance(section_desc, list):
            section_desc = "，".join(section_desc)
        
        result[slide_key] = {
            "shape-0": {
                "paragraphs": [
                    {
                        "text": section_title,
                        "bold": True
                    }
                ]
            },
            "shape-1": {
                "paragraphs": [
                    {
                        "text": section_desc[:60] if len(section_desc) > 60 else section_desc
                    }
                ]
            }
        }
    
    return result


def generate_rearrange_args(data):
    """
    生成rearrange.py所需的slide映射参数
    
    模板slide索引(0-based):
      0 = 封面
      1 = 目录页
      2 = 章节标题页
    
    生成映射: 0(封面) + 1(目录) + 2*(章节标题页)*N
    """
    num_sections = len(data["sections"])
    
    # 封面 + 目录 + N个章节标题页
    mapping = [0, 1]
    for i in range(num_sections):
        mapping.append(2)  # 每次复用slide-2（章节标题页）
    
    return mapping


def generate_pptx(data, style, output_path, skill_pptx_dir=None):
    """
    主生成函数：基于模板生成完整PPT
    
    流程:
    1. 确定模板路径
    2. 生成rearrange参数 → 调用rearrange.py
    3. 生成inventory → 调用inventory.py
    4. 生成replacement JSON → 调用replace.py
    5. 输出最终PPTX
    """
    if skill_pptx_dir is None:
        # 尝试查找pptx skill目录
        possible_paths = [
            Path.home() / ".config" / "teleai-super-agent" / "skills" / "pptx",
            Path(__file__).parent.parent.parent / "pptx",
        ]
        for p in possible_paths:
            if p.exists():
                skill_pptx_dir = p
                break
        else:
            raise FileNotFoundError("找不到pptx skill目录，请通过 --pptx-dir 指定")
    
    skill_pptx_dir = Path(skill_pptx_dir)
    template_path = TEMPLATE_PATH
    rearrange_script = skill_pptx_dir / "scripts" / "rearrange.py"
    inventory_script = skill_pptx_dir / "scripts" / "inventory.py"
    replace_script = skill_pptx_dir / "scripts" / "replace.py"
    
    # 验证脚本存在
    for script_path in [rearrange_script, inventory_script, replace_script]:
        if not script_path.exists():
            raise FileNotFoundError(f"缺少必要脚本: {script_path}")
    
    import subprocess
    
    # 确保子进程使用UTF-8编码（Windows默认GBK会导致JSON读取失败）
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    # 步骤1: Rearrange
    mapping = generate_rearrange_args(data)
    mapping_str = ",".join(str(x) for x in mapping)
    
    working_path = Path(output_path).parent / ".temp" / "working.pptx"
    working_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[1/4] Rearranging slides: {mapping_str}")
    result = subprocess.run(
        [sys.executable, str(rearrange_script), str(template_path), str(working_path), mapping_str],
        capture_output=True, text=True, encoding="utf-8", env=env
    )
    if result.returncode != 0:
        print(f"Rearrange error: {result.stderr}")
        raise RuntimeError(f"rearrange.py执行失败: {result.stderr}")
    
    # 步骤2: Inventory
    inventory_path = Path(output_path).parent / ".temp" / "inventory.json"
    print(f"[2/4] Extracting inventory")
    result = subprocess.run(
        [sys.executable, str(inventory_script), str(working_path), str(inventory_path)],
        capture_output=True, text=True, encoding="utf-8", env=env
    )
    if result.returncode != 0:
        print(f"Inventory error: {result.stderr}")
        raise RuntimeError(f"inventory.py执行失败: {result.stderr}")
    
    # 步骤3: Generate replacement JSON
    replacement_data = generate_replacement_data(data, style)
    replacement_path = Path(output_path).parent / ".temp" / "replacement.json"
    with open(replacement_path, "w", encoding="utf-8", newline="") as f:
        json.dump(replacement_data, f, ensure_ascii=False, indent=2)
    print(f"[3/4] Generated replacement JSON ({len(replacement_data)} slides)")
    
    # 步骤4: Replace
    print(f"[4/4] Applying replacements")
    result = subprocess.run(
        [sys.executable, str(replace_script), str(working_path), str(replacement_path), str(output_path)],
        capture_output=True, text=True, encoding="utf-8", env=env
    )
    if result.returncode != 0:
        print(f"Replace error: {result.stderr}")
        raise RuntimeError(f"replace.py执行失败: {result.stderr}")
    
    print(f"✅ PPTX generated: {output_path}")
    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="中国电信央企风格PPT生成器")
    parser.add_argument("--outline", required=True, help="大纲JSON文件路径")
    parser.add_argument("--style", default="government", choices=["government", "marketing", "party"],
                        help="风格: government(汇报), marketing(科技), party(党建)")
    parser.add_argument("--output", default=None, help="输出PPTX文件路径")
    parser.add_argument("--pptx-dir", default=None, help="pptx skill目录路径")
    
    # 仅生成replacement JSON模式
    parser.add_argument("--json-only", action="store_true", help="仅输出replacement JSON到stdout")
    parser.add_argument("--rearrange-only", action="store_true", help="仅输出rearrange参数到stdout")
    
    args = parser.parse_args()
    
    # 解析大纲
    data = parse_outline(args.outline)
    validate_outline(data)
    
    if args.rearrange_only:
        mapping = generate_rearrange_args(data)
        print(",".join(str(x) for x in mapping))
        return
    
    if args.json_only:
        replacement_data = generate_replacement_data(data, args.style)
        print(json.dumps(replacement_data, ensure_ascii=False, indent=2))
        return
    
    # 完整生成
    output = args.output or f"{data.get('title', 'output')}.pptx"
    generate_pptx(data, args.style, output, args.pptx_dir)


if __name__ == "__main__":
    main()
