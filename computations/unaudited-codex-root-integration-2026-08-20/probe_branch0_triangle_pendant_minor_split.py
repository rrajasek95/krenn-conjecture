#!/usr/bin/env python3
"""Discovery probe for the best a4/a5 minor split in triangle+pendant.

The source-faithful localized chain leaves equations linear in ``a4,a5``.
Rows 7 and 12 have determinant ``unit * P`` on the live chart, with a
26-term primitive factor P.  This probe tests the two exhaustive branches
P!=0 (Cramer substitution) and P=0 (unsolved linear system).

Only an exact characteristic-zero UNIT together with a replayable lift would
be a theorem.  Finite-field statuses are discovery evidence only.
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
    spec = importlib.util.spec_from_file_location("root_tp_minor_reduction", path)
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


def expression(poly):
    return sp.expand(sum(
        sp.Rational(value.numerator, value.denominator)
        * sp.prod(symbol ** power
                  for symbol, power in zip(ALL, monomial))
        for monomial, value in poly.items()
    ))


def numerator(value):
    return sp.expand(sp.cancel(value).as_numer_denom()[0])


def primitive(value, variables):
    return sp.primitive(sp.Poly(sp.expand(value), *variables))[1].as_expr()


def strip_live_parameter_factors(value):
    """Remove factors already inverted throughout the current chart."""
    value = primitive(value, PARAMETERS)
    polynomial = sp.Poly(value, *PARAMETERS)
    minima = [min(monomial[index] for monomial, _ in polynomial.terms())
              for index in range(len(PARAMETERS))]
    monomial = sp.prod(variable ** power
                       for variable, power in zip(PARAMETERS, minima))
    value = sp.cancel(value / monomial)
    live_d3 = B1*D4+B0*D5
    while sp.rem(sp.Poly(value, *PARAMETERS),
                 sp.Poly(live_d3, *PARAMETERS)) == 0:
        value = sp.cancel(value / live_d3)
    return primitive(value, PARAMETERS)


def derive():
    rows, _, live, _ = D.solve_full_chain_use_e()
    row_map = {label: expression(poly) for label, poly in rows}

    def coefficients(value):
        u = sp.expand(value.coeff(A4))
        v = sp.expand(value.coeff(A5))
        w = sp.expand(value.subs({A4: 0, A5: 0}))
        assert sp.expand(value - u*A4 - v*A5 - w) == 0
        return u, v, w

    left = coefficients(row_map[7])
    right = coefficients(row_map[12])
    determinant = sp.expand(left[0]*right[1] - right[0]*left[1])
    factor_list = sp.factor_list(primitive(determinant, PARAMETERS), *PARAMETERS)[1]
    nonunit = [factor for factor, multiplicity in factor_list
               for _ in range(multiplicity)
               if len(sp.Poly(factor, *PARAMETERS).terms()) > 2]
    if len(nonunit) != 1:
        raise RuntimeError(f"expected one nonmonomial split factor, got {nonunit}")
    split = sp.expand(nonunit[0])

    # Cramer's rule for u*a4+v*a5=-w.
    a4_value = sp.cancel((left[1]*right[2] - right[1]*left[2]) / determinant)
    a5_value = sp.cancel((right[0]*left[2] - left[0]*right[2]) / determinant)
    compatibility = []
    seen = set()
    for label, value in row_map.items():
        if label in (7, 12):
            continue
        reduced = strip_live_parameter_factors(numerator(value.subs(
            {A4: a4_value, A5: a5_value})))
        if reduced == 0:
            continue
        encoded = str(reduced)
        if encoded in seen or str(-reduced) in seen:
            continue
        seen.add(encoded)
        compatibility.append((label, reduced))

    live_factors = [B0, B1, B3, D4, D5, B1*D4+B0*D5]
    for index in (2, 3):
        live_factors.append(primitive(numerator(expression(live[index])),
                                      (A4, A5) + PARAMETERS))
    live_factors += [A4, A5]
    generic_live = [primitive(numerator(factor.subs({A4: a4_value,
                                                     A5: a5_value})), PARAMETERS)
                    for factor in live_factors]
    return row_map, split, compatibility, generic_live, live_factors


def singular(value):
    return str(sp.expand(value)).replace("**", "^")


def run(branch, characteristic, timeout, algorithm):
    row_map, split, compatibility, generic_live, boundary_live = derive()
    if branch == "generic":
        variables = PARAMETERS
        generators = [value for _, value in compatibility]
        live = generic_live + [split]
    else:
        variables = (A4, A5) + PARAMETERS
        generators = list(row_map.values()) + [split]
        live = boundary_live
    # Keep localizers separate: expanding their product creates a needlessly
    # enormous input polynomial and destroys the intended reduction.
    unique_live = []
    seen_live = set()
    for factor in live:
        factor = primitive(factor, variables)
        encoded = str(factor)
        if encoded in seen_live or str(-factor) in seen_live:
            continue
        seen_live.add(encoded)
        unique_live.append(factor)
    live = unique_live
    if algorithm == "facstd":
        names = tuple(map(str, variables))
        generators_string = ",".join(singular(value)
                                     for value in generators)
        constraints = ",".join(singular(factor) for factor in live)
        command = (
            f"ring R={characteristic},({','.join(names)}),dp;"
            f"ideal I={generators_string};ideal C={constraints};"
            "list L=facstd(I,C);"
            'print("BEGIN");print(size(L));'
            'for(int j=1;j<=size(L);j++){print(size(L[j]));'
            'print(dim(std(L[j])));};print("END");quit;')
    else:
        inverse_names = tuple(f"z{index}" for index in range(len(live)))
        names = tuple(map(str, variables)) + inverse_names
        generators_string = ",".join(
            [singular(value) for value in generators]
            + [f"z{index}*({singular(factor)})-1"
               for index, factor in enumerate(live)])
        command = (
            f"ring R={characteristic},({','.join(names)}),dp;"
            f"ideal I={generators_string};ideal G={algorithm}(I);"
            'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
            'print(dim(G));print("END");quit;')
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"{branch}: TIMEOUT after {time.monotonic()-started:.3f}s")
        return
    print(f"{branch}: elapsed {time.monotonic()-started:.3f}s")
    print("split_terms_degree:", len(sp.Poly(split, *PARAMETERS).terms()),
          sp.Poly(split, *PARAMETERS).total_degree())
    print("generator_count:", len(generators), "live_factor_count:", len(live))
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", choices=("generic", "boundary"), required=True)
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--algorithm", choices=("slimgb", "std", "facstd"),
                        default="slimgb")
    args = parser.parse_args()
    run(args.branch, args.characteristic, args.timeout, args.algorithm)


if __name__ == "__main__":
    main()
