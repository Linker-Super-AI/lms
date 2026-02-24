# 配置邮件服务器

配置邮件后，用户可以：
- 自助注册并通过邮件设置密码
- 接收欢迎邮件
- 接收密码重置链接
- 接收课程通知

## 快速配置（使用 Gmail）

### 1. 访问邮件账户设置

```
http://192.168.20.118:8001/app/email-account
```

### 2. 创建新邮件账户

点击「New」或「新建」

### 3. 填写配置

```
Email Account Name: Gmail Outgoing
Email Address: your-email@gmail.com
Default Outgoing: ✓ 勾选

SMTP Settings:
  SMTP Server: smtp.gmail.com
  SMTP Port: 587
  Use TLS: ✓ 勾选
  Login Id: your-email@gmail.com
  Password: 应用专用密码（不是 Gmail 密码）

Enable Outgoing: ✓ 勾选
```

### 4. 获取 Gmail 应用专用密码

1. 访问 Google 账户设置: https://myaccount.google.com/security
2. 启用两步验证
3. 生成应用专用密码
4. 将生成的密码填入上面的 Password 字段

### 5. 保存并测试

点击「Save」后，点击「Send Test Email」测试

## 其他邮件服务商

### 163 邮箱

```
SMTP Server: smtp.163.com
SMTP Port: 465 或 587
Use TLS: ✓
Login Id: yourname@163.com
Password: 授权码（不是邮箱密码）
```

### QQ 邮箱

```
SMTP Server: smtp.qq.com
SMTP Port: 465 或 587
Use TLS: ✓
Login Id: yourname@qq.com
Password: 授权码
```

### 阿里云企业邮箱

```
SMTP Server: smtp.mxhichina.com
SMTP Port: 465
Use TLS: ✓
Login Id: yourname@yourdomain.com
Password: 邮箱密码
```

## 配置后的效果

✓ 用户在 http://192.168.20.118:8001/signup 注册后会收到邮件
✓ 邮件中包含设置密码的链接
✓ 用户点击链接设置密码后即可登录

## 验证配置

运行测试脚本：

```python
import frappe

# 发送测试邮件
frappe.sendmail(
    recipients=["test@example.com"],
    subject="测试邮件",
    message="这是一封测试邮件，如果收到说明配置成功！"
)
```
