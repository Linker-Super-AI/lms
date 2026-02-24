# LMS 二次开发指南

## 📋 当前状态

### Git 仓库信息
- **原始仓库：** https://github.com/frappe/lms.git
- **当前分支：** develop
- **本地修改：** 大量配置和脚本文件

### 已有的定制内容
```
新增文件/目录：
- docker-compose-prod.yml（生产环境配置）
- docker/nginx.conf（Nginx 配置）
- scripts/（批量用户管理、课程创建等脚本）
- docs/（完整的中文文档）
- data/（用户数据模板）

修改文件：
- docker/docker-compose.yml
- docker/init.sh
```

---

## 🚀 开始二次开发

### 方案1：基于当前仓库创建开发分支（推荐）

这种方式可以方便地同步上游更新。

#### 步骤1：创建自己的开发分支

```bash
cd /home/services/lms

# 创建并切换到新分支（基于当前的 develop）
git checkout -b custom-dev

# 查看状态
git status
```

#### 步骤2：提交所有当前的修改

```bash
# 添加所有新文件和修改
git add .

# 查看将要提交的内容
git status

# 提交（建议详细说明）
git commit -m "feat: 初始二次开发配置

- 添加生产环境 docker-compose 配置
- 添加 nginx 静态文件服务
- 添加批量用户管理脚本
- 添加课程内容导入脚本
- 添加完整中文文档
- 修复图片上传和内容字段大小限制
- 添加防复制保护功能
- 禁用自助注册功能
"

# 查看提交历史
git log --oneline -5
```

#### 步骤3：创建远程仓库（可选）

**方式A：使用 GitHub/GitLab**

1. 在 GitHub/GitLab 创建新仓库，例如：
   ```
   https://github.com/your-username/lms-custom.git
   ```

2. 添加远程仓库：
   ```bash
   # 添加自己的远程仓库
   git remote add custom https://github.com/your-username/lms-custom.git

   # 推送到自己的仓库
   git push -u custom custom-dev

   # 查看远程仓库
   git remote -v
   ```

   现在你有两个远程仓库：
   - `origin`: Frappe 官方仓库（只读，用于同步更新）
   - `custom`: 你的仓库（可读写，存储你的修改）

**方式B：使用 Gitea/GitLab 自建**

如果想完全私有化：

```bash
# 假设你在内网搭建了 Gitea
git remote add custom http://git.linker.net/lms-custom.git
git push -u custom custom-dev
```

---

### 方案2：Fork 官方仓库（适合长期维护）

1. **Fork 官方仓库**
   - 访问：https://github.com/frappe/lms
   - 点击右上角「Fork」
   - Fork 到你的账号下

2. **修改本地远程仓库**
   ```bash
   cd /home/services/lms

   # 保存当前修改
   git stash

   # 添加你的 fork 为远程仓库
   git remote add myfork https://github.com/your-username/lms.git

   # 拉取你的 fork
   git fetch myfork

   # 创建开发分支
   git checkout -b custom-dev

   # 恢复修改
   git stash pop

   # 提交修改
   git add .
   git commit -m "feat: 初始定制化配置"

   # 推送到你的 fork
   git push -u myfork custom-dev
   ```

---

## 🔧 日常开发工作流

### 1. 进行修改

```bash
# 切换到开发分支
git checkout custom-dev

# 修改代码...
nano lms/lms/doctype/...

# 查看修改
git status
git diff

# 提交修改
git add .
git commit -m "feat: 添加新功能"

# 推送到远程
git push custom custom-dev
```

### 2. 同步上游更新

定期同步 Frappe 官方的更新：

```bash
# 切换到 develop 分支
git checkout develop

# 从官方仓库拉取最新代码
git pull origin develop

# 切换回你的开发分支
git checkout custom-dev

# 合并官方更新（可能需要解决冲突）
git merge develop

# 如果有冲突，解决后：
git add .
git commit -m "merge: 同步上游更新"

# 推送
git push custom custom-dev
```

### 3. 管理多个功能分支

```bash
# 为新功能创建分支
git checkout -b feature/video-upload
# 开发...
git commit -m "feat: 添加视频批量上传"
git push custom feature/video-upload

# 为 bug 修复创建分支
git checkout custom-dev
git checkout -b fix/user-login-issue
# 修复...
git commit -m "fix: 修复用户登录问题"
git push custom fix/user-login-issue

# 合并到主开发分支
git checkout custom-dev
git merge feature/video-upload
git push custom custom-dev
```

---

## 📦 管理自定义代码

### 推荐的目录结构

将自定义代码放在特定目录，便于管理：

```
/home/services/lms/
├─ custom/                    # 自定义代码目录（新建）
│   ├─ scripts/              # 自定义脚本
│   ├─ fixtures/             # 自定义数据
│   ├─ apps/                 # 自定义应用（如需要）
│   └─ patches/              # 数据库补丁
├─ scripts/                  # ✅ 已有（批量用户等）
├─ docs/                     # ✅ 已有（中文文档）
├─ data/                     # ✅ 已有（用户模板）
└─ docker-compose-prod.yml   # ✅ 已有（生产配置）
```

### .gitignore 配置

创建或修改 `.gitignore`，排除不需要版本控制的文件：

```bash
cat >> .gitignore <<'EOF'

# 自定义配置
/custom/local_config.py
*.local

# 数据文件
/data/*.csv
!/data/users_template.csv

# 临时文件
/tmp/
*.tmp
*.log

# 环境变量
.env.local
EOF

git add .gitignore
git commit -m "chore: 更新 gitignore"
```

---

## 🔄 版本管理策略

### 分支策略

```
master/main          # 生产环境（稳定版本）
  └─ develop         # 开发主分支
       └─ custom-dev # 你的主开发分支 ⭐
            ├─ feature/xxx  # 功能分支
            ├─ fix/xxx      # 修复分支
            └─ hotfix/xxx   # 紧急修复
```

### 提交规范

使用语义化提交信息：

```bash
# 新功能
git commit -m "feat(user): 添加批量用户导入功能"

# Bug 修复
git commit -m "fix(course): 修复内容字段大小限制"

# 文档
git commit -m "docs: 添加视频上传指南"

# 配置
git commit -m "chore(docker): 更新 nginx 配置"

# 重构
git commit -m "refactor(scripts): 优化用户创建脚本"

# 性能优化
git commit -m "perf(database): 优化课程查询性能"
```

---

## 🛠️ 常见开发任务

### 1. 添加新的 DocType

```bash
# 使用 Frappe bench 命令
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 new-doctype

# 或手动创建
mkdir -p lms/lms/doctype/custom_doctype
# 创建 JSON 和 Python 文件...

# 提交
git add lms/lms/doctype/custom_doctype/
git commit -m "feat: 添加 Custom DocType"
```

### 2. 修改现有功能

```bash
# 编辑文件
nano lms/lms/doctype/course_lesson/course_lesson.py

# 测试修改
docker compose restart lms

# 提交
git add lms/lms/doctype/course_lesson/course_lesson.py
git commit -m "feat(lesson): 添加视频自动播放功能"
```

### 3. 添加自定义脚本

```bash
# 创建脚本
nano scripts/custom_feature.py

# 测试
docker compose -f docker-compose-prod.yml exec -T lms \
  bench --site 192.168.20.118 console < scripts/custom_feature.py

# 提交
git add scripts/custom_feature.py
git commit -m "feat: 添加自定义功能脚本"
```

### 4. 数据库迁移

```bash
# 创建数据库补丁
nano lms/patches/v1_0/custom_migration.py

# 在 patches.txt 中注册
echo "lms.patches.v1_0.custom_migration" >> lms/patches.txt

# 执行迁移
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 migrate

# 提交
git add lms/patches/v1_0/custom_migration.py lms/patches.txt
git commit -m "feat: 添加数据库迁移补丁"
```

---

## 📋 代码审查和测试

### 开发前检查

```bash
# 1. 确保在正确的分支
git branch

# 2. 拉取最新代码
git pull custom custom-dev

# 3. 创建功能分支
git checkout -b feature/new-feature
```

### 提交前检查

```bash
# 1. 查看修改
git status
git diff

# 2. 运行测试（如果有）
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 run-tests

# 3. 检查代码质量
# pylint, flake8 等...

# 4. 提交
git add .
git commit -m "feat: 新功能"

# 5. 推送
git push custom feature/new-feature
```

---

## 🚀 部署流程

### 开发环境

```bash
# 1. 拉取最新代码
git pull custom custom-dev

# 2. 重启服务
docker compose -f docker-compose-prod.yml restart

# 3. 清除缓存
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache

# 4. 执行迁移（如有数据库变更）
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 migrate
```

### 生产环境

```bash
# 1. 创建发布分支
git checkout custom-dev
git checkout -b release/v1.0.0

# 2. 更新版本号
# 编辑 version 文件...

# 3. 提交并打 tag
git add .
git commit -m "chore: 发布 v1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"

# 4. 推送
git push custom release/v1.0.0
git push custom v1.0.0

# 5. 在生产服务器部署
ssh production-server
cd /path/to/lms
git fetch custom
git checkout v1.0.0
docker compose down
docker compose up -d
```

---

## 🔍 查看和管理修改

### 查看提交历史

```bash
# 最近 10 次提交
git log --oneline -10

# 图形化查看分支
git log --oneline --graph --all

# 查看某个文件的历史
git log --follow -- docker/nginx.conf

# 查看某次提交的详情
git show <commit-id>
```

### 比较差异

```bash
# 查看工作区修改
git diff

# 查看暂存区修改
git diff --staged

# 比较两个分支
git diff develop..custom-dev

# 比较两个提交
git diff HEAD~1 HEAD
```

### 撤销修改

```bash
# 撤销工作区修改（未 add）
git restore <file>

# 撤销暂存（已 add，未 commit）
git restore --staged <file>

# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃修改）⚠️
git reset --hard HEAD~1
```

---

## 📦 备份和恢复

### 备份代码

```bash
# 方式1：推送到远程仓库
git push custom custom-dev

# 方式2：导出 patch
git format-patch -10  # 导出最近 10 次提交

# 方式3：打包
tar -czf lms-backup-$(date +%Y%m%d).tar.gz \
  --exclude='.git' \
  --exclude='node_modules' \
  /home/services/lms/
```

### 恢复代码

```bash
# 从远程仓库恢复
git clone https://github.com/your-username/lms-custom.git
cd lms-custom
git checkout custom-dev

# 应用 patch
git am *.patch

# 从备份恢复
tar -xzf lms-backup-20260224.tar.gz
```

---

## 🐛 问题排查

### 查看 Git 配置

```bash
# 查看所有配置
git config --list

# 查看远程仓库
git remote -v

# 查看当前分支
git branch

# 查看所有分支
git branch -a
```

### 解决合并冲突

```bash
# 合并时如果有冲突
git merge develop
# Auto-merging xxx
# CONFLICT (content): Merge conflict in xxx

# 1. 查看冲突文件
git status

# 2. 手动编辑解决冲突
nano <conflicted-file>

# 3. 标记为已解决
git add <conflicted-file>

# 4. 完成合并
git commit -m "merge: 解决合并冲突"
```

---

## 📚 推荐工具

### Git GUI 工具

- **SourceTree**（免费，功能强大）
- **GitKraken**（可视化好）
- **VS Code Git 插件**（轻量级）
- **Tower**（Mac/Windows，付费）

### 命令行工具

```bash
# 安装 tig（终端 Git 浏览器）
apt install tig

# 使用
tig  # 浏览提交历史
```

### 代码编辑器

- **VS Code**（推荐，有 Remote SSH 插件）
- **PyCharm**（Python 开发）
- **Vim/Neovim**（服务器端）

---

## ✅ 下一步

1. **立即操作：**
   ```bash
   cd /home/services/lms
   git checkout -b custom-dev
   git add .
   git commit -m "feat: 初始定制化配置"
   ```

2. **创建远程仓库（推荐）：**
   - 在 GitHub/GitLab 创建仓库
   - 推送代码
   - 设置 CI/CD（可选）

3. **开始开发：**
   - 参考本文档的工作流
   - 保持定期提交
   - 定期同步上游更新

4. **文档化：**
   - 记录你的修改
   - 更新 README
   - 编写部署文档

---

## 🔗 相关资源

### Frappe 开发文档
- https://frappeframework.com/docs/user/en/basics
- https://frappeframework.com/docs/user/en/api

### Git 学习资源
- https://git-scm.com/book/zh/v2
- https://www.atlassian.com/git/tutorials

### LMS 官方资源
- 官方仓库：https://github.com/frappe/lms
- 文档：https://docs.frappe.io/lms

---

**开始你的二次开发之旅！** 🚀
