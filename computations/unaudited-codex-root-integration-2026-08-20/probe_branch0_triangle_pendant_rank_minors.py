#!/usr/bin/env python3
"""Determinantal elimination probe for branch-0 triangle+pendant.

After the exact Laurent chain and E substitution every remaining literal row
has the form ``u*a4+v*a5+w``.  Existence of ``a4,a5`` therefore forces every
3x3 minor of the coefficient matrix ``[u v w]`` to vanish.  This probe forms
that necessary five-parameter ideal and tests it after localizing only the
denominators used by the exact chain.  If it is the unit ideal over Q, that
is a sound (indeed stronger) emptiness proof; modular output is discovery
only.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import time

import sympy as sp


HERE = Path(__file__).resolve().parent
REDUCTION = (HERE.parent /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "discover_branch0_triangle_pendant_reduction.py")


def load(path: Path):
    spec = importlib.util.spec_from_file_location("root_tp_rank_reduction", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load(REDUCTION)
C = D.CHART
ALL = sp.symbols(" ".join(C.names))
A4, A5 = ALL[4], ALL[5]
B0, B1, B3 = ALL[6], ALL[7], ALL[9]
D4, D5 = ALL[C.d_index[4]], ALL[C.d_index[5]]
PARAMETERS = (B0, B1, B3, D4, D5)
LIVE_D3 = B1*D4+B0*D5


def expression(poly):
    return sp.expand(sum(
        sp.Rational(value.numerator, value.denominator)
        * sp.prod(symbol ** power
                  for symbol, power in zip(ALL, monomial))
        for monomial, value in poly.items()
    ))


def primitive(value):
    return sp.primitive(sp.Poly(sp.expand(value), *PARAMETERS))[1].as_expr()


def strip_live(value):
    value = primitive(value)
    polynomial = sp.Poly(value, *PARAMETERS)
    minima = [min(monomial[index] for monomial, _ in polynomial.terms())
              for index in range(len(PARAMETERS))]
    value = sp.cancel(value / sp.prod(
        variable ** power for variable, power in zip(PARAMETERS, minima)))
    while sp.rem(sp.Poly(value, *PARAMETERS),
                 sp.Poly(LIVE_D3, *PARAMETERS)) == 0:
        value = sp.cancel(value / LIVE_D3)
    return primitive(value)


def derive():
    rows, _, _, _ = D.solve_full_chain_use_e()
    coefficient_rows = []
    for label, raw in rows:
        value = expression(raw)
        u = sp.expand(value.coeff(A4))
        v = sp.expand(value.coeff(A5))
        w = sp.expand(value.subs({A4: 0, A5: 0}))
        assert sp.expand(value-u*A4-v*A5-w) == 0
        coefficient_rows.append((label, (u, v, w)))
    return coefficient_rows


def singular(value):
    return str(sp.expand(value)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=240)
    parser.add_argument("--algorithm", choices=("slimgb", "std", "facstd"),
                        default="slimgb")
    args = parser.parse_args()
    started = time.monotonic()
    rows = derive()
    print("derive_seconds:", time.monotonic()-started)
    print("coefficient_rows:", len(rows), "formal_minor_count:",
          len(list(__import__('itertools').combinations(rows, 3))))

    live = (B0, B1, B3, D4, D5, LIVE_D3)
    matrix_entries = ",".join(
        singular(value) for _, row in rows for value in row)
    names = ",".join(map(str, PARAMETERS))
    if args.algorithm == "facstd":
        constraints = ",".join(singular(value) for value in live)
        command = (f"ring R={args.characteristic},({names}),dp;"
                   f"matrix M[{len(rows)}][3]={matrix_entries};"
                   f"ideal I=minor(M,3);ideal C={constraints};"
                   "list L=facstd(I,C);"
                   'print("BEGIN");print(size(L));'
                   'for(int j=1;j<=size(L);j++){print(size(L[j]));'
                   'print(dim(std(L[j])));};print("END");quit;')
    else:
        inverse = tuple(f"z{index}" for index in range(len(live)))
        names = ",".join(tuple(map(str, PARAMETERS)) + inverse)
        localizers = ",".join(
            f"z{index}*({singular(value)})-1"
            for index, value in enumerate(live))
        command = (f"ring R={args.characteristic},({names}),dp;"
                   f"matrix M[{len(rows)}][3]={matrix_entries};"
                   f"ideal I=minor(M,3);I=I+ideal({localizers});"
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
