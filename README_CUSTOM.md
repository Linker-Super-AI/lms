# LMS 定制版 - 完整使用指南

> 基于 Frappe LMS 的定制化学习管理系统
> 包含：中文化、批量用户管理、防复制保护、视频支持等功能

---

## 🚀 快速开始

### 当前环境信息

```
访问地址：http://192.168.20.118:8001
管理后台：http://192.168.20.118:8001/app
登录页面：http://192.168.20.118:8001/login

默认管理员：Administrator
课程 ID：uf67dh57kl（一周学习版）
```

### 已部署的服务

| 服务 | 端口 | 说明 |
|------|------|------|
| LMS Web | 8001 | 主应用（nginx 代理） |
| LMS Backend | 9002 | 后端 API |
| MariaDB | 3307 | 数据库 |
| Redis | 6380 | 缓存 |

---

## 📚 完整文档索引

### 🎯 快速入门

| 文档 | 说明 | 位置 |
|------|------|------|
| **FORK_AND_SYNC_GUIDE.md** | Fork 仓库和代码同步指南 ⭐ | `docs/` |
| **CUSTOM_DEVELOPMENT_GUIDE.md** | 二次开发完整指南 ⭐ | `docs/` |
| **QUICK_START_BATCH_USERS.md** | 5分钟快速批量添加用户 ⭐ | `docs/` |

### 👥 用户管理

| 文档 | 说明 |
|------|------|
| **USER_MANAGEMENT.md** | 用户管理完整指南 |
| **BATCH_USER_IMPORT.md** | 批量导入用户详细教程 |
| **SIGNUP_ISSUE_SOLUTION.md** | 注册页面问题说明 |

### 📹 内容管理

| 文档 | 说明 |
|------|------|
| **VIDEO_UPLOAD_GUIDE.md** | 视频添加完整指南（YouTube/Bilibili/自托管） |
| **IMAGE_UPLOAD_FIX.md** | 图片上传配置和使用 |

### 🐛 问题修复

| 文档 | 说明 |
|------|------|
| **DATAERROR_FIX.md** | 保存错误（字段大小限制）修复 |
| **EMAIL_SETUP.md** | 邮件服务器配置（可选） |

### 📦 部署相关

根目录文件：
- `DEPLOYMENT_SUMMARY.md` - 部署总结
- `CHINESE_LANGUAGE_SETUP.md` - 中文化配置
- `LAN_ACCESS_READY.md` - 局域网访问说明
- `QUICK_ACCESS_GUIDE.md` - 快速访问指南

---

## 🎯 主要功能

### ✅ 已实现的定制功能

1. **中文化**
   - ✅ 系统界面中文
   - ✅ 完整中文文档
   - ✅ 用户默认语言设置

2. **用户管理**
   - ✅ 批量用户导入（CSV）
   - ✅ 用户密码管理
   - ✅ 课程自动注册
   - ✅ 自助注册已禁用（管理员创建）

3. **课程管理**
   - ✅ Markdown 格式导入
   - ✅ Word 文档解析
   - ✅ 章节课时层级
   - ✅ 内容格式保留

4. **内容保护**
   - ✅ 防复制（CSS + JS）
   - ✅ 禁用右键、打印
   - ✅ 水印和版权声明
   - ✅ 禁用开发者工具

5. **多媒体支持**
   - ✅ YouTube 视频
   - ✅ Bilibili 等平台
   - ✅ 图片上传显示
   - ✅ 自托管视频

6. **Bug 修复**
   - ✅ 图片显示问题
   - ✅ 内容字段大小限制
   - ✅ 静态文件访问
   - ✅ 端口冲突解决

---

## 🛠️ 常用操作

### 批量添加用户

```bash
# 1. 编辑 CSV 模板
nano /home/services/lms/data/users_template.csv

# 格式：
# email,first_name,last_name,password
# user@example.com,张三,,Password@2024

# 2. 导入用户
cd /home/services/lms
docker compose -f docker-compose-prod.yml cp data/users_template.csv lms:/home/frappe/frappe-bench/sites/data/
docker compose -f docker-compose-prod.yml exec -T lms \
  bench --site 192.168.20.118 console < scripts/batch_create_users.py
```

**详细文档：** `docs/QUICK_START_BATCH_USERS.md`

### 为课时添加视频

**方式1：YouTube（推荐）**
1. 上传视频到 YouTube（设置为不公开）
2. 后台编辑课时：`http://192.168.20.118:8001/app/course-lesson/[name]`
3. 在「YouTube Video URL」字段粘贴链接
4. 保存

**方式2：其他平台**
在课时内容中使用 iframe：
```html
<iframe src="视频嵌入链接" width="100%" height="500"></iframe>
```

**详细文档：** `docs/VIDEO_UPLOAD_GUIDE.md`

### 服务管理

```bash
# 查看服务状态
docker compose -f docker-compose-prod.yml ps

# 重启服务
docker compose -f docker-compose-prod.yml restart

# 查看日志
docker compose -f docker-compose-prod.yml logs -f lms

# 停止服务
docker compose -f docker-compose-prod.yml down

# 启动服务
docker compose -f docker-compose-prod.yml up -d
```

### 清除缓存

```bash
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache
```

### 数据库备份

```bash
# 备份
docker compose -f docker-compose-prod.yml exec mariadb \
  mysqldump -u root -padmin _28befd2a5cb08663 > backup_$(date +%Y%m%d).sql

# 压缩
gzip backup_$(date +%Y%m%d).sql

# 恢复
gunzip backup_20260224.sql.gz
docker compose -f docker-compose-prod.yml exec -T mariadb \
  mysql -u root -padmin _28befd2a5cb08663 < backup_20260224.sql
```

---

## 🌐 Fork 和部署

### Fork 到你的 GitHub

1. **Fork 官方仓库**
   ```
   访问：https://github.com/frappe/lms
   点击：Fork 按钮
   ```

2. **添加你的远程仓库**
   ```bash
   cd /home/services/lms
   git remote add myfork https://github.com/YOUR-USERNAME/lms.git
   ```

3. **推送代码**
   ```bash
   git push myfork custom-dev
   ```

4. **在其他服务器部署**
   ```bash
   # 克隆你的 fork
   git clone https://github.com/YOUR-USERNAME/lms.git
   cd lms
   git checkout custom-dev

   # 启动服务
   docker compose -f docker-compose-prod.yml up -d
   ```

**✅ 优点：**
- 一次配置，到处部署
- 团队成员共享配置
- 代码安全备份到 GitHub

**详细文档：** `docs/FORK_AND_SYNC_GUIDE.md`

---

## 🔧 二次开发

### 当前分支结构

```
* custom-dev          # 你的主开发分支（当前）
  develop            # Frappe 官方 develop 分支
```

### 开发工作流

1. **创建功能分支**
   ```bash
   git checkout custom-dev
   git checkout -b feature/new-feature
   ```

2. **修改代码**
   ```bash
   # 编辑文件...
   nano lms/lms/doctype/...

   # 测试
   docker compose restart lms
   ```

3. **提交修改**
   ```bash
   git add .
   git commit -m "feat: 新功能"
   git push myfork feature/new-feature
   ```

4. **合并到主分支**
   ```bash
   git checkout custom-dev
   git merge feature/new-feature
   git push myfork custom-dev
   ```

### 同步上游更新

```bash
# 拉取官方最新代码
git checkout develop
git pull origin develop

# 合并到你的分支
git checkout custom-dev
git merge develop
git push myfork custom-dev
```

**详细文档：** `docs/CUSTOM_DEVELOPMENT_GUIDE.md`

---

## 📋 目录结构

```
/home/services/lms/
├── docker-compose-prod.yml    # 生产环境配置 ⭐
├── docker/
│   ├── nginx.conf             # Nginx 配置（静态文件）⭐
│   ├── docker-compose.yml     # 开发环境配置
│   └── init.sh
├── docs/                      # 完整中文文档 ⭐
│   ├── FORK_AND_SYNC_GUIDE.md
│   ├── CUSTOM_DEVELOPMENT_GUIDE.md
│   ├── QUICK_START_BATCH_USERS.md
│   ├── USER_MANAGEMENT.md
│   ├── VIDEO_UPLOAD_GUIDE.md
│   ├── IMAGE_UPLOAD_FIX.md
│   ├── DATAERROR_FIX.md
│   └── ...
├── scripts/                   # 管理脚本 ⭐
│   ├── batch_create_users.py         # 批量创建用户
│   ├── set_user_password.py          # 设置密码
│   ├── create_course_with_markdown.py # 创建课程
│   ├── apply_copy_protection.py      # 防复制保护
│   └── ...
├── data/                      # 数据模板 ⭐
│   ├── users_template.csv     # 用户导入模板
│   └── users_demo.csv
├── lms/                       # LMS 应用源代码
│   ├── lms/
│   │   ├── doctype/
│   │   ├── api/
│   │   └── ...
│   └── ...
└── README_CUSTOM.md           # 本文档 ⭐
```

---

## 🎓 使用场景

### 场景1：企业内部培训

1. 批量导入员工账号（CSV）
2. 创建培训课程（Markdown）
3. 添加视频教程（YouTube/自托管）
4. 启用防复制保护
5. 跟踪学习进度

### 场景2：在线课程平台

1. Fork 仓库到自己账号
2. 添加品牌定制
3. 配置支付功能（可选）
4. 部署到云服务器
5. 持续更新内容

### 场景3：学校教学系统

1. 批量导入学生账号
2. 按班级/课程组织
3. 教师创建课程内容
4. 学生在线学习
5. 考试和证书

---

## ⚙️ 高级配置

### 启用邮件服务器

参考：`docs/EMAIL_SETUP.md`

配置后可以：
- 发送欢迎邮件
- 密码重置
- 课程通知
- 证书发放

### 自定义域名

1. **配置 DNS**
   ```
   A 记录：lms.yourdomain.com → 192.168.20.118
   ```

2. **修改 nginx 配置**
   ```nginx
   server_name lms.yourdomain.com;
   ```

3. **配置 SSL（推荐）**
   ```bash
   # 使用 Let's Encrypt
   certbot --nginx -d lms.yourdomain.com
   ```

### 集成 SSO

Frappe 支持：
- LDAP/Active Directory
- SAML
- OAuth (Google, GitHub, etc.)

参考 Frappe 官方文档配置。

---

## 🐛 问题排查

### 服务无法启动

```bash
# 查看日志
docker compose -f docker-compose-prod.yml logs

# 检查端口占用
netstat -tlnp | grep -E '8001|9002|3307|6380'

# 重新构建
docker compose -f docker-compose-prod.yml up -d --build
```

### 图片无法显示

1. 检查 nginx 配置是否有 `/files` 路径
2. 重启 nginx：`docker compose restart nginx`
3. 查看 nginx 日志：`docker compose logs nginx`

参考：`docs/IMAGE_UPLOAD_FIX.md`

### 保存内容报错 DataError

已修复，content 字段已改为 LONGTEXT。

如仍有问题，参考：`docs/DATAERROR_FIX.md`

### 用户无法登录

1. 检查密码是否正确
2. 确认用户类型是「Website User」
3. 查看用户是否已启用
4. 重置密码：`scripts/set_user_password.py`

参考：`docs/USER_MANAGEMENT.md`

---

## 📞 获取帮助

### 文档位置

所有文档都在 `/home/services/lms/docs/` 目录下，可以用任何文本编辑器查看：

```bash
# 查看文档列表
ls -1 docs/

# 查看某个文档
cat docs/VIDEO_UPLOAD_GUIDE.md
# 或
nano docs/VIDEO_UPLOAD_GUIDE.md
```

### 官方资源

- **Frappe 文档：** https://frappeframework.com/docs
- **LMS 仓库：** https://github.com/frappe/lms
- **Frappe 论坛：** https://discuss.frappe.io/

### 社区支持

- **GitHub Issues：** 报告 bug 和功能请求
- **讨论区：** 技术讨论和问答

---

## ✅ 完成检查清单

### 基础功能

- [x] 系统已部署并运行
- [x] 中文界面已配置
- [x] 课程已创建（uf67dh57kl）
- [x] 防复制保护已启用
- [x] 图片上传已修复
- [x] 内容字段大小已修复

### 用户管理

- [x] 批量用户导入脚本
- [x] 用户密码管理
- [x] 自助注册已禁用
- [x] 测试用户已创建

### 二次开发

- [x] Git 分支已创建（custom-dev）
- [x] 所有修改已提交
- [x] 文档已完善
- [ ] 代码已推送到 GitHub（待操作）

### 可选配置

- [ ] Fork 仓库到 GitHub
- [ ] 配置邮件服务器
- [ ] 配置自定义域名
- [ ] 配置 SSL 证书
- [ ] 集成 SSO

---

## 🎉 开始使用

### 管理员

1. 访问后台：http://192.168.20.118:8001/app
2. 管理用户、课程、内容
3. 查看统计数据

### 学员

1. 访问登录页：http://192.168.20.118:8001/login
2. 使用管理员提供的账号密码登录
3. 访问课程：http://192.168.20.118:8001/courses/uf67dh57kl
4. 开始学习

---

**祝您使用愉快！** 🚀

如有问题，请查阅 `docs/` 目录下的详细文档。
