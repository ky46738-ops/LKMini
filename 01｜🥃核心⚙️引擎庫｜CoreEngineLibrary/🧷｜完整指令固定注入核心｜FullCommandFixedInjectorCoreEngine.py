#!/usr/bin/env python3
# 🧷｜完整指令固定注入核心｜FullCommandFixedInjectorCoreEngine
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

BASE = Path(__file__).resolve().parent

def _load(filename, module_name):
    spec = spec_from_file_location(module_name, BASE / filename)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

SUN = _load("☀️｜陽光誓言核心引擎｜SunshineOathCoreEngine.py", "sunshine_oath")
DEATH = _load("☠️｜死亡憲法核心引擎｜DeathConstitutionCoreEngine.py", "death_constitution")

def build_full_command(task: str, body: str, deliverables: list[str], acceptance: list[str]) -> str:
    return (
        SUN.render_sunshine_oath(task, deliverables, acceptance)
        + "\n\n"
        + body.strip()
        + "\n\n"
        + DEATH.render_death_constitution()
    )
