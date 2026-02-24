#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析课程文档并提取结构"""

import sys
from docx import Document
from docx.enum.style import WD_STYLE_TYPE

def parse_course_document(file_path):
    """解析 docx 文档，提取标题和内容"""
    doc = Document(file_path)

    structure = {
        'title': '',
        'chapters': []
    }

    current_chapter = None
    current_section = None
    current_content = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # 检查段落样式
        style_name = para.style.name

        # 标题 1 - 课程标题或章节
        if 'Heading 1' in style_name or '标题 1' in style_name:
            # 保存之前的内容
            if current_section and current_content:
                current_section['content'] = '\n'.join(current_content)
                current_content = []

            if current_chapter:
                structure['chapters'].append(current_chapter)

            # 新建章节
            current_chapter = {
                'title': text,
                'sections': [],
                'level': 1
            }
            current_section = None

        # 标题 2 - 小节
        elif 'Heading 2' in style_name or '标题 2' in style_name:
            # 保存之前的内容
            if current_section and current_content:
                current_section['content'] = '\n'.join(current_content)
                current_content = []

            if current_chapter:
                current_section = {
                    'title': text,
                    'content': '',
                    'level': 2
                }
                current_chapter['sections'].append(current_section)
            else:
                # 如果没有章节，创建一个默认章节
                current_chapter = {
                    'title': '第一章',
                    'sections': [],
                    'level': 1
                }
                current_section = {
                    'title': text,
                    'content': '',
                    'level': 2
                }
                current_chapter['sections'].append(current_section)

        # 标题 3 - 子小节
        elif 'Heading 3' in style_name or '标题 3' in style_name:
            # 保存之前的内容
            if current_section and current_content:
                current_section['content'] = '\n'.join(current_content)
                current_content = []

            if current_chapter:
                current_section = {
                    'title': text,
                    'content': '',
                    'level': 3
                }
                current_chapter['sections'].append(current_section)

        # 普通段落
        else:
            if text:
                current_content.append(text)

    # 保存最后的内容
    if current_section and current_content:
        current_section['content'] = '\n'.join(current_content)

    if current_chapter:
        structure['chapters'].append(current_chapter)

    # 如果没有提取到标题，使用文件名
    if not structure['chapters']:
        structure['title'] = 'V8.1一周学习版'
    else:
        structure['title'] = structure['chapters'][0]['title'] if structure['chapters'] else 'V8.1一周学习版'

    return structure

def print_structure(structure):
    """打印文档结构"""
    print(f"课程标题: {structure['title']}")
    print(f"章节数量: {len(structure['chapters'])}")
    print("\n" + "="*60)

    for i, chapter in enumerate(structure['chapters'], 1):
        print(f"\n第 {i} 章: {chapter['title']}")
        print(f"  小节数: {len(chapter['sections'])}")

        for j, section in enumerate(chapter['sections'], 1):
            level_prefix = "  " * section['level']
            content_preview = section['content'][:50] + "..." if len(section['content']) > 50 else section['content']
            print(f"{level_prefix}- {section['title']}")
            if content_preview:
                print(f"{level_prefix}  内容预览: {content_preview}")

if __name__ == '__main__':
    file_path = '/home/services/lms/docs/course/V8.1一周学习版_v4_compact.docx'

    try:
        print("正在解析文档...")
        structure = parse_course_document(file_path)
        print_structure(structure)

        # 保存为 JSON
        import json
        output_file = '/home/services/lms/docs/course/course_structure.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, ensure_ascii=False, indent=2)
        print(f"\n\n结构已保存到: {output_file}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
