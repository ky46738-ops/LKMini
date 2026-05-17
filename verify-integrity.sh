#!/usr/bin/env bash
set -e

echo "========================================="
echo "  Semantic Civilization Architecture"
echo "  A=A Integrity Verification"
echo "  Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="
echo ""

# 檢查 SHA256SUMS 存在
if [ ! -f SHA256SUMS ]; then
  echo "❌ 錯誤: 找不到 SHA256SUMS"
  exit 1
fi

# 跑驗證
echo "▶ 驗證檔案完整性..."
if shasum -a 256 -c SHA256SUMS > verify_report.txt 2>&1; then
  echo "✅ 全部通過"
  PASSED=1
else
  echo "❌ 發現失敗"
  PASSED=0
fi

# 統計
TOTAL=$(grep -v '^#' SHA256SUMS | grep -v '^$' | wc -l | tr -d ' ')
OK=$(grep -c " OK$" verify_report.txt || true)
FAIL=$(grep -c " FAILED$" verify_report.txt || true)

echo ""
echo "結果統計:"
echo "  總檔案數: $TOTAL"
echo "  通過:     $OK"
echo "  失敗:     $FAIL"
echo ""
echo "詳細報告已保存到: verify_report.txt"
echo ""

# 輸出到控制台
cat verify_report.txt

# 退出碼
if [ $PASSED -eq 1 ]; then
  echo ""
  echo "🔒 A=A 成立。文明狀態: ALIVE"
  exit 0
else
  echo ""
  echo "⚠️  發現污染檔案，立即隔離"
  echo "    ReverseChain(Seed_v0) 可回推至今晚封存狀態"
  exit 1
fi
