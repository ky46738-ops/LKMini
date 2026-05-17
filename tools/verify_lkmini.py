#!/usr/bin/env python3
"""
LKMini 本地驗證器
用途：就算 GitHub Actions 掛掉，本地也能驗證
"""

import os
import hashlib
import sys

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "MANIFEST.json",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/gatekeeper.yml",
]

PRIVATE_MARKERS = ["PRIVATE_ENGINE", "ENGINE_REGISTRY_PRIVATE"]

def check_files():
    print("[1] 檢查必要檔案...")
    all_ok = True
    for f in REQUIRED_FILES:
        if os.path.exists(f):
            print(f"  PASS: {f}")
        else:
            print(f"  FAIL: 缺少 {f}")
            all_ok = False
    return all_ok

def check_a_equals_a():
    print("[2] 檢查 A=A 標記...")
    with open("README.md", "r") as f:
        content = f.read()
    if "A_EQUALS_A=true" in content:
        print("  PASS: A=A 標記存在")
        return True
    else:
        print("  FAIL: README.md 缺少 A_EQUALS_A=true")
        return False

def check_private_leakage():
    print("[3] 檢查私有資料外洩...")
    all_ok = True
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d != ".git"]
        for filename in files:
            if filename.endswith((".md", ".json", ".txt")):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", errors="ignore") as f:
                    content = f.read()
                for marker in PRIVATE_MARKERS:
                    if marker in content:
                        print(f"  FAIL: 私有標記 '{marker}' 出現在 {filepath}")
                        all_ok = False
    if all_ok:
        print("  PASS: 無私有資料外洩")
    return all_ok

def check_sha256():
    print("[4] 檢查 SHA256SUMS...")
    if not os.path.exists("SHA256SUMS"):
        print("  FAIL: SHA256SUMS 不存在")
        return False
    with open("SHA256SUMS", "r") as f:
        content = f.read()
    if "SHA256SUMS_STATUS=PLACEHOLDER" in content:
        print("  WARNING: SHA256SUMS 仍是 placeholder，跳過驗證")
        return True
    # 真正驗證
    all_ok = True
    for line in content.strip().split("\n"):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) != 2:
            continue
        expected_hash, filepath = parts
        filepath = filepath.lstrip("./")
        if not os.path.exists(filepath):
            print(f"  FAIL: 檔案不存在 {filepath}")
            all_ok = False
            continue
        with open(filepath, "rb") as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()
        if actual_hash == expected_hash:
            print(f"  PASS: {filepath}")
        else:
            print(f"  FAIL: hash 不符 {filepath}")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    print("=== LKMini 驗證器 seed_v0 ===")
    results = [
        check_files(),
        check_a_equals_a(),
        check_private_leakage(),
        check_sha256(),
    ]
    print("")
    if all(results):
        print("✅ 全部通過 A_EQUALS_A=true")
        sys.exit(0)
    else:
        print("❌ 有項目未通過")
        sys.exit(1)
