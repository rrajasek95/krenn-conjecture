#!/usr/bin/env python3
"""Specialized discovery probe for the true both-term-live k4 cycle.

The source is ``probe_branch0_defect_support.py`` with S={1,2,3,4}.
We substitute the lossless gauge b2=b4=b5=d2=1 before Groebner work and
localize H, the remaining b's, every a_e*d_e and every 1+a_e*d_e on S.
UNIT is sound; NONUNIT/dimension/timeout are discovery data only.
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


PROBE = load("n8_branch0_cycle_interior_source",
             HERE / "probe_branch0_defect_support.py")
SUPPORT = (1, 2, 3, 4)
NAMES = (tuple(f"a{i}" for i in range(6))
         + ("b0", "b1", "b3", "d1", "d3", "d4"))
OLD_TO_NEW = {old: new for new, old in enumerate(
    (0, 1, 2, 3, 4, 5, 6, 7, 9, 13, 15, 16))}
GAUGE_INDICES = frozenset((8, 10, 11, 14))


def specialize(poly):
    answer = Counter()
    for exponent, coefficient in poly.items():
        new = [0] * len(NAMES)
        for old, power in enumerate(exponent):
            if not power or old in GAUGE_INDICES:
                continue
            if old not in OLD_TO_NEW:
                raise RuntimeError(f"ungauged variable x{old} occurred")
            new[OLD_TO_NEW[old]] = power
        answer[tuple(new)] += coefficient
    return {key: value for key, value in answer.items() if value}


def singular(poly):
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = [name + (f"^{power}" if power != 1 else "")
                   for name, power in zip(NAMES, exponent) if power]
        body = "*".join(factors) or "1"
        coefficient = Fraction(coefficient)
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def singular_named(poly, names):
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = [name + (f"^{power}" if power != 1 else "")
                   for name, power in zip(names, exponent) if power]
        body = "*".join(factors) or "1"
        coefficient = Fraction(coefficient)
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def c_zero_specialize(poly, edge):
    """Substitute a_edge=-1/d_edge (or -1 for the gauged edge 2)."""
    d_index = {1: 9, 2: None, 3: 10, 4: 11}[edge]
    answer = Counter()
    for exponent, coefficient in poly.items():
        exponent = list(exponent)
        power = exponent[edge]
        exponent[edge] = 0
        coefficient *= (-1) ** power
        if d_index is not None:
            exponent[d_index] -= power
        del exponent[edge]
        answer[tuple(exponent)] += coefficient
    answer = {key: value for key, value in answer.items() if value}
    if not answer:
        return {}
    if d_index is not None:
        new_d_index = d_index - (1 if edge < d_index else 0)
        shift = max(0, -min(exponent[new_d_index] for exponent in answer))
        if shift:
            answer = {
                tuple(power + shift if index == new_d_index else power
                      for index, power in enumerate(exponent)): coefficient
                for exponent, coefficient in answer.items()
            }
    return answer


def multi_c_zero_specialize(poly, zero_edges):
    zero_edges = tuple(sorted(zero_edges))
    answer = Counter()
    for exponent, coefficient in poly.items():
        exponent = list(exponent)
        for edge in zero_edges:
            power = exponent[edge]
            exponent[edge] = 0
            coefficient *= (-1) ** power
            d_index = {1: 9, 2: None, 3: 10, 4: 11}[edge]
            if d_index is not None:
                exponent[d_index] -= power
        exponent = tuple(power for index, power in enumerate(exponent)
                         if index not in zero_edges)
        answer[exponent] += coefficient
    answer = {key: value for key, value in answer.items() if value}
    if not answer:
        return {}
    old_indices = tuple(index for index in range(len(NAMES))
                        if index not in zero_edges)
    for old_d in (9, 10, 11):
        new_d = old_indices.index(old_d)
        shift = max(0, -min(exponent[new_d] for exponent in answer))
        if shift:
            answer = {
                tuple(power + shift if index == new_d else power
                      for index, power in enumerate(exponent)): coefficient
                for exponent, coefficient in answer.items()
            }
    return answer


def data():
    rows, hafnian, _ = PROBE.derived(SUPPORT)
    specialized = []
    seen = set()
    for label, poly, _, _ in rows:
        value = specialize(poly)
        encoded = singular(value)
        if value and encoded not in seen:
            seen.add(encoded)
            specialized.append((label, value, encoded))
    return tuple(specialized), specialize(hafnian)


def command(characteristic, print_gb=False, split="all", use_h=True):
    rows, hafnian = data()
    live = ("b0*b1*b3*a1*d1*a2*a3*d3*a4*d4"
            "*(1+a1*d1)*(1+a2)*(1+a3*d3)*(1+a4*d4)")
    generators = [row[2] for row in rows]
    delta = "b1*d3+b3*d1*d4"
    if split == "generic":
        live += f"*({delta})"
    elif split == "exceptional":
        generators.append(delta)
    h_factor = f"({singular(hafnian)})*" if use_h else ""
    generators.append(f"z*{h_factor}{live}-1")
    tail = ('print("BEGIN");size(G);dim(G);G;print("END");quit;'
            if print_gb else
            'print("BEGIN");size(G);dim(G);reduce(1,G);print("END");quit;')
    return (f"ring R={characteristic},({','.join(NAMES)},z),dp;"
            f"ideal I={','.join(generators)};ideal G=slimgb(I);" + tail)


def separate_localizer_command(characteristic, split="all"):
    rows, hafnian = data()
    delta = "b1*d3+b3*d1*d4"
    factors = [
        ("h", singular(hafnian)),
        ("b0", "b0"), ("b1", "b1"), ("b3", "b3"),
        ("a1", "a1"), ("d1", "d1"), ("a2", "a2"),
        ("a3", "a3"), ("d3", "d3"), ("a4", "a4"), ("d4", "d4"),
        ("c1", "1+a1*d1"), ("c2", "1+a2"),
        ("c3", "1+a3*d3"), ("c4", "1+a4*d4"),
    ]
    if split == "generic":
        factors.append(("delta", delta))
    inverse_names = [f"z_{name}" for name, _ in factors]
    generators = [row[2] for row in rows]
    generators += [f"z_{name}*({factor})-1" for name, factor in factors]
    if split == "exceptional":
        generators.append(delta)
    return (
        f"ring R={characteristic},({','.join(NAMES + tuple(inverse_names))}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");size(G);dim(G);reduce(1,G);print("END");quit;'
    )


def boundary_command(characteristic, edge):
    """Impose one c numerator zero; test propagation to the other three."""
    rows, hafnian = data()
    c_factors = {1: "1+a1*d1", 2: "1+a2",
                 3: "1+a3*d3", 4: "1+a4*d4"}
    live = "b0*b1*b3*a1*d1*a2*a3*d3*a4*d4"
    generators = [row[2] for row in rows] + [c_factors[edge]]
    pieces = [
        f"ring R={characteristic},({','.join(NAMES)},z),dp;",
        f"ideal I={','.join(generators)},z*({singular(hafnian)})*{live}-1;",
        "ideal G=slimgb(I);",
        'print("BEGIN");size(G);dim(G);reduce(1,G);',
    ]
    for other in (1, 2, 3, 4):
        pieces.append(f'print("C{other}");reduce({c_factors[other]},G);')
    pieces.append('print("END");quit;')
    return "".join(pieces)


def specialized_boundary_command(characteristic, edge):
    rows, hafnian = data()
    names = tuple(name for index, name in enumerate(NAMES) if index != edge)
    specialized_rows = []
    seen = set()
    for _, poly, _ in rows:
        value = c_zero_specialize(poly, edge)
        encoded = singular_named(value, names)
        if value and encoded not in seen:
            seen.add(encoded)
            specialized_rows.append(encoded)
    specialized_h = c_zero_specialize(hafnian, edge)
    # a_edge is automatically live because d_edge is; all other defect a's
    # remain explicit localization factors.
    live_names = ["b0", "b1", "b3", "d1", "d3", "d4"]
    live_names += [f"a{other}" for other in (1, 2, 3, 4)
                   if other != edge]
    live = "*".join(live_names)
    c_factors = {1: "1+a1*d1", 2: "1+a2",
                 3: "1+a3*d3", 4: "1+a4*d4"}
    pieces = [
        f"ring R={characteristic},({','.join(names)},z),dp;",
        f"ideal I={','.join(specialized_rows)},"
        f"z*({singular_named(specialized_h, names)})*{live}-1;",
        "ideal G=slimgb(I);",
        'print("BEGIN");size(G);dim(G);reduce(1,G);',
    ]
    for other in (1, 2, 3, 4):
        if other != edge:
            pieces.append(f'print("C{other}");reduce({c_factors[other]},G);')
    pieces.append('print("END");quit;')
    return "".join(pieces)


def boundary_stratum_command(characteristic, zero_edges, use_h=True,
                             print_gb=False):
    zero_edges = tuple(sorted(set(zero_edges)))
    rows, hafnian = data()
    names = tuple(name for index, name in enumerate(NAMES)
                  if index not in zero_edges)
    specialized_rows = []
    seen = set()
    for _, poly, _ in rows:
        value = multi_c_zero_specialize(poly, zero_edges)
        encoded = singular_named(value, names)
        if value and encoded not in seen:
            seen.add(encoded)
            specialized_rows.append(encoded)
    specialized_h = multi_c_zero_specialize(hafnian, zero_edges)
    live = ["b0", "b1", "b3", "d1", "d3", "d4"]
    live += [f"a{edge}" for edge in (1, 2, 3, 4)
             if edge not in zero_edges]
    live += [{1: "1+a1*d1", 2: "1+a2",
              3: "1+a3*d3", 4: "1+a4*d4"}[edge]
             for edge in (1, 2, 3, 4) if edge not in zero_edges]
    h_factor = f"({singular_named(specialized_h, names)})*" if use_h else ""
    tail = ('print("BEGIN");size(G);dim(G);G;print("END");quit;'
            if print_gb else
            'print("BEGIN");size(G);dim(G);reduce(1,G);print("END");quit;')
    return (
        f"ring R={characteristic},({','.join(names)},z),dp;"
        f"ideal I={','.join(specialized_rows)},"
        f"z*{h_factor}{'*'.join(live)}-1;"
        "ideal G=slimgb(I);" + tail
    )


def generic_reduce_command(characteristic):
    """Reduce all rows after solving the four upper cofactor equations."""
    rows, _ = data()
    row_map = {label: encoded for label, _, encoded in rows}
    upper_labels = tuple(f"cofactor_{edge}_0" for edge in (1, 2, 3, 4))
    upper = [row_map[label] for label in upper_labels]
    remaining = [(label, encoded) for label, _, encoded in rows
                 if label not in upper_labels]
    parameters = "b0,b1,b3,d1,d3,d4"
    variables = "a1,a2,a3,a4,a0,a5"
    pieces = [
        f"ring R=({characteristic},{parameters}),({variables}),dp;",
        f"ideal U={','.join(upper)};ideal G=std(U);",
        'print("UPPER");G;',
    ]
    for label, encoded in remaining:
        pieces.append(f'print("ROW {label}");reduce({encoded},G);')
    pieces.append("quit;")
    return "".join(pieces)


def generic_six_solve_command(characteristic):
    """Solve upper four plus one a0- and one a5-row generically."""
    rows, _ = data()
    row_map = {label: encoded for label, _, encoded in rows}
    solve_labels = (tuple(f"cofactor_{edge}_0" for edge in (1, 2, 3, 4))
                    + ("t_012", "t_023"))
    selected = [row_map[label] for label in solve_labels]
    remaining = [(label, encoded) for label, _, encoded in rows
                 if label not in solve_labels]
    parameters = "b0,b1,b3,d1,d3,d4"
    variables = "a1,a2,a3,a4,a0,a5"
    pieces = [
        f"ring R=({characteristic},{parameters}),({variables}),dp;",
        f"ideal U={','.join(selected)};ideal G=std(U);",
        'print("SOLVE");size(G);',
    ]
    for label, encoded in remaining:
        pieces.append(f'print("ROW {label}");reduce({encoded},G);')
    pieces.append("quit;")
    return "".join(pieces)


def generic_factor_command(characteristic, label="t_013"):
    rows, _ = data()
    row_map = {name: encoded for name, _, encoded in rows}
    solve_labels = (tuple(f"cofactor_{edge}_0" for edge in (1, 2, 3, 4))
                    + ("t_012", "t_023"))
    selected = [row_map[name] for name in solve_labels]
    parameters = "b0,b1,b3,d1,d3,d4"
    variables = "a1,a2,a3,a4,a0,a5"
    return (
        f"ring R=({characteristic},{parameters}),({variables}),dp;"
        f"ideal U={','.join(selected)};ideal G=std(U);"
        f"poly q=reduce({row_map[label]},G);"
        'print("BEGIN");factorize(q);print("END");quit;'
    )


def eliminate_command(characteristic):
    """Eliminate all six a variables before any localization."""
    rows, _ = data()
    generators = [row[2] for row in rows]
    variables = "a1,a2,a3,a4,a0,a5,b0,b1,b3,d1,d3,d4"
    return (
        f"ring R={characteristic},({variables}),(lp(6),dp(6));"
        f"ideal I={','.join(generators)};"
        "ideal E=eliminate(I,a1*a2*a3*a4*a0*a5);"
        'print("BEGIN");size(E);E;print("END");quit;'
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--print-rows", action="store_true")
    parser.add_argument("--print-gb", action="store_true")
    parser.add_argument("--generic-reduce", action="store_true")
    parser.add_argument("--generic-six-solve", action="store_true")
    parser.add_argument("--generic-factor")
    parser.add_argument("--eliminate", action="store_true")
    parser.add_argument("--split", choices=("all", "generic", "exceptional"),
                        default="all")
    parser.add_argument("--separate-localizers", action="store_true")
    parser.add_argument("--boundary-edge", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--specialized-boundary-edge", type=int,
                        choices=(1, 2, 3, 4))
    parser.add_argument("--zero-edges", nargs="*", type=int,
                        choices=(1, 2, 3, 4))
    parser.add_argument("--omit-h", action="store_true")
    args = parser.parse_args()
    rows, hafnian = data()
    print("distinct rows / H terms:", len(rows), len(hafnian))
    if args.print_rows:
        for label, _, encoded in rows:
            print(label, "=", encoded)
    try:
        requested = (boundary_stratum_command(args.characteristic,
                                               args.zero_edges,
                                               not args.omit_h,
                                               args.print_gb)
                     if args.zero_edges else
                     specialized_boundary_command(
                         args.characteristic, args.specialized_boundary_edge)
                     if args.specialized_boundary_edge else
                     boundary_command(args.characteristic, args.boundary_edge)
                     if args.boundary_edge else
                     generic_factor_command(args.characteristic,
                                             args.generic_factor)
                     if args.generic_factor else
                     separate_localizer_command(args.characteristic, args.split)
                     if args.separate_localizers else
                     eliminate_command(args.characteristic)
                     if args.eliminate else
                     generic_six_solve_command(args.characteristic)
                     if args.generic_six_solve else
                     generic_reduce_command(args.characteristic)
                     if args.generic_reduce else
                     command(args.characteristic, args.print_gb, args.split,
                             not args.omit_h))
        completed = subprocess.run(
            ["Singular", "-q", "-c", requested],
            text=True, capture_output=True, timeout=args.timeout, check=False,
        )
        print("return", completed.returncode)
        print(completed.stdout)
        print(completed.stderr)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")


if __name__ == "__main__":
    main()
