# 课程内容安全保护功能 - 开发记录

## 基本信息
- **开发时间：** 2026-02-25
- **开发者：** Claude + 用户
- **分支：** （待创建）
- **状态：** ✅ 已完成开发，待测试

## 需求说明

### 问题描述
目前学生可以轻易地复制课程的文字内容和保存图片，导致课程内容容易被复制传播，影响课程的价值和版权保护。

### 功能需求
1. 在课程设置中添加"安全保护"选项
2. 提供禁用复制粘贴功能
3. 提供禁用右键菜单功能
4. 讲师和管理员不受限制
5. 保护措施对普通学生生效

## 技术方案

### 设计思路

#### 后端设计
在 LMS Course DocType 中添加新的 Section Break "安全保护"，包含两个布尔字段：
- `disable_copy_paste`: 禁用复制粘贴
- `disable_right_click`: 禁用右键菜单

#### 前端设计
在课程学习页面（Lesson.vue）中：
1. 从 API 获取课程的安全保护设置
2. 根据设置动态应用保护措施
3. 使用 JavaScript 事件监听器禁用相关操作
4. 使用 CSS `user-select: none` 禁用文本选择

### 涉及文件
1. `lms/lms/doctype/lms_course/lms_course.json` - 添加安全保护字段
2. `lms/lms/utils.py` - 修改 get_lesson API 返回安全保护设置
3. `frontend/src/pages/Lesson.vue` - 实现前端保护逻辑

## 实现细节

### 1. 后端 DocType 修改

#### 添加字段到 field_order
在 `disable_self_learning` 后添加：
```json
"security_section",
"disable_copy_paste",
"disable_right_click",
```

#### 添加字段定义
```json
{
  "fieldname": "security_section",
  "fieldtype": "Section Break",
  "label": "安全保护"
},
{
  "default": "0",
  "fieldname": "disable_copy_paste",
  "fieldtype": "Check",
  "label": "禁用复制粘贴",
  "description": "启用后，学生无法复制课程内容（包括文字和图片）"
},
{
  "default": "0",
  "fieldname": "disable_right_click",
  "fieldtype": "Check",
  "label": "禁用右键菜单",
  "description": "启用后，学生无法使用鼠标右键（防止另存为图片等操作）"
}
```

### 2. 后端 API 修改

#### 文件：`lms/lms/utils.py`

**修改 get_lesson 函数获取课程信息部分：**
```python
course_info = frappe.db.get_value(
    "LMS Course",
    course,
    ["title", "paid_certificate", "disable_self_learning",
     "disable_copy_paste", "disable_right_click"],
    as_dict=1,
)
```

**添加字段到返回数据：**
```python
lesson_details.disable_copy_paste = course_info.disable_copy_paste or 0
lesson_details.disable_right_click = course_info.disable_right_click or 0
```

### 3. 前端保护逻辑实现

#### 文件：`frontend/src/pages/Lesson.vue`

**核心函数：setupContentProtection()**

```javascript
const setupContentProtection = () => {
    const isAdmin = allowEdit()

    // 管理员和讲师不受保护限制
    if (isAdmin) return

    const contentArea = lessonContainer.value
    if (!contentArea) return

    // 禁用复制粘贴
    if (lesson.data?.disable_copy_paste) {
        // 禁用选择文本
        contentArea.style.userSelect = 'none'
        contentArea.style.webkitUserSelect = 'none'
        contentArea.style.mozUserSelect = 'none'
        contentArea.style.msUserSelect = 'none'

        // 禁用复制事件
        const preventCopy = (e) => e.preventDefault()
        contentArea.addEventListener('copy', preventCopy)
        contentArea.addEventListener('cut', preventCopy)
        contentArea.addEventListener('selectstart', preventCopy)
        contentArea.addEventListener('dragstart', preventCopy)

        // 清理函数
        onBeforeUnmount(() => {
            contentArea.removeEventListener('copy', preventCopy)
            contentArea.removeEventListener('cut', preventCopy)
            contentArea.removeEventListener('selectstart', preventCopy)
            contentArea.removeEventListener('dragstart', preventCopy)
        })
    }

    // 禁用右键菜单
    if (lesson.data?.disable_right_click) {
        const preventContextMenu = (e) => e.preventDefault()
        contentArea.addEventListener('contextmenu', preventContextMenu)

        onBeforeUnmount(() => {
            contentArea.removeEventListener('contextmenu', preventContextMenu)
        })
    }
}
```

**监听数据变化，应用保护：**
```javascript
watch(
    () => lesson.data,
    (newData) => {
        if (newData && (newData.disable_copy_paste || newData.disable_right_click)) {
            nextTick(() => {
                setupContentProtection()
            })
        }
    },
    { immediate: true }
)
```

## 保护措施说明

### 禁用复制粘贴
- ✅ 禁用 Ctrl+C / Cmd+C 复制
- ✅ 禁用 Ctrl+X / Cmd+X 剪切
- ✅ 禁用鼠标选择文本
- ✅ 禁用拖拽选择
- ✅ 禁用拖拽图片

### 禁用右键菜单
- ✅ 禁用鼠标右键点击
- ✅ 防止"另存为图片"
- ✅ 防止"检查元素"（普通用户）

### 权限管理
- ✅ 讲师不受限制（can edit）
- ✅ 管理员不受限制
- ✅ 普通学生受限制

## 使用说明

### 如何启用内容保护

1. **进入课程编辑页面**
   - 以讲师或管理员身份登录
   - 打开需要保护的课程

2. **配置安全保护**
   - 找到"安全保护"区域
   - 勾选"禁用复制粘贴"：防止学生复制文字和图片
   - 勾选"禁用右键菜单"：防止学生右键保存图片或查看源代码

3. **保存设置**
   - 点击保存
   - 学生访问课程时将自动应用保护措施

### 测试方法

#### 测试禁用复制粘贴：
1. 以学生身份登录
2. 进入启用保护的课程
3. 尝试选择文字 → 应该无法选中
4. 尝试 Ctrl+C → 无效
5. 尝试拖拽图片 → 无法拖拽

#### 测试禁用右键菜单：
1. 以学生身份登录
2. 在课程内容区域右键点击
3. 右键菜单不应出现

#### 测试管理员权限：
1. 以讲师/管理员身份登录
2. 进入同一课程
3. 应该可以正常复制和右键

## 技术亮点

### 1. 多层次保护
- CSS 层：禁用文本选择
- JavaScript 层：监听并阻止复制事件
- 事件层：阻止选择、复制、剪切、拖拽

### 2. 兼容性处理
- 支持标准浏览器（user-select）
- 支持 WebKit 内核（-webkit-user-select）
- 支持 Firefox（-moz-user-select）
- 支持 IE/Edge（-ms-user-select）

### 3. 权限区分
- 自动识别用户角色
- 管理员和讲师不受限制
- 学生根据设置受保护

### 4. 资源清理
- 使用 `onBeforeUnmount` 清理事件监听器
- 防止内存泄漏

### 5. 响应式设计
- 使用 Vue3 watch 监听数据变化
- 动态应用/移除保护措施
- 立即生效（immediate: true）

## 局限性说明

### 技术局限
1. **无法完全阻止截图**
   - 用户仍可以使用系统截图工具
   - 可以使用手机拍照

2. **浏览器开发者工具**
   - 有技术背景的用户可以通过开发者工具绕过
   - 建议配合使用"禁止预览"功能

3. **浏览器扩展**
   - 某些浏览器扩展可能绕过保护
   - 建议在课程说明中提醒学生遵守版权

### 最佳实践
1. 结合"禁止预览"功能，只对已注册学生开放
2. 在课程开头添加版权声明
3. 定期检查课程内容是否被泄露
4. 对于特别重要的内容，考虑使用视频形式（更难复制）

## 后续优化建议

- [ ] 添加水印功能（显示学生账号）
- [ ] 添加内容加密功能
- [ ] 记录可疑的复制尝试行为
- [ ] 在移动端也实施保护措施
- [ ] 添加防截屏 API（如果浏览器支持）
- [ ] 提供批量设置功能（一次性为多个课程启用保护）

## 相关文档

- [内容保护最佳实践](https://docs.frappe.io/lms/content-protection)
- [Vue 3 事件处理](https://vuejs.org/guide/essentials/event-handling.html)

## 数据库迁移

需要运行数据库迁移来添加新字段：

```bash
# 在容器内执行
bench --site lms.localhost migrate
```

## 测试记录

### 测试环境
- 浏览器：Chrome 120+, Firefox 120+, Edge 120+
- 用户角色：学生、讲师、管理员

### 测试用例
- [ ] 启用禁用复制粘贴，学生无法复制文字
- [ ] 启用禁用复制粘贴，学生无法选择文本
- [ ] 启用禁用复制粘贴，学生无法拖拽图片
- [ ] 启用禁用右键菜单，学生无法右键点击
- [ ] 讲师不受任何限制
- [ ] 管理员不受任何限制
- [ ] 不同浏览器兼容性测试
- [ ] 性能测试（确保不影响页面加载速度）

## 提交信息

待测试通过后提交到 Git 仓库。

**建议提交信息：**
```
feat(security): 添加课程内容安全保护功能

- 在课程设置中添加"安全保护"区域
- 支持禁用复制粘贴功能
- 支持禁用右键菜单功能
- 讲师和管理员不受限制
- 修改 get_lesson API 返回安全设置
- 在 Lesson.vue 实现前端保护逻辑

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```
