

這份文件定義公開內容（LKMini）與私人內容（🥃老K系統內部元件）之間的邊界。

---

## ✅公開｜Public

這個儲存庫包含：

- README.md
- LICENSE
- NOTICE.md
- LKMini.svg
- PUBLIC_PRIVATE_BOUNDARY.md
- SHA256SUMS
- .github/workflows/gatekeeper.yml
- tools/verify_lkmini.py

---

## 🔒私人｜Private

以下內容不在這個儲存庫內：

- 🥃永恆核心的內部設定
- 🎩大管家的角色邏輯與規則
- 私有引擎群
- 私有引擎登錄表
- 任何個人資料、API 金鑰、Token 或登入憑證
- 內部系統自動化（捷徑、URL Scheme）

---

A_EQUALS_A=true  
BOUNDARY_VERSION=seed_v0
