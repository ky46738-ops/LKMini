#!/usr/bin/env python3
"""
verify_lkmini.py — LKMini seed_v0 public Mirror gate
Author: ky46738-ops
A_EQUALS_A=true

公開 Mirror 規則：
- 只允許 8 個公開最小種子檔。
- 不接收膠囊、正式任務鏈、內部定位器、Manifest、ReverseChain、Snapshot、Package、回執、私有引擎。
- 不接收 Drive/FileID/MessageID/ObjectID/捷徑 URL Scheme 等私域接線資料。
- Gate 只保護公開邊界；私有本體留在正式私有容器。
"""
from pathlib import Path
import hashlib
import sys

REPO_ROOT = Path(".").resolve()

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "LKMini.svg",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/gatekeeper.yml",
    "tools/verify_lkmini.py",
]

ALLOWED_FILES = set(REQUIRED_FILES)

ALLOWED_DIRS = {
    ".github",
    ".github/workflows",
    "tools",
}

PRIVATE_MARKERS = [
    "PRIVATE_ENGINE",
    "ENGINE_REGISTRY_PRIVATE",
    "RootMetadataSHA256",
    "metadata_sha256",
    "🪞幻影膠囊",
    "幻影膠囊",
    "膠囊",
    "Current",
    "Locator",
    "LOCATOR",
    "定位器",
    "Manifest",
    "MANIFEST",
    "清單",
    "ReverseChain",
    "REVERSECHAIN",
    "回推鏈",
    "Snapshot",
    "SNAPSHOT",
    "快照",
    "Package",
    "PACKAGE",
    "AICORE",
    "Google Drive",
    "GoogleDrive",
    "Drive FileID",
    "drive.google.com",
    "docs.google.com",
    "Library StableID",
    "Library ZIP",
    "Library HTML",
    "library_file_id",
    "libfile_",
    "FileID",
    "ObjectID",
    "MessageID",
    "ThreadID",
    "Revision",
    "shortcuts://",
    "obsidian://",
    "Apple Shortcuts",
    "URL Scheme",
    "file_00000000",
    "正式任務鏈",
    "任務筆記本",
    "回執",
    "接線回執",
    "execution_output",
    "萬用呼叫器",
    "融合引擎",
    "私人引擎",
]

FORBIDDEN_PATH_PARTS = [
    "LKMINI/",
    "evidence/",
    "🪞幻影膠囊",
    "幻影膠囊",
    "膠囊",
    "Current",
    "Locator",
    "LOCATOR",
    "Manifest",
    "MANIFEST",
    "ReverseChain",
    "REVERSECHAIN",
    "Snapshot",
    "SNAPSHOT",
    "Package",
    "PACKAGE",
    "AICORE",
    "receipt",
    "Receipt",
    "回執",
]

FORBIDDEN_EXTENSIONS = {
    ".zip",
    ".pdf",
    ".xlsx",
    ".xls",
    ".numbers",
    ".pages",
    ".key",
    ".html",
    ".webarchive",
    ".wacz",
    ".json",
    ".csv",
    ".tsv",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".mp4",
    ".aicore",
}

MAX_PUBLIC_FILE_BYTES = 500_000

# 政策與驗證檔必須描述禁用標記；這些位置只允許明確列出的字串。
ALLOWED_PRIVATE_MARKERS_BY_FILE = {
    "README.md": {"私人引擎"},
    "PUBLIC_PRIVATE_BOUNDARY.md": set(PRIVATE_MARKERS),
    ".github/workflows/gatekeeper.yml": {"PRIVATE_ENGINE", "ENGINE_REGISTRY_PRIVATE"},
    "tools/verify_lkmini.py": set(PRIVATE_MARKERS),
}


def iter_repo_files():
    for path in sorted(REPO_ROOT.rglob("*")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if path.is_file():
            yield rel, path


def iter_repo_dirs():
    for path in sorted(REPO_ROOT.rglob("*")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if path.is_dir():
            yield rel


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_required_files():
    missing = [f for f in REQUIRED_FILES if not Path(f).exists()]
    if missing:
        print(f"FAIL: Missing files: {missing}")
        return False
    print("PASS: All required public Mirror files exist")
    return True


def check_public_mirror_whitelist():
    ok = True

    for rel in iter_repo_dirs():
        if rel not in ALLOWED_DIRS:
            print(f"FAIL: Public Mirror contains extra directory: {rel}")
            ok = False

    for rel, path in iter_repo_files():
        if rel not in ALLOWED_FILES:
            print(f"FAIL: Public Mirror contains extra file: {rel}")
            ok = False
        if any(part in rel for part in FORBIDDEN_PATH_PARTS):
            print(f"FAIL: Forbidden private path marker in: {rel}")
            ok = False
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS and rel not in ALLOWED_FILES:
            print(f"FAIL: Forbidden extension in public Mirror: {rel}")
            ok = False
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            print(f"FAIL: Public Mirror file too large: {rel}")
            ok = False

    if ok:
        print("PASS: Public Mirror whitelist locked")
    return ok


def check_a_equals_a():
    content = Path("README.md").read_text(encoding="utf-8", errors="ignore")
    if "A_EQUALS_A=true" not in content:
        print("FAIL: A=A marker missing")
        return False
    print("PASS: A=A marker found")
    return True


def check_sha256sums():
    if not Path("SHA256SUMS").exists():
        print("FAIL: SHA256SUMS missing")
        return False

    ok = True
    seen = set()
    for line in Path("SHA256SUMS").read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            print(f"FAIL: Bad SHA256SUMS line: {line}")
            ok = False
            continue
        expected, rel = parts
        seen.add(rel)
        if rel not in ALLOWED_FILES or rel == "SHA256SUMS":
            print(f"FAIL: SHA256SUMS contains non-public target: {rel}")
            ok = False
            continue
        path = Path(rel)
        if not path.exists():
            print(f"FAIL: {rel} not found")
            ok = False
            continue
        actual = sha256_file(path)
        if actual != expected:
            print(f"FAIL: {rel} hash mismatch")
            ok = False
        else:
            print(f"OK: {rel}")

    expected_hashed = ALLOWED_FILES - {"SHA256SUMS"}
    if seen != expected_hashed:
        print(f"FAIL: SHA256SUMS target set mismatch: expected={sorted(expected_hashed)} observed={sorted(seen)}")
        ok = False

    if ok:
        print("PASS: All public hashes match")
    return ok


def check_no_private_leak():
    ok = True
    for rel, path in iter_repo_files():
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        allowed_markers = ALLOWED_PRIVATE_MARKERS_BY_FILE.get(rel, set())
        for marker in PRIVATE_MARKERS:
            if marker in content and marker not in allowed_markers:
                print(f"FAIL: Private marker '{marker}' in {rel}")
                ok = False
    if ok:
        print("PASS: No private markers found")
    return ok


if __name__ == "__main__":
    results = [
        check_required_files(),
        check_public_mirror_whitelist(),
        check_a_equals_a(),
        check_sha256sums(),
        check_no_private_leak(),
    ]
    if all(results):
        print("\nA=A — Public Mirror gate locked.")
        sys.exit(0)
    print("\nFAIL — Public Mirror gate is NOT locked.")
    sys.exit(1)
