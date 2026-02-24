# 二次开发环境配置指南

## 🎯 问题说明

使用 Docker 镜像进行二次开发的痛点：
- ❌ 代码在镜像内部，修改不方便
- ❌ 每次修改需要复制文件到容器
- ❌ 无法实时看到代码修改效果
- ❌ 调试困难

## ✅ 解决方案：Volume 挂载

使用 Docker Volume 将本地代码目录挂载到容器中，这样：
- ✅ 在本地编辑器修改代码
- ✅ 容器自动使用最新代码
- ✅ 实时构建和测试
- ✅ 开发体验更流畅

---

## 📂 方案一：Volume 挂载（推荐）

### 1.1 目录结构

```bash
/home/services/lms/
├── docker-compose-prod.yml    # 生产环境（使用镜像内代码）
├── docker-compose-dev.yml     # 开发环境（挂载本地代码）
├── lms/                        # LMS 后端代码（挂载到容器）
│   ├── lms/                    # Python 模块
│   ├── hooks.py
│   └── ...
├── frontend/                   # 前端代码（挂载到容器）
│   ├── src/
│   ├── package.json
│   └── ...
└── docs/                       # 文档
```

### 1.2 使用开发环境

#### 启动开发环境

```bash
# 停止生产环境
docker compose -f docker-compose-prod.yml down

# 启动开发环境
docker compose -f docker-compose-dev.yml up -d

# 查看日志
docker compose -f docker-compose-dev.yml logs -f lms
```

#### 修改后端代码

```bash
# 1. 在本地编辑代码
nano /home/services/lms/lms/lms/某个文件.py

# 2. 重启服务生效（Python 代码需要重启）
docker compose -f docker-compose-dev.yml restart lms
```

#### 修改前端代码

```bash
# 1. 在本地编辑前端代码
nano /home/services/lms/frontend/src/components/某个组件.vue

# 2. 在容器中构建前端
docker compose -f docker-compose-dev.yml exec lms bash -c \
  "cd /home/frappe/frappe-bench/apps/lms/frontend && yarn build"

# 3. 重启 nginx
docker compose -f docker-compose-dev.yml restart nginx
```

### 1.3 开发工作流

```bash
# 修改代码
vim /home/services/lms/lms/lms/user.py

# 提交到 Git
cd /home/services/lms
git add lms/lms/user.py
git commit -m "feat: 添加新功能"

# 推送到 GitHub
git push myfork custom-dev
```

---

## 📂 方案二：开发容器（进阶）

如果需要更完整的开发环境，可以创建专门的开发容器：

### 2.1 创建 Dockerfile.dev

```dockerfile
FROM ghcr.io/frappe/lms:stable

# 安装开发工具
RUN pip install ipython ipdb black flake8

# 安装 Node.js 开发工具
RUN cd /home/frappe/frappe-bench/apps/lms/frontend && \
    yarn add --dev @vue/devtools

# 启用热重载
ENV FRAPPE_DEV_MODE=1
```

### 2.2 使用开发容器

```bash
# 构建开发镜像
docker build -f Dockerfile.dev -t lms:dev .

# 修改 docker-compose-dev.yml 使用开发镜像
# image: lms:dev

# 启动
docker compose -f docker-compose-dev.yml up -d
```

---

## 📂 方案三：本地开发环境（最灵活）

完全在本地运行 Frappe，不使用 Docker：

### 3.1 安装依赖

```bash
# 安装 Frappe Bench
sudo apt-get install -y \
    python3-dev python3-pip \
    nodejs npm redis-server mariadb-server

# 安装 Frappe Bench CLI
pip3 install frappe-bench

# 初始化 Bench
bench init frappe-bench --frappe-branch version-14
cd frappe-bench

# 获取 LMS 应用
bench get-app lms https://github.com/YOUR-USERNAME/lms.git \
    --branch custom-dev
```

### 3.2 创建站点

```bash
# 创建站点
bench new-site lms.local

# 安装应用
bench --site lms.local install-app lms

# 启动开发服务器
bench start
```

### 3.3 开发流程

```bash
# 修改代码
vim apps/lms/lms/lms/user.py

# 实时生效（Frappe 开发模式自动重载）
# 访问 http://localhost:8000
```

---

## 🔧 推荐的开发工具配置

### VS Code

安装 Remote Development 扩展，直接编辑容器内代码：

```bash
# 安装 Remote - Containers 扩展
code --install-extension ms-vscode-remote.remote-containers

# 附加到运行中的容器
# Ctrl+Shift+P → "Remote-Containers: Attach to Running Container"
# 选择 lms-prod-lms-1
```

### VIM/Neovim

配置远程编辑：

```bash
# 使用 docker cp 同步
alias lms-sync='docker cp /home/services/lms/lms lms-prod-lms-1:/home/frappe/frappe-bench/apps/'
```

---

## 🎯 各方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Volume 挂载** | 配置简单<br>修改即生效<br>保留生产环境 | 需要手动构建前端 | ✅ **推荐**<br>小到中型修改 |
| **开发容器** | 完整开发环境<br>工具齐全 | 镜像较大<br>需要重建 | 大规模开发 |
| **本地环境** | 最灵活<br>热重载 | 配置复杂<br>依赖多 | 全职开发<br>需要调试 |

---

## 📋 快速开始（推荐流程）

### 第一步：使用 Volume 挂载

```bash
# 1. 停止生产环境
docker compose -f docker-compose-prod.yml down

# 2. 启动开发环境
docker compose -f docker-compose-dev.yml up -d

# 3. 修改代码
nano /home/services/lms/lms/lms/user.py

# 4. 重启生效
docker compose -f docker-compose-dev.yml restart lms

# 5. 测试
curl http://192.168.20.118:8001/

# 6. 提交代码
git add .
git commit -m "feat: 添加新功能"
git push myfork custom-dev
```

### 第二步：前端开发

```bash
# 1. 修改前端代码
nano /home/services/lms/frontend/src/components/xxx.vue

# 2. 构建
docker compose -f docker-compose-dev.yml exec lms \
  bash -c "cd /home/frappe/frappe-bench/apps/lms/frontend && yarn build"

# 3. 重启
docker compose -f docker-compose-dev.yml restart nginx

# 4. 清除浏览器缓存测试
# Ctrl+Shift+Delete 或 无痕模式
```

### 第三步：切换回生产环境

```bash
# 开发测试完成后
docker compose -f docker-compose-dev.yml down

# 切换回生产环境
docker compose -f docker-compose-prod.yml up -d
```

---

## ⚠️ 注意事项

### 1. Volume 挂载的限制

- **文件权限问题**：容器内用户是 `frappe`（UID 1000），确保本地文件可读写
  ```bash
  sudo chown -R 1000:1000 /home/services/lms/lms
  sudo chown -R 1000:1000 /home/services/lms/frontend
  ```

- **性能问题**：在 macOS/Windows 上，Volume 性能可能较差
  - 解决方案：使用 `docker-compose-dev.yml` 中的 `delegated` 模式
  ```yaml
  volumes:
    - ./lms:/home/frappe/frappe-bench/apps/lms:delegated
  ```

### 2. 前端构建

- 每次修改前端代码后需要重新构建
- 构建时间约 10-15 秒
- 可以考虑在本地运行 `yarn dev` 进行开发（需要配置代理）

### 3. 数据库迁移

- 如果修改了 DocType，需要运行迁移：
  ```bash
  docker compose -f docker-compose-dev.yml exec lms \
    bench --site 192.168.20.118 migrate
  ```

---

## 🚀 进阶技巧

### 实时前端开发（热重载）

```bash
# 1. 在本地运行前端开发服务器
cd /home/services/lms/frontend
yarn dev

# 2. 配置代理指向 LMS 容器
# 修改 vite.config.js:
# server: {
#   proxy: {
#     '/api': 'http://192.168.20.118:8001',
#   }
# }

# 3. 访问本地开发服务器
# http://localhost:3000
```

### 自动重启脚本

```bash
# 创建 watch 脚本
cat > /home/services/lms/scripts/watch-and-restart.sh <<'EOF'
#!/bin/bash
# 监听文件变化并自动重启

inotifywait -m -r -e modify /home/services/lms/lms/lms/ |
while read path action file; do
    echo "检测到变化: $file"
    docker compose -f docker-compose-dev.yml restart lms
    echo "服务已重启"
done
EOF

chmod +x /home/services/lms/scripts/watch-and-restart.sh

# 运行
./scripts/watch-and-restart.sh
```

---

## ✅ 总结

**当前最佳实践：**

1. **日常开发**：使用 `docker-compose-dev.yml` + Volume 挂载
2. **前端开发**：在容器中构建，或使用本地 `yarn dev`
3. **测试验证**：在开发环境充分测试
4. **生产部署**：切换回 `docker-compose-prod.yml`

**文件位置：**
- 开发配置：`docker-compose-dev.yml`
- 生产配置：`docker-compose-prod.yml`
- 代码目录：`/home/services/lms/lms/` 和 `/home/services/lms/frontend/`

**下次开发时：**
```bash
# 一条命令启动开发环境
docker compose -f docker-compose-dev.yml up -d

# 编辑代码
vim /home/services/lms/lms/lms/xxx.py

# 重启生效
docker compose -f docker-compose-dev.yml restart lms
```

---

**这样二次开发就方便多了！** 🎉
