#!/usr/bin/env python3
"""
启用用户注册功能
"""

import frappe

print("="*60)
print("启用 LMS 用户注册功能")
print("="*60)
print()

# 1. 启用 Website Settings 的注册功能
print("步骤 1: 配置 Website Settings...")
website_settings = frappe.get_single("Website Settings")
website_settings.disable_signup = 0  # 启用注册
website_settings.save(ignore_permissions=True)
print("✓ Website Settings: 已启用注册")

# 2. 配置 LMS Settings
print("\n步骤 2: 配置 LMS Settings...")
if frappe.db.exists("LMS Settings", "LMS Settings"):
    lms_settings = frappe.get_single("LMS Settings")
    lms_settings.disable_signup = 0  # 启用 LMS 注册
    lms_settings.save(ignore_permissions=True)
    print("✓ LMS Settings: 已启用注册")

# 3. 检查 Portal Settings
print("\n步骤 3: 配置 Portal Settings...")
if frappe.db.exists("Portal Settings", "Portal Settings"):
    portal_settings = frappe.get_single("Portal Settings")
    # 确保门户可以访问
    print("✓ Portal Settings 存在")
else:
    print("⚠ Portal Settings 不存在")

frappe.db.commit()

print()
print("="*60)
print("✅ 用户注册功能已启用！")
print("="*60)
print()
print("用户现在可以通过以下方式注册：")
print(f"1. 访问注册页面: http://192.168.20.118:8001/signup")
print(f"2. 或在登录页面点击「注册」链接")
print()
print("管理员也可以通过后台手动创建用户：")
print(f"- 访问: http://192.168.20.118:8001/app/user")
print(f"- 点击「新建」创建新用户")
print()
