#!/bin/bash
# 推送代码到 GitHub 的脚本

echo "=================================="
echo "推送代码到 GitHub"
echo "=================================="
echo ""

# 检查是否已经添加了 myfork
if git remote | grep -q "^myfork$"; then
    echo "✓ 远程仓库 'myfork' 已存在"
    git remote -v | grep myfork
else
    echo "请输入你的 GitHub 用户名："
    read GITHUB_USERNAME

    if [ -z "$GITHUB_USERNAME" ]; then
        echo "❌ 用户名不能为空"
        exit 1
    fi

    echo ""
    echo "添加远程仓库..."
    git remote add myfork https://github.com/$GITHUB_USERNAME/lms.git

    echo "✓ 已添加远程仓库："
    git remote -v | grep myfork
fi

echo ""
echo "=================================="
echo "开始推送代码..."
echo "=================================="

# 推送到 custom-dev 分支
git push -u myfork custom-dev

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ 推送成功！"
    echo "=================================="
    echo ""
    echo "查看你的仓库："
    REMOTE_URL=$(git remote get-url myfork)
    REPO_URL=$(echo $REMOTE_URL | sed 's/\.git$//')
    echo "$REPO_URL/tree/custom-dev"
    echo ""
else
    echo ""
    echo "=================================="
    echo "❌ 推送失败"
    echo "=================================="
    echo ""
    echo "可能的原因："
    echo "1. 还没有 Fork 仓库"
    echo "2. GitHub 用户名输入错误"
    echo "3. 需要身份验证"
    echo ""
    echo "请检查并重试"
fi
