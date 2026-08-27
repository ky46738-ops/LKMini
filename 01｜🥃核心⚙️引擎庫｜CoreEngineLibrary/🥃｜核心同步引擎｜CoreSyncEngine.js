// 🥃｜核心同步引擎｜CoreSyncEngine
// Identity：LKMINI://
// 職責：把本機正式執行與遠端送達分開裁決，保存同步佇列事件。
// 邊界：外部端點真正 WRITE 由既有端點適配器執行；本核心不偽造遠端成功。

export const 系統執行狀態 = Object.freeze({
  PENDING: "PENDING",
  RUNNING: "RUNNING",
  COMMITTED: "COMMITTED",
  VERIFIED: "VERIFIED",
  FAIL: "FAIL"
});

export const 遠端送達狀態 = Object.freeze({
  NOT_REQUIRED: "NOT_REQUIRED",
  QUEUED: "QUEUED",
  PENDING_REMOTE_DELIVERY: "PENDING_REMOTE_DELIVERY",
  DELIVERED: "DELIVERED",
  READBACK_VERIFIED: "READBACK_VERIFIED",
  FAIL: "FAIL"
});

const SHA256_PATTERN = /^[a-f0-9]{64}$/i;

function 必填字串(value, name) {
  if (typeof value !== "string" || value.trim() === "") {
    throw new TypeError(`缺少或無效：${name}`);
  }
  return value.trim();
}

function 驗證SHA256(value) {
  const sha256 = 必填字串(value, "🔐｜SHA256｜SHA256");
  if (!SHA256_PATTERN.test(sha256)) {
    throw new TypeError("SHA256 必須為 64 字元十六進位字串");
  }
  return sha256.toLowerCase();
}

function 建立工作鍵({ identity, targetEndpoint, sha256 }) {
  return `${identity}::${targetEndpoint}::${sha256}`;
}

export function 建立核心同步引擎({
  監聽事件,
  發送同步事件,
  寫入同步佇列,
  記錄,
  現在 = () => new Date().toISOString()
} = {}) {
  if (typeof 監聽事件 !== "function") {
    throw new Error("缺少：📡｜事件監聽器｜EventListener");
  }

  const log = typeof 記錄 === "function" ? 記錄 : console.log;
  const queueWriter =
    typeof 寫入同步佇列 === "function"
      ? 寫入同步佇列
      : (job) => job;
  const jobs = new Map();

  const broadcast = (type, payload) => {
    log(`🔁｜同步事件｜${type}`, payload);
    if (typeof 發送同步事件 === "function") {
      發送同步事件(type, payload);
    }
  };

  const 建立同步工作 = ({
    identity,
    canonicalPath,
    sha256,
    locator,
    targetEndpoint,
    payloadReference = null,
    remoteRequired = true
  }) => {
    const normalized = {
      identity: 必填字串(identity, "🪪｜Identity｜Identity"),
      canonicalPath: 必填字串(canonicalPath, "📍｜正式路徑｜CanonicalPath"),
      sha256: 驗證SHA256(sha256),
      locator: 必填字串(locator, "📍｜定位器｜Locator"),
      targetEndpoint: remoteRequired
        ? 必填字串(targetEndpoint, "☁️｜目標端點｜TargetEndpoint")
        : targetEndpoint || "LOCAL_ONLY",
      payloadReference,
      attemptCount: 0,
      lastError: null,
      createdAt: 現在(),
      updatedAt: 現在(),
      systemExecution: 系統執行狀態.PENDING,
      remoteDelivery: remoteRequired
        ? 遠端送達狀態.QUEUED
        : 遠端送達狀態.NOT_REQUIRED
    };

    const key = 建立工作鍵(normalized);
    const existing = jobs.get(key);
    if (existing) {
      return Object.freeze({ ...existing, deduplicated: true });
    }

    const queued = Object.freeze({ ...normalized, jobKey: key });
    jobs.set(key, queued);
    queueWriter(queued);
    broadcast("🔁｜同步工作入列｜SyncJobQueued", queued);
    return queued;
  };

  const 更新工作 = (jobKey, patch, eventType) => {
    const existing = jobs.get(必填字串(jobKey, "🔑｜工作鍵｜JobKey"));
    if (!existing) {
      throw new Error(`找不到同步工作：${jobKey}`);
    }
    const next = Object.freeze({
      ...existing,
      ...patch,
      updatedAt: 現在()
    });
    jobs.set(jobKey, next);
    queueWriter(next);
    broadcast(eventType, next);
    return next;
  };

  const 標記本機執行中 = (jobKey) =>
    更新工作(
      jobKey,
      { systemExecution: 系統執行狀態.RUNNING },
      "⚙️｜本機執行中｜LocalExecutionRunning"
    );

  const 標記本機提交 = (jobKey) =>
    更新工作(
      jobKey,
      { systemExecution: 系統執行狀態.COMMITTED },
      "✍️｜本機提交完成｜LocalExecutionCommitted"
    );

  const 標記本機驗證完成 = (jobKey) =>
    更新工作(
      jobKey,
      { systemExecution: 系統執行狀態.VERIFIED },
      "🔬｜本機執行驗證完成｜LocalExecutionVerified"
    );

  const 標記遠端不可達 = (jobKey, error = "REMOTE_UNREACHABLE") => {
    const existing = jobs.get(jobKey);
    if (!existing) {
      throw new Error(`找不到同步工作：${jobKey}`);
    }
    return 更新工作(
      jobKey,
      {
        attemptCount: existing.attemptCount + 1,
        lastError: String(error),
        remoteDelivery: 遠端送達狀態.PENDING_REMOTE_DELIVERY
      },
      "⏳｜等待遠端送達｜PendingRemoteDelivery"
    );
  };

  const 標記遠端已送達 = (jobKey) =>
    更新工作(
      jobKey,
      { remoteDelivery: 遠端送達狀態.DELIVERED, lastError: null },
      "☁️｜遠端送達完成待讀回｜RemoteDeliveredAwaitingReadBack"
    );

  const 標記遠端讀回驗證 = (jobKey, syncReceipt) => {
    if (!syncReceipt || typeof syncReceipt !== "object") {
      throw new TypeError("遠端驗證必須提供 🧾｜同步回執｜SyncReceipt");
    }
    return 更新工作(
      jobKey,
      {
        remoteDelivery: 遠端送達狀態.READBACK_VERIFIED,
        syncReceipt,
        lastError: null
      },
      "🧾｜遠端讀回驗證完成｜RemoteReadBackVerified"
    );
  };

  const 標記失敗 = (jobKey, { scope, error }) => {
    const message = 必填字串(String(error || "UNKNOWN_ERROR"), "錯誤訊息");
    if (scope === "SYSTEM_EXECUTION") {
      return 更新工作(
        jobKey,
        {
          systemExecution: 系統執行狀態.FAIL,
          lastError: message
        },
        "❌｜系統執行失敗｜SystemExecutionFailed"
      );
    }
    if (scope === "REMOTE_DELIVERY") {
      return 更新工作(
        jobKey,
        {
          remoteDelivery: 遠端送達狀態.FAIL,
          lastError: message
        },
        "❌｜遠端送達失敗｜RemoteDeliveryFailed"
      );
    }
    throw new TypeError("scope 必須為 SYSTEM_EXECUTION 或 REMOTE_DELIVERY");
  };

  const 取得工作 = (jobKey) => jobs.get(jobKey) || null;
  const 列出工作 = () => [...jobs.values()];

  監聽事件("registry更新", (payload) =>
    broadcast("🏷️｜登記更新｜RegistryUpdated", payload)
  );
  監聽事件("manifest更新", (payload) =>
    broadcast("📋｜完整清單更新｜ManifestUpdated", payload)
  );
  監聽事件("零件更新", (payload) =>
    broadcast("🧩｜零件更新｜PartUpdated", payload)
  );

  監聽事件("PathChanged", (change) => {
    broadcast("📍｜路徑變更同步｜PathChangeSync", {
      ...change,
      required: [
        "📍｜定位器｜Locator",
        "📋｜完整清單｜Manifest",
        "🔐｜SHA256｜SHA256",
        "📸｜快照｜Snapshot",
        "↩️｜反向鏈｜ReverseChain",
        "👀｜顯影端｜VisualProjection",
        "📖｜讀回｜ReadBack",
        "⚖️｜比較｜Compare",
        "🔬｜驗證｜Verify",
        "🧾｜同步回執｜SyncReceipt"
      ]
    });
  });

  監聽事件("CanonicalChanged", (payload) => 建立同步工作(payload));
  監聽事件("RemoteUnavailable", ({ jobKey, error }) =>
    標記遠端不可達(jobKey, error)
  );
  監聽事件("RemoteDelivered", ({ jobKey }) =>
    標記遠端已送達(jobKey)
  );
  監聽事件("RemoteReadBackVerified", ({ jobKey, syncReceipt }) =>
    標記遠端讀回驗證(jobKey, syncReceipt)
  );

  return Object.freeze({
    status: "ACTIVE",
    identity: "🥃｜核心同步引擎｜CoreSyncEngine",
    rootProtocol: "LKMINI://",
    建立同步工作,
    標記本機執行中,
    標記本機提交,
    標記本機驗證完成,
    標記遠端不可達,
    標記遠端已送達,
    標記遠端讀回驗證,
    標記失敗,
    取得工作,
    列出工作
  });
}
