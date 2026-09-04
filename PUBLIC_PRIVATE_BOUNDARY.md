# PUBLIC_PRIVATE_BOUNDARY

This document defines the boundary between public (LKMini) and private (🥃老K系統 internal) components.

---

## ✅ Public (This Repo — LKMini)

- README.md — Project overview
- LICENSE — MIT open source license
- NOTICE — Authorship attribution
- MANIFEST — File registry
- PUBLIC_PRIVATE_BOUNDARY.md — This file
- SHA256SUMS — Hash verification
- .github/workflows/gatekeeper.yml — CI integrity check
- Any files explicitly marked as PUBLIC

---

## 🔒 Private (NOT in this repo)

- 🥃永恆核心 (Eternal Core) internal configuration
- 🎩大管家 (Gatekeeper) role logic and rules
- 私有引擎註冊表 — Private engine registry
- ENGINE_ANCHOR_TEMPLATE — Internal engine templates
- 私有模組註冊表 — Private module registry
- Any personal data, API keys, tokens, or credentials
- Internal system automation (Shortcuts, URL Schemes)

---

## Enforcement

The Gatekeeper workflow will FAIL if any private markers  
(`私有引擎註冊表`, `私有模組註冊表`) are detected in public files.

---

A_EQUALS_A=true  
BOUNDARY_VERSION=seed_v0.1
