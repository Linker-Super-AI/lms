#!/usr/bin/env python3
"""
禁用自助注册
"""

import frappe

print("="*60)
print("禁用自助注册功能")
print("="*60)
print()

# 禁用 Website Settings 注册
ws = frappe.get_single("Website Settings")
ws.disable_signup = 1
ws.save(ignore_permissions=True)
print("✓ Website Settings: 已禁用自助注册")

# 禁用 LMS Settings 注册
lms = frappe.get_single("LMS Settings")
lms.disable_signup = 1
lms.save(ignore_permissions=True)
print("✓ LMS Settings: 已禁用自助注册")

frappe.db.commit()

print()
print("="*60)
print("✅ 自助注册已禁用！")
print("="*60)
print()
print("现在只能通过管理员创建用户：")
print("1. 访问: http://192.168.20.118:8001/app/user")
print("2. 点击「新建」创建用户")
print("3. 填写姓名、邮箱、密码")
print("4. 保存后告知用户登录信息")
print()
print("用户登录地址: http://192.168.20.118:8001/login")
print()
