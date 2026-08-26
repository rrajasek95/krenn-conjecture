#!/usr/bin/env python3
"""Run one bounded Singular guard-dual gate atomically."""

from __future__ import annotations

import argparse
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


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ring", choices=("p32003", "Q"), required=True)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    source = HERE / f"canonical_guard_dual_{args.ring}.sing"
    output = HERE / f"results_guard_dual_{args.ring}.json"
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", str(source)],
            text=True,
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
        returncode = completed.returncode
        stdout, stderr = completed.stdout, completed.stderr
        timed_out = False
    except subprocess.TimeoutExpired as error:
        returncode = 124
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        timed_out = True
    wall = time.monotonic() - started
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    unit = returncode == 0 and "STATUS=UNIT_IDEAL" in stdout
    nonunit = returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    mathematical = unit and args.ring == "Q"
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_GUARD_DUAL_SINGULAR_RUN_V1",
        "status": (
            "PASS_RATIONAL_UNIT_IDEAL" if mathematical else
            "PASS_MODULAR_UNIT_DIAGNOSTIC" if unit else
            "TERMINAL_NONUNIT_OR_UNRESOLVED" if nonunit else
            "INCOMPLETE_WALL_GATE"
        ),
        "ring": args.ring,
        "algorithm": "slimgb",
        "input_sha256": sha256(source),
        "timeout_seconds": args.timeout,
        "wall_seconds": wall,
        "peak_rss_raw_darwin_bytes": usage.ru_maxrss,
        "returncode": returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "unit_ideal": unit,
        "mathematical_coverage": mathematical,
    }
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({key: result[key] for key in (
        "status", "ring", "wall_seconds", "peak_rss_raw_darwin_bytes", "returncode", "unit_ideal"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
