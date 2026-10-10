# SECURITY — LKMini 安全政策

## 範圍

此 repo 為公開種子，不含私有引擎或核心設定。

## 回報安全問題

請透過 GitHub Issues 回報，標記 `security`。

## 私有資料保護

Gatekeeper workflow 會自動檢查以下私有標記是否意外出現在公開檔案中：
- `PRIVATE_ENGINE`
- `ENGINE_REGISTRY_PRIVATE`

如發現私有資料外洩，請立即通知 @ky46738-ops。

## 完整性驗證

所有核心檔案透過 SHA256SUMS 驗證。

A_EQUALS_A=true
