#!/usr/bin/env python3
"""Function-field/qring probe for Delta=0,Bplus!=0,Au!=0."""

from __future__ import annotations

import importlib.util
import argparse
import itertools
from pathlib import Path
import subprocess
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
INTERFACE_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTERFACE = load("n8_cycle_delta_au_open_source", INTERFACE_PATH)
SOURCE = INTERFACE.SOURCE


def singular(poly):
    return str(sp.expand(poly)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--minor-count", type=int, default=3)
    parser.add_argument("--resultant-only", action="store_true")
    parser.add_argument("--lift", action="store_true")
    args = parser.parse_args()
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    p1, p2, p3, p4 = SOURCE.P
    a0, a5 = SOURCE.A0, SOURCE.A5
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    ratio = {b3: x*b1, d3: -x*d1*d4}
    upper = [sp.factor(rows[f"cofactor_{edge}_0"].subs(ratio))
             for edge in range(1, 5)]
    p3_p4 = sp.solve([upper[2], upper[3]], [p4, p3], dict=True,
                     simplify=False)[0]
    u = sp.factor(-sp.cancel(upper[0].subs(p3_p4))/d4)
    v = sp.factor(sp.cancel(upper[1].subs(p3_p4))
                  /(b1**2*d1*d4*x))
    au = sp.factor(sp.diff(u, d4))
    d4_value = sp.cancel(-u.subs(d4, 0)/au)
    q = sp.factor(sp.resultant(u, v, d4)/b0)

    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    reduced = {label: sp.cancel(rows[label].subs(ratio).subs(p3_p4))
               for label in labels}
    a0_value = sp.solve(reduced["cofactor_5_0"], a0, dict=True,
                        simplify=False)[0][a0]
    current = {label: sp.cancel(value.subs(a0, a0_value)
                                .subs(d4, d4_value))
               for label, value in reduced.items()
               if label != "cofactor_5_0"}
    tops = {label: sp.cancel(value).as_numer_denom()[0]
            for label, value in current.items()}
    for label, value in tops.items():
        print(label, len(sp.Poly(value, b0, b1, x, d1, p1, p2, a5).terms()),
              flush=True)

    normalized = INTERFACE.derive(rows)[6]
    live_row_factors = (b1**2*d1**2*x, 1, 1, d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row]) for entry in entries]
              for row, entries in enumerate(normalized)]
    combinations = ((2, 3, 4, 5), (0, 2, 3, 4), (1, 2, 3, 4),
                    (0, 2, 3, 5), (1, 2, 3, 5), (0, 1, 2, 3))
    determinants = []
    for combination in combinations[:args.minor_count]:
        value = 0
        for permutation in itertools.permutations(range(4)):
            inversions = sum(permutation[left] > permutation[right]
                             for left in range(4)
                             for right in range(left + 1, 4))
            value += ((-1)**inversions
                      * sp.prod(matrix[combination[row]][permutation[row]]
                                for row in range(4)))
        value = sp.cancel(sp.expand(value).subs(d4, d4_value)) \
            .as_numer_denom()[0]
        value = sp.rem(sp.Poly(value, b0, domain="QQ(b1,x,d1)"),
                       sp.Poly(q, b0, domain="QQ(b1,x,d1)")).as_expr()
        value = sp.cancel(value).as_numer_denom()[0]
        b1_power = min(monomial[1]
                       for monomial, _ in sp.Poly(
                           value, b0, b1, x, d1).terms())
        value = sp.cancel(value/b1**b1_power)
        determinants.append(value)
        print("minor", combination,
              len(sp.Poly(value, b0, b1, x, d1).terms()),
              "removed_b1", b1_power, flush=True)

    if args.resultant_only:
        specialization = {d1: 2, x: 3}
        left = determinants[0].subs(specialization)
        right = determinants[1].subs(specialization)
        q_special = q.subs(specialization)
        resultant = sp.resultant(left, right, b1)
        resultant = sp.rem(sp.Poly(resultant, b0),
                           sp.Poly(q_special, b0)).as_expr()
        print("specialized Q", sp.factor(q_special), flush=True)
        print("specialized resultant remainder", sp.factor(resultant),
              flush=True)
        return

    # d1,x are coefficient-field parameters.  Q is quadratic in b0 and
    # becomes the qring relation.  All rational substitution denominators
    # are chart-live on Au!=0 and may be cleared.
    basis_command = ("matrix T;ideal G=liftstd(I,T);"
                     if args.lift else "ideal G=std(I);")
    print_command = ('print(G);print("TRANSFORM");print(T);'
                     if args.lift else "print(G);")
    command = (
        f"ring R=({args.characteristic},d1,x),(b0,b1),dp;"
        f"ideal J={singular(q)};"
        "qring S=std(J);"
        f"ideal I={','.join(singular(value) for value in determinants)};"
        "option(redSB);"
        f"{basis_command}"
        f'print("BEGIN");print(size(G));print(dim(G));{print_command}'
        'print("END");quit;'
    )
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   capture_output=True, text=True,
                                   timeout=180, check=False)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)


if __name__ == "__main__":
    main()
