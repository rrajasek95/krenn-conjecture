#!/usr/bin/env python3
"""Modular/exact probe for the sparse D0=0,C0!=0 rank interface.

Rows t013 and Cof(0,3) give the smallest nonzero 2x2 coefficient minor in
(a0,a5).  On that pivot-open chart the other four augmented 3x3 minors are
the complete consistency equations.  This probe factors the pivot and can
run the resulting localized system in Singular.  A positive modular result
is discovery only; the pivot-zero complement is always out of scope.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import time


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))

import sympy as sp


HERE = Path(__file__).resolve().parent
INTERFACE = HERE / "probe_branch0_cycle_d0_c0_generic.py"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_d0_pivot", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(INTERFACE)


def singular(value):
    return str(sp.expand(value)).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--factor-only", action="store_true")
    parser.add_argument("--export")
    parser.add_argument("--export-saturation")
    args = parser.parse_args()
    variables, residual, c0 = P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    pivot_rows = (1, 4)
    pivot = sp.primitive(sp.Poly(
        sp.expand(matrix[list(pivot_rows), :].det()), b0, d1, d4))[1].as_expr()
    compatibilities = []
    for row in (0, 2, 3, 5):
        value = sp.primitive(sp.Poly(
            sp.expand(augmented[[*pivot_rows, row], :].det()),
            b0, d1, d4))[1].as_expr()
        compatibilities.append(value)
    print("pivot / compatibility terms:",
          len(sp.Poly(pivot, b0, d1, d4).terms()),
          [len(sp.Poly(value, b0, d1, d4).terms())
           for value in compatibilities])

    if args.export:
        exported = [singular(value) for value in compatibilities]
        # msolve 0.10.1 silently misparses ``z*(poly)-1``.  Keep the
        # Rabinowitsch row fully distributed; the shared toolkit rejects
        # parentheses for exactly this reason.
        z = sp.Symbol("z")
        exported.append(singular(sp.expand(z * pivot - 1)))
        Path(args.export).write_text(
            "b0,d1,d4,z\n" + str(args.characteristic) + "\n" +
            ",\n".join(exported) + "\n")
        print("exported:", args.export)

    if args.export_saturation:
        # msolve -S interprets the last input polynomial as the saturating
        # polynomial.  Keeping the pivot out of the ideal and avoiding the
        # Rabinowitsch variable z materially reduces the F4 matrices.
        exported = [singular(value) for value in compatibilities]
        exported.append(singular(pivot))
        Path(args.export_saturation).write_text(
            "b0,d1,d4\n" + str(args.characteristic) + "\n" +
            ",\n".join(exported) + "\n")
        print("exported saturation:", args.export_saturation)

    prefix = (f"ring R={args.characteristic},(b0,d1,d4,z),dp;"
              f"poly P={singular(pivot)};")
    if args.factor_only:
        body = ('list L=factorize(P);print("BEGIN");print(size(L));'
                'for(int i=1;i<=size(L);i++){print(size(L[i]));'
                'print(deg(L[i]));print(L[i]);};print("END");quit;')
    else:
        generators = ",".join(singular(value) for value in compatibilities)
        body = (f"ideal I={generators},z*P-1;ideal G=slimgb(I);"
                'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
                'print(dim(G));print("END");quit;')
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", prefix+body],
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
