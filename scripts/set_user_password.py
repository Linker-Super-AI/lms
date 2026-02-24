#!/usr/bin/env python3
"""
为用户设置密码
"""

import frappe

# 用户信息
email = "cdg1234@linker.net"
new_password = "Linker@2024"  # 初始密码

print("="*60)
print("设置用户密码")
print("="*60)
print()

if not frappe.db.exists("User", email):
    print(f"❌ 用户不存在: {email}")
    print("请先创建用户")
else:
    user = frappe.get_doc("User", email)

    # 设置密码
    user.new_password = new_password
    user.save(ignore_permissions=True)

    frappe.db.commit()

    print(f"✓ 用户: {email}")
    print(f"✓ 姓名: {user.full_name}")
    print(f"✓ 新密码已设置")
    print()
    print("="*60)
    print("✅ 密码设置完成！")
    print("="*60)
    print()
    print("登录信息：")
    print(f"  网址: http://192.168.20.118:8001/login")
    print(f"  邮箱: {email}")
    print(f"  密码: {new_password}")
    print()
    print("提示：")
    print("- 用户首次登录后可以修改密码")
    print("- 建议告知用户登录后立即修改密码")
    print()
