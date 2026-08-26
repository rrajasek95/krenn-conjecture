#!/usr/bin/env python3
"""A three-row unit certificate on the cloned diagonal superpair ansatz."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
             "audit_dangerous_charts.py")
OUT = HERE / "results_pairconstant_plus_breaker_block_ansatz.json"
Q = Fraction
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
WORDS = {
    "pairconstant": tuple(map(int, "00001122")),
    "breaker_ad": tuple(map(int, "01010101")),
    "breaker_bc": tuple(map(int, "01101001")),
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_module("n8_pc_breaker_base", BASE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(left, right):
    answer = Counter(left)
    answer.update(right)
    return Counter({monomial: coefficient for monomial, coefficient in answer.items()
                    if coefficient})


def scale(poly, scalar):
    return Counter({monomial: scalar * coefficient
                    for monomial, coefficient in poly.items()
                    if scalar * coefficient})


def multiply(left, right):
    answer = Counter()
    for le, lc in left.items():
        for re, rc in right.items():
            answer[tuple(le[index] + re[index] for index in range(4))] += lc * rc
    return Counter({monomial: coefficient for monomial, coefficient in answer.items()
                    if coefficient})


ONE = Counter({(0, 0, 0, 0): Q(1)})
A = Counter({(1, 0, 0, 0): Q(1)})
B = Counter({(0, 1, 0, 0): Q(1)})
C = Counter({(0, 0, 1, 0): Q(1)})
D = Counter({(0, 0, 0, 1): Q(1)})


def word_polynomial(word):
    """Raw 105-PM replay after imposing the cloned diagonal ansatz."""
    answer = Counter()
    for matching in BASE.PM8:
        exponent = [0, 0, 0, 0]
        live = True
        for u, v in matching:
            if word[u] != word[v]:
                live = False
                break
            if u // 2 == v // 2:
                # Normalized same-colour M0 anchor equals one.
                continue
            require(u // 2 < v // 2,
                    "cross-superpair edge orientation changed")
            exponent[2 * (u % 2) + (v % 2)] += 1
        if live:
            answer[tuple(exponent)] += 1
    return answer


def evaluate(poly, point):
    return sum(coefficient
               * point[0] ** exponent[0]
               * point[1] ** exponent[1]
               * point[2] ** exponent[2]
               * point[3] ** exponent[3]
               for exponent, coefficient in poly.items())


def main():
    x = multiply(A, D)
    y = multiply(B, C)
    e = add(ONE, add(x, y))
    g1 = scale(multiply(x, x), Q(9))
    g2 = multiply(add(x, scale(y, Q(2))),
                  add(x, scale(y, Q(2))))

    literal = {name: word_polynomial(word) for name, word in WORDS.items()}
    require(literal["pairconstant"] == e,
            "00001122 did not replay to 1+ad+bc")
    require(literal["breaker_ad"] == g1,
            "01010101 did not replay to 9(ad)^2")
    require(literal["breaker_bc"] == g2,
            "01101001 did not replay to (ad+2bc)^2")

    # In Q[a,b,c,d], with E=1+x+y:
    # 1=(x+3)G1/36 -(x-1)G2/4 -(x-1)E(x+2-E).
    x_plus_3 = add(x, scale(ONE, Q(3)))
    x_minus_1 = add(x, scale(ONE, Q(-1)))
    x_plus_2_minus_e = add(add(x, scale(ONE, Q(2))), scale(e, Q(-1)))
    certificate = add(
        scale(multiply(x_plus_3, g1), Q(1, 36)),
        add(scale(multiply(x_minus_1, g2), Q(-1, 4)),
            scale(multiply(multiply(x_minus_1, e), x_plus_2_minus_e), Q(-1)))
    )
    require(certificate == ONE,
            "three-row Nullstellensatz certificate has nonconstant residual")

    # Positive control: the previously frozen rational 78-zero is killed by
    # the first breaker row.
    witness = (Q(1), Q(-2, 3), Q(0), Q(-1))
    witness_values = {name: evaluate(poly, witness)
                      for name, poly in literal.items()}
    require(witness_values["pairconstant"] == 0
            and witness_values["breaker_ad"] == 9,
            "rational 78-zero breaker control changed")
    hostile = add(g2, ONE)
    hostile_certificate = add(
        scale(multiply(x_plus_3, g1), Q(1, 36)),
        add(scale(multiply(x_minus_1, hostile), Q(-1, 4)),
            scale(multiply(multiply(x_minus_1, e), x_plus_2_minus_e), Q(-1)))
    )
    require(hostile_certificate != ONE,
            "G2 constant mutation did not fire")

    def terms(poly):
        return [{"exponents_abcd": list(exponent),
                 "coefficient": [coefficient.numerator, coefficient.denominator]}
                for exponent, coefficient in sorted(poly.items())]

    result = {
        "status": "UNAUDITED exact block-ansatz three-row unit certificate",
        "ansatz": (
            "The twelve same-colour M0 anchors are one; cross-colour cells "
            "are zero; every same-colour cross-supervertex clone block is "
            "the same M=[[a,b],[c,d]]."
        ),
        "pairconstant_word": "00001122",
        "pairconstant_polynomial": "E=1+ad+bc",
        "breaker_words": ["01010101", "01101001"],
        "breaker_polynomials": ["G1=9(ad)^2", "G2=(ad+2bc)^2"],
        "smallest_breaker_orbit_representative": "01010101",
        "literal_polynomials": {name: terms(poly)
                                for name, poly in literal.items()},
        "certificate": (
            "1=(ad+3)G1/36 -(ad-1)G2/4 "
            "-(ad-1)E(ad+2-E)"
        ),
        "certificate_residual_terms": terms(add(certificate, scale(ONE, -1))),
        "rational_78_zero_abcd": [[value.numerator, value.denominator]
                                  for value in witness],
        "rational_78_zero_row_values": {
            name: [value.numerator, value.denominator]
            for name, value in witness_values.items()
        },
        "conclusion": (
            "On this four-parameter normalized superpair ansatz, one of the "
            "78 pair-constant rows plus two rows from the smallest breaker "
            "orbit generate the unit ideal over Q. Thus adding the smallest "
            "breaker orbit not only removes the known rational witness; it "
            "leaves no point at all on the ansatz."
        ),
        "scope": (
            "This is an exact ansatz theorem, not a result for arbitrary "
            "normalized orbit0 blocks. It relies on cross-colour zero and "
            "one cloned 2x2 matrix across all six supervertex pairs."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("pairconstant + smallest-breaker block ansatz: PASS")
    print("rows:", WORDS)
    print("rational witness E/G1/G2:", witness_values)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
