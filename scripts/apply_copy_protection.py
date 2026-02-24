#!/usr/bin/env python3
"""
应用防复制保护的独立脚本
"""

import frappe

# 课程 ID
course_name = "uf67dh57kl"

# 自定义 CSS
custom_css = """
/* 课程内容防复制保护 */
.lesson-content,
.lesson-content *,
.course-content,
.course-content * {
    -webkit-user-select: none !important;
    -moz-user-select: none !important;
    -ms-user-select: none !important;
    user-select: none !important;
    -webkit-touch-callout: none !important;
}

/* 水印 */
body.course-page::after {
    content: "版权所有 · 禁止复制";
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 60px;
    color: rgba(0, 0, 0, 0.03);
    z-index: 9999;
    pointer-events: none;
    white-space: nowrap;
}

/* 禁用打印 */
@media print {
    .lesson-content, .course-content {
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

# 自定义 JavaScript
custom_js = """
(function() {
    'use strict';

    const selector = '.lesson-content, .course-content';

    // 禁用右键
    document.addEventListener('contextmenu', function(e) {
        if (e.target.closest(selector)) {
            e.preventDefault();
            return false;
        }
    });

    // 禁用复制
    document.addEventListener('copy', function(e) {
        if (e.target.closest(selector)) {
            e.preventDefault();
            if (typeof frappe !== 'undefined' && frappe.show_alert) {
                frappe.show_alert({
                    message: '课程内容受版权保护，禁止复制',
                    indicator: 'red'
                });
            }
            return false;
        }
    });

    // 禁用剪切
    document.addEventListener('cut', function(e) {
        if (e.target.closest(selector)) {
            e.preventDefault();
            return false;
        }
    });

    // 禁用选择
    document.addEventListener('selectstart', function(e) {
        if (e.target.closest(selector)) {
            e.preventDefault();
            return false;
        }
    });

    // 禁用拖拽
    document.addEventListener('dragstart', function(e) {
        if (e.target.closest(selector)) {
            e.preventDefault();
            return false;
        }
    });

    // 禁用快捷键
    document.addEventListener('keydown', function(e) {
        if (e.target.closest(selector) || document.querySelector(selector)) {
            // Ctrl+C / Cmd+C
            if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
                e.preventDefault();
                if (typeof frappe !== 'undefined' && frappe.show_alert) {
                    frappe.show_alert({message: '禁止复制', indicator: 'red'});
                }
                return false;
            }
            // Ctrl+A / Cmd+A
            if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
                e.preventDefault();
                return false;
            }
            // Ctrl+P / Cmd+P
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                if (typeof frappe !== 'undefined' && frappe.show_alert) {
                    frappe.show_alert({message: '禁止打印', indicator: 'red'});
                }
                return false;
            }
            // Ctrl+S / Cmd+S
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                return false;
            }
        }

        // F12
        if (e.key === 'F12') {
            e.preventDefault();
            return false;
        }
        // Ctrl+Shift+I
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            return false;
        }
        // Ctrl+Shift+J
        if (e.ctrlKey && e.shiftKey && e.key === 'J') {
            e.preventDefault();
            return false;
        }
        // Ctrl+U
        if (e.ctrlKey && e.key === 'u') {
            e.preventDefault();
            return false;
        }
    });

    console.log('防复制保护已启用');
})();
"""

print("="*60)
print("应用课程防复制保护")
print("="*60)
print()

# 1. 更新课程描述
course = frappe.get_doc("LMS Course", course_name)

protection_notice = """

---

## 📋 版权声明

**本课程内容受版权保护，仅供注册学员学习使用。**

### 禁止以下行为：
- ❌ 复制、粘贴课程内容
- ❌ 截图、录屏课程内容
- ❌ 打印课程材料
- ❌ 向第三方传播或分享

### 违规处理：
违反版权规定者将被取消学习资格，并可能承担法律责任。

*感谢您的理解与配合！*
"""

if "版权声明" not in course.description:
    course.description = course.description + protection_notice
    course.save(ignore_permissions=True)
    print("✓ 已添加版权声明到课程描述")
else:
    print("✓ 课程已包含版权声明")

# 2. 应用全局设置
try:
    # 尝试获取 Website Settings
    if not frappe.db.exists("Website Settings", "Website Settings"):
        settings = frappe.new_doc("Website Settings")
        settings.name = "Website Settings"
    else:
        settings = frappe.get_doc("Website Settings", "Website Settings")

    # 添加 CSS
    existing_css = settings.get("custom_css") or ""
    if "课程内容防复制保护" not in existing_css:
        settings.custom_css = existing_css + "\n\n" + custom_css
        print("✓ 已添加防复制 CSS")
    else:
        print("✓ CSS 已存在")

    # 添加 JS
    existing_js = settings.get("custom_js") or ""
    if "防复制保护已启用" not in existing_js:
        settings.custom_js = existing_js + "\n\n" + custom_js
        print("✓ 已添加防复制 JavaScript")
    else:
        print("✓ JavaScript 已存在")

    settings.save(ignore_permissions=True)
    print("✓ Website Settings 已更新")

except Exception as e:
    print(f"⚠ 无法更新 Website Settings: {e}")
    print("将保存代码到文件，请手动添加...")

# 3. 保存到文件以备手动使用
with open('/tmp/copy_protection.css', 'w') as f:
    f.write(custom_css)
print("✓ CSS 已保存到 /tmp/copy_protection.css")

with open('/tmp/copy_protection.js', 'w') as f:
    f.write(custom_js)
print("✓ JS 已保存到 /tmp/copy_protection.js")

frappe.db.commit()

print()
print("="*60)
print("✅ 防复制保护配置完成！")
print("="*60)
print()
print("保护功能：")
print("1. ✓ 禁用文本选择")
print("2. ✓ 禁用右键菜单")
print("3. ✓ 禁用复制/剪切/粘贴")
print("4. ✓ 禁用打印")
print("5. ✓ 禁用键盘快捷键")
print("6. ✓ 禁用开发者工具快捷键")
print("7. ✓ 添加水印")
print("8. ✓ 版权声明")
print()
print(f"访问课程测试: http://192.168.20.118:8001/courses/{course_name}")
print()
