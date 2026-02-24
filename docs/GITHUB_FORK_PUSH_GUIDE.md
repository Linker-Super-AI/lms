# GitHub Fork 和推送完整指南

## 📋 第一步：Fork 仓库

### 1.1 访问官方仓库

在浏览器中打开：
```
https://github.com/frappe/lms
```

### 1.2 点击 Fork 按钮

- 在页面右上角找到「**Fork**」按钮
- 点击它

```
页面布局：
┌─────────────────────────────────────────────────┐
│  frappe / lms                    🌟 Star  🍴 Fork │
└─────────────────────────────────────────────────┘
                                      ↑
                                 点击这里
```

### 1.3 选择 Fork 目标

- 选择你的账号（会显示你的用户名）
- 点击「Create fork」
- 等待几秒钟

### 1.4 Fork 完成

完成后会自动跳转到你的 Fork 仓库，地址格式：
```
https://github.com/YOUR-USERNAME/lms
```

**例如：**
- 如果你的用户名是 `zhangsan`，地址就是：`https://github.com/zhangsan/lms`
- 如果你的用户名是 `linker-dev`，地址就是：`https://github.com/linker-dev/lms`

---

## 📤 第二步：推送代码到你的 Fork

### 方法1：使用自动脚本（推荐）

```bash
cd /home/services/lms

# 运行推送脚本
./PUSH_TO_GITHUB.sh

# 脚本会提示输入 GitHub 用户名
# 然后自动推送代码
```

### 方法2：手动操作

#### 2.1 添加你的远程仓库

**替换 `YOUR-USERNAME` 为你的 GitHub 用户名：**

```bash
cd /home/services/lms

# 添加你的 fork 为远程仓库（命名为 myfork）
git remote add myfork https://github.com/YOUR-USERNAME/lms.git

# 查看所有远程仓库
git remote -v
```

**应该看到：**
```
origin    https://github.com/frappe/lms.git (fetch)
origin    https://github.com/frappe/lms.git (push)
myfork    https://github.com/YOUR-USERNAME/lms.git (fetch)
myfork    https://github.com/YOUR-USERNAME/lms.git (push)
```

#### 2.2 推送代码

```bash
# 推送 custom-dev 分支到你的 fork
git push -u myfork custom-dev
```

**首次推送会提示输入 GitHub 凭据：**

```
Username for 'https://github.com': YOUR-USERNAME
Password for 'https://YOUR-USERNAME@github.com':
```

**⚠️ 注意：**
- **Password** 不是你的 GitHub 登录密码
- 需要使用 **Personal Access Token**（个人访问令牌）

---

## 🔑 第三步：创建 GitHub Personal Access Token

如果推送时提示需要密码，需要创建 Token：

### 3.1 访问 GitHub Settings

1. 登录 GitHub
2. 点击右上角头像 → **Settings**
3. 左侧菜单最下方 → **Developer settings**
4. 左侧菜单 → **Personal access tokens** → **Tokens (classic)**
5. 点击 **Generate new token** → **Generate new token (classic)**

### 3.2 配置 Token

**Note (描述):** `LMS Development`

**Expiration (过期时间):** 选择 `90 days` 或 `No expiration`

**Select scopes (权限):** 勾选：
- ✅ `repo` (完整的仓库权限)

### 3.3 生成并保存

1. 点击页面底部 **Generate token**
2. **⚠️ 复制生成的 token（只显示一次！）**
3. 保存到安全的地方

### 3.4 使用 Token 推送

```bash
# 推送时使用 token 作为密码
git push -u myfork custom-dev

# 提示输入时：
Username: YOUR-USERNAME
Password: [粘贴你的 token]
```

---

## 🔐 第四步：使用 SSH 密钥（可选，更方便）

### 4.1 生成 SSH 密钥

```bash
# 生成密钥
ssh-keygen -t ed25519 -C "your-email@example.com"

# 一路回车，使用默认设置

# 查看公钥
cat ~/.ssh/id_ed25519.pub
```

### 4.2 添加 SSH 密钥到 GitHub

1. 复制公钥内容
2. 访问 GitHub → Settings → SSH and GPG keys
3. 点击 **New SSH key**
4. **Title:** `LMS Server`
5. **Key:** 粘贴公钥内容
6. 点击 **Add SSH key**

### 4.3 修改远程仓库 URL 为 SSH

```bash
# 修改 myfork 的 URL
git remote set-url myfork git@github.com:YOUR-USERNAME/lms.git

# 验证
git remote -v
```

### 4.4 推送（不需要密码）

```bash
git push -u myfork custom-dev
# ✅ 不会要求输入密码！
```

---

## 👀 第五步：查看你的仓库

### 5.1 访问你的 Fork 仓库

浏览器打开：
```
https://github.com/YOUR-USERNAME/lms
```

### 5.2 切换到 custom-dev 分支

在仓库页面：
1. 点击左上角的分支下拉菜单（默认显示 `main` 或 `develop`）
2. 选择 `custom-dev`

或直接访问：
```
https://github.com/YOUR-USERNAME/lms/tree/custom-dev
```

### 5.3 查看你的提交

点击仓库页面的 **Commits** 链接，应该能看到：

```
✓ e4ee108c docs: 添加二次开发快速开始指南
✓ 0fa2a773 docs: 添加 Fork 指南和完整使用文档
✓ c352c086 feat: 初始定制化配置和功能增强
```

### 5.4 查看代码

你可以在 GitHub 上直接浏览：
- `docs/` - 所有文档
- `scripts/` - 所有脚本
- `docker-compose-prod.yml` - 生产配置
- `README_CUSTOM.md` - 总索引

---

## 📊 验证推送成功

### 在服务器上验证

```bash
# 查看远程分支
git branch -r

# 应该看到：
# origin/develop
# myfork/custom-dev

# 查看推送记录
git log origin/develop..custom-dev --oneline
```

### 在 GitHub 上验证

访问你的仓库，应该能看到：

```
┌─────────────────────────────────────────────┐
│ YOUR-USERNAME / lms                          │
│                                              │
│ Forked from frappe/lms                       │
│                                              │
│ [custom-dev ▼]  📁 Code  📊 47 commits      │
│                                              │
│ ✓ docs: 添加二次开发快速开始指南              │
│ ✓ docs: 添加 Fork 指南和完整使用文档          │
│ ✓ feat: 初始定制化配置和功能增强              │
└─────────────────────────────────────────────┘
```

---

## 🔄 日常工作流程

### 推送新的修改

```bash
# 1. 修改代码
nano lms/lms/...

# 2. 提交
git add .
git commit -m "feat: 新功能"

# 3. 推送到 GitHub
git push myfork custom-dev

# ✅ 几秒钟后就能在 GitHub 上看到！
```

### 从 GitHub 拉取更新

```bash
# 如果你在其他地方修改了代码
git pull myfork custom-dev
```

---

## 🌐 在其他服务器部署

### 克隆你的 Fork

```bash
# 在新服务器上
git clone https://github.com/YOUR-USERNAME/lms.git
cd lms

# 切换到开发分支
git checkout custom-dev

# 启动服务
docker compose -f docker-compose-prod.yml up -d

# ✅ 所有配置和代码都一样！
```

---

## 👥 团队协作

### 邀请团队成员

1. 访问你的 Fork 仓库
2. **Settings** → **Collaborators**
3. 点击 **Add people**
4. 输入团队成员的 GitHub 用户名
5. 选择权限（Write 或 Admin）

### 团队成员克隆

```bash
git clone https://github.com/YOUR-USERNAME/lms.git
cd lms
git checkout custom-dev

# 可以推送修改
git push origin custom-dev
```

---

## 🔍 查看仓库的其他方式

### 1. GitHub Desktop（图形界面）

下载：https://desktop.github.com/

使用：
1. File → Clone Repository
2. 输入：`YOUR-USERNAME/lms`
3. 选择本地路径
4. Clone

### 2. VS Code

1. 安装 GitHub Pull Requests 插件
2. 命令面板：`Git: Clone`
3. 输入：`https://github.com/YOUR-USERNAME/lms`

### 3. 网页浏览

**直接在 GitHub 网页上：**
- 浏览代码
- 查看提交历史
- 查看修改差异
- 下载 ZIP 文件

---

## 📋 快速参考

### 常用命令

```bash
# 查看远程仓库
git remote -v

# 推送代码
git push myfork custom-dev

# 拉取更新
git pull myfork custom-dev

# 查看推送状态
git status

# 查看提交历史
git log --oneline -10
```

### 重要 URL

| 项目 | URL |
|------|-----|
| Frappe 官方仓库 | https://github.com/frappe/lms |
| 你的 Fork | https://github.com/YOUR-USERNAME/lms |
| custom-dev 分支 | https://github.com/YOUR-USERNAME/lms/tree/custom-dev |
| 提交历史 | https://github.com/YOUR-USERNAME/lms/commits/custom-dev |

---

## ❓ 常见问题

### Q: 推送时提示 "Permission denied"？

**A:** 需要创建 Personal Access Token 或配置 SSH 密钥。

### Q: 忘记 GitHub 用户名？

**A:** 访问 https://github.com/settings/profile 查看。

### Q: 如何删除错误的远程仓库？

```bash
git remote remove myfork
# 然后重新添加正确的
```

### Q: 推送失败怎么办？

```bash
# 查看详细错误
git push myfork custom-dev --verbose

# 强制推送（⚠️ 谨慎使用）
git push -f myfork custom-dev
```

### Q: 如何更新 Fork 仓库？

```bash
# 同步官方仓库的更新
git checkout develop
git pull origin develop
git checkout custom-dev
git merge develop
git push myfork custom-dev
```

---

## ✅ 检查清单

推送成功后，确认：

- [ ] 能访问你的 Fork：`https://github.com/YOUR-USERNAME/lms`
- [ ] 能看到 custom-dev 分支
- [ ] 能看到所有提交记录（3个定制提交）
- [ ] 能看到 docs/ 和 scripts/ 目录
- [ ] 能看到 README_CUSTOM.md 文件

---

**完成！现在你的代码已经安全备份到 GitHub 了！** 🎉

任何时候都可以：
- 在 GitHub 网页上查看代码
- 在其他服务器克隆部署
- 与团队成员协作
- 保留完整的版本历史
