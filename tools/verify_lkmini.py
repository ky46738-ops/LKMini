#!/usr/bin/env python3
"""
verify_lkmini.py — LKMini seed_v0 integrity verifier
Author: ky46738-ops
A_EQUALS_A=true
"""
import hashlib
import sys
import os

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "LKMini.svg",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/🎩大管家.yml",
    "tools/verify_lkmini.py",
]

PRIVATE_MARKERS = ["PRIVATE_ENGINE", "ENGINE_REGISTRY_PRIVATE"]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def check_required_files():
    missing = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    if missing:
        print(f"FAIL: Missing files: {missing}")
        return False
    print("PASS: All required files exist")
    return True

def check_a_equals_a():
    with open("README.md", "r") as f:
        if "A_EQUALS_A=true" not in f.read():
            print("FAIL: A=A marker missing")
            return False
    print("PASS: A=A marker found")
    return True

def check_sha256sums():
    if not os.path.exists("SHA256SUMS"):
        print("FAIL: SHA256SUMS missing")
        return False
    ok = True
    with open("SHA256SUMS", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                continue
            expected, path = parts
            if not os.path.exists(path):
                print(f"FAIL: {path} not found")
                ok = False
                continue
            actual = sha256_file(path)
            if actual != expected:
                print(f"FAIL: {path} hash mismatch")
                ok = False
            else:
                print(f"OK: {path}")
    if ok:
        print("PASS: All hashes match")
    return ok

# 這些是公開安全政策中對禁止詞的「文字說明」，不是引擎資料本體。
# 僅放行完全相同的原句；其餘包含私有標記的內容仍拒絕。
DOCUMENTED_MARKER_LINES = {
    "PUBLIC_PRIVATE_BOUNDARY.md": {
        "- PRIVATE_ENGINE_FLEET",
        "- ENGINE_REGISTRY_PRIVATE",
    },
    "GOVERNANCE.md": {
        "- 私有引擎設定（PRIVATE_ENGINE_FLEET 內容）",
    },
    "SECURITY.md": {
        "- `PRIVATE_ENGINE`",
        "- `ENGINE_REGISTRY_PRIVATE`",
    },
}

def check_no_private_leak():
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fname in files:
            if fname.endswith((".md", ".json", ".txt")):
                fpath = os.path.join(root, fname)
                relpath = os.path.relpath(fpath, ".").replace(os.sep, "/")
                with open(fpath, "r", errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        if any(marker in line for marker in PRIVATE_MARKERS):
                            if line.strip() in DOCUMENTED_MARKER_LINES.get(relpath, set()):
                                continue
                            print(f"FAIL: Private marker in {relpath}:{lineno}")
                            return False
    print("PASS: No undocumented private markers found")
    return True

if __name__ == "__main__":
    results = [
        check_required_files(),
        check_a_equals_a(),
        check_sha256sums(),
        check_no_private_leak(),
    ]
    if all(results):
        print("\n✅ A=A — All checks passed. Gate is locked.")
        sys.exit(0)
    else:
        print("\n❌ FAIL — Gate is NOT locked.")
        sys.exit(1)
