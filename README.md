# 🧩老K系統公開種子｜LKMini

> 🧩公開種子（LKMini）是 🥃老K系統對外開源的最小根與可擴充公開模組入口。  
> 👤原始作者（Author）＝Kevin Yang／老K（ky46738-ops，台灣）。

---

## 🌱這個公開種子是什麼

🧩公開種子（LKMini）定義：

- 🥃單一核心架構＝永恆核心
- 🎩保護角色＝大管家
- 🧭唯一根協議＝`LKMINI://`
- 🌐唯一外顯格式＝`LKMINI://物件名稱/動作`
- 🔬所有公開主張都必須可驗證、可追蹤
- ♻️公開模組必須可回推來源，不得因守門規則被無故刪除
- ⚖️核心公理＝`A_EQUALS_A=true`

📖公開說明書（README）是儲存庫入口顯影，不是 🪪本體身分（Identity）。  
🧾公開模組登記是目前公開模組的唯一清冊；九個必要核心只是最低保護集合，不是公開內容上限。

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
| 🧾公開模組登記 | `🧾公開模組登記｜PublicModuleRegistry.json` |

## 🧩已登記公開模組

| 公開模組 | 🌐外顯網址 | 📍正式相對路徑 |
|---|---|---|
| 🔧工具規範｜ToolSpecifications | `LKMINI://工具規範/查看` | `07｜公開顯影｜PublicProjection/🔧工具規範｜ToolSpecifications.html` |
| 🎨介面研究互動範例｜UIResearchInteractiveExamples | `LKMINI://介面研究/操作` | `07｜公開顯影｜PublicProjection/🎨介面研究互動範例｜UIResearchInteractiveExamples.html` |
| 🖥️動作容器互動範例｜ActionContainerInteractiveExample | `LKMINI://動作容器/操作` | `07｜公開顯影｜PublicProjection/🖥️動作容器互動範例｜ActionContainerInteractiveExample.html` |
| 🎴本體顯影關係圖｜IdentityProjectionDiagram | `LKMINI://本體顯影關係圖/查看` | `07｜公開顯影｜PublicProjection/🎴本體顯影關係圖｜IdentityProjectionDiagram.svg` |
| 🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring | `LKMINI://蘋果捷徑/查看` | `08｜自動化同步｜SyncAutomation/🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring.md` |
| 🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder | `LKMINI://工具規範建置器/執行` | `08｜自動化同步｜SyncAutomation/🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder.py` |
| 🔧工具規範公開建置流程｜ToolSpecificationsPublicBuildWorkflow | `LKMINI://工具規範建置流程/執行` | `.github/workflows/🔧工具規範公開建置流程｜ToolSpecificationsPublicBuildWorkflow.yml` |
| 🌱唯一真相源｜MarkdownSeed | `LKMINI://唯一真相源/查看` | `09｜公開協議｜PublicProtocol/🌱唯一真相源｜MarkdownSeed.md` |
| 🧭動作鏈｜S0-S10 | `LKMINI://動作鏈/查看` | `09｜公開協議｜PublicProtocol/🧭動作鏈｜S0-S10.md` |
| 📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual | `LKMINI://全副檔名可逆轉換手冊/查看` | `09｜公開協議｜PublicProtocol/📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual.md` |
| ♾️公開回推鏈｜PublicReverseChain | `LKMINI://公開回推鏈/查看` | `09｜公開協議｜PublicProtocol/♾️公開回推鏈｜PublicReverseChain.json` |
| 🧭公開定位器｜PublicLocator | `LKMINI://公開定位器/查看` | `09｜公開協議｜PublicProtocol/🧭公開定位器｜PublicLocator.json` |
| 🧾開源刪除鑑識清冊｜OpenSourceDeletionForensics | `LKMINI://開源刪除鑑識清冊/查看` | `09｜公開協議｜PublicProtocol/🧾開源刪除鑑識清冊｜OpenSourceDeletionForensics.json` |

目前固定保護：`13` 個公開模組。新增模組時，必須同時更新 🧾公開模組登記、🔬公開驗證器與 🔐雜湊清單，不能只改其中一處。

## 🚫不可用「保護」當理由刪掉開源

守門器只攔截：

- 🔑密鑰、憑證與登入資料
- 🆔私人檔案識別碼、郵件識別碼與帳號座標
- ☁️私人雲端文件網址
- 🪞私人執行資料與未授權內容

守門器不得因文件出現「捷徑、網址協議、顯影、定位、快照、回推」等公開技術概念，就刪掉整份開源內容。正確處理是：

私人值定位
→ 局部去除或改成公開佔位符
→ 保留公開程式、結構與說明
→ 更新登記與雜湊
→ 重新驗證
→ `A=A`

## ⚖️授權

採用 ⚖️麻省理工開源授權（MIT License）。完整法律原文請看 `LICENSE`。

⚖️正式法律原文保留在 `LICENSE`，避免翻譯改寫造成授權識別失真；中文說明只作閱讀輔助，不取代正式原文。
