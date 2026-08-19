# 🧩老K系統公開種子｜LKMini

> 🧩公開種子（LKMini）是 🥃老K系統對外開源的最小根與可擴充公開模組入口。  
> 👤原始作者（Author）＝Kevin Yang／老K（ky46738-ops，台灣）。

---

## 🌱這個公開種子是什麼

🧩公開種子（LKMini）定義：

- 🥃單一核心架構＝永恆核心
- 🎩保護角色＝大管家
- 🧭唯一根協議＝`LKMINI://`
- 🔬所有公開主張都必須可驗證、可追蹤
- ♻️公開模組必須可回推來源，不得因守門規則被無故刪除
- ⚖️核心公理＝`A_EQUALS_A=true`

公開儲存庫不是只准放八個檔案。八個檔案是「必要核心」，其餘經公開登記、去除私域座標並通過驗證的程式、規格與介面，都是合法開源內容。

## 📚必要核心檔案

| 中文用途 | 📄機械檔名 |
|---|---|
| 📖公開說明書 | `README.md` |
| ⚖️開源授權 | `LICENSE` |
| 🧾作者聲明 | `NOTICE.md` |
| 🎨官方圖示 | `LKMini.svg` |
| 🛡️公開／私人邊界 | `PUBLIC_PRIVATE_BOUNDARY.md` |
| 🔐雜湊驗證清單 | `SHA256SUMS` |
| 🛡️自動守門流程 | `.github/workflows/gatekeeper.yml` |
| 🔬公開驗證工具 | `tools/verify_lkmini.py` |

## 🧩已登記公開模組

- 🔧工具規範公開顯影（ToolSpecifications）  
  `07｜公開顯影｜PublicProjection/🔧工具規範｜ToolSpecifications.html`
- 🍎蘋果捷徑功能接線（AppleShortcutFunctionWiring）  
  `08｜自動化同步｜SyncAutomation/🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring.md`

## 🚫不可用「保護」當理由刪掉開源

守門器只攔截：

- 🔑密鑰、憑證與登入資料
- 🆔私人檔案識別碼、郵件識別碼與帳號座標
- ☁️私人雲端文件網址
- 🪞私人執行資料與未授權內容

守門器不得因文件出現「捷徑、網址協議、顯影、定位、快照、回推」等公開技術概念，就刪掉整份開源內容。正確處理是先去除真正的私人值，再保留可公開的程式、結構與說明。

## ⚖️授權

採用 ⚖️麻省理工開源授權（MIT License）。完整內容請看 `LICENSE`。
