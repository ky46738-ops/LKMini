#!/usr/bin/env python3
"""🔬公開種子驗證工具｜verify_lkmini

保護必要核心、固定公開模組、中文優先命名、公開邊界、雜湊、
逐檔刪除裁決、互動顯影、定位器、回推鏈與本體不漂移原則。

A_EQUALS_A=true
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(".").resolve()
REGISTRY = "🧾公開模組登記｜PublicModuleRegistry.json"
FORENSICS = "09｜公開協議｜PublicProtocol/🧾開源刪除鑑識清冊｜OpenSourceDeletionForensics.json"
STATE = "09｜公開協議｜PublicProtocol/📸開源內容復原狀態｜OpenSourceRestorationState.json"
ROOT_PROTOCOL = "LKMINI://"
ROOT_SHA256 = "6c0f6f487d8af27de4a8cee9f3fc853f0fbcf417cbd21acb56ac65c55adfcf34"

REQUIRED_CORE = {
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "LKMini.svg",
    "PUBLIC_PRIVATE_BOUNDARY.md",
    "SHA256SUMS",
    ".github/workflows/gatekeeper.yml",
    "tools/verify_lkmini.py",
    REGISTRY,
}

PROTECTED_MODULES = {
    '07｜公開顯影｜PublicProjection/🔧工具規範｜ToolSpecifications.html',
    '07｜公開顯影｜PublicProjection/🎨介面研究互動範例｜UIResearchInteractiveExamples.html',
    '07｜公開顯影｜PublicProjection/🎨介面研究延伸範例｜UIResearchExtendedExamples.html',
    '07｜公開顯影｜PublicProjection/🖥️系統流程互動範例｜SystemFlowInteractiveExample.html',
    '07｜公開顯影｜PublicProjection/🎴本體顯影關係圖｜IdentityProjectionDiagram.svg',
    '08｜自動化同步｜SyncAutomation/🍎蘋果捷徑功能接線｜AppleShortcutFunctionWiring.md',
    '08｜自動化同步｜SyncAutomation/🔧工具規範公開建置器｜ToolSpecificationsPublicBuilder.py',
    '.github/workflows/🔧工具規範公開建置流程｜ToolSpecificationsPublicBuildWorkflow.yml',
    '03｜知識驗證｜KnowledgeVerification/🐙章魚貓介面能力研究｜GitHubRestCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🐙章魚貓事件能力研究｜GitHubEventCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🐙章魚貓執行證據能力研究｜GitHubExecutionEvidenceCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🐙章魚貓安全能力研究｜GitHubSecurityCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🐙章魚貓流程能力研究｜GitHubWorkflowCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🐙章魚貓成品快取能力研究｜GitHubArtifactCacheCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🔗供應鏈證據能力研究｜SupplyChainEvidenceCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🖥️執行環境能力研究｜DeploymentRunnerCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🧪評分器介面能力研究｜OpenAIGradersCapabilityResearch.json',
    '03｜知識驗證｜KnowledgeVerification/🎨介面研究歷程｜UIResearchHistory.json',
    '03｜知識驗證｜KnowledgeVerification/🎨素材介面研究歷程｜MaterialUIResearchHistory.json',
    '03｜知識驗證｜KnowledgeVerification/🧪可逆結構實驗歷程｜ReversibleStructureExperimentHistory.json',
    '09｜公開協議｜PublicProtocol/🌱唯一真相源｜MarkdownSeed.md',
    '09｜公開協議｜PublicProtocol/🧭系統流程｜SystemFlowS0S10.md',
    '09｜公開協議｜PublicProtocol/📘全副檔名可逆轉換完整手冊｜ReversibleFormatManual.md',
    '09｜公開協議｜PublicProtocol/🔗本體顯影互換協議｜IdentityProjectionInterchangeProtocol.md',
    '09｜公開協議｜PublicProtocol/♾️公開回推鏈｜PublicReverseChain.json',
    '09｜公開協議｜PublicProtocol/🧭公開定位器｜PublicLocator.json',
    '09｜公開協議｜PublicProtocol/🧾開源刪除鑑識清冊｜OpenSourceDeletionForensics.json',
    '09｜公開協議｜PublicProtocol/📸開源內容復原狀態｜OpenSourceRestorationState.json',
}

PUBLIC_ROOTS = {
    "03｜知識驗證｜KnowledgeVerification",
    "07｜公開顯影｜PublicProjection",
    "08｜自動化同步｜SyncAutomation",
    "09｜公開協議｜PublicProtocol",
}

CORE_DIRS = {
    ".github",
    ".github/workflows",
    "tools",
}

SAFE_SUFFIXES = {".md", ".py", ".html", ".svg", ".json", ".yml", ".yaml", ".txt", ".css", ".js", ".ts", ".sh"}
FORBIDDEN_BINARY = {".zip", ".pdf", ".xlsx", ".xls", ".numbers", ".pages", ".key", ".webarchive", ".wacz", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".aicore"}
FORBIDDEN_OBJECT_NAME_TERMS = ("動作容器", "動作鏈")
MAX_BYTES = 2_000_000
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
URI = re.compile(r"^LKMINI://[^/?#]+/[^/?#]+$")
PRIVATE_PATTERNS = {
    "密鑰或權杖": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=：]\s*[\"']?[A-Za-z0-9_./+=-]{8,}"),
    "常見秘密格式": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "私人檔案識別碼": re.compile(r"\bfile_[0-9a-f]{16,}\b"),
    "私人穩定識別碼": re.compile(r"\blibfile_[0-9a-f]{16,}\b"),
    "私人雲端網址": re.compile(r"https://(?:drive|docs)\.google\.com/"),
    "私人郵件地址": re.compile(r"(?i)\b[A-Z0-9._%+-]+@(?:gmail|googlemail)\.com\b"),
    "私人追蹤識別值": re.compile(r"(?i)\b(?:MessageID|ThreadID|RevisionID|DocumentID|FolderID|FileID|ObjectID)\s*[:=：]\s*[\"']?[A-Za-z0-9_-]{8,}"),
}

class PublicHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html = 0
        self.title = 0
        self.viewport = 0
        self.external_script = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.html += 1
            if data.get("lang") != "zh-Hant":
                raise ValueError("網頁缺少繁體中文語言標記")
        elif tag == "title":
            self.title += 1
        elif tag == "meta" and data.get("name") == "viewport":
            self.viewport += 1
        elif tag == "script" and data.get("src"):
            self.external_script += 1

def path_for(rel: str) -> Path:
    p = (ROOT / rel).resolve()
    if p != ROOT and ROOT not in p.parents:
        raise ValueError(f"路徑越界：{rel}")
    return p

def all_files() -> list[tuple[str, Path]]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if p.is_file():
            out.append((rel, p))
    return out

def all_dirs() -> list[str]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if p.is_dir():
            out.append(rel)
    return out

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def is_module_path(rel: str) -> bool:
    return rel in PROTECTED_MODULES

def check_required() -> bool:
    required = REQUIRED_CORE | PROTECTED_MODULES
    missing = sorted(x for x in required if not path_for(x).is_file())
    if missing:
        print("失敗：缺少必要檔案：", missing)
        return False
    print(f"通過：必要核心 {len(REQUIRED_CORE)} 項、固定公開模組 {len(PROTECTED_MODULES)} 項均存在")
    return True

def check_tree() -> bool:
    ok = True
    for rel in all_dirs():
        if rel in CORE_DIRS or any(rel == root or rel.startswith(root + "/") for root in PUBLIC_ROOTS):
            continue
        print("失敗：未登記資料夾：", rel)
        ok = False

    for rel, p in all_files():
        if rel not in REQUIRED_CORE and rel not in PROTECTED_MODULES:
            print("失敗：未登記檔案：", rel)
            ok = False
            continue
        if p.stat().st_size > MAX_BYTES:
            print("失敗：檔案過大：", rel)
            ok = False
        suffix = p.suffix.lower()
        if suffix in FORBIDDEN_BINARY:
            print("失敗：公開儲存庫出現二進位交付物：", rel)
            ok = False
        if rel in PROTECTED_MODULES and suffix not in SAFE_SUFFIXES:
            print("失敗：公開模組副檔名不允許：", rel)
            ok = False
    if ok:
        print("通過：公開樹只有必要核心與固定登記模組")
    return ok

def check_registry() -> bool:
    try:
        data = json.loads(path_for(REGISTRY).read_text(encoding="utf-8"))
    except Exception as exc:
        print("失敗：公開模組登記不可讀：", exc)
        return False

    ok = True
    if data.get("🧭根協議") != ROOT_PROTOCOL or data.get("🔐根錨點雜湊") != ROOT_SHA256:
        print("失敗：公開模組登記根協議或錨點錯誤")
        ok = False

    records = data.get("🧩公開模組")
    if not isinstance(records, list):
        print("失敗：公開模組登記不是清單")
        return False

    paths = [x.get("路徑") for x in records]
    names = [x.get("名稱") for x in records]
    urls = [x.get("網址") for x in records]
    if set(paths) != PROTECTED_MODULES or len(paths) != len(PROTECTED_MODULES):
        print("失敗：固定保護集合與登記路徑不一致")
        ok = False
    for label, values in (("名稱", names), ("網址", urls), ("路徑", paths)):
        if len(values) != len(set(values)):
            print(f"失敗：公開模組{label}重複")
            ok = False
    for record in records:
        name = record.get("名稱", "")
        url = record.get("網址", "")
        rel = record.get("路徑", "")
        if "｜" not in name or not CJK.search(name.split("｜", 1)[0]):
            print("失敗：人類名稱不是中文優先：", name)
            ok = False
        if not URI.fullmatch(url):
            print("失敗：公開網址格式錯誤：", url)
            ok = False
        if not path_for(rel).is_file():
            print("失敗：登記路徑不存在：", rel)
            ok = False
        if any(term in name or term in Path(rel).name for term in FORBIDDEN_OBJECT_NAME_TERMS):
            print("失敗：物件名稱使用禁用命名：", rel)
            ok = False
    if ok:
        print("通過：公開模組登記、固定集合、網址與中文優先命名一致")
    return ok

def check_formats() -> bool:
    ok = True
    for rel, p in all_files():
        suffix = p.suffix.lower()
        try:
            if suffix == ".json":
                json.loads(p.read_text(encoding="utf-8"))
            elif suffix == ".html":
                parser = PublicHTMLParser()
                parser.feed(p.read_text(encoding="utf-8"))
                if parser.html != 1 or parser.title != 1 or parser.viewport < 1 or parser.external_script:
                    raise ValueError("網頁結構、標題、viewport 或外部程式不合格")
            elif suffix == ".svg":
                ET.fromstring(p.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"失敗：格式驗證：{rel}：{exc}")
            ok = False
    if ok:
        print("通過：JSON、HTML 與 SVG 結構可解析")
    return ok

def check_private_values() -> bool:
    ok = True
    for rel, p in all_files():
        if p.suffix.lower() not in SAFE_SUFFIXES:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                print(f"失敗：{label} 出現在 {rel}")
                ok = False
    if ok:
        print("通過：未發現密鑰、私人識別碼、私人雲端網址或私人郵件")
    return ok

def check_license() -> bool:
    text = path_for("LICENSE").read_text(encoding="utf-8")
    required = (
        "MIT License",
        "Copyright (c) 2026 ky46738-ops",
        "Permission is hereby granted, free of charge",
        'THE SOFTWARE IS PROVIDED "AS IS"',
    )
    missing = [x for x in required if x not in text]
    if missing or not text.startswith("MIT License\n\n"):
        print("失敗：正式麻省理工開源授權原文不完整：", missing)
        return False
    print("通過：正式麻省理工開源授權原文存在")
    return True

def check_forensics() -> bool:
    try:
        data = json.loads(path_for(FORENSICS).read_text(encoding="utf-8"))
        review = data["📊逐檔裁決"]
        items = review["項目"]
    except Exception as exc:
        print("失敗：鑑識清冊不可讀：", exc)
        return False
    paths = [x.get("source_path") for x in items]
    ok = True
    if review.get("來源刪除路徑數") != 91 or review.get("未裁決數") != 0:
        print("失敗：鑑識裁決計數錯誤")
        ok = False
    if len(paths) != 91 or len(set(paths)) != 91:
        print("失敗：鑑識路徑不是九十一個唯一項目")
        ok = False
    if any(x.get("decision") in (None, "", "待人工裁決") for x in items):
        print("失敗：仍有未裁決項目")
        ok = False
    if ok:
        print("通過：九十一個刪除路徑均有唯一裁決")
    return ok

def check_state() -> bool:
    try:
        data = json.loads(path_for(STATE).read_text(encoding="utf-8"))
    except Exception as exc:
        print("失敗：復原狀態不可讀：", exc)
        return False
    ok = True
    if data.get("State") not in ("PREPARED", "COMMITTED"):
        print("失敗：復原狀態值錯誤")
        ok = False
    counts = data.get("Counts", {})
    if counts.get("deleted_paths_reviewed") != 91 or counts.get("unresolved_decisions") != 0:
        print("失敗：復原狀態裁決計數錯誤")
        ok = False
    if not data.get("Transition", {}).get("from") or not data.get("Transition", {}).get("to"):
        print("失敗：缺少 from → to")
        ok = False
    if ok:
        print("通過：復原狀態具備時間戳、轉換與零未裁決")
    return ok

def check_sha256sums() -> bool:
    observed = {}
    ok = True
    for raw in path_for("SHA256SUMS").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            print("失敗：雜湊清單格式錯誤：", line)
            ok = False
            continue
        expected, rel = parts
        observed[rel] = expected
        p = path_for(rel)
        if not p.is_file():
            print("失敗：雜湊目標不存在：", rel)
            ok = False
        elif sha256(p) != expected:
            print("失敗：雜湊不一致：", rel)
            ok = False
    expected_targets = {rel for rel, _ in all_files()} - {"SHA256SUMS"}
    if set(observed) != expected_targets:
        print("失敗：雜湊目標集合不一致")
        print("缺少：", sorted(expected_targets - set(observed)))
        print("多出：", sorted(set(observed) - expected_targets))
        ok = False
    if ok:
        print(f"通過：{len(observed)} 個公開檔案雜湊一致")
    return ok

def check_axiom() -> bool:
    text = path_for("README.md").read_text(encoding="utf-8")
    if "A_EQUALS_A=true" not in text or "Projection != Identity" not in text:
        print("失敗：公開說明書缺少公理或本體顯影區分")
        return False
    print("通過：A=A 與顯影不等於本體標記存在")
    return True

def main() -> int:
    checks = [
        check_required(),
        check_tree(),
        check_registry(),
        check_formats(),
        check_private_values(),
        check_license(),
        check_forensics(),
        check_state(),
        check_axiom(),
        check_sha256sums(),
    ]
    if all(checks):
        print("\nA=A：公開核心、二十八個公開模組與九十一項刪除裁決全部通過。")
        return 0
    print("\n失敗：公開種子尚未通過完整驗證。")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
