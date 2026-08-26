#!/usr/bin/env python3
"""Exact discovery probe for one univariate factor of the C9 residual tree.

The interface is rederived from literal sparse source rows exactly as in the
frozen L!=0 audit.  For a selected univariate resultant factor, this adds all
five still-unused lower cofactor rows and asks for an exact-Q unit.  A UNIT is
useful discovery but still needs a compact replay/minimization audit.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import time

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.fields import field


HERE = Path(__file__).resolve().parent
GENERIC = HERE / "discover_branch0_k4_cycle_cramer_generic.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("root_cycle_c9_source", GENERIC)


def derive():
    raw_rows, raw_hafnian = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, SOURCE.P, dict=True, simplify=False)[0]
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

    rational_field, _, _, _ = field("b0,d1,d4", QQ)
    values = [rational_field.from_expr(sp.cancel(
        p_solution[variable].subs(base))) for variable in SOURCE.P]
    values += [rational_field.from_expr(sp.cancel(base[a0].subs(base))),
               rational_field.from_expr(sp.cancel(base[a5].subs(base)))]
    values += [rational_field.from_expr(sp.cancel(base.get(variable, variable)))
               for variable in SOURCE.PARAMETERS]

    def evaluate(poly):
        answer = rational_field.zero
        for exponent, coefficient in poly.items():
            term = rational_field.from_expr(sp.Rational(
                coefficient.numerator, coefficient.denominator))
            for value, power in zip(values, exponent):
                term *= value**power
            answer += term
        return answer.numer.as_expr()

    f = max((factor for factor, _ in sp.factor_list(evaluate(raw["t_012"]))[1]),
            key=lambda value: len(sp.Poly(value, b0, d1, d4).terms()))
    g = max((factor for factor, _ in sp.factor_list(evaluate(raw["t_013"]))[1]),
            key=lambda value: len(sp.Poly(value, b0, d1, d4).terms()))
    cparts = sorted((factor for factor, _ in
                     sp.factor_list(evaluate(raw["cofactor_0_3"]))[1]
                     if len(sp.Poly(factor, b0, d1, d4).terms()) > 2),
                    key=lambda value: len(sp.Poly(value, b0, d1, d4).terms()))
    c9 = cparts[0]
    rf = sp.resultant(f, c9, b0)
    rg = sp.resultant(g, c9, b0)
    bigf = max((factor for factor, _ in sp.factor_list(rf)[1]),
               key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    bigg = max((factor for factor, _ in sp.factor_list(rg)[1]),
               key=lambda value: len(sp.Poly(value, d1, d4).terms()))
    univariate = sp.factor_list(sp.resultant(bigf, bigg, d4))[1]
    named = {
        "qplus": d1**2+2*d1-1,
        "qa": d1**3+d1**2+3*d1-1,
        "qfour": d1**4+6*d1**2+1,
        "deg34": next(factor for factor, _ in univariate
                      if sp.degree(factor, d1) == 34),
    }
    unused = [(label, evaluate(raw[label])) for label in
              ("cofactor_1_3", "cofactor_2_3", "cofactor_3_3",
               "cofactor_4_3", "cofactor_5_3")]
    # Complete nonvanishing contract of the true interior chart.  Only
    # numerators matter because all displayed rational denominators are
    # listed as constraints as well.
    l_factor = (2*b0*d1**2-2*b0*d1
                - d4*(d1**3+3*d1**2-d1+1))
    m_factor = (2*b0*d1**4-2*b0*d1**2-d1**4*d4-2*d1**4
                -2*d1**3*d4-2*d1**3-4*d1**2*d4+6*d1**2
                -2*d1*d4-2*d1+d4)
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    kplus = b3*d1-b3+d1+1
    live = [("b0", b0), ("d1", d1), ("d4", d4),
            ("d1m1", d1-1), ("d1p1", d1+1),
            ("L", l_factor), ("M", m_factor)]
    for name, value in (("Delta", delta), ("D0", d0), ("Kplus", kplus)):
        live.append((name, sp.cancel(value.subs(base)).as_numer_denom()[0]))
    for index, variable in enumerate(SOURCE.P, 1):
        value = sp.cancel(p_solution[variable].subs(base))
        top, bottom = value.as_numer_denom()
        live.extend(((f"p{index}", top), (f"onep{index}", top+bottom)))
    live.append(("H", evaluate(raw_hafnian)))
    live = [(name, sp.expand(value)) for name, value in live
            if sp.expand(value) not in (1, -1)]
    return (b0, d1, d4), f, g, c9, named, unused, live


def singular(value):
    return str(sp.expand(value)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor", choices=("qplus", "qa", "qfour", "deg34"),
                        required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=240)
    parser.add_argument("--localized", action="store_true")
    parser.add_argument("--lower", default="all",
                        choices=("all", "none", "cofactor_1_3", "cofactor_2_3",
                                 "cofactor_3_3", "cofactor_4_3",
                                 "cofactor_5_3"))
    parser.add_argument("--live", default="all")
    args = parser.parse_args()
    started = time.monotonic()
    variables, f, g, c9, named, unused, live = derive()
    if args.live == "all":
        selected_live = [value for _, value in live]
    elif args.live == "scan":
        selected_live = []
    else:
        selected_live = [value for name, value in live if name == args.live]
        if not selected_live:
            raise RuntimeError(f"unknown live constraint {args.live}; "
                               f"choices={[name for name, _ in live]}")
    selected_unused = ([value for _, value in unused] if args.lower == "all"
                       else ([] if args.lower == "none" else
                             [value for label, value in unused
                              if label == args.lower]))
    generators = (f, g, c9, named[args.factor], *selected_unused)
    if args.localized and args.live == "scan":
        body = ""
        for index, (name, value) in enumerate(live):
            body += (f'list L{index}=facstd(I,ideal({singular(value)}));'
                     f'print("LIVE {name}");print(size(L{index}));')
        command = (f"ring R={args.characteristic},"
                   f"({','.join(map(str, variables))}),dp;"
                   f"ideal I={','.join(singular(value) for value in generators)};"
                   'print("BEGIN");'+body+'print("END");quit;')
    elif args.localized:
        command = (f"ring R={args.characteristic},"
                   f"({','.join(map(str, variables))}),dp;"
                   f"ideal I={','.join(singular(value) for value in generators)};"
                   f"ideal C={','.join(singular(value) for value in selected_live)};"
                   "list L=facstd(I,C);"
                   'print("BEGIN");print(size(L));'
                   'for(int j=1;j<=size(L);j++){print(size(L[j]));'
                   'print(dim(std(L[j])));};print("END");quit;')
    else:
        command = (f"ring R={args.characteristic},"
                   f"({','.join(map(str, variables))}),dp;"
                   f"ideal I={','.join(singular(value) for value in generators)};"
                   "ideal G=slimgb(I);"
                   'print("BEGIN");print(string(reduce(1,G)));'
                   'print(size(G));print(dim(G));print("END");quit;')
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"{args.factor}: TIMEOUT after {time.monotonic()-started:.3f}s")
        return
    print("factor / degree:", args.factor,
          sp.degree(named[args.factor], variables[1]))
    print("elapsed_seconds:", time.monotonic()-started)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
