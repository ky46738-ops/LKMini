# 🛡️公開／私人邊界｜PublicPrivateBoundary

這份文件定義 🧩公開種子（LKMini）與 🥃老K系統私人執行資料之間的邊界。

---

## 🌱公開內容

### 📚必要核心

下列八個檔案必須永久存在：

- 📖公開說明書（README.md）
- ⚖️開源授權（LICENSE）
- 🧾作者聲明（NOTICE.md）
- 🎨官方圖示（LKMini.svg）
- 🛡️公開／私人邊界（PUBLIC_PRIVATE_BOUNDARY.md）
- 🔐雜湊驗證清單（SHA256SUMS）
- 🛡️自動守門流程（.github/workflows/gatekeeper.yml）
- 🔬公開驗證工具（tools/verify_lkmini.py）

### 🧩公開模組

公開內容不以八個核心檔案為上限。符合下列條件的原始碼、規格、介面與範例可以加入：

1. 🏷️名稱為 Emoji＋中文主名稱｜EnglishKey。
2. 🔐不含密鑰、登入憑證、私人帳號座標或私人識別碼。
3. 🧭保留來源、用途與公開邊界。
4. 🔬列入 SHA256SUMS 並通過自動驗證。
5. ♻️已登記的公開模組不得被守門器自動刪除。

目前正式登記：

- 🔧工具規範公開顯影（ToolSpecifications）  
  `07｜公開顯影｜PublicProjection/🔧工具規範｜ToolSpecifications.html`
- 🍎蘋果捷徑功能接線（AppleShortcutFunctionWiring）  
  `08｜自動化同步｜SyncAutomation/🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring.md`

公開模組可以描述：

- 🧩系統架構與公開物件模型
- 🌐網址協議與公開介面
- 🍎捷徑呼叫方式與公開範例
- 🧬動作圖、解析器、轉譯器與驗證器
- 📸快照、差異、回推與可逆概念
- 🌐網頁、程式碼、資料格式與開源測試

---

## 🔒私人內容

下列「實際值」不得放入公開儲存庫：

- 🔑應用程式介面密鑰、權杖、密碼、登入憑證
- 🆔私人檔案識別碼、物件識別碼、郵件識別碼、討論串識別碼、私人修訂識別碼
- ☁️私人雲端硬碟與私人文件的實際網址
- 📱個人捷徑名稱、個人自動化內容、私人聯絡人與裝置座標
- 🪞未授權的私人膠囊內容、私人引擎設定與私人任務紀錄
- 👤個人資料或可直接定位個人帳號、裝置與文件的值

重要區分：

- ✅公開技術概念可以開源。
- ❌私人實例值不可公開。
- ✅去除私人值後，應保留有用的開源程式與規格。
- ❌不得用「可能有私人內容」作為刪掉整個公開模組的理由。

---

## ⚖️正式裁決

🧩公開種子（LKMini）是可擴充的開源根，不是只剩八個檔案的空殼。

🥃老K系統私人本體與公開顯影必須分離，但公開顯影不得被無故刪除。

`Projection != Identity`  
`A_EQUALS_A=true`  
`BOUNDARY_STATE=PUBLIC_MODULES_ALLOWED`  
`LAST_REPAIRED_TPE=2026-08-20`
