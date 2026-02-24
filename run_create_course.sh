#!/bin/bash

echo "========================================"
echo "  自动创建 LMS 课程"
echo "========================================"
echo ""

cd /home/services/lms

# 复制文件到容器
echo "1. 准备文件..."
docker compose -f docker-compose-prod.yml cp parse_course_doc.py lms:/tmp/
docker compose -f docker-compose-prod.yml cp create_course_from_doc.py lms:/tmp/
docker compose -f docker-compose-prod.yml cp docs/course/V8.1一周学习版_v4_compact.docx lms:/tmp/
docker compose -f docker-compose-prod.yml cp docs/course/course_structure.json lms:/tmp/ 2>/dev/null || echo "  (结构文件将在容器内生成)"
echo "✓ 文件准备完成"
echo ""

# 在容器内执行
echo "2. 解析文档并创建课程..."
echo ""

docker compose -f docker-compose-prod.yml exec -T lms bash << 'EOF'
cd /home/frappe/frappe-bench

# 安装 python-docx
pip install python-docx -q

# 解析文档
echo "正在解析文档..."
python3 /tmp/parse_course_doc.py

# 复制结构文件到正确位置
mkdir -p /tmp/docs/course
cp /tmp/course_structure.json /tmp/docs/course/

# 创建课程
echo ""
echo "正在创建课程..."
bench --site 192.168.20.118 console < /tmp/create_course_from_doc.py

EOF

echo ""
echo "========================================"
echo "  完成！"
echo "========================================"
echo ""
echo "请访问以下地址查看课程："
echo "http://192.168.20.118:8001/courses"
echo ""
