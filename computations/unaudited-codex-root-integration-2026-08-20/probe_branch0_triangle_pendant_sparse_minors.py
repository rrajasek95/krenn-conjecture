#!/usr/bin/env python3
"""Sparse exact rank-minor probe for the reduced triangle+pendant chart.

Unlike the symbolic prototype, this forms all 3x3 minors directly in the
source audit's sparse Laurent representation, orders them by support size,
and permits bounded prefixes.  A prefix that is already a localized unit is
a smaller necessary-system certificate candidate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import importlib.util
import math
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
REDUCTION = (HERE.parent /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "discover_branch0_triangle_pendant_reduction.py")


def load(path: Path):
    spec = importlib.util.spec_from_file_location("root_tp_sparse_reduction", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load(REDUCTION)
C = D.CHART


def split_row(poly):
    pieces = [{}, {}, {}]  # coefficient of a4, coefficient of a5, constant
    for monomial, value in poly.items():
        p4, p5 = monomial[4], monomial[5]
        if p4 < 0 or p5 < 0 or p4+p5 > 1:
            raise RuntimeError((p4, p5))
        target = 0 if p4 else (1 if p5 else 2)
        exponent = list(monomial)
        exponent[4] = exponent[5] = 0
        pieces[target][tuple(exponent)] = value
    return tuple(pieces)


def determinant(rows):
    a, b, c = rows
    return C.add(
        C.multiply(a[0], b[1], c[2]),
        C.multiply(a[1], b[2], c[0]),
        C.multiply(a[2], b[0], c[1]),
        C.scale(C.multiply(a[2], b[1], c[0]), -1),
        C.scale(C.multiply(a[1], b[0], c[2]), -1),
        C.scale(C.multiply(a[0], b[2], c[1]), -1),
    )


def normalize(poly):
    if not poly:
        return poly
    minima = [min(monomial[index] for monomial in poly)
              for index in range(C.n)]
    shifted = {tuple(power-minimum for power, minimum
                     in zip(monomial, minima)): value
               for monomial, value in poly.items()}
    denominator_lcm = math.lcm(*(value.denominator for value in shifted.values()))
    integers = [value.numerator*(denominator_lcm//value.denominator)
                for value in shifted.values()]
    content = math.gcd(*map(abs, integers))
    scale = Fraction(denominator_lcm, content)
    shifted = C.scale(shifted, scale)
    first = shifted[min(shifted)]
    if first < 0:
        shifted = C.scale(shifted, -1)
    return shifted


def derive():
    rows, _, _, _ = D.solve_full_chain_use_e()
    coefficient_rows = [(label, split_row(poly)) for label, poly in rows]
    minors, seen = [], set()
    for triple in combinations(coefficient_rows, 3):
        value = normalize(determinant([row for _, row in triple]))
        if not value:
            continue
        encoded = C.singular(value)
        if encoded in seen:
            continue
        seen.add(encoded)
        minors.append((len(value), tuple(label for label, _ in triple), value))
    return sorted(minors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--algorithm", choices=("slimgb", "std"), default="slimgb")
    args = parser.parse_args()
    started = time.monotonic()
    minors = derive()
    print("derive_seconds:", time.monotonic()-started, flush=True)
    print("minor_count:", len(minors), "term_range:",
          minors[0][0], minors[-1][0], flush=True)
    selected = minors[:args.limit] if args.limit else minors
    print("selected:", [(terms, labels) for terms, labels, _ in selected],
          flush=True)

    b0, b1, b3 = (C.variable(index) for index in (6, 7, 9))
    d4, d5 = (C.variable(C.d_index[index]) for index in (4, 5))
    d3 = C.add(C.multiply(b1, d4), C.multiply(b0, d5))
    live = (b0, b1, b3, d4, d5, d3)
    inverse = tuple(f"z{index}" for index in range(len(live)))
    parameter_names = ("b0", "b1", "b3", "d4", "d5")
    names = ",".join(parameter_names + inverse)
    generators = [C.singular(poly) for _, _, poly in selected]
    generators += [f"z{index}*({C.singular(poly)})-1"
                   for index, poly in enumerate(live)]
    command = (f"ring R={args.characteristic},({names}),dp;"
               f"ideal I={','.join(generators)};"
               f"ideal G={args.algorithm}(I);"
               'print("BEGIN");print(string(reduce(1,G)));'
               'print(size(G));print(dim(G));print("END");quit;')
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT after {time.monotonic()-started:.3f}s")
        return
    print("elapsed_seconds:", time.monotonic()-started)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
