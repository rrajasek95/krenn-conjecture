#!/usr/bin/env python3
"""Exact Cramer determinant for the branch-0 k4-cycle upper packet."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_upper_cramer.json"
SOURCE = HERE / "probe_branch0_cycle_interior.py"
N = 12
TARGETS = (1, 2, 3, 4)  # a1,a2,a3,a4 in the gauge-fixed source ring.


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SOURCE_MODULE = load("n8_cycle_upper_cramer_source", SOURCE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {key: Fraction(value) for key, value in poly.items() if value}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, scalar):
    return clean({key: Fraction(scalar) * value for key, value in poly.items()})


def multiply(*polys):
    answer = {(0,) * N: Fraction(1)}
    for poly in polys:
        updated = Counter()
        for left, lc in answer.items():
            for right, rc in poly.items():
                updated[tuple(a + b for a, b in zip(left, right))] += lc * rc
        answer = clean(updated)
    return answer


def variable(index, power=1, coefficient=1):
    exponent = [0] * N
    exponent[index] = power
    return {tuple(exponent): Fraction(coefficient)}


def linear_parts(poly):
    coefficients = [Counter() for _ in TARGETS]
    constant = Counter()
    for exponent, scalar in poly.items():
        target_degree = sum(exponent[target] for target in TARGETS)
        require(target_degree <= 1, "an upper row ceased to be linear")
        if not target_degree:
            constant[exponent] += scalar
            continue
        target = next(target for target in TARGETS if exponent[target])
        require(exponent[target] == 1,
                "an upper target occurred with nonunit exponent")
        reduced = list(exponent)
        reduced[target] = 0
        coefficients[TARGETS.index(target)][tuple(reduced)] += scalar
    return tuple(clean(value) for value in coefficients), clean(constant)


def parity(permutation):
    inversions = sum(permutation[left] > permutation[right]
                     for left in range(len(permutation))
                     for right in range(left + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def determinant(matrix):
    answer = {}
    for permutation in permutations(range(len(matrix))):
        answer = add(answer, scale(multiply(*(
            matrix[row][permutation[row]] for row in range(len(matrix)))),
            parity(permutation)))
    return answer


def encode(poly):
    return [[list(exponent), coefficient.numerator, coefficient.denominator]
            for exponent, coefficient in sorted(poly.items())]


def main():
    rows, _ = SOURCE_MODULE.data()
    row_map = {label: poly for label, poly, _ in rows}
    labels = tuple(f"cofactor_{edge}_0" for edge in (1, 2, 3, 4))
    parts = tuple(linear_parts(row_map[label]) for label in labels)
    matrix = tuple(row[0] for row in parts)
    determinant_value = determinant(matrix)

    b0, b1, b3 = (variable(index) for index in (6, 7, 8))
    d1, d3, d4 = (variable(index) for index in (9, 10, 11))
    delta = add(multiply(b1, d3), multiply(b3, d1, d4))
    expected = multiply(scale(multiply(b0, b0, b1, b3, d1, d3, d4), 4),
                        delta, delta)
    require(determinant_value == expected,
            "the upper Cramer determinant factorization changed")

    zero_pattern = tuple(tuple(bool(entry) for entry in row) for row in matrix)
    require(zero_pattern == ((False, True, False, True),
                             (True, False, True, False),
                             (False, True, False, True),
                             (True, False, True, False)),
            "the two 2x2 upper blocks changed")

    # A sign mutation in the first nonzero matrix coefficient must break the
    # exact determinant factorization.
    mutated = [list(row) for row in matrix]
    mutated[0][1] = scale(mutated[0][1], -1)
    require(determinant(tuple(tuple(row) for row in mutated)) != expected,
            "the determinant sign mutation did not fire")

    result = {
        "status": "UNAUDITED exact branch-0 cycle Cramer determinant",
        "gauge": ["b2=1", "b4=1", "b5=1", "d2=1"],
        "upper_source_rows": list(labels),
        "target_variables": ["a1", "a2", "a3", "a4"],
        "coefficient_zero_pattern": [list(row) for row in zero_pattern],
        "determinant_factorization": (
            "4*b0^2*b1*b3*d1*d3*d4*(b1*d3+b3*d1*d4)^2"
        ),
        "delta": "b1*d3+b3*d1*d4",
        "determinant_term_count": len(determinant_value),
        "delta_squared_expansion": encode(expected),
        "scope": (
            "All monomial factors outside Delta are live on the corrected "
            "interior chart. Thus Delta!=0 is the unique generic Cramer "
            "branch and Delta=0 is the exact exceptional branch. This audit "
            "does not decide either branch."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 cycle upper Cramer determinant: PASS")
    print("zero pattern:", zero_pattern)
    print("determinant terms:", len(determinant_value))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
