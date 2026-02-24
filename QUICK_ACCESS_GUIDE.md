# LMS 局域网访问快速指南

## 局域网访问地址

### 🌐 主要访问地址
**http://192.168.20.118:8001/lms**

局域网内的任何设备（电脑、平板、手机）都可以通过这个地址访问 LMS。

## 登录信息

- **用户名**: Administrator
- **密码**: admin

## 不同设备访问方式

### 电脑访问
1. 打开浏览器（Chrome、Firefox、Edge 等）
2. 在地址栏输入: `http://192.168.20.118:8001/lms`
3. 按回车键访问
4. 使用上述登录信息登录

### 手机/平板访问
1. 打开浏览器
2. 在地址栏输入: `http://192.168.20.118:8001/lms`
3. 使用上述登录信息登录

### 服务器本机访问
`http://lms.localhost:8001/lms`

## 各功能模块访问地址

### 学习平台（前台）
- **地址**: http://192.168.20.118:8001/lms
- **用途**: 学生浏览课程、学习、做作业、考试等

### 管理后台
- **地址**: http://192.168.20.118:8001/app
- **用途**: 管理员创建课程、管理用户、查看统计等

### Desk 工作台
- **地址**: http://192.168.20.118:8001/desk
- **用途**: Frappe 框架的管理界面

## 端口说明

- **8001**: Web 访问端口（主要使用）
- **9002**: WebSocket 端口（用于实时通信）
- **3307**: 数据库端口（仅管理员使用）
- **6380**: Redis 缓存端口（仅内部使用）

## 防火墙配置

如果其他设备无法访问，可能需要在服务器上开放端口：

```bash
# 使用 ufw（Ubuntu/Debian）
sudo ufw allow 8001/tcp
sudo ufw allow 9002/tcp

# 或使用 firewalld（CentOS/RHEL）
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --permanent --add-port=9002/tcp
sudo firewall-cmd --reload
```

## 测试连接

### 从其他设备测试
打开命令提示符或终端，执行：

```bash
# Windows
ping 192.168.20.118

# Linux/Mac
ping -c 4 192.168.20.118
```

如果能 ping 通，说明网络连接正常。

### 测试 Web 服务
在浏览器中访问: http://192.168.20.118:8001

如果看到页面，说明服务正常。

## 常见问题

### Q1: 无法访问怎么办？

**检查清单**:
1. 确认服务器和客户端在同一局域网
2. 确认服务正在运行: `docker compose ps`
3. 检查防火墙是否开放 8001 端口
4. 尝试 ping 服务器 IP: `ping 192.168.20.118`
5. 检查服务器日志: `docker compose logs lms`

### Q2: 访问很慢怎么办？

1. 检查网络连接质量
2. 查看服务器资源使用情况
3. 清除浏览器缓存
4. 重启 LMS 服务: `docker compose restart lms`

### Q3: 如何修改端口？

编辑 `/home/services/lms/docker-compose-prod.yml` 文件，修改 ports 配置后重启服务。

### Q4: 能否使用域名访问？

可以，需要：
1. 在路由器配置 DNS 解析，或
2. 在每台设备的 hosts 文件中添加解析记录

### Q5: 如何修改管理员密码？

登录后访问: http://192.168.20.118:8001/app/user/Administrator
点击 "Change Password" 修改密码。

## 安全建议

1. **尽快修改默认密码**
2. 如果需要从公网访问，务必配置 HTTPS
3. 定期备份数据
4. 限制管理员账户数量
5. 定期检查系统日志

## 技术支持

如遇到问题：
1. 查看日志: `docker compose -f /home/services/lms/docker-compose-prod.yml logs -f lms`
2. 检查容器状态: `docker compose -f /home/services/lms/docker-compose-prod.yml ps`
3. 查看完整文档: `/home/services/lms/DEPLOYMENT_SUMMARY.md`

---

**服务器 IP**: 192.168.20.118
**Web 端口**: 8001
**访问地址**: http://192.168.20.118:8001/lms
