#!/usr/bin/env python3
"""UNAUDITED PROBE (P2 appendix) -- the h=3 span, without a Groebner basis.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

At h = 2 every component of the cap error lies in W_2 = Sym^2 (x) Sym^2 and
kappa_c^2 lies in W_2, so a generic six-site source is split-blocked at every
pair.  This script tests the same two statements at N = 8 (h = 3) using exact
linear algebra only:

 (i)  is every one of the 729 cubic components in W_3 = Sym^3 (x) Sym^3
      (dim 100 of the 165 cubics)?
 (ii) does a degree-3 L-monomial (the plan's pattern list at h = 3) lie in the
      degree-3 part of the error ideal, i.e. in the span of those components?

A positive answer to (ii) is a complete blocking certificate at that pair.

Usage: python3 appendix_n8_span.py [--sources 3]
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations_with_replacement
import json
import random
import time

from appendix_n8_h3 import (SITES8, error_cubics, in_sym_cube, random_blocks)
from wsplit_core import KAPPA_VARS, NVAR, lin_zero, require

CUBIC_KEYS = tuple(combinations_with_replacement(range(NVAR), 3))  # 165
CUBIC_INDEX = {key: index for index, key in enumerate(CUBIC_KEYS)}


def vector(cubic):
    out = [Fraction(0)] * len(CUBIC_KEYS)
    for key, value in cubic.items():
        out[CUBIC_INDEX[key]] = value
    return out


def row_reduce(vectors):
    basis, pivots = [], []
    for raw in vectors:
        row = list(raw)
        for pivot, brow in zip(pivots, basis):
            if row[pivot] != 0:
                factor = row[pivot] / brow[pivot]
                row = [a - factor * b for a, b in zip(row, brow)]
        pivot = next((n for n, value in enumerate(row) if value != 0), None)
        if pivot is None:
            continue
        basis.append(row)
        pivots.append(pivot)
    return pivots, basis


def in_span(pivots, basis, raw):
    row = list(raw)
    for pivot, brow in zip(pivots, basis):
        if row[pivot] != 0:
            factor = row[pivot] / brow[pivot]
            row = [a - factor * b for a, b in zip(row, brow)]
    return all(value == 0 for value in row)


def lin_from_matrix(matrix):
    return [matrix[i][j] for i in range(3) for j in range(3)]


def monomial_cubic(forms, combo):
    """Product of three linear forms as a cubic dict."""
    product = {(): Fraction(1)}
    for index in combo:
        form = forms[index]
        new = {}
        for key, value in product.items():
            for var in range(NVAR):
                if form[var] == 0:
                    continue
                nkey = tuple(sorted(key + (var,)))
                new[nkey] = new.get(nkey, Fraction(0)) + value * form[var]
        product = new
    return {key: value for key, value in product.items() if value != 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=int, default=3)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--out", default="results_n8_span.json")
    args = parser.parse_args()
    results = []
    for index in range(args.sources):
        rng = random.Random(90000 + args.offset + index)
        blocks = random_blocks(rng)
        start = time.time()
        s_form, cubics = error_cubics(blocks, 0, 1)
        outside = sum(1 for cubic in cubics if not in_sym_cube(cubic))
        build = time.time() - start
        start = time.time()
        pivots, basis = row_reduce(vector(cubic) for cubic in cubics)
        forms = [s_form]
        for colour in range(3):
            form = lin_zero()
            form[KAPPA_VARS[colour]] = Fraction(1)
            forms.append(form)
        names = ("s", "kappa_0", "kappa_1", "kappa_2")
        found = []
        for combo in combinations_with_replacement(range(4), 3):
            product = monomial_cubic(forms, combo)
            if in_span(pivots, basis, vector(product)):
                found.append("*".join(names[i] for i in combo))
        record = {
            "seed": 90000 + args.offset + index,
            "components": len(cubics),
            "components_outside_Sym3": outside,
            "span_dimension": len(basis),
            "dim_Sym3_tensor_Sym3": 100,
            "dim_all_cubics": len(CUBIC_KEYS),
            "degree3_patterns_in_span": found,
            "build_seconds": round(build, 1),
            "linear_algebra_seconds": round(time.time() - start, 1),
        }
        results.append(record)
        print(json.dumps(record), flush=True)
    with open(args.out, "w") as handle:
        json.dump(results, handle, indent=1)


if __name__ == "__main__":
    main()
