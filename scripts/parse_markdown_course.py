#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 Markdown 文件解析课程结构，保留完整格式"""

import re
import json

def unescape_markdown(text):
    """去除 markdown 转义符号"""
    # 去掉反斜杠转义
    text = text.replace('\\#', '#')
    text = text.replace('\\*', '*')
    text = text.replace('\\|', '|')
    text = text.replace('\\=', '=')
    text = text.replace('\\-', '-')
    text = text.replace('\\<', '<')
    text = text.replace('\\>', '>')
    return text

def parse_markdown_course(file_path):
    """解析 markdown 课程文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 去除转义
    content = unescape_markdown(content)

    # 分割成行
    lines = content.split('\n')

    structure = {
        'title': '',
        'chapters': []
    }

    current_chapter = None
    current_section = None
    current_content = []

    for line in lines:
        # 一级标题 - 章节
        if line.startswith('# ') and not line.startswith('## '):
            # 保存之前的内容
            if current_section and current_content:
                current_section['content'] = '\n'.join(current_content).strip()
                current_content = []

            if current_chapter:
                structure['chapters'].append(current_chapter)

            # 新章节
            chapter_title = line[2:].strip()
            current_chapter = {
                'title': chapter_title,
                'sections': [],
                'content': ''  # 章节级别的内容
            }
            current_section = None

        # 二级标题 - 小节
        elif line.startswith('## '):
            # 保存之前的小节内容
            if current_section and current_content:
                current_section['content'] = '\n'.join(current_content).strip()
                current_content = []

            section_title = line[3:].strip()

            if current_chapter:
                current_section = {
                    'title': section_title,
                    'content': ''
                }
                current_chapter['sections'].append(current_section)
            else:
                # 如果没有章节，创建默认章节
                current_chapter = {
                    'title': '课程介绍',
                    'sections': [],
                    'content': ''
                }
                current_section = {
                    'title': section_title,
                    'content': ''
                }
                current_chapter['sections'].append(current_section)

        # 普通内容
        else:
            if line.strip():  # 非空行
                current_content.append(line)
            elif current_content:  # 空行，保留段落分隔
                current_content.append('')

    # 保存最后的内容
    if current_section and current_content:
        current_section['content'] = '\n'.join(current_content).strip()
    elif current_chapter and current_content:
        # 如果有章节但没有小节，内容归入章节
        current_chapter['content'] = '\n'.join(current_content).strip()

    if current_chapter:
        structure['chapters'].append(current_chapter)

    # 提取课程标题
    if structure['chapters']:
        structure['title'] = structure['chapters'][0]['title']

    return structure

def print_structure(structure):
    """打印文档结构"""
    print(f"课程标题: {structure['title']}")
    print(f"章节数量: {len(structure['chapters'])}")
    print("\n" + "="*60)

    for i, chapter in enumerate(structure['chapters'], 1):
        print(f"\n第 {i} 章: {chapter['title']}")

        if chapter.get('content'):
            print(f"  章节内容长度: {len(chapter['content'])} 字符")

        if chapter['sections']:
            print(f"  小节数: {len(chapter['sections'])}")
            for j, section in enumerate(chapter['sections'], 1):
                content_preview = section['content'][:80].replace('\n', ' ') if section['content'] else ''
                if content_preview:
                    content_preview += "..."
                print(f"    {j}. {section['title']}")
                if content_preview:
                    print(f"       内容: {content_preview}")

if __name__ == '__main__':
    file_path = '/home/services/lms/docs/course/course.md'

    try:
        print("正在解析 Markdown 文档...")
        structure = parse_markdown_course(file_path)
        print_structure(structure)

        # 保存为 JSON
        output_file = '/home/services/lms/docs/course/course_structure_md.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, ensure_ascii=False, indent=2)
        print(f"\n\n结构已保存到: {output_file}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
