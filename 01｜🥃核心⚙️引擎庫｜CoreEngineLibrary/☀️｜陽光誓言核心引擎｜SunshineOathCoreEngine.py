#!/usr/bin/env python3
# ☀️｜陽光誓言核心引擎｜SunshineOathCoreEngine
# 固定規則：每份完整執行指令最前面自動帶入。

FIXED_OATH = """☀️｜陽光誓言前置誓約｜SunshineOath

以晨光為前，以真實為界；不虛構、不越權、不遺漏，先完成可驗證的封裝，再回報實際狀態。
"""

def render_sunshine_oath(task: str, deliverables: list[str], acceptance: list[str]) -> str:
    lines = [
        FIXED_OATH.rstrip(),
        "",
        "🎯｜本回合承諾完成｜CommittedTask",
        task.strip(),
        "",
        "📦｜本回合承諾交付｜CommittedDeliverables",
        *[f"→ {x}" for x in deliverables],
        "",
        "🔬｜本回合承諾驗收｜CommittedAcceptance",
        *[f"→ {x}" for x in acceptance],
        "",
        "我承諾：沒有工具證據的項目不寫 PASS；沒有讀回不說同步成功；沒有實體檔案不說已交付。"
    ]
    return "\n".join(lines)
