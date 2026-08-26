#!/usr/bin/env python3
"""Three-mode wrapper for the base12 plus raw t_123 degree-9 dual."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "replay_plus10_d9_dual.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("face03113_plus9_replay_base", BASE_PATH)
BASE.CORE = HERE / "face03113_plus9_d9_core.jsonl"
BASE.SOLVE = HERE / "results_face03113_plus9_d9_p1009.json"
BASE.RESULT_PREFIX = HERE / "results_plus9_d9_dual_replay"
BASE.EXTRA = 9
BASE.CORE_SHA = "926a20243ad08b183399095d4800a41371eda23c738ba3ce8c0dcc292d18be1e"
BASE.SOLVE_SHA = "9593204edaee51daa61f3c1b2e4719fa10cecdb65ba90e5ec9b5513c78036d07"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    BASE.replay(args.mode)


if __name__ == "__main__":
    main()
