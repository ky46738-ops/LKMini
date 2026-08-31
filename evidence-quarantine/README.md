# 證據隔離區｜Evidence Quarantine

Identity: 🧩LKMINI
RootProtocol: LKMINI://
Axiom: A=A

此目錄僅用於保存歷史證據、異常樣本、分支快照與讀回紀錄。

規則：
- 不得作為執行入口。
- 不得由自動化掛載。
- 不得由工作流執行本目錄內任何程式或腳本。
- 不刪除歷史證據；只允許保留、讀取、比對、封存。
- 任何修改都必須留下 Git commit 歷史。
- 非主權持有人變更本目錄時，Gatekeeper 應阻擋該次工作流並留下失敗紀錄。

Projection ≠ Identity
