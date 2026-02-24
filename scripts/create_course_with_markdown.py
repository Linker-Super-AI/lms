#!/usr/bin/env python3
"""
从 Markdown 结构创建 LMS 课程，保留完整格式
不创建测验占位符
"""

import json
import frappe

def create_markdown_content(title, markdown_text):
    """创建保留 Markdown 格式的课时内容"""
    blocks = []

    # 如果有内容，添加一个 markdown 块
    if markdown_text and markdown_text.strip():
        blocks.append({
            "id": f"md-{hash(markdown_text[:50]) % 100000}",
            "type": "markdown",
            "data": {
                "text": markdown_text.strip()
            }
        })
    else:
        # 如果没有内容，添加占位符
        blocks.append({
            "id": "placeholder",
            "type": "markdown",
            "data": {
                "text": f"## {title}\n\n*本节内容待完善...*"
            }
        })

    return json.dumps({
        "time": 1765194986690,
        "blocks": blocks,
        "version": "2.29.0"
    }, ensure_ascii=False)

def main():
    """主函数"""
    # 读取结构文件
    structure_file = "/tmp/course_structure_md.json"
    with open(structure_file, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    course_title = structure.get('title', 'V8.1 课程')
    chapters = structure.get('chapters', [])

    print(f"\n{'='*60}")
    print(f"开始创建课程: {course_title}")
    print(f"章节数量: {len(chapters)}")
    print(f"保留 Markdown 格式: ✓")
    print(f"创建测验: ✗ (请手动添加)")
    print(f"{'='*60}\n")

    # 1. 创建课程
    print("步骤 1: 创建课程...")
    course = frappe.new_doc("LMS Course")
    course.update({
        "title": course_title,
        "short_introduction": "贝叶斯交易飞轮 3.0 - 完整培训课程",
        "description": """链接者集团（Linker Group）统一投研交易体系与执行指南 V8.1

本课程涵盖：
- 贝叶斯交易飞轮的核心理念和八环模型
- 九大支柱：从宏观视角到团队管理的完整体系
- 四维核心研究语言（V+D+P+Vol）
- 策略框架、执行体系、风控系统
- 交易心理学与复盘迭代方法

学习目标：
✓ 统一研究语言
✓ 掌握策略矩阵
✓ 会填一页纸作战地图
✓ 建立完整框架认知

适合对象：交易员、研究员、投资经理、风控人员""",
        "published": 1,
        "featured": 1,
        "enable_certification": 1,
    })

    course.append("instructors", {"instructor": "Administrator"})
    course.insert(ignore_permissions=True)
    print(f"✓ 课程创建成功: {course.name}")

    # 2. 创建章节和课时
    print(f"\n步骤 2: 创建 {len(chapters)} 个章节...\n")

    for chapter_idx, chapter_data in enumerate(chapters, 1):
        chapter_title = chapter_data['title']
        sections = chapter_data.get('sections', [])
        chapter_content = chapter_data.get('content', '')

        print(f"[{chapter_idx}/{len(chapters)}] 创建章节: {chapter_title}")

        # 创建章节
        chapter = frappe.new_doc("Course Chapter")
        chapter.update({
            "course": course.name,
            "title": chapter_title,
        })
        chapter.insert(ignore_permissions=True)
        print(f"  ✓ 章节创建: {chapter.name}")

        # 添加章节引用
        chapter_ref = frappe.new_doc("Chapter Reference")
        chapter_ref.update({
            "chapter": chapter.name,
            "idx": chapter_idx,
            "parent": course.name,
            "parenttype": "LMS Course",
            "parentfield": "chapters",
        })
        chapter_ref.insert(ignore_permissions=True)

        # 如果章节本身有内容但没有小节，创建一个概述课时
        if chapter_content and not sections:
            lesson = frappe.new_doc("Course Lesson")
            lesson.update({
                "title": f"{chapter_title}",
                "chapter": chapter.name,
                "course": course.name,
                "content": create_markdown_content(chapter_title, chapter_content),
                "include_in_preview": chapter_idx == 1,  # 第一章可预览
            })
            lesson.insert(ignore_permissions=True)
            print(f"  ✓ 创建章节内容课时")

            lesson_ref = frappe.new_doc("Lesson Reference")
            lesson_ref.update({
                "lesson": lesson.name,
                "idx": 1,
                "parent": chapter.name,
                "parenttype": "Course Chapter",
                "parentfield": "lessons",
            })
            lesson_ref.insert(ignore_permissions=True)

        # 创建小节课时
        if sections:
            print(f"  创建 {len(sections)} 个课时 (保留 Markdown 格式):")
            for lesson_idx, section in enumerate(sections, 1):
                section_title = section['title']
                section_content = section.get('content', '')

                # 创建课时
                lesson = frappe.new_doc("Course Lesson")
                lesson.update({
                    "title": section_title,
                    "chapter": chapter.name,
                    "course": course.name,
                    "content": create_markdown_content(section_title, section_content),
                    "include_in_preview": (chapter_idx == 1 and lesson_idx == 1),  # 第一章第一节可预览
                })
                lesson.insert(ignore_permissions=True)

                content_len = len(section_content) if section_content else 0
                print(f"    [{lesson_idx}] ✓ {section_title} ({content_len} 字符)")

                # 添加课时引用
                lesson_ref = frappe.new_doc("Lesson Reference")
                lesson_ref.update({
                    "lesson": lesson.name,
                    "idx": lesson_idx,
                    "parent": chapter.name,
                    "parenttype": "Course Chapter",
                    "parentfield": "lessons",
                })
                lesson_ref.insert(ignore_permissions=True)

        print()  # 空行分隔

    frappe.db.commit()

    print(f"\n{'='*60}")
    print(f"✅ 课程创建完成！")
    print(f"{'='*60}")
    print(f"课程名称: {course.title}")
    print(f"课程 ID: {course.name}")
    print(f"章节数量: {len(chapters)}")
    print(f"内容格式: Markdown (保留原始格式)")
    print(f"测验: 无 (请在后台手动添加)")
    print(f"\n访问地址: http://192.168.20.118:8001/courses/{course.name}")
    print(f"{'='*60}\n")

    return course.name

# 运行脚本
import frappe
course_name = main()
print(f"✅ 课程 ID: {course_name}")
