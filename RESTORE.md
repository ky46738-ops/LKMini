# RESTORE — LKMini 恢復指南

## 如何從 seed_v0 恢復

1. Clone repo
```bash
git clone https://github.com/ky46738-ops/LKMini.git
cd LKMini
```

2. 驗證完整性
```bash
python3 tools/verify_lkmini.py
```

3. 確認 SHA256SUMS
```bash
sha256sum -c SHA256SUMS
```

4. 確認 A=A 標記
```bash
grep 'A_EQUALS_A=true' README.md
```

## 重要原則

- Public seed 只包含公開邊界內的檔案
- Private engine fleet 不在此 repo
- 永恆核心內部設定不在此 repo

A_EQUALS_A=true
