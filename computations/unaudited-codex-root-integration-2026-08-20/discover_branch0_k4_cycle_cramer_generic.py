#!/usr/bin/env python3
"""Cramer/Schur discovery probe for one generic k4-cycle branch.

This derives the p_e=a_e*d_e interface from the literal source, solves the
four upper cofactor rows, then solves Cof(5,0) for a0 and t023 for a5.  The
result is five compatibility numerators in the six Laurent parameters
``b0,b1,b3,d1,d3,d4``.

The probe is restricted to the branch where all Cramer/solve denominators
are nonzero.  Its complement must be treated separately, so even an exact
UNIT here is not by itself a full k4-cycle theorem.
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
PCOORDS = (HERE.parent /
           "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
           "probe_branch0_cycle_pcoords.py")


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_pcoords", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(PCOORDS)
SYMBOLS = sp.symbols(" ".join(SOURCE.NAMES))
P = SYMBOLS[:4]
A0, A5 = SYMBOLS[4:6]
PARAMETERS = SYMBOLS[6:]


def expression(poly):
    return sp.expand(sum(
        sp.Rational(coefficient.numerator, coefficient.denominator)
        * sp.prod(variable ** power
                  for variable, power in zip(SYMBOLS, monomial))
        for monomial, coefficient in poly.items()
    ))


def numerator(poly, substitutions):
    return sp.expand(sp.together(poly.subs(substitutions))
                     .as_numer_denom()[0])


def derive():
    rows = {label: expression(poly)
            for label, poly, _ in SOURCE.data()[0]}
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    matrix, _ = sp.linear_eq_to_matrix(upper, P)
    delta = PARAMETERS[1] * PARAMETERS[4] \
        + PARAMETERS[2] * PARAMETERS[3] * PARAMETERS[5]
    expected = (4 * PARAMETERS[0] ** 2 * PARAMETERS[1] * PARAMETERS[2]
                * PARAMETERS[3] * PARAMETERS[4] * PARAMETERS[5]
                * delta ** 2)
    if sp.expand(matrix.det() - expected) != 0:
        raise RuntimeError("upper Cramer determinant changed")
    p_solution = sp.solve(upper, P, dict=True, simplify=False)[0]
    labels = ("t_012", "t_013", "cofactor_5_0", "t_023",
              "t_123", "cofactor_0_0", "cofactor_0_3")
    residual = {label: numerator(rows[label], p_solution)
                for label in labels}
    a0_solution = sp.solve(residual["cofactor_5_0"], A0,
                           dict=True, simplify=False)[0]
    residual = {label: numerator(poly, a0_solution)
                for label, poly in residual.items()
                if label != "cofactor_5_0"}
    a5_solution = sp.solve(residual["t_023"], A5,
                           dict=True, simplify=False)[0]
    compatibility = []
    for label in ("t_012", "t_013", "t_123",
                  "cofactor_0_0", "cofactor_0_3"):
        poly = numerator(residual[label], a5_solution)
        # The last three acquire an extraneous Cramer denominator factor.
        while sp.rem(sp.Poly(poly, *PARAMETERS),
                     sp.Poly(delta, *PARAMETERS)) == 0:
            poly = sp.cancel(poly / delta)
        compatibility.append((label, sp.expand(poly)))

    factors = list(PARAMETERS) + [delta,
        PARAMETERS[3] * PARAMETERS[5] + PARAMETERS[4],
        PARAMETERS[1] + PARAMETERS[3]]
    # p_i and 1+p_i must remain nonzero in the true interior.
    for variable in P:
        value = sp.cancel(p_solution[variable])
        top, bottom = value.as_numer_denom()
        factors += [sp.expand(top), sp.expand(top + bottom)]
    unique = []
    seen = set()
    for factor in factors:
        primitive = sp.primitive(sp.Poly(factor, *PARAMETERS))[1].as_expr()
        key = str(primitive)
        if key in seen or str(-primitive) in seen:
            continue
        seen.add(key)
        unique.append(sp.expand(primitive))
    return compatibility, unique


def singular(poly):
    return str(sp.expand(poly)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--lift", action="store_true")
    parser.add_argument("--product-localizer", action="store_true")
    parser.add_argument("--no-localizers", action="store_true")
    parser.add_argument("--power-bound", type=int, default=0)
    parser.add_argument("--sequential-saturation", action="store_true")
    parser.add_argument("--reverse-saturation", action="store_true")
    args = parser.parse_args()
    compatibility, factors = derive()
    generators = [singular(poly) for _, poly in compatibility]
    if args.no_localizers:
        inverse = ()
    elif args.product_localizer:
        inverse = (sp.Symbol("z"),)
        product = "*".join(f"({singular(factor)})" for factor in factors)
        generators.append(f"z*{product}-1")
    else:
        inverse = tuple(sp.Symbol(f"z{index}")
                        for index in range(len(factors)))
        generators += [f"z{index}*({singular(factor)})-1"
                       for index, factor in enumerate(factors)]
    variables = PARAMETERS + inverse
    prefix = (f"ring R={args.characteristic},"
              f"({','.join(map(str, variables))}),dp;"
              f"ideal I={','.join(generators)};")
    if args.sequential_saturation:
        body = 'LIB "elim.lib";ideal J=I;'
        saturation_factors = list(reversed(factors)) \
            if args.reverse_saturation else factors
        for index, factor in enumerate(saturation_factors):
            body += (f'J=sat(J,ideal({singular(factor)}))[1];'
                     f'print("SAT {index}");print(size(J));'
                     'print(dim(std(J)));')
        body += ('ideal G=std(J);print("BEGIN");'
                 'print(string(reduce(1,G)));print(size(G));print(dim(G));'
                 'print("END");quit;')
    elif args.lift:
        body = (
            "matrix L;ideal G=liftstd(I,L);"
            'print("BEGIN");print(size(G));print(string(G[1]));print(dim(G));'
            "for(int i=1;i<=nrows(L);i++){if(L[i,1]!=0){"
            'print("ACTIVE");print(i);print(deg(L[i,1]));'
            'print(size(L[i,1]));}};print("END");quit;'
        )
    else:
        body = (
            "ideal G=slimgb(I);"
            'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
            'print(dim(G));'
        )
        if args.power_bound:
            product = "*".join(f"({singular(factor)})"
                               for factor in factors)
            for power in range(1, args.power_bound + 1):
                body += (f'print("POWER {power}");'
                         f'print(string(reduce(({product})^{power},G)));')
        body += 'print("END");quit;'
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", prefix + body],
            text=True, capture_output=True, timeout=args.timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT after {time.monotonic() - started:.3f}s")
        return
    print(f"elapsed_seconds: {time.monotonic() - started:.3f}")
    print("compatibility:", [label for label, _ in compatibility])
    print("localized_factor_count:", len(factors))
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
