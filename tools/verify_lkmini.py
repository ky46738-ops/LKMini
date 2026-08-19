#!/usr/bin/env python3
"""🔬公開種子驗證工具｜verify_lkmini

用途：
- 保護八個必要核心檔案。
- 保護已登記的開源模組，避免守門規則自傷誤刪。
- 只攔截真正的私人實例值與秘密，不封鎖公開技術概念。
- 驗證全部公開檔案均列入雜湊清單。

A_EQUALS_A=true
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(".").resolve()

REQUIRED_CORE_FILES = {
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "LKMini.svg",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/gatekeeper.yml",
    "tools/verify_lkmini.py",
}

REQUIRED_PUBLIC_MODULES = {
    "08｜自動化同步｜SyncAutomation/🍎Apple捷徑功能接線｜AppleShortcutFunctionWiring.md",
}

PUBLIC_MODULE_ROOTS = {
    "08｜自動化同步｜SyncAutomation",
}

CORE_DIRS = {
    ".github",
    ".github/workflows",
    "tools",
}

SAFE_PUBLIC_SUFFIXES = {
    ".md",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".svg",
    ".json",
    ".yaml",
    ".yml",
    ".sh",
    ".txt",
}

FORBIDDEN_BINARY_SUFFIXES = {
    ".zip",
    ".pdf",
    ".xlsx",
    ".xls",
    ".numbers",
    ".pages",
    ".key",
    ".webarchive",
    ".wacz",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".mp4",
    ".aicore",
}

MAX_PUBLIC_FILE_BYTES = 2_000_000

# 只偵測實際秘密與私人實例值；公開概念、格式名稱與網址協議不視為外洩。
PRIVATE_VALUE_PATTERNS = {
    "應用程式介面密鑰或權杖": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=：]\s*[\"']?[A-Za-z0-9_./+=-]{8,}"
    ),
    "常見秘密金鑰格式": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "私人檔案庫識別碼": re.compile(r"\bfile_[0-9a-f]{16,}\b"),
    "私人穩定檔案識別碼": re.compile(r"\blibfile_[0-9a-f]{16,}\b"),
    "私人追蹤欄位實際值": re.compile(
        r"(?i)\b(?:FileID|ObjectID|MessageID|ThreadID|RevisionID)\s*[:=：]\s*[A-Za-z0-9_-]{8,}"
    ),
    "私人雲端文件網址": re.compile(r"https://(?:drive|docs)\.google\.com/"),
}

POLICY_FILES = {
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "tools/verify_lkmini.py",
}


def iter_repo_files() -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for path in sorted(REPO_ROOT.rglob("*")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if path.is_file():
            result.append((rel, path))
    return result


def iter_repo_dirs() -> list[str]:
    result: list[str] = []
    for path in sorted(REPO_ROOT.rglob("*")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if path.is_dir():
            result.append(rel)
    return result


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_public_module_path(rel: str) -> bool:
    return any(rel == root or rel.startswith(root + "/") for root in PUBLIC_MODULE_ROOTS)


def check_required_files() -> bool:
    required = REQUIRED_CORE_FILES | REQUIRED_PUBLIC_MODULES
    missing = sorted(rel for rel in required if not Path(rel).is_file())
    if missing:
        print(f"失敗：缺少必要公開檔案：{missing}")
        return False
    print("通過：八個必要核心與已登記公開模組均存在")
    return True


def check_public_tree() -> bool:
    ok = True

    for rel in iter_repo_dirs():
        if rel in CORE_DIRS or is_public_module_path(rel):
            continue
        print(f"失敗：出現未登記公開資料夾：{rel}")
        ok = False

    for rel, path in iter_repo_files():
        is_core = rel in REQUIRED_CORE_FILES
        is_module = is_public_module_path(rel)
        if not is_core and not is_module:
            print(f"失敗：出現未登記公開檔案：{rel}")
            ok = False
            continue

        suffix = path.suffix.lower()
        if is_module and suffix not in SAFE_PUBLIC_SUFFIXES:
            print(f"失敗：公開模組使用未允許的原始碼格式：{rel}")
            ok = False
        if suffix in FORBIDDEN_BINARY_SUFFIXES:
            print(f"失敗：公開儲存庫不得直接放入二進位交付包：{rel}")
            ok = False
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            print(f"失敗：公開檔案超過大小限制：{rel}")
            ok = False

    if ok:
        print("通過：公開樹允許核心檔案與已登記開源模組")
    return ok


def check_a_equals_a() -> bool:
    content = Path("README.md").read_text(encoding="utf-8", errors="strict")
    if "A_EQUALS_A=true" not in content:
        print("失敗：公開說明書缺少 A=A 標記")
        return False
    print("通過：A=A 標記存在")
    return True


def check_restored_open_source_module() -> bool:
    rel = next(iter(REQUIRED_PUBLIC_MODULES))
    content = Path(rel).read_text(encoding="utf-8", errors="strict")
    required_phrases = {
        "🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring",
        "LKMINI://AppleShortcuts",
        "不得因出現通用技術詞而被整份刪除",
        "私人實例值不回填",
        "A=A",
    }
    missing = sorted(phrase for phrase in required_phrases if phrase not in content)
    if missing:
        print(f"失敗：復原開源模組缺少必要內容：{missing}")
        return False
    print("通過：蘋果捷徑公開接線已復原並具備防誤刪聲明")
    return True


def check_sha256sums() -> bool:
    manifest_path = Path("SHA256SUMS")
    if not manifest_path.is_file():
        print("失敗：缺少雜湊清單")
        return False

    ok = True
    observed: set[str] = set()
    for raw_line in manifest_path.read_text(encoding="utf-8", errors="strict").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            print(f"失敗：雜湊清單格式錯誤：{line}")
            ok = False
            continue
        expected, rel = parts
        observed.add(rel)
        path = Path(rel)
        if not path.is_file():
            print(f"失敗：雜湊目標不存在：{rel}")
            ok = False
            continue
        actual = sha256_file(path)
        if actual != expected:
            print(f"失敗：雜湊不一致：{rel}")
            ok = False
        else:
            print(f"通過：{rel}")

    expected_targets = {rel for rel, _ in iter_repo_files()} - {"SHA256SUMS"}
    if observed != expected_targets:
        print(
            "失敗：雜湊目標集合不一致："
            f"應有={sorted(expected_targets)}；實際={sorted(observed)}"
        )
        ok = False

    if ok:
        print("通過：所有公開檔案均已列入雜湊清單且內容一致")
    return ok


def check_no_private_values() -> bool:
    ok = True
    for rel, path in iter_repo_files():
        if rel in POLICY_FILES:
            continue
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PRIVATE_VALUE_PATTERNS.items():
            if pattern.search(content):
                print(f"失敗：{label} 出現在 {rel}")
                ok = False
    if ok:
        print("通過：未發現密鑰、私人識別碼或私人雲端座標")
    return ok


def main() -> int:
    results = [
        check_required_files(),
        check_public_tree(),
        check_a_equals_a(),
        check_restored_open_source_module(),
        check_no_private_values(),
        check_sha256sums(),
    ]
    if all(results):
        print("\nA=A：公開核心與開源模組均已保留並通過驗證。")
        return 0
    print("\n失敗：公開種子尚未通過驗證。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
