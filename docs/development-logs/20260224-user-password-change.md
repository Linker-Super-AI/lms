# 用户密码修改功能 - 开发记录

## 基本信息
- **开发时间：** 2026-02-24
- **开发者：** Claude + 用户
- **分支：** feature/user-password-change
- **状态：** 进行中

## 需求说明

### 问题描述
管理员批量创建用户账号后，所有用户都使用默认密码。用户登录后，无法找到修改密码的入口，导致：
1. 安全隐患：所有用户使用相同的默认密码
2. 用户体验差：用户想修改密码但找不到入口

### 功能需求
1. 为普通用户提供密码修改功能
2. 用户可以在登录后自主修改密码
3. 需要验证旧密码以确保安全性
4. 界面友好，易于访问

## 技术方案

### 设计思路
- 利用 Frappe 已有的密码修改 API：`frappe.core.doctype.user.user.update_password`
- 该 API 已在 `/home/services/lms/lms/auth.py:33` 白名单中，可以被网站用户调用
- 在前端用户下拉菜单中添加"修改密码"选项
- 创建密码修改弹窗组件

### 涉及文件
1. `frontend/src/components/Sidebar/UserDropdown.vue` - 添加"修改密码"菜单项
2. `frontend/src/components/Modals/ChangePasswordModal.vue` - 新建密码修改弹窗组件
3. `lms/auth.py` - 确认 API 白名单配置（已存在，无需修改）

## 实现细节

### 核心功能

#### 1. 添加菜单项
在用户下拉菜单中添加"修改密码"选项，位于"我的资料"和"切换主题"之间。

#### 2. 密码修改弹窗
创建独立的 Vue 组件，包含：
- 旧密码输入框（必填，用于验证身份）
- 新密码输入框（必填，需符合密码强度要求）
- 确认新密码输入框（必填，需与新密码一致）
- 提交按钮
- 错误提示信息

#### 3. 表单验证
- 旧密码不能为空
- 新密码长度至少 8 位
- 新密码与确认密码必须一致
- 新密码不能与旧密码相同

#### 4. API 调用
```javascript
frappe.call({
  method: 'frappe.core.doctype.user.user.update_password',
  args: {
    old_password: oldPassword,
    new_password: newPassword
  },
  callback: function(r) {
    if (r.message) {
      // 成功：显示提示，关闭弹窗
    }
  },
  error: function(r) {
    // 失败：显示错误信息（如旧密码错误）
  }
})
```

### 关键代码

#### UserDropdown.vue 修改
在 `menuItems` 数组中添加新项：
```javascript
{
  label: '修改密码',
  icon: 'lock',
  action: 'changePassword'
}
```

#### ChangePasswordModal.vue 组件结构
```vue
<template>
  <Dialog v-model="show" :options="{ title: '修改密码' }">
    <template #body-content>
      <div class="space-y-4">
        <FormControl
          type="password"
          label="当前密码"
          v-model="oldPassword"
        />
        <FormControl
          type="password"
          label="新密码"
          v-model="newPassword"
        />
        <FormControl
          type="password"
          label="确认新密码"
          v-model="confirmPassword"
        />
      </div>
    </template>
    <template #actions>
      <Button @click="handleSubmit" variant="solid">确认修改</Button>
    </template>
  </Dialog>
</template>
```

## 测试记录

### 测试内容
- [ ] 用户下拉菜单显示"修改密码"选项
- [ ] 点击后弹出密码修改弹窗
- [ ] 表单验证正常工作
  - [ ] 空字段提示
  - [ ] 新密码与确认密码不一致提示
  - [ ] 密码长度不足提示
- [ ] 旧密码错误时显示错误信息
- [ ] 修改成功后显示成功提示
- [ ] 修改成功后可以使用新密码登录
- [ ] 修改成功后旧密码不能再使用

### 测试用户
- 使用批量创建的测试用户（如 test001）
- 默认密码：Test@123456

### 测试步骤
1. 使用默认密码登录
2. 点击右上角用户菜单
3. 选择"修改密码"
4. 输入旧密码和新密码
5. 提交修改
6. 退出登录
7. 使用新密码重新登录验证

### 测试结果
（待测试后填写）

## 遇到的问题

### 问题1：
（开发过程中记录问题）

## 后续优化

- [ ] 考虑添加密码强度提示（弱/中/强）
- [ ] 考虑添加首次登录强制修改密码功能
- [ ] 考虑添加密码过期策略
- [ ] 优化错误提示信息的中文化

## 发布记录
- **发布时间：** （待定）
- **版本号：** v1.1.0
- **发布说明：** 新增用户密码自主修改功能，提升系统安全性
