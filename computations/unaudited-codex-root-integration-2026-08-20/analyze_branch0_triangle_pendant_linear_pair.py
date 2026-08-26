#!/usr/bin/env python3
"""Exact coefficient-minor census for the reduced triangle+pendant chart.

This is a discovery helper, not a closure certificate.  It imports the
source-faithful Laurent reduction, substitutes the exact relation
``d3=-b1*d4-b0*d5``, and regards every remaining source row as a linear
equation in ``a4,a5``.  It reports coefficient-minor factors without dumping
the usually large factors themselves.
"""

from __future__ import annotations

from functools import reduce
import argparse
import importlib.util
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REDUCTION = (HERE.parent /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "discover_branch0_triangle_pendant_reduction.py")


def load(path: Path):
    spec = importlib.util.spec_from_file_location("root_tp_reduction", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load(REDUCTION)
C = D.CHART
SYMBOLS = sp.symbols(" ".join(C.names))
A4, A5 = SYMBOLS[4], SYMBOLS[5]
PARAMETERS = (SYMBOLS[6], SYMBOLS[7], SYMBOLS[9],
              SYMBOLS[C.d_index[4]], SYMBOLS[C.d_index[5]])


def expression(poly):
    return sp.expand(sum(
        sp.Rational(value.numerator, value.denominator)
        * sp.prod(symbol ** power
                  for symbol, power in zip(SYMBOLS, monomial))
        for monomial, value in poly.items()
    ))


def primitive(poly):
    value = sp.Poly(sp.expand(poly), *PARAMETERS)
    return sp.primitive(value)[1].as_expr()


def factor_signature(poly):
    coefficient, factors = sp.factor_list(primitive(poly), *PARAMETERS)
    return {
        "terms": len(sp.Poly(poly, *PARAMETERS).terms()),
        "total_degree": sp.Poly(poly, *PARAMETERS).total_degree(),
        "factors": [
            (len(sp.Poly(factor, *PARAMETERS).terms()),
             sp.Poly(factor, *PARAMETERS).total_degree(), multiplicity)
            for factor, multiplicity in factors
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", nargs=2, type=int)
    args = parser.parse_args()
    rows, _, _, _ = D.solve_full_chain_use_e()
    decomposed = []
    for label, raw in rows:
        value = expression(raw)
        polynomial = sp.Poly(value, A4, A5)
        if polynomial.total_degree() > 1:
            raise RuntimeError(f"row {label} is nonlinear in a4,a5")
        u = sp.expand(value.coeff(A4))
        v = sp.expand(value.coeff(A5))
        w = sp.expand(value.subs({A4: 0, A5: 0}))
        if sp.expand(value - u*A4 - v*A5 - w) != 0:
            raise RuntimeError(f"row {label} decomposition failed")
        decomposed.append((label, u, v, w))

    minors = []
    nonzero = []
    for left_index, left in enumerate(decomposed):
        for right in decomposed[left_index + 1:]:
            determinant = sp.expand(left[1]*right[2] - right[1]*left[2])
            if determinant == 0:
                continue
            determinant = primitive(determinant)
            nonzero.append(determinant)
            signature = factor_signature(determinant)
            score = (max((terms for terms, _, _ in signature["factors"]),
                         default=0),
                     signature["terms"], signature["total_degree"])
            minors.append((score, left[0], right[0], signature))

    gcd = reduce(lambda x, y: sp.gcd(sp.Poly(x, *PARAMETERS),
                                      sp.Poly(y, *PARAMETERS)).as_expr(),
                 nonzero)
    print("row_labels:", [label for label, *_ in decomposed])
    print("parameter_names:", [str(symbol) for symbol in PARAMETERS])
    print("nonzero_minor_count:", len(minors))
    print("all_minor_gcd:", sp.factor(gcd))
    print("best_minor_signatures:")
    for score, left, right, signature in sorted(minors)[:20]:
        print(left, right, score, signature)
    if args.pair:
        left_label, right_label = args.pair
        row_map = {label: (u, v, w) for label, u, v, w in decomposed}
        left, right = row_map[left_label], row_map[right_label]
        determinant = primitive(left[0]*right[1] - right[0]*left[1])
        print("selected_pair:", left_label, right_label)
        print("selected_determinant_factorization:", sp.factor(determinant))
        a4_numerator = sp.expand(left[1]*right[2] - right[1]*left[2])
        a5_numerator = sp.expand(right[0]*left[2] - left[0]*right[2])
        print("a4_numerator_signature:", factor_signature(a4_numerator))
        print("a5_numerator_signature:", factor_signature(a5_numerator))


if __name__ == "__main__":
    main()
