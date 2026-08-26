#!/usr/bin/env python3
"""Atomic bounded runner for the 19-variable exact-Q support chart."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "rep2_core43_f3_support_chart_Q.sing"


def main():
    started = time.monotonic()
    process = subprocess.run(
        ["gtimeout", "60", "Singular", str(INPUT)], capture_output=True, text=True,
        timeout=65,
    )
    wall = time.monotonic() - started
    stdout = process.stdout + process.stderr
    assert process.returncode == 0
    assert "INPUT_GENERATORS=14" in stdout
    assert "UNIT_REMAINDER=1" in stdout and "STATUS=NONUNIT" in stdout
    stdout_path = HERE / "rep2_core43_f3_support_chart_Q.stdout"
    temporary = stdout_path.with_suffix(".stdout.tmp")
    temporary.write_text(stdout)
    os.replace(temporary, stdout_path)
    result = {
        "schema": "KRENN_X5_REP2_CORE43_Q_SUPPORT_CHART_RUN_V1",
        "status": "PASS_TERMINAL_NONUNIT",
        "returncode": process.returncode,
        "wall_seconds": wall,
        "input_generators_after_zero_simplification": 14,
        "groebner_size": 43,
        "unit_remainder": "1",
        "scope": "19-variable zero-pattern chart for the 43 amplitude equations only",
    }
    path = HERE / "results_core43_q_chart.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
