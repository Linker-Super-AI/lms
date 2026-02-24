# 二次开发快速开始

## ✅ 当前状态

```
当前分支：custom-dev
最新提交：0fa2a773 (docs: 添加 Fork 指南和完整使用文档)
工作目录：干净（所有修改已提交）

Git 配置：
- origin: https://github.com/frappe/lms.git (Frappe 官方)
- 可添加 myfork: 你的 GitHub Fork
```

**你现在已经在开发分支上，可以开始二次开发了！** ✅

---

## 🚀 快速开始二次开发

### 1. 创建功能分支（推荐）

为每个新功能创建独立分支：

```bash
# 确保在 custom-dev 分支
cd /home/services/lms
git checkout custom-dev

# 创建新功能分支
git checkout -b feature/your-feature-name

# 例如：
git checkout -b feature/add-exam-system
# 或
git checkout -b feature/custom-certificate
```

### 2. 进行开发

```bash
# 修改代码
nano lms/lms/doctype/...

# 或添加新的 DocType
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 new-doctype

# 测试修改
docker compose -f docker-compose-prod.yml restart lms

# 清除缓存
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache
```

### 3. 提交修改

```bash
# 查看修改
git status
git diff

# 添加到暂存区
git add .

# 提交（使用语义化提交信息）
git commit -m "feat: 添加考试系统功能

- 创建 Exam DocType
- 添加考试管理界面
- 实现自动评分
"

# 查看提交历史
git log --oneline -5
```

### 4. 合并到主开发分支

```bash
# 切换回主开发分支
git checkout custom-dev

# 合并功能分支
git merge feature/your-feature-name

# 如果有冲突，解决后继续
git add .
git commit -m "merge: 合并功能分支"

# 删除已合并的功能分支（可选）
git branch -d feature/your-feature-name
```

### 5. 推送到远程（可选）

```bash
# 如果已添加你的 fork
git push myfork custom-dev

# 如果还没添加，先添加：
git remote add myfork https://github.com/YOUR-USERNAME/lms.git
git push -u myfork custom-dev
```

---

## 📁 常见开发任务

### 添加新的 DocType

```bash
# 方式1：使用 bench 命令
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 new-doctype

# 会提示输入：
# DocType Name: My Custom DocType
# Module: LMS
# Is Submittable: No

# 方式2：手动创建
mkdir -p lms/lms/doctype/my_custom_doctype
# 创建必要的文件...
```

### 修改现有 DocType

```bash
# 编辑 Python 文件
nano lms/lms/doctype/course_lesson/course_lesson.py

# 编辑 JSON 配置
nano lms/lms/doctype/course_lesson/course_lesson.json

# 重启服务生效
docker compose -f docker-compose-prod.yml restart lms
```

### 添加自定义 API

```bash
# 创建 API 文件
nano lms/lms/api/custom_api.py

# 内容示例：
"""
import frappe

@frappe.whitelist()
def get_custom_data():
    return {"message": "Hello from custom API"}
"""

# 测试 API
curl http://192.168.20.118:8001/api/method/lms.lms.api.custom_api.get_custom_data
```

### 添加数据库字段

```bash
# 1. 编辑 DocType JSON，添加字段

# 2. 执行迁移
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 migrate

# 3. 清除缓存
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache

# 4. 重启服务
docker compose -f docker-compose-prod.yml restart lms
```

### 修改前端页面

```bash
# 编辑模板文件
nano lms/lms/templates/...

# 编辑 JavaScript
nano lms/lms/public/js/...

# 编辑 CSS
nano lms/lms/public/css/...

# 构建前端资源
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 build

# 清除缓存
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache
```

---

## 🔧 开发环境配置

### VS Code 远程开发（推荐）

1. **安装 Remote - SSH 插件**

2. **连接到服务器**
   ```
   Host: 192.168.20.118
   User: root
   ```

3. **打开项目目录**
   ```
   /home/services/lms
   ```

4. **推荐的 VS Code 插件**
   - Python
   - Jinja
   - GitLens
   - Docker
   - Markdown All in One

### 开发者模式

```bash
# 启用开发者模式
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 set-config developer_mode 1

# 禁用（生产环境）
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 set-config developer_mode 0
```

### 调试模式

```bash
# 查看实时日志
docker compose -f docker-compose-prod.yml logs -f lms

# 进入容器调试
docker compose -f docker-compose-prod.yml exec lms bash

# 进入 bench console
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 console
```

---

## 📝 提交规范

使用语义化提交信息：

```bash
# 新功能
git commit -m "feat(module): 添加新功能描述"

# Bug 修复
git commit -m "fix(module): 修复某个问题"

# 文档更新
git commit -m "docs: 更新文档"

# 代码重构
git commit -m "refactor: 重构某个模块"

# 性能优化
git commit -m "perf: 优化性能"

# 测试
git commit -m "test: 添加测试用例"

# 配置修改
git commit -m "chore: 更新配置"

# 样式修改
git commit -m "style: 调整代码格式"
```

**示例：**

```bash
git commit -m "feat(exam): 添加在线考试功能

- 创建 Exam 和 ExamQuestion DocType
- 实现考试时间限制
- 添加自动评分功能
- 支持多种题型（单选、多选、简答）

Closes #123
"
```

---

## 🔄 分支管理策略

### 推荐的分支结构

```
custom-dev              # 主开发分支（稳定版本）
  ├─ feature/exam       # 功能分支：考试系统
  ├─ feature/cert       # 功能分支：证书系统
  ├─ fix/login-bug      # 修复分支：登录问题
  └─ hotfix/urgent      # 紧急修复
```

### 分支命名规范

```bash
# 功能分支
feature/功能名称
feature/exam-system
feature/video-upload

# 修复分支
fix/问题描述
fix/user-login-error
fix/image-display

# 紧急修复
hotfix/紧急问题
hotfix/security-patch

# 发布分支
release/版本号
release/v1.0.0
```

### 分支操作

```bash
# 创建并切换分支
git checkout -b feature/new-feature

# 查看所有分支
git branch -a

# 切换分支
git checkout custom-dev

# 删除分支
git branch -d feature/old-feature

# 强制删除（未合并的分支）
git branch -D feature/abandoned

# 合并分支
git checkout custom-dev
git merge feature/new-feature

# 变基（保持提交历史整洁）
git rebase custom-dev
```

---

## 🧪 测试流程

### 开发时测试

```bash
# 1. 修改代码
nano lms/lms/...

# 2. 重启服务
docker compose -f docker-compose-prod.yml restart lms

# 3. 清除缓存
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache

# 4. 测试功能
# 访问前台或后台测试

# 5. 查看日志
docker compose -f docker-compose-prod.yml logs -f lms
```

### 运行单元测试（如果有）

```bash
# 运行所有测试
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 run-tests

# 运行特定测试
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 run-tests --module lms.lms.doctype.course_lesson
```

---

## 📦 常用命令速查

### Git 命令

```bash
# 状态查看
git status                    # 查看工作区状态
git log --oneline -10         # 查看提交历史
git diff                      # 查看未暂存的修改
git diff --staged             # 查看已暂存的修改

# 分支操作
git branch                    # 查看本地分支
git checkout -b <branch>      # 创建并切换分支
git merge <branch>            # 合并分支
git branch -d <branch>        # 删除分支

# 提交操作
git add .                     # 添加所有修改
git commit -m "message"       # 提交
git commit --amend            # 修改最后一次提交

# 远程操作
git push myfork custom-dev    # 推送到远程
git pull myfork custom-dev    # 拉取更新
git fetch origin              # 获取上游更新

# 撤销操作
git restore <file>            # 撤销工作区修改
git restore --staged <file>   # 取消暂存
git reset --soft HEAD~1       # 撤销提交（保留修改）
```

### Docker 命令

```bash
# 服务管理
docker compose -f docker-compose-prod.yml ps       # 查看服务状态
docker compose -f docker-compose-prod.yml restart  # 重启所有服务
docker compose -f docker-compose-prod.yml logs -f  # 查看日志

# 进入容器
docker compose -f docker-compose-prod.yml exec lms bash
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 console

# 清理
docker compose -f docker-compose-prod.yml down     # 停止并删除容器
docker system prune -a                             # 清理未使用的镜像
```

### Bench 命令

```bash
# 站点管理
bench --site 192.168.20.118 migrate        # 执行数据库迁移
bench --site 192.168.20.118 clear-cache    # 清除缓存
bench --site 192.168.20.118 build          # 构建前端资源
bench --site 192.168.20.118 console        # 进入 Python 控制台

# 开发工具
bench --site 192.168.20.118 new-doctype   # 创建 DocType
bench --site 192.168.20.118 run-tests     # 运行测试
```

---

## 🎯 下一步建议

### 立即可做

1. **创建功能分支开始开发**
   ```bash
   git checkout -b feature/my-first-feature
   ```

2. **熟悉代码结构**
   ```bash
   # 查看 LMS 源代码
   tree -L 3 lms/lms/

   # 查看 DocType
   ls lms/lms/doctype/
   ```

3. **修改一个小功能测试流程**
   ```bash
   # 例如：修改课程标题样式
   nano lms/lms/public/css/...
   ```

### 学习资源

- **Frappe 文档：** https://frappeframework.com/docs
- **Python API：** https://frappeframework.com/docs/user/en/api
- **DocType 开发：** https://frappeframework.com/docs/user/en/basics/doctypes

### 推荐的开发顺序

1. 熟悉现有代码结构
2. 修改小功能测试流程
3. 创建简单的自定义 DocType
4. 添加自定义 API
5. 修改前端页面
6. 实现复杂功能

---

## ⚠️ 注意事项

### 开发时

1. **总是在功能分支开发**
   - 不要直接在 custom-dev 提交
   - 功能完成后再合并

2. **经常提交**
   - 小步快跑
   - 每个功能点提交一次

3. **保持 custom-dev 干净**
   - custom-dev 应该是稳定版本
   - 未完成的功能不要合并

### 推送代码前

1. **测试功能是否正常**
2. **检查代码质量**
3. **更新相关文档**
4. **写清楚提交信息**

### 定期操作

1. **同步上游更新**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout custom-dev
   git merge develop
   ```

2. **推送到 GitHub 备份**
   ```bash
   git push myfork custom-dev
   ```

3. **清理旧分支**
   ```bash
   git branch -d feature/old-feature
   ```

---

## 🆘 遇到问题？

### 代码冲突

```bash
# 合并时如果有冲突
git merge feature/xxx
# CONFLICT...

# 1. 查看冲突文件
git status

# 2. 手动编辑解决冲突
nano <conflicted-file>

# 3. 标记为已解决
git add <conflicted-file>

# 4. 完成合并
git commit
```

### 误操作恢复

```bash
# 查看操作历史
git reflog

# 恢复到某个状态
git reset --hard <commit-id>

# 或使用 reflog 恢复
git reset --hard HEAD@{2}
```

### 服务问题

```bash
# 重启所有服务
docker compose -f docker-compose-prod.yml restart

# 查看详细日志
docker compose -f docker-compose-prod.yml logs -f

# 重新构建
docker compose -f docker-compose-prod.yml up -d --build
```

---

## 📞 获取帮助

- **查看文档：** `cat docs/CUSTOM_DEVELOPMENT_GUIDE.md`
- **Frappe 论坛：** https://discuss.frappe.io/
- **GitHub Issues：** 报告 bug

---

**准备好开始二次开发了！祝你开发顺利！** 🚀
