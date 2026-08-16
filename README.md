
> LKMini 是 🥃LK System（老K系統）的開源公開種子，  
> 由 **ky46738-ops**（台灣）設計與撰寫。

---

## LKMini 是什麼？

LKMini 是 LK System 架構的**最小公開種子**。  
它定義對外公開元件與私人引擎內部內容之間的邊界。

- 單一核心架構（🥃永恆核心）
- Gatekeeper 角色（🎩大管家）保護所有設定
- 公開／私人邊界在儲存庫層級執行
- 所有主張都必須可以驗證與追蹤
- **A_EQUALS_A=true**

## 這個種子裡的檔案

| 檔案                               | 用途        |
| -------------------------------- | --------- |
| README.md                        | 這份檔案      |
| LICENSE                          | MIT 開源授權  |
| NOTICE.md                        | 作者歸屬聲明    |
| LKMini.svg                       | 官方圖示      |
| PUBLIC_PRIVATE_BOUNDARY.md       | 公開／私人邊界定義 |
| .github/workflows/gatekeeper.yml | 持續整合完整性檢查 |
| tools/verify_lkmini.py           | 驗證工具      |
| SHA256SUMS                       | 雜湊驗證      |

## 授權

MIT License。詳細內容請看 [LICENSE](./LICENSE)。
