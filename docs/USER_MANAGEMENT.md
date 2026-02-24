# LMS 用户管理指南

## 一、用户注册方式

### 1.1 自助注册（已启用）

用户可以自己注册账号：

**注册地址：** http://192.168.20.118:8001/signup

用户需要提供：
- 邮箱地址
- 全名
- 密码

注册后会收到欢迎邮件（如果配置了邮件服务器）。

### 1.2 管理员手动创建

管理员可以在后台直接创建用户：

1. 访问用户列表：http://192.168.20.118:8001/app/user
2. 点击「新建」按钮
3. 填写用户信息：
   - 邮箱（必填）
   - 名字（必填）
   - 姓氏（可选）
   - 语言：选择 "zh"（中文）
   - 用户类型：选择 "Website User"（门户用户）
4. 勾选「发送欢迎邮件」
5. 保存

### 1.3 通过脚本批量邀请

使用 `/home/services/lms/scripts/invite_users.py` 脚本：

#### 步骤：

1. **编辑脚本**，添加要邀请的用户：

```python
users = [
    ("student1@example.com", "张三", ""),
    ("student2@example.com", "李四", ""),
    ("student3@example.com", "王五", ""),
]
```

2. **运行脚本**：

```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml exec -T lms \
  bench --site 192.168.20.118 console < scripts/invite_users.py
```

脚本会自动：
- 创建用户账号
- 发送欢迎邮件
- 将用户注册到指定课程

## 二、课程注册管理

### 2.1 手动将用户注册到课程

**后台操作：**

1. 访问课程列表：http://192.168.20.118:8001/app/lms-course
2. 打开课程（如：uf67dh57kl）
3. 在「Students」标签页
4. 点击「Add Row」添加学员
5. 选择用户邮箱
6. 保存

### 2.2 用户自己注册课程

用户登录后，访问课程页面：
- http://192.168.20.118:8001/courses/uf67dh57kl

点击「Enroll」或「注册」按钮即可。

### 2.3 课程访问权限设置

**公开课程：**
```python
course = frappe.get_doc("LMS Course", "uf67dh57kl")
course.published = 1  # 发布
course.save()
```

**付费课程：**
```python
course.paid_course = 1
course.course_price = 99.00
course.currency = "CNY"
course.save()
```

## 三、用户角色和权限

### 3.1 用户类型

- **System User**：系统用户，可以访问后台
- **Website User**：门户用户，只能访问前台课程

### 3.2 LMS 角色

- **Instructor**（讲师）：可以创建和管理课程
- **Moderator**（版主）：可以管理讨论和评论
- **Student**（学员）：普通学习者
- **LMS Admin**：LMS 管理员

### 3.3 分配角色

后台操作：
1. 打开用户：http://192.168.20.118:8001/app/user/[email]
2. 滚动到「Roles」部分
3. 添加角色（如：Instructor）
4. 保存

## 四、常用管理操作

### 4.1 查看所有学员

```python
# 查看特定课程的学员
enrollments = frappe.get_all("LMS Enrollment",
    filters={"course": "uf67dh57kl"},
    fields=["member", "member_type", "creation"]
)
for e in enrollments:
    print(f"{e.member} - {e.member_type}")
```

### 4.2 批量注册用户到课程

```python
course_name = "uf67dh57kl"
emails = ["user1@example.com", "user2@example.com"]

for email in emails:
    if not frappe.db.exists("LMS Enrollment", {"member": email, "course": course_name}):
        enrollment = frappe.new_doc("LMS Enrollment")
        enrollment.member = email
        enrollment.course = course_name
        enrollment.member_type = "Student"
        enrollment.insert()
        print(f"✓ {email} 已注册")
frappe.db.commit()
```

### 4.3 移除课程学员

```python
enrollment_name = frappe.db.get_value("LMS Enrollment",
    {"member": "user@example.com", "course": "uf67dh57kl"},
    "name"
)
if enrollment_name:
    frappe.delete_doc("LMS Enrollment", enrollment_name)
    frappe.db.commit()
```

## 五、配置说明

### 5.1 注册功能开关

当前配置（已启用）：
- Website Settings → disable_signup = 0
- LMS Settings → disable_signup = 0

如需关闭注册：
```python
settings = frappe.get_single("Website Settings")
settings.disable_signup = 1
settings.save()
```

### 5.2 邮件配置

配置邮件服务器后，用户注册时会收到欢迎邮件。

访问：http://192.168.20.118:8001/app/email-account

### 5.3 用户注册验证

可以要求邮箱验证：

```python
settings = frappe.get_single("Website Settings")
settings.disable_signup = 0
settings.enable_email_verification = 1
settings.save()
```

## 六、快速参考

| 操作 | 地址/命令 |
|------|----------|
| 用户注册页 | http://192.168.20.118:8001/signup |
| 登录页面 | http://192.168.20.118:8001/login |
| 用户管理 | http://192.168.20.118:8001/app/user |
| 课程管理 | http://192.168.20.118:8001/app/lms-course |
| 启用注册 | 运行 `scripts/enable_user_signup.py` |
| 批量邀请 | 运行 `scripts/invite_users.py` |

## 七、常见问题

**Q: 用户注册后看不到课程？**
A: 需要将用户手动注册到课程，或者设置课程为「允许自由注册」。

**Q: 如何设置课程需要审批才能注册？**
A: 在课程设置中启用「Paid Course」或使用自定义工作流。

**Q: 如何批量导入用户？**
A: 使用 Data Import 工具或修改 `invite_users.py` 脚本。

**Q: 用户忘记密码怎么办？**
A: 用户可以在登录页点击「忘记密码」，或管理员在后台重置。
