#!/usr/bin/env python3
"""
修复课程内容字段大小限制
将 TEXT 字段修改为 LONGTEXT 以支持大量内容
"""

import frappe

print("="*60)
print("修复课程内容字段大小限制")
print("="*60)
print()

# 需要修改的表和字段
fields_to_fix = [
    ('tabCourse Lesson', 'content'),
    ('tabLMS Course', 'description'),
    ('tabLMS Course', 'video_embed'),
    ('tabCourse Chapter', 'description'),
]

success_count = 0
skip_count = 0
error_count = 0

for table, column in fields_to_fix:
    print(f"处理 {table}.{column}...")

    # 检查字段是否存在
    check_result = frappe.db.sql(f"""
        SELECT DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = '{table}'
        AND COLUMN_NAME = '{column}'
    """, as_dict=True)

    if not check_result:
        print(f"  - 字段不存在，跳过\n")
        skip_count += 1
        continue

    current_type = check_result[0].DATA_TYPE

    if current_type == 'longtext':
        print(f"  ✓ 已经是 LONGTEXT，无需修改\n")
        skip_count += 1
        continue

    # 修改字段类型
    try:
        print(f"  ⚠️ 当前类型: {current_type.upper()}")
        print(f"  正在修改为 LONGTEXT...")

        frappe.db.sql(f"""
            ALTER TABLE `{table}`
            MODIFY COLUMN `{column}` LONGTEXT
        """)

        print(f"  ✓ 修改成功\n")
        success_count += 1

    except Exception as e:
        print(f"  ❌ 修改失败: {e}\n")
        error_count += 1

frappe.db.commit()

print("="*60)
print("✅ 修复完成！")
print("="*60)
print(f"成功修改: {success_count} 个字段")
print(f"跳过: {skip_count} 个字段")
print(f"失败: {error_count} 个字段")
print()
print("字段大小对比：")
print("- TEXT: 最大 65,535 字节 (约 64KB)")
print("- LONGTEXT: 最大 4,294,967,295 字节 (约 4GB)")
print()
print("现在可以保存大量课程内容了！")
print()
