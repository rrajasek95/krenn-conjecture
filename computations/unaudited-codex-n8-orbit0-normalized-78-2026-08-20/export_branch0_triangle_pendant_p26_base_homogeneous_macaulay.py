#!/usr/bin/env python3
"""Export a bounded homogeneous Macaulay component for the TP P26 core.

The nine exact generators are the eight frozen source rows
7,8,9,10,12,15,19,101 and the expanded Rabinowitsch equation for
F0=b0*b1*b3*d4*d5*(b1*d4+b0*d5).  Each generator is homogenized separately
with t.  At degree D, the target is t^D and columns are every homogeneous
degree-D multiple of a generator.

The JSONL matrix is exact over Q (in fact integral), but a modular solve is
discovery only until an exact selected-column replay is supplied.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import comb
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_triangle_pendant_p26_boundary_msolve.py"
CORE_LABELS = (7, 8, 9, 10, 12, 15, 19, 101)
AFFINE_NAMES = ("z", "a4", "a5", "b0", "b1", "b3", "d4", "d5")
HOMOGENEOUS_NAMES = (*AFFINE_NAMES, "t")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load(EXPORTER, "n8_tp_p26_exporter_homogeneous")
D = E.D
C = E.C
C_INDICES = tuple(C.names.index(name) for name in AFFINE_NAMES[1:])


def compositions(total: int, length: int, prefix=()):
    if length == 1:
        yield prefix + (total,)
        return
    for value in range(total, -1, -1):
        yield from compositions(total - value, length - 1,
                                prefix + (value,))


def affine_source(poly) -> dict[tuple[int, ...], int]:
    poly = E.primitive_integer(poly)
    answer = {}
    for exponent, coefficient in poly.items():
        if coefficient.denominator != 1:
            raise RuntimeError("primitive source row is not integral")
        if any(exponent[index] for index in range(C.n)
               if index not in C_INDICES):
            raise RuntimeError(("row escaped active variables", exponent))
        key = (0, *(exponent[index] for index in C_INDICES))
        answer[key] = int(coefficient)
    return answer


def affine_rabinowitsch(base) -> dict[tuple[int, ...], int]:
    base = E.primitive_integer(base)
    answer = {(0,) * len(AFFINE_NAMES): -1}
    for exponent, coefficient in base.items():
        if coefficient.denominator != 1:
            raise RuntimeError("base factor is not integral")
        if any(exponent[index] for index in range(C.n)
               if index not in C_INDICES):
            raise RuntimeError(("base escaped active variables", exponent))
        key = (1, *(exponent[index] for index in C_INDICES))
        answer[key] = int(coefficient)
    return answer


def homogenize(poly: dict[tuple[int, ...], int]):
    degree = max(sum(exponent) for exponent in poly)
    value = {(exponent + (degree - sum(exponent),)): coefficient
             for exponent, coefficient in poly.items()}
    if any(sum(exponent) != degree for exponent in value):
        raise RuntimeError("homogenization failed")
    return value, degree


def generators():
    data = D.cramer_branch_system(7, 12)
    rows = {label: poly for label, poly in data["closed_rows"]}
    answer = []
    for label in CORE_LABELS:
        poly, degree = homogenize(affine_source(rows[label]))
        answer.append((f"source_{label}", poly, degree))
    poly, degree = homogenize(affine_rabinowitsch(
        data["closed_live_factors"][0]))
    answer.append(("rabinowitsch_F0", poly, degree))
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    gens = generators()
    if args.degree < max(degree for _, _, degree in gens):
        raise SystemExit("degree lies below a generator degree")
    row_exponents = list(compositions(args.degree, len(HOMOGENEOUS_NAMES)))
    row_index = {exponent: index for index, exponent in enumerate(row_exponents)}
    if len(row_exponents) != comb(args.degree + 8, 8):
        raise RuntimeError("row census changed")
    column_count = sum(comb(args.degree - degree + 8, 8)
                       for _, _, degree in gens)
    target_exponent = (0,) * 8 + (args.degree,)
    header = {
        "type": "header",
        "format": "n8-tp-p26-base-homogeneous-macaulay-v1",
        "degree": args.degree,
        "variables": list(HOMOGENEOUS_NAMES),
        "row_count": len(row_exponents),
        "column_count": column_count,
        "target": [[row_index[target_exponent], 1, 1]],
        "generator_degrees": {label: degree for label, _, degree in gens},
        "source_labels": [label for label, _, _ in gens],
        "row_exponents_sha256": sha256(json.dumps(
            row_exponents, separators=(",", ":")).encode()).hexdigest(),
        "logical_scope": (
            "Exact homogeneous degree component over Q; modular membership "
            "is discovery until exact replay"
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as stream:
        stream.write(json.dumps(header, sort_keys=True,
                                separators=(",", ":")) + "\n")
        column = 0
        for label, poly, degree in sorted(
                gens, key=lambda item: (len(item[1]), item[0])):
            for multiplier in compositions(args.degree - degree,
                                           len(HOMOGENEOUS_NAMES)):
                entries = []
                for exponent, coefficient in poly.items():
                    shifted = tuple(a + b for a, b in zip(
                        exponent, multiplier, strict=True))
                    entries.append([row_index[shifted], coefficient])
                entries.sort()
                record = {
                    "type": "column", "index": column,
                    "entries": entries, "source_label": label,
                    "multiplier_exponent": list(multiplier),
                    "rational_column_scale": 1,
                }
                stream.write(json.dumps(record, sort_keys=True,
                                        separators=(",", ":")) + "\n")
                column += 1
    if column != column_count:
        raise RuntimeError((column, column_count))
    print("TP P26 base homogeneous Macaulay export: PASS")
    print("degree / rows / columns:", args.degree, len(row_exponents),
          column_count)
    print("generator degrees:", header["generator_degrees"])
    print("row exponent sha256:", header["row_exponents_sha256"])
    print("output sha256:", sha256(args.out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
