#!/usr/bin/env python3
"""
快速创建测试用户
"""

import frappe

print("="*60)
print("创建测试用户")
print("="*60)
print()

# 用户信息
email = "student@test.com"
password = "Test@123456"  # 符合密码强度要求
first_name = "测试学员"
course_id = "uf67dh57kl"

# 1. 创建用户
if frappe.db.exists("User", email):
    print(f"⚠ 用户已存在: {email}")
    user = frappe.get_doc("User", email)
else:
    user = frappe.new_doc("User")
    user.update({
        "email": email,
        "first_name": first_name,
        "language": "zh",
        "user_type": "Website User",
        "send_welcome_email": 0,  # 不发送邮件
    })
    user.insert(ignore_permissions=True)
    print(f"✓ 用户创建成功: {email}")

    # 设置密码
    user.new_password = password
    user.save(ignore_permissions=True)
    print(f"✓ 密码已设置")

# 2. 注册到课程
if not frappe.db.exists("LMS Enrollment", {"member": email, "course": course_id}):
    enrollment = frappe.new_doc("LMS Enrollment")
    enrollment.update({
        "member": email,
        "course": course_id,
        "member_type": "Student",
    })
    enrollment.insert(ignore_permissions=True)
    print(f"✓ 已注册到课程")
else:
    print(f"⚠ 已经注册到课程")

frappe.db.commit()

print()
print("="*60)
print("✅ 测试用户创建完成！")
print("="*60)
print()
print("登录信息：")
print(f"  网址: http://192.168.20.118:8001/login")
print(f"  邮箱: {email}")
print(f"  密码: {password}")
print()
print("课程地址：")
print(f"  http://192.168.20.118:8001/courses/{course_id}")
print()
