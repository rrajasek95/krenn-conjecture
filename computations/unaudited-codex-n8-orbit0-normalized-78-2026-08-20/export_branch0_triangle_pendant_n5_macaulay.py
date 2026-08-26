#!/usr/bin/env python3
"""Stream the bounded exact-Q Macaulay interface for N5^3.

The output is one JSON object per line and is accepted by the existing
`anchor-k-echelon` modular discovery solver.  Rows are all monomials of total
degree at most D in (b0,b1,b3,d4,d5); columns are m*R for each transported
source row R and every multiplier m with deg(m)+deg(R)<=D.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from math import comb
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
DISCOVERY = HERE / "discover_branch0_triangle_pendant_reduction.py"


def load():
    spec = importlib.util.spec_from_file_location("n8_tp_discovery", DISCOVERY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D = load()
C = D.CHART
ACTIVE = (6, 7, 9, C.d_index[4], C.d_index[5])


def compositions(total, length, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for value in range(total, -1, -1):
        yield from compositions(total - value, length - 1, prefix + (value,))


def monomials_upto(degree):
    for total in range(degree + 1):
        yield from compositions(total, len(ACTIVE))


def restrict_exponent(exponent):
    if any(exponent[index] for index in range(C.n) if index not in ACTIVE):
        raise RuntimeError(("polynomial escaped active variables", exponent))
    return tuple(exponent[index] for index in ACTIVE)


def triples(poly, row_index, shift=None):
    answer = []
    shift = shift or (0,) * len(ACTIVE)
    for exponent, coefficient in poly.items():
        active = restrict_exponent(exponent)
        shifted = tuple(active[index] + shift[index]
                        for index in range(len(ACTIVE)))
        answer.append([row_index[shifted], coefficient.numerator,
                       coefficient.denominator])
    answer.sort()
    return answer


def integer_pairs(poly, row_index, shift=None):
    """Clear a column's denominators for the integer-entry Rust interface."""
    scale = 1
    for coefficient in poly.values():
        scale = scale * coefficient.denominator // gcd(
            scale, coefficient.denominator)
    rational = triples(poly, row_index, shift)
    return [[row, numerator * (scale // denominator)]
            for row, numerator, denominator in rational], scale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.degree < 24:
        raise RuntimeError("N5^3 has degree 24; smaller cutoffs are impossible")

    data = D.cramer_branch_system(7, 12)
    rows = [(label, poly, max(sum(exponent) for exponent in poly))
            for label, poly in data["open_rows"]]
    exponents = list(monomials_upto(args.degree))
    row_index = {exponent: index for index, exponent in enumerate(exponents)}
    if len(exponents) != comb(args.degree + 5, 5):
        raise RuntimeError("monomial census changed")
    column_count = sum(comb(args.degree - degree + 5, 5)
                       for _, _, degree in rows)
    target = C.multiply(data["numerator_a5"], data["numerator_a5"],
                        data["numerator_a5"])
    row_digest = sha256(json.dumps(exponents, separators=(",", ":")).encode(
        "ascii")).hexdigest()
    header = {
        "type": "header",
        "format": "n8-branch0-tp-N5-cube-macaulay-v1",
        "degree_cutoff": args.degree,
        "variables": ["b0", "b1", "b3", "d4", "d5"],
        "row_count": len(exponents),
        "column_count": column_count,
        "target": triples(target, row_index),
        "row_exponents_sha256": row_digest,
        "logical_scope": (
            "Exact rational matrix; modular membership is discovery until a "
            "selected solution is replayed over Q"
        ),
    }
    with args.out.open("w") as stream:
        stream.write(json.dumps(header, sort_keys=True, separators=(",", ":")) + "\n")
        column = 0
        # Sparse rows first tends to reduce fill in the common-echelon engine.
        for label, poly, degree in sorted(rows, key=lambda item: (len(item[1]), item[0])):
            for multiplier in monomials_upto(args.degree - degree):
                entries, column_scale = integer_pairs(
                    poly, row_index, multiplier)
                record = {
                    "type": "column",
                    "index": column,
                    "entries": entries,
                    "source_label": label,
                    "multiplier_exponent": list(multiplier),
                    "rational_column_scale": column_scale,
                }
                stream.write(json.dumps(record, sort_keys=True,
                                        separators=(",", ":")) + "\n")
                column += 1
    if column != column_count:
        raise RuntimeError(("column census changed", column, column_count))
    print("TP N5^3 Macaulay export: PASS")
    print("degree / rows / columns:", args.degree, len(exponents), column_count)
    print("row exponent sha256:", row_digest)
    print("output:", args.out)


if __name__ == "__main__":
    main()
