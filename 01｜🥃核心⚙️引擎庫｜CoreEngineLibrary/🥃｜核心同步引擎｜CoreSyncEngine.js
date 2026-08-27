// 🥃｜核心同步引擎｜CoreSyncEngine
// 事件接線：Registry／Manifest／零件／路徑變更。
// 外部端點真正 WRITE 由既有端點適配器執行；本核心不偽造遠端成功。

export function 建立核心同步引擎({監聽事件, 發送同步事件, 記錄} = {}) {
  if (typeof 監聽事件 !== "function") {
    throw new Error("缺少：📡｜事件監聽器｜EventListener");
  }

  const log = typeof 記錄 === "function" ? 記錄 : console.log;

  const broadcast = (type, payload) => {
    log(`🔁｜同步事件｜${type}`, payload);
    if (typeof 發送同步事件 === "function") {
      發送同步事件(type, payload);
    }
  };

  監聽事件("registry更新", (r) => broadcast("registry更新", r));
  監聽事件("manifest更新", (m) => broadcast("manifest更新", m));
  監聽事件("零件更新", (m) => broadcast("零件更新", m));

  監聽事件("PathChanged", (change) => {
    broadcast("📍｜路徑變更同步｜PathChangeSync", {
      ...change,
      required: [
        "📍｜定位器｜Locator",
        "📋｜完整清單｜Manifest",
        "🔗｜全域連結總帳｜GlobalLinkLedger",
        "🏷️｜命名連動器登記｜NamingRegistry",
        "📸｜快照｜Snapshot",
        "↩️｜反向鏈｜ReverseChain",
        "📖｜讀回｜ReadBack",
        "🔬｜驗證｜Verify"
      ]
    });
  });

  return Object.freeze({ status: "ACTIVE", identity: "🥃｜核心同步引擎｜CoreSyncEngine" });
}
