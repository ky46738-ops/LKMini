#!/usr/bin/env python3
"""
verify_lkmini.py — LKMini seed_v0 integrity verifier
Author: ky46738-ops
A_EQUALS_A=true
"""
import hashlib
import sys
import os
import re
import subprocess

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "LKMini.svg",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/大管家.yml",
    "tools/verify_lkmini.py",
]

PRIVATE_MARKERS = ["PRIVATE_ENGINE", "ENGINE_REGISTRY_PRIVATE"]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def check_required_files():
    expected = set(REQUIRED_FILES)
    tracked = set(subprocess.check_output(["git", "ls-files", "-z"]).decode("utf-8").rstrip("\0").split("\0"))
    missing = sorted(expected - tracked)
    extra = sorted(tracked - expected)
    invalid = sorted(p for p in expected if not os.path.isfile(p) or os.path.islink(p))
    if missing or extra or invalid:
        print(f"FAIL: missing={missing}; extra={extra}; invalid={invalid}")
        return False
    print("PASS: Exactly eight tracked public files")
    return True

def check_a_equals_a():
    with open("README.md", "r") as f:
        if "A_EQUALS_A=true" not in f.read():
            print("FAIL: A=A marker missing")
            return False
    print("PASS: A=A marker found")
    return True

def check_sha256sums():
    expected_paths = set(REQUIRED_FILES) - {"SHA256SUMS"}
    seen = set()
    ok = True
    with open("SHA256SUMS", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\r\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                print("FAIL: Invalid SHA256 record")
                ok = False
                continue
            expected, path = parts
            if (not re.fullmatch(r"[0-9a-f]{64}", expected) or
                    path not in expected_paths or path in seen):
                print(f"FAIL: Invalid or duplicate SHA256 path: {path}")
                ok = False
                continue
            seen.add(path)
            if not os.path.isfile(path) or os.path.islink(path) or sha256_file(path) != expected:
                print(f"FAIL: {path} hash mismatch or invalid file")
                ok = False
            else:
                print(f"OK: {path}")
    if seen != expected_paths:
        print("FAIL: SHA256 coverage incomplete")
        ok = False
    if ok:
        print("PASS: All seven content hashes match")
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
