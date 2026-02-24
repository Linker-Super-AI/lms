#!/bin/bash

echo "========================================"
echo "     LMS 中文界面验证工具"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd /home/services/lms

echo "1. 检查系统默认语言配置..."
DEFAULT_LANG=$(docker compose -f docker-compose-prod.yml exec -T lms bash -c "cd /home/frappe/frappe-bench && cat sites/192.168.20.118/site_config.json" 2>/dev/null | grep default_language | cut -d'"' -f4)

if [ "$DEFAULT_LANG" = "zh" ]; then
    echo -e "${GREEN}✓${NC} 系统默认语言: 简体中文 (zh)"
else
    echo -e "${YELLOW}!${NC} 系统默认语言: $DEFAULT_LANG"
fi
echo ""

echo "2. 检查管理员用户语言..."
ADMIN_LANG=$(docker compose -f docker-compose-prod.yml exec -T lms bash -c "cd /home/frappe/frappe-bench && bench --site 192.168.20.118 console" << 'EOF' 2>/dev/null | grep -A1 "language" | tail -1
import frappe
frappe.connect()
admin = frappe.get_doc("User", "Administrator")
print(f"language: {admin.language}")
exit()
EOF
)

if echo "$ADMIN_LANG" | grep -q "zh"; then
    echo -e "${GREEN}✓${NC} Administrator 用户语言: 简体中文"
else
    echo -e "${RED}✗${NC} Administrator 用户语言未设置或非中文"
fi
echo ""

echo "3. 检查服务状态..."
CONTAINERS=$(docker compose -f docker-compose-prod.yml ps --format json 2>/dev/null | grep -c "running")
if [ "$CONTAINERS" -ge 4 ]; then
    echo -e "${GREEN}✓${NC} 所有服务正常运行"
else
    echo -e "${RED}✗${NC} 部分服务未运行"
fi
echo ""

echo "4. 检查页面访问..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.20.118:8001/lms 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓${NC} 页面访问正常 (HTTP 200)"
else
    echo -e "${RED}✗${NC} 页面访问异常 (HTTP $HTTP_CODE)"
fi
echo ""

echo "========================================"
echo "         验证完成"
echo "========================================"
echo ""
echo -e "${YELLOW}访问地址:${NC}"
echo "  http://192.168.20.118:8001/lms"
echo ""
echo -e "${YELLOW}登录信息:${NC}"
echo "  用户名: Administrator"
echo "  密码: admin"
echo ""
echo -e "${YELLOW}提示:${NC}"
echo "  • 首次访问请清除浏览器缓存"
echo "  • 使用 Ctrl+Shift+Delete 清除缓存"
echo "  • 或使用隐私/无痕模式访问"
echo ""
