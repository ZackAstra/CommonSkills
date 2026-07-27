# -*- coding: utf-8 -*-
"""
将层级结构的 Markdown 文件转换为 XMind 2020+ 格式文件 (.xmind)。

特性：
- 支持 # ~ ###### 六级标题（6级自动映射为5级）
- 非标题行自动聚合为上一个标题节点的 notes
- 自动过滤 AIGC 水印行（> AI生成）
- 蓝色系主题、微软雅黑字体、圆角矩形、曲线连接线
- 三级旗帜标识：flag-blue(主题) / flag-yellow(章节) / flag-green(子节)
- 深层叶子节点自动折叠
- unbalanced 布局：左右均衡，右侧 N 个、左侧剩余，左侧自动反序保证从上到下 1->N

用法：
  python md2xmind.py <input.md> <output.xmind> [--right N] [--theme blue|green|red]

参数：
  --right N   右侧分支数，默认取总分支数的一半（向上取整）
  --theme     主题色，默认 blue
"""

import re
import uuid
import json
import zipfile
import argparse


def gen_id():
    return str(uuid.uuid4())


# ---- 主题定义 ----

THEMES = {
    "blue": {
        "subTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "line-width": "1pt",
                "line-color": "#558ED5",
                "border-line-color": "#558ED5",
                "border-line-width": "3pt",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "summary": {
            "id": gen_id(),
            "properties": {
                "line-width": "5pt",
                "line-color": "#C3D69B",
                "shape-class": "org.xmind.summaryShape.square"
            }
        },
        "boundary": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "10pt",
                "fo:font-style": "italic",
                "fo:color": "#FFFFFF",
                "svg:fill": "#C3D69B",
                "svg:opacity": ".2",
                "line-width": "3pt",
                "line-color": "#77933C",
                "line-pattern": "dot",
                "shape-class": "org.xmind.boundaryShape.roundedRect"
            }
        },
        "calloutTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "svg:fill": "#FBF09C",
                "border-line-color": "#F1BD51",
                "border-line-width": "2pt"
            }
        },
        "centralTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:color": "#376092",
                "svg:fill": "#DCE6F2",
                "line-width": "1pt",
                "line-color": "#558ED5",
                "border-line-color": "#558ED5",
                "border-line-width": "5pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "mainTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:color": "#17375E",
                "svg:fill": "#DCE6F2",
                "line-width": "1pt",
                "line-color": "#558ED5",
                "border-line-color": "#558ED5",
                "border-line-width": "2pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "summaryTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "10pt",
                "fo:font-style": "italic",
                "fo:color": "#FFFFFF",
                "svg:fill": "#77933C",
                "border-line-width": "0pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "floatingTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:font-weight": "bold",
                "fo:color": "#FFFFFF",
                "svg:fill": "#558ED5",
                "line-color": "#558ED5",
                "border-line-width": "0pt"
            }
        },
        "relationship": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:font-size": "10pt",
                "fo:font-weight": "normal",
                "fo:font-style": "italic",
                "fo:color": "#595959",
                "fo:text-decoration": "none",
                "line-width": "3pt",
                "line-color": "#77933C",
                "line-pattern": "dash",
                "arrow-end-class": "org.xmind.arrowShape.triangle"
            }
        },
        "map": {
            "id": gen_id(),
            "properties": {
                "svg:fill": "#FFFFFF",
                "multi-line-colors": "none",
                "line-tapered": "none"
            }
        }
    },
    "green": {
        "subTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "line-width": "1pt",
                "line-color": "#4A7C59",
                "border-line-color": "#4A7C59",
                "border-line-width": "3pt",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "centralTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:color": "#2D5016",
                "svg:fill": "#E2EFDA",
                "line-width": "1pt",
                "line-color": "#4A7C59",
                "border-line-color": "#4A7C59",
                "border-line-width": "5pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "mainTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:color": "#2D5016",
                "svg:fill": "#E2EFDA",
                "line-width": "1pt",
                "line-color": "#4A7C59",
                "border-line-color": "#4A7C59",
                "border-line-width": "2pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "summary": {
            "id": gen_id(),
            "properties": {"line-width": "5pt", "line-color": "#A9D18F",
                           "shape-class": "org.xmind.summaryShape.square"}
        },
        "boundary": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-size": "10pt",
                "fo:font-style": "italic", "fo:color": "#FFFFFF",
                "svg:fill": "#A9D18F", "svg:opacity": ".2",
                "line-width": "3pt", "line-color": "#548235",
                "line-pattern": "dot",
                "shape-class": "org.xmind.boundaryShape.roundedRect"
            }
        },
        "calloutTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "svg:fill": "#C6EFCE", "border-line-color": "#548235",
                "border-line-width": "2pt"
            }
        },
        "summaryTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-size": "10pt",
                "fo:font-style": "italic", "fo:color": "#FFFFFF",
                "svg:fill": "#548235", "border-line-width": "0pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "floatingTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-weight": "bold",
                "fo:color": "#FFFFFF", "svg:fill": "#4A7C59",
                "line-color": "#4A7C59", "border-line-width": "0pt"
            }
        },
        "relationship": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-size": "10pt",
                "fo:font-weight": "normal", "fo:font-style": "italic",
                "fo:color": "#595959", "fo:text-decoration": "none",
                "line-width": "3pt", "line-color": "#548235",
                "line-pattern": "dash",
                "arrow-end-class": "org.xmind.arrowShape.triangle"
            }
        },
        "map": {
            "id": gen_id(),
            "properties": {
                "svg:fill": "#FFFFFF", "multi-line-colors": "none",
                "line-tapered": "none"
            }
        }
    },
    "red": {
        "subTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "line-width": "1pt",
                "line-color": "#C00000",
                "border-line-color": "#C00000",
                "border-line-width": "3pt",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "centralTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:color": "#8C0000",
                "svg:fill": "#FBE5D6",
                "line-width": "1pt",
                "line-color": "#C00000",
                "border-line-color": "#C00000",
                "border-line-width": "5pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "mainTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "fo:color": "#8C0000",
                "svg:fill": "#FBE5D6",
                "line-width": "1pt",
                "line-color": "#C00000",
                "border-line-color": "#C00000",
                "border-line-width": "2pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "summary": {
            "id": gen_id(),
            "properties": {"line-width": "5pt", "line-color": "#F4B183",
                           "shape-class": "org.xmind.summaryShape.square"}
        },
        "boundary": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-size": "10pt",
                "fo:font-style": "italic", "fo:color": "#FFFFFF",
                "svg:fill": "#F4B183", "svg:opacity": ".2",
                "line-width": "3pt", "line-color": "#C55A11",
                "line-pattern": "dot",
                "shape-class": "org.xmind.boundaryShape.roundedRect"
            }
        },
        "calloutTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei",
                "svg:fill": "#FCE4D6", "border-line-color": "#C55A11",
                "border-line-width": "2pt"
            }
        },
        "summaryTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-size": "10pt",
                "fo:font-style": "italic", "fo:color": "#FFFFFF",
                "svg:fill": "#C55A11", "border-line-width": "0pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.curve"
            }
        },
        "floatingTopic": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-weight": "bold",
                "fo:color": "#FFFFFF", "svg:fill": "#C00000",
                "line-color": "#C00000", "border-line-width": "0pt"
            }
        },
        "relationship": {
            "id": gen_id(),
            "properties": {
                "fo:font-family": "Microsoft YaHei", "fo:font-size": "10pt",
                "fo:font-weight": "normal", "fo:font-style": "italic",
                "fo:color": "#595959", "fo:text-decoration": "none",
                "line-width": "3pt", "line-color": "#C55A11",
                "line-pattern": "dash",
                "arrow-end-class": "org.xmind.arrowShape.triangle"
            }
        },
        "map": {
            "id": gen_id(),
            "properties": {
                "svg:fill": "#FFFFFF", "multi-line-colors": "none",
                "line-tapered": "none"
            }
        }
    }
}

# flag-red 标记关键词
FLAG_RED_KEYWORDS = ['Skill', 'skill', '智能体', 'Agent', 'agent',
                     '算法', 'AI算法仓', '语言大模型', '大模型']


def parse_md(filepath):
    """解析 Markdown，返回结构化节点列表。

    规则：
    - # ~ ##### 解析为层级节点
    - 连续非标题行聚合为上一个节点的 notes
    - 过滤 '> AI生成' 水印行
    """
    nodes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pending_notes = []

    def flush_notes():
        nonlocal pending_notes
        if pending_notes and nodes:
            text = '\n'.join(pending_notes).strip()
            if text:
                if nodes[-1]['notes']:
                    nodes[-1]['notes'] += '\n' + text
                else:
                    nodes[-1]['notes'] = text
            pending_notes = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == '---':
            continue

        m = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if m:
            flush_notes()
            level = min(len(m.group(1)), 5)  # 6级标题映射为5级
            title = m.group(2).strip()
            nodes.append({'level': level, 'title': title, 'notes': ''})
        else:
            # 过滤 AIGC 水印
            if stripped.startswith('> AI生成') or stripped == '> AI生成':
                continue
            pending_notes.append(stripped)

    flush_notes()
    return nodes


def build_tree(nodes):
    """将节点列表构建为树结构。"""
    root = {'title': 'ROOT', 'notes': '', 'children': []}
    stack = [(0, root)]

    for node in nodes:
        new_node = {'title': node['title'], 'notes': node['notes'], 'children': []}
        while len(stack) > 1 and stack[-1][0] >= node['level']:
            stack.pop()
        parent = stack[-1][1]
        parent['children'].append(new_node)
        stack.append((node['level'], new_node))

    return root['children']


def topic_to_dict(node, depth=1, hl_map=None):
    """将树节点转为 XMind 2020+ JSON 格式的 topic dict，带样式和标记。
    
    hl_map: {title: flag_id} 底色映射，仅标题有底色时插入同色旗帜
    """
    topic = {
        'id': gen_id(),
        'class': 'topic',
        'title': node['title'],
    }

    # 仅在标题有底色时插入对应旗帜（底色→旗帜映射由外部提供）
    if hl_map:
        flag = hl_map.get(node['title'])
        if flag:
            topic['markers'] = [{'markerId': flag}]

    # 折叠规则：深层叶子节点且有较长 notes
    num_children = len(node['children'])
    if depth >= 3 and num_children > 2 and node.get('notes') and len(node['notes']) > 100:
        topic['branch'] = 'folded'
    if depth >= 4 and num_children == 0 and node.get('notes') and len(node['notes']) > 80:
        topic['branch'] = 'folded'

    # notes
    if node.get('notes'):
        topic['notes'] = {'plain': {'content': node['notes']}}

    # 递归子节点
    if node['children']:
        attached = [topic_to_dict(child, depth + 1, hl_map) for child in node['children']]
        topic['children'] = {'attached': attached}

    return topic


def create_xmind(md_path, xmind_path, right_count=None, theme_name='blue', hl_map=None):
    """将 Markdown 转换为 XMind 2020+ 格式文件。

    Args:
        md_path: 输入 Markdown 文件路径
        xmind_path: 输出 XMind 文件路径
        right_count: 右侧分支数，None 则自动均等划分（左ceil右floor）
        theme_name: 主题色名称 blue/green/red
        hl_map: {title: flag_id} 底色→旗帜映射，仅标题有底色时插入旗帜
    """
    if hl_map is None:
        hl_map = {}
    nodes = parse_md(md_path)
    tree = build_tree(nodes)

    if not tree:
        print('No content found in markdown file.')
        return

    first = tree[0]
    root_title = first['title']
    root_notes = first.get('notes', '')
    all_children = first['children']

    total = len(all_children)
    # 均等划分：左侧 ceil(total/2)，右侧 floor(total/2)
    # 实现从左到右、从上到下升序排列
    left_count = (total + 1) // 2
    if right_count is None:
        right_count = total - left_count
    right_count = min(right_count, total)
    left_count = total - right_count

    # XMind unbalanced 布局规则：
    # children 数组中前 right_count 个放右侧（从上到下正序）
    # 剩余放左侧（从数组末尾往上渲染，需反序保证升序）
    left_branches = [topic_to_dict(c, depth=1, hl_map=hl_map) for c in all_children[:left_count]]
    right_branches = [topic_to_dict(c, depth=1, hl_map=hl_map) for c in all_children[left_count:]]
    left_branches.reverse()  # 反序：XMind 左侧从数组末尾往上渲染
    root_children = right_branches + left_branches

    root_topic = {
        'id': gen_id(),
        'class': 'topic',
        'title': root_title,
        'structureClass': 'org.xmind.ui.map.unbalanced',
        'extensions': [{
            'provider': 'org.xmind.ui.map.unbalanced',
            'content': [{'name': 'right-number', 'content': str(right_count)}]
        }],
        'children': {
            'attached': root_children
        }
    }

    if root_notes:
        root_topic['notes'] = {'plain': {'content': root_notes}}

    theme = THEMES.get(theme_name, THEMES['blue'])

    content_json = [{
        'id': gen_id(),
        'class': 'sheet',
        'title': first['title'],
        'rootTopic': root_topic,
        'theme': theme
    }]

    metadata_json = {
        'dataStructureVersion': '3',
        'creator': {
            'name': 'XMind',
            'version': '24.01'
        },
        'layoutEngineVersion': '5'
    }

    manifest_json = {
        'file-entries': {
            'content.json': {},
            'metadata.json': {},
            'manifest.json': {}
        }
    }

    with zipfile.ZipFile(xmind_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('content.json', json.dumps(content_json, ensure_ascii=False, indent=2))
        zf.writestr('metadata.json', json.dumps(metadata_json, ensure_ascii=False, indent=2))
        zf.writestr('manifest.json', json.dumps(manifest_json, ensure_ascii=False, indent=2))

    print(f'XMind file created: {xmind_path}')
    print(f'  Total branches: {total}, Right: {right_count}, Left: {total - right_count}')
    print(f'  Theme: {theme_name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Markdown to XMind 2020+')
    parser.add_argument('input', help='Input Markdown file path')
    parser.add_argument('output', help='Output XMind file path')
    parser.add_argument('--right', type=int, default=None,
                        help='Number of branches on right side (default: half, rounded up)')
    parser.add_argument('--theme', choices=['blue', 'green', 'red'], default='blue',
                        help='Theme color (default: blue)')
    args = parser.parse_args()
    create_xmind(args.input, args.output, args.right, args.theme)
