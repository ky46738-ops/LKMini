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
    ".github/workflows/gatekeeper.yml",
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

def check_no_private_leak():
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fname in files:
            if fname.endswith((".md", ".json", ".txt")):
                fpath = os.path.join(root, fname)
                with open(fpath, "r", errors="ignore") as f:
                    content = f.read()
                for marker in PRIVATE_MARKERS:
                    if marker in content:
                        print(f"FAIL: Private marker '{marker}' in {fpath}")
                        return False
    print("PASS: No private data leaked")
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
