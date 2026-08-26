#!/usr/bin/env python3
"""Singular probe for the 4x4 minors of the Delta linear interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_branch0_cycle_delta_zero_linear_interface.json"


def singular(text):
    return text.replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--no-localizers", action="store_true")
    parser.add_argument("--print-gb", action="store_true")
    args = parser.parse_args()
    data = json.loads(RESULT.read_text())
    variables = data["variables"]
    matrix = data["normalized_augmented_matrix"]
    entries = ",".join(singular(entry)
                       for row in matrix for entry in row)
    equations = [singular(data["U"]), singular(data["V"])]
    if args.no_localizers:
        inverse_names = []
        localizers = []
    else:
        factors = ["b0", "b1", "x", "d1", "d4", "b1+d1", "x-1"]
        inverse_names = [f"z{index}" for index in range(len(factors))]
        localizers = [f"{name}*({factor})-1"
                      for name, factor in zip(inverse_names, factors)]
    command = (
        f"ring R={args.characteristic},"
        f"({','.join(variables + inverse_names)}),dp;"
        f"matrix M[6][4]={entries};"
        "ideal J=minor(M,4);"
        f"ideal I={','.join(equations + localizers)},J;"
        "ideal G=slimgb(I);"
        'print("BEGIN");print(size(J));print(size(G));print(dim(G));'
        'print(string(reduce(1,G)));'
    )
    if args.print_gb:
        command += 'print(G);'
    command += 'print("END");quit;'
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)


if __name__ == "__main__":
    main()
