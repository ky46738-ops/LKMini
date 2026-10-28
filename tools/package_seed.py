#!/usr/bin/env python3
"""
LKMini 封裝腳本
輸出：LKMini_seed_v0.zip
"""

import zipfile
import os
import datetime

SEED_FILES = [
    "📖入口宣告｜README.md",
    "⚖️授權條款｜LICENSE",
    "✍️作者歸屬｜NOTICE.md",
    "MANIFEST.json",
    "LOCATOR.json",
    "SNAPSHOT.json",
    "ReverseChain.json",
    "RESTORE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "VERSION.md",
    "🚧公私邊界｜PUBLIC_PRIVATE_BOUNDARY.md",
    "🥃永恆核心政策｜ETERNAL_CORE_POLICY.md",
    "GOVERNANCE.md",
    "THREAT_MODEL.md",
    "CITATION.cff",
    "🧾雜湊校驗清單｜SHA256SUMS",
    ".github/CODEOWNERS",
    ".github/workflows/🎩大管家｜Gatekeeper.yml",
    "tools/🔍驗證工具｜verify_lkmini.py",
    "tools/package_seed.py",
]

OUTPUT = "LKMini_seed_v0.zip"

if __name__ == "__main__":
    print(f"封裝 LKMini seed_v0 -> {OUTPUT}")
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in SEED_FILES:
            if os.path.exists(f):
                zf.write(f)
                print(f"  加入: {f}")
            else:
                print(f"  跳過（不存在）: {f}")
    print(f"\n✅ 完成: {OUTPUT}")
    print("A_EQUALS_A=true")
