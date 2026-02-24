#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从文档自动创建 LMS 课程"""

import json

def create_quiz_for_chapter(chapter_title, chapter_number):
    """为每个章节创建一个测验"""
    import frappe

    # 创建 3-5 个测验问题
    questions = []
    num_questions = 3

    for i in range(1, num_questions + 1):
        question = frappe.new_doc("LMS Question")
        question.update({
            "question": f"{chapter_title} - 测验题 {i}：请根据本章内容回答",
            "type": "Choices",
            "option_1": "选项 A",
            "is_correct_1": 1,
            "explanation_1": "这是正确答案的解释",
            "option_2": "选项 B",
            "is_correct_2": 0,
            "explanation_2": "这不是正确答案",
            "option_3": "选项 C",
            "is_correct_3": 0,
            "option_4": "选项 D",
            "is_correct_4": 0,
        })
        question.insert(ignore_permissions=True)
        questions.append(question)
        print(f"  ✓ 创建问题 {i}/{num_questions}")

    # 创建测验
    quiz = frappe.new_doc("LMS Quiz")
    quiz.update({
        "title": f"{chapter_title} - 章节测验",
        "passing_percentage": 70,
        "show_answers": 1,
        "max_attempts": 3,
    })

    # 添加问题到测验
    total_marks = 0
    for question in questions:
        quiz.append("questions", {
            "question": question.name,
            "marks": 10,
        })
        total_marks += 10

    quiz.total_marks = total_marks
    quiz.insert(ignore_permissions=True)
    print(f"  ✓ 创建测验: {quiz.name} (总分: {total_marks})")

    return quiz

def create_lesson_content(section_title, section_content):
    """创建课时内容（Editor.js 格式）"""
    blocks = []

    # 添加标题块
    blocks.append({
        "id": f"heading-{hash(section_title) % 100000}",
        "type": "header",
        "data": {
            "text": section_title,
            "level": 2
        }
    })

    # 添加内容块（将内容分段）
    if section_content:
        paragraphs = section_content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                blocks.append({
                    "id": f"para-{hash(para[:20]) % 100000}",
                    "type": "paragraph",
                    "data": {
                        "text": para.strip()
                    }
                })
    else:
        blocks.append({
            "id": f"para-default",
            "type": "paragraph",
            "data": {
                "text": "本节内容待完善..."
            }
        })

    return json.dumps({
        "time": 1765194986690,
        "blocks": blocks,
        "version": "2.29.0"
    }, ensure_ascii=False)

def create_course_from_structure(structure_file, instructor_email="Administrator"):
    """从文档结构创建课程"""
    import frappe

    # 读取结构文件
    with open(structure_file, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    course_title = structure.get('title', 'V8.1一周学习版')
    chapters = structure.get('chapters', [])

    print(f"\n{'='*60}")
    print(f"开始创建课程: {course_title}")
    print(f"章节数量: {len(chapters)}")
    print(f"{'='*60}\n")

    # 1. 创建课程
    print("步骤 1: 创建课程...")
    course = frappe.new_doc("LMS Course")
    course.update({
        "title": course_title,
        "short_introduction": "贝叶斯交易飞轮 3.0 完整培训课程",
        "description": """本课程为链接者集团（Linker Group）统一投研交易体系与执行指南，
包含完整的交易理念、研究框架、策略体系、执行方法和风控规范。

学习目标：
- 掌握统一的研究语言和交易框架
- 理解宏观定位与战场选择
- 学习四维核心研究方法（V+D+P+Vol）
- 掌握策略制定与执行体系
- 建立完善的风控意识和心理管理能力

适合对象：交易员、研究员、投资经理""",
        "published": 1,
        "featured": 1,
        "enable_certification": 1,
    })

    # 添加讲师
    course.append("instructors", {"instructor": instructor_email})
    course.insert(ignore_permissions=True)
    print(f"✓ 课程创建成功: {course.name}")

    # 2. 创建章节和课时
    print(f"\n步骤 2: 创建 {len(chapters)} 个章节...\n")

    for chapter_idx, chapter_data in enumerate(chapters, 1):
        chapter_title = chapter_data['title']
        sections = chapter_data.get('sections', [])

        print(f"[{chapter_idx}/{len(chapters)}] 创建章节: {chapter_title}")

        # 创建章节
        chapter = frappe.new_doc("Course Chapter")
        chapter.update({
            "course": course.name,
            "title": chapter_title,
        })
        chapter.insert(ignore_permissions=True)
        print(f"  ✓ 章节创建: {chapter.name}")

        # 添加章节引用到课程
        chapter_ref = frappe.new_doc("Chapter Reference")
        chapter_ref.update({
            "chapter": chapter.name,
            "idx": chapter_idx,
            "parent": course.name,
            "parenttype": "LMS Course",
            "parentfield": "chapters",
        })
        chapter_ref.insert(ignore_permissions=True)

        # 创建课时
        if sections:
            print(f"  创建 {len(sections)} 个课时:")
            for lesson_idx, section in enumerate(sections, 1):
                section_title = section['title']
                section_content = section.get('content', '')

                # 创建课时
                lesson = frappe.new_doc("Course Lesson")
                lesson.update({
                    "title": section_title,
                    "chapter": chapter.name,
                    "course": course.name,
                    "content": create_lesson_content(section_title, section_content),
                    "include_in_preview": 1 if lesson_idx == 1 else 0,  # 第一节可预览
                })
                lesson.insert(ignore_permissions=True)
                print(f"    [{lesson_idx}] ✓ {section_title}")

                # 添加课时引用到章节
                lesson_ref = frappe.new_doc("Lesson Reference")
                lesson_ref.update({
                    "lesson": lesson.name,
                    "idx": lesson_idx,
                    "parent": chapter.name,
                    "parenttype": "Course Chapter",
                    "parentfield": "lessons",
                })
                lesson_ref.insert(ignore_permissions=True)
        else:
            # 如果没有小节，创建一个默认课时
            lesson = frappe.new_doc("Course Lesson")
            lesson.update({
                "title": f"{chapter_title} - 概述",
                "chapter": chapter.name,
                "course": course.name,
                "content": create_lesson_content(chapter_title, "本章内容概述..."),
                "include_in_preview": 1,
            })
            lesson.insert(ignore_permissions=True)
            print(f"  ✓ 创建默认课时")

            lesson_ref = frappe.new_doc("Lesson Reference")
            lesson_ref.update({
                "lesson": lesson.name,
                "idx": 1,
                "parent": chapter.name,
                "parenttype": "Course Chapter",
                "parentfield": "lessons",
            })
            lesson_ref.insert(ignore_permissions=True)

        # 为每章创建测验
        print(f"  创建章节测验:")
        quiz = create_quiz_for_chapter(chapter_title, chapter_idx)

        # 创建一个测验课时
        quiz_lesson = frappe.new_doc("Course Lesson")
        quiz_lesson.update({
            "title": f"{chapter_title} - 章节测验",
            "chapter": chapter.name,
            "course": course.name,
            "quiz_id": quiz.name,
            "content": json.dumps({
                "time": 1765194986690,
                "blocks": [
                    {
                        "type": "quiz",
                        "data": {"quiz": quiz.name}
                    }
                ],
                "version": "2.29.0"
            }, ensure_ascii=False),
        })
        quiz_lesson.insert(ignore_permissions=True)

        # 添加测验课时到章节（放在最后）
        quiz_lesson_ref = frappe.new_doc("Lesson Reference")
        quiz_lesson_ref.update({
            "lesson": quiz_lesson.name,
            "idx": (len(sections) if sections else 1) + 1,
            "parent": chapter.name,
            "parenttype": "Course Chapter",
            "parentfield": "lessons",
        })
        quiz_lesson_ref.insert(ignore_permissions=True)
        print(f"  ✓ 测验课时已添加\n")

    # 提交所有更改
    frappe.db.commit()

    print(f"\n{'='*60}")
    print(f"✅ 课程创建完成！")
    print(f"{'='*60}")
    print(f"课程名称: {course.title}")
    print(f"课程 ID: {course.name}")
    print(f"章节数量: {len(chapters)}")
    print(f"访问地址: http://192.168.20.118:8001/courses/{course.name}")
    print(f"{'='*60}\n")

    return course

# 运行脚本
import frappe
structure_file = "/home/services/lms/docs/course/course_structure.json"
course = create_course_from_structure(structure_file)
print("✅ 所有操作完成！")
print(f"\n现在您可以访问以下地址查看课程：")
print(f"http://192.168.20.118:8001/courses/{course.name}")
