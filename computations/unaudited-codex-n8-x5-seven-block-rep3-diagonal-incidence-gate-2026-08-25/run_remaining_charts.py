#!/usr/bin/env python3
"""Sequential fail-closed modular then Q runs for the other four rep3 charts."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import run_q_p00 as core


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
CHARTS = ("p01", "p10", "p11", "p12")


def run_one(chart, label, wall_cap):
    metadata = json.loads((HERE / "gate_metadata.json").read_text())
    record = metadata["inputs"][chart][label]
    source = HERE / record["path"]
    assert core.sha256(source) == record["sha256"]
    started = time.monotonic()
    process = subprocess.Popen(["/usr/local/bin/Singular", source.name], cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    peak_rss = 0
    termination = None
    while process.poll() is None:
        elapsed = time.monotonic() - started
        peak_rss = max(peak_rss, core.rss_bytes(process.pid))
        if peak_rss > core.RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif elapsed > wall_cap:
            termination = f"WALL_CAP_{wall_cap}"
        if termination:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            break
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    unit = termination is None and process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout
    nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    if unit:
        status = "UNIT_IDEAL_MODULAR" if label == "p32003" else "UNIT_IDEAL_EXACT_Q"
    elif nonunit:
        status = "NONUNIT_DIAGNOSTIC"
    else:
        status = "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS"
    result = {
        "schema": "KRENN_X5_REP3_DIAGONAL_INCIDENCE_SEQUENTIAL_CHART_V1",
        "status": status, "mathematical_coverage": unit, "chart": chart, "ring": label,
        "wall_seconds": wall, "wall_cap_seconds": wall_cap, "rss_cap_bytes": core.RSS_CAP,
        "observed_peak_rss_bytes": peak_rss, "termination": termination, "returncode": process.returncode,
        "input_sha256": record["sha256"], "stdout": stdout, "stderr": stderr,
    }
    core.atomic_json(HERE / f"results_{label}_{chart}.json", result)
    print(json.dumps({"chart": chart, "ring": label, "status": status, "wall_seconds": wall, "peak_rss": peak_rss}, sort_keys=True), flush=True)
    return unit


def main():
    for chart in CHARTS:
        if not run_one(chart, "p32003", 60):
            raise SystemExit(f"fail closed at {chart} modular")
        if not run_one(chart, "Q", 120):
            raise SystemExit(f"fail closed at {chart} Q")


if __name__ == "__main__":
    main()
