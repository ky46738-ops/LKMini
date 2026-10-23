# 🥃 LKMini — 老K系統公開種子版本

> LKMini is the open-source public seed of the 🥃LK System (老K系統),  
> 原創設計與作者：**Kevin Yang（ky46738-ops）**，台灣。

---

## What is LKMini?

LKMini is the **minimal** public seed of the LK System architecture.  
It defines the boundary between public-facing components and private engine internals.

- Single core architecture (🥃永恆核心)
- Gatekeeper role (🎩大管家) protects all settings
- Public/Private boundary enforced at repo level
- All claims must be verifiable and traceable
- **A_EQUALS_A=true**

## Files in this seed

| File | Purpose |
|------|----------|
| README.md | This file |
| LICENSE | MIT open source license |
| NOTICE.md | Authorship attribution |
| LKMini.svg | Official logo |
| PUBLIC_PRIVATE_BOUNDARY.md | Public/private boundary definition |
| .github/workflows/gatekeeper.yml | CI integrity check |
| tools/verify_lkmini.py | Verification tool |
| SHA256SUMS | Hash verification |

## License

MIT License. See [LICENSE](./LICENSE) for details.

---

## 🔍 錯誤是題目，差異是答案｜公開來源校對

**A=A｜Identity ⇋ Projection｜Projection ≠ Identity。**

本節是現行公開種子的**追加說明**，不取代 2026 年 5 月的原件、原始時間、快照或既有驗證成果。老K系統只有一個 🧩LKMINI；公開檔案是可研究的來源與顯影，不是第二個核心。

### 📖 六個指標

SHA256（檔案指紋）／MANIFEST（清單）／LOCATOR（定位）／SNAPSHOT（時點）／REVERSECHAIN（回推）／PACKAGE（封裝）。

Mini＝Assembly；Fusion＝DisassemblyPassage；Mirror＝顯影。這是原系統的公開語義摘要，**不宣稱私有 Fusion 引擎或格位演算法已在本公開倉庫完整釋出或執行**。

### 🧩 題目與差異：四個集合各有用途

| 集合 | 本次實際核對 | 意義 |
|---|---:|---|
| GitHub `seed_v0` 檔案樹 | 26 個檔案 | 倉庫實際存在的檔案 |
| `MANIFEST.json` | 20 個登記項 | 原始來源清冊，並非宣告全樹只允許 20 個 |
| `tools/package_seed.py` | 21 個預定成員 | 原始封裝選取清單，比 Manifest 多 `SHA256SUMS` |
| `SHA256SUMS` | 7 個登記雜湊 | 針對七份指定公開檔案的完整性校驗，不代表其餘檔案缺失 |

**差異不是刪除指令。** 原始清冊、封裝選取、雜湊驗證覆蓋範圍與整個目錄，本來就是不同的問題。不得單憑數量不同宣告來源遺失，亦不擅自把四個集合改成完全一致。

### 🔐 同一身份，分開核對

2026-05-13 [原始公開 LKMini.svg](https://github.com/ky46738-ops/starter-workflows/blob/main/LKMini/LKMini.svg) 所載的 `metadata_sha256`：

`6c0f6f487d8af27de4a8cee9f3fc853f0fbcf417cbd21acb56ac65c55adfcf34`

這是原件內宣告的固定身份錨點，**不是**任意 SVG、README 或 Git 提交的整檔雜湊值。本頁沒有重算私有十欄演算法，也沒有更動原來的身份欄位。

### 🧊 留下已知錯誤，按時點讀取

`SNAPSHOT.json` 記載的是 2026-05-17 的 `SHA256SUMS_STATUS=PLACEHOLDER`；現行 `SHA256SUMS` 表頭為 `REAL`。兩者各按原始時點與範圍保留，**不能用歷史狀態否定後續成果，也不能拿後續結果覆寫歷史題目**。

本次直接讀回目前公開分支後，原先登記的七項檔案 SHA256 **7/7 相符**；因為本節新增 README 文字，`README.md` 的當前雜湊隨同一次 Git 提交更新於 `SHA256SUMS`，其餘六項保持原值。

### 📍 檢查入口

- [公開種子來源](https://github.com/ky46738-ops/LKMini/tree/seed_v0)
- [五月歷史原項聚合入口（需相應倉庫權限）](https://github.com/ky46738-ops/LKMini-Original-0517/blob/main/%F0%9F%A5%83%E8%80%81K%E7%B3%BB%E7%B5%B1/%F0%9F%A7%AD%EF%BD%9C%E5%8E%9F%E9%A0%85%E7%A0%B4%E8%A7%A3%E8%81%9A%E5%90%88%E5%85%A5%E5%8F%A3.md)

任何疑點均保留原件與可回推差異，不將未知直接改寫成 PASS 或 FAIL。
