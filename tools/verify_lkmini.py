#!/usr/bin/env python3
"""🔬公開種子驗證工具｜verify_lkmini

用途：
- 保護九個必要核心檔案。
- 以固定集合＋公開模組登記雙重保護公開模組。
- 防止只刪登記或只刪檔案後仍誤判通過。
- 只攔截真正的私人實例值與秘密，不封鎖公開技術概念。
- 驗證命名、網址、結構、雜湊、標準授權與可逆證據。

A_EQUALS_A=true
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(".").resolve()
REGISTRY_PATH = "🧾公開模組登記｜PublicModuleRegistry.json"
ROOT_PROTOCOL = "LKMINI://"
ROOT_SHA256 = "6c0f6f487d8af27de4a8cee9f3fc853f0fbcf417cbd21acb56ac65c55adfcf34"

REQUIRED_CORE_FILES = {
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "LKMini.svg",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/gatekeeper.yml",
    "tools/verify_lkmini.py",
    REGISTRY_PATH,
}

# 這份固定集合故意與登記檔分開保存：
# 若有人同時從登記檔與儲存庫刪除公開模組，驗證仍會失敗。
PROTECTED_PUBLIC_MODULES = {
    "07｜公開顯影｜PublicProjection/🔧工具規範｜ToolSpecifications.html",
    "07｜公開顯影｜PublicProjection/🎨介面研究互動範例｜UIResearchInteractiveExamples.html",
    "07｜公開顯影｜PublicProjection/🖥️動作容器互動範例｜ActionContainerInteractiveExample.html",
    "07｜公開顯影｜PublicProjection/🎴本體顯影關係圖｜IdentityProjectionDiagram.svg",
    "08｜自動化同步｜SyncAutomation/🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring.md",
    "08｜自動化同步｜SyncAutomation/🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder.py",
    ".github/workflows/🔧工具規範公開建置流程｜ToolSpecificationsPublicBuildWorkflow.yml",
    "09｜公開協議｜PublicProtocol/🌱唯一真相源｜MarkdownSeed.md",
    "09｜公開協議｜PublicProtocol/🧭動作鏈｜S0-S10.md",
    "09｜公開協議｜PublicProtocol/📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual.md",
    "09｜公開協議｜PublicProtocol/♾️公開回推鏈｜PublicReverseChain.json",
    "09｜公開協議｜PublicProtocol/🧭公開定位器｜PublicLocator.json",
    "09｜公開協議｜PublicProtocol/🧾開源刪除鑑識清冊｜OpenSourceDeletionForensics.json",
}

PUBLIC_MODULE_ROOTS = {
    "07｜公開顯影｜PublicProjection",
    "08｜自動化同步｜SyncAutomation",
    "09｜公開協議｜PublicProtocol",
}

MODULE_CONTENT_REQUIREMENTS = {
    "07｜公開顯影｜PublicProjection/🔧工具規範｜ToolSpecifications.html": {
        "🔧工具規範｜ToolSpecifications",
        "LKMINI://Specification/ToolSpecifications",
        "公開用途與結構復原",
        "私人雲端座標、私人識別碼與舊時效狀態不回填",
        "A=A",
    },
    "07｜公開顯影｜PublicProjection/🎨介面研究互動範例｜UIResearchInteractiveExamples.html": {
        "🎨介面研究互動範例｜UIResearchInteractiveExamples",
        "LKMINI://介面研究/操作",
        "這是從被刪歷史公開頁抽回並重新整理的安全開源版本",
        "尚未操作",
        "A=A",
    },
    "07｜公開顯影｜PublicProjection/🖥️動作容器互動範例｜ActionContainerInteractiveExample.html": {
        "🖥️動作容器互動範例｜ActionContainerInteractiveExample",
        "LKMINI://動作容器/操作",
        "S0",
        "S10",
        "A=A",
    },
    "07｜公開顯影｜PublicProjection/🎴本體顯影關係圖｜IdentityProjectionDiagram.svg": {
        "🎴本體顯影關係圖｜IdentityProjectionDiagram",
        "🧩LKMINI",
        "🪞顯影不等於🪪本體",
        "A=A",
    },
    "08｜自動化同步｜SyncAutomation/🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring.md": {
        "🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring",
        "LKMINI://AppleShortcuts",
        "不得因出現通用技術詞而被整份刪除",
        "私人實例值不回填",
        "A=A",
    },
    "08｜自動化同步｜SyncAutomation/🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder.py": {
        "🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder",
        "🧾公開模組登記｜PublicModuleRegistry.json",
        "FIXED_ZIP_TIME",
        "重複封包成員",
        "循環冗餘檢查",
        "A=A",
    },
    ".github/workflows/🔧工具規範公開建置流程｜ToolSpecificationsPublicBuildWorkflow.yml": {
        "🔧工具規範公開建置",
        "🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder.py",
        "actions/upload-artifact@v4",
        "工具規範公開建置",
    },
    "09｜公開協議｜PublicProtocol/🌱唯一真相源｜MarkdownSeed.md": {
        "🌱唯一真相源｜MarkdownSeed",
        "LKMINI://",
        "🪞顯影（Projection）不等於 🪪本體身分（Identity）",
        "S0 搜尋去重",
        "A=A",
    },
    "09｜公開協議｜PublicProtocol/🧭動作鏈｜S0-S10.md": {
        "🧭動作鏈｜S0-S10",
        "S0｜🔍搜尋與去重",
        "S10｜🚫禁令查核",
        "🐙章魚貓（GitHub）",
        "A=A",
    },
    "09｜公開協議｜PublicProtocol/📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual.md": {
        "📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual",
        "🍎蘋果格式",
        "有損轉換不得宣稱位元可逆",
        "♻️固定回推",
        "A=A",
    },
    "09｜公開協議｜PublicProtocol/♾️公開回推鏈｜PublicReverseChain.json": {
        "LKMINI.PublicReverseChain/1.0",
        "🗑️未裁決永久刪除數",
        "LKMINI://",
        "A=A",
    },
    "09｜公開協議｜PublicProtocol/🧭公開定位器｜PublicLocator.json": {
        "LKMINI.PublicLocator/2.0",
        "只保存公開儲存庫相對路徑",
        "🧾公開模組登記",
        "A=A",
    },
    "09｜公開協議｜PublicProtocol/🧾開源刪除鑑識清冊｜OpenSourceDeletionForensics.json": {
        "32e6a02d75b3fc82ffbfdba3b54922c33f8f774b",
        "eb426724521a8b0abcc2dac5652003500e65a8f9",
        "公開技術與程式要復原",
        "私人實例值不回填",
        "A=A",
    },
}

SAFE_PUBLIC_SUFFIXES = {
    ".md", ".py", ".js", ".ts", ".html", ".css", ".svg",
    ".json", ".yaml", ".yml", ".sh", ".txt",
}
FORBIDDEN_BINARY_SUFFIXES = {
    ".zip", ".pdf", ".xlsx", ".xls", ".numbers", ".pages", ".key",
    ".webarchive", ".wacz", ".png", ".jpg", ".jpeg", ".webp",
    ".gif", ".mp4", ".aicore",
}
MAX_PUBLIC_FILE_BYTES = 2_000_000

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
    "私人黑曜石資料庫座標": re.compile(r"obsidian://open\?vault=[^\s\"'<>]+"),
    "私人電子郵件地址": re.compile(r"(?i)\b[A-Z0-9._%+-]+@(?:gmail|googlemail)\.com\b"),
}

# 政策與驗證器會列出偵測規則本身，所以不掃描其規則文字。
PRIVATE_SCAN_EXEMPT = {
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "tools/verify_lkmini.py",
}

MIT_LICENSE_REQUIRED_PHRASES = {
    "MIT License",
    "Copyright (c) 2026 ky46738-ops",
    "Permission is hereby granted, free of charge",
    "THE SOFTWARE IS PROVIDED \"AS IS\"",
}

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
URI_RE = re.compile(r"^LKMINI://[^/?#]+/[^/?#]+$")


class MinimalHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_count = 0
        self.title_count = 0
        self.viewport_count = 0
        self.external_script_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "html":
            self.html_count += 1
            if attrs_dict.get("lang") != "zh-Hant":
                raise ValueError("網頁缺少繁體中文語言標記")
        elif tag == "title":
            self.title_count += 1
        elif tag == "meta" and attrs_dict.get("name") == "viewport":
            self.viewport_count += 1
        elif tag == "script" and attrs_dict.get("src"):
            self.external_script_count += 1


def repo_path(rel: str) -> Path:
    target = (REPO_ROOT / rel).resolve()
    if target != REPO_ROOT and REPO_ROOT not in target.parents:
        raise ValueError(f"路徑越界：{rel}")
    return target


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


def load_registry() -> dict:
    try:
        data = json.loads(repo_path(REGISTRY_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"公開模組登記讀取失敗：{exc}") from exc
    return data


def check_registry() -> bool:
    try:
        data = load_registry()
        if data.get("🧭根協議") != ROOT_PROTOCOL:
            raise ValueError("根協議不符")
        if data.get("🔐根錨點雜湊") != ROOT_SHA256:
            raise ValueError("根錨點雜湊不符")
        if data.get("🏷️命名規則") != "Emoji＋中文主名稱｜EnglishKey":
            raise ValueError("命名規則不符")
        if data.get("🪞顯影不等於本體") is not True:
            raise ValueError("顯影與本體裁決不符")
        if data.get("⚖️公理") != "A=A":
            raise ValueError("A=A 公理缺失")
        if set(data.get("📚必要核心", [])) != REQUIRED_CORE_FILES:
            raise ValueError("必要核心集合與固定保護集合不一致")
        if set(data.get("📂公開模組根", [])) != PUBLIC_MODULE_ROOTS:
            raise ValueError("公開模組根集合不一致")

        records = data.get("🧩公開模組")
        if not isinstance(records, list):
            raise ValueError("公開模組不是清單")
        paths = [record.get("路徑") for record in records]
        names = [record.get("名稱") for record in records]
        uris = [record.get("網址") for record in records]
        if any(not isinstance(value, str) or not value for value in paths + names + uris):
            raise ValueError("公開模組登記含空欄位")
        if len(paths) != len(set(paths)) or len(names) != len(set(names)) or len(uris) != len(set(uris)):
            raise ValueError("公開模組登記含重複路徑、名稱或網址")
        if set(paths) != PROTECTED_PUBLIC_MODULES:
            missing = sorted(PROTECTED_PUBLIC_MODULES - set(paths))
            extra = sorted(set(paths) - PROTECTED_PUBLIC_MODULES)
            raise ValueError(f"登記與固定防誤刪集合不一致；缺少={missing}；多出={extra}")

        for record in records:
            rel = record["路徑"]
            name = record["名稱"]
            uri = record["網址"]
            if record.get("狀態") != "啟用（ACTIVE）":
                raise ValueError(f"公開模組不是啟用狀態：{rel}")
            pure = PurePosixPath(rel)
            if pure.is_absolute() or ".." in pure.parts:
                raise ValueError(f"公開模組路徑不安全：{rel}")
            path = repo_path(rel)
            if not path.is_file():
                raise ValueError(f"公開模組不存在：{rel}")
            stem = path.stem
            if name != stem:
                raise ValueError(f"名稱與檔名不一致：{name} != {stem}")
            if "｜" not in stem:
                raise ValueError(f"公開模組檔名缺少中文／英文分隔：{rel}")
            chinese_part = stem.split("｜", 1)[0]
            if not CJK_RE.search(chinese_part):
                raise ValueError(f"公開模組檔名不是中文優先：{rel}")
            if stem[0].isascii() and stem[0].isalnum():
                raise ValueError(f"公開模組檔名缺少前置 Emoji：{rel}")
            if not URI_RE.fullmatch(uri):
                raise ValueError(f"外顯網址不符合 LKMINI://物件名稱/動作：{uri}")
            parts = urlsplit(uri)
            if parts.scheme.lower() != "lkmini" or parts.query or parts.fragment:
                raise ValueError(f"外顯網址解析失敗：{uri}")
            if not unquote(parts.netloc).strip() or len([x for x in parts.path.split("/") if x]) != 1:
                raise ValueError(f"外顯網址缺少物件或單一動作：{uri}")

        guards = data.get("🚫刪除保護", {})
        if not guards or not all(value is True for value in guards.values()):
            raise ValueError("刪除保護規則未全部啟用")
    except Exception as exc:
        print(f"失敗：公開模組登記驗證：{exc}")
        return False
    print(f"通過：公開模組登記、固定防誤刪集合與網址文法一致（{len(PROTECTED_PUBLIC_MODULES)} 個模組）")
    return True


def check_required_files() -> bool:
    required = REQUIRED_CORE_FILES | PROTECTED_PUBLIC_MODULES
    missing = sorted(rel for rel in required if not repo_path(rel).is_file())
    if missing:
        print(f"失敗：缺少必要公開檔案：{missing}")
        return False
    print(f"通過：九個必要核心與 {len(PROTECTED_PUBLIC_MODULES)} 個固定公開模組均存在")
    return True


def check_public_tree() -> bool:
    allowed_files = REQUIRED_CORE_FILES | PROTECTED_PUBLIC_MODULES
    allowed_dirs: set[str] = set()
    for rel in allowed_files:
        parent = PurePosixPath(rel).parent
        while str(parent) not in {"", "."}:
            allowed_dirs.add(parent.as_posix())
            parent = parent.parent

    ok = True
    for rel in iter_repo_dirs():
        if rel not in allowed_dirs:
            print(f"失敗：出現未登記公開資料夾：{rel}")
            ok = False
    for rel, path in iter_repo_files():
        if rel not in allowed_files:
            print(f"失敗：出現未登記公開檔案：{rel}")
            ok = False
            continue
        suffix = path.suffix.lower()
        if rel in PROTECTED_PUBLIC_MODULES and suffix not in SAFE_PUBLIC_SUFFIXES:
            print(f"失敗：公開模組使用未允許的原始碼格式：{rel}")
            ok = False
        if suffix in FORBIDDEN_BINARY_SUFFIXES:
            print(f"失敗：公開儲存庫不得直接放入未裁決二進位交付包：{rel}")
            ok = False
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            print(f"失敗：公開檔案超過大小限制：{rel}")
            ok = False
    if ok:
        print("通過：公開樹只包含必要核心與已登記公開模組")
    return ok


def check_mit_license() -> bool:
    content = repo_path("LICENSE").read_text(encoding="utf-8", errors="strict")
    missing = sorted(phrase for phrase in MIT_LICENSE_REQUIRED_PHRASES if phrase not in content)
    if missing:
        print(f"失敗：正式麻省理工開源授權原文缺失：{missing}")
        return False
    if not content.startswith("MIT License\n\n"):
        print("失敗：授權檔不是標準麻省理工開源授權開頭")
        return False
    print("通過：正式麻省理工開源授權原文存在")
    return True


def check_readable_controls() -> bool:
    readme = repo_path("README.md").read_text(encoding="utf-8", errors="strict")
    boundary = repo_path("PUBLIC_PRIVATE_BOUNDARY.md").read_text(encoding="utf-8", errors="strict")
    registry = load_registry()
    requirements = {
        "README.md": [
            "LKMINI://物件名稱/動作",
            "九個必要核心只是最低保護集合，不是公開內容上限",
            "A_EQUALS_A=true",
        ],
        "PUBLIC_PRIVATE_BOUNDARY.md": [
            "九個檔案是最低保護集合",
            "🧾公開模組登記",
            "不得用「可能有私人內容」作為刪掉整個公開模組的理由",
            f"PROTECTED_PUBLIC_MODULES={len(PROTECTED_PUBLIC_MODULES)}",
        ],
    }
    for record in registry["🧩公開模組"]:
        requirements["README.md"].extend([record["名稱"], record["網址"], record["路徑"]])
    for label, content in (("README.md", readme), ("PUBLIC_PRIVATE_BOUNDARY.md", boundary)):
        missing = [value for value in requirements[label] if value not in content]
        if missing:
            print(f"失敗：{label} 缺少必要可讀控制：{missing}")
            return False
    print("通過：公開說明書與公開／私人邊界完整列出保護規則")
    return True


def check_module_contents() -> bool:
    ok = True
    for rel, required_phrases in MODULE_CONTENT_REQUIREMENTS.items():
        content = repo_path(rel).read_text(encoding="utf-8", errors="strict")
        missing = sorted(phrase for phrase in required_phrases if phrase not in content)
        if missing:
            print(f"失敗：復原公開模組缺少必要內容：{rel}：{missing}")
            ok = False
        else:
            print(f"通過：復原公開模組內容完整：{rel}")
    return ok


def check_structures() -> bool:
    ok = True
    for rel, path in iter_repo_files():
        suffix = path.suffix.lower()
        try:
            if suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif suffix == ".html":
                parser = MinimalHTMLParser()
                parser.feed(path.read_text(encoding="utf-8"))
                parser.close()
                if parser.html_count != 1 or parser.title_count != 1 or parser.viewport_count < 1:
                    raise ValueError("網頁結構缺少 html、title 或 viewport")
                if parser.external_script_count:
                    raise ValueError("網頁不得載入外部程式碼")
            elif suffix == ".svg":
                root = ET.fromstring(path.read_text(encoding="utf-8"))
                if not root.tag.endswith("svg"):
                    raise ValueError("向量圖根節點不是 svg")
            elif suffix == ".py":
                compile(path.read_text(encoding="utf-8"), rel, "exec")
        except Exception as exc:
            print(f"失敗：結構解析失敗：{rel}：{exc}")
            ok = False
    if ok:
        print("通過：結構化資料、網頁、向量圖與 Python 程式均可解析")
    return ok


def check_builder_safety() -> bool:
    rel = "08｜自動化同步｜SyncAutomation/🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder.py"
    content = repo_path(rel).read_text(encoding="utf-8")
    forbidden = ["subprocess", "socket", "requests", "urllib.request", "eval(", "exec(", "os.system"]
    hits = [token for token in forbidden if token in content]
    if hits:
        print(f"失敗：公開建置器含不允許的外部執行或網路能力：{hits}")
        return False
    print("通過：公開建置器只讀取本機登記檔與公開文字檔")
    return True


def check_no_private_values() -> bool:
    ok = True
    for rel, path in iter_repo_files():
        if rel in PRIVATE_SCAN_EXEMPT:
            continue
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PRIVATE_VALUE_PATTERNS.items():
            if pattern.search(content):
                print(f"失敗：{label} 出現在 {rel}")
                ok = False
    if ok:
        print("通過：未發現密鑰、私人識別碼、私人郵件或私人雲端座標")
    return ok


def check_sha256sums() -> bool:
    manifest_path = repo_path("SHA256SUMS")
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
        path = repo_path(rel)
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


def main() -> int:
    results = [
        check_registry(),
        check_required_files(),
        check_public_tree(),
        check_mit_license(),
        check_readable_controls(),
        check_module_contents(),
        check_structures(),
        check_builder_safety(),
        check_no_private_values(),
        check_sha256sums(),
    ]
    passed = sum(results)
    total = len(results)
    print(f"\n🔬公開驗證總結：{passed}/{total} 項通過")
    if all(results):
        print("A=A：公開核心與固定公開模組均已保留並通過驗證。")
        return 0
    print("失敗：公開種子尚未通過驗證。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
