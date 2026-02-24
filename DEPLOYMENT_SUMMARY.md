# Frappe LMS 部署总结

## 部署状态
✅ 部署成功！

## 访问信息

### 本地访问（仅服务器本机）
http://lms.localhost:8001/lms

### 局域网访问（所有设备）
http://192.168.20.118:8001/lms

**说明**: 局域网内的任何设备都可以通过 IP 地址直接访问，无需配置 hosts 文件。

### 默认登录凭据
- 用户名: `Administrator`
- 密码: `admin`

### 界面语言
- **默认语言**: 简体中文
- **支持语言**: 简体中文、繁体中文、英语等 60+ 种语言
- **详细说明**: 查看 `/home/services/lms/CHINESE_LANGUAGE_SETUP.md`

## 端口配置

所有端口已修改以避免冲突：

| 服务 | 容器内端口 | 主机端口 | 原端口 |
|------|-----------|---------|--------|
| Frappe Web | 8000 | **8001** | 8000 |
| Frappe SocketIO | 9000 | **9002** | 9000 |
| MariaDB | 3306 | **3307** | 3306 |
| Redis | 6379 | **6380** | 6379 |

## 部署架构

- **Docker Compose**: 使用生产环境镜像部署
- **配置文件**: `/home/services/lms/docker-compose-prod.yml`
- **数据持久化**:
  - MariaDB 数据: Docker volume `mariadb-data`
  - 站点数据: Docker volume `lms-sites`
  - 日志: Docker volume `lms-logs`

## 常用命令

### 查看服务状态
```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml ps
```

### 查看日志
```bash
# 查看所有服务日志
docker compose -f docker-compose-prod.yml logs -f

# 查看 lms 服务日志
docker compose -f docker-compose-prod.yml logs -f lms
```

### 停止服务
```bash
docker compose -f docker-compose-prod.yml stop
```

### 启动服务
```bash
docker compose -f docker-compose-prod.yml start
```

### 重启服务
```bash
docker compose -f docker-compose-prod.yml restart
```

### 完全停止并删除容器
```bash
docker compose -f docker-compose-prod.yml down
```

### 完全重置（删除所有数据）
```bash
docker compose -f docker-compose-prod.yml down --volumes
```

## 数据库连接信息

如需从主机连接数据库进行管理：

```
主机: localhost
端口: 3307
用户名: root
密码: lms_password_123
```

## 站点信息

系统已配置两个站点：

### 站点 1: lms.localhost（本地访问）
- **站点名称**: lms.localhost
- **访问地址**: http://lms.localhost:8001
- **管理后台**: http://lms.localhost:8001/app
- **学习平台**: http://lms.localhost:8001/lms

### 站点 2: 192.168.20.118（局域网访问）
- **站点名称**: 192.168.20.118
- **访问地址**: http://192.168.20.118:8001
- **管理后台**: http://192.168.20.118:8001/app
- **学习平台**: http://192.168.20.118:8001/lms

**注意**: 两个站点数据独立，各自拥有独立的数据库和管理员账户。

## 配置文件位置

- **Docker Compose**: `/home/services/lms/docker-compose-prod.yml`
- **Hosts 配置**: `/etc/hosts` (已添加 `127.0.0.1 lms.localhost`)
- **站点配置**: 容器内 `/home/frappe/frappe-bench/sites/lms.localhost/`

## 主要功能

1. **课程管理**: 创建和管理在线课程
2. **批次管理**: 将学习者分组到批次中
3. **在线直播课**: 集成 Zoom 进行直播教学
4. **测验和作业**: 创建评估和作业
5. **证书**: 为完成课程的学习者颁发证书

## 下一步操作

1. 访问 http://lms.localhost:8001/lms 查看学习平台
2. 使用 Administrator/admin 登录
3. 首次登录后建议修改管理员密码
4. 访问 http://lms.localhost:8001/app 进入后台管理界面
5. 开始创建课程和内容

## 注意事项

- 本地访问需要在 `/etc/hosts` 中配置域名解析
- 生产环境建议修改默认密码
- 定期备份数据库和站点数据
- 可以通过 Docker volumes 进行数据备份

## 故障排查

### 如果无法访问
1. 检查容器是否运行: `docker compose -f docker-compose-prod.yml ps`
2. 检查日志: `docker compose -f docker-compose-prod.yml logs lms`
3. 确认 hosts 文件配置正确
4. 确认端口未被占用

### 重启所有服务
```bash
docker compose -f docker-compose-prod.yml restart
```
