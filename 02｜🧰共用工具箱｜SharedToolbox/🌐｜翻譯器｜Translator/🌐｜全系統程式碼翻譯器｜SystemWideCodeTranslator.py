from __future__ import annotations

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import ast
import csv
import hashlib
import json
import re
import shutil
import subprocess
import tokenize
import zipfile
from io import BytesIO
from typing import Callable

try:
    from googletrans import Translator
except Exception:
    Translator = None

支援副檔名 = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".html", ".htm", ".css", ".scss", ".vue", ".json", ".jsonl", ".yml", ".yaml", ".toml", ".md", ".txt", ".sql", ".sh", ".bash", ".zsh", ".xml", ".plist", ".ini", ".cfg"}
跳過資料夾 = {".git", ".venv", "venv", "node_modules", "__pycache__", "output", "輸出", "翻譯輸出", "dist", "build"}
不翻譯鍵名 = {"id", "identity", "sha256", "hash", "url", "uri", "path", "filename", "file", "type", "version", "status", "key", "name_en", "engine_key", "module_id", "root_sha256"}

def 台北時間() -> str:
    return datetime.now(ZoneInfo("Asia/Taipei")).isoformat()

def 檔名時間() -> str:
    return datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d-%H%M%S_TPE")

def 計算雜湊(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

class 翻譯核心:
    def __init__(self, 詞典路徑: Path | None = None, 啟用線上翻譯: bool = True):
        self.快取: dict[str, str] = {}
        self.詞典: dict[str, str] = {}
        self.翻譯器 = Translator() if (啟用線上翻譯 and Translator is not None) else None
        if 詞典路徑 and 詞典路徑.exists():
            try:
                self.詞典 = json.loads(詞典路徑.read_text(encoding="utf-8"))
            except Exception:
                self.詞典 = {}
    def 翻譯(self, text: str) -> str:
        原文 = text.strip()
        if not 原文: return text
        if 原文 in self.快取: return self._保留空白(text, self.快取[原文])
        if 原文 in self.詞典:
            譯文 = self.詞典[原文]; self.快取[原文] = 譯文; return self._保留空白(text, 譯文)
        if self._看起來不像自然語言(原文): self.快取[原文] = 原文; return text
        譯文 = 原文
        if self.翻譯器 is not None:
            try:
                result = self.翻譯器.translate(原文, src="auto", dest="zh-tw")
                if getattr(result, "text", None): 譯文 = result.text
            except Exception:
                譯文 = 原文
        self.快取[原文] = 譯文
        return self._保留空白(text, 譯文)
    @staticmethod
    def _保留空白(original: str, translated: str) -> str:
        leading = original[:len(original) - len(original.lstrip())]
        trailing = original[len(original.rstrip()):]
        return f"{leading}{translated}{trailing}"
    @staticmethod
    def _看起來不像自然語言(text: str) -> bool:
        if len(text) <= 1: return True
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text): return True
        if re.fullmatch(r"[0-9a-fA-F]{32,128}", text): return True
        if text.startswith(("http://", "https://", "/", "./", "../")): return True
        if re.fullmatch(r"[A-Z0-9_./:-]+", text): return True
        return False

def 翻譯_python(source: str, 核心: 翻譯核心) -> str:
    tokens = list(tokenize.tokenize(BytesIO(source.encode("utf-8")).readline)); output=[]
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            body=tok.string[1:]
            if body.startswith("!"): output.append(tok); continue
            new="#"+核心.翻譯(body); output.append(tokenize.TokenInfo(tok.type,new,tok.start,tok.end,tok.line))
        elif tok.type == tokenize.STRING:
            raw=tok.string; m=re.match(r"(?is)^([rubf]*)(['\"]{1,3})(.*)\2$", raw)
            if not m: output.append(tok); continue
            prefix, quote, body=m.groups()
            if "f" in prefix.lower() or "b" in prefix.lower(): output.append(tok); continue
            translated=核心.翻譯(body); new=f"{prefix}{quote}{translated}{quote}"; output.append(tokenize.TokenInfo(tok.type,new,tok.start,tok.end,tok.line))
        else: output.append(tok)
    return tokenize.untokenize(output).decode("utf-8")

def 翻譯_js類(source: str, 核心: 翻譯核心) -> str:
    source=re.sub(r"//([^\n]*)",lambda m:"//"+核心.翻譯(m.group(1)),source)
    source=re.sub(r"/\*([\s\S]*?)\*/",lambda m:"/*"+核心.翻譯(m.group(1))+"*/",source)
    pattern=re.compile(r"""(['\"])([^'\"\\\n]{2,})\1""")
    def repl_string(m):
        body=m.group(2)
        if re.search(r"[A-Za-z\u4e00-\u9fff]",body): return m.group(1)+核心.翻譯(body)+m.group(1)
        return m.group(0)
    return pattern.sub(repl_string,source)

def 翻譯_html(source: str, 核心: 翻譯核心) -> str:
    source=re.sub(r"<!--([\s\S]*?)-->",lambda m:"<!--"+核心.翻譯(m.group(1))+"-->",source)
    parts=re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>)",source,flags=re.I)
    attribute_pattern=re.compile(r'(placeholder|title|alt|aria-label)=(?:"([^"]*)"|\'([^\']*)\')',flags=re.I)
    for i in range(0,len(parts),2):
        parts[i]=re.sub(r">([^<>]+)<",lambda m:">"+核心.翻譯(m.group(1))+"<",parts[i])
        def repl_attr(m):
            text=m.group(2) if m.group(2) is not None else m.group(3)
            return f'{m.group(1)}="'+核心.翻譯(text or "")+'"'
        parts[i]=attribute_pattern.sub(repl_attr,parts[i])
    return "".join(parts)

def 翻譯_json(source: str, 核心: 翻譯核心) -> str:
    data=json.loads(source)
    def walk(value,key=None):
        if isinstance(value,dict): return {k:walk(v,k) for k,v in value.items()}
        if isinstance(value,list): return [walk(v,key) for v in value]
        if isinstance(value,str) and str(key).lower() not in 不翻譯鍵名: return 核心.翻譯(value)
        return value
    return json.dumps(walk(data),ensure_ascii=False,indent=2)

def 翻譯_純文字(source: str, 核心: 翻譯核心) -> str:
    return "\n".join(核心.翻譯(line) if line.strip() else line for line in source.splitlines())

def 選擇翻譯器(path: Path) -> Callable[[str, 翻譯核心], str]:
    ext=path.suffix.lower()
    if ext==".py": return 翻譯_python
    if ext in {".js",".mjs",".cjs",".ts",".tsx",".jsx",".vue"}: return 翻譯_js類
    if ext in {".html",".htm"}: return 翻譯_html
    if ext in {".json",".jsonl"}: return 翻譯_json
    return 翻譯_純文字

def 驗證(path: Path) -> tuple[bool,str]:
    ext=path.suffix.lower()
    try:
        if ext==".py": ast.parse(path.read_text(encoding="utf-8")); return True,"語法通過"
        if ext==".json": json.loads(path.read_text(encoding="utf-8")); return True,"結構通過"
        if ext in {".js",".mjs",".cjs"} and shutil.which("node"):
            result=subprocess.run(["node","--check",str(path)],capture_output=True,text=True); return result.returncode==0,result.stderr.strip() or "語法通過"
        if ext in {".sh",".bash",".zsh"} and shutil.which("bash"):
            result=subprocess.run(["bash","-n",str(path)],capture_output=True,text=True); return result.returncode==0,result.stderr.strip() or "語法通過"
        return True,"已完成文字輸出"
    except Exception as exc: return False,str(exc)

def 掃描來源(root: Path, output_root: Path) -> list[Path]:
    result=[]
    for path in root.rglob("*"):
        if not path.is_file(): continue
        if path.stat().st_size==0: continue
        if output_root in path.parents: continue
        if any(part in 跳過資料夾 for part in path.parts): continue
        if "｜繁體中文" in path.stem: continue
        if path.suffix.lower() in 支援副檔名: result.append(path)
    return sorted(result)

def 翻譯檔案(source: Path, source_root: Path, output_root: Path, 核心: 翻譯核心) -> dict:
    rel=source.relative_to(source_root); target_dir=output_root/rel.parent; target_dir.mkdir(parents=True,exist_ok=True); target=target_dir/f"{source.stem}｜繁體中文{source.suffix}"
    row={"正式原名":source.name,"來源相對路徑":str(rel),"來源位元組":source.stat().st_size,"來源雜湊":計算雜湊(source),"輸出正式原名":target.name,"輸出相對路徑":str(target.relative_to(output_root)),"輸出位元組":"","輸出雜湊":"","狀態":"錯誤","驗證":"","錯誤":""}
    try:
        source_text=source.read_text(encoding="utf-8"); translated=選擇翻譯器(source)(source_text,核心); target.write_text(translated,encoding="utf-8"); ok,message=驗證(target)
        row.update({"輸出位元組":target.stat().st_size,"輸出雜湊":計算雜湊(target),"狀態":"完成" if ok else "錯誤","驗證":message})
    except Exception as exc: row["錯誤"]=str(exc)
    return row

def 寫清單(path: Path, rows: list[dict]) -> None:
    fields=["正式原名","來源相對路徑","來源位元組","來源雜湊","輸出正式原名","輸出相對路徑","輸出位元組","輸出雜湊","狀態","驗證","錯誤"]
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)

def 建立交付包(output_root: Path) -> Path:
    package=output_root.parent/f"🌐全系統程式碼翻譯📦交付包｜{檔名時間()}.zip"
    with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(output_root.rglob("*")):
            if p.is_file(): z.write(p,arcname=str(p.relative_to(output_root)))
    return package

def main() -> int:
    parser=argparse.ArgumentParser(description="同資料夾全系統程式碼翻譯器"); parser.add_argument("--來源",default=".",help="來源資料夾"); parser.add_argument("--輸出",default="翻譯輸出",help="輸出資料夾"); parser.add_argument("--詞典",default="📚程式碼翻譯詞典.json",help="本機翻譯詞典"); parser.add_argument("--停用線上翻譯",action="store_true"); args=parser.parse_args()
    source_root=Path(args.來源).resolve(); output_root=(source_root/args.輸出).resolve(); output_root.mkdir(parents=True,exist_ok=True)
    詞典=source_root/args.詞典; 核心=翻譯核心(詞典,啟用線上翻譯=not args.停用線上翻譯)
    rows=[]
    for source in 掃描來源(source_root,output_root):
        row=翻譯檔案(source,source_root,output_root,核心); rows.append(row); print(f"{row['狀態']}｜{row['正式原名']}")
    清單=output_root/"📋翻譯清單.csv"; 寫清單(清單,rows)
    回執={"回執名稱":"🌐全系統程式碼翻譯回執","時間":台北時間(),"來源":str(source_root),"輸出":str(output_root),"掃描數":len(rows),"完成數":sum(r["狀態"]=="完成" for r in rows),"錯誤數":sum(r["狀態"]=="錯誤" for r in rows),"來源修改":0}
    回執路徑=output_root/"🧾翻譯回執.json"; 回執路徑.write_text(json.dumps(回執,ensure_ascii=False,indent=2),encoding="utf-8")
    package=建立交付包(output_root); 回執["交付包"]=package.name; 回執["交付包雜湊"]=計算雜湊(package); 回執路徑.write_text(json.dumps(回執,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(回執,ensure_ascii=False,indent=2)); return 0 if 回執["錯誤數"]==0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
