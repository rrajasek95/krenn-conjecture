#!/usr/bin/env python3
"""Discovery audit of unrestricted full-block ideals on 11 invisible pairs."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
import shutil
import subprocess
import time

from test_polarized_fixed_q_pair17_minimal_full_ideals import coordinate_program
from verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction import COLOURS


PAIRS = (
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 2), (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
)


def run_job(singular, pair):
    cells = tuple((pair[0], pair[1], a, b)
                  for a, b in product(COLOURS, repeat=2))
    program, equations, variables = coordinate_program(cells, saturate=False)
    start = time.monotonic()
    result = subprocess.run(
        [singular, "-q"], input=program, text=True,
        capture_output=True, check=True, timeout=600,
    )
    elapsed = time.monotonic() - start
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    size = lines[lines.index("BASIS_SIZE") + 1]
    first = lines[lines.index("BASIS_FIRST") + 1]
    assert size == first == "1"
    return pair, equations, variables, elapsed


def main():
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular required")
    start = time.monotonic()
    outputs = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(run_job, singular, pair): pair for pair in PAIRS}
        for future in as_completed(jobs):
            outputs.append(future.result())
    for pair, equations, variables, elapsed in sorted(outputs):
        print(pair, "basis [1]", "equations", equations,
              "variables", variables, "seconds", f"{elapsed:.3f}")
    print("all 11 unrestricted invisible full-block ideals: PASS")
    print("parallel wall seconds", f"{time.monotonic() - start:.3f}")


if __name__ == "__main__":
    main()
