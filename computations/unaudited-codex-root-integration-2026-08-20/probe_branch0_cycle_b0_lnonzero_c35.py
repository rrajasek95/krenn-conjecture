#!/usr/bin/env python3
"""Discovery probe for the C35 half of the frozen cycle resultant tree.

This deliberately rederives the literal-source specialization used by the
independent frozen L!=0 audit.  It exposes either the common resultant
factor S13 or the intersection of the two distinct resultant factors, and
can ask an exact characteristic-zero factorizing-basis question after a
chosen live constraint.  UNIT output is discovery until separately audited.
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
C9_PATH = HERE / "probe_branch0_cycle_b0_lnonzero_c9_factor.py"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c35_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(C9_PATH)


def derive():
    variables, f, g, c9, named, unused, live = P.derive()
    raw_rows, _ = P.SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: P.SOURCE.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = P.SOURCE.A0, P.SOURCE.A5
    b0, b1, b3, d1, d3, d4 = P.SOURCE.PARAMETERS
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, P.SOURCE.P, dict=True, simplify=False)[0]
    base = {b1: -d1, d3: d4*(d1+1)/(d1-1)}
    base.update(sp.solve(sp.cancel(rows["cofactor_5_0"]
                                   .subs(p_solution).subs(base)),
                         a0, dict=True, simplify=False)[0])
    t5 = (2*a5*d1**2*d4-2*b0*d1**2+2*b0*d1+d1**2*d4+d4)
    base.update(sp.solve(t5, a5, dict=True, simplify=False)[0])
    top00 = sp.cancel(rows["cofactor_0_0"].subs(p_solution)
                      .subs(base)).as_numer_denom()[0]
    core00 = max((factor for factor, _ in sp.factor_list(top00)[1]),
                 key=lambda value: len(sp.Poly(value, b3).terms()))
    base[b3] = sp.solve(core00, b3, dict=True, simplify=False)[0][b3]

    rational_field, _, _, _ = P.field("b0,d1,d4", P.QQ)
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(base))) for variable in P.SOURCE.P]
    values += [rational_field.from_expr(sp.cancel(base[a0].subs(base))),
               rational_field.from_expr(sp.cancel(base[a5].subs(base)))]
    values += [rational_field.from_expr(sp.cancel(base.get(variable, variable)))
               for variable in P.SOURCE.PARAMETERS]

    def evaluate(poly):
        answer = rational_field.zero
        for exponent, coefficient in poly.items():
            term = rational_field.from_expr(sp.Rational(
                coefficient.numerator, coefficient.denominator))
            for value, power in zip(values, exponent):
                term *= value**power
            answer += term
        return answer.numer.as_expr()

    cparts = sorted((factor for factor, _ in sp.factor_list(
        evaluate(raw["cofactor_0_3"]))[1]
                     if len(sp.Poly(factor, *variables).terms()) > 2),
                    key=lambda value: len(sp.Poly(value, *variables).terms()))
    c35 = cparts[1]
    rf = sp.resultant(f, c35, b0)
    rg = sp.resultant(g, c35, b0)
    factor_f = sp.factor_list(rf)[1]
    factor_g = sp.factor_list(rg)[1]
    shared = next(factor for factor, _ in sp.factor_list(sp.gcd(
        sp.Poly(rf, d1, d4), sp.Poly(rg, d1, d4)).as_expr())[1]
                  if len(sp.Poly(factor, d1, d4).terms()) == 13)
    distinct_f = next(factor for factor, _ in factor_f
                      if len(sp.Poly(factor, d1, d4).terms()) == 140)
    distinct_g = next(factor for factor, _ in factor_g
                      if len(sp.Poly(factor, d1, d4).terms()) == 136)
    return variables, f, g, c35, shared, distinct_f, distinct_g, unused, live


def singular(value):
    return str(sp.expand(value)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", choices=("shared", "distinct"),
                        required=True)
    parser.add_argument("--factor",
                        choices=("none", "qplus", "qi", "qfour",
                                 "q24", "q153"), default="none")
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--constraint", default="all")
    parser.add_argument("--lower", default="all")
    parser.add_argument("--timeout", type=float, default=240)
    args = parser.parse_args()
    started = time.monotonic()
    variables, f, g, c35, shared, df, dg, unused, live = derive()
    generators = [f, g, c35]
    if args.branch == "shared":
        generators.append(shared)
    else:
        generators.extend((df, dg))
        low_factors = {
            "qplus": variables[1]**2 + 2*variables[1] - 1,
            "qi": variables[1]**2 + 1,
            "qfour": (variables[1]**4 + 2*variables[1]**3
                      + 6*variables[1]**2 - 2*variables[1] + 1),
        }
        if args.factor in ("q24", "q153"):
            target_degree = int(args.factor[1:])
            univariate = sp.factor_list(sp.resultant(
                df, dg, variables[2]))[1]
            low_factors[args.factor] = next(
                factor for factor, _ in univariate
                if sp.degree(factor, variables[1]) == target_degree)
        if args.factor != "none":
            generators.append(low_factors[args.factor])
    scan_lower = args.lower == "scan"
    reduce_lower = args.lower == "remainders"
    reduce_live = args.lower == "live_remainders"
    if args.lower == "all":
        generators.extend(value for _, value in unused)
    elif args.lower == "c34":
        generators.extend(value for name, value in unused
                          if name in ("cofactor_3_3", "cofactor_4_3"))
    elif args.lower not in ("none", "scan", "remainders",
                            "live_remainders"):
        generators.extend(value for name, value in unused
                          if name == args.lower)
    live_map = dict(live)
    scan_live = args.constraint == "scan"
    if args.constraint == "none":
        constraints = []
    elif args.constraint == "all":
        constraints = [value for _, value in live]
    elif args.constraint == "LH":
        constraints = [live_map["L"], live_map["H"]]
    elif scan_live:
        constraints = []
    else:
        if args.constraint not in live_map:
            raise RuntimeError(f"unknown constraint {args.constraint}; "
                               f"choices={sorted(live_map)}")
        constraints = [live_map[args.constraint]]
    ring = f"ring R={args.characteristic},({','.join(map(str, variables))}),dp;"
    ideal = f"ideal I={','.join(singular(value) for value in generators)};"
    if scan_live:
        body = ""
        for index, (name, value) in enumerate(live):
            body += (f"ideal C{index}=ideal({singular(value)});"
                     f"list L{index}=facstd(I,C{index});"
                     f'print("LIVE {name}");print(size(L{index}));')
        command = ring+ideal+'print("BEGIN");'+body+'print("END");quit;'
    elif reduce_live:
        if not constraints:
            raise RuntimeError("live remainders require a nonzero constraint")
        body = ""
        for index, (name, value) in enumerate(live):
            body += (f'print("LIVE {name}");'
                     f"print(size(reduce({singular(value)},G)));")
        command = (ring+ideal+
                   f"ideal C={','.join(singular(x) for x in constraints)};"+
                   'list L=facstd(I,C);print("BEGIN");print(size(L));'
                   'ideal G=std(L[1]);'+body+'print("END");quit;')
    elif reduce_lower:
        if not constraints:
            raise RuntimeError("lower remainders require a nonzero constraint")
        body = ""
        for index, (name, value) in enumerate(unused):
            body += (f'print("LOWER {name}");'
                     f"print(reduce({singular(value)},G));")
        command = (ring+ideal+
                   f"ideal C={','.join(singular(x) for x in constraints)};"+
                   'list L=facstd(I,C);print("BEGIN");print(size(L));'
                   'ideal G=std(L[1]);'+body+'print("END");quit;')
    elif scan_lower:
        if not constraints:
            raise RuntimeError("lower scan requires a nonzero constraint")
        body = ""
        for index, (name, value) in enumerate(unused):
            body += (f"ideal J{index}=I+ideal({singular(value)});"
                     f"list L{index}=facstd(J{index},C);"
                     f'print("LOWER {name}");print(size(L{index}));')
        command = (ring+ideal+
                   f"ideal C={','.join(singular(x) for x in constraints)};"+
                   'print("BEGIN");'+body+'print("END");quit;')
    elif constraints:
        command = (ring+ideal+f"ideal C={','.join(singular(x) for x in constraints)};"
                   'list L=facstd(I,C);print("BEGIN");print(size(L));'
                   'for(int j=1;j<=size(L);j++){print(size(L[j]));'
                   'print(dim(std(L[j])));};print("END");quit;')
    else:
        command = (ring+ideal+'list L=facstd(I);print("BEGIN");print(size(L));'
                   'for(int j=1;j<=size(L);j++){print(size(L[j]));'
                   'print(dim(std(L[j])));};print("END");quit;')
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"{args.branch}: TIMEOUT after {time.monotonic()-started:.3f}s")
        return
    print("branch:", args.branch)
    print("factor:", args.factor)
    print("core terms:", [len(sp.Poly(x, *variables).terms())
                           for x in (f, g, c35)])
    print("eliminant terms:", len(sp.Poly(shared, variables[1], variables[2]).terms()),
          len(sp.Poly(df, variables[1], variables[2]).terms()),
          len(sp.Poly(dg, variables[1], variables[2]).terms()))
    print("elapsed_seconds:", time.monotonic()-started)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
