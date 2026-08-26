#!/usr/bin/env python3
"""Discovery probe for the k4 cycle in p_e=a_e*d_e coordinates.

All d_e on the defect cycle are live.  Replacing a_e by p_e/d_e makes the
interior factors simply p_e*(1+p_e) and often lowers Groebner fill.  The
literal rows are inherited from the gauge-fixed source probe and Laurent
denominators in d1,d3,d4 are cleared losslessly.
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BASE = load("n8_cycle_pcoords_source", HERE / "probe_branch0_cycle_interior.py")
NAMES = ("p1", "p2", "p3", "p4", "a0", "a5",
         "b0", "b1", "b3", "d1", "d3", "d4")


def transform(poly):
    answer = Counter()
    for exponent, coefficient in poly.items():
        new = [0] * 12
        # p coordinates and their Laurent d denominators.
        for old_a, new_p, old_d, new_d in (
                (1, 0, 9, 9), (2, 1, None, None),
                (3, 2, 10, 10), (4, 3, 11, 11)):
            power = exponent[old_a]
            new[new_p] += power
            if old_d is not None:
                new[new_d] -= power
        new[4] += exponent[0]
        new[5] += exponent[5]
        for old, target in ((6, 6), (7, 7), (8, 8),
                            (9, 9), (10, 10), (11, 11)):
            new[target] += exponent[old]
        answer[tuple(new)] += coefficient
    answer = {key: value for key, value in answer.items() if value}
    if not answer:
        return {}
    shifts = {index: max(0, -min(exponent[index] for exponent in answer))
              for index in (9, 10, 11)}
    return {
        tuple(power + shifts.get(index, 0)
              for index, power in enumerate(exponent)): coefficient
        for exponent, coefficient in answer.items()
    }


def singular(poly):
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        coefficient = Fraction(coefficient)
        factors = [name + (f"^{power}" if power != 1 else "")
                   for name, power in zip(NAMES, exponent) if power]
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def data():
    rows, hafnian = BASE.data()
    transformed = []
    seen = set()
    for label, poly, _ in rows:
        value = transform(poly)
        encoded = singular(value)
        if value and encoded not in seen:
            seen.add(encoded)
            transformed.append((label, value, encoded))
    return tuple(transformed), transform(hafnian)


def command(characteristic, use_h, print_gb, block_order=False,
            core11=False, separate=False):
    rows, hafnian = data()
    if core11:
        labels = ({f"cofactor_{edge}_0" for edge in (0, 1, 2, 3, 4, 5)}
                  | {"cofactor_0_3", "t_012", "t_013", "t_023", "t_123"})
        rows = tuple(row for row in rows if row[0] in labels)
    factors = [(name, name) for name in
               ("b0", "b1", "b3", "d1", "d3", "d4",
                "p1", "p2", "p3", "p4")]
    factors += [(f"c{edge}", f"1+p{edge}") for edge in (1, 2, 3, 4)]
    if use_h:
        factors.append(("h", singular(hafnian)))
    tail = ('print("BEGIN");size(G);dim(G);G;print("END");quit;'
            if print_gb else
            'print("BEGIN");size(G);dim(G);reduce(1,G);print("END");quit;')
    order = "(dp(4),dp(2),dp(6),dp(1))" if block_order else "dp"
    if separate:
        inverse_names = tuple(f"z_{name}" for name, _ in factors)
        variables = NAMES + inverse_names
        localizers = [f"z_{name}*({factor})-1" for name, factor in factors]
    else:
        variables = NAMES + ("z",)
        localizers = [f"z*{'*'.join(f'({factor})' for _, factor in factors)}-1"]
    if separate:
        order = "dp"
    return (
        f"ring R={characteristic},({','.join(variables)}),{order};"
        f"ideal I={','.join(row[2] for row in rows)},"
        f"{','.join(localizers)};"
        "ideal G=slimgb(I);" + tail
    )


def facstd_command(characteristic, core11=False):
    rows, _ = data()
    if core11:
        labels = ({f"cofactor_{edge}_0" for edge in (0, 1, 2, 3, 4, 5)}
                  | {"cofactor_0_3", "t_012", "t_013", "t_023", "t_123"})
        rows = tuple(row for row in rows if row[0] in labels)
    return (
        'LIB "facstd.lib";'
        f"ring R={characteristic},({','.join(NAMES)}),dp;"
        f"ideal I={','.join(row[2] for row in rows)};"
        "list L=facstd(I);"
        'print("BEGIN");size(L);'
        "int i;for(i=1;i<=size(L);i++){print(size(L[i]));print(dim(L[i]));};"
        'print("END");quit;'
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--omit-h", action="store_true")
    parser.add_argument("--print-rows", action="store_true")
    parser.add_argument("--print-gb", action="store_true")
    parser.add_argument("--block-order", action="store_true")
    parser.add_argument("--core11", action="store_true")
    parser.add_argument("--separate-localizers", action="store_true")
    parser.add_argument("--facstd", action="store_true")
    args = parser.parse_args()
    rows, hafnian = data()
    print("rows / H terms:", len(rows), len(hafnian))
    if args.print_rows:
        for label, _, encoded in rows:
            print(label, "=", encoded)
    try:
        requested = (facstd_command(args.characteristic, args.core11)
                     if args.facstd else
                     command(args.characteristic, not args.omit_h,
                             args.print_gb, args.block_order, args.core11,
                             args.separate_localizers))
        completed = subprocess.run(
            ["Singular", "-q", "-c",
             requested],
            text=True, capture_output=True, timeout=args.timeout, check=False,
        )
        print("return", completed.returncode)
        print(completed.stdout)
        print(completed.stderr)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")


if __name__ == "__main__":
    main()
