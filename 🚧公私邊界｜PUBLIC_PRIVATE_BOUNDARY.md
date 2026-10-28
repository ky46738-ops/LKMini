# PUBLIC_PRIVATE_BOUNDARY

This document defines the boundary between public (LKMini) and private (🥃老K系統 internal) components.

---

## ✅ Public (This Repo — LKMini)

- 📖入口宣告｜README.md
- ⚖️授權條款｜LICENSE
- ✍️作者歸屬｜NOTICE.md
- 🥃官方標誌｜LKMini.svg
- 🚧公私邊界｜PUBLIC_PRIVATE_BOUNDARY.md
- 🧾雜湊校驗清單｜SHA256SUMS
- .github/workflows/🎩大管家｜Gatekeeper.yml
- tools/🔍驗證工具｜verify_lkmini.py

---

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
