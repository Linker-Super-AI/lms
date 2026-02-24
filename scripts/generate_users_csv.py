#!/usr/bin/env python3
"""
快速生成用户 CSV 文件
可以批量生成测试用户或按规则生成用户列表
"""

import csv

# 配置
OUTPUT_FILE = "/home/services/lms/data/users_batch.csv"

# 方式1：手动列表
manual_users = [
    # (email, first_name, last_name, password)
    ("zhangsan@linker.net", "张三", "", "Linker@2024"),
    ("lisi@linker.net", "李四", "", "Linker@2024"),
    ("wangwu@linker.net", "王五", "", "Linker@2024"),
]

# 方式2：批量生成（适合测试）
def generate_test_users(count=10, prefix="student", domain="linker.net", password="Linker@2024"):
    """
    批量生成测试用户

    count: 生成数量
    prefix: 邮箱前缀，如 student -> student001@domain.com
    domain: 邮箱域名
    password: 统一密码
    """
    users = []
    for i in range(1, count + 1):
        email = f"{prefix}{i:03d}@{domain}"
        first_name = f"{prefix.capitalize()}{i:03d}"
        last_name = ""
        users.append((email, first_name, last_name, password))
    return users

def main():
    """主函数"""
    print("="*60)
    print("生成用户 CSV 文件")
    print("="*60)
    print()

    # 选择生成方式
    print("选择生成方式：")
    print("1. 使用手动列表（修改脚本中的 manual_users）")
    print("2. 批量生成测试用户")
    print()

    # 这里可以修改
    use_manual = True  # True=使用手动列表, False=批量生成

    if use_manual:
        users = manual_users
        print(f"使用手动列表，共 {len(users)} 个用户")
    else:
        # 批量生成参数
        count = 20  # 生成数量
        prefix = "student"  # 邮箱前缀
        domain = "linker.net"  # 域名
        password = "Linker@2024"  # 密码

        users = generate_test_users(count, prefix, domain, password)
        print(f"批量生成 {count} 个测试用户")
        print(f"格式: {prefix}001@{domain}, {prefix}002@{domain}, ...")

    # 写入 CSV 文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['email', 'first_name', 'last_name', 'password'])
        for user in users:
            writer.writerow(user)

    print()
    print("="*60)
    print("✅ CSV 文件生成完成！")
    print("="*60)
    print(f"文件路径: {OUTPUT_FILE}")
    print(f"用户数量: {len(users)}")
    print()
    print("预览前5个用户：")
    for i, user in enumerate(users[:5], 1):
        email, first_name, last_name, password = user
        full_name = f"{first_name} {last_name}".strip()
        print(f"{i}. {email} - {full_name}")

    if len(users) > 5:
        print(f"... 还有 {len(users) - 5} 个用户")

    print()
    print("下一步：运行导入脚本")
    print("docker compose -f docker-compose-prod.yml exec -T lms \\")
    print("  bench --site 192.168.20.118 console < scripts/batch_create_users.py")
    print()

if __name__ == "__main__":
    main()
