#!/usr/bin/env python3
"""
🧭Markdown標題改名器｜MarkdownH1RenameTool

Purpose:
- Walk a target folder and read every .md file.
- Use the first-line H1 as the canonical filename source.
- Sanitize illegal filename characters.
- Rename through `git mv` so Git history is preserved.
- Rewrite repo references to old filenames/paths in wikilink, obsidian URL, locator, JSON, Markdown, HTML, YAML, TXT, CSV, TSV, and other text files.
- Emit reversible logs for SHA-256 verification and rollback.

Usage:
  python3 tools/rename_md_by_h1.py --target . --apply
  python3 tools/rename_md_by_h1.py --target docs --dry-run

A_EQUALS_A=true
NO_FAKE_RESULT=true
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ILLEGAL_FILENAME_CHARS = r'[/\\:*?"<>|\x00-\x1F]'
TEXT_EXTENSIONS = {
    ".md", ".markdown", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".csv", ".tsv",
    ".html", ".htm", ".xml", ".js", ".ts", ".css", ".py", ".sh", ".toml",
    ".ini", ".conf", ".manifest", "",
}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache"}


@dataclass
class RenameItem:
    old_path: str
    new_path: str
    old_filename: str
    new_filename: str
    h1: str
    reason: str
    status: str


@dataclass
class ReplaceItem:
    file_path: str
    replacements: int
    sha256_before: str
    sha256_after: str


def repo_root() -> Path:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
        return Path(out).resolve()
    except Exception:
        return Path.cwd().resolve()


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sanitize_filename_stem(raw: str) -> str:
    raw = raw.strip().lstrip("#").strip()
    raw = re.sub(ILLEGAL_FILENAME_CHARS, "｜", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    raw = raw.strip(" .")
    # Avoid Windows reserved device names.
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    if not raw or raw.upper() in reserved:
        raw = "未命名Markdown｜UntitledMarkdown"
    return raw[:180]


def first_line_h1(path: Path) -> str | None:
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace") as f:
            first = f.readline().rstrip("\n\r")
    except Exception:
        return None
    m = re.match(r"^#\s+(.+?)\s*$", first)
    if not m:
        return None
    return m.group(1).strip()


def walk_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            yield Path(current) / name


def all_markdown_files(target: Path) -> list[Path]:
    return sorted([p for p in walk_files(target) if p.suffix.lower() == ".md"])


def unique_target(path: Path, used: set[Path]) -> Path:
    if path not in used and not path.exists():
        used.add(path)
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    i = 2
    while True:
        candidate = parent / f"{stem}｜{i:02d}{suffix}"
        if candidate not in used and not candidate.exists():
            used.add(candidate)
            return candidate
        i += 1


def build_plan(target: Path, root: Path) -> list[RenameItem]:
    used: set[Path] = set()
    plan: list[RenameItem] = []
    for md in all_markdown_files(target):
        h1 = first_line_h1(md)
        if not h1:
            plan.append(RenameItem(rel(md, root), rel(md, root), md.name, md.name, "", "NO_FIRST_LINE_H1", "SKIP"))
            continue
        new_stem = sanitize_filename_stem(h1)
        new_path = unique_target(md.with_name(new_stem + md.suffix), used)
        if md.name == new_path.name:
            plan.append(RenameItem(rel(md, root), rel(md, root), md.name, md.name, h1, "ALREADY_MATCH", "UNCHANGED"))
        else:
            plan.append(RenameItem(rel(md, root), rel(new_path, root), md.name, new_path.name, h1, "H1_FILENAME", "PENDING"))
    return plan


def run_git_mv(items: list[RenameItem], root: Path, apply: bool) -> None:
    for item in items:
        if item.status != "PENDING":
            continue
        if not apply:
            item.status = "DRY_RUN"
            continue
        old = root / item.old_path
        new = root / item.new_path
        new.parent.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(["git", "mv", "--", str(old), str(new)])
        item.status = "RENAMED"


def replacement_variants(item: RenameItem) -> list[tuple[str, str]]:
    old_path = item.old_path
    new_path = item.new_path
    old_name = item.old_filename
    new_name = item.new_filename
    old_stem = Path(old_name).stem
    new_stem = Path(new_name).stem
    variants = [
        (old_path, new_path),
        (urllib.parse.quote(old_path), urllib.parse.quote(new_path)),
        (urllib.parse.quote(old_path, safe=""), urllib.parse.quote(new_path, safe="")),
        (old_name, new_name),
        (urllib.parse.quote(old_name), urllib.parse.quote(new_name)),
        (urllib.parse.quote(old_name, safe=""), urllib.parse.quote(new_name, safe="")),
        (old_stem, new_stem),
        (urllib.parse.quote(old_stem), urllib.parse.quote(new_stem)),
        (urllib.parse.quote(old_stem, safe=""), urllib.parse.quote(new_stem, safe="")),
    ]
    # Longer replacements first to prevent partial replacement damage.
    seen: set[str] = set()
    uniq: list[tuple[str, str]] = []
    for old, new in sorted(variants, key=lambda x: len(x[0]), reverse=True):
        if old and old != new and old not in seen:
            seen.add(old)
            uniq.append((old, new))
    return uniq


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    # Include extensionless manifest/index-like files.
    if path.suffix == "" and path.name.upper() in {"MANIFEST", "SHA256SUMS", "LICENSE"}:
        return True
    return False


def rewrite_references(root: Path, plan: list[RenameItem], apply: bool, output_dir: Path) -> list[ReplaceItem]:
    replacements = [v for item in plan if item.status in {"RENAMED", "DRY_RUN"} for v in replacement_variants(item)]
    logs: list[ReplaceItem] = []
    if not replacements:
        return logs
    output_dir_rel = rel(output_dir, root) if output_dir.exists() or output_dir.parent.exists() else ""
    for path in walk_files(root):
        if not is_probably_text(path):
            continue
        rpath = rel(path, root)
        if rpath.startswith(".git/") or (output_dir_rel and rpath.startswith(output_dir_rel + "/")):
            continue
        try:
            data = path.read_bytes()
            text = data.decode("utf-8")
        except Exception:
            continue
        new_text = text
        count = 0
        for old, new in replacements:
            c = new_text.count(old)
            if c:
                new_text = new_text.replace(old, new)
                count += c
        if count:
            before = sha256_bytes(data)
            after = sha256_bytes(new_text.encode("utf-8"))
            logs.append(ReplaceItem(rpath, count, before, after))
            if apply:
                path.write_text(new_text, encoding="utf-8")
    return logs


def write_outputs(root: Path, output_dir: Path, plan: list[RenameItem], replace_log: list[ReplaceItem], apply: bool) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rename_csv = output_dir / "🧭Markdown標題改名對照表｜MarkdownH1RenameMap.csv"
    rename_json = output_dir / "🧭Markdown標題改名對照表｜MarkdownH1RenameMap.json"
    replace_jsonl = output_dir / "🔁引用替換紀錄｜ReferenceRewriteLog.jsonl"
    run_log = output_dir / "🧾執行紀錄｜ExecutionLog.md"
    sha_file = output_dir / "🔐SHA256SUMS.txt"

    with rename_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(plan[0]).keys()) if plan else ["old_path", "new_path", "status"])
        writer.writeheader()
        for item in plan:
            writer.writerow(asdict(item))
    rename_json.write_text(json.dumps([asdict(i) for i in plan], ensure_ascii=False, indent=2), encoding="utf-8")
    with replace_jsonl.open("w", encoding="utf-8") as f:
        for item in replace_log:
            f.write(json.dumps(asdict(item), ensure_ascii=False) + "\n")

    renamed_count = sum(1 for i in plan if i.status == "RENAMED")
    dry_count = sum(1 for i in plan if i.status == "DRY_RUN")
    skip_count = sum(1 for i in plan if i.status == "SKIP")
    unchanged_count = sum(1 for i in plan if i.status == "UNCHANGED")
    replacement_count = sum(i.replacements for i in replace_log)
    mode = "APPLY" if apply else "DRY_RUN"
    run_log.write_text(
        "# 🧾執行紀錄｜ExecutionLog\n\n"
        f"- mode: {mode}\n"
        f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}\n"
        f"- renamed_count: {renamed_count}\n"
        f"- dry_run_count: {dry_count}\n"
        f"- unchanged_count: {unchanged_count}\n"
        f"- skip_count: {skip_count}\n"
        f"- reference_replacement_count: {replacement_count}\n"
        "- rollback_hint: use rename map in reverse order, then re-run reference rewrite with old/new swapped.\n",
        encoding="utf-8",
    )

    output_files = [rename_csv, rename_json, replace_jsonl, run_log]
    with sha_file.open("w", encoding="utf-8") as f:
        for p in output_files:
            f.write(f"{sha256_file(p)}  {rel(p, root)}\n")
    return {p.name: rel(p, root) for p in output_files + [sha_file]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Rename Markdown files by first-line H1 and rewrite repo references.")
    parser.add_argument("--target", default=".", help="Target folder containing Markdown files. Default: repo root.")
    parser.add_argument("--output", default="09_🧾清單_MANIFEST_📤輸出_OUTPUT/🧭Markdown標題改名器｜MarkdownH1RenameTool", help="Output log folder.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Actually run git mv and rewrite references.")
    mode.add_argument("--dry-run", action="store_true", help="Only create plan/logs; do not change source files.")
    args = parser.parse_args()

    root = repo_root()
    os.chdir(root)
    target = (root / args.target).resolve()
    output_dir = (root / args.output).resolve()
    if not target.exists() or not target.is_dir():
        print(f"FAIL: target folder not found: {target}", file=sys.stderr)
        return 2

    apply = bool(args.apply)
    plan = build_plan(target, root)
    run_git_mv(plan, root, apply=apply)
    replace_log = rewrite_references(root, plan, apply=apply, output_dir=output_dir)
    outputs = write_outputs(root, output_dir, plan, replace_log, apply=apply)

    print("✅ Markdown H1 rename tool finished")
    print(f"mode={'APPLY' if apply else 'DRY_RUN'}")
    print(f"markdown_files={len(plan)}")
    print(f"renamed={sum(1 for i in plan if i.status == 'RENAMED')}")
    print(f"dry_run={sum(1 for i in plan if i.status == 'DRY_RUN')}")
    print(f"reference_replacements={sum(i.replacements for i in replace_log)}")
    for name, path in outputs.items():
        print(f"output:{name}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
