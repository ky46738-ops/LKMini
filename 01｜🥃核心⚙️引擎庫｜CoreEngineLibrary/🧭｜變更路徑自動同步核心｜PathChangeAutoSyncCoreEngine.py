#!/usr/bin/env python3
# 🧭｜變更路徑自動同步核心｜PathChangeAutoSyncCoreEngine
# 功能：同一 Identity 改名／搬移後，自動產生完整更新鏈與讀回驗收計畫。

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json

@dataclass(frozen=True)
class PathChange:
    identity: str
    old_path: str
    new_path: str
    timestamp: str

UPDATE_TARGETS = (
    "📍｜定位器｜Locator",
    "📋｜完整清單｜Manifest",
    "🔗｜全域連結總帳｜GlobalLinkLedger",
    "🥳｜歡迎光臨連結｜WelcomeGatewayLinks",
    "📘｜資料夾跳轉說明書｜FolderJumpManual",
    "🎛️｜主控跳轉區｜DashboardLinks",
    "🏷️｜命名連動器登記｜NamingRegistry",
    "📸｜快照｜Snapshot",
    "↩️｜反向鏈｜ReverseChain",
    "🧾｜同步回執｜SyncReceipt",
)

PIPELINE = (
    "🔍｜差異偵測器｜DifferenceDetector",
    "✍️｜回寫來源｜WriteBackToSource",
    "🧮｜公式重建｜FormulaRebuild",
    "🧩｜JSON核心重建｜JsonCoreRebuild",
    "🥃｜核心同步引擎｜CoreSyncEngine",
    "📡｜投影廣播｜ProjectionBroadcast",
    "📋｜完整清單更新｜ManifestUpdate",
    "📍｜定位器更新｜LocatorUpdate",
    "🔐｜SHA256更新｜SHA256Update",
    "📸｜快照更新｜SnapshotUpdate",
    "↩️｜反向鏈更新｜ReverseChainUpdate",
    "👀｜顯影更新｜VisualProjectionUpdate",
    "📖｜讀回｜ReadBack",
    "⚖️｜比對｜Compare",
    "🔬｜驗證｜Verify",
    "🧾｜同步回執｜SyncReceipt",
)

class PathChangeAutoSyncCoreEngine:
    def __init__(self, emit_event=None):
        self.emit_event = emit_event

    def build_event(self, identity: str, old_path: str, new_path: str) -> dict:
        if not identity or not old_path or not new_path:
            raise ValueError("Identity、舊路徑、新路徑不得為空")
        change = PathChange(
            identity=identity,
            old_path=old_path,
            new_path=new_path,
            timestamp=datetime.now().astimezone().isoformat(),
        )
        return {
            "event": "🔔｜路徑變更事件｜PathChanged",
            "change": asdict(change),
            "update_targets": list(UPDATE_TARGETS),
            "pipeline": list(PIPELINE),
            "completion_gate": "所有已登記引用 ReadBack + Compare + Verify 後才可 PASS",
            "A=A": True,
        }

    def dispatch(self, identity: str, old_path: str, new_path: str) -> dict:
        payload = self.build_event(identity, old_path, new_path)
        if self.emit_event is not None:
            self.emit_event("PathChanged", payload)
        return payload

    @staticmethod
    def write_receipt(payload: dict, output_path: str) -> str:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(p)
