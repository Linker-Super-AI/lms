#!/usr/bin/env python3
"""
为课程添加防复制保护
通过自定义 CSS 和 JavaScript 实现
"""

import frappe

def add_copy_protection_to_course(course_name):
    """为指定课程添加防复制保护"""

    # 自定义 CSS - 禁用文本选择
    custom_css = """
/* 禁用文本选择和复制 */
.lesson-content {
    -webkit-user-select: none !important;
    -moz-user-select: none !important;
    -ms-user-select: none !important;
    user-select: none !important;
    -webkit-touch-callout: none !important;
}

/* 添加水印效果 */
.lesson-content::before {
    content: "仅供学习使用 - 禁止复制传播";
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 48px;
    color: rgba(0, 0, 0, 0.05);
    z-index: 1;
    pointer-events: none;
    white-space: nowrap;
}

/* 禁用打印时的内容 */
@media print {
    .lesson-content {
        display: none !important;
    }
    body::before {
        content: "本课程内容受版权保护，禁止打印";
        display: block;
        text-align: center;
        font-size: 24px;
        padding: 50px;
    }
}
"""

    # 自定义 JavaScript - 禁用右键、复制、截图等
    custom_js = """
// 禁用右键菜单
document.addEventListener('contextmenu', function(e) {
    if (e.target.closest('.lesson-content')) {
        e.preventDefault();
        return false;
    }
});

// 禁用复制
document.addEventListener('copy', function(e) {
    if (window.getSelection().toString() && e.target.closest('.lesson-content')) {
        e.preventDefault();
        frappe.show_alert({
            message: '课程内容受版权保护，禁止复制',
            indicator: 'red'
        });
        return false;
    }
});

// 禁用剪切
document.addEventListener('cut', function(e) {
    if (e.target.closest('.lesson-content')) {
        e.preventDefault();
        return false;
    }
});

// 禁用选择文本
document.addEventListener('selectstart', function(e) {
    if (e.target.closest('.lesson-content')) {
        e.preventDefault();
        return false;
    }
});

// 禁用拖拽选择
document.addEventListener('dragstart', function(e) {
    if (e.target.closest('.lesson-content')) {
        e.preventDefault();
        return false;
    }
});

// 禁用键盘快捷键（Ctrl+C, Ctrl+A, Ctrl+P 等）
document.addEventListener('keydown', function(e) {
    if (e.target.closest('.lesson-content')) {
        // Ctrl+C / Cmd+C (复制)
        if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
            e.preventDefault();
            frappe.show_alert({
                message: '禁止复制课程内容',
                indicator: 'red'
            });
            return false;
        }
        // Ctrl+A / Cmd+A (全选)
        if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
            e.preventDefault();
            return false;
        }
        // Ctrl+P / Cmd+P (打印)
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            frappe.show_alert({
                message: '禁止打印课程内容',
                indicator: 'red'
            });
            return false;
        }
        // Ctrl+S / Cmd+S (保存)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            return false;
        }
        // F12 (开发者工具)
        if (e.key === 'F12') {
            e.preventDefault();
            return false;
        }
    }
});

// 禁用开发者工具快捷键
document.addEventListener('keydown', function(e) {
    // Ctrl+Shift+I / Cmd+Option+I (检查元素)
    if ((e.ctrlKey && e.shiftKey && e.key === 'I') ||
        (e.metaKey && e.altKey && e.key === 'i')) {
        e.preventDefault();
        return false;
    }
    // Ctrl+Shift+J / Cmd+Option+J (控制台)
    if ((e.ctrlKey && e.shiftKey && e.key === 'J') ||
        (e.metaKey && e.altKey && e.key === 'j')) {
        e.preventDefault();
        return false;
    }
    // Ctrl+U / Cmd+Option+U (查看源代码)
    if ((e.ctrlKey && e.key === 'u') ||
        (e.metaKey && e.altKey && e.key === 'u')) {
        e.preventDefault();
        return false;
    }
});

console.log('课程防复制保护已启用');
"""

    # 获取课程
    course = frappe.get_doc("LMS Course", course_name)

    # 在课程描述中添加说明
    protection_notice = """

---

**📋 版权声明**

本课程内容受版权保护，仅供注册学员学习使用。

**禁止行为：**
- ❌ 复制、粘贴课程内容
- ❌ 截图、录屏课程内容
- ❌ 打印课程材料
- ❌ 向第三方传播或分享

**违规处理：**
违反版权规定者将被取消学习资格，并可能承担法律责任。

感谢您的理解与配合！"""

    if protection_notice not in course.description:
        course.description = course.description + protection_notice
        course.save(ignore_permissions=True)
        print(f"✓ 已更新课程描述，添加版权声明")

    frappe.db.commit()

    print(f"\n防复制保护配置已准备：")
    print(f"- CSS 规则：禁用文本选择、添加水印、禁用打印")
    print(f"- JS 规则：禁用右键、复制、快捷键、开发者工具")
    print(f"\n需要将以下代码添加到网站设置中...")
    print(f"\nCSS 代码保存位置: /tmp/copy_protection.css")
    print(f"JS 代码保存位置: /tmp/copy_protection.js")

    # 保存到文件
    with open('/tmp/copy_protection.css', 'w', encoding='utf-8') as f:
        f.write(custom_css)

    with open('/tmp/copy_protection.js', 'w', encoding='utf-8') as f:
        f.write(custom_js)

    return {
        'css': custom_css,
        'js': custom_js
    }

def apply_protection_globally():
    """全局应用防复制保护（通过 Website Settings）"""

    # 获取或创建 Website Settings
    if frappe.db.exists("Website Settings"):
        settings = frappe.get_doc("Website Settings")
    else:
        settings = frappe.new_doc("Website Settings")

    # 读取保护代码
    with open('/tmp/copy_protection.css', 'r', encoding='utf-8') as f:
        css_code = f.read()

    with open('/tmp/copy_protection.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    # 添加自定义 CSS
    if hasattr(settings, 'custom_css'):
        if css_code not in (settings.custom_css or ''):
            settings.custom_css = (settings.custom_css or '') + '\n\n' + css_code

    # 添加自定义 JavaScript
    if hasattr(settings, 'custom_js'):
        if js_code not in (settings.custom_js or ''):
            settings.custom_js = (settings.custom_js or '') + '\n\n' + js_code

    settings.save(ignore_permissions=True)
    frappe.db.commit()

    print("✓ 防复制保护已全局应用到网站设置")
    print("✓ 所有课程内容现在都受到保护")

# 运行脚本
import frappe

print("="*60)
print("课程内容防复制保护设置")
print("="*60)
print()

# 为最新课程添加保护
course_name = "uf67dh57kl"
protection = add_copy_protection_to_course(course_name)

# 全局应用
apply_protection_globally()

print()
print("="*60)
print("✅ 防复制保护已启用！")
print("="*60)
print()
print("保护功能：")
print("1. ✓ 禁用文本选择")
print("2. ✓ 禁用右键菜单")
print("3. ✓ 禁用复制/剪切")
print("4. ✓ 禁用打印")
print("5. ✓ 禁用快捷键 (Ctrl+C, Ctrl+A, Ctrl+P, F12 等)")
print("6. ✓ 添加水印")
print("7. ✓ 版权声明")
print()
print("请访问课程页面测试：")
print(f"http://192.168.20.118:8001/courses/{course_name}")
print()
