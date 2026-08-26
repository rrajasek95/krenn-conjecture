#!/usr/bin/env python3
"""Discovery interface for branch-0 anti-term defect-support strata.

For a support S, c_e=-(1+a_e*d_e)/b_e and d_e is set to zero off S.
The probe localizes only H, every b_e, and a_e*d_e for e in S.  It is a
discovery tool; NONUNIT and dimensions are not proof claims.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
N = 18
ONE = {(0,) * N: Fraction(1)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SCREEN = load("n8_b0_defect_screen", SOURCE / "screen_lowq_joint_branch_orbits.py")
PROBE = SCREEN.PROBE


def clean(poly):
    return {key: value for key, value in poly.items() if value}


def add(*polys):
    result = Counter()
    for poly in polys:
        result.update(poly)
    return clean(result)


def scale(poly, scalar):
    return clean({key: Fraction(scalar) * value for key, value in poly.items()})


def multiply(*polys):
    result = ONE
    for poly in polys:
        updated = Counter()
        for left, lc in result.items():
            for right, rc in poly.items():
                updated[tuple(x + y for x, y in zip(left, right))] += lc * rc
        result = clean(updated)
    return result


def variable(index, power=1, coefficient=1):
    exponent = [0] * N
    exponent[index] = power
    return {tuple(exponent): Fraction(coefficient)}


def entries(support):
    support = frozenset(support)
    result = []
    for edge in range(6):
        a, b = variable(edge), variable(6 + edge)
        d = variable(12 + edge) if edge in support else {}
        c = variable(6 + edge, -1, -1)
        if edge in support:
            c = add(c, multiply(a, d, variable(6 + edge, -1, -1)))
        result.extend((a, b, c, d))
    return tuple(result)


def substitute(raw, values):
    result = {}
    for monomial, coefficient in raw.items():
        term = scale(ONE, coefficient)
        for index in monomial:
            term = multiply(term, values[index])
        result = add(result, term)
    return result


def clear(poly):
    if not poly:
        return {}, (0,) * N
    shift = tuple(max(0, -min(exponent[index] for exponent in poly))
                  for index in range(N))
    return clean({tuple(exponent[index] + shift[index]
                        for index in range(N)): coefficient
                  for exponent, coefficient in poly.items()}), shift


def singular(poly):
    if not poly:
        return "0"
    names = tuple([f"a{i}" for i in range(6)]
                  + [f"b{i}" for i in range(6)]
                  + [f"d{i}" for i in range(6)])
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = [names[index] + (f"^{power}" if power != 1 else "")
                   for index, power in enumerate(exponent) if power]
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces)


def derived(support):
    values = entries(support)
    equations, raw_h = PROBE.equations((0,) * 6)
    labels = ["e_" + "".join(map(str, edge))
              for edge in PROBE.CORE.SUPER_EDGES]
    labels += ["t_" + "".join(map(str, triple))
               for triple in __import__("itertools").combinations(range(4), 3)]
    labels += [f"cofactor_{edge}_{position}"
               for edge in range(6) for position in (0, 3)]
    rows, seen = [], set()
    for label, raw in zip(labels, equations):
        poly, shift = clear(substitute(raw, values))
        if not poly:
            continue
        encoded = singular(poly)
        if encoded in seen:
            continue
        seen.add(encoded)
        rows.append((label, poly, shift, encoded))
    h, h_shift = clear(substitute(raw_h, values))
    return tuple(rows), h, h_shift


def run(support, timeout, characteristic=0):
    rows, h, _ = derived(support)
    variables = ([f"a{i}" for i in range(6)] + [f"b{i}" for i in range(6)]
                 + [f"d{i}" for i in sorted(support)] + ["z"])
    b_product = "*".join(f"b{i}" for i in range(6))
    defects = "*".join(f"a{i}*d{i}" for i in sorted(support)) or "1"
    localization = f"z*({singular(h)})*{b_product}*{defects}-1"
    ideal = ",".join(row[3] for row in rows) + "," + localization
    command = (
        f"ring R={characteristic},({','.join(variables)}),dp;ideal I={ideal};"
        "ideal G=slimgb(I);poly witness=reduce(1,G);"
        'print("BEGIN");if(witness==0){print("UNIT");}'
        'else{print("NONUNIT");};print(size(G));print(dim(G));print("END");quit;'
    )
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=timeout, check=False)
        return rows, completed
    except subprocess.TimeoutExpired:
        return rows, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("edges", nargs="*", type=int, default=[0, 1, 3])
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--print-rows", action="store_true")
    args = parser.parse_args()
    support = tuple(sorted(set(args.edges)))
    rows, completed = run(support, args.timeout, args.characteristic)
    print("support / distinct rows:", support, len(rows))
    if args.print_rows:
        for label, _, shift, encoded in rows:
            print(label, list(shift), "=", encoded)
    if completed is None:
        print("TIMEOUT")
    else:
        print("return", completed.returncode)
        print(completed.stdout)
        print(completed.stderr)


if __name__ == "__main__":
    main()
