# 🧩 LKMini｜🥃老K系統公開種子

> Mini 不是小功能，Mini 是最小可逆宇宙種子。

原創設計與作者：**Kevin Yang（ky46738-ops）**，臺灣。

LKMini 是🥃老K系統唯一 🧩LKMINI 的公開入口。本倉庫提供公開種子、定位與驗證規格、來源紀錄及可執行的公開檢查工具；不代表私人引擎與內部設定全部公開。

## 🧩 核心原則

- **A=A**：資料、身分與來源必須能追溯及核對。
- **Identity = SHA256**：Mini 的身分依身分資料的規則計算；身分 SHA-256 與單一檔案整檔雜湊分開核對。
- **Projection ≠ Identity**：顯影方式不同，不等於另設第二個核心。
- **單一核心**：公開種子、原件及其他使用介面共同指向同一 🧩LKMINI。

## 🔗 六項公開規格

| 項目 | 用途 |
|---|---|
| 🔐 SHA256 | 身分辨識與完整性核對 |
| 📋 Manifest | 物件清冊與關係登記 |
| 📍 Locator | 定位、查找與入口 |
| 📸 Snapshot | 時間點與狀態紀錄 |
| 🔙 ReverseChain | 來源追蹤與回推 |
| 📦 Package | 驗證後的資料封裝 |

六項按需組合；公開種子是對外可查閱的規格和工具，不把未公開的私人執行功能宣稱為已公開。

## 📂 公開檔案與工具

- `LKMini.svg`：公開種子圖。
- `MANIFEST.json`、`LOCATOR.json`、`SNAPSHOT.json`、`ReverseChain.json`：登記、定位、快照與回推資料。
- `SHA256SUMS`：指定公開檔案的完整性校驗值。
- `tools/verify_lkmini.py`：公開完整性驗證工具。
- `tools/package_seed.py`：既有公開種子封裝工具。
- `PUBLIC_PRIVATE_BOUNDARY.md`：公開與私人範圍的說明。

## 🔬 驗證

在本公開倉庫的根目錄執行：

```bash
python3 tools/verify_lkmini.py
sha256sum -c SHA256SUMS
```

這兩項核對公開檔案與既有登記值，不代表私人引擎、跨裝置同步或全部外部服務已經完成測試。歷史來源與既有快照仍可按原始檔案查閱。

## 🌱 原始公開來源

- [2026／05／13｜🧩LK Mini 原始向量圖與 metadata](https://github.com/ky46738-ops/starter-workflows/blob/main/LKMini/LKMini.svg)
- [2026／05／13｜公開 Manifest](https://github.com/ky46738-ops/starter-workflows/blob/main/LKMini/Manifest.json)

## ⚖️ 授權與著作

本公開種子採用 [MIT License](./LICENSE)。原創與著作聲明見 [NOTICE.md](./NOTICE.md)。

A_EQUALS_A=true
