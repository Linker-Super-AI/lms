# LMS 端口配置说明

## 修改后的端口映射

为避免端口冲突，已将端口配置修改如下：

| 服务 | 容器内端口 | 主机端口 | 说明 |
|------|-----------|---------|------|
| Frappe Web | 8000 | 8001 | 主要 Web 访问端口 |
| Frappe SocketIO | 9000 | 9002 | WebSocket 连接端口 |
| MariaDB | 3306 | 3307 | 数据库端口 |
| Redis | 6379 | 6380 | 缓存服务端口 |

## 访问地址

由于 Frappe 需要主机名解析，需要配置 hosts 文件：

### 方法1: 修改 hosts 文件（推荐）

在 `/etc/hosts` 文件中添加以下行：
```
127.0.0.1 lms.localhost
```

然后访问: http://lms.localhost:8001/lms

### 方法2: 使用 curl 命令测试
```bash
curl -H "Host: lms.localhost" http://localhost:8001/lms
```

- **默认登录凭据**:
  - 用户名: Administrator
  - 密码: admin

## 数据库连接

如需从主机连接数据库：
- 主机: localhost
- 端口: 3307
- 用户名: root
- 密码: 123

## 部署命令

在 lms/docker 目录下运行：

```bash
# 启动服务（后台运行）
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 完全重置（删除所有数据）
docker compose down --volumes
```

## 注意事项

1. 首次启动需要等待几分钟来初始化数据库和安装应用
2. 如果遇到问题，可以查看日志: `docker compose logs -f frappe`
3. 数据持久化存储在 Docker volume `mariadb-data` 中
