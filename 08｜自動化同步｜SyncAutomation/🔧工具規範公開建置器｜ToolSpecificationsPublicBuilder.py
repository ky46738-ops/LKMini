#!/usr/bin/env python3
"""🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder

建立可重現的公開原始碼封包。只讀取登記檔列出的公開文字檔，
不讀取私人雲端、郵件、裝置或帳號座標。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "🧾公開模組登記｜PublicModuleRegistry.json"
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_path(rel: str) -> Path:
    target = (ROOT / rel).resolve()
    root = ROOT.resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"路徑越界：{rel}")
    if not target.is_file():
        raise FileNotFoundError(rel)
    return target


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("🧭根協議") != "LKMINI://":
        raise ValueError("根協議不符")
    modules = data.get("🧩公開模組")
    if not isinstance(modules, list) or not modules:
        raise ValueError("公開模組登記為空")
    return data


def prepare_output_directory(out_dir: Path) -> Path:
    target = out_dir.resolve()
    root = ROOT.resolve()
    if target == root or target in root.parents:
        raise ValueError("輸出資料夾不可是儲存庫本身或其上層")
    if target.exists():
        if not target.is_dir():
            raise ValueError("輸出位置不是資料夾")
        if any(target.iterdir()):
            raise ValueError("輸出資料夾必須不存在或為空，避免破壞既有資料")
    else:
        target.mkdir(parents=True)
    return target


def build(out_dir: Path) -> dict:
    registry = load_registry()
    out_dir = prepare_output_directory(out_dir)

    selected = []
    for record in registry["🧩公開模組"]:
        rel = record["路徑"]
        path = safe_path(rel)
        selected.append({
            "名稱": record["名稱"],
            "網址": record["網址"],
            "路徑": rel,
            "位元組": path.stat().st_size,
            "雜湊": sha256(path),
        })

    manifest = {
        "📚格式": "LKMINI.ToolSpecificationsPublicBuild/1.0",
        "🧭根協議": "LKMINI://",
        "🪞顯影不等於本體": True,
        "📦成員": selected,
        "♻️回推": ["公開建置封包", "🧾公開模組登記", "🧩LKMINI", "LKMINI://", "A=A"],
    }
    manifest_path = out_dir / "📜公開建置清單｜PublicBuildManifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    zip_path = out_dir / "📦工具規範公開建置｜ToolSpecificationsPublicBuild.zip"
    members = [(REGISTRY, REGISTRY.relative_to(ROOT).as_posix()), (manifest_path, manifest_path.name)]
    members += [(safe_path(item["路徑"]), item["路徑"]) for item in selected]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        seen = set()
        for path, arcname in sorted(members, key=lambda x: x[1]):
            if arcname in seen:
                raise ValueError(f"重複封包成員：{arcname}")
            seen.add(arcname)
            info = zipfile.ZipInfo(arcname, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes())

    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"壓縮檔循環冗餘檢查失敗：{bad}")
        duplicate_count = len(zf.namelist()) - len(set(zf.namelist()))
        if duplicate_count:
            raise RuntimeError("壓縮檔含重複成員")

    with zipfile.ZipFile(zip_path) as zf:
        member_count = len(zf.namelist())

    result = {
        "狀態": "通過（PASS）",
        "封包": zip_path.name,
        "位元組": zip_path.stat().st_size,
        "雜湊": sha256(zip_path),
        "成員數": member_count,
        "重複成員數": 0,
        "循環冗餘檢查": "通過（PASS）",
    }
    (out_dir / "🔬公開建置驗收｜PublicBuildAcceptance.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="🔧工具規範公開建置器")
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.out_dir.resolve()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
