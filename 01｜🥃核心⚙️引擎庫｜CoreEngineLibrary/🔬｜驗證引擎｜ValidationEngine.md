# 🔬｜驗證引擎｜ValidationEngine

## 📖｜概覽｜Overview

每一次驗證完成後，針對實際目標檔案計算 64 字元 🔐｜SHA256｜SHA256，作為 🏷️｜唯一識別徽章｜BadgeID，並與 🕒｜時間戳｜Timestamp 組成 📍｜徽章定位器｜BadgeLocator。

## ⚓️｜錨點流程｜AnchorFlow

📥｜待驗證檔案｜Target
→ 🔐｜實際雜湊｜ACTUAL_SHA256
→ 🎯｜預期雜湊｜EXPECTED_SHA256
→ ⚖️｜比對｜Compare

### ✅｜通過｜PASS

→ 🏷️｜徽章識別碼｜BadgeID = ACTUAL_SHA256
→ 🕒｜時間戳｜Timestamp = YYYYMMDD-HHMMSS
→ 📍｜徽章定位器｜BadgeLocator
→ 📋｜驗證日誌｜verify_log.json
→ 🚩｜驗證通過旗標｜verify_pass.flag
→ 📸｜快照｜Snapshot
→ ↩️｜反向鏈｜ReverseChain

定位器格式：
`https://engine.local/badge/<SHA256_64>?ts=<YYYYMMDD-HHMMSS>`

此格式是 Locator Schema；沒有實際服務時，不宣稱它是公開可連網址。

### ❌｜失敗｜FAIL

→ 寫入 `hashfail_<Timestamp>.log`
→ 🚫｜禁止版本切換｜BlockVersionSwitch
→ 📦｜保留來源｜PreserveSource
→ 📸｜保存證據｜PreserveEvidence

## 🔬｜驗收｜Acceptance

可讀、可驗證、可追溯、可回滾、可重建、可交付。
任何同步端沒有 ReadBack，不得判定同步成功。
