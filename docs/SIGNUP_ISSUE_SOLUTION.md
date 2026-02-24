# 注册页面密码问题说明

## ⚠️ 问题

访问 http://192.168.20.118:8001/signup 时，注册表单只有：
- 全名
- 邮箱

**没有密码输入框！**

## 📖 原因

Frappe LMS 的注册流程设计为：

1. 用户填写姓名和邮箱
2. 系统自动生成随机密码
3. **系统发送验证邮件**（包含设置密码的链接）
4. 用户点击邮件链接设置密码
5. 用户登录

**关键：** 这个流程依赖邮件服务器！

## ✅ 解决方案

### 推荐方案：禁用自助注册，管理员创建用户

**适合：** 企业内部培训、受控的学员管理

#### 步骤：

1. **禁用自助注册**
   ```bash
   cd /home/services/lms
   docker compose -f docker-compose-prod.yml exec -T lms \
     bench --site 192.168.20.118 console < scripts/disable_self_signup.py
   ```

2. **管理员创建用户**

   a. 访问后台：http://192.168.20.118:8001/app/user

   b. 点击「+ Add User」或「新建」

   c. 填写信息：
      ```
      Email: user@example.com
      First Name: 张三
      Language: zh
      User Type: Website User

      ⚠️ 向下滚动，找到「New Password」字段
      New Password: Linker@2024
      ```

   d. 保存

3. **将用户添加到课程**

   a. 访问：http://192.168.20.118:8001/app/lms-course/uf67dh57kl

   b. 在「Students」部分添加用户邮箱

   c. 保存

4. **告知用户登录信息**
   ```
   登录地址: http://192.168.20.118:8001/login
   邮箱: user@example.com
   密码: Linker@2024
   ```

### 备选方案：配置邮件服务器

**适合：** 公开课程、需要大量用户自助注册

参考文档：`/home/services/lms/docs/EMAIL_SETUP.md`

配置邮件后：
- 用户在注册页面填写姓名和邮箱
- 系统发送验证邮件
- 用户点击邮件中的链接设置密码
- 完成注册并登录

## 🎯 当前建议

**对于企业内部使用：**

✅ **使用方案1**（管理员创建用户）
- 简单直接
- 无需配置邮件
- 便于管理和控制

**对于公开课程：**

如需大量用户自助注册，建议：
1. 配置邮件服务器（见 EMAIL_SETUP.md）
2. 或使用第三方认证（OAuth、LDAP等）

## 📝 快速操作指南

### 创建单个用户

```bash
# 使用脚本快速创建
cd /home/services/lms

# 编辑脚本，修改用户信息
nano scripts/set_user_password.py

# 运行
docker compose -f docker-compose-prod.yml exec -T lms \
  bench --site 192.168.20.118 console < scripts/set_user_password.py
```

### 批量创建用户

```bash
# 编辑脚本，添加用户列表
nano scripts/invite_users.py

# 运行
docker compose -f docker-compose-prod.yml exec -T lms \
  bench --site 192.168.20.118 console < scripts/invite_users.py
```

## ❓ 常见问题

**Q: 用户已经在注册页面注册了，怎么办？**

A: 管理员需要手动为这些用户设置密码：
1. 访问 http://192.168.20.118:8001/app/user/用户邮箱
2. 在「New Password」字段设置密码
3. 保存
4. 告知用户密码

**Q: 可以修改注册页面添加密码字段吗？**

A: 可以，但需要修改 LMS 源代码，比较复杂。建议使用管理员创建用户的方式。

**Q: 忘记告诉用户密码怎么办？**

A: 随时可以在用户管理页面重置密码。
