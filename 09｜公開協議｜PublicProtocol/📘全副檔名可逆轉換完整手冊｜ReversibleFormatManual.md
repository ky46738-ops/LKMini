# 📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual

## 🧬唯一出口

所有副檔名的原始結構、轉換器、逆向器、封裝器與格式知識，統一收束到 🧬融合唯一出口。其他區域只供應入口、說明、⚙️執行環境（Runtime）、驗證、零件、樣式、快照、自動化與唯一真相，不建立第二出口。

## ➡️共通正向流程

來源原件
→ 📦原始位元（ORIGINAL）唯讀保存
→ 🔍魔術位元（Magic Bytes）／🧾媒體類型（MIME）／副檔名／🪪本體身分（Identity）辨識
→ 📥安全掛載（MOUNT）
→ 內容索引與逐件 🔐雜湊（SHA256）
→ 解析／零件化／🪞顯影（Projection）
→ 📸快照封包（SNAPSHOT ZIP）
→ 📜清單（Manifest）／🧭定位器（Locator）／🔐雜湊清單（SHA256SUMS）／♻️回推鏈（ReverseChain）
→ 🧬融合唯一出口
→ 📤輸出（Output）
→ 📥讀回（ReadBack）

## ⬅️共通逆向流程

📸快照封包（SNAPSHOT ZIP）
→ 壓縮結構／循環冗餘檢查（CRC）／📜清單（Manifest）／🔐雜湊清單（SHA256SUMS）驗證
→ 原始原件取回
→ 原名、位元組數、🔐雜湊（SHA256）驗證
→ ♻️還原（Restore）
→ `A=A`

## 🍎蘋果格式

- `.pages`、`.numbers`、`.key`：原包保持同一 🪪本體身分（Identity）；依真實內部結構分流。🌐網頁（HTML）、📊試算表、📄逗號分隔資料（CSV）、📄定位分隔資料（TSV）、🧾結構化資料（JSON）、🖼️圖片（PNG）與 📄可攜文件（PDF）均為顯影，不取代原件。
- `.ipa`、`.app`、`.dmg`、`.pkg`、`.plist`、`.shortcut`：依 🔍魔術位元（Magic Bytes）與真實容器格式分流，不一律改名成壓縮檔；原生簽章、安裝、匯入、啟動與真機讀回由相符裝置端驗證。

## 🌐網頁與文字

`.html`、`.css`、`.js`、`.json`、`.md`、`.svg`：保存原件、驗證結構、建立顯影並支援原始位元回航。

## 📦壓縮與封裝

`.zip`、`.rar`、`.7z`、`.tar`、`.iso`：依真實 🔍魔術位元（Magic Bytes）與可用解包工具處理；原件永遠保存在唯讀原始區。

## 🐧企鵝系統（Linux）與 🪟視窗系統（Windows）

`.deb`、`.exe`、`.dll`、`.msi`：保存原件與結構索引；原生重建、簽章與執行由相符平台工具驗證。

## 🎞️媒體

`.mp4`、`.mov`、`.png`、`.jpg`、`.mp3`：保存原件；顯影與轉碼屬於 🪞顯影（Projection）；有損轉換不得宣稱位元可逆。

## 🧩無副檔名

以 🔍魔術位元（Magic Bytes）、📜清單（Manifest）、🧭定位器（Locator）與 🪪本體身分（Identity）辨識，不以副檔名決定本體。

## ♻️固定回推

來源 → 🧬融合唯一出口 → 🪞幻影膠囊 → 🧩LKMINI → `LKMINI://` → `A=A`
