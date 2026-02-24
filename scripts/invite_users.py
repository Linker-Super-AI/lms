#!/usr/bin/env python3
"""
邀请用户到课程
可以直接创建用户并分配到课程
"""

import frappe

def create_user(email, first_name, last_name="", send_welcome_email=True):
    """创建新用户"""
    if frappe.db.exists("User", email):
        print(f"⚠ 用户已存在: {email}")
        return frappe.get_doc("User", email)

    user = frappe.new_doc("User")
    user.update({
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "send_welcome_email": 1 if send_welcome_email else 0,
        "language": "zh",
        "user_type": "Website User",  # 门户用户
    })
    user.insert(ignore_permissions=True)
    print(f"✓ 用户创建成功: {email} ({first_name} {last_name})")
    return user

def enroll_user_to_course(email, course_name):
    """将用户注册到课程"""
    # 检查是否已经注册
    if frappe.db.exists("LMS Enrollment", {
        "member": email,
        "course": course_name
    }):
        print(f"  ⚠ 用户 {email} 已经注册到课程")
        return

    enrollment = frappe.new_doc("LMS Enrollment")
    enrollment.update({
        "member": email,
        "course": course_name,
        "member_type": "Student",
    })
    enrollment.insert(ignore_permissions=True)
    print(f"  ✓ 用户 {email} 已注册到课程")

def main():
    """主函数"""
    print("="*60)
    print("用户邀请和课程注册")
    print("="*60)
    print()

    # 示例：创建用户并注册到课程
    # 修改这里的用户信息
    users = [
        # 格式: (email, first_name, last_name)
        # ("student1@example.com", "学员一", ""),
        # ("student2@example.com", "学员二", ""),
    ]

    # 课程 ID
    course_name = "uf67dh57kl"  # 一周学习版课程

    if not users:
        print("请在脚本中添加要邀请的用户信息")
        print()
        print("示例代码：")
        print('users = [')
        print('    ("student@example.com", "张三", ""),')
        print('    ("teacher@example.com", "李四", ""),')
        print(']')
        print()
        return

    print(f"将创建 {len(users)} 个用户并注册到课程: {course_name}\n")

    for email, first_name, last_name in users:
        # 创建用户
        user = create_user(email, first_name, last_name, send_welcome_email=True)

        # 注册到课程
        enroll_user_to_course(email, course_name)
        print()

    frappe.db.commit()

    print("="*60)
    print("✅ 用户邀请完成！")
    print("="*60)
    print()
    print(f"用户已注册到课程，可以访问:")
    print(f"http://192.168.20.118:8001/courses/{course_name}")
    print()

# 运行脚本
import frappe
main()
