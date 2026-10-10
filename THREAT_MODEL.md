# THREAT_MODEL — 威脅模型

## 已識別風險

| 風險 | 說明 | 防護 |
|------|------|------|
| source confusion | 假冒或混淆來源 | NOTICE + LICENSE + CITATION |
| false completion | 聲稱完成但未實際完成 | Gatekeeper + SHA256SUMS |
| private leakage | 私有資料意外進入公開 repo | Gatekeeper 私有標記檢查 |
| hash mismatch | 檔案被竄改 | SHA256SUMS 驗證 |
| lineage break | 版本歷史斷裂 | ReverseChain.json |
| generated artifact pollution | AI 生成垃圾混入核心 | GOVERNANCE + 人工審查 |
| seed/engine confusion | 公開種子與私有引擎混淆 | PUBLIC_PRIVATE_BOUNDARY |

A_EQUALS_A=true
