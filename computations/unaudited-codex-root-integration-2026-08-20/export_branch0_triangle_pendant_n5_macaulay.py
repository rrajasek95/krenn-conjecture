#!/usr/bin/env python3
"""Export a homogeneous Macaulay interface for the TP N5^3 membership.

The source polynomials and target are reconstructed exactly from the frozen
Cramer reduction.  Rows are degree-D monomials in five geometric variables
and the homogenizer ``t``; target rows are ordered first.  Columns are sorted
by target overlap to help the dependency-free sparse modular solver.

A modular solution is discovery only.  Any selected column ledger must be
reconstructed over Q and replayed against these exact polynomials.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
MINOR = HERE / "probe_branch0_triangle_pendant_minor_split.py"


def load(path: Path):
    spec = importlib.util.spec_from_file_location("root_tp_macaulay_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


M = load(MINOR)


def compositions(total, count, prefix=()):
    if count == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from compositions(total-value, count-1, prefix+(value,))


def integer_terms(expression):
    polynomial = M.sp.Poly(M.sp.expand(expression), *M.PARAMETERS)
    raw = [(tuple(monomial), Fraction(coefficient))
           for monomial, coefficient in polynomial.terms()]
    denominator = math.lcm(*(value.denominator for _, value in raw))
    integers = [(monomial, value.numerator*(denominator//value.denominator))
                for monomial, value in raw]
    content = math.gcd(*(abs(value) for _, value in integers))
    integers = [(monomial, value//content) for monomial, value in integers]
    if integers[0][1] < 0:
        integers = [(monomial, -value) for monomial, value in integers]
    return integers


def homogenize(expression):
    terms = integer_terms(expression)
    degree = max(sum(monomial) for monomial, _ in terms)
    return degree, [(monomial+(degree-sum(monomial),), value)
                    for monomial, value in terms]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=24)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    _, split, compatibility, generic_live, _ = M.derive()
    n5 = generic_live[-1]
    source = [(label,)+homogenize(poly) for label, poly in compatibility]
    target_degree, target_terms = homogenize(M.sp.expand(n5**3))
    if args.degree < target_degree:
        raise RuntimeError(f"degree {args.degree} below target degree {target_degree}")
    target_terms = [
        (monomial[:-1]+(monomial[-1]+args.degree-target_degree,), value)
        for monomial, value in target_terms
    ]
    target_monomials = {monomial for monomial, _ in target_terms}

    all_rows = list(compositions(args.degree, 6))
    all_rows.sort(key=lambda monomial: (monomial not in target_monomials,
                                        monomial))
    row_index = {monomial: index for index, monomial in enumerate(all_rows)}

    columns = []
    for source_position, (label, degree, terms) in enumerate(source):
        multiplier_degree = args.degree-degree
        if multiplier_degree < 0:
            continue
        for multiplier in compositions(multiplier_degree, 6):
            overlap = sum(tuple(a+b for a, b in zip(monomial, multiplier))
                          in target_monomials for monomial, _ in terms)
            columns.append((-overlap, len(terms), source_position,
                            multiplier, label, terms))
    columns.sort(key=lambda item: item[:5])

    target = [[row_index[monomial], value, 1]
              for monomial, value in target_terms]
    header = {
        "column_count": len(columns),
        "degree": args.degree,
        "format": "krenn-tp-n5-homogeneous-macaulay-v1",
        "row_count": len(all_rows),
        "source_degrees": {str(label): degree for label, degree, _ in source},
        "target": sorted(target),
        "target_degree": target_degree,
        "type": "header",
        "variables": [str(value) for value in M.PARAMETERS]+["t"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    digest = sha256()
    with args.output.open("w") as stream:
        line = json.dumps(header, sort_keys=True, separators=(",", ":"))
        stream.write(line+"\n")
        digest.update((line+"\n").encode("ascii"))
        for index, (_, _, source_position, multiplier, label, terms) in enumerate(columns):
            entries = []
            for monomial, value in terms:
                output = tuple(a+b for a, b in zip(monomial, multiplier))
                entries.append([row_index[output], value])
            record = {
                "entries": sorted(entries),
                "index": index,
                "multiplier": list(multiplier),
                "source_label": label,
                "source_position": source_position,
                "type": "column",
            }
            line = json.dumps(record, sort_keys=True, separators=(",", ":"))
            stream.write(line+"\n")
            digest.update((line+"\n").encode("ascii"))
    print("TP N5 homogeneous Macaulay export: PASS")
    print("degree / rows / columns / target:", args.degree, len(all_rows),
          len(columns), len(target_terms))
    print("source degrees:", [(label, degree, len(terms))
                              for label, degree, terms in source])
    print("sha256:", digest.hexdigest())
    print("elapsed_seconds:", time.monotonic()-started)


if __name__ == "__main__":
    main()
