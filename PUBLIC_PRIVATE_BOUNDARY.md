# PUBLIC_PRIVATE_BOUNDARY

This document defines the boundary between public (LKMini) and private (🥃老K系統 internal) components.

---

## ✅ Public (This Repo — LKMini)

- README.md
- LICENSE
- NOTICE.md
- LKMini.svg
- PUBLIC_PRIVATE_BOUNDARY.md
- SHA256SUMS
- .github/workflows/大管家.yml
- tools/verify_lkmini.py

---

公開追蹤檔案固定為上述八份。每次發布以八檔白名單及實際內容驗證為準；歷史與私人資料另行保全。

## 🔒 Private (NOT in this repo)

- 🥃永恆核心 (Eternal Core) internal configuration
- 🎩大管家 (Gatekeeper) role logic and rules
- PRIVATE_ENGINE_FLEET
- ENGINE_REGISTRY_PRIVATE
- Any personal data, API keys, tokens, or credentials
- Internal system automation (Shortcuts, URL Schemes)

---

A_EQUALS_A=true
BOUNDARY_VERSION=seed_v0
