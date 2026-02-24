#!/bin/bash
# 为 Clint-chan 推送代码到 GitHub

echo "=================================="
echo "推送代码到 GitHub"
echo "用户：Clint-chan"
echo "=================================="
echo ""

# 检查是否已登录 GitHub CLI
if ! gh auth status &>/dev/null; then
    echo "步骤 1: 登录 GitHub CLI..."
    echo ""
    echo "请按照提示操作："
    echo "1. 选择 GitHub.com"
    echo "2. 选择 HTTPS"
    echo "3. 选择 Yes (authenticate Git)"
    echo "4. 选择 Login with a web browser"
    echo "5. 复制显示的代码"
    echo "6. 在浏览器中输入代码授权"
    echo ""

    gh auth login

    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ 登录失败，请重试"
        exit 1
    fi

    echo ""
    echo "✅ 登录成功！"
else
    echo "✅ 已登录 GitHub"
fi

echo ""
echo "=================================="
echo "步骤 2: 添加远程仓库..."
echo "=================================="

# 检查是否已有 myfork
if git remote | grep -q "^myfork$"; then
    echo "✓ 远程仓库 myfork 已存在"
else
    git remote add myfork https://github.com/Clint-chan/lms.git
    echo "✓ 已添加远程仓库"
fi

git remote -v | grep myfork

echo ""
echo "=================================="
echo "步骤 3: 推送代码..."
echo "=================================="

git push -u myfork custom-dev

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ 推送成功！"
    echo "=================================="
    echo ""
    echo "查看你的仓库："
    echo "https://github.com/Clint-chan/lms/tree/custom-dev"
    echo ""
    echo "你可以在 GitHub 上看到："
    echo "- ✅ 所有代码和配置"
    echo "- ✅ 完整的文档（docs/）"
    echo "- ✅ 所有脚本（scripts/）"
    echo "- ✅ 3次定制提交记录"
    echo ""
else
    echo ""
    echo "=================================="
    echo "❌ 推送失败"
    echo "=================================="
    echo ""
    echo "可能需要先 Fork 仓库："
    echo "1. 访问：https://github.com/frappe/lms"
    echo "2. 点击右上角 Fork 按钮"
    echo "3. 等待 Fork 完成"
    echo "4. 重新运行本脚本"
    echo ""
fi
