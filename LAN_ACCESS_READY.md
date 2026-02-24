# ✅ LMS 局域网访问已就绪

## 🎉 配置完成

Frappe LMS 已成功配置，现在可以从局域网内的任何设备访问！

---

## 🌐 访问地址

### 主要访问地址（局域网）
```
http://192.168.20.118:8001/lms
```

### 管理后台
```
http://192.168.20.118:8001/app
```

---

## 🔐 登录信息

| 项目 | 值 |
|------|-----|
| 用户名 | `Administrator` |
| 密码 | `admin` |

**⚠️ 安全提示**: 首次登录后请立即修改默认密码！

---

## 📱 支持的设备

以下设备都可以通过浏览器访问：

- ✅ 台式电脑
- ✅ 笔记本电脑
- ✅ 平板电脑
- ✅ 智能手机
- ✅ 任何支持浏览器的设备

---

## 🚀 快速开始

### 步骤 1: 从任意局域网设备访问
在浏览器地址栏输入:
```
http://192.168.20.118:8001/lms
```

### 步骤 2: 登录
使用上述登录信息登录系统

### 步骤 3: 开始使用
- 学生：浏览课程、学习、做作业
- 教师/管理员：创建课程、管理内容、查看统计

---

## 📊 服务状态

当前所有服务运行正常：

| 服务 | 状态 | 端口 |
|------|------|------|
| Web 服务 | ✅ 运行中 | 8001 |
| WebSocket | ✅ 运行中 | 9002 |
| 数据库 | ✅ 运行中 | 3307 |
| 缓存 | ✅ 运行中 | 6380 |

---

## 🛠️ 服务管理命令

### 查看服务状态
```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml ps
```

### 重启服务
```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml restart
```

### 查看日志
```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml logs -f lms
```

### 停止服务
```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml stop
```

### 启动服务
```bash
cd /home/services/lms
docker compose -f docker-compose-prod.yml start
```

---

## 🧪 运行测试脚本

系统提供了一键测试脚本，可以快速检查所有服务状态：

```bash
/home/services/lms/test_access.sh
```

该脚本会检查：
- ✅ 容器运行状态
- ✅ Web 服务访问
- ✅ 端口开放情况
- ✅ 防火墙状态

---

## 📚 相关文档

- **完整部署文档**: `/home/services/lms/DEPLOYMENT_SUMMARY.md`
- **快速访问指南**: `/home/services/lms/QUICK_ACCESS_GUIDE.md`
- **端口配置说明**: `/home/services/lms/docker/PORT_CONFIG.md`

---

## 🔧 故障排查

### 问题：无法从其他设备访问

**解决方案**：
1. 确认设备在同一局域网 (192.168.20.x)
2. 检查服务器 IP 是否为 192.168.20.118
3. 运行测试脚本: `/home/services/lms/test_access.sh`
4. 尝试 ping 服务器: `ping 192.168.20.118`

### 问题：页面加载慢

**解决方案**：
1. 检查网络连接质量
2. 重启服务: `docker compose restart lms`
3. 清除浏览器缓存

### 问题：无法登录

**解决方案**：
1. 确认使用正确的凭据: Administrator / admin
2. 尝试清除浏览器 Cookie
3. 检查服务日志: `docker compose logs lms`

---

## 💡 使用技巧

### 1. 移动设备访问
建议将网址添加到主屏幕以便快速访问：
- iOS: Safari → 分享 → 添加到主屏幕
- Android: Chrome → 菜单 → 添加到主屏幕

### 2. 书签
建议收藏以下页面：
- 学习平台: http://192.168.20.118:8001/lms
- 管理后台: http://192.168.20.118:8001/app

### 3. 多用户访问
系统支持多个用户同时访问，每个用户都有独立的登录会话。

---

## 📞 获取帮助

遇到问题？

1. **查看日志**
   ```bash
   docker compose -f /home/services/lms/docker-compose-prod.yml logs -f lms
   ```

2. **运行测试**
   ```bash
   /home/services/lms/test_access.sh
   ```

3. **检查文档**
   查看 `/home/services/lms/` 目录下的各种文档

---

## 🎯 下一步

1. ✅ 访问 http://192.168.20.118:8001/lms
2. ✅ 使用 Administrator/admin 登录
3. ✅ 修改管理员密码（重要！）
4. ✅ 创建课程和内容
5. ✅ 邀请用户开始学习

---

## 📋 系统信息总结

| 项目 | 值 |
|------|-----|
| 服务器 IP | 192.168.20.118 |
| Web 端口 | 8001 |
| 学习平台 | http://192.168.20.118:8001/lms |
| 管理后台 | http://192.168.20.118:8001/app |
| 默认用户 | Administrator |
| 默认密码 | admin |
| 部署方式 | Docker Compose |
| 数据持久化 | ✅ 已配置 |

---

<div align="center">

## ✨ 部署成功！✨

### 现在就可以从局域网访问 LMS 了！

**http://192.168.20.118:8001/lms**

</div>

---

*文档生成时间: 2026-02-24*
*部署位置: /home/services/lms*
