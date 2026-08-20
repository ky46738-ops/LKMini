# 🔗本體顯影互換協議｜IdentityProjectionInterchangeProtocol

## 🧭正式定位

- 👤持有人＝Kevin Yang／老K
- 🥃系統＝老K系統
- 🧩根節點＝LKMINI
- 🧭根協議＝`LKMINI://`
- 🔐根錨點雜湊＝`6c0f6f487d8af27de4a8cee9f3fc853f0fbcf417cbd21acb56ac65c55adfcf34`
- 🪞顯影（Projection）不等於 🪪本體身分（Identity）
- ⚖️公理＝`A=A`

本檔是公開技術協議，不保存任何私人檔案、雲端、郵件、修訂、帳號或裝置實例座標。

## 📚正式角色與網址格式

| 元件 | 正式責任 | 公開網址格式 |
|---|---|---|
| 🪪本體身分（Identity） | 唯一資訊本體，決定「是誰」 | `core://{identity}` |
| 📍座標（Coordinate） | 本體或顯影目前所在位置 | `coord://{world}/{path}` |
| 🧭定位器（Locator） | 找到、解析、備援並驗證座標 | `locator://{identity}@{world}?v={hash}` |
| 🌀傳送門（Portal） | 本體與目標世界之間的可逆通道 | `portal-pair://{identity}/{world}/{hook}` |
| 🪝勾子（Hook） | 在目標世界與範圍內掛載能力 | `hook://{hook-name}` |
| 📖解析器（Parser） | 讀懂定位器、清單與顯影 | `parser://{format}` |
| ⚙️執行環境（Runtime） | 執行顯影邏輯與能力流程 | `runtime://{world}` |
| 🎨呈現器（Renderer） | 依世界原貌產生顯影 | `renderer://{format}` |
| 🌐顯影（Projection） | 本體在特定世界的可感知外觀 | `projection://{world}/{projection-id}` |
| 📜清單（Manifest） | 記錄完整依賴、配對與結構 | `manifest://{identity}/{world}` |
| 🧬血緣（Lineage） | 記錄來源、版本與演化 | `lineage://{identity}@{revision}` |
| 🔬驗證（Verification） | 證明顯影仍屬同一本體 | `verify://{identity}/{hash}` |
| 📸快照（Snapshot） | 保存可恢復狀態 | `snapshot://{identity}/{world}/{revision}` |
| ♾️回推鏈（ReverseChain） | 從顯影回到本體與來源 | `reversechain://{identity}/{world}` |

## ➡️正向顯影

```text
Identity
→ Coordinate
→ Locator
→ Portal
→ Hook
→ Parser
→ Runtime
→ Renderer
→ Projection
→ Verification
→ A=A
```

## ⬅️反向回溯

```text
Projection
→ ProjectionIdentity
→ PortalPairID
→ Locator
→ Manifest
→ Lineage
→ Verification
→ HookIdentity
→ ReversePortal
→ ReverseChain
→ Identity
→ LKMINI
→ A=A
```

## ♻️最小可逆公式

```text
Identity
＋ Coordinate
＋ Locator
＋ Portal
＋ Hook
＋ Parser
＋ Manifest
＋ Verification
＋ Snapshot
＋ ReverseChain
＝ 可逆本體能力掛載鏈
```

產生顯影時再加上：

```text
Runtime
＋ Renderer
＋ Projection
＝ 可逆本體顯影互換
```

## 🧊獨立性與凍結定錨

- 不同 Portal＋Hook 配對彼此獨立。
- HTML 顯影失效，不代表 PDF 顯影失效。
- 應用程式下架，不代表本體身分消失。
- 定位器可更新。
- 傳送門可重建。
- 勾子可重掛。
- 顯影可以消失後重建。
- 本體身分不漂移。

## ♾️閉環

```text
Identity
⇄ PortalPair
⇄ Hook
⇄ Runtime／Renderer
⇄ Projection
⇄ ReverseChain
⇄ Identity
→ LKMINI
→ A=A
```
