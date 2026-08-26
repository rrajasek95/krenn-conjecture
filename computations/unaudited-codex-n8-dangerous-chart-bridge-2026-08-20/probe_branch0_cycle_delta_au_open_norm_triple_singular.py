#!/usr/bin/env python3
"""Time-bounded Singular probe of the p1009 pair-norm triple."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", choices=("dp", "lp"), default="lp")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    factors = [
        (HERE / f"branch0_cycle_delta_au_open_norm_{pair}_p1009.factor")
        .read_text().strip()
        for pair in ("LR", "LT", "RT")
    ]
    program = (
        f"ring R=1009,(d1,x),{args.order};option(redSB);"
        f"ideal I={','.join(factors)};ideal G=slimgb(I);"
        'print("BEGIN");print(size(G));print(dim(G));'
        'if(size(G)==1){print(G[1]);};print("END");quit;'
    )
    try:
        completed = subprocess.run(
            ["Singular", "-q", "--no-warn"], input=program, text=True,
            capture_output=True, timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return
    print("returncode", completed.returncode)
    print(completed.stdout)
    if completed.stderr:
        print("STDERR")
        print(completed.stderr)


if __name__ == "__main__":
    main()
