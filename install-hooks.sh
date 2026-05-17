#!/usr/bin/env bash
# install-hooks.sh
# 執行一次，把 .githooks 裡的鉤子安裝到本地 .git/hooks
# 用法：bash install-hooks.sh

set -e

echo "🔧 安裝 LKMini git hooks..."

cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ pre-commit hook 安裝完成"
echo "從現在起，每次 commit 前會自動檢查 SHA256SUMS 登記。"
echo ""
echo "工作流程："
echo "  1. 新增或修改 .md 檔案"
echo "  2. shasum -a 256 <file> >> SHA256SUMS"
echo "  3. git add <file> SHA256SUMS"
echo "  4. git commit"
echo ""
echo "A=A 強制執行。未登記 = 擋住。"
