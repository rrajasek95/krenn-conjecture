#!/usr/bin/env python3
"""Replay all four exact F2 SAT orbits for W_6 + e_2^tensor6.

This does not certify nonexistence over extensions of F2.
"""

from __future__ import annotations

import concurrent.futures
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEARCH = HERE / "search_char2_general.py"


def run_orbit(orbit: int):
    command = [
        sys.executable,
        str(SEARCH),
        "--n",
        "6",
        "--target-kind",
        "w-plus-product",
        "--no-canonical",
        "--fix-w-matching",
        "--fix-w-product-orbit",
        str(orbit),
        "--solver",
        "kissat404",
    ]
    completed = subprocess.run(
        command,
        cwd=HERE.parent,
        check=False,
        capture_output=True,
        text=True,
    )
    return orbit, completed


def main() -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_orbit, range(4)))

    for orbit, completed in sorted(results):
        print(f"--- orbit {orbit} ---")
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        assert completed.returncode == 0
        assert "sat=False" in completed.stdout
        assert "sat=True" not in completed.stdout
    print("verified all four W_6 + product F2 orbits UNSAT")
    print("scope: exact over F2 only; no algebraic-extension claim")


if __name__ == "__main__":
    main()
