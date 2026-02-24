# 二次开发规范

## 📋 开发流程规范

### 标准开发流程

```
1. 需求分析 → 2. 创建分支 → 3. 开发实现 → 4. 测试验证 → 5. 合并发布
```

---

## 🔄 完整开发流程

### 1️⃣ 开发前准备

#### 1.1 确认需求
- 明确开发目标和功能需求
- 评估技术可行性
- 确定预期效果

#### 1.2 切换到 custom-dev 分支
```bash
# 确保在 custom-dev 分支
git checkout custom-dev

# 拉取最新代码
git pull myfork custom-dev

# 查看当前状态
git status
```

#### 1.3 创建功能分支
```bash
# 创建并切换到功能分支
git checkout -b feature/功能名称

# 命名规范：
# feature/exam-system    # 新功能
# fix/login-bug          # Bug 修复
# enhance/video-player   # 功能增强
# refactor/user-module   # 代码重构
```

#### 1.4 创建开发记录
```bash
# 创建开发记录文件
nano docs/development-logs/YYYYMMDD-功能名称.md

# 例如：
# docs/development-logs/20260224-exam-system.md
```

---

### 2️⃣ 开发阶段

#### 2.1 代码开发
- 遵循项目编码规范
- 编写清晰的代码注释
- 保持代码简洁可读

#### 2.2 定期提交
```bash
# 小步提交，便于回溯
git add .
git commit -m "feat: 添加考试系统基础结构"

# 提交信息规范：
# feat: 新功能
# fix: Bug 修复
# docs: 文档更新
# refactor: 代码重构
# test: 测试相关
# chore: 配置修改
```

#### 2.3 更新开发记录
- 记录开发进度
- 记录遇到的问题和解决方案
- 记录重要的设计决策

---

### 3️⃣ 测试阶段

#### 3.1 本地测试
```bash
# 重启服务
docker compose -f docker-compose-prod.yml restart lms

# 清除缓存
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 clear-cache

# 查看日志
docker compose -f docker-compose-prod.yml logs -f lms
```

#### 3.2 功能测试清单
- [ ] 核心功能正常工作
- [ ] 界面显示正确
- [ ] 没有控制台错误
- [ ] 数据保存正确
- [ ] 与现有功能无冲突

#### 3.3 记录测试结果
在开发记录中更新测试结果

---

### 4️⃣ 合并到 custom-dev

#### 4.1 切换到 custom-dev
```bash
git checkout custom-dev
git pull myfork custom-dev
```

#### 4.2 合并功能分支
```bash
# 合并功能分支
git merge feature/功能名称

# 如果有冲突，解决后：
git add .
git commit -m "merge: 合并功能分支"
```

#### 4.3 推送到 GitHub
```bash
git push myfork custom-dev
```

#### 4.4 删除功能分支（可选）
```bash
# 本地删除
git branch -d feature/功能名称

# 远程删除（如果推送过）
git push myfork --delete feature/功能名称
```

---

### 5️⃣ 合并到 main（发布稳定版本）

#### 5.1 确认 custom-dev 稳定
- 所有功能测试通过
- 没有已知 Bug
- 文档已更新

#### 5.2 合并到 main
```bash
# 切换到 main 分支
git checkout main

# 拉取最新代码
git pull myfork main

# 合并 custom-dev
git merge custom-dev

# 查看合并结果
git log --oneline -5
```

#### 5.3 打版本标签
```bash
# 创建版本标签
git tag -a v1.1.0 -m "Release v1.1.0

新增功能：
- 考试系统
- 在线答题
- 自动评分

Bug 修复：
- 修复登录问题
- 优化性能
"

# 查看标签
git tag -l
```

#### 5.4 推送到 GitHub
```bash
# 推送 main 分支
git push myfork main

# 推送标签
git push myfork v1.1.0

# 或一次性推送所有标签
git push myfork --tags
```

#### 5.5 切回 custom-dev
```bash
git checkout custom-dev
```

---

## 📝 开发记录规范

### 记录文件命名
```
docs/development-logs/YYYYMMDD-功能名称.md

例如：
20260224-exam-system.md
20260225-video-upload.md
20260226-fix-login-bug.md
```

### 记录内容模板
```markdown
# 功能名称 - 开发记录

## 基本信息
- **开发时间：** YYYY-MM-DD
- **开发者：** 姓名
- **分支：** feature/功能名称
- **状态：** 进行中/已完成/已发布

## 需求说明
简要描述功能需求和目标

## 技术方案
### 设计思路
- 方案选择
- 架构设计

### 涉及文件
- 文件1：说明
- 文件2：说明

## 实现细节
### 核心功能
1. 功能点1
2. 功能点2

### 关键代码
代码片段和说明

## 测试记录
### 测试内容
- [ ] 测试项1
- [ ] 测试项2

### 测试结果
- 成功/失败
- 问题说明

## 遇到的问题
### 问题1
- 问题描述
- 解决方案

## 后续优化
- 待优化点1
- 待优化点2

## 发布记录
- **发布时间：** YYYY-MM-DD
- **版本号：** v1.1.0
- **发布说明：** 简要说明
```

---

## 🎯 代码规范

### 提交信息规范

**格式：**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型（type）：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具/配置

**示例：**
```bash
feat(exam): 添加在线考试功能

- 创建 Exam DocType
- 实现考试时间限制
- 添加自动评分功能
- 支持多种题型

Closes #123
```

### 分支命名规范

```bash
# 功能开发
feature/功能名称-简短描述
feature/exam-system
feature/video-upload

# Bug 修复
fix/问题描述
fix/login-error
fix/image-display

# 功能增强
enhance/功能名称
enhance/video-player
enhance/user-profile

# 代码重构
refactor/模块名称
refactor/user-module
refactor/api-layer

# 紧急修复
hotfix/问题描述
hotfix/security-patch
```

### 代码注释规范

**Python：**
```python
def create_exam(title, duration):
    """
    创建考试

    Args:
        title (str): 考试标题
        duration (int): 考试时长（分钟）

    Returns:
        str: 考试 ID

    Raises:
        ValidationError: 参数验证失败
    """
    # 验证参数
    if not title:
        raise ValidationError("考试标题不能为空")

    # 创建考试记录
    exam = frappe.new_doc("Exam")
    exam.title = title
    exam.duration = duration
    exam.insert()

    return exam.name
```

**JavaScript：**
```javascript
/**
 * 开始考试
 * @param {string} examId - 考试 ID
 * @param {number} duration - 考试时长（分钟）
 * @returns {Promise} 考试实例
 */
function startExam(examId, duration) {
    // 检查考试是否存在
    if (!examId) {
        throw new Error('考试 ID 不能为空');
    }

    // 初始化考试
    const exam = new Exam(examId);
    exam.start(duration);

    return exam;
}
```

---

## 🔍 代码审查清单

### 功能完整性
- [ ] 功能符合需求
- [ ] 边界情况已处理
- [ ] 错误处理完善

### 代码质量
- [ ] 代码清晰易读
- [ ] 命名规范合理
- [ ] 注释充分准确
- [ ] 没有重复代码

### 性能优化
- [ ] 数据库查询优化
- [ ] 避免 N+1 查询
- [ ] 缓存使用合理

### 安全性
- [ ] 输入验证
- [ ] SQL 注入防护
- [ ] XSS 防护
- [ ] 权限检查

### 兼容性
- [ ] 不影响现有功能
- [ ] 数据库变更向后兼容
- [ ] API 接口向后兼容

---

## 📊 版本管理规范

### 版本号规则

采用语义化版本：`主版本号.次版本号.修订号`

```
v1.0.0 → v1.1.0 → v1.1.1 → v2.0.0

主版本号：重大更新，可能不兼容
次版本号：新增功能，向后兼容
修订号：Bug 修复，向后兼容
```

**示例：**
- `v1.0.0` - 初始版本
- `v1.1.0` - 新增考试系统
- `v1.1.1` - 修复考试系统 Bug
- `v2.0.0` - 重大架构升级

### 发布清单

- [ ] 代码已合并到 main
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] 开发记录已完成
- [ ] 版本号已更新
- [ ] CHANGELOG 已更新

---

## 🚨 回滚流程

### 紧急回滚

```bash
# 1. 查看版本历史
git tag -l

# 2. 回滚到上一个稳定版本
git checkout v1.0.0

# 3. 部署
docker compose -f docker-compose-prod.yml restart

# 4. 如需永久回滚
git checkout main
git reset --hard v1.0.0
git push -f myfork main
```

### 修复后重新发布

```bash
# 1. 在 custom-dev 修复问题
git checkout custom-dev
# 修复...
git commit -m "fix: 修复紧急问题"

# 2. 合并到 main
git checkout main
git merge custom-dev
git tag -a v1.0.1 -m "Hotfix: 修复紧急问题"
git push myfork main v1.0.1
```

---

## 📚 文档规范

### 必须更新的文档

1. **开发记录**
   - `docs/development-logs/YYYYMMDD-功能名称.md`

2. **使用文档**（如果有新功能）
   - 更新 `README_CUSTOM.md`
   - 添加功能说明文档

3. **API 文档**（如果有新 API）
   - 接口说明
   - 参数说明
   - 示例代码

4. **CHANGELOG**（可选）
   - 记录版本变更

---

## ✅ 快速检查清单

### 开发前
- [ ] 切换到 custom-dev 分支
- [ ] 拉取最新代码
- [ ] 创建功能分支
- [ ] 创建开发记录

### 开发中
- [ ] 定期提交代码
- [ ] 更新开发记录
- [ ] 编写代码注释

### 开发后
- [ ] 本地测试通过
- [ ] 代码已提交
- [ ] 合并到 custom-dev
- [ ] 推送到 GitHub

### 发布前
- [ ] custom-dev 稳定
- [ ] 文档已更新
- [ ] 合并到 main
- [ ] 打版本标签
- [ ] 推送到 GitHub

---

## 🔗 相关文档

- **分支策略：** `docs/BRANCH_STRATEGY.md`
- **开发快速开始：** `DEVELOPMENT_QUICK_START.md`
- **完整开发指南：** `docs/CUSTOM_DEVELOPMENT_GUIDE.md`

---

**遵循这些规范，确保开发过程规范、高效、可追溯！** 🚀
