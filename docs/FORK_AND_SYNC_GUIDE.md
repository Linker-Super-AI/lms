# Fork 仓库并同步代码指南

## 🍴 Fork 官方仓库

### 步骤1：在 GitHub 上 Fork

1. **访问官方仓库**
   ```
   https://github.com/frappe/lms
   ```

2. **点击右上角「Fork」按钮**
   - 等待几秒钟
   - Fork 会出现在你的 GitHub 账号下
   - 地址格式：`https://github.com/your-username/lms`

3. **Fork 完成后**
   - 你会被重定向到你的 Fork 仓库
   - 这个仓库完全属于你，可以任意修改

---

## 🔗 添加你的 Fork 为远程仓库

### 在服务器上操作

```bash
cd /home/services/lms

# 添加你的 fork 为远程仓库（命名为 myfork）
git remote add myfork https://github.com/YOUR-USERNAME/lms.git

# 查看所有远程仓库
git remote -v

# 应该看到：
# origin    https://github.com/frappe/lms.git (fetch)
# origin    https://github.com/frappe/lms.git (push)
# myfork    https://github.com/YOUR-USERNAME/lms.git (fetch)
# myfork    https://github.com/YOUR-USERNAME/lms.git (push)
```

**说明：**
- `origin`：Frappe 官方仓库（只读，用于同步上游更新）
- `myfork`：你的 Fork 仓库（可读写，存储你的修改）

---

## 📤 推送代码到你的 Fork

### 首次推送

```bash
# 确保在 custom-dev 分支
git checkout custom-dev

# 推送到你的 fork（设置上游分支）
git push -u myfork custom-dev

# 输出示例：
# Enumerating objects: 100, done.
# Counting objects: 100% (100/100), done.
# Writing objects: 100% (100/100), 250 KiB | 5 MiB/s, done.
# Total 100 (delta 50), reused 0 (delta 0)
# To https://github.com/YOUR-USERNAME/lms.git
#  * [new branch]      custom-dev -> custom-dev
```

### 日常推送

以后每次提交后：

```bash
# 提交修改
git add .
git commit -m "feat: 添加新功能"

# 推送到你的 fork
git push myfork custom-dev

# 或简写（已设置上游分支）
git push
```

---

## 🔄 同步工作流

### 完整的工作流程

```
┌─────────────────────────────────────────┐
│  Frappe 官方仓库 (origin)                │
│  github.com/frappe/lms                  │
└─────────────┬───────────────────────────┘
              │ fork
              ▼
┌─────────────────────────────────────────┐
│  你的 Fork 仓库 (myfork)                 │
│  github.com/your-username/lms           │
└─────────────┬───────────────────────────┘
              │ clone/pull/push
              ▼
┌─────────────────────────────────────────┐
│  本地服务器                              │
│  /home/services/lms                     │
└─────────────────────────────────────────┘
```

### 日常开发

1. **在本地修改代码**
   ```bash
   cd /home/services/lms
   git checkout custom-dev

   # 修改代码...
   nano lms/lms/doctype/...

   # 测试
   docker compose restart lms
   ```

2. **提交修改**
   ```bash
   git add .
   git commit -m "feat: 新功能"
   ```

3. **推送到你的 Fork**
   ```bash
   git push myfork custom-dev
   ```

4. **在 GitHub 上查看**
   - 访问你的 Fork：`https://github.com/your-username/lms`
   - 应该能看到最新的提交

---

## 🔄 同步上游更新

### 定期同步 Frappe 官方的更新

```bash
cd /home/services/lms

# 1. 切换到 develop 分支
git checkout develop

# 2. 拉取官方最新代码
git pull origin develop

# 3. 切换回你的开发分支
git checkout custom-dev

# 4. 合并官方更新
git merge develop

# 5. 如果有冲突，解决后提交
git add .
git commit -m "merge: 同步上游更新"

# 6. 推送到你的 fork
git push myfork custom-dev
```

### 在 GitHub 上同步（Web 界面）

1. 访问你的 Fork 仓库
2. 点击「Sync fork」按钮
3. 点击「Update branch」
4. 在本地拉取：
   ```bash
   git pull myfork custom-dev
   ```

---

## 🌐 在其他服务器部署

### 场景：在另一台服务器上部署相同的配置

```bash
# 在新服务器上

# 1. 克隆你的 fork
git clone https://github.com/your-username/lms.git
cd lms

# 2. 切换到开发分支
git checkout custom-dev

# 3. 启动服务
docker compose -f docker-compose-prod.yml up -d

# 4. 初始化（如果需要）
# 按照 DEPLOYMENT_SUMMARY.md 操作

# 5. 配置（参考 docs/ 中的文档）
```

**✅ 优点：**
- 一次配置，到处部署
- 所有定制化配置都在代码库中
- 团队成员可以共享相同的配置

---

## 👥 团队协作

### 添加团队成员

1. **在 GitHub 上添加协作者**
   - 访问你的 Fork 仓库
   - Settings → Collaborators
   - 添加团队成员的 GitHub 账号

2. **团队成员克隆仓库**
   ```bash
   git clone https://github.com/your-username/lms.git
   cd lms
   git checkout custom-dev
   ```

3. **团队成员提交修改**
   ```bash
   # 修改代码
   git add .
   git commit -m "feat: 团队成员的修改"
   git push origin custom-dev
   ```

### 使用 Pull Request

**推荐的协作方式：**

1. **团队成员创建功能分支**
   ```bash
   git checkout custom-dev
   git checkout -b feature/new-feature

   # 开发...
   git add .
   git commit -m "feat: 新功能"

   # 推送到自己的分支
   git push origin feature/new-feature
   ```

2. **在 GitHub 上创建 Pull Request**
   - 访问你的 Fork 仓库
   - 点击「Compare & pull request」
   - Base: `custom-dev` ← Compare: `feature/new-feature`
   - 描述修改内容
   - 创建 PR

3. **代码审查和合并**
   - 团队负责人审查代码
   - 讨论和修改
   - 合并到 `custom-dev`

---

## 🔐 使用 SSH 密钥（推荐）

### 避免每次输入密码

1. **生成 SSH 密钥**
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   # 一路回车，使用默认路径
   ```

2. **查看公钥**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. **添加到 GitHub**
   - 访问 GitHub Settings → SSH and GPG keys
   - 点击「New SSH key」
   - 粘贴公钥内容
   - 保存

4. **修改远程仓库 URL**
   ```bash
   # 查看当前 URL
   git remote -v

   # 修改为 SSH URL
   git remote set-url myfork git@github.com:your-username/lms.git

   # 验证
   git remote -v
   ```

5. **测试**
   ```bash
   git push myfork custom-dev
   # 不再需要输入密码！
   ```

---

## 📦 备份策略

### 多重备份

```
┌─────────────────────────────────────────┐
│  GitHub Fork (云端主备份)                │
│  github.com/your-username/lms           │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┴─────────┬─────────────┐
    ▼                   ▼             ▼
┌─────────┐      ┌─────────┐   ┌─────────┐
│生产服务器│      │开发服务器│   │本地电脑 │
└─────────┘      └─────────┘   └─────────┘
```

### 定期备份

```bash
# 方式1：推送到 GitHub（已自动备份）
git push myfork custom-dev

# 方式2：导出到文件
git bundle create lms-backup-$(date +%Y%m%d).bundle --all

# 方式3：打包
tar -czf lms-$(date +%Y%m%d).tar.gz \
  --exclude='.git' \
  --exclude='node_modules' \
  /home/services/lms/

# 下载到本地
scp root@192.168.20.118:/home/services/lms-*.tar.gz ./
```

---

## 🚀 CI/CD（可选）

### 使用 GitHub Actions 自动部署

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Production

on:
  push:
    branches: [ custom-dev ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: 192.168.20.118
          username: root
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/services/lms
            git pull myfork custom-dev
            docker compose -f docker-compose-prod.yml restart
```

**配置：**
1. GitHub Settings → Secrets → Add secret
2. 添加 `SSH_PRIVATE_KEY`
3. 每次推送代码会自动部署

---

## 📋 快速参考

### 常用命令

```bash
# 查看状态
git status

# 查看远程仓库
git remote -v

# 拉取更新
git pull myfork custom-dev

# 推送代码
git push myfork custom-dev

# 同步上游
git checkout develop
git pull origin develop
git checkout custom-dev
git merge develop
git push myfork custom-dev

# 查看提交历史
git log --oneline -10

# 查看分支
git branch -a
```

### 解决常见问题

**问题1：推送被拒绝**
```bash
# 先拉取
git pull myfork custom-dev --rebase

# 再推送
git push myfork custom-dev
```

**问题2：忘记分支名**
```bash
# 查看所有分支
git branch -a

# 查看当前分支
git branch
```

**问题3：需要撤销修改**
```bash
# 撤销工作区修改
git restore <file>

# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1
```

---

## ✅ 检查清单

部署到新服务器时：

- [ ] Fork 官方仓库
- [ ] 在服务器上克隆你的 fork
- [ ] 切换到 custom-dev 分支
- [ ] 运行 docker-compose-prod.yml
- [ ] 参考 docs/ 中的文档配置
- [ ] 测试所有功能
- [ ] 定期推送代码到 GitHub

---

## 📞 相关资源

- **GitHub 文档：** https://docs.github.com/
- **Git 教程：** https://git-scm.com/book/zh/v2
- **二次开发指南：** `/home/services/lms/docs/CUSTOM_DEVELOPMENT_GUIDE.md`

---

**现在你的代码已经安全备份到 GitHub，可以随时在任何地方部署！** 🎉
