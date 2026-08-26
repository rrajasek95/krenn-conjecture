#!/usr/bin/env python3
"""Modular/exact probe for the exported Delta=0 linear interface."""

from __future__ import annotations

import argparse
import importlib.util
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
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_zero_linear_interface.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_linear_audit", AUDIT_PATH)


def singular(poly):
    return str(sp.expand(poly)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--exact", action="store_true")
    parser.add_argument("--omit-h", action="store_true")
    parser.add_argument("--separate", action="store_true")
    args = parser.parse_args()

    raw_rows, raw_h = AUDIT.SOURCE.SOURCE.data()
    rows = {label: AUDIT.SOURCE.expression(poly)
            for label, poly, _ in raw_rows}
    derived = AUDIT.derive(rows)
    variables, u, v, p3_p4, a0_value, _, matrix = derived[:7]
    b0, b1, x, d1, d4 = variables
    p1, p2 = AUDIT.SOURCE.P[:2]
    a5 = AUDIT.SOURCE.A5
    equations = [u, v]
    equations += [row[0]*p1 + row[1]*p2 + row[2]*a5 + row[3]
                  for row in matrix]

    factors = [b0, b1, x, d1, d4, b1 + d1, x - 1,
               p1, p1 + 1, p2, p2 + 1]
    for value in (p3_p4[AUDIT.SOURCE.P[2]],
                  p3_p4[AUDIT.SOURCE.P[3]]):
        top, bottom = sp.cancel(value).as_numer_denom()
        factors.extend((top, sp.expand(top + bottom)))
    if not args.omit_h:
        h = AUDIT.SOURCE.expression(raw_h)
        b0_old, b1_old, b3_old, d1_old, d3_old, d4_old = \
            AUDIT.SOURCE.PARAMETERS
        ratio = {b3_old: x*b1, d3_old: -x*d1*d4}
        h_value = sp.cancel(h.subs(ratio).subs(p3_p4)
                            .subs(AUDIT.SOURCE.A0, a0_value))
        factors.append(h_value.as_numer_denom()[0])

    ring_variables = (b0, b1, x, d1, d4, p1, p2, a5)
    if args.separate:
        inverses = tuple(sp.Symbol(f"z{index}")
                         for index in range(len(factors)))
        localizers = [inverse*factor - 1
                      for inverse, factor in zip(inverses, factors)]
    else:
        inverses = (sp.Symbol("z"),)
        localizers = [inverses[0]*sp.prod(factors) - 1]
    all_variables = ring_variables + inverses
    characteristic = 0 if args.exact else args.characteristic
    command = (
        f"ring R={characteristic},"
        f"({','.join(map(str, all_variables))}),dp;"
        f"ideal I={','.join(singular(poly) for poly in equations + localizers)};"
        "ideal G=slimgb(I);"
        'print("BEGIN");print(size(G));print(dim(G));'
        'print(string(reduce(1,G)));print("END");quit;'
    )
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
