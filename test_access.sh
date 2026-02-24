#!/bin/bash

# LMS 访问测试脚本

echo "=========================================="
echo "       LMS 服务访问测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取服务器 IP
SERVER_IP=$(ip addr show | grep "inet 192.168" | awk '{print $2}' | cut -d'/' -f1)
echo -e "${YELLOW}服务器 IP:${NC} $SERVER_IP"
echo ""

# 测试容器状态
echo "1. 检查容器状态..."
cd /home/services/lms
CONTAINER_STATUS=$(docker compose -f docker-compose-prod.yml ps --format json 2>/dev/null | grep -c "running")
if [ "$CONTAINER_STATUS" -ge 3 ]; then
    echo -e "${GREEN}✓${NC} 所有容器正在运行"
else
    echo -e "${RED}✗${NC} 部分容器未运行"
    docker compose -f docker-compose-prod.yml ps
fi
echo ""

# 测试本地访问 (localhost)
echo "2. 测试本地访问 (lms.localhost)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://lms.localhost:8001/lms 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓${NC} http://lms.localhost:8001/lms - 访问成功"
else
    echo -e "${RED}✗${NC} http://lms.localhost:8001/lms - 访问失败 (HTTP $HTTP_CODE)"
fi
echo ""

# 测试 IP 访问
echo "3. 测试 IP 访问 ($SERVER_IP)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://$SERVER_IP:8001/lms 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓${NC} http://$SERVER_IP:8001/lms - 访问成功"
else
    echo -e "${RED}✗${NC} http://$SERVER_IP:8001/lms - 访问失败 (HTTP $HTTP_CODE)"
fi
echo ""

# 测试管理后台
echo "4. 测试管理后台..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://$SERVER_IP:8001/app 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓${NC} http://$SERVER_IP:8001/app - 后台访问成功"
else
    echo -e "${RED}✗${NC} http://$SERVER_IP:8001/app - 后台访问失败 (HTTP $HTTP_CODE)"
fi
echo ""

# 检查端口
echo "5. 检查端口占用..."
PORTS=("8001" "9002" "3307" "6380")
for port in "${PORTS[@]}"; do
    if netstat -tuln | grep -q ":$port "; then
        echo -e "${GREEN}✓${NC} 端口 $port 已开放"
    else
        echo -e "${RED}✗${NC} 端口 $port 未开放"
    fi
done
echo ""

# 防火墙状态
echo "6. 检查防火墙状态..."
UFW_STATUS=$(ufw status 2>/dev/null | grep "Status:" | awk '{print $2}')
if [ "$UFW_STATUS" = "inactive" ] || [ "$UFW_STATUS" = "不活动" ]; then
    echo -e "${GREEN}✓${NC} 防火墙未启用（端口全开）"
else
    echo -e "${YELLOW}!${NC} 防火墙已启用: $UFW_STATUS"
    echo "   请确保已开放端口 8001 和 9002"
fi
echo ""

# 站点列表
echo "7. 可用站点..."
echo -e "   • lms.localhost (本地访问)"
echo -e "   • $SERVER_IP (局域网访问)"
echo ""

echo "=========================================="
echo "           访问信息汇总"
echo "=========================================="
echo ""
echo -e "${YELLOW}局域网访问地址:${NC}"
echo -e "  学习平台: http://$SERVER_IP:8001/lms"
echo -e "  管理后台: http://$SERVER_IP:8001/app"
echo ""
echo -e "${YELLOW}登录凭据:${NC}"
echo -e "  用户名: Administrator"
echo -e "  密码: admin"
echo ""
echo -e "${YELLOW}服务管理:${NC}"
echo -e "  启动: cd /home/services/lms && docker compose -f docker-compose-prod.yml start"
echo -e "  停止: cd /home/services/lms && docker compose -f docker-compose-prod.yml stop"
echo -e "  重启: cd /home/services/lms && docker compose -f docker-compose-prod.yml restart"
echo -e "  日志: cd /home/services/lms && docker compose -f docker-compose-prod.yml logs -f lms"
echo ""
echo "=========================================="

# 二维码生成（如果有 qrencode）
if command -v qrencode &> /dev/null; then
    echo ""
    echo "扫描二维码访问（手机）:"
    qrencode -t ANSIUTF8 "http://$SERVER_IP:8001/lms"
    echo ""
fi

echo -e "${GREEN}测试完成！${NC}"
echo ""
