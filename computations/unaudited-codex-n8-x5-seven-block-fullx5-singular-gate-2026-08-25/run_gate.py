#!/usr/bin/env python3
"""Atomic bounded runner for the canonical exact Singular gate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
INPUT = HERE / "canonical_full_x5.sing"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", str(INPUT)],
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        timed_out = False
    except subprocess.TimeoutExpired as error:
        returncode = 124
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        timed_out = True
    wall = time.monotonic() - started
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    unit = "STATUS=UNIT_IDEAL" in stdout and returncode == 0
    nonunit = "STATUS=NONUNIT_OR_UNRESOLVED" in stdout and returncode == 0
    status = "PASS_UNIT_IDEAL" if unit else (
        "TERMINAL_NONUNIT_RESULT" if nonunit else "INCOMPLETE_WALL_GATE"
    )
    result = {
        "schema": "KRENN_X5_CANONICAL_SEVEN_BLOCK_SINGULAR_GATE_RUN_V1",
        "status": status,
        "algorithm": "slimgb",
        "input_sha256": sha256(INPUT),
        "timeout_seconds": 120,
        "wall_seconds": wall,
        "peak_rss_kib": usage.ru_maxrss,
        "returncode": returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "unit_ideal": unit,
        "mathematical_coverage": unit,
    }
    temporary = HERE / "results_singular_gate.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_singular_gate.json")
    print(json.dumps({key: result[key] for key in (
        "status", "wall_seconds", "peak_rss_kib", "returncode", "timed_out", "unit_ideal"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
