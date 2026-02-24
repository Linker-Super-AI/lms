# LMS 中文汉化配置说明

## ✅ 已完成的配置

系统已成功配置为中文界面。

### 配置内容

1. **系统默认语言**: 简体中文 (zh)
2. **管理员用户语言**: 简体中文
3. **已清除缓存**: 所有缓存已刷新
4. **服务已重启**: 配置已生效

## 🌐 访问地址

- **局域网**: http://192.168.20.118:8001/lms
- **本地**: http://lms.localhost:8001/lms

## 🔐 登录信息

- 用户名: `Administrator`
- 密码: `admin`

## 📝 使用说明

### 首次登录后看到中文

1. 访问系统后，界面应该显示为中文
2. 如果仍显示英文，请按以下步骤操作：
   - 清除浏览器缓存（Ctrl+Shift+Delete）
   - 刷新页面（Ctrl+F5 或 Cmd+Shift+R）
   - 重新登录

### 手动切换语言

如果需要手动切换语言：

1. 登录系统
2. 点击右上角用户头像
3. 选择 "My Settings" 或 "我的设置"
4. 在 "Language" 或 "语言" 下拉框中选择 "简体中文"
5. 点击保存

## 🔧 支持的语言

系统已安装以下中文语言包：

- **zh** - 简体中文（已设为默认）
- **zh-TW** - 繁體中文

## 🎯 前端/后台语言设置

### 前台学习平台 (/lms)

前台已自动使用中文界面，包括：
- 课程列表
- 课程详情
- 学习界面
- 讨论区
- 个人中心

### 后台管理界面 (/app)

管理后台也已设置为中文，包括：
- 系统设置
- 用户管理
- 课程管理
- 数据统计

## 📱 移动设备

移动设备访问时也会自动显示中文界面，体验一致。

## 🔄 为新用户设置默认语言

系统已配置默认语言为简体中文，新注册的用户会自动使用中文界面。

### 通过命令行修改默认语言

如需修改系统默认语言：

```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml exec lms bash -c \
  "cd /home/frappe/frappe-bench && \
   bench --site 192.168.20.118 set-config default_language zh"
```

### 为现有用户批量设置语言

如果有其他用户需要设置中文：

```bash
docker compose -f docker-compose-prod.yml exec lms bash -c \
  "cd /home/frappe/frappe-bench && bench --site 192.168.20.118 console" << 'EOF'
import frappe
frappe.connect()

# 获取所有用户
users = frappe.get_all("User",
    filters={"enabled": 1, "user_type": "System User"},
    fields=["name"])

# 为每个用户设置中文
for user in users:
    doc = frappe.get_doc("User", user.name)
    doc.language = "zh"
    doc.save(ignore_permissions=True)
    print(f"已设置 {user.name} 的语言为中文")

frappe.db.commit()
exit()
EOF
```

## 🌍 切换到其他语言

### 切换到繁体中文

```bash
docker compose -f docker-compose-prod.yml exec lms bash -c \
  "cd /home/frappe/frappe-bench && \
   bench --site 192.168.20.118 set-config default_language zh-TW && \
   bench --site 192.168.20.118 clear-cache"
```

### 切换回英文

```bash
docker compose -f docker-compose-prod.yml exec lms bash -c \
  "cd /home/frappe/frappe-bench && \
   bench --site 192.168.20.118 set-config default_language en && \
   bench --site 192.168.20.118 clear-cache"
```

## 🔍 翻译覆盖率

Frappe LMS 的中文翻译包含：

- ✅ 核心系统界面
- ✅ 课程管理功能
- ✅ 用户管理功能
- ✅ 批次管理功能
- ✅ 作业和测验功能
- ✅ 证书功能
- ✅ 讨论功能

**注意**: 部分专业术语或新功能可能仍保留英文，这是正常现象。

## 🛠️ 故障排查

### 问题1: 界面仍显示英文

**解决方案**:
1. 清除浏览器缓存
2. 使用隐私/无痕模式访问
3. 检查用户设置中的语言选项
4. 重新登录系统

### 问题2: 部分内容是中文，部分是英文

**原因**: 这是正常的，某些内容可能还未完全翻译。

**解决方案**:
- 系统核心功能都已翻译
- 用户创建的内容（课程标题、描述等）需要手动输入中文

### 问题3: 登录页面显示英文

**解决方案**:
登录页面语言基于浏览器设置，登录后会自动切换到中文。

## 📚 其他多语言功能

### 创建多语言课程

LMS 支持创建多语言课程内容：

1. 在课程设置中可以为不同语言创建不同版本
2. 用户根据其语言设置自动看到对应版本

### 语言包更新

要更新翻译或贡献翻译：

1. 访问 Frappe 官方翻译平台
2. 参与简体中文翻译改进
3. 或在本地自定义翻译

## 💡 提示

- 首次加载中文界面可能稍慢，因为需要加载语言文件
- 建议在用户设置中将语言固定为简体中文
- 如果发现翻译不准确，可以通过 Frappe 社区反馈

## ✅ 验证配置

访问以下地址验证中文界面：

1. **学习平台**: http://192.168.20.118:8001/lms
   - 应该看到中文导航菜单
   - 按钮和标签应为中文

2. **管理后台**: http://192.168.20.118:8001/app
   - 登录后界面为中文
   - 菜单和功能都是中文

3. **用户设置**: http://192.168.20.118:8001/app/user/Administrator
   - Language 字段应显示"简体中文"

---

**配置完成时间**: 2026-02-24
**当前默认语言**: 简体中文 (zh)
**系统版本**: Frappe 15.x + LMS
