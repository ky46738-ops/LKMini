# 🧩｜老K系統公開種子｜LKMini

> LKMini 是 🥃老K系統的開源公開種子，  
> 由 **Kevin Yang／老K（ky46738-ops，台灣）**設計與撰寫。

---

## LKMini 是什麼？

LKMini 是 🥃老K系統架構的**最小公開種子**。  
它定義對外公開元件與私有引擎內部內容之間的邊界。

- 單一核心架構：🥃永恆核心
- 保護角色：🎩大管家保護所有設定
- 公開／私有邊界在儲存庫層級執行
- 所有主張都必須可以驗證與追蹤
- 核心公理：`A_EQUALS_A=true`

## 這個種子裡的檔案

| 原檔名 | 中文用途 |
|---|---|
| `README.md` | 本說明書 |
| `LICENSE` | MIT 開源授權 |
| `NOTICE.md` | 作者歸屬聲明 |
| `LKMini.svg` | 官方圖示 |
| `PUBLIC_PRIVATE_BOUNDARY.md` | 公開／私人邊界定義 |
| `.github/workflows/gatekeeper.yml` | 持續整合完整性檢查 |
| `tools/verify_lkmini.py` | 驗證工具 |
| `SHA256SUMS` | 雜湊驗證清單 |

## 授權

採用 MIT 開源授權。完整內容請看 [`LICENSE`](./LICENSE)。
