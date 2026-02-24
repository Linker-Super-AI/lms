#!/usr/bin/env python3
"""
批量创建用户并注册到课程
从 CSV 文件导入用户信息
"""

import frappe
import csv

# 配置
CSV_FILE = "/home/frappe/frappe-bench/sites/data/users_batch.csv"  # CSV 文件路径
# 备选：/home/frappe/frappe-bench/sites/data/users_template.csv
COURSE_ID = "uf67dh57kl"  # 课程 ID，留空则不自动注册到课程
DEFAULT_PASSWORD = "Linker@2024"  # 如果 CSV 中没有密码，使用这个默认密码

def create_user(email, first_name, last_name="", password=None):
    """创建用户"""
    if frappe.db.exists("User", email):
        print(f"  ⚠ 用户已存在: {email}")
        return frappe.get_doc("User", email)

    user = frappe.new_doc("User")
    user.update({
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "language": "zh",
        "user_type": "Website User",
        "send_welcome_email": 0,
    })
    user.insert(ignore_permissions=True)

    # 设置密码
    if password:
        user.new_password = password
        user.flags.ignore_password_policy = False  # 检查密码强度
        user.save(ignore_permissions=True)

    print(f"  ✓ 用户创建: {email} ({first_name} {last_name})")
    return user

def enroll_to_course(email, course_id):
    """注册到课程"""
    if frappe.db.exists("LMS Enrollment", {"member": email, "course": course_id}):
        return False

    enrollment = frappe.new_doc("LMS Enrollment")
    enrollment.update({
        "member": email,
        "course": course_id,
        "member_type": "Student",
    })
    enrollment.insert(ignore_permissions=True)
    return True

def main():
    """主函数"""
    print("="*60)
    print("批量创建用户")
    print("="*60)
    print()

    # 读取 CSV 文件
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            users_data = list(reader)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {CSV_FILE}")
        print()
        print("请创建 CSV 文件，格式如下：")
        print("email,first_name,last_name,password")
        print("user1@example.com,张三,,Linker@2024")
        print("user2@example.com,李四,,Linker@2024")
        return
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return

    if not users_data:
        print("❌ CSV 文件为空")
        return

    print(f"从 CSV 文件读取 {len(users_data)} 个用户\n")

    success_count = 0
    error_count = 0
    enrolled_count = 0

    for idx, row in enumerate(users_data, 1):
        email = row.get('email', '').strip()
        first_name = row.get('first_name', '').strip()
        last_name = row.get('last_name', '').strip()
        password = row.get('password', '').strip() or DEFAULT_PASSWORD

        if not email or not first_name:
            print(f"[{idx}] ⚠ 跳过：邮箱或姓名为空")
            error_count += 1
            continue

        print(f"[{idx}/{len(users_data)}] 处理: {email}")

        try:
            # 创建用户
            user = create_user(email, first_name, last_name, password)
            success_count += 1

            # 注册到课程
            if COURSE_ID:
                if enroll_to_course(email, COURSE_ID):
                    print(f"  ✓ 已注册到课程")
                    enrolled_count += 1
                else:
                    print(f"  - 已在课程中")

        except Exception as e:
            print(f"  ❌ 失败: {e}")
            error_count += 1

        print()

    frappe.db.commit()

    print("="*60)
    print("✅ 批量创建完成！")
    print("="*60)
    print(f"成功创建: {success_count} 个用户")
    print(f"注册课程: {enrolled_count} 个用户")
    print(f"失败/跳过: {error_count} 个")
    print()
    print(f"课程地址: http://192.168.20.118:8001/courses/{COURSE_ID}")
    print(f"用户登录: http://192.168.20.118:8001/login")
    print()

# 运行脚本
import frappe
main()
