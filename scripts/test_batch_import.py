#!/usr/bin/env python3
"""测试批量导入"""
import frappe
import csv

CSV_FILE = "/home/frappe/frappe-bench/sites/data/users_demo.csv"
COURSE_ID = "uf67dh57kl"
DEFAULT_PASSWORD = "Linker@2024"

print("="*60)
print("测试批量导入（3个演示用户）")
print("="*60)
print()

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    users_data = list(reader)

print(f"读取到 {len(users_data)} 个用户\n")

for idx, row in enumerate(users_data, 1):
    email = row.get('email', '').strip()
    first_name = row.get('first_name', '').strip()
    password = row.get('password', '').strip() or DEFAULT_PASSWORD

    print(f"[{idx}] {email} - {first_name}")

    if frappe.db.exists("User", email):
        print(f"  ⚠ 用户已存在，跳过")
        continue

    try:
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = first_name
        user.language = "zh"
        user.user_type = "Website User"
        user.send_welcome_email = 0
        user.insert(ignore_permissions=True)

        user.new_password = password
        user.save(ignore_permissions=True)
        print(f"  ✓ 创建成功")

        # 注册到课程
        enrollment = frappe.new_doc("LMS Enrollment")
        enrollment.member = email
        enrollment.course = COURSE_ID
        enrollment.member_type = "Student"
        enrollment.insert(ignore_permissions=True)
        print(f"  ✓ 已注册到课程")

    except Exception as e:
        print(f"  ❌ 失败: {e}")

    print()

frappe.db.commit()

print("="*60)
print("✅ 测试完成！")
print("="*60)
print()
print(f"登录测试：http://192.168.20.118:8001/login")
print(f"  邮箱：demo001@linker.net")
print(f"  密码：Linker@2024")
print()
