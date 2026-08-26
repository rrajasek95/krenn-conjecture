#!/usr/bin/env python3
"""Atomic bounded Singular runner for one representative-2 gate."""

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
CHARTS = ("all_equal", "incidence_eq_u", "incidence_eq_v", "minor_equal_not_incidence", "all_distinct")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", choices=("rank1", "rank1split", "rank1gauge", "rank2"), required=True)
    parser.add_argument("--chart", choices=CHARTS)
    parser.add_argument("--ring", choices=("p32003", "Q"), required=True)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.rank == "rank1":
        assert args.chart is None
        stem = f"rep2_rank1_{args.ring}"
    elif args.rank == "rank1split":
        assert args.chart is not None
        stem = f"rep2_rank1split_{args.chart}_{args.ring}"
    elif args.rank == "rank1gauge":
        assert args.chart in ("pivot_at_incidence", "pivot_off_incidence")
        stem = f"rep2_rank1gauge_{args.chart}_{args.ring}"
    else:
        assert args.chart is not None
        stem = f"rep2_rank2_{args.chart}_{args.ring}"
    source = HERE / f"{stem}.sing"
    output = HERE / f"results_{stem}.json"
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", str(source)], text=True, capture_output=True,
            timeout=args.timeout, check=False,
        )
        returncode, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
        timed_out = False
    except subprocess.TimeoutExpired as error:
        returncode = 124
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        timed_out = True
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    unit = returncode == 0 and "STATUS=UNIT_IDEAL" in stdout
    nonunit = returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    rational = unit and args.ring == "Q"
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_GATE_RUN_V1",
        "status": (
            "PASS_RATIONAL_UNIT_IDEAL" if rational else
            "PASS_MODULAR_UNIT_DIAGNOSTIC" if unit else
            "TERMINAL_NONUNIT_OR_UNRESOLVED" if nonunit else
            "INCOMPLETE_WALL_GATE"
        ),
        "representative_id": 2,
        "rank_branch": args.rank,
        "chart": args.chart,
        "ring": args.ring,
        "algorithm": "slimgb",
        "input_sha256": sha256(source),
        "timeout_seconds": args.timeout,
        "wall_seconds": time.monotonic() - started,
        "peak_rss_raw_darwin_bytes": usage.ru_maxrss,
        "returncode": returncode,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
        "unit_ideal": unit,
        "mathematical_coverage": rational,
    }
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({key: result[key] for key in (
        "status", "rank_branch", "chart", "ring", "wall_seconds", "peak_rss_raw_darwin_bytes", "returncode"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
