# 公開／私人邊界｜Public Private Boundary

這份文件定義公開內容（LKMini）與私人內容（🥃老K系統內部元件）之間的邊界。

---

## 公開｜Public

這個儲存庫只允許下列 8 個公開最小種子檔：

- README.md
- LICENSE
- NOTICE.md
- LKMini.svg
- PUBLIC_PRIVATE_BOUNDARY.md
- SHA256SUMS
- .github/workflows/gatekeeper.yml
- tools/verify_lkmini.py

公開種子只提供：

- 專案名稱與開源說明
- 授權條款與作者聲明
- 公開邊界規則
- 公開圖示
- 公開檔案雜湊
- 公開驗證工具與 GitHub Actions gate

---

## 私人｜Private

以下內容不得放入這個公開儲存庫：

- 🥃老K系統完整本體
- 🥃永恆核心的內部設定
- 🎩大管家的角色邏輯與規則
- 🪞幻影膠囊、膠囊內容、膠囊封裝
- 私有引擎群與私有引擎登錄表
- Current、Locator、Manifest、ReverseChain、Snapshot、Package
- 任務筆記本、正式任務鏈、執行回執、接線回執
- Google Drive、Library、Gmail、Obsidian、Apple Shortcuts 的私域接線資料
- Drive FileID、Library StableID、ObjectID、MessageID、ThreadID、Revision、Commit 等內部追蹤欄位
- drive.google.com、docs.google.com、shortcuts://、obsidian:// 等私域入口或 URL Scheme
- 任何個人資料、API 金鑰、Token 或登入憑證
- HTML、PDF、ZIP、JSON、CSV、TSV、影像、影片或 AICORE 等正式投影與封裝輸出

---

## 裁決｜Decision

LKMini 是公開種子，不是 🥃老K系統私有 Runtime。

Projection != Identity
A_EQUALS_A=true
BOUNDARY_VERSION=seed_v0
LAST_REPAIRED_TPE=2026-08-19
