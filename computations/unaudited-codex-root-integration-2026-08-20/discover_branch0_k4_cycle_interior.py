#!/usr/bin/env python3
"""Discovery interface for the branch-0 four-cycle interior.

The chart uses the off-diagonal permanent parametrization

    M_e = [[a_e,b_e],[-(1+a_e*d_e)/b_e,d_e]]

with defect support {02,03,12,13}.  The legitimate clone torus gauge is
``b03=b13=b23=d03=1``.  This helper derives all packet rows from the raw
24-cell definitions, so modular and exact probes use the same source.

This is deliberately a discovery helper: a modular UNIT or an exact basis
without a serialized lift is not promoted to a theorem artifact.
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
AUDIT = HERE / "audit_branch0_both_live_easy_strata.py"
SUPPORT = (1, 2, 3, 4)
GAUGE = {"b2": 1, "b4": 1, "b5": 1, "d2": 1}


def load(path: Path):
    spec = importlib.util.spec_from_file_location("root_k4_cycle_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(AUDIT)


def singular(expression) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def source_rows():
    variables, rows, pure_h = SOURCE.derive(SUPPORT)
    substitutions = {sp.Symbol(name): value for name, value in GAUGE.items()}
    kept_variables = tuple(variable for variable in variables
                           if str(variable) not in GAUGE)
    seen = set()
    specialized = []
    for label, expression, _ in rows:
        expression = sp.expand(expression.subs(substitutions))
        encoded = singular(expression)
        if expression == 0 or encoded in seen:
            continue
        seen.add(encoded)
        specialized.append((label, encoded))
    return kept_variables, specialized, singular(pure_h.subs(substitutions))


def localizers(split: bool, include_c: bool):
    h = "HINV*PUREH-1"
    if split:
        records = [("H_localizer", h)]
        records += [(f"b{edge}_localizer", f"IB{edge}*b{edge}-1")
                    for edge in (0, 1, 3)]
        records += [
            ("a1_localizer", "IA1*a1-1"),
            ("d1_localizer", "ID1*d1-1"),
            ("a2_localizer", "IA2*a2-1"),
            ("a3_localizer", "IA3*a3-1"),
            ("d3_localizer", "ID3*d3-1"),
            ("a4_localizer", "IA4*a4-1"),
            ("d4_localizer", "ID4*d4-1"),
        ]
        if include_c:
            records += [
                ("c1_localizer", "IC1*(1+a1*d1)-1"),
                ("c2_localizer", "IC2*(1+a2)-1"),
                ("c3_localizer", "IC3*(1+a3*d3)-1"),
                ("c4_localizer", "IC4*(1+a4*d4)-1"),
            ]
        return records
    records = [
        ("H_localizer", h),
        ("b_product_localizer", "BINV*b0*b1*b3-1"),
        ("ad_product_localizer",
         "ADINV*a1*a2*a3*a4*d1*d3*d4-1"),
    ]
    if include_c:
        records.append((
            "c_product_localizer",
            "CINV*(1+a1*d1)*(1+a2)*(1+a3*d3)*(1+a4*d4)-1",
        ))
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--include-c", action="store_true")
    parser.add_argument("--split-localizers", action="store_true")
    parser.add_argument("--lift", action="store_true")
    parser.add_argument("--power-bound", type=int, default=0)
    args = parser.parse_args()

    variables, rows, pure_h = source_rows()
    locs = localizers(args.split_localizers, args.include_c)
    locs = [(label, polynomial.replace("PUREH", f"({pure_h})"))
            for label, polynomial in locs]
    labels = [label for label, _ in rows] + [label for label, _ in locs]
    generators = [polynomial for _, polynomial in rows] + [p for _, p in locs]

    extra_variables = sorted({token for _, polynomial in locs
                              for token in polynomial.replace("(", " ")
                              .replace(")", " ").replace("*", " ")
                              .replace("-", " ").split()
                              if token.isalpha() and token.isupper()})
    # The preceding lexical extraction intentionally finds only the explicit
    # inverse-variable names; ordinary source variables contain digits.
    ring_variables = [str(variable) for variable in variables] + extra_variables
    prefix = (f"ring R={args.characteristic},"
              f"({','.join(ring_variables)}),dp;"
              f"ideal I={','.join(generators)};")
    if args.lift:
        body = (
            "matrix L;ideal G=liftstd(I,L);"
            'print("BEGIN");print(size(G));print(string(G[1]));print(dim(G));'
            "for(int i=1;i<=nrows(L);i++){if(L[i,1]!=0){"
            'print("ACTIVE");print(i);print(deg(L[i,1]));'
            "print(size(L[i,1]));}};print(\"END\");quit;"
        )
    else:
        body = (
            "ideal G=slimgb(I);"
            'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
            'print(dim(G));'
        )
        c_product = "(1+a1*d1)*(1+a2)*(1+a3*d3)*(1+a4*d4)"
        for power in range(1, args.power_bound + 1):
            body += (f'print("POWER {power}");'
                     f'print(string(reduce(({c_product})^{power},G)));')
        body += 'print("END");quit;'

    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", prefix + body],
            text=True, capture_output=True, timeout=args.timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT after {time.monotonic() - started:.3f}s")
        print("labels:", labels)
        return
    print(f"elapsed_seconds: {time.monotonic() - started:.3f}")
    print("labels:", labels)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
