#!/usr/bin/env python3
# PhantomCapsuleMaker — public seed
# Scan → SHA dedup → identity group → one shell + one Control set
# Do not nest the previous zip into the next shell.

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

TPE = timezone(timedelta(hours=8))
MAGIC = "LKMINI-PHANTOM-CAPSULE/2"
CONTROL_NAMES = {
    "locator", "manifest", "sha256sums", "reversechain",
    "snapshot", "package", "sha256identity",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_name(path: Path) -> tuple[str, str]:
    name = path.name
    if "." in name:
        stem, ext = name.rsplit(".", 1)
        return stem, "." + ext.lower()
    return name, "[none]"


def is_control(stem: str) -> bool:
    key = stem.lower().replace(" ", "")
    return any(c in key for c in CONTROL_NAMES) or stem.startswith(
        ("📍", "📋", "🔐", "🔁", "📸", "📦可重建", "🚀")
    )


def scan(src: Path) -> list[dict]:
    items = []
    seen = set()
    for path in src.rglob("*"):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        digest = sha256_file(path)
        stem, ext = split_name(path)
        if ext == ".zip":
            items.append({
                "identity": stem, "ext": ext, "path": str(path),
                "bytes": path.stat().st_size, "sha256": digest, "role": "archive-ref",
            })
            continue
        if digest in seen:
            continue
        seen.add(digest)
        role = "control" if is_control(stem) else "projection"
        if ext == "[none]" and "幻影膠囊" in stem:
            role = "shell"
        items.append({
            "identity": stem, "ext": ext, "path": str(path),
            "bytes": path.stat().st_size, "sha256": digest, "role": role,
        })
    return items


def build_chain(items: list[dict], out_dir: Path, title: str) -> dict:
    now = datetime.now(TPE).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    identities = {}
    for it in items:
        identities.setdefault(it["identity"], []).append(it)
    projections = []
    for name, group in sorted(identities.items()):
        projections.append({
            "identity": name,
            "projections": [
                {"ext": g["ext"], "bytes": g["bytes"], "sha256": g["sha256"], "role": g["role"]}
                for g in group
            ],
        })
    locator = {
        "canonical": "LKMINI://capsule/maker",
        "formal_path": "LKMini / LKMINI / phantom-capsule",
        "built_at": now,
        "title": title,
    }
    reversechain = [title, "Projection", "phantom-capsule", "LKMINI", "A=A"]
    manifest = {
        "schema": "LKMINI.PhantomMaker.v1",
        "identity_count": len(identities),
        "file_count": len(items),
        "rule": "extension=projection; no-ext=shell; zip=reference only",
        "families": projections,
    }
    snapshot = {"built_at": now, "status": "maker", "identity_count": len(identities)}
    control = out_dir / "Control"
    control.mkdir(parents=True, exist_ok=True)
    (control / "LOCATOR.json").write_text(json.dumps(locator, ensure_ascii=False, indent=2), encoding="utf-8")
    (control / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (control / "REVERSECHAIN.json").write_text(json.dumps({"chain": reversechain}, ensure_ascii=False, indent=2), encoding="utf-8")
    (control / "SNAPSHOT.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    payload = {
        "identity": {
            "axiom": "A=A",
            "container": "phantom-capsule",
            "projection_is_not_identity": True,
            "protocol": "LKMINI://",
            "root": "LKMINI",
        },
        "locator": locator,
        "manifest": {
            "identity_count": len(identities),
            "file_count": len(items),
            "actions": ["search", "read", "activate", "mount", "verify", "update", "broadcast", "fusion", "snapshot", "sync", "reversible-loop"],
        },
        "reversechain": reversechain,
        "snapshot": snapshot,
        "families": projections,
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    payload_sha = sha256_bytes(body.encode("utf-8"))
    header = "\n".join([MAGIC, f"PAYLOAD-SHA256:{payload_sha}", "CONTENT-TYPE:application/vnd.lkmini.phantom+json", ""])
    shell = (header + body).encode("utf-8")
    root_sha = sha256_bytes(shell)
    (out_dir / "phantom-capsule").write_bytes(shell)
    (control / "SHA256Identity.json").write_text(json.dumps({"root_sha256": root_sha, "payload_sha256": payload_sha}, indent=2), encoding="utf-8")
    return {"bytes": len(shell), "root_sha256": root_sha, "identities": len(identities), "files": len(items)}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 public/PhantomCapsuleMaker.py <source-dir> [out-dir]")
        return 2
    src = Path(sys.argv[1]).expanduser().resolve()
    out = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else src / "maker-out"
    if not src.is_dir():
        print("source is not a folder:", src)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    print(json.dumps(build_chain(scan(src), out, src.name), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
